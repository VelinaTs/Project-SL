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
    userMsg.textContent = "You: " + message;
    chatBox.appendChild(userMsg);
    input.value = "";

    setTimeout(() => {
      const reply = document.createElement('p');
      reply.textContent = "Barber Bot: We'll get back to you shortly!";
      chatBox.appendChild(reply);
      chatBox.scrollTop = chatBox.scrollHeight;
    }, 1000);
  }