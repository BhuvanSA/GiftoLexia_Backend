import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve
import uuid
import requests
import time
import psycopg2


# Local Scripts
from compare import StringComparator
from validator import ResponseValidator
from modules import eval_survey

Storage = []


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

expectedTranscription = """
Once upon a time, there was a little girl named Alice who lived in a small town. 
One day, Alice was walking in the woods when she came across a strange hole in the ground. 
Alice was curious, so she decided to climb down the hole. When she reached the bottom,
Alice found herself in a strange and wonderful world called wonderland.
"""
actualTranscription = "Your transcipt goes here"
cal = "Error Rate:"


@app.route("/", methods=["GET"])
def get_transcription():
    return jsonify({
        "expected": expectedTranscription,
        "actual": actualTranscription,
        "calculate": cal
    })


@app.route("/record", methods=["POST"])
def record():
    # Check if the POST request contains the audio file
    # print(request.files["file"])
    if "audio_data" not in request.files:
        return jsonify({"message": "No audio file found"}), 400

    audio_file = request.files["audio_data"]

    # Save the audio file to the server
    if audio_file:
        filename = "recording.mp3"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        audio_file.save(file_path)
        return jsonify({"message": "Audio saved successfully", "filename": filename})


@app.route("/transcribe", methods=["POST"])
def transcribe():
    base_url = "https://api.assemblyai.com/v2"
    headers = {"authorization": "4d4a6f271c0f4f3da6716441e49f72ec"}

    with open("./uploads/recording.mp3", "rb") as f:
        response = requests.post(base_url + "/upload", headers=headers, data=f)

    upload_url = response.json()["upload_url"]

    data = {
        "audio_url": upload_url  # You can also use a URL to an audio or video file on the web
    }

    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=headers)

    transcript_id = response.json()["id"]
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    while True:
        transcription_result = requests.get(
            polling_endpoint, headers=headers).json()

        if transcription_result["status"] == "completed":
            break
        elif transcription_result["status"] == "error":
            return jsonify({"message": f"Transcription failed: {transcription_result['error']}"}), 500
        else:
            time.sleep(3)

    global actualTranscription
    actualTranscription = transcription_result["text"]
    return jsonify({"message": "Transcription completed successfully", "actual_transcription": actualTranscription})


@app.route("/check", methods=["GET"])
def check():
    global actualTranscription
    return jsonify({"actual_transcription": actualTranscription})


@app.route("/calculate", methods=["GET"])
def calculate():
    expected_transcription = expectedTranscription.lower()
    actual_transcription = actualTranscription.lower()

    comparator = StringComparator(expected_transcription, actual_transcription)

    error_rate = comparator.calculate_error_rate()
    misspelled_words = comparator.find_misspelled_words()

    global cal
    cal = f"Error Rate: {error_rate:.2f}% | Misspelled Words: {misspelled_words}"

    return jsonify({"expected": expectedTranscription, "actual": actualTranscription, "calculate": cal})


@app.route("/submitEntryForm", methods=["POST"])
def submitEntryForm():
    response = request.get_json()
    validator = ResponseValidator(response)
    if validator.validate():
        response['id'] = uuid.uuid4().hex
        # Add to DB Here
        time.sleep(1)
        return jsonify({"Validation": "True", "id": f"{response['id']}"}), 200
    else:
        return jsonify({"Validation": "False"}), 400

    # Storage.append(response)
    # return response['id']

# Fetch and return the right json file


@app.route("/survey/<lang_code>/<age_grp>", methods=['GET'])
def get_survey_json(lang_code, age_grp):
    # print("hit", lang_code, age_grp)
    json_txt = None
    json_path = "./assets/"
    filename = f"survey/{lang_code}/{age_grp}.json"
    full_path = os.path.join(json_path, filename)
    # print(f"Retrieving survey questions: {full_path}")
    try:
        # try to open the file
        assert os.path.isfile(
            full_path), f"Requested json file {full_path} not found"

        with open(full_path) as f:
            return f.read(), 200

        # print(json_txt)
        # print(type(json_txt))
    except AssertionError as ae:
        print(ae)
        return json_txt, 404

    except Exception as e:
        print(f"Error:{e}")
        return json_txt, 404


# POST Survey answers - calculate and return score + recommendation


@app.route("/survey",  methods=['POST'])
def eval_survey_answers():
    data = request.get_json()
    threshold = 70
    print(data)
    agegroup = data['age_group']
    num_responses = len(data["selectedOptions"])
    best_score = num_responses * 1
    worst_score = num_responses * 5

    threshold = worst_score * 0.70
    print(f"{num_responses} responses from {agegroup} agegroup. Threshold: {threshold}")

    if agegroup == "3-5":
        result = eval_survey.eval_agegroup1(data, threshold)
    if agegroup == "5-8":
        result = eval_survey.eval_agegroup2(data, threshold)
    if agegroup == "8-12":
        result = eval_survey.eval_agegroup3(data, threshold)

    print(f"Score:{result}")

    user_msg = eval_survey.get_eval_message(data, result)
    result["msg"] = user_msg

    print("sadfsadfasdfasdfasdfasdf", result)

    # Connect to database to enter the values
    db_params = {
        "dbname": "giftolexia-postgres",
        "user": "bhuvansa",
        "password": "giftolexia",
        "host": "127.0.0.1",
        "port": "5432"
    }

    # Data to be inserted
    dbdata = {
        'selectedOptions': data['selectedOptions'],
        'age_group': data['age_group'],
        'child_name': data['child_name'],
        'language': data['language'],
        'email': data['email'],
        'score': result['score'],
        'action': 'ok',
        'msg': result["msg"]
    }

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        print("worked")

        # Create a cursor object
        cursor = conn.cursor()

        # Execute the SQL statement to create the table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id SERIAL PRIMARY KEY,
                child_name TEXT,
                language TEXT,
                age_group TEXT,
                email TEXT,
                msg TEXT,
                score INTEGER
            )
        """)

        # Insert data into the user_data table
        cursor.execute(
            "INSERT INTO user_data (child_name, language, age_group, email, msg, score) VALUES (%s, %s, %s, %s, %s, %s)",
            (dbdata['child_name'], dbdata['language'],
             dbdata['age_group'], dbdata['email'], dbdata['msg'], dbdata['score'])
        )

        # Commit the transaction
        cursor.close()
        conn.commit()
        conn.close()

        print("Data inserted successfully!")

    except Exception as e:
        print(f"Error: {e}")

    return jsonify(result)


if __name__ == "__main__":
    app.run()
