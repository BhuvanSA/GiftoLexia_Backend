import os
from flask import Flask, render_template, request

import requests
import json
import time

from compare import StringComparator

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

expectedTranscription = "Once upon a time, there was a little girl named Alice who lived in a small town. One day, Alice was walking in the woods when she came across a strange hole in the ground. Alice was curious, so she decided to climb down the hole. When she reached the bottom, Alice found herself in a strange and wonderful world called wonderland."
actualTranscription = "Your transcipt goes here"
cal = "Error Rate:"


@app.route("/")
def index():
    # return render_template(
    #     "index.html",
    #     expected=expectedTranscription,
    #     actual="Your Transcript goes here",
    #     calculate=cal,
    # )

    return {
        "expected":expectedTranscription,
        "actual":"Your transcription Goes here",
        "calculate":cal,
    }


@app.route("/record", methods=["POST"])
def record():
    # Check if the POST request contains the audio file
    if "audio_data" not in request.files:
        return "No audio file found", 400

    audio_file = request.files["audio_data"]

    # Save the audio file to the server
    if audio_file:
        filename = "recording.mp3"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        audio_file.save(file_path)
        return "Audio saved successfully as " + filename


@app.route("/transcribe", methods=["GET"])
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
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result["status"] == "completed":
            break

        elif transcription_result["status"] == "error":
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)

    global actualTranscription
    actualTranscription = transcription_result["text"]
    return render_template(
        "index.html",
        expected=expectedTranscription,
        actual=actualTranscription,
        calculate=cal,
    )


@app.route("/check", methods=["GET"])
def check():
    global actualTranscription
    print(actualTranscription)
    return "okay"


@app.route("/calculate", methods=["GET"])
def calculate():
    expected_transcription = expectedTranscription.lower()
    actual_transcription = actualTranscription.lower()

    comparator = StringComparator(expected_transcription, actual_transcription)

    error_rate = comparator.calculate_error_rate()
    misspelled_words = comparator.find_misspelled_words()

    global cal
    cal = f"Error Rate: {error_rate:.2f}% | Misspelled Words: {misspelled_words}"

    return render_template(
        "index.html",
        expected=expectedTranscription,
        actual=actualTranscription,
        calculate=cal,
    )


if __name__ == "__main__":
    app.run()
