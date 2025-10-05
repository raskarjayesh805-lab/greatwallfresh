const chatContainer = document.getElementById('chat');
const userInput = document.getElementById('userInput');

function addMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = message;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    addMessage(message, 'user');
    userInput.value = '';

    const typingIndicator = document.createElement('div');
    typingIndicator.classList.add('message', 'bot');
    typingIndicator.textContent = '💬 ...';
    chatContainer.appendChild(typingIndicator);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message, user_id: 'default' })
        });
        const data = await response.json();
        typingIndicator.remove();
        addMessage(data.response, 'bot');
    } catch (error) {
        typingIndicator.remove();
        addMessage('⚠️ Error connecting to server.', 'bot');
    }
}

userInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') sendMessage();
});
