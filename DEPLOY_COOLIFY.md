# 🚀 Tek Tıkla Coolify Deploy

Bu repository'yi Coolify'da tek tıkla deploy edin!

## ⚡ Hızlı Deploy

### Yöntem 1: Coolify Dashboard ile

1. **Coolify dashboard**'ınızı açın
2. **New Resource** → **GitHub Repository** seçin
3. Repository URL'i girin:
   ```
   https://github.com/burakdegirmenci/Chatbot
   ```
4. Branch: `main`
5. **Deploy Configuration**: Otomatik tespit edilir (docker-compose.yml)
6. **Environment Variables** ekleyin (aşağıda)
7. **Deploy** butonuna tıklayın!

### Yöntem 2: Coolify API ile (Tek Komut)

```bash
curl -X POST https://your-coolify.com/api/v1/deploy \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{
    "repository": "https://github.com/burakdegirmenci/Chatbot",
    "branch": "main",
    "project": "rasa-chatbot"
  }'
```

## 📋 Gerekli Environment Variables

Coolify dashboard'da **Environment** sekmesinden ekleyin:

### Minimum (Zorunlu):
```env
RASA_PORT=5005
ACTIONS_PORT=5055
WIDGET_PORT=8080
CORS_ORIGINS=*
```

### Önerilen (Production):
```env
RASA_PORT=5005
ACTIONS_PORT=5055
WIDGET_PORT=8080
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=INFO
XML_CACHE_HOURS=1
```

### Tam Liste:
`.env.example` dosyasına bakın.

## 🌐 Domain Ayarları

### 1. Domain Ekle
Coolify dashboard'da:
```
Domains → Add Domain → chatbot.yourdomain.com
```

### 2. DNS Ayarları
Domain sağlayıcınızda (Cloudflare, Namecheap, vb.):
```
A Record:
  Name: chatbot
  Value: YOUR_SERVER_IP
  TTL: Auto
```

### 3. SSL
Coolify otomatik Let's Encrypt SSL sertifikası oluşturur.
- **Settings** → **SSL** → **Enable**

## ✅ Deploy Sonrası Kontrol

### 1. Health Check
```bash
# Rasa API
curl https://chatbot.yourdomain.com/api/

# Actions
curl https://chatbot.yourdomain.com/api/webhook
```

### 2. Widget Test
Browser'da aç:
```
https://chatbot.yourdomain.com
```

### 3. Logs Kontrol
Coolify dashboard:
```
Resources → Container seç → Logs
```

## 🔧 Build Süreci

Deployment sırasında otomatik olarak:

```
✅ 1. Git repository clone
✅ 2. Docker images build
     - Rasa server (Dockerfile)
     - Actions server (Dockerfile.actions)
     - Widget (Nginx)
✅ 3. Environment variables inject
✅ 4. Containers start
✅ 5. Health checks
✅ 6. Domain routing
✅ 7. SSL certificate
```

**Toplam süre:** ~5-10 dakika

## 🎨 Widget Entegrasyonu

Deploy tamamlandıktan sonra:

### 1. Embed Generator Aç
```
https://chatbot.yourdomain.com/embed-demo.html
```

### 2. Kodu Al ve Sitenize Ekle
```html
<script
    src="https://chatbot.yourdomain.com/embed.js"
    data-rasa-url="https://chatbot.yourdomain.com/api"
    data-widget-title="Alışveriş Asistanı"
></script>
```

## 🔄 Otomatik Güncelleme

### Auto Deploy Aktif Et

Coolify dashboard:
```
Settings → Auto Deploy → Enable
Branch: main
Trigger: On Push
```

Artık her `git push` otomatik deploy tetikler!

## 📊 Servis Detayları

Deploy edilen servisler:

| Servis | Port | URL | Açıklama |
|--------|------|-----|----------|
| **Rasa Server** | 5005 | `/api/` | Chatbot API |
| **Actions Server** | 5055 | Internal | Custom actions |
| **Widget** | 8080 | `/` | Web widget |

## 🐛 Sorun Giderme

### Build hatası alıyorum

**Out of Memory:**
```bash
# Sunucuya swap ekle
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Port conflict:**
```env
# Environment variables'da portları değiştir
RASA_PORT=5006
ACTIONS_PORT=5056
WIDGET_PORT=8081
```

### Container başlamıyor

Coolify logs kontrol:
```
Resources → Container → Logs
```

Yaygın sorunlar:
- Environment variable eksik
- Port kullanımda
- Disk dolmuş
- Memory yetersiz

### Widget görünmüyor

```bash
# Nginx logs
docker logs chatbot-widget

# embed.js erişilebilir mi?
curl https://chatbot.yourdomain.com/embed.js
```

## 💡 Production İpuçları

### 1. CORS Sınırla
```env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 2. Log Seviyesi
```env
LOG_LEVEL=WARNING  # Production'da DEBUG kullanma
```

### 3. Cache Süresini Artır
```env
XML_CACHE_HOURS=6  # XML cache 6 saat
```

### 4. Backup Oluştur
```bash
# Cron job
0 2 * * * docker exec rasa-server tar -czf /backup/models-$(date +\%Y\%m\%d).tar.gz /app/models
```

## 📚 Detaylı Dokümantasyon

- **Tam Deployment Rehberi:** [COOLIFY_DEPLOYMENT.md](COOLIFY_DEPLOYMENT.md)
- **Widget Entegrasyonu:** [WIDGET_INTEGRATION.md](WIDGET_INTEGRATION.md)
- **XML Kullanımı:** [XML_KULLANIMI.md](XML_KULLANIMI.md)
- **Ana README:** [README.md](README.md)

## 💰 Sunucu Gereksinimleri

| Kullanım | RAM | CPU | Disk | Tahmini Maliyet |
|----------|-----|-----|------|-----------------|
| **Test** | 2GB | 1 | 10GB | €5-10/ay |
| **Küçük** | 4GB | 2 | 20GB | €15-25/ay |
| **Orta** | 8GB | 4 | 40GB | €40-60/ay |

**Önerilen VPS:**
- Hetzner Cloud CX21: 2GB RAM → €5.83/ay
- DigitalOcean Droplet: 2GB RAM → $12/ay
- Contabo VPS S: 8GB RAM → €6.99/ay

## ✅ Deployment Checklist

- [ ] Coolify kurulu
- [ ] Domain hazır (opsiyonel)
- [ ] Environment variables ayarlandı
- [ ] DNS kayıtları eklendi (domain varsa)
- [ ] Deploy butonu tıklandı
- [ ] Build tamamlandı
- [ ] Health check başarılı
- [ ] Widget test edildi
- [ ] Embed kodu alındı
- [ ] Production sitesine eklendi

## 🎉 Başarılı!

Chatbot'unuz artık canlıda!

**Widget URL:** https://chatbot.yourdomain.com
**Embed Generator:** https://chatbot.yourdomain.com/embed-demo.html
**API:** https://chatbot.yourdomain.com/api/

---

**Yardım gerekirse:** [GitHub Issues](https://github.com/burakdegirmenci/Chatbot/issues)
