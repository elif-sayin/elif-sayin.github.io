"""Site denetimi (CLAUDE.md m.4, m.6, m.7, m.9). FAIL varken commit atılmaz.

Kullanım:  python3 tools/kontrol.py
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

KOK = Path(__file__).resolve().parent.parent
DOCS = KOK / "docs"
SITE_URL = "https://elif-sayin.github.io"
AZAMI_GORSEL = 120 * 1024
METIN_UZANTILARI = {".html", ".js", ".css", ".txt", ".xml", ".svg"}

# Kişisel veri desenleri (m.6) — gerçek numara YAZILMAZ, yalnızca genel desen
KISISEL_DESENLER = [
    (r"(?<!\d)\d{11}(?!\d)", "11 haneli sayı (T.C. kimlik no olabilir)"),
    (r"(?<!\d)0?5\d{2}[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}(?!\d)", "cep telefonu numarası"),
    (r"[\w.+-]+@[\w-]+\.[\w.]+", "düz metin e-posta adresi (site.js ile birleştirilmeli)"),
    (r"(?i)\b(mahallesi|mah\.|sokak|sok\.|caddesi|cad\.|apt\.|apartmanı|daire\s*\d|kapı\s*no)", "adres bilgisi"),
    (r"(?i)öğrenci\s*no|ogrenci\s*no", "öğrenci numarası"),
    (r"(?i)instagram", "Instagram (kullanıcı kararı: yalnız LinkedIn)"),
    (r"belgeler-ham", "gizli klasöre bağlantı"),
]

# Yasak reklam / unvan dili (m.7) — yalnızca ziyaretçiye görünen metinde aranır
YASAK_DIL = [
    r"\brandevu", r"\bmuayene", r"\bfiyat", r"\bücret", r"\bkampanya", r"\bindirim",
    r"\bgaranti", r"\ben iyi\b", r"\bağrısız", r"%\s?100", r"\buzman(ı)?\b",
    r"tedavi (ediyorum|yapıyorum|ediyoruz|yapıyoruz|edilir)", r"\bmuayenehane",
    r"önce\s*/\s*sonra", r"öncesi ve sonrası", r"hasta (yorum|referans|görüş)",
    r"\bdiş hekimi\b",
]
YASAK_UNVAN = [r"\bDt\.", r"\bDr\."]  # büyük/küçük harf duyarlı

hatalar = []
uyarilar = []


def hata(dosya, mesaj):
    hatalar.append(f"{dosya.relative_to(KOK) if isinstance(dosya, Path) else dosya}: {mesaj}")


def tr_kucuk(s):
    return s.replace("I", "ı").replace("İ", "i").lower()


class Ayristirici(HTMLParser):
    BOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.yigin = []
        self.metin = []
        self.idler = set()
        self.baglantilar = []
        self.meta = {}
        self.canonical = None
        self.h1 = 0
        self.lang = None
        self.title = ""
        self.gorseller = []
        self.dis_kaynak = []
        self.yapisal = []
        self._gizli = 0  # script/style içi
        self._title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in self.BOS:
            self.yigin.append(tag)
        if "id" in a:
            if a["id"] in self.idler:
                self.yapisal.append(f"yinelenen id: {a['id']}")
            self.idler.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._title = True
        if tag in ("script", "style"):
            self._gizli += 1
        if tag == "meta":
            anahtar = a.get("property") or a.get("name")
            if anahtar:
                self.meta[anahtar] = a.get("content", "")
                if anahtar in ("description", "og:title", "og:description", "og:image:alt"):
                    self.metin.append(a.get("content", ""))
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        for ozn in ("href", "src"):
            if ozn in a and a[ozn] is not None:
                self.baglantilar.append((tag, a[ozn]))
        if tag == "img":
            self.gorseller.append(a)
            if a.get("alt"):
                self.metin.append(a["alt"])
        if tag in ("iframe", "embed", "object"):
            self.dis_kaynak.append(f"<{tag}> kullanılamaz")
        if tag == "script" and a.get("src", "").startswith(("http:", "https:", "//")):
            self.dis_kaynak.append(f"dış betik: {a['src']}")
        if tag == "link" and a.get("rel") in ("stylesheet", "preload", "preconnect") and \
                a.get("href", "").startswith(("http:", "https:", "//")):
            self.dis_kaynak.append(f"dış stil/kaynak: {a['href']}")

    def handle_endtag(self, tag):
        if tag in self.BOS:
            return
        if tag in ("script", "style"):
            self._gizli = max(0, self._gizli - 1)
        if tag == "title":
            self._title = False
        if self.yigin and self.yigin[-1] == tag:
            self.yigin.pop()
        elif tag in self.yigin:
            while self.yigin and self.yigin[-1] != tag:
                self.yapisal.append(f"kapanmamış <{self.yigin.pop()}>")
            self.yigin.pop()
        else:
            self.yapisal.append(f"fazladan </{tag}>")

    def handle_data(self, data):
        if self._title:
            self.title += data
        if not self._gizli:
            self.metin.append(data)


def yerel_yol(sayfa, adres):
    """Sayfadaki göreli/kök adresi docs/ içindeki dosyaya çevirir."""
    yol = unquote(urlparse(adres).path)
    if not yol:
        return None
    hedef = (DOCS / yol.lstrip("/")) if yol.startswith("/") else (sayfa.parent / yol)
    if yol.endswith("/") or hedef.is_dir():
        hedef = hedef / "index.html"
    return hedef


def html_denetle(sayfa, tum_idler):
    p = Ayristirici()
    p.feed(sayfa.read_text(encoding="utf-8"))
    p.close()
    for y in p.yapisal:
        hata(sayfa, f"HTML yapısı — {y}")
    for t in p.yigin:
        if t not in ("html", "body", "head"):
            hata(sayfa, f"HTML yapısı — kapanmamış <{t}>")
    if not p.lang:
        hata(sayfa, "<html lang> yok")
    if not p.title.strip():
        hata(sayfa, "<title> boş")
    if p.h1 != 1:
        hata(sayfa, f"tam bir <h1> olmalı (bulunan: {p.h1})")
    for d in p.dis_kaynak:
        hata(sayfa, f"dış kaynak yasak — {d}")
    for g in p.gorseller:
        if not g.get("alt"):
            hata(sayfa, f"<img> alt metni yok: {g.get('src')}")
        if not (g.get("width") and g.get("height")):
            uyarilar.append(f"{sayfa.relative_to(KOK)}: <img> width/height yok: {g.get('src')}")

    for tag, adres in p.baglantilar:
        if adres.startswith(("mailto:", "tel:", "data:")):
            continue
        if adres.startswith(SITE_URL):
            adres = adres[len(SITE_URL):] or "/"
        elif adres.startswith(("http:", "https:", "//")):
            continue
        if adres.startswith("#"):
            if adres[1:] and adres[1:] not in p.idler:
                hata(sayfa, f"sayfa içi bağlantı hedefi yok: {adres}")
            continue
        hedef = yerel_yol(sayfa, adres)
        if hedef and not hedef.exists():
            hata(sayfa, f"kırık bağlantı/görsel: {adres}")

    # Ana sayfalarda paylaşım etiketleri
    if sayfa.name == "index.html" or sayfa.parent.name == "notlar":
        for m in ("description", "og:title", "og:description", "og:url", "og:image"):
            if not p.meta.get(m):
                hata(sayfa, f"meta/OG etiketi eksik: {m}")
        if not p.canonical:
            hata(sayfa, "canonical bağlantı yok")
        og = p.meta.get("og:image", "")
        if og and not og.startswith(SITE_URL):
            hata(sayfa, "og:image tam adres olmalı (SITE_URL ile)")

    # Yasak dil — yalnızca görünen metin (HTML yorumları hariç)
    gorunen = tr_kucuk(" ".join(p.metin))
    gorunen_ham = " ".join(p.metin)
    istisnasiz = gorunen.replace("protetik diş tedavisi", "")
    for desen in YASAK_DIL:
        m = re.search(desen, istisnasiz)
        if m:
            hata(sayfa, f"yasak reklam/unvan dili (m.7): \"{m.group(0)}\"")
    for desen in YASAK_UNVAN:
        m = re.search(desen, gorunen_ham)
        if m:
            hata(sayfa, f"mezuniyet öncesi unvan kullanılamaz (m.7): \"{m.group(0)}\"")

    tum_idler[sayfa] = p
    return p


def metin_denetle(dosya):
    icerik = dosya.read_text(encoding="utf-8")
    if dosya.suffix == ".html":
        icerik = re.sub(r'<script type="application/ld\+json">.*?</script>', "", icerik, flags=re.S)
        icerik = re.sub(r'(content|href)="https://www\.linkedin\.com[^"]*"', "", icerik)
    for desen, ad in KISISEL_DESENLER:
        m = re.search(desen, icerik)
        if m:
            hata(dosya, f"kişisel veri şüphesi — {ad}: \"{m.group(0)}\"")


def gorsel_denetle(dosya):
    boyut = dosya.stat().st_size
    if boyut > AZAMI_GORSEL:
        hata(dosya, f"görsel {boyut // 1024} KB (sınır 120 KB)")
    try:
        from PIL import Image
    except ImportError:
        uyarilar.append("Pillow yok — EXIF denetimi atlandı (pip3 install --user pillow)")
        return
    with Image.open(dosya) as img:
        if dict(img.getexif()) or "exif" in img.info:
            hata(dosya, "EXIF üst verisi var (konum/cihaz bilgisi) — tools/gorsel.py ile temizleyin")
        if dosya.name == "og.jpg" and img.size != (1200, 630):
            hata(dosya, f"og.jpg 1200×630 olmalı (bulunan {img.size[0]}×{img.size[1]})")


def surum_denetle(ana):
    m = re.search(r'data-surum="([^"]+)"', ana.read_text(encoding="utf-8"))
    cl = KOK / "CHANGELOG.md"
    c = re.search(r"^## \[(\d+\.\d+\.\d+)\] - \d{4}-\d{2}-\d{2}", cl.read_text(encoding="utf-8"), re.M) if cl.exists() else None
    if not m:
        hata(ana, "altbilgide data-surum yok")
    elif not c:
        hata("CHANGELOG.md", "## [X.Y.Z] - YYYY-MM-DD başlığı bulunamadı")
    elif m.group(1) != c.group(1):
        hata(ana, f"sürüm uyuşmuyor: sayfa {m.group(1)}, CHANGELOG {c.group(1)}")
    for diger in (DOCS / "en" / "index.html",):
        if diger.exists() and m:
            d = re.search(r'data-surum="([^"]+)"', diger.read_text(encoding="utf-8"))
            if not d or d.group(1) != m.group(1):
                hata(diger, "sürüm Türkçe sayfayla aynı olmalı")


def main():
    if not DOCS.is_dir():
        print("docs/ klasörü yok")
        return 1
    sayfalar = {}
    for dosya in sorted(DOCS.rglob("*")):
        if not dosya.is_file():
            continue
        if dosya.suffix == ".html":
            html_denetle(dosya, sayfalar)
        if dosya.suffix in METIN_UZANTILARI:
            metin_denetle(dosya)
        if dosya.suffix.lower() in (".webp", ".jpg", ".jpeg", ".png"):
            gorsel_denetle(dosya)
        if dosya.suffix.lower() in (".jpeg", ".png", ".heic") and dosya.name != "og.jpg":
            uyarilar.append(f"{dosya.relative_to(KOK)}: WebP'ye çevrilmesi önerilir")

    surum_denetle(DOCS / "index.html")

    tr, en = DOCS / "index.html", DOCS / "en" / "index.html"
    if tr in sayfalar and en in sayfalar:
        eksik = {i for i in sayfalar[tr].idler if not i.endswith("-baslik")} - sayfalar[en].idler
        if eksik:
            hata(en, f"Türkçe sayfadaki bölümler eksik: {', '.join(sorted(eksik))}")

    for u in uyarilar:
        print("UYARI ", u)
    for h in hatalar:
        print("FAIL  ", h)
    print(f"\n{len(sayfalar)} sayfa denetlendi · {len(hatalar)} hata · {len(uyarilar)} uyarı")
    print("SONUÇ:", "FAIL" if hatalar else "PASS")
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main())
