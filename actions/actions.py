"""
Rasa Custom Actions - Elle Shoes E-Ticaret Chatbot
XML verisi ile entegre
"""

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import random

# XML helper'ı import et
from actions.xml_helper import katalog


class ActionUrunAra(Action):
    """Ürün arama işlemi - XML katalogdan"""

    def name(self) -> Text:
        return "action_urun_ara"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if katalog is None:
            dispatcher.utter_message(text="⚠️ Ürün kataloğu yüklenemedi. Lütfen daha sonra tekrar deneyin.")
            return []

        urun_ismi = tracker.get_slot("urun")
        kategori = tracker.get_slot("kategori")

        # Kategori araması
        if kategori:
            sonuclar = katalog.kategoriye_gore_bul(kategori, limit=5)

            if sonuclar:
                message = f"🏷️ **{kategori.title()}** kategorisinde ürünler:\n\n"
                for urun in sonuclar[:5]:
                    fiyat = urun['indirimli_fiyat'] or urun['fiyat']
                    message += f"• {urun['isim']}: {fiyat:.2f} TL"
                    if urun['indirimli']:
                        indirim_oran = ((urun['fiyat'] - urun['indirimli_fiyat']) / urun['fiyat']) * 100
                        message += f" 🔥 (%{indirim_oran:.0f} indirim)"
                    message += "\n"
            else:
                message = f"⚠️ {kategori} kategorisinde ürün bulunamadı."

            dispatcher.utter_message(text=message)
            return []

        # Ürün ismi ile arama
        if not urun_ismi:
            # Genel arama - kategorileri göster
            kategoriler = katalog.tum_kategoriler()[:5]
            message = "🔍 Hangi ürünü arıyorsunuz?\n\n📂 Kategoriler:\n"
            message += "\n".join([f"• {k}" for k in kategoriler])
            dispatcher.utter_message(text=message)
            return []

        # Ürünü bul
        urun = katalog.urun_bul(urun_ismi)

        if urun:
            fiyat = urun['indirimli_fiyat'] or urun['fiyat']

            message = f"✅ **{urun['isim']}** bulundu!\n\n"
            message += f"💰 Fiyat: {fiyat:.2f} TL"

            if urun['indirimli']:
                message += f" ~~{urun['fiyat']:.2f} TL~~"
                indirim_oran = ((urun['fiyat'] - urun['indirimli_fiyat']) / urun['fiyat']) * 100
                message += f" 🔥 %{indirim_oran:.0f} İNDİRİM!"

            message += f"\n🏷️ Kategori: {urun['kategori']}"
            message += f"\n🎨 Renk: {urun['renk']}"
            message += f"\n📏 Beden: {urun['beden']}"
            message += f"\n📦 Stok: {'Stokta var ✓' if urun['stokta'] else 'Stokta yok ✗'}"
            message += f"\n\n🔗 [Ürünü Görüntüle]({urun['link']})"
            message += f"\n\nSepete eklemek ister misiniz?"

            # Aynı gruptaki diğer varyantları göster
            varyantlar = katalog.grup_urunleri(urun['grup_id'])
            if len(varyantlar) > 1:
                diger_renkler = set(v['renk'] for v in varyantlar if v['id'] != urun['id'])
                if diger_renkler:
                    message += f"\n\n🎨 Diğer renkler: {', '.join(list(diger_renkler)[:3])}"

        else:
            # Benzer ürünler öner
            sonuclar = katalog.ara(urun_ismi, limit=3)

            if sonuclar:
                message = f"❌ '{urun_ismi}' bulunamadı. Şunlara bakabilirsiniz:\n\n"
                for urun in sonuclar:
                    fiyat = urun['indirimli_fiyat'] or urun['fiyat']
                    message += f"• {urun['isim']}: {fiyat:.2f} TL\n"
            else:
                message = f"❌ '{urun_ismi}' için sonuç bulunamadı."

        dispatcher.utter_message(text=message)
        return [SlotSet("urun", urun_ismi if urun else None)]


class ActionFiyatGetir(Action):
    """Ürün fiyat sorgulama"""

    def name(self) -> Text:
        return "action_fiyat_getir"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if katalog is None:
            dispatcher.utter_message(text="⚠️ Fiyat bilgisi alınamıyor.")
            return []

        urun_ismi = tracker.get_slot("urun")

        if not urun_ismi:
            dispatcher.utter_message(text="🤔 Hangi ürünün fiyatını öğrenmek istersiniz?")
            return []

        urun = katalog.urun_bul(urun_ismi)

        if urun:
            fiyat = urun['indirimli_fiyat'] or urun['fiyat']
            message = f"💰 **{urun['isim']}**: {fiyat:.2f} TL"

            if urun['indirimli']:
                message += f" ~~{urun['fiyat']:.2f} TL~~"
                indirim_oran = ((urun['fiyat'] - urun['indirimli_fiyat']) / urun['fiyat']) * 100
                message += f" 🔥 (%{indirim_oran:.0f} indirim!)"
        else:
            message = f"❌ {urun_ismi} ürünü bulunamadı."

        dispatcher.utter_message(text=message)
        return []


class ActionStokKontrol(Action):
    """Stok durumu kontrolü"""

    def name(self) -> Text:
        return "action_stok_kontrol"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if katalog is None:
            dispatcher.utter_message(text="⚠️ Stok bilgisi alınamıyor.")
            return []

        urun_ismi = tracker.get_slot("urun")

        if not urun_ismi:
            dispatcher.utter_message(text="📦 Hangi ürünün stoğunu kontrol etmek istersiniz?")
            return []

        urun = katalog.urun_bul(urun_ismi)

        if urun:
            if urun['stokta']:
                message = f"✅ **{urun['isim']}** stokta mevcut!"

                # Varyant bilgisi
                varyantlar = katalog.grup_urunleri(urun['grup_id'])
                if len(varyantlar) > 1:
                    message += f"\n\n📦 {len(varyantlar)} farklı varyant mevcut"
                    renkler = set(v['renk'] for v in varyantlar)
                    message += f"\n🎨 Renkler: {', '.join(list(renkler)[:5])}"
            else:
                message = f"❌ **{urun['isim']}** şu anda stokta yok."

                # Alternatif öner
                kategori_urunler = katalog.kategoriye_gore_bul(urun['kategori'], limit=2)
                if kategori_urunler:
                    message += "\n\n💡 Benzer ürünler:"
                    for alt_urun in kategori_urunler[:2]:
                        if alt_urun['id'] != urun['id'] and alt_urun['stokta']:
                            message += f"\n• {alt_urun['isim']}"
                            break
        else:
            message = f"❌ {urun_ismi} ürünü bulunamadı."

        dispatcher.utter_message(text=message)
        return []


class ActionSepeteEkle(Action):
    """Ürünü sepete ekleme"""

    def name(self) -> Text:
        return "action_sepete_ekle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if katalog is None:
            dispatcher.utter_message(text="⚠️ Sepet işlemi yapılamıyor.")
            return []

        urun_ismi = tracker.get_slot("urun")
        miktar = tracker.get_slot("miktar") or 1
        mevcut_sepet = tracker.get_slot("sepet") or []

        if not urun_ismi:
            dispatcher.utter_message(text="🛒 Hangi ürünü eklemek istersiniz?")
            return []

        urun = katalog.urun_bul(urun_ismi)

        if not urun:
            dispatcher.utter_message(text=f"❌ {urun_ismi} ürünü bulunamadı.")
            return []

        if not urun['stokta']:
            dispatcher.utter_message(text=f"⚠️ Üzgünüm, **{urun['isim']}** stokta yok.")
            return []

        # Fiyat hesapla
        birim_fiyat = urun['indirimli_fiyat'] or urun['fiyat']
        toplam_fiyat = birim_fiyat * miktar

        # Sepete ekle
        sepet_item = {
            "urun_id": urun['id'],
            "isim": urun['isim'],
            "renk": urun['renk'],
            "beden": urun['beden'],
            "miktar": miktar,
            "birim_fiyat": birim_fiyat,
            "toplam": toplam_fiyat,
            "resim": urun['resim'],
            "link": urun['link']
        }

        mevcut_sepet.append(sepet_item)

        message = (f"✅ **{urun['isim']}** sepete eklendi!\n"
                  f"   🎨 {urun['renk']} - 📏 {urun['beden']}\n"
                  f"   💰 {toplam_fiyat:.2f} TL\n\n"
                  f"🛒 Sepetinizde {len(mevcut_sepet)} ürün var.\n"
                  f"'Sepetimi göster' diyerek görüntüleyebilirsiniz.")

        dispatcher.utter_message(text=message)

        return [
            SlotSet("sepet", mevcut_sepet),
            SlotSet("miktar", None)
        ]


