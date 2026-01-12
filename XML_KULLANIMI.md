# 📋 XML Ürün Kataloğu Kullanımı

Chatbot artık **gerçek XML verisi** ile çalışıyor! Mock data yok.

## 🎯 Nasıl Çalışıyor?

### 1. XML Kaynağı

Sistem şu XML'i kullanıyor:
```
https://www.elleshoes.com/XMLExport/E66DEED5CBA14B96B8596164ECE0160C
```

Bu **Google Shopping Feed** formatında (RSS 2.0 + Google namespace).

### 2. Otomatik İndirme ve Cache

- İlk çalıştırmada XML otomatik indirilir
- `data/urunler_cache.xml` dosyasına kaydedilir
- **1 saat** boyunca cache'den okunur (hızlı)
- 1 saat sonra tekrar indirilir (güncel kalır)

### 3. Parse Edilen Bilgiler

Her ürün için şu bilgiler çıkarılır:

```python
{
    'id': '108266',
    'isim': 'Siyah Deri Erkek Kemer',
    'kategori': 'Erkek Kemer',
    'marka': 'ELLE',
    'fiyat': 1249.90,
    'indirimli_fiyat': 1998.43,  # Varsa
    'indirimli': True/False,
    'stokta': True/False,
    'renk': 'Siyah',
    'beden': '130',
    'link': 'https://...',
    'resim': 'https://...',
    'grup_id': '24980',  # Aynı ürünün farklı varyantları
}
```

## 🔧 Kendi XML'inizi Kullanmak

### Metod 1: URL Değiştir

`actions/xml_helper.py` dosyasında:

```python
# Satır 304
XML_URL = "https://sizin-siteniz.com/urunler.xml"
```

### Metod 2: Lokal Dosya

`data/urunler.xml` dosyasını oluşturun:

```xml
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
  <channel>
    <item>
      <g:id>1</g:id>
      <g:title>Ürün Adı</g:title>
      <g:price>100.00 TRY</g:price>
      <g:sale_price>80.00 TRY</g:sale_price>  <!-- Opsiyonel -->
      <g:availability>in stock</g:availability>
      <g:product_type>Kategori</g:product_type>
      <g:brand>Marka</g:brand>
      <g:color>Renk</g:color>
      <g:size>Beden</g:size>
      <g:link>https://...</g:link>
      <g:image_link>https://...</g:image_link>
      <g:item_group_id>1</g:item_group_id>
    </item>
    <!-- Daha fazla item... -->
  </channel>
</rss>
```

Sonra:
```python
katalog = UrunKatalog(xml_source="data/urunler.xml")
```

## 🎨 Desteklenen XML Formatları

### ✅ Google Shopping Feed (RSS)
Kullanımdaki format. Namespace: `http://base.google.com/ns/1.0`

### 🔄 Farklı Format İçin

Kendi XML yapınız farklıysa, `xml_helper.py`'deki `_parse_item()` fonksiyonunu özelleştirin:

```python
def _parse_item(self, item: ET.Element) -> Optional[Dict]:
    # Kendi XML yapınıza göre parse edin
    return {
        'id': item.find('urun_id').text,
        'isim': item.find('urun_adi').text,
        'fiyat': float(item.find('fiyat').text),
        # ...
    }
```

## 📊 Katalog Fonksiyonları

```python
from actions.xml_helper import katalog

# Ürün ara
urun = katalog.urun_bul("ayakkabı")

# Kategoriye göre
ayakkabi_listesi = katalog.kategoriye_gore_bul("Kadın Ayakkabı", limit=10)

# Genel arama
sonuclar = katalog.ara("siyah bot", limit=5)

# İndirimli ürünler
indirimli = katalog.indirimli_urunler(limit=10)

# Renk filtresi
siyahlar = katalog.renk_filtrele("siyah")

# Fiyat aralığı
ucuz = katalog.fiyat_araliginda(min_fiyat=100, max_fiyat=500)

# Kategoriler
tum_kategoriler = katalog.tum_kategoriler()

# Yeniden yükle (cache'i zorla güncelle)
katalog.reload()
```

