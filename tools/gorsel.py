"""Fotoğrafı siteye hazırlar: kırpar, küçültür, WebP'ye çevirir, EXIF/GPS siler.

Kullanım:
  python3 tools/gorsel.py GIRIS CIKIS.webp [--kirp X,Y,KENAR] [--kare] [--boyut 640]

  --kirp X,Y,KENAR  sol üst köşesi (X,Y) olan KENAR×KENAR kare alanı keser
  --kare            --kirp verilmezse ortadan kare keser
  --boyut           en uzun kenar (piksel)

Çıktı ≤ 120 KB olana kadar kalite düşürülür (CLAUDE.md m.4).
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

AZAMI_BAYT = 120 * 1024


def hazirla(giris, cikis, kirp=None, kare=False, boyut=640):
    img = Image.open(giris)
    img = ImageOps.exif_transpose(img)  # telefonda döndürülmüş fotoğrafı düzelt
    img = img.convert("RGB")  # EXIF/ICC dahil tüm üst veriyi bırakır

    if kirp:
        x, y, kenar = kirp
        img = img.crop((x, y, x + kenar, y + kenar))
    elif kare:
        kenar = min(img.size)
        x = (img.width - kenar) // 2
        y = (img.height - kenar) // 2
        img = img.crop((x, y, x + kenar, y + kenar))

    img.thumbnail((boyut, boyut), Image.LANCZOS)

    # Yeni, üst verisiz bir görüntüye kopyala (EXIF kesinlikle taşınmasın)
    temiz = Image.new("RGB", img.size)
    temiz.paste(img)

    Path(cikis).parent.mkdir(parents=True, exist_ok=True)
    for kalite in range(85, 39, -5):
        temiz.save(cikis, "WEBP", quality=kalite, method=6)
        if Path(cikis).stat().st_size <= AZAMI_BAYT:
            break
    boyut_kb = Path(cikis).stat().st_size / 1024
    print(f"{cikis}: {temiz.width}x{temiz.height}, {boyut_kb:.0f} KB, kalite {kalite}")
    if boyut_kb * 1024 > AZAMI_BAYT:
        print("UYARI: 120 KB sınırı aşıldı, --boyut değerini küçültün", file=sys.stderr)
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("giris")
    ap.add_argument("cikis")
    ap.add_argument("--kirp", help="X,Y,KENAR")
    ap.add_argument("--kare", action="store_true")
    ap.add_argument("--boyut", type=int, default=640)
    a = ap.parse_args()
    kirp = tuple(int(v) for v in a.kirp.split(",")) if a.kirp else None
    if kirp and len(kirp) != 3:
        ap.error("--kirp X,Y,KENAR biçiminde olmalı")
    return hazirla(a.giris, a.cikis, kirp, a.kare, a.boyut)


if __name__ == "__main__":
    sys.exit(main())
