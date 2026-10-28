# İLERLEME (oturumlar arası iş takibi)

Son güncelleme: 2026-10-28

## Aktif plan
`IS_PLANI.md` — v1.0.0 ilk yayın. Site **0.4.1**, YAYINDA: https://elif-sayin.github.io (depo `elif-sayin/elif-sayin.github.io`, Pages: main /docs).

## Tamamlananlar
- 2026-10-28: `CLAUDE.md`, `IS_PLANI.md` hazırlandı; Elif'in bilgileri işlendi.
- 2026-10-28: Adres kararı: `https://elif-sayin.github.io` (Elif `elifsayin3` hesabını `elif-sayin` olarak yeniden adlandırdı — `DAGITIM.md` §0).
- 2026-10-28: Yönetim paneli kararı: YOK.
- 2026-10-28: Faz 0 (iskelet), Faz 1 (metinler + portre), Faz 2 (ana sayfa), Faz 3 (araçlar) bitti.
  Portre logosuz kırpıldı (önlük cebindeki "DENTAL CLINIC" logosu çıkarıldı — m.7).
  `og.jpg` ve JSON-LD Faz 6'dan öne alındı.
- 2026-10-28: Elif'in isteğiyle git geçmişi tek kayda indirildi (`55c1744`) ve GitHub'a zorla gönderildi; eski kayıtlar (ham not alıntıları) silindi.
- 2026-10-28: 0.4.1 — ortaöğretim bilgisi kaldırıldı.
- 2026-10-28: 0.4.0 — İngilizce sürüm `docs/en/` + TR/EN düğmesi, hreflang, site haritası (Faz 5 bitti).
- 2026-10-28: 0.3.0 — Elif'in renk kartelasıyla yeni tasarım (CLAUDE.md m.8.2).
- 2026-10-28: 0.2.2 — İngilizce puan yerine düzey (B2) olarak yazıldı.
- 2026-10-28: 0.2.1 — hayvan cümlesi ve "tur" ifadeleri kaldırıldı (Elif'in isteği).
- 2026-10-28: 0.2.0 — tüm metinler uzman gözüyle yeniden yazıldı (Elif'in isteği; kural CLAUDE.md m.3.6). Geçmiş yeniden tek kayda indirildi.
- 2026-10-28: 0.1.2 — "Uzmanlık için düşündüğüm alanlar" bölümü Elif'in isteğiyle kaldırıldı.
- 2026-10-28: gh 2.103.3 `~/.local/bin`'e kuruldu (SHA256 doğrulandı), `elif-sayin` olarak giriş yapıldı.
- 2026-10-28: Depo açıldı, Elif'in "sen yap" talimatıyla push edildi, Pages main /docs olarak ayarlandı.
- Tarayıcı kontrolü: 375 px açık/koyu, mobil menü, 1280 px masaüstü — sorun yok.

## Şu an
Faz 4 sırada (notlar) — Elif'in not konusu onayı bekleniyor.

## Sırada
1. Faz 4 — Ağız ve Diş Sağlığı Notları (3 not, Elif'in bilimsel onayıyla)
3. Faz 6 — kalanlar: Lighthouse, paylaşım önizleme kontrolü
4. Faz 7 — canlı sitede Lighthouse ve paylaşım önizlemesi kontrolü

## Kullanıcıdan beklenenler
- Klinik Stajlar'daki 8 anabilim dalı listesinin fakültedeki adlarla birebir aynı olduğunun teyidi
- İlk 3 not konusunun onayı

## Bilinçli ertelenenler
- Akademik çalışma / kongre / gönüllülük / ödül / notlar bölümleri: içerik yok, `index.html`'de yorum satırında hazır.
- Notların İngilizce çevirisi: v1.0.0 sonrası.

## Ortam notları
- Python 3.9.6 + Pillow 11.3.0 (`--user`). `gh` CLI ve `cwebp` yok.
- Yerel önizleme: `.claude/launch.json` → "site" (port 8000).
- Git kimliği bu depoda yerel: Elif Sayın / elif.sayin3@gmail.com.

## Son test
2026-10-28 — `python3 tools/kontrol.py`: PASS (0.2.0). Tarayıcı: 375 px açık, 1280 px koyu kontrol edildi.
