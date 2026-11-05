"""Pick a by-hand sample per neighbourhood and fetch what the eye check needs.

Per area: 5 random listings (seeded) and 5 'most suspicious' (the 3 cheapest against their own registered deals,
then the 2 longest 'available'). Downloads the first 3 thumbnails, keeps the permit validation link, and draws one
contact sheet per area. Read-only, paced. Output: data/raw/pf/hand/ (git-ignored) + research/hand_sample.json.
"""

import json
import random
import re
import time
from datetime import date
from pathlib import Path
from statistics import median
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw

AREAS: list[str] = ["palm-jumeirah", "downtown-dubai", "dubai-marina", "jumeirah-village-circle",
                    "discovery-gardens", "international-city"]
TODAY: date = date(2026, 11, 5)
UA: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"
NEXT_DATA: re.Pattern[str] = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL)
OUT: Path = Path("data/raw/pf/hand")


def ratio(r: dict) -> float | None:
    recent = [a for d, a in r["deals"] if (TODAY - date.fromisoformat(d)).days <= 183 and a > 0]
    return r["price"] / median(recent) if len(recent) >= 3 and r["price"] else None


def stale_days(r: dict) -> int:
    return (TODAY - date.fromisoformat(r["available_from"])).days if r["available_from"] else -1


def pick(rows: list[dict], rng: random.Random) -> list[tuple[str, dict]]:
    judged = sorted((x for x in rows if ratio(x) is not None), key=lambda x: ratio(x) or 9)
    suspicious = judged[:3] + [x for x in sorted(rows, key=stale_days, reverse=True) if x not in judged[:3]][:2]
    rest = [x for x in rows if x not in suspicious]
    return [("suspicious", x) for x in suspicious] + [("random", x) for x in rng.sample(rest, 5)]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20261105)
    sample: list[dict] = []
    for area in AREAS:
        rows = json.loads(Path(f"data/raw/pf/areas/{area}.json").read_text())
        tiles: list[tuple[str, Path]] = []
        for why, r in pick(rows, rng):
            url = f"https://www.propertyfinder.ae/en/plp/rent/x-{r['id']}.html"
            html = urlopen(Request(url, headers={"User-Agent": UA}), timeout=30).read().decode()
            prop = json.loads(NEXT_DATA.search(html).group(1))["props"]["pageProps"]["propertyResult"]["property"]
            time.sleep(3)
            images = prop.get("images") or {}
            listing_images = images.get("property", []) if isinstance(images, dict) else images
            for k, im in enumerate(listing_images[:3]):
                p = OUT / f"{r['id']}_{k}.jpg"
                if not p.exists():
                    p.write_bytes(urlopen(Request(im.get("small") or im["medium"], headers={"User-Agent": UA}), timeout=30).read())
                    time.sleep(2)
                tiles.append((f"{r['id']}_{k}", p))
            rt = ratio(r)
            sample.append({
                "area": area, "why": why, "id": r["id"], "url": prop.get("share_url") or url,
                "building": r["building"], "bedrooms": r["bedrooms"], "size": r["size"], "price": r["price"],
                "vs_deals": None if rt is None else round(rt - 1, 3), "stale_days": stale_days(r),
                "verified": r["verified"], "furnished": prop.get("furnished"), "title": prop.get("title"),
                "agency": r["agency"], "permit_url": (prop.get("rera") or {}).get("permit_validation_url"),
            })
            Path("research/hand_sample.json").write_text(json.dumps(sample, indent=1, ensure_ascii=False))
        W, H, cols = 200, 140, 6
        rows_n = (len(tiles) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * W, rows_n * (H + 14)), "white")
        draw = ImageDraw.Draw(sheet)
        for n, (label, p) in enumerate(tiles):
            t = Image.open(p).convert("RGB")
            t.thumbnail((W, H))
            x, y = (n % cols) * W, (n // cols) * (H + 14)
            sheet.paste(t, (x, y))
            draw.text((x + 2, y + H), label, fill="black")
        sheet.save(OUT / f"sheet_{area}.jpg", quality=75)
        print(area, "done", flush=True)


if __name__ == "__main__":
    main()
