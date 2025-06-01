function toggleChat() {
  const overlay = document.getElementById('chatOverlay');
  overlay.style.display = overlay.style.display === 'none' ? 'flex' : 'none';
}

function sendChat() {
  const input = document.getElementById('chatInput');
  const message = input.value.trim();
  if (!message) return;

  const chatBox = document.getElementById('chatMessages');
  const userMsg = document.createElement('p');
  userMsg.textContent = "Ти: " + message;
  chatBox.appendChild(userMsg);
  input.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;

  fetch('/chat/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken()
    },
    body: JSON.stringify({ message: message })
  })
    .then(response => response.json())
    .then(data => {
      const reply = document.createElement('p');
      reply.textContent = "FYRE: " + (data.reply || "We'll get back to you shortly!");
      chatBox.appendChild(reply);
      chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(() => {
      const reply = document.createElement('p');
      reply.textContent = "FYRE: Възникна грешка при изпращането на съобщението.";
      chatBox.appendChild(reply);
      chatBox.scrollTop = chatBox.scrollHeight;
    });
}

function getCSRFToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name + '=')) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return '';
}

document.addEventListener('click', function (event) {
  const overlay = document.getElementById('chatOverlay');
  const chatBox = document.getElementById('chatBox');
  if (
    overlay.style.display !== 'none' &&
    !chatBox.contains(event.target) &&
    !event.target.closest('[onclick="toggleChat()"]')
  ) {
    overlay.style.display = 'none';
  }
});

document.addEventListener('keydown', function (event) {
  const overlay = document.getElementById('chatOverlay');
  if (event.key === 'Escape' && overlay.style.display !== 'none') {
    overlay.style.display = 'none';
  }
});

const input = document.getElementById('chatInput');
input.addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    sendChat();
  }
});