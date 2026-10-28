# Yayın (GitHub Pages)

Hedef adres: **https://elif-sayin.github.io** · GitHub hesabı: `elif-sayin`

Push ve yayın kararı Elif'indir; her push öncesi onay alınır.

## 0. GitHub hesabı (Elif kararı 2026-10-28)

Kişisel sitenin adresi her zaman `<kullanıcı-adı>.github.io` olur. Elif, adreste "3"
olmasın diye `elifsayin3` hesabının adını **`elif-sayin`** yaptı (`elifsayin` adı 2020'den
beri eski bir hesapta dolu). Site bu hesapta yayınlanır.

Not: kullanıcı adı yeniden değiştirilirse adres de değişir ve eski `github.io` adresi
YÖNLENDİRİLMEZ — paylaşılmış bağlantılar kırılır. Bu yüzden ad bundan sonra sabit tutulur.
Hesapta **iki adımlı doğrulama (2FA)** açılması önerilir.

## 1. Depoyu açmak (bir kez — Elif yapar)

1. https://github.com/new adresine git (elif-sayin hesabıyla giriş yapılmış olmalı).
2. **Repository name:** tam olarak `elif-sayin.github.io` yaz.
   Başka bir ad verilirse site `https://elif-sayin.github.io/<ad>/` altında açılır.
3. **Public** seç (ücretsiz GitHub Pages için gerekli).
4. "Add a README", ".gitignore", "license" seçeneklerinin HİÇBİRİNİ işaretleme
   (bu dosyalar zaten projede var; işaretlenirse ilk push çakışır).
5. **Create repository**.

## 2. Bilgisayardaki projeyi depoya bağlamak (bir kez)

```bash
git remote add origin https://github.com/elif-sayin/elif-sayin.github.io.git
```

```bash
git push -u origin main
```

İlk push'ta GitHub kullanıcı adı ve şifre yerine **token** ister:
GitHub → Settings → Developer settings → Personal access tokens → Fine-grained →
yalnızca bu depo, "Contents: Read and write". Token'ı kimseyle (Claude dahil) paylaşma;
macOS anahtar zinciri bir kez girildikten sonra hatırlar.

## 3. Pages'i açmak (bir kez)

Depo → **Settings** → **Pages** →
- Source: **Deploy from a branch**
- Branch: **main**, klasör: **/docs** → **Save**

1–2 dakika sonra site https://elif-sayin.github.io adresinde açılır.
"Enforce HTTPS" kutusu işaretli olmalı.

## 4. Sonraki güncellemeler

```bash
python3 tools/kontrol.py
```

Kontrol geçtiyse (Elif onayıyla):

```bash
git push
```

## 5. Google Search Console

Doğrulama dosyası `docs/googlef5187027f5eb942f.html` (2026-10-29). Google'ın
verdiği dosya **deponun köküne değil `docs/` klasörüne** konmalıdır; site yalnızca
`docs/`'tan yayınlanır. Dosya silinirse doğrulama düşer. Doğrulandıktan sonra
Search Console → Site haritaları → `sitemap.xml` gönderilir.

## 6. İleride gerçek alan adı (ör. elifsayin.com)

1. Alan adını bir kayıt firmasından al.
2. `docs/CNAME` dosyasına yalnızca alan adını yaz (`elifsayin.com`).
3. DNS'te dört A kaydı: `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153`, `185.199.111.153`; `www` için CNAME → `elif-sayin.github.io`.
4. Settings → Pages → Custom domain alanına alan adını yaz, "Enforce HTTPS".
5. Sitenin adresi geçen üç dosyayı güncelle: `docs/index.html` (ve `docs/en/index.html`),
   `docs/robots.txt`, `docs/sitemap.xml` (`CLAUDE.md` m.4).
