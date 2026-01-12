# 🎨 Widget Entegrasyon Rehberi

Web sitenize chatbot widget'ı ekleme rehberi.

## 🚀 Hızlı Başlangıç

### Adım 1: Embed Generator'ı Açın

```
https://your-chatbot-domain.com/embed-demo.html
```

### Adım 2: Ayarları Yapılandırın

Widget'ınızı özelleştirin:
- Rasa API URL
- Widget başlığı
- Hoşgeldin mesajı
- Renkler
- Pozisyon (sağ/sol)

### Adım 3: Kodu Kopyalayın

"Embed Kodu Oluştur" butonuna tıklayın ve oluşan kodu kopyalayın.

### Adım 4: Sitenize Ekleyin

HTML dosyanızın sonuna, `</body>` tag'inden önce yapıştırın.

---

## 📝 Detaylı Kullanım

### Temel Entegrasyon

```html
<!DOCTYPE html>
<html lang="tr">
<head>
    <title>E-Ticaret Sitem</title>
</head>
<body>
    <!-- Sitenizin içeriği -->
    <h1>Hoş Geldiniz</h1>

    <!-- Chatbot Widget -->
    <script
        src="https://your-chatbot-domain.com/embed.js"
        data-rasa-url="https://your-chatbot-domain.com/api"
    ></script>
</body>
</html>
```

### Özelleştirilmiş Entegrasyon

```html
<script
    src="https://your-chatbot-domain.com/embed.js"
    data-rasa-url="https://your-chatbot-domain.com/api"
    data-widget-title="Alışveriş Asistanı"
    data-greeting="Merhaba! Nasıl yardımcı olabilirim?"
    data-primary-color="#FF6B6B"
    data-secondary-color="#FF8E53"
    data-position="right"
    data-avatar="🛒"
></script>
```

---

## 🎨 Özelleştirme Seçenekleri

### Tüm Parametreler

| Parametre | Tip | Varsayılan | Açıklama |
|-----------|-----|-----------|----------|
| `data-rasa-url` | string | **Zorunlu** | Rasa API URL'i |
| `data-widget-title` | string | "Alışveriş Asistanı" | Widget başlığı |
| `data-greeting` | string | "Merhaba!..." | İlk mesaj |
| `data-primary-color` | color | #667eea | Ana renk |
| `data-secondary-color` | color | #764ba2 | İkinci renk |
| `data-position` | "right"\|"left" | right | Pozisyon |
| `data-avatar` | emoji | 🤖 | Avatar |
| `data-language` | string | tr | Dil kodu |

### Renk Örnekleri

**Klasik Mavi:**
```html
data-primary-color="#2196F3"
data-secondary-color="#1976D2"
```

**Modern Mor:**
```html
data-primary-color="#9C27B0"
data-secondary-color="#7B1FA2"
```

**Yeşil Dostu:**
```html
data-primary-color="#4CAF50"
data-secondary-color="#388E3C"
```

**Turuncu Enerjik:**
```html
data-primary-color="#FF6B6B"
data-secondary-color="#FF8E53"
```

---

## 🖥️ Platform Örnekleri

### WordPress

**Tema dosyasına ekle** (`footer.php`):

```php
<?php wp_footer(); ?>

<!-- Chatbot Widget -->
<script
    src="https://your-chatbot-domain.com/embed.js"
    data-rasa-url="https://your-chatbot-domain.com/api"
></script>

</body>
</html>
```

**Plugin ile:**
1. "Insert Headers and Footers" plugin'i kur
2. Settings → Insert Headers and Footers
3. Footer'a script'i yapıştır

### Shopify

**Theme.liquid dosyasına:**

1. Online Store → Themes → Actions → Edit code
2. `Layout/theme.liquid` aç
3. `</body>` tag'inden önce ekle:

```liquid
<!-- Chatbot Widget -->
<script
    src="https://your-chatbot-domain.com/embed.js"
    data-rasa-url="https://your-chatbot-domain.com/api"
    data-widget-title="{{ shop.name }} Asistan"
></script>

</body>
```

### React

**App.js veya index.html:**

```jsx
// public/index.html içinde
<!DOCTYPE html>
<html lang="tr">
<head>
    <title>React App</title>
</head>
<body>
    <div id="root"></div>

    <!-- Chatbot Widget -->
    <script
        src="https://your-chatbot-domain.com/embed.js"
        data-rasa-url="https://your-chatbot-domain.com/api"
    ></script>
</body>
</html>
```

**Veya Component olarak:**

```jsx
// ChatbotWidget.jsx
import { useEffect } from 'react';

export default function ChatbotWidget() {
    useEffect(() => {
        const script = document.createElement('script');
        script.src = 'https://your-chatbot-domain.com/embed.js';
        script.setAttribute('data-rasa-url', 'https://your-chatbot-domain.com/api');
        document.body.appendChild(script);

        return () => {
            document.body.removeChild(script);
        };
    }, []);

    return null;
}

// App.jsx'de kullan
import ChatbotWidget from './ChatbotWidget';

function App() {
    return (
        <div>
            {/* Sitenizin içeriği */}
            <ChatbotWidget />
        </div>
    );
}
```

### Vue.js

```vue
<!-- App.vue -->
<template>
  <div id="app">
    <!-- Sitenizin içeriği -->
  </div>
</template>

<script>
export default {
  mounted() {
    const script = document.createElement('script');
    script.src = 'https://your-chatbot-domain.com/embed.js';
    script.setAttribute('data-rasa-url', 'https://your-chatbot-domain.com/api');
    document.body.appendChild(script);
  }
}
</script>
```

