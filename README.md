# Elif Sayın — Kişisel Site

Trakya Üniversitesi Diş Hekimliği Fakültesi öğrencisi Elif Sayın'ın akademik
portfolyo sitesi. Adres: **https://elif-sayin.github.io**

Kurallar: `CLAUDE.md` · Plan: `IS_PLANI.md` · Takip: `ILERLEME.md` · Yayın: `DAGITIM.md`

## Yapı

```
docs/            → GitHub Pages'in yayınladığı klasör (yalnızca bu klasör yayında)
  index.html     → Türkçe ana sayfa
  en/index.html  → İngilizce sürüm
  notlar/        → Ağız ve Diş Sağlığı Notları (her not ayrı sayfa)
  style.css      → tüm stil (açık / koyu tema)
  site.js        → e-posta, tema düğmesi, menü
  img/           → WebP görseller, og.jpg
tools/
  kontrol.py     → site denetimi (her değişiklikten sonra)
  gorsel.py      → fotoğrafı WebP'ye çevirir, konum/EXIF bilgisini siler
belgeler-ham/    → ham fotoğraf ve belgeler (GİZLİ — git'e girmez)
```

## Sık kullanılan komutlar

Siteyi bilgisayarda açmak:

```bash
python3 -m http.server 8000 -d docs
```

Ardından tarayıcıda `http://localhost:8000`.

Denetim (FAIL varken commit atılmaz):

```bash
python3 tools/kontrol.py
```

Yeni fotoğrafı siteye hazırlamak:

```bash
python3 tools/gorsel.py belgeler-ham/foto.jpg docs/img/ad.webp --kare --boyut 640
```

## Yol haritası

- [x] Proje iskeleti
- [x] Kontrol ve görsel araçları
- [x] Ana sayfa (Türkçe)
- [ ] Ağız ve Diş Sağlığı Notları (3 not, Elif'in bilimsel onayıyla)
- [x] İngilizce sürüm
- [ ] SEO ve paylaşım görseli
- [x] GitHub Pages'te yayın
