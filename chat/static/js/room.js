const chatWindow = document.querySelector('.chat-window');
const closeBtn = document.querySelector('.close-btn');
const chatBody = document.querySelector('.chat-body');
const inputField = document.querySelector('input[type="text"]');
const sendBtn = document.getElementById('send-btn');

// Создаем объект WebSocket и устанавливаем соединение
const socket = new WebSocket('ws://localhost:8080');

// Обработчик события для кнопки "закрыть"
closeBtn.addEventListener('click', () => {
  chatWindow.style.display = 'none';
});

// Обработчик события для кнопки "отправить"
sendBtn.addEventListener('click', () => {
  const message = inputField.value;
  socket.send(message);
  inputField.value = '';
});

// Обработчик события для получения сообщения от сервера
socket.addEventListener('message', (event) => {
  const message = event.data;
  const chatMessage = document.createElement('div');
  chatMessage.textContent = message;
  chatBody.appendChild(chatMessage);
});