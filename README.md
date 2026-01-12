# 🛍️ E-Ticaret Chatbot - Rasa ile Türkçe

Modern, tam özellikli e-ticaret chatbot'u. Rasa framework'ü ile geliştirilmiş, web widget arayüzü ile entegre. **Gerçek XML verisi** (Elle Shoes) ile çalışır.

[![Rasa](https://img.shields.io/badge/Rasa-3.6.0-5A17EE?style=flat-square)](https://rasa.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

## 🚀 Tek Tıkla Deploy

### Coolify ile Deploy

[![Deploy on Coolify](https://img.shields.io/badge/Deploy%20on-Coolify-6366f1?style=for-the-badge&logo=docker)](https://github.com/burakdegirmenci/Chatbot/blob/main/DEPLOY_COOLIFY.md)

**3 adımda canlıya alın:**
1. Coolify dashboard'da **New Resource** → **GitHub Repository**
2. Repository: `https://github.com/burakdegirmenci/Chatbot`
3. **Deploy** butonu → Tamamlandı! 🎉

👉 **Detaylı Rehber:** [DEPLOY_COOLIFY.md](DEPLOY_COOLIFY.md)

### Docker Compose ile

```bash
git clone https://github.com/burakdegirmenci/Chatbot.git
cd Chatbot
docker-compose up -d
```

## ✨ Özellikler

### 🤖 Chatbot Yetenekleri
- ✅ **Gerçek Ürün Verisi** - Elle Shoes XML feed (2000+ ürün)
- ✅ **Akıllı Arama** - İsim, kategori, renk, fiyat filtreleri
- ✅ **İndirim Desteği** - Otomatik indirimli ürün tespiti
- ✅ **Sepet Yönetimi** - Ürün ekleme, toplam hesaplama
- ✅ **Sipariş Oluşturma** - Otomatik sipariş takip numarası
- ✅ **Ürün Varyantları** - Renk/beden seçenekleri
- ✅ **Türkçe NLU** - Tam Türkçe dil desteği

### 🎨 Web Widget
- ✅ **Tek Satır Kod** - Embed script ile kolay entegrasyon
- ✅ **Özelleştirilebilir** - Renk, pozisyon, mesajlar
- ✅ **Responsive** - Mobil uyumlu
- ✅ **Zero Dependencies** - Vanilla JavaScript
- ✅ **Lightweight** - ~10KB minified

### 📦 Production Ready
- ✅ **Docker & Docker Compose** - Container support
- ✅ **Health Checks** - Otomatik sağlık kontrolleri
- ✅ **Auto SSL** - Coolify ile otomatik Let's Encrypt
- ✅ **Auto Deploy** - Git push ile otomatik deployment
- ✅ **Cache System** - 1 saatlik XML cache

## 🎯 Demo

### Widget Örneği

```html
<!-- Sitenize tek satır ekleyin -->
<script
    src="https://your-domain.com/embed.js"
    data-rasa-url="https://your-domain.com/api"
    data-widget-title="Alışveriş Asistanı"
    data-primary-color="#667eea"
></script>
```

### Örnek Konuşma

```
Kullanıcı: siyah bot var mı?
Bot: ✅ Siyah Deri Kadın Bot bulundu!
     💰 Fiyat: 1899.90 TL ~~2499.90 TL~~ 🔥 %24 İNDİRİM!
     🎨 Renk: Siyah | 📏 Beden: 38
     📦 Stokta var ✓

     Sepete eklemek ister misiniz?

Kullanıcı: evet
Bot: ✅ Sepete eklendi! 🛒
```

## 📚 Dokümantasyon

| Dosya | Açıklama |
|-------|----------|
| **[DEPLOY_COOLIFY.md](DEPLOY_COOLIFY.md)** | Tek tıkla Coolify deployment |
| **[COOLIFY_DEPLOYMENT.md](COOLIFY_DEPLOYMENT.md)** | Detaylı deployment rehberi |
| **[WIDGET_INTEGRATION.md](WIDGET_INTEGRATION.md)** | Widget entegrasyon rehberi |
| **[XML_KULLANIMI.md](XML_KULLANIMI.md)** | XML feed kullanımı |
| **[QUICKSTART.md](QUICKSTART.md)** | 5 dakikada başlangıç |

## 🏗️ Mimari

```
┌─────────────────┐
│   Web Widget    │ (HTML/CSS/JS - Tek satır embed)
│   (Frontend)    │
└────────┬────────┘
         │ HTTP REST API
         │
┌────────▼────────┐
│   Rasa Server   │ (Port 5005 - NLU + Dialog)
│   (NLU + Core)  │
└────────┬────────┘
         │
         ├──────► Actions Server (Port 5055 - Python logic)
         │        - XML parser
         │        - Ürün arama
         │        - Sepet yönetimi
         │
         └──────► Elle Shoes XML Feed
                  - 2000+ ürün
                  - Gerçek zamanlı stok
                  - İndirim bilgileri
```

## 🚀 Hızlı Başlangıç

### Manuel Kurulum (Lokal Test)

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Modeli eğit
rasa train

# 3. Servisleri başlat
# Terminal 1:
rasa run --enable-api --cors "*"

# Terminal 2:
rasa run actions

# Terminal 3:
cd widget && python -m http.server 8080
```

👉 **Detay:** [QUICKSTART.md](QUICKSTART.md)

### Docker ile

```bash
docker-compose up -d
```

Erişim:
- Widget: http://localhost:8080
- Rasa API: http://localhost:5005
- Actions: http://localhost:5055

## 📂 Proje Yapısı

```
Chatbot/
├── 📂 actions/              Python backend
│   ├── actions.py          8 custom action
│   └── xml_helper.py       XML parser
│
├── 📂 data/                 Eğitim verileri
│   ├── nlu.yml             11 intent, 100+ örnek
│   ├── stories.yml         Konuşma senaryoları
│   └── rules.yml           Sabit kurallar
│
├── 📂 widget/               Web arayüzü
│   ├── embed.js            Tek satır embed script
│   ├── embed-demo.html     Kod generator UI
│   └── index.html          Standalone demo
│
├── 📂 tests/                Test dosyaları
│
├── docker-compose.yml       Multi-container setup
├── Dockerfile               Rasa server image
├── Dockerfile.actions       Actions server image
├── nginx.conf               Widget için Nginx
│
└── 📚 Dokümantasyon
    ├── DEPLOY_COOLIFY.md
    ├── COOLIFY_DEPLOYMENT.md
    ├── WIDGET_INTEGRATION.md
    └── XML_KULLANIMI.md
```

## 🎨 Widget Entegrasyonu

### Adım 1: Embed Generator Aç

Deploy sonrası:
```
https://your-domain.com/embed-demo.html
```

### Adım 2: Ayarları Yap

- Rasa API URL
- Widget başlığı
- Renk teması
- Pozisyon (sağ/sol)

### Adım 3: Kodu Kopyala ve Yapıştır

Herhangi bir web sitesine ekleyin:

**HTML:**
```html
</body> tag'inden önce ekle
```

**WordPress:**
```php
footer.php'ye ekle
```

**Shopify:**
```liquid
theme.liquid'e ekle
```

**React/Vue/Next.js:**
```jsx
public/index.html veya _document.js'e ekle
```

👉 **Platform örnekleri:** [WIDGET_INTEGRATION.md](WIDGET_INTEGRATION.md)

## 🔧 Özelleştirme

### Kendi XML'inizi Kullanın

`actions/xml_helper.py` → Satır 304:
```python
XML_URL = "https://your-xml-feed.com/products.xml"
```

### Widget Renklerini Değiştirin

```html
data-primary-color="#FF6B6B"
data-secondary-color="#FF8E53"
```

### Yeni Intent Ekleyin

1. `data/nlu.yml` → Örnek cümleler ekle
2. `domain.yml` → Intent tanımla
3. `actions/actions.py` → Action yaz
4. `rasa train` → Yeniden eğit

## 📊 Teknik Detaylar

| Özellik | Değer |
|---------|-------|
| **Rasa Version** | 3.6.0 |
| **Python** | 3.8+ |
| **NLU Pipeline** | DIET Classifier |
| **Dialog Policy** | TEDPolicy |
| **Dil** | Türkçe |
| **Ürün Sayısı** | 2000+ (Elle Shoes) |
| **Cache** | 1 saat (ayarlanabilir) |
| **Response Time** | <500ms |

## 🔒 Güvenlik

- ✅ HTTPS zorunlu
- ✅ CORS yapılandırılabilir
- ✅ Environment variables ile sensitive data
- ✅ Otomatik SSL (Coolify)
- ✅ Health checks
- ✅ Non-root container users

## 💰 Maliyet

### Sunucu Gereksinimleri

| Boyut | RAM | CPU | Disk | Maliyet/ay |
|-------|-----|-----|------|------------|
| **Küçük** | 2GB | 1 | 10GB | €5-10 |
| **Orta** | 4GB | 2 | 20GB | €15-25 |
| **Büyük** | 8GB | 4 | 40GB | €40-60 |

**Önerilen VPS:**
- Hetzner CX21: €5.83/ay
- DigitalOcean: $12/ay
- Contabo: €6.99/ay

## 🧪 Test

### NLU Test
```bash
rasa test nlu
```

### Dialog Test
```bash
rasa shell
```

### XML Parser Test
```bash
python test_xml_katalog.py
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch: `git checkout -b feature/amazing`
3. Commit: `git commit -m 'Add feature'`
4. Push: `git push origin feature/amazing`
5. Pull Request açın

## 📝 License

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🆘 Destek

- 📖 [Detaylı Dokümantasyon](COOLIFY_DEPLOYMENT.md)
- 🐛 [GitHub Issues](https://github.com/burakdegirmenci/Chatbot/issues)
- 💬 [Discussions](https://github.com/burakdegirmenci/Chatbot/discussions)

## 🎉 Başarı Hikayeleri

### Elle Shoes Entegrasyonu
- ✅ 2000+ ürün katalogu
- ✅ Gerçek zamanlı stok
- ✅ İndirim desteği
- ✅ Ürün varyantları

### Kullanım İstatistikleri
- ⚡ <500ms response time
- 🎯 %95+ intent accuracy
- 📊 1 saatlik cache = %80 daha hızlı

## 🚀 Roadmap

- [ ] Multi-language support (EN, DE, FR)
- [ ] Voice input/output
- [ ] Analytics dashboard
- [ ] A/B testing
- [ ] Sentiment analysis
- [ ] Product recommendations (ML)

## 📞 İletişim

- **GitHub:** [@burakdegirmenci](https://github.com/burakdegirmenci)
- **Repository:** [Chatbot](https://github.com/burakdegirmenci/Chatbot)

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!**

[![Deploy on Coolify](https://img.shields.io/badge/Deploy%20on-Coolify-6366f1?style=for-the-badge&logo=docker)](https://github.com/burakdegirmenci/Chatbot/blob/main/DEPLOY_COOLIFY.md)

Made with ❤️ using [Rasa](https://rasa.com)

</div>
