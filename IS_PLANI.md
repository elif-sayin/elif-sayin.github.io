# İş Planı — Elif Sayın Kişisel Sitesi

Hazırlanma: 2026-10-28 · Kurallar: `CLAUDE.md` · Takip: `ILERLEME.md`

Hedef: `https://elif-sayin.github.io` adresinde, mobil öncelikli, Türkçe +
İngilizce, statik bir akademik portfolyo sitesi. İlk yayın sürümü **v1.0.0**.

---

## Temel kararlar (gerekçeli)

| Konu | Karar | Gerekçe |
|---|---|---|
| Teknoloji | Düz HTML + tek CSS + az JS, `docs/` klasörü | Bakımı kolay, ücretsiz, hızlı; GitHub Pages doğrudan yayınlar |
| Barındırma | GitHub Pages, depo `elif-sayin/elif-sayin.github.io` | Kök adreste açılması için depo adı bu olmalı |
| Sayfa yapısı | Tek ana sayfa + her not için ayrı sayfa | Notlar WhatsApp/LinkedIn'de tek tek paylaşılabilsin |
| Boş bölümler | Kongre, akademik çalışma, gönüllülük, ödül şu an **gizli** | Boş başlık güven vermez; içerik gelince açılır |
| Unvan | "Diş Hekimliği Öğrencisi" (mezuniyete kadar) | Reklam/unvan mevzuatı, `CLAUDE.md` m.7 |
| İlgi alanları | "İlgi alanlarım" olarak 4 anabilim dalı | Kesin DUS hedefi yazmak ileride bağlayıcı görünebilir |
| Yönetim paneli | Yok | Elif kararı 2026-10-28: sadelik; güncellemeler Claude ile ya da github.com düzenleyicisinden |
| Dış kaynak | Yok (font, analitik, gömülü video yok) | KVKK; çerez bandı gerekmez |
| Görseller | Pillow ile WebP + EXIF silme (`tools/gorsel.py`) | Mac'te `cwebp` yok; Pillow `pip install --user pillow` ile kurulur |

---

## Site haritası (v1.0.0)

**Ana sayfa (`docs/index.html`)**
1. **Giriş** — Elif Sayın · Diş Hekimliği Öğrencisi · Trakya Üniversitesi · Edirne; kısa tek cümle; LinkedIn ve e-posta düğmeleri
2. **Hakkımda** — 2–3 paragraf (birlikte yazılacak), portre
3. **Eğitim** — zaman çizelgesi: Trakya Üni. Diş Hekimliği Fak. (2022 – Haziran 2027, beklenen)
4. **Klinik Stajlar** — 8 anabilim dalı etiket listesi; 1. tur tamamlandı, 2. tur sürüyor (hasta bilgisi yok)
5. ~~İlgi Alanlarım~~ — Elif kararıyla kaldırıldı (0.1.2)
6. **Dil Yeterliliği** — Türkçe (ana dil) · İngilizce — ÖSYM TıpDil 70 (2026)
7. **Ağız ve Diş Sağlığı Notları** — not kartları (başlık, kısa özet, tarih)
8. **İletişim** — e-posta, LinkedIn; konum Edirne (Instagram yok — Elif kararı)
9. **Altbilgi** — © 2026 Elif Sayın · Site yapımı: Süreyya Sayın · sürüm

*Gizli (hazır bekleyen) bölümler:* Akademik Çalışmalar · Kongre/Kurs/Sertifikalar · Gönüllülük · Ödüller/Burslar

**Notlar (`docs/notlar/`) — ilk 3 not önerisi**
1. Doğru diş fırçalama ve diş ipi kullanımı
2. Florürlü diş macunu: ne kadar, kime?
3. Çocuklarda ilk diş ve biberon çürüğü

Her notta: kaynak bağlantıları (Sağlık Bakanlığı, TDB, WHO/FDI), yazılış tarihi,
sabit "tanı ve tedavi yerine geçmez" uyarısı. Metinleri ben taslak olarak yazarım,
**Elif bilimsel doğruluğunu kontrol edip onaylar**; onaysız not yayınlanmaz.

**İngilizce sürüm (`docs/en/`)** — ana sayfanın tamamı. Notlar ilk aşamada yalnızca
Türkçe (İngilizce sayfada "Notes are available in Turkish" bağlantısı); istenirse sonra çevrilir.

