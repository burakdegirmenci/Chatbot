# ⚡ Hızlı Başlangıç Kılavuzu

5 dakikada chatbot'unuzu çalıştırın!

## 🎯 Adım 1: Kurulum (2 dk)

```bash
# Python ve pip yüklü olduğundan emin olun
python --version  # 3.8+ olmalı

# Virtual environment oluştur
python -m venv venv

# Aktif et
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

## 🎓 Adım 2: Model Eğit (2 dk)

```bash
rasa train
```

**Not**: İlk eğitim 5-10 dakika sürebilir. Kahve molası verin ☕

## 🚀 Adım 3: Çalıştır (1 dk)

**Terminal 1** - Rasa Server:
```bash
rasa run --enable-api --cors "*"
```

**Terminal 2** - Action Server:
```bash
rasa run actions
```

**Terminal 3** - Web Widget:
```bash
cd widget
python -m http.server 8080
```

## ✅ Adım 4: Test Et!

1. Tarayıcıda aç: **http://localhost:8080**
2. Sağ alttaki chat butonuna tıkla
3. Şunları dene:

```
→ "merhaba"
→ "elma var mı?"
→ "fiyat ne kadar?"
→ "2 kilo ekle"
→ "sepetimi göster"
```

## 🎉 Tebrikler!

Chatbot'unuz çalışıyor! Şimdi ne yapabilirsiniz?

### Sonraki Adımlar:

1. **Yeni ürünler ekle** → `actions/actions.py` dosyasında `URUN_KATALOG`
2. **Yeni intent ekle** → `data/nlu.yml` ve `domain.yml`
3. **Widget'ı özelleştir** → `widget/chatbot-widget.css`
4. **Kendi web sitene entegre et** → Sadece widget klasörünü kopyala

## 🐛 Sorun mu var?

### Rasa çalışmıyor
```bash
# Port'u kontrol et
netstat -ano | findstr :5005  # Windows
lsof -i :5005                  # Mac/Linux

# Port değiştir
rasa run --port 5006 --enable-api --cors "*"
```

### Model bulunamadı hatası
```bash
# Yeniden eğit
rasa train
```

### Actions çalışmıyor
```bash
# endpoints.yml'yi kontrol et
cat endpoints.yml

# Action server'ı doğru porttan başlat
rasa run actions --port 5055
```

## 📚 Daha Fazla Bilgi

→ Detaylı dokümantasyon için: `README.md`
→ Rasa dokümantasyonu: https://rasa.com/docs

## 💡 Hızlı Test Komutları

```bash
# CLI'dan test et
rasa shell

# Tek bir mesajı test et
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender":"test", "message":"elma var mı"}'

# NLU'yu test et
rasa shell nlu
```

---

Kolay gelsin! 🚀
