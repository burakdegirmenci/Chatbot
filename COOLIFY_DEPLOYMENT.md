# 🚀 Coolify Deployment Rehberi

Rasa Chatbot'unuzu kendi sunucunuzda Coolify ile deploy edin.

## 📋 Ön Gereksinimler

- ✅ Coolify kurulu bir sunucu (VPS, Dedicated Server, vb.)
- ✅ Domain adı (opsiyonel ama önerilir)
- ✅ En az 2GB RAM, 2 CPU core
- ✅ 10GB disk alanı

## 🎯 Adım 1: Coolify'da Proje Oluştur

### 1.1 Coolify Dashboard'a Giriş
```
https://your-coolify-domain.com
```

### 1.2 Yeni Proje Oluştur
1. **Projects** → **New Project**
2. İsim: `rasa-chatbot`
3. **Create**

### 1.3 Environment Oluştur
1. Projeye tıkla
2. **New Environment** → `production`

## 🐳 Adım 2: Git Repository Bağla

### Metod 1: GitHub/GitLab ile

1. **New Resource** → **Git Repository**
2. Repository URL'inizi girin:
   ```
   https://github.com/yourusername/rasa-chatbot
   ```
3. Branch: `main` veya `master`
4. **Continue**

### Metod 2: Lokal Deploy (Git olmadan)

SSH ile sunucuya bağlan:
```bash
ssh user@your-server.com

# Proje klasörü oluştur
mkdir -p /opt/rasa-chatbot
cd /opt/rasa-chatbot

# Dosyaları yükle (scp veya git clone ile)
```

## ⚙️ Adım 3: Docker Compose Konfigürasyonu

Coolify dashboard'da:

1. **Settings** → **Docker Compose**
2. `coolify.yaml` dosyasını yükle veya yapıştır
3. **Save**

## 🔐 Adım 4: Environment Variables

**Environment** sekmesinde şu değişkenleri ekle:

```env
RASA_PORT=5005
ACTIONS_PORT=5055
WIDGET_PORT=8080
CORS_ORIGINS=*
```

### Production için önerilen ek değişkenler:

```env
# Domain (Coolify otomatik ekleyecek)
DOMAIN=chatbot.yourdomain.com

# Docker registry (kendi registry'niz varsa)
DOCKER_REGISTRY=ghcr.io/yourusername

# Monitoring
LOG_LEVEL=INFO
```

## 🌐 Adım 5: Domain ve SSL Ayarları

### 5.1 Domain Ekle

1. **Domains** → **Add Domain**
2. Domain gir: `chatbot.yourdomain.com`
3. **Add**

### 5.2 DNS Ayarları

Domain sağlayıcınızda (Cloudflare, Namecheap, vb.):

```
A Record:
  Host: chatbot
  Value: YOUR_SERVER_IP
  TTL: Auto
```

### 5.3 SSL (Otomatik)

Coolify otomatik Let's Encrypt SSL sertifikası alacak.
- **Settings** → **SSL** → **Enable SSL**

## 🏗️ Adım 6: Build ve Deploy

### 6.1 İlk Build

1. **Deploy** butonuna tıkla
2. Build süreci başlayacak (5-10 dakika)

**Build adımları:**
```
1. ✅ Git repository clone
2. ✅ Docker image build (Rasa + Actions)
3. ✅ Model eğitimi (rasa train)
4. ✅ Containers başlatma
5. ✅ Health check
```

### 6.2 Build Logs

Real-time logs görmek için:
- **Deployments** → En son deployment → **Logs**

### 6.3 Build Hatası Durumunda

Yaygın hatalar ve çözümleri:

**Hata 1: Out of Memory**
```bash
# Sunucuya swap ekle
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Hata 2: Port Already in Use**
```bash
# Coolify dashboard'da portları değiştir
RASA_PORT=5006
ACTIONS_PORT=5056
```

## ✅ Adım 7: Deploy Doğrulama

### 7.1 Health Check

Terminal'de veya browser'da:

```bash
# Rasa API
curl https://chatbot.yourdomain.com/api/

# Actions Server
curl https://chatbot.yourdomain.com/api/webhook
```

Başarılı yanıt:
```json
{"version": "3.6.0"}
```

### 7.2 Widget Test

Browser'da aç:
```
https://chatbot.yourdomain.com
```

Widget sağ altta görünmeli.

### 7.3 Container Status

Coolify dashboard:
- **Resources** → Tüm containerlar "Running" olmalı

## 🔧 Adım 8: Widget Embed Kodu Oluştur

### 8.1 Embed Generator Aç

Browser'da:
```
https://chatbot.yourdomain.com/embed-demo.html
```

### 8.2 Ayarları Yap

1. **Rasa API URL**: `https://chatbot.yourdomain.com`
2. Widget ayarlarını özelleştir
3. **Embed Kodu Oluştur** butonuna tıkla

