const chatForm = document.getElementById('chat-form');
const chatWindow = document.getElementById('chat-window');
const messageInput = document.getElementById('message-input');
const newChatBtn = document.getElementById('new-chat-btn');
const userIdInput = document.getElementById('user-id');
const systemPromptInput = document.getElementById('system-prompt');
const temperatureInput = document.getElementById('temperature');
const tempValue = document.getElementById('temp-value');

let sessionId = null;

function appendMessage(role, content) {
  const msg = document.createElement('div');
  msg.className = `message ${role}`;
  msg.textContent = content;
  chatWindow.appendChild(msg);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

temperatureInput.addEventListener('input', () => {
  tempValue.textContent = temperatureInput.value;
});

newChatBtn.addEventListener('click', () => {
  sessionId = null;
  chatWindow.innerHTML = `<div class="welcome"><h2>New chat started</h2><p>Ask anything.</p></div>`;
});

chatForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const text = messageInput.value.trim();
  if (!text) return;

  appendMessage('user', text);
  messageInput.value = '';

  const loading = document.createElement('div');
  loading.className = 'message assistant';
  loading.textContent = 'Thinking...';
  chatWindow.appendChild(loading);

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userIdInput.value || 'web-user',
        session_id: sessionId,
        message: text,
        system_prompt: systemPromptInput.value,
        temperature: Number(temperatureInput.value),
      }),
    });

    const data = await response.json();
    sessionId = data.session_id;
    loading.remove();
    appendMessage('assistant', data.response || 'No response returned.');
  } catch (error) {
    loading.remove();
    appendMessage('assistant', 'Error talking to backend. Please try again.');
  }
});
