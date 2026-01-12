"""
XML Ürün Kataloğu Yönetimi - Google Shopping Feed
Elle Shoes XML formatı için özelleştirilmiş parser
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
import os
import urllib.request
from datetime import datetime, timedelta


class UrunKatalog:
    """Google Shopping Feed (RSS) formatındaki XML ürün kataloğu yöneticisi"""

    # Google namespace
    NAMESPACES = {'g': 'http://base.google.com/ns/1.0'}

    def __init__(self, xml_source: str = "data/urunler.xml"):
        """
        Args:
            xml_source: XML dosya yolu VEYA URL
        """
        self.xml_source = xml_source
        self.urunler = []
        self.cache_file = "data/urunler_cache.xml"
        self.cache_duration = timedelta(hours=1)  # 1 saat cache
        self.yukle()

    def yukle(self):
        """XML'i okur - URL ise indirir, dosya ise okur"""
        xml_path = self._get_xml_path()

        if not os.path.exists(xml_path):
            raise FileNotFoundError(f"XML dosyası bulunamadı: {xml_path}")

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            self.urunler = []

            # RSS/channel/item yapısı
            channel = root.find('channel')
            if channel is None:
                raise Exception("RSS channel bulunamadı")

            items = channel.findall('item')
            print(f"📦 {len(items)} ürün varyantı bulundu...")

            for item in items:
                urun = self._parse_item(item)
                if urun and urun['stokta']:
                    self.urunler.append(urun)

            print(f"✅ {len(self.urunler)} stokta ürün yüklendi")

        except ET.ParseError as e:
            raise Exception(f"XML parse hatası: {e}")

    def _get_xml_path(self) -> str:
        """XML kaynağını belirler - URL ise indirir"""
        if self.xml_source.startswith('http'):
            # URL - cache kontrolü
            if self._cache_valid():
                print("📂 Cache'den yükleniyor...")
                return self.cache_file
            else:
                print("🌐 XML indiriliyor...")
                self._download_xml()
                return self.cache_file
        else:
            # Lokal dosya
            return self.xml_source

    def _cache_valid(self) -> bool:
        """Cache'in geçerli olup olmadığını kontrol eder"""
        if not os.path.exists(self.cache_file):
            return False

        cache_time = datetime.fromtimestamp(os.path.getmtime(self.cache_file))
        return datetime.now() - cache_time < self.cache_duration

    def _download_xml(self):
        """XML'i URL'den indirir"""
        try:
            urllib.request.urlretrieve(self.xml_source, self.cache_file)
            print("✅ XML indirildi")
        except Exception as e:
            raise Exception(f"XML indirme hatası: {e}")

    def _parse_item(self, item: ET.Element) -> Optional[Dict]:
        """Tek bir item'i parse eder"""
        try:
            # Fiyat parse (örn: "1249.90 TRY" -> 1249.90)
            fiyat_text = self._get_g_text(item, 'price', '0 TRY')
            fiyat = float(fiyat_text.replace(' TRY', '').strip())

            # İndirimli fiyat varsa
            sale_price_text = self._get_g_text(item, 'sale_price')
            if sale_price_text:
                indirimli_fiyat = float(sale_price_text.replace(' TRY', '').strip())
            else:
                indirimli_fiyat = None

            # Stok kontrolü
            availability = self._get_g_text(item, 'availability', 'out of stock')
            stokta = availability.lower() == 'in stock'

            return {
                'id': self._get_g_text(item, 'id'),
                'isim': self._get_g_text(item, 'title'),
                'aciklama': self._get_g_text(item, 'description'),
                'kategori': self._get_g_text(item, 'product_type'),
                'google_kategori': self._get_g_text(item, 'google_product_category'),
                'link': self._get_g_text(item, 'link'),
                'resim': self._get_g_text(item, 'image_link'),
                'marka': self._get_g_text(item, 'brand'),
                'fiyat': fiyat,
                'indirimli_fiyat': indirimli_fiyat,
                'indirimli': indirimli_fiyat is not None,
                'stokta': stokta,
                'mpn': self._get_g_text(item, 'mpn'),
                'renk': self._get_g_text(item, 'color'),
                'beden': self._get_g_text(item, 'size'),
                'grup_id': self._get_g_text(item, 'item_group_id'),
                'gtin': self._get_g_text(item, 'gtin'),
            }

        except Exception as e:
            print(f"⚠️ Item parse hatası: {e}")
            return None

    def _get_g_text(self, element: ET.Element, tag: str, default: str = "") -> str:
        """Google namespace'li tag'den text okur"""
        child = element.find(f'g:{tag}', self.NAMESPACES)
        return child.text.strip() if child is not None and child.text else default

    def urun_bul(self, isim: str) -> Optional[Dict]:
        """
        İsme göre ürün bulur (case-insensitive, fuzzy match)

        Args:
            isim: Ürün ismi

        Returns:
            Ürün dict veya None
        """
        isim_lower = isim.lower()

        # Tam eşleşme
        for urun in self.urunler:
            if urun['isim'].lower() == isim_lower:
                return urun

        # Kısmi eşleşme
        for urun in self.urunler:
            if isim_lower in urun['isim'].lower():
                return urun

        # Kelime bazlı eşleşme
        isim_words = isim_lower.split()
        for urun in self.urunler:
            urun_words = urun['isim'].lower().split()
            if any(word in urun_words for word in isim_words):
                return urun

        return None

    def kategoriye_gore_bul(self, kategori: str, limit: int = 10) -> List[Dict]:
        """
        Kategoriye göre ürün listesi döner

        Args:
            kategori: Kategori ismi
            limit: Maksimum sonuç sayısı

        Returns:
            Ürün listesi
        """
        kategori_lower = kategori.lower()
        sonuclar = []

        for urun in self.urunler:
            if (kategori_lower in urun['kategori'].lower() or
                kategori_lower in urun['google_kategori'].lower()):
                sonuclar.append(urun)

                if len(sonuclar) >= limit:
                    break

        return sonuclar

    def ara(self, anahtar: str, limit: int = 10) -> List[Dict]:
        """
        Genel arama - isim, kategori, renk, markada arar

        Args:
            anahtar: Arama kelimesi
            limit: Maksimum sonuç

        Returns:
            Ürün listesi
        """
        anahtar_lower = anahtar.lower()
        sonuclar = []

        for urun in self.urunler:
            if (anahtar_lower in urun['isim'].lower() or
                anahtar_lower in urun['kategori'].lower() or
                anahtar_lower in urun['renk'].lower() or
                anahtar_lower in urun['marka'].lower()):

                sonuclar.append(urun)

                if len(sonuclar) >= limit:
                    break

        return sonuclar

    def indirimli_urunler(self, limit: int = 10) -> List[Dict]:
        """
        İndirimli ürünleri döner

        Args:
            limit: Maksimum sonuç

        Returns:
            İndirimli ürün listesi
        """
        indirimli = [u for u in self.urunler if u['indirimli']]

        # İndirim yüzdesine göre sırala
        indirimli.sort(
            key=lambda x: ((x['fiyat'] - x['indirimli_fiyat']) / x['fiyat']) * 100,
            reverse=True
        )

        return indirimli[:limit]

    def grup_urunleri(self, grup_id: str) -> List[Dict]:
        """
        Aynı gruba ait tüm varyantları döner (farklı renk/beden)

        Args:
            grup_id: item_group_id

        Returns:
            Ürün varyantları
        """
        return [u for u in self.urunler if u['grup_id'] == grup_id]

    def renk_filtrele(self, renk: str) -> List[Dict]:
        """Renge göre filtreler"""
        renk_lower = renk.lower()
        return [u for u in self.urunler if renk_lower in u['renk'].lower()]

    def beden_filtrele(self, beden: str) -> List[Dict]:
        """Bedene göre filtreler"""
        return [u for u in self.urunler if beden in u['beden']]

    def fiyat_araliginda(self, min_fiyat: float = 0, max_fiyat: float = float('inf')) -> List[Dict]:
        """Fiyat aralığında ürün arar"""
        return [
            u for u in self.urunler
            if min_fiyat <= (u['indirimli_fiyat'] or u['fiyat']) <= max_fiyat
        ]

    def tum_kategoriler(self) -> List[str]:
        """Tüm benzersiz kategorileri döner"""
        kategoriler = set()
        for urun in self.urunler:
            if urun['kategori']:
                kategoriler.add(urun['kategori'])
        return sorted(list(kategoriler))

    def tum_markalar(self) -> List[str]:
        """Tüm benzersiz markaları döner"""
        markalar = set(u['marka'] for u in self.urunler if u['marka'])
        return sorted(list(markalar))

    def tum_renkler(self) -> List[str]:
        """Tüm benzersiz renkleri döner"""
        renkler = set(u['renk'] for u in self.urunler if u['renk'])
        return sorted(list(renkler))

    def reload(self):
        """XML'i yeniden yükler"""
        # Cache'i zorla güncelle
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        self.yukle()

    def __len__(self):
        """Ürün sayısını döner"""
        return len(self.urunler)

    def __repr__(self):
        return f"<UrunKatalog: {len(self.urunler)} ürün>"


# Global instance - XML URL ile
# Elle Shoes XML URL'i
XML_URL = "https://www.elleshoes.com/XMLExport/E66DEED5CBA14B96B8596164ECE0160C"

try:
    print("🔄 Ürün kataloğu yükleniyor...")
    katalog = UrunKatalog(xml_source=XML_URL)
    print(f"✅ Katalog hazır: {len(katalog)} ürün")
except Exception as e:
    print(f"⚠️ XML yükleme hatası: {e}")
    print("ℹ️ Fallback: Lokal XML dosyası deneniyor...")
    try:
        katalog = UrunKatalog(xml_source="data/urunler.xml")
    except:
        katalog = None
        print("❌ Katalog yüklenemedi!")
