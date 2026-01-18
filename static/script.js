document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const attachBtn = document.getElementById('attach-btn');
    const uploadStatus = document.getElementById('upload-status');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const clearBtn = document.getElementById('clear-chat');
    const welcomeHero = document.getElementById('welcome-hero');

    let documentLoaded = false;

    // Handle File Selection
    attachBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleUpload(file);
    });

    async function handleUpload(file) {
        if (file.type !== 'application/pdf') {
            showIndicator('Please upload a PDF file ❌', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        showIndicator('Studying your document... 📖', 'processing');
        attachBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (response.ok) {
                showIndicator('Expertly indexed! ✅', 'success');
                documentLoaded = true;
                attachBtn.classList.add('active');
                attachBtn.classList.add('disabled');
                attachBtn.style.pointerEvents = 'none';
                attachBtn.style.opacity = '0.6';
                attachBtn.title = `Loaded: ${file.name}`;
                attachBtn.innerHTML = '<i class="fas fa-check"></i>';
                enableChat();

                // Hide Welcome Hero if it's there
                if (welcomeHero) welcomeHero.style.display = 'none';

                addBotMessage(`I've read "${file.name}". I'm ready to answer any questions about it.`);

                setTimeout(() => {
                    showIndicator('', '');
                    attachBtn.innerHTML = '<i class="fas fa-plus"></i>';
                }, 3000);
            } else {
                showIndicator(data.error || 'Upload failed ❌', 'error');
                attachBtn.innerHTML = '<i class="fas fa-plus"></i>';
            }
        } catch (error) {
            showIndicator('Network error occurred ❌', 'error');
            attachBtn.innerHTML = '<i class="fas fa-plus"></i>';
        }
    }

    function showIndicator(text, type) {
        uploadStatus.textContent = text;
        uploadStatus.style.opacity = text ? '1' : '0';
    }

    function enableChat() {
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.placeholder = "Ask or search for anything...";
        userInput.focus();
    }

    // Chat Logic
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    async function sendMessage() {
        const question = userInput.value.trim();
        if (!question || !documentLoaded) return;

        // Hide Welcome Hero on first message if not already hidden
        if (welcomeHero) welcomeHero.style.display = 'none';

        addUserMessage(question);
        userInput.value = '';

        // Add loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot loading-msg';
        loadingDiv.innerHTML = `
            <div class="message-label">AI Assistant</div>
            <div class="message-content"><i class="fas fa-circle-notch fa-spin"></i> Thinking...</div>
        `;
        chatMessages.appendChild(loadingDiv);
        scrollToBottom();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            });
            const data = await response.json();

            chatMessages.removeChild(loadingDiv);

            if (response.ok) {
                addBotMessage(data.response, data.sources);
            } else {
                addBotMessage(`Sorry, I encountered an error: ${data.error}`);
            }
        } catch (error) {
            if (chatMessages.contains(loadingDiv)) {
                chatMessages.removeChild(loadingDiv);
            }
            addBotMessage("Network error. Please try again.");
        }
    }

    function addUserMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message user';
        msgDiv.innerHTML = `
            <div class="message-label">YOU</div>
            <div class="message-content">${text}</div>
        `;
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function addBotMessage(text, sources = []) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message bot';

        let sourcesHtml = '';
        if (sources.length > 0) {
            sourcesHtml = `
                <div class="sources-container">
                    <p style="font-size: 0.75rem; font-weight: 600; color: #94a3b8; margin-bottom: 8px;">SOURCES</p>
                    ${sources.map((s, i) => `
                        <div class="source-item">
                            ${s.content.substring(0, 200)}...
                        </div>
                    `).join('')}
                </div>
            `;
        }

        msgDiv.innerHTML = `
            <div class="message-label">AI Assistant</div>
            <div class="message-content">
                <p>${text.replace(/\n/g, '<br>')}</p>
                ${sourcesHtml}
            </div>
        `;
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    clearBtn.addEventListener('click', () => {
        if (confirm("Start a new conversation?")) {
            location.reload(); // Simplest way to reset state
        }
    });
});
