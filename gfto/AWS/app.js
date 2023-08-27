// eprem

const startButton = document.getElementById("start-button");
const stopButton = document.getElementById("stop-button");
const audioElement = document.getElementById("recorded-audio");
const submitButton = document.getElementById("submit-button");

let mediaRecorder;
let mediaStream;
let recordedChunks = [];

startButton.addEventListener("click", () => {
  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      mediaRecorder = new MediaRecorder(stream);
      mediaStream = stream;

      mediaRecorder.addEventListener("dataavailable", (e) => {
        recordedChunks.push(e.data);
      });

      mediaRecorder.addEventListener("stop", () => {
        const audioBlob = new Blob(recordedChunks, { type: "audio/mp3" });
        recordedChunks = [];

        const audioURL = URL.createObjectURL(audioBlob);
        audioElement.src = audioURL;
      });

      mediaRecorder.start();
    })
    .catch((error) => {
      console.error("Error accessing microphone:", error);
    });
});

stopButton.addEventListener("click", () => {
  mediaRecorder.stop();
  mediaStream.getTracks().forEach((track) => {
    track.stop();
  });
});

submitButton.addEventListener("click", () => {
  const audioBlob = new Blob(recordedChunks, { type: "audio/mp3" });
  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.mp3");

  fetch("/audio", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      // Handle the server response
    })
    .catch((error) => {
      console.error("Error uploading audio:", error);
    });
});
