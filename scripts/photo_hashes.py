"""Download the first few public thumbnails of each listing and record a 64-bit difference hash.

Read-only, one image at a time with a pause. Images go to data/raw/pf/img/ (git-ignored);
hashes to data/raw/pf/photo_hashes.json as {listing_id: [hex hash, ...]}.
"""

import io
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image

RAW: Path = Path("data/raw/pf")
IMG: Path = RAW / "img"
PER_LISTING: int = 3
PAUSE_S: float = 2.0
UA: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"


def dhash(image: Image.Image) -> str:
    """64-bit difference hash: compares neighbouring pixels of a 9x8 greyscale thumbnail."""
    px = list(image.convert("L").resize((9, 8), Image.Resampling.LANCZOS).getdata())
    bits = [px[r * 9 + c] > px[r * 9 + c + 1] for r in range(8) for c in range(8)]
    return f"{int(''.join('1' if b else '0' for b in bits), 2):016x}"


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    out_path = RAW / "photo_hashes.json"
    hashes: dict[str, list[str]] = json.loads(out_path.read_text()) if out_path.exists() else {}
    seen: set[str] = set()
    for offering in ("rent", "sale"):
        for p in json.loads((RAW / f"princess_tower_{offering}.json").read_text()):
            lid = str(p["id"])
            if lid in seen or lid in hashes:
                continue
            seen.add(lid)
            found: list[str] = []
            for i, im in enumerate(p.get("images", [])[:PER_LISTING]):
                url = im.get("small") or im.get("medium")
                if not url:
                    continue
                data = urlopen(Request(url, headers={"User-Agent": UA}), timeout=30).read()
                (IMG / f"{lid}_{i}.jpg").write_bytes(data)
                found.append(dhash(Image.open(io.BytesIO(data))))
                time.sleep(PAUSE_S)
            hashes[lid] = found
            out_path.write_text(json.dumps(hashes))
            print(lid, len(found), flush=True)


if __name__ == "__main__":
    main()
