import boto3
import time
import json

# s3 = boto3.client("s3")
# client = boto3.client("transcribe")

# bucket_name = "glexiaweb"
# file_name = "Alice2.mp3"

# Upload Files to S3

# with open("Alice2.mp3", "rb") as data:
#     s3.Bucket(bucket_name).put_object(Key="TranscribeTest/Alice2.mp3", Body=data)


#  Transcribe uploaded file

# response = client.start_transcription_job(
#     TranscriptionJobName="sttt1",  #
#     LanguageCode="en-IN",
#     MediaFormat="mp3",
#     Media={"MediaFileUri": "s3://glexiaweb/TranscribeTest/Alice2.mp3"},
#     OutputBucketName="glexiaweb",
#     OutputKey="TranscribeTest/Alice2.json",
# )

# Download the transcribed json file
# s3.download_file(bucket_name, "TranscribeTest/Alice2.json", "./alice.json")


# Read the json file
with open("alice.json") as f:
    data = json.load(f)


text = data["results"]["transcripts"][0]["transcript"]
print(text)
