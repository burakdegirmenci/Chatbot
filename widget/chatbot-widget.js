/**
 * Rasa E-Ticaret Chatbot Widget
 * Rasa REST API ile iletişim kurar
 */

class ChatbotWidget {
    constructor() {
        // Konfigürasyon
        this.config = {
            rasaServerUrl: 'http://localhost:5005',
            userId: this.generateUserId(),
        };

        // DOM elementleri
        this.chatButton = document.getElementById('chat-button');
        this.chatWindow = document.getElementById('chat-window');
        this.chatMessages = document.getElementById('chat-messages');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.closeBtn = document.getElementById('close-btn');
        this.minimizeBtn = document.getElementById('minimize-btn');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.notificationBadge = document.querySelector('.notification-badge');
        this.quickReplies = document.querySelectorAll('.quick-reply');

        this.isOpen = false;

        this.init();
    }

    init() {
        // Event listeners
        this.chatButton.addEventListener('click', () => this.toggleChat());
        this.closeBtn.addEventListener('click', () => this.closeChat());
        this.minimizeBtn.addEventListener('click', () => this.closeChat());
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Quick replies
        this.quickReplies.forEach(btn => {
            btn.addEventListener('click', () => {
                const text = btn.textContent.trim().replace(/^[🔍🛒🔥❓]\s*/, '');
                this.userInput.value = text;
                this.sendMessage();
            });
        });

        console.log('Chatbot Widget initialized. User ID:', this.config.userId);
    }

    generateUserId() {
        // Benzersiz kullanıcı ID'si oluştur
        let userId = localStorage.getItem('rasa_user_id');
        if (!userId) {
            userId = 'user_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('rasa_user_id', userId);
        }
        return userId;
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        this.chatWindow.style.display = this.isOpen ? 'flex' : 'none';

        if (this.isOpen) {
            this.userInput.focus();
            this.notificationBadge.style.display = 'none';
        }
    }

    closeChat() {
        this.isOpen = false;
        this.chatWindow.style.display = 'none';
    }

    async sendMessage() {
        const message = this.userInput.value.trim();

        if (!message) return;

        // Kullanıcı mesajını göster
        this.addMessage(message, 'user');

        // Input'u temizle
        this.userInput.value = '';

        // Typing indicator göster
        this.showTyping();

        try {
            // Rasa'ya mesaj gönder
            const response = await this.sendToRasa(message);

            // Typing indicator gizle
            this.hideTyping();

            // Bot cevaplarını göster
            if (response && response.length > 0) {
                response.forEach((msg, index) => {
                    setTimeout(() => {
                        this.addMessage(msg.text, 'bot');
                    }, index * 300); // Her mesaj arası 300ms
                });
            } else {
                this.addMessage('Üzgünüm, şu anda cevap veremiyorum.', 'bot');
            }
        } catch (error) {
            this.hideTyping();
            console.error('Rasa bağlantı hatası:', error);

            // Hata durumunda mock cevap (demo için)
            this.addMessage(
                '⚠️ Sunucuya bağlanılamadı. Demo modunda çalışıyorsunuz.\n\n' +
                'Rasa sunucusunu başlatmak için:\n' +
                '1. `rasa run --enable-api --cors "*"`\n' +
                '2. `rasa run actions`',
                'bot'
            );

            // Demo cevapları
            this.handleDemoResponse(message);
        }
    }

    async sendToRasa(message) {
        const response = await fetch(`${this.config.rasaServerUrl}/webhooks/rest/webhook`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sender: this.config.userId,
                message: message,
            }),
        });

        if (!response.ok) {
            throw new Error('Rasa sunucusu yanıt vermiyor');
        }

        return await response.json();
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.textContent = sender === 'user' ? '👤' : '🤖';

        const content = document.createElement('div');
        content.className = 'message-content';

        const p = document.createElement('p');
        // Markdown-like formatlar için basit parse
        p.innerHTML = this.parseMarkdown(text);

        const timestamp = document.createElement('span');
        timestamp.className = 'timestamp';
        timestamp.textContent = this.getCurrentTime();

        content.appendChild(p);
        content.appendChild(timestamp);

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();

        // Kapalıysa bildirim göster
        if (!this.isOpen && sender === 'bot') {
            this.notificationBadge.style.display = 'flex';
            this.notificationBadge.textContent = '1';
        }
    }

    parseMarkdown(text) {
        // Basit markdown parse
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // **bold**
            .replace(/\*(.*?)\*/g, '<em>$1</em>') // *italic*
            .replace(/\n/g, '<br>'); // newlines
    }

    showTyping() {
        this.typingIndicator.style.display = 'block';
        this.scrollToBottom();
    }

    hideTyping() {
        this.typingIndicator.style.display = 'none';
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString('tr-TR', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    // Demo modunda mock cevaplar (Rasa çalışmıyorsa)
    handleDemoResponse(message) {
        const lowerMsg = message.toLowerCase();

        setTimeout(() => {
            if (lowerMsg.includes('merhaba') || lowerMsg.includes('selam')) {
                this.addMessage('Merhaba! Size nasıl yardımcı olabilirim? 🛍️', 'bot');
            } else if (lowerMsg.includes('elma')) {
                this.addMessage(
                    '✅ Elma bulundu!\n💰 Fiyat: 15 TL/kg\n📦 Stok: 100 kg\nSepete eklemek ister misiniz?',
                    'bot'
                );
            } else if (lowerMsg.includes('fiyat')) {
                this.addMessage('Hangi ürünün fiyatını öğrenmek istersiniz?', 'bot');
            } else if (lowerMsg.includes('sepet')) {
                this.addMessage('🛒 Sepetiniz şu anda boş. Ürün aramak ister misiniz?', 'bot');
            } else if (lowerMsg.includes('yardım')) {
                this.addMessage(
                    'Size şu konularda yardımcı olabilirim:\n\n' +
                    '🔍 Ürün arama ve fiyat sorgulama\n' +
                    '🛒 Sepete ürün ekleme\n' +
                    '📦 Sipariş takibi\n' +
                    '💡 Ürün önerileri',
                    'bot'
                );
            } else {
                this.addMessage(
                    'Demo modunda çalışıyorum. Şunları deneyebilirsiniz:\n' +
                    '• "elma var mı?"\n' +
                    '• "fiyatlar"\n' +
                    '• "sepetim"\n' +
                    '• "yardım"',
                    'bot'
                );
            }
        }, 500);
    }
}

// Widget'ı başlat
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new ChatbotWidget();
    console.log('✅ Chatbot Widget yüklendi!');
});
