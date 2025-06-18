console.log("Чат загружен");

const socket = new WebSocket("ws://localhost:8000/ws");

socket.onopen = () => {
  console.log("WebSocket подключён");
};

socket.onmessage = (event) => {
  console.log("Ответ от сервера:", event.data);
  appendMessage(event.data, "bot");
};

socket.onerror = (e) => {
  console.error("WebSocket ошибка:", e);
};

window.sendMessage = function () {
  const input = document.getElementById("input");
  const message = input.value;
  if (message.trim() === "") return;

  appendMessage(message, "user");
  socket.send(message);
  input.value = "";
};

document.getElementById("input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});

function appendMessage(text, sender) {
  const chat = document.getElementById("chat");
  const messageDiv = document.createElement("div");
  messageDiv.className = sender;
  messageDiv.textContent = text;
  chat.appendChild(messageDiv);
  chat.scrollTop = chat.scrollHeight;
}