## ⚙️ Konfigürasyon

### Cache Süresi Değiştir

`xml_helper.py` → `__init__`:

```python
self.cache_duration = timedelta(hours=2)  # 2 saat
self.cache_duration = timedelta(minutes=30)  # 30 dakika
```

### Cache Lokasyonu

```python
self.cache_file = "data/urunler_cache.xml"  # Varsayılan
```

## 🚀 Production İpuçları

### 1. Scheduled Update

Cron job ile XML'i düzenli güncelle:

```bash
# Her gece 2'de
0 2 * * * python -c "from actions.xml_helper import katalog; katalog.reload()"
```

### 2. Hata Yönetimi

XML yüklenemezse fallback:

```python
try:
    katalog = UrunKatalog(xml_source=XML_URL)
except:
    katalog = UrunKatalog(xml_source="data/backup_urunler.xml")
```

### 3. Performance

Büyük XML için:
- Cache'i artırın (6-12 saat)
- Sadece stokta olanları yükleyin (zaten yapılıyor)
- Database'e import edin (production için önerilir)

### 4. Database Migration

XML'den DB'ye geçiş için script:

```python
from actions.xml_helper import UrunKatalog
import psycopg2

katalog = UrunKatalog()
conn = psycopg2.connect(...)

for urun in katalog.urunler:
    cursor.execute(
        "INSERT INTO urunler VALUES (...)",
        (urun['id'], urun['isim'], ...)
    )
```

## 🧪 Test

### XML Parser Test

```python
from actions.xml_helper import UrunKatalog

# Test katalog yükle
katalog = UrunKatalog(xml_source="data/urunler.xml")

# İstatistikler
print(f"Toplam ürün: {len(katalog)}")
print(f"Kategoriler: {katalog.tum_kategoriler()}")
print(f"İndirimli: {len(katalog.indirimli_urunler(limit=999))}")

# Arama test
test_urun = katalog.urun_bul("kemer")
print(f"Test: {test_urun['isim'] if test_urun else 'Bulunamadı'}")
```

### CLI Test

```bash
# XML'i indir ve parse et
cd actions
python -c "from xml_helper import katalog; print(len(katalog), 'ürün')"
```

## 📝 XML Yapısı Gereksinimleri

### Zorunlu Alanlar:
- `g:id` - Benzersiz ürün ID
- `g:title` - Ürün adı
- `g:price` - Fiyat (`1000.00 TRY` formatında)
- `g:availability` - Stok durumu (`in stock` / `out of stock`)

### Önerilen Alanlar:
- `g:sale_price` - İndirimli fiyat
- `g:product_type` - Kategori
- `g:color` - Renk
- `g:size` - Beden
- `g:image_link` - Resim URL
- `g:link` - Ürün sayfası
- `g:item_group_id` - Varyant gruplandırma

## ❓ Sık Sorulan Sorular

### XML nerede saklanır?
`data/urunler_cache.xml` - gitignore'da, commit edilmez.

### Her çalıştırmada indirilir mi?
Hayır. 1 saat cache var. Manuel `reload()` ile güncelleyebilirsiniz.

### Kendi e-ticaret platformumu nasıl entegre ederim?
Platform XML/JSON export sağlıyorsa URL'i değiştirin. Yoksa API ile kendi XML'i generate edin.

### Stokları gerçek zamanlı günceller mi?
Hayır, XML'deki veriye göre. Gerçek zamanlı için API entegrasyonu gerekir.

### Binlerce ürün varsa yavaşlar mı?
İlk yükleme yavaş olabilir, sonrası cache'den hızlı. Production'da database önerilir.

---

Sorularınız için: Issue açın veya dokümantasyona bakın!