### 8.3 Kodu Kopyala

Örnek çıktı:
```html
<!-- Rasa Chatbot Widget -->
<script
    src="https://chatbot.yourdomain.com/embed.js"
    data-rasa-url="https://chatbot.yourdomain.com/api"
    data-widget-title="Alışveriş Asistanı"
    data-greeting="Merhaba! Size nasıl yardımcı olabilirim?"
    data-primary-color="#667eea"
    data-secondary-color="#764ba2"
    data-position="right"
></script>
```

### 8.4 Sitenize Ekleyin

HTML dosyanızın sonuna, `</body>` tag'inden önce yapıştırın:

```html
<!DOCTYPE html>
<html>
<head>
    <title>E-Ticaret Sitem</title>
</head>
<body>
    <!-- Sitenizin içeriği -->

    <!-- Chatbot Widget - En sona ekleyin -->
    <script
        src="https://chatbot.yourdomain.com/embed.js"
        data-rasa-url="https://chatbot.yourdomain.com/api"
        data-widget-title="Alışveriş Asistanı"
        data-greeting="Merhaba! Nasıl yardımcı olabilirim?"
    ></script>
</body>
</html>
```

## 🎨 Widget Özelleştirme Seçenekleri

### Tüm Parametreler:

```html
<script
    src="https://chatbot.yourdomain.com/embed.js"

    <!-- Zorunlu -->
    data-rasa-url="https://chatbot.yourdomain.com/api"

    <!-- Opsiyonel -->
    data-widget-title="Alışveriş Asistanı"
    data-greeting="Merhaba! Size nasıl yardımcı olabilirim?"
    data-primary-color="#667eea"
    data-secondary-color="#764ba2"
    data-position="right"      <!-- right veya left -->
    data-avatar="🤖"
    data-language="tr"
></script>
```

### Örnekler:

**1. Minimalist Tema:**
```html
<script
    src="https://chatbot.yourdomain.com/embed.js"
    data-rasa-url="https://chatbot.yourdomain.com/api"
    data-primary-color="#000000"
    data-secondary-color="#333333"
></script>
```

**2. Marka Renkleri ile:**
```html
<script
    src="https://chatbot.yourdomain.com/embed.js"
    data-rasa-url="https://chatbot.yourdomain.com/api"
    data-primary-color="#FF6B6B"
    data-secondary-color="#FF8E53"
    data-widget-title="Destek Asistanı"
></script>
```

**3. Sol Tarafa Yerleştirilmiş:**
```html
<script
    src="https://chatbot.yourdomain.com/embed.js"
    data-rasa-url="https://chatbot.yourdomain.com/api"
    data-position="left"
></script>
```

## 📊 Adım 9: Monitoring ve Logs

### 9.1 Coolify Dashboard

**Real-time logs:**
- **Resources** → Container seç → **Logs**

**Metrics:**
- CPU kullanımı
- Memory kullanımı
- Network trafiği

### 9.2 Container Logs (SSH)

```bash
# Rasa server logs
docker logs rasa-server -f

# Actions server logs
docker logs rasa-actions -f

# Widget logs (Nginx)
docker logs chatbot-widget -f
```

### 9.3 Hata Debug

**Chatbot yanıt vermiyor:**
```bash
# Rasa server status
curl https://chatbot.yourdomain.com/api/
curl https://chatbot.yourdomain.com/api/version

# Actions server status
docker exec rasa-actions curl http://localhost:5055/health
```

**Widget görünmüyor:**
```bash
# Nginx logs
docker logs chatbot-widget -f

# embed.js erişilebilir mi?
curl https://chatbot.yourdomain.com/embed.js
```

## 🔄 Adım 10: Güncelleme ve Yeni Deployment

### 10.1 Otomatik Deploy (Git ile)

Coolify'da **Settings** → **Auto Deploy**:
- ✅ Enable Auto Deploy
- Branch: `main`
- Trigger: `On Push`

Her git push'ta otomatik deploy olur.

### 10.2 Manuel Deploy

1. Kodu güncelle (git push)
2. Coolify dashboard → **Deploy**
3. Yeni container'lar başlatılır
4. Zero-downtime deployment

### 10.3 Model Güncelleme

