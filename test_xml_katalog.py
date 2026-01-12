"""
XML Katalog Test Script
Elle Shoes XML'inin başarıyla yüklendiğini test eder
"""

import sys
import os

# actions klasörünü Python path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'actions'))

from xml_helper import UrunKatalog

def test_katalog():
    """Katalog fonksiyonlarını test eder"""

    print("=" * 60)
    print("🧪 XML KATALOG TEST")
    print("=" * 60)

    # Elle Shoes XML URL
    xml_url = "https://www.elleshoes.com/XMLExport/E66DEED5CBA14B96B8596164ECE0160C"

    print(f"\n📥 XML yükleniyor: {xml_url[:50]}...")

    try:
        katalog = UrunKatalog(xml_source=xml_url)
        print(f"✅ Katalog yüklendi!")
    except Exception as e:
        print(f"❌ Hata: {e}")
        return

    # İstatistikler
    print("\n" + "=" * 60)
    print("📊 KATALOG İSTATİSTİKLERİ")
    print("=" * 60)
    print(f"Toplam ürün: {len(katalog)}")

    # Kategoriler
    kategoriler = katalog.tum_kategoriler()
    print(f"\n📂 Kategoriler ({len(kategoriler)} adet):")
    for kat in kategoriler[:10]:
        count = len(katalog.kategoriye_gore_bul(kat, limit=9999))
        print(f"  • {kat}: {count} ürün")
    if len(kategoriler) > 10:
        print(f"  ... ve {len(kategoriler) - 10} kategori daha")

    # Markalar
    markalar = katalog.tum_markalar()
    print(f"\n🏷️ Markalar: {', '.join(markalar)}")

    # Renkler
    renkler = katalog.tum_renkler()
    print(f"\n🎨 Renkler ({len(renkler)} adet): {', '.join(renkler[:10])}")
    if len(renkler) > 10:
        print(f"   ... ve {len(renkler) - 10} renk daha")

    # İndirimli ürünler
    indirimli = katalog.indirimli_urunler(limit=999)
    if indirimli:
        print(f"\n🔥 İndirimli ürün: {len(indirimli)} adet")
        ortalama_indirim = sum(
            ((u['fiyat'] - u['indirimli_fiyat']) / u['fiyat'] * 100)
            for u in indirimli
        ) / len(indirimli)
        print(f"   Ortalama indirim: %{ortalama_indirim:.1f}")

    # Test aramaları
    print("\n" + "=" * 60)
    print("🔍 TEST ARAMALARI")
    print("=" * 60)

    test_aramalar = ["kemer", "terlik", "ayakkabı", "çanta", "bot"]

    for arama in test_aramalar:
        sonuc = katalog.urun_bul(arama)
        if sonuc:
            fiyat = sonuc['indirimli_fiyat'] or sonuc['fiyat']
            print(f"\n✅ '{arama}' → {sonuc['isim']}")
            print(f"   💰 {fiyat:.2f} TL | 🎨 {sonuc['renk']} | 📏 {sonuc['beden']}")

            # Varyantlar
            varyantlar = katalog.grup_urunleri(sonuc['grup_id'])
            if len(varyantlar) > 1:
                print(f"   📦 {len(varyantlar)} varyant mevcut")
        else:
            print(f"\n❌ '{arama}' → Bulunamadı")

    # Kategori araması
    print("\n" + "=" * 60)
    print("🏷️ KATEGORİ ARAMASI")
    print("=" * 60)

    test_kategori = "Kadın"
    sonuclar = katalog.kategoriye_gore_bul(test_kategori, limit=3)
    print(f"\n'{test_kategori}' kategorisinde {len(sonuclar)} ürün:")

    for urun in sonuclar:
        fiyat = urun['indirimli_fiyat'] or urun['fiyat']
        indirim_str = ""
        if urun['indirimli']:
            indirim_oran = ((urun['fiyat'] - urun['indirimli_fiyat']) / urun['fiyat']) * 100
            indirim_str = f" 🔥 %{indirim_oran:.0f} indirim"
        print(f"  • {urun['isim']}: {fiyat:.2f} TL{indirim_str}")

    # Fiyat aralığı
    print("\n" + "=" * 60)
    print("💰 FİYAT ARALIĞI")
    print("=" * 60)

    ucuz = katalog.fiyat_araliginda(0, 1000)
    orta = katalog.fiyat_araliginda(1000, 2500)
    pahali = katalog.fiyat_araliginda(2500, 999999)

    print(f"0-1000 TL: {len(ucuz)} ürün")
    print(f"1000-2500 TL: {len(orta)} ürün")
    print(f"2500+ TL: {len(pahali)} ürün")

    # Örnek ürün detayı
    print("\n" + "=" * 60)
    print("📄 ÖRNEK ÜRÜN DETAYI")
    print("=" * 60)

    ornek = katalog.urunler[0] if katalog.urunler else None
    if ornek:
        print(f"\nID: {ornek['id']}")
        print(f"İsim: {ornek['isim']}")
        print(f"Kategori: {ornek['kategori']}")
        print(f"Marka: {ornek['marka']}")
        print(f"Fiyat: {ornek['fiyat']:.2f} TL")
        if ornek['indirimli']:
            print(f"İndirimli Fiyat: {ornek['indirimli_fiyat']:.2f} TL")
        print(f"Renk: {ornek['renk']}")
        print(f"Beden: {ornek['beden']}")
        print(f"Stokta: {'✓ Evet' if ornek['stokta'] else '✗ Hayır'}")
        print(f"Link: {ornek['link']}")
        print(f"Grup ID: {ornek['grup_id']}")

    print("\n" + "=" * 60)
    print("✅ TEST TAMAMLANDI")
    print("=" * 60)


if __name__ == "__main__":
    test_katalog()