---

## Fazlar

### Faz 0 — Proje iskeleti
- [x] `git init`, `.gitignore` (`belgeler-ham/`, asıl portre, `.DS_Store`)
- [x] `README.md`, `CHANGELOG.md`, `LICENSE`, `ILERLEME.md`, `DAGITIM.md`
- [x] `docs/.nojekyll`, `robots.txt`, `sitemap.xml`, `404.html`, `favicon.svg`
- [x] İlk commit

### Faz 1 — İçerik metinleri (Elif ile birlikte)
- [x] Hakkımda taslağı → Elif'in düzeltmesi → onay
- [x] Klinik Eğitim metni (hangi stajlar yapıldı/yapılıyor)
- [x] İlgi alanları cümleleri
- [x] Portre fotoğrafı → `docs/img/elif.webp` (kare, EXIF'siz)

### Faz 2 — Tasarım ve ana sayfa
- [x] Renk token'ları (açık/koyu), tipografi, düğmeler
- [x] `index.html` bölümleri, mobil menü, tema düğmesi, "içeriğe geç"
- [x] `site.js`: e-posta birleştirme, tema, yıl
- [ ] Önizleme: 390 px ve masaüstü, açık ve koyu tema → **Elif onayı**

### Faz 3 — Kontrol aracı
- [x] `tools/kontrol.py`: HTML ayrıştırma, kırık bağlantı/görsel, görsel ≤120 KB ve EXIF yok, OG etiketleri, sürüm eşleşmesi, kişisel veri deseni, yasak reklam dili (anabilim dalı adları istisna), TR/EN bölüm eşleşmesi
- [x] `tools/gorsel.py`: fotoğraf → WebP + EXIF temizleme

### Faz 4 — Ağız ve Diş Sağlığı Notları
- [ ] Not sayfa şablonu (breadcrumb, OG, uyarı kutusu, kaynaklar)
- [ ] 3 not taslağı → Elif'in bilimsel kontrolü → yayın

### Faz 5 — İngilizce sürüm
- [x] `docs/en/index.html`, dil değiştirme bağlantısı, `hreflang`

### Faz 6 — SEO ve paylaşım
- [x] `og.jpg` (1200×630), meta açıklamalar, JSON-LD `Person` (Faz 2'de öne alındı)
- [ ] WhatsApp/LinkedIn paylaşım önizlemesi kontrolü
- [ ] Lighthouse mobil ≥ 95

### Faz 7 — Yayın (Elif'in onayıyla)
- [x] Elif GitHub'da `elif-sayin.github.io` adında **public** depo açar (adımlar `DAGITIM.md`)
- [x] Uzak depo bağlanır, push (Elif onayı ile)
- [x] Settings → Pages → "Deploy from a branch" → `main` / `/docs`
- [ ] Canlı adreste son kontrol → **v1.0.0**

### Faz 8 — Sonrası (sürekli)
- Kongre, kurs, sertifika, poster geldikçe gizli bölümleri açmak (MINOR sürüm)
- Yeni notlar
- **2027 mezuniyet:** unvanın "Dt. Elif Sayın" olarak güncellenmesi (`CLAUDE.md` m.7-B)
- İsteğe bağlı: alan adı (`elifsayin.com` vb.)

---

## Metinler

Elif'in isteğiyle (2026-10-28) tüm metinler uzman gözüyle yeniden yazıldı (0.2.0).
Güncel metinlerin tek kaynağı `docs/index.html`'dir; burada kopyası tutulmaz.

---

## Elif'ten beklenenler
1. ~~Portre~~ → alındı (`belgeler-ham/IMG_1166.JPG`, gizli klasör)
2. ~~Hakkımda bilgileri~~ → alındı, taslak yukarıda: **onay / düzeltme**
3. ~~Klinik stajlar~~ → alındı
4. ~~Mezuniyet ayı~~ → Haziran 2027
5. ~~Instagram~~ → yalnız LinkedIn
6. **Not konuları:** önerilen 3 konu uygun mu? (cevap bekleniyor)
7. ~~Yönetim paneli~~ → YOK (Elif kararı 2026-10-28; güncellemeler Claude ile / github.com düzenleyicisi)