### Next.js

```jsx
// pages/_document.js
import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html>
      <Head />
      <body>
        <Main />
        <NextScript />

        {/* Chatbot Widget */}
        <script
          src="https://your-chatbot-domain.com/embed.js"
          data-rasa-url="https://your-chatbot-domain.com/api"
        />
      </body>
    </Html>
  )
}
```

### Wix

1. Dashboard → Settings → Custom Code
2. Body - End of `</body>` seç
3. Script'i yapıştır
4. Apply to All Pages seç

### Squarespace

1. Settings → Advanced → Code Injection
2. Footer'a script'i yapıştır
3. Save

---

## 🎯 Koşullu Gösterim

### Sadece Belirli Sayfalarda Göster

```html
<script>
    // Sadece ürün sayfalarında göster
    if (window.location.pathname.includes('/urun/')) {
        const script = document.createElement('script');
        script.src = 'https://your-chatbot-domain.com/embed.js';
        script.setAttribute('data-rasa-url', 'https://your-chatbot-domain.com/api');
        document.body.appendChild(script);
    }
</script>
```

### Mobilde Gizle

```html
<script>
    // Desktop'ta göster, mobilde gizle
    if (window.innerWidth > 768) {
        const script = document.createElement('script');
        script.src = 'https://your-chatbot-domain.com/embed.js';
        script.setAttribute('data-rasa-url', 'https://your-chatbot-domain.com/api');
        document.body.appendChild(script);
    }
</script>
```

### Belirli Süreden Sonra Göster

```html
<script>
    // 10 saniye sonra göster
    setTimeout(() => {
        const script = document.createElement('script');
        script.src = 'https://your-chatbot-domain.com/embed.js';
        script.setAttribute('data-rasa-url', 'https://your-chatbot-domain.com/api');
        document.body.appendChild(script);
    }, 10000);
</script>
```

---

## 🧪 Test ve Debug

### Widget Yüklendi mi Kontrol

Browser console'da:

```javascript
// Widget element'i var mı?
document.getElementById('rasa-chatbot-widget')

// Script yüklendi mi?
document.querySelector('script[src*="embed.js"]')
```

### API Bağlantısı Test

```javascript
// Rasa API'ye test isteği
fetch('https://your-chatbot-domain.com/api/')
    .then(res => res.json())
    .then(data => console.log('Rasa version:', data.version))
    .catch(err => console.error('API error:', err));
```

### Console Logs

Widget yüklendiğinde göreceğiniz log:
```
✅ Rasa Chatbot Widget yüklendi
```

---

## ⚡ Performance

### Async Loading

Widget'ı asenkron yükle (sayfa hızını etkilemez):

```html
<script async
    src="https://your-chatbot-domain.com/embed.js"
    data-rasa-url="https://your-chatbot-domain.com/api"
></script>
```

### Lazy Loading

Kullanıcı scroll edince yükle:

```html
<script>
    window.addEventListener('scroll', function loadWidget() {
        const script = document.createElement('script');
        script.src = 'https://your-chatbot-domain.com/embed.js';
        script.setAttribute('data-rasa-url', 'https://your-chatbot-domain.com/api');
        document.body.appendChild(script);

        // Bir kere çalıştır
        window.removeEventListener('scroll', loadWidget);
    });
</script>
```

---

## 🔒 Güvenlik

### HTTPS Zorunlu

Widget sadece HTTPS üzerinde çalışır. HTTP siteler desteklenmez.

### CORS Ayarları

Rasa sunucunuzda CORS doğru ayarlanmalı:

```yaml
# credentials.yml
rest:
  cors_origins: "https://your-website.com"
```

### Content Security Policy

CSP header'ınız varsa, ekleyin:

```html
<meta http-equiv="Content-Security-Policy"
      content="script-src 'self' https://your-chatbot-domain.com;">
```

---

## 📊 Analytics

### Google Analytics Event Tracking

```javascript
// Widget açıldığında event gönder
document.getElementById('rasa-chat-button').addEventListener('click', () => {
    gtag('event', 'chatbot_opened', {
        'event_category': 'engagement',
        'event_label': 'Chatbot Widget'
    });
});
```

---

## ❓ Sık Sorulan Sorular

### Widget görünmüyor?

1. Console'da hata var mı kontrol edin (F12)
2. Script URL'i doğru mu?
3. Rasa API erişilebilir mi?
4. CORS ayarları doğru mu?

### Widget çok büyük/küçük?

CSS ile boyutunu özelleştirin:

```html
<style>
    #rasa-chat-window {
        width: 400px !important;
        height: 650px !important;
    }
</style>
```

### Mobilde farklı ayar?

```html
<style>
    @media (max-width: 768px) {
        #rasa-chat-window {
            width: 100vw !important;
            height: 100vh !important;
            bottom: 0 !important;
            right: 0 !important;
        }
    }
</style>
```

### Widget'ı programatik aç/kapa?

```javascript
// Aç
document.getElementById('rasa-chat-button').click();

// Kapat
document.getElementById('rasa-close-btn').click();
```

---

## 🎉 Başarılı Entegrasyon!

Widget başarıyla eklendiğinde:
- ✅ Sağ/sol altta yuvarlak buton görünür
- ✅ Butona tıklanınca chat penceresi açılır
- ✅ İlk hoşgeldin mesajı otomatik gelir
- ✅ Kullanıcı mesaj gönderebilir

---

**Yardım:** [COOLIFY_DEPLOYMENT.md](COOLIFY_DEPLOYMENT.md) | [README.md](README.md)
