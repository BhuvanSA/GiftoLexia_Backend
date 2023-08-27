const audioChunks = [];
let mediaRecorder;

function startRecording() {
  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then(function (mediaStream) {
      mediaRecorder = new MediaRecorder(mediaStream);
      mediaRecorder.start();

      mediaRecorder.addEventListener("dataavailable", function (event) {
        audioChunks.push(event.data);
      });
    })
    .catch(function (err) {
      console.log(err);
    });
}

function stopRecording() {
  if (mediaRecorder) {
    mediaRecorder.stop();
  }
}

function uploadRecording() {
  if (audioChunks.length === 0) {
    console.log("No recording available.");
    return;
  }

  const blob = new Blob(audioChunks, { type: "audio/mp3" });
  const formData = new FormData();
  formData.append("audio_data", blob, "recording.mp3");

  fetch("/record", {
    method: "POST",
    body: formData,
  })
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
}