```bash
# SSH ile sunucuya bağlan
ssh user@your-server.com

# Container'a gir
docker exec -it rasa-server bash

# Modeli yeniden eğit
rasa train

# Container'ı restart et (Coolify dashboard'dan)
```

## 🔒 Güvenlik

### SSL/TLS
✅ Coolify otomatik Let's Encrypt
✅ Auto-renewal

### CORS
Production için belirli domainlere sınırla:

```env
# .env dosyasında
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Firewall
```bash
# UFW ile sadece gerekli portları aç
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### Rate Limiting (Nginx)

`nginx.conf` dosyasına ekle:
```nginx
limit_req_zone $binary_remote_addr zone=chatbot:10m rate=10r/s;

location /api/ {
    limit_req zone=chatbot burst=20;
    proxy_pass http://rasa-server:5005/;
}
```

## 💰 Maliyet Optimizasyonu

### Sunucu Gereksinimleri:

| Kullanım | RAM | CPU | Disk | Aylık Maliyet* |
|----------|-----|-----|------|----------------|
| Test     | 2GB | 1   | 10GB | $5-10          |
| Küçük    | 4GB | 2   | 20GB | $15-25         |
| Orta     | 8GB | 4   | 40GB | $40-60         |
| Büyük    | 16GB| 8   | 80GB | $80-120        |

*Hetzner, DigitalOcean, Linode fiyatları

### VPS Önerileri:

1. **Hetzner Cloud** (En ucuz)
   - CX21: 2GB RAM, 2 CPU → €5.83/ay
   - CX31: 4GB RAM, 2 CPU → €11.66/ay

2. **DigitalOcean**
   - Basic Droplet: 2GB RAM → $12/ay
   - Regular: 4GB RAM → $24/ay

3. **Contabo**
   - VPS S: 8GB RAM → €6.99/ay (çok ucuz!)

## 🆘 Troubleshooting

### Problem: Container başlamıyor

**Çözüm:**
```bash
# Logs kontrol et
docker logs rasa-server
docker logs rasa-actions

# Manuel başlat
docker-compose up -d
```

### Problem: XML indirilemiyor

**Çözüm:**
```bash
# Container'a gir
docker exec -it rasa-actions bash

# Manuel test
python -c "from actions.xml_helper import katalog; print(len(katalog))"
```

### Problem: Out of disk space

**Çözüm:**
```bash
# Eski Docker image'leri temizle
docker system prune -a

# Logları temizle
docker logs --tail 100 rasa-server > /dev/null
```

### Problem: SSL certificate alınamıyor

**Çözüm:**
1. DNS'in doğru yayıldığını kontrol et: `nslookup chatbot.yourdomain.com`
2. Port 80/443 açık mı: `sudo netstat -tlnp`
3. Coolify → **Settings** → **SSL** → **Force Regenerate**

## 📚 İleri Seviye

### 1. PostgreSQL Ekleme

Tracker store için:

```yaml
# docker-compose.yml'e ekle
postgres:
  image: postgres:15
  environment:
    POSTGRES_DB: rasa
    POSTGRES_USER: rasa
    POSTGRES_PASSWORD: ${DB_PASSWORD}
  volumes:
    - postgres-data:/var/lib/postgresql/data
```

### 2. Redis Cache

```yaml
redis:
  image: redis:7-alpine
  volumes:
    - redis-data:/data
```

### 3. Monitoring (Prometheus + Grafana)

Coolify'da ayrı proje olarak ekle.

### 4. Backup Stratejisi

```bash
# Cron job ekle
0 2 * * * docker exec rasa-server tar -czf /backup/models-$(date +\%Y\%m\%d).tar.gz /app/models
```

## ✅ Deployment Checklist

Deployment öncesi:
- [ ] `.env.production` ayarlandı
- [ ] Domain DNS'e eklendi
- [ ] SSL aktif
- [ ] Health check çalışıyor
- [ ] Widget test edildi
- [ ] Backup yapılandırıldı

Deployment sonrası:
- [ ] Tüm servisler çalışıyor
- [ ] Widget embed kodu alındı
- [ ] Production sitesinde test edildi
- [ ] Monitoring kuruldu
- [ ] Takımı bilgilendir

## 🎉 Tebrikler!

Chatbot'unuz artık canlıda!

**Sonraki adımlar:**
1. Widget'ı ana sitenize ekleyin
2. Kullanıcı feedback'lerini toplayın
3. NLU'yu iyileştirin
4. Analytics ekleyin

---

**Sorular için:** GitHub Issues veya dokumentasyon
