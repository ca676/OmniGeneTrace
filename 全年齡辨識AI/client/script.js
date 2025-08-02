const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const output = document.getElementById("output");
const socket = new WebSocket("ws://localhost:8000/ws");

navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
    video.srcObject = stream;
    video.play();
});

setInterval(() => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL("image/jpeg").split(",")[1];
    socket.send(imageData);
}, 100);

socket.onmessage = (event) => {
    output.src = "data:image/jpeg;base64," + event.data;
};
