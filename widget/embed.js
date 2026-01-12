/**
 * Rasa Chatbot Widget - Embed Script
 * Tek satırlık script ile sitenize chatbot ekleyin
 *
 * Kullanım:
 * <script src="https://your-domain.com/embed.js" data-rasa-url="https://your-rasa-api.com"></script>
 */

(function() {
    'use strict';

    // Konfigürasyon - script tag'den al
    const currentScript = document.currentScript || document.querySelector('script[src*="embed.js"]');
    const config = {
        rasaUrl: currentScript.getAttribute('data-rasa-url') || 'http://localhost:5005',
        widgetTitle: currentScript.getAttribute('data-widget-title') || 'Alışveriş Asistanı',
        primaryColor: currentScript.getAttribute('data-primary-color') || '#667eea',
        secondaryColor: currentScript.getAttribute('data-secondary-color') || '#764ba2',
        position: currentScript.getAttribute('data-position') || 'right', // right or left
        greeting: currentScript.getAttribute('data-greeting') || 'Merhaba! Size nasıl yardımcı olabilirim?',
        avatar: currentScript.getAttribute('data-avatar') || '🤖',
        language: currentScript.getAttribute('data-language') || 'tr',
    };

    // Widget zaten yüklü mü kontrol et
    if (document.getElementById('rasa-chatbot-widget')) {
        console.warn('Rasa Chatbot Widget zaten yüklü');
        return;
    }

    // CSS inject et
    function injectCSS() {
        const css = `
            #rasa-chatbot-widget {
                position: fixed;
                ${config.position}: 20px;
                bottom: 20px;
                z-index: 999999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }

            #rasa-chat-button {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, ${config.primaryColor} 0%, ${config.secondaryColor} 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
                transition: all 0.3s ease;
                border: none;
            }

            #rasa-chat-button:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }

            #rasa-chat-button svg {
                width: 28px;
                height: 28px;
                fill: white;
            }

            #rasa-chat-window {
                display: none;
                position: absolute;
                bottom: 80px;
                ${config.position}: 0;
                width: 380px;
                height: 600px;
                background: white;
                border-radius: 16px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.15);
                flex-direction: column;
                overflow: hidden;
                animation: slideUp 0.3s ease;
            }

            @keyframes slideUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            #rasa-chat-header {
                background: linear-gradient(135deg, ${config.primaryColor} 0%, ${config.secondaryColor} 100%);
                color: white;
                padding: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            #rasa-chat-header h3 {
                margin: 0;
                font-size: 16px;
            }

            #rasa-close-btn {
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 18px;
            }

            #rasa-chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                background: #f9f9f9;
            }

            .rasa-message {
                display: flex;
                gap: 10px;
                margin-bottom: 16px;
                animation: fadeIn 0.3s ease;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .rasa-message-content {
                background: white;
                padding: 12px 16px;
                border-radius: 12px;
                max-width: 70%;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }

            .rasa-message-content p {
                margin: 0;
                line-height: 1.5;
                color: #333;
            }

            .rasa-user-message {
                flex-direction: row-reverse;
            }

            .rasa-user-message .rasa-message-content {
                background: linear-gradient(135deg, ${config.primaryColor} 0%, ${config.secondaryColor} 100%);
                color: white;
            }

            #rasa-typing {
                display: none;
            }

            .rasa-typing-dots {
                display: flex;
                gap: 4px;
                padding: 12px 16px;
                background: white;
                border-radius: 12px;
            }

            .rasa-typing-dots span {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: ${config.primaryColor};
                animation: typing 1.4s infinite;
            }

            .rasa-typing-dots span:nth-child(2) { animation-delay: 0.2s; }
            .rasa-typing-dots span:nth-child(3) { animation-delay: 0.4s; }

            @keyframes typing {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-10px); }
            }

            #rasa-chat-input-area {
                padding: 16px;
                background: white;
                border-top: 1px solid #eee;
                display: flex;
                gap: 10px;
            }

            #rasa-user-input {
                flex: 1;
                border: 1px solid #ddd;
                border-radius: 24px;
                padding: 12px 16px;
                font-size: 14px;
                outline: none;
            }

            #rasa-send-btn {
                width: 44px;
                height: 44px;
                border-radius: 50%;
                background: linear-gradient(135deg, ${config.primaryColor} 0%, ${config.secondaryColor} 100%);
                border: none;
                color: white;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            @media (max-width: 480px) {
                #rasa-chat-window {
                    width: calc(100vw - 40px);
                    height: calc(100vh - 100px);
                }
            }
        `;

        const style = document.createElement('style');
        style.textContent = css;
        document.head.appendChild(style);
    }

    // HTML inject et
    function injectHTML() {
        const html = `
            <div id="rasa-chatbot-widget">
                <button id="rasa-chat-button" aria-label="Open chat">
                    <svg viewBox="0 0 24 24">
                        <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
                    </svg>
                </button>
                <div id="rasa-chat-window">
                    <div id="rasa-chat-header">
                        <div>
                            <h3>${config.widgetTitle}</h3>
                            <small>● Çevrimiçi</small>
                        </div>
                        <button id="rasa-close-btn" aria-label="Close chat">✕</button>
                    </div>
                    <div id="rasa-chat-messages">
                        <div class="rasa-message">
                            <div>${config.avatar}</div>
                            <div class="rasa-message-content">
                                <p>${config.greeting}</p>
                            </div>
                        </div>
                    </div>
                    <div id="rasa-typing">
                        <div class="rasa-message">
                            <div>${config.avatar}</div>
                            <div class="rasa-typing-dots">
                                <span></span><span></span><span></span>
                            </div>
                        </div>
                    </div>
                    <div id="rasa-chat-input-area">
                        <input type="text" id="rasa-user-input" placeholder="Mesajınızı yazın..." />
                        <button id="rasa-send-btn" aria-label="Send message">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                                <path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;

        const div = document.createElement('div');
        div.innerHTML = html;
        document.body.appendChild(div.firstElementChild);
    }

    // Widget logic
    function initWidget() {
        const chatButton = document.getElementById('rasa-chat-button');
        const chatWindow = document.getElementById('rasa-chat-window');
        const closeBtn = document.getElementById('rasa-close-btn');
        const sendBtn = document.getElementById('rasa-send-btn');
        const userInput = document.getElementById('rasa-user-input');
        const messagesContainer = document.getElementById('rasa-chat-messages');
        const typingIndicator = document.getElementById('rasa-typing');

        let isOpen = false;
        const userId = 'user_' + Math.random().toString(36).substr(2, 9);

        // Toggle chat
        chatButton.addEventListener('click', () => {
            isOpen = !isOpen;
            chatWindow.style.display = isOpen ? 'flex' : 'none';
            if (isOpen) userInput.focus();
        });

        closeBtn.addEventListener('click', () => {
            isOpen = false;
            chatWindow.style.display = 'none';
        });

        // Send message
        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;

            // Add user message
            addMessage(message, 'user');
            userInput.value = '';

            // Show typing
            typingIndicator.style.display = 'block';
            scrollToBottom();

            try {
                const response = await fetch(\`\${config.rasaUrl}/webhooks/rest/webhook\`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ sender: userId, message })
                });

                const data = await response.json();

                typingIndicator.style.display = 'none';

                if (data && data.length > 0) {
                    data.forEach((msg, i) => {
                        setTimeout(() => addMessage(msg.text, 'bot'), i * 300);
                    });
                } else {
                    addMessage('Üzgünüm, cevap veremiyorum.', 'bot');
                }
            } catch (error) {
                typingIndicator.style.display = 'none';
                addMessage('⚠️ Bağlantı hatası. Lütfen daha sonra tekrar deneyin.', 'bot');
                console.error('Rasa error:', error);
            }
        }

        sendBtn.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });

        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = \`rasa-message \${sender === 'user' ? 'rasa-user-message' : ''}\`;
            messageDiv.innerHTML = \`
                <div>\${sender === 'user' ? '👤' : config.avatar}</div>
                <div class="rasa-message-content">
                    <p>\${text.replace(/\n/g, '<br>')}</p>
                </div>
            \`;
            messagesContainer.appendChild(messageDiv);
            scrollToBottom();
        }

        function scrollToBottom() {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    // DOM ready olunca çalıştır
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            injectCSS();
            injectHTML();
            initWidget();
        });
    } else {
        injectCSS();
        injectHTML();
        initWidget();
    }

    console.log('✅ Rasa Chatbot Widget yüklendi');
})();