class ActionSepetGoster(Action):
    """Sepet içeriğini gösterme"""

    def name(self) -> Text:
        return "action_sepet_goster"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sepet = tracker.get_slot("sepet") or []

        if not sepet:
            dispatcher.utter_message(response="utter_sepet_bos")
            return []

        message = "🛒 **Sepetiniz:**\n\n"
        toplam = 0

        for idx, item in enumerate(sepet, 1):
            message += (f"{idx}. **{item['isim']}**\n"
                       f"   🎨 {item['renk']} - 📏 {item['beden']}\n"
                       f"   {item['miktar']} adet × {item['birim_fiyat']:.2f} TL = "
                       f"**{item['toplam']:.2f} TL**\n\n")
            toplam += item['toplam']

        message += f"💰 **Toplam: {toplam:.2f} TL**\n\n"
        message += "Siparişi tamamlamak için 'siparişi tamamla' yazabilirsiniz."

        dispatcher.utter_message(text=message)
        return []


class ActionSiparisOlustur(Action):
    """Sipariş oluşturma"""

    def name(self) -> Text:
        return "action_siparis_olustur"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sepet = tracker.get_slot("sepet") or []

        if not sepet:
            dispatcher.utter_message(text="⚠️ Sepetiniz boş. Önce ürün eklemelisiniz.")
            return []

        # Sipariş numarası oluştur
        siparis_no = f"ES{random.randint(100000, 999999)}"

        toplam = sum(item['toplam'] for item in sepet)

        # Kargo ücretsiz (Elle Shoes'da genelde ücretsiz)
        kargo = 0 if toplam > 500 else 29.90
        genel_toplam = toplam + kargo

        message = (f"✅ **Siparişiniz Oluşturuldu!**\n\n"
                  f"📦 Sipariş No: **{siparis_no}**\n"
                  f"💰 Ürünler: {toplam:.2f} TL\n"
                  f"🚚 Kargo: {kargo:.2f} TL")

        if kargo == 0:
            message += " (ÜCRETSİZ!)"

        message += (f"\n━━━━━━━━━━━━━━━━━\n"
                   f"💳 **Toplam: {genel_toplam:.2f} TL**\n\n"
                   f"🚚 Tahmini teslimat: 2-3 iş günü\n"
                   f"📍 Kargo takibi için: '{siparis_no}' numarasını kullanın")

        dispatcher.utter_message(text=message)

        # Sepeti temizle
        return [
            SlotSet("sepet", []),
            SlotSet("siparis_no", siparis_no)
        ]


class ActionSiparisTakip(Action):
    """Sipariş takibi"""

    def name(self) -> Text:
        return "action_siparis_takip"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        siparis_no = tracker.get_slot("siparis_no")

        if not siparis_no:
            dispatcher.utter_message(
                text="🔍 Sipariş numaranızı söyleyebilir misiniz? (Örn: ES123456)"
            )
            return []

        # Mock sipariş durumu (gerçekte API'den gelecek)
        durumlar = [
            ("📦 Siparişiniz hazırlanıyor", "Ürünleriniz paketleniyor"),
            ("🚚 Kargoya verildi", "DHL ile yola çıktı"),
            ("✈️ Dağıtım merkezinde", "Şubenizdeki depoya ulaştı"),
            ("🚗 Kurye ile yolda", "Bugün teslim edilecek")
        ]

        durum, aciklama = random.choice(durumlar)

        message = (f"📍 **Sipariş Durumu**\n\n"
                  f"📦 Sipariş No: **{siparis_no}**\n"
                  f"🔄 Durum: {durum}\n"
                  f"ℹ️ {aciklama}\n\n"
                  f"⏰ Tahmini teslimat: Yarın 18:00'a kadar")

        dispatcher.utter_message(text=message)
        return []


class ActionOneriVer(Action):
    """Ürün önerisi - İndirimli ve popüler ürünler"""

    def name(self) -> Text:
        return "action_oneri_ver"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if katalog is None:
            dispatcher.utter_message(text="⚠️ Öneri sistemi şu an çalışmıyor.")
            return []

        # İndirimli ürünleri getir
        indirimli = katalog.indirimli_urunler(limit=5)

        if indirimli:
            message = "🔥 **İndirimli Ürünler:**\n\n"

            for urun in indirimli:
                indirim_oran = ((urun['fiyat'] - urun['indirimli_fiyat']) / urun['fiyat']) * 100
                message += (f"• **{urun['isim']}**\n"
                           f"  {urun['indirimli_fiyat']:.2f} TL "
                           f"~~{urun['fiyat']:.2f} TL~~ "
                           f"(%{indirim_oran:.0f} indirim)\n\n")

            message += "\nHangisini incelemek istersiniz?"
        else:
            message = "💡 Şu anda aktif indirim bulunmuyor."

        dispatcher.utter_message(text=message)
        return []
