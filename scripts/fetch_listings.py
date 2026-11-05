"""Fetch the public Property Finder search pages for one building and save the raw listing JSON.

Read-only, one request per page with a pause. Output goes to data/raw/pf/ (git-ignored).
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

LOCATION_ID: str = os.environ.get("PF_LOCATION_ID", "3092")  # default: Princess Tower, Dubai Marina
SLUG: str = os.environ.get("PF_SLUG", "princess_tower")
OFFERINGS: dict[str, str] = {"rent": "c=2&rp=y", "sale": "c=1"}
UA: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"
OUT: Path = Path("data/raw/pf")
NEXT_DATA: re.Pattern[str] = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL)


def fetch_page(offering: str, page: int) -> dict:
    url = f"https://www.propertyfinder.ae/en/search?l={LOCATION_ID}&{OFFERINGS[offering]}&t=1&fu=0&ob=mr&page={page}"
    html = urlopen(Request(url, headers={"User-Agent": UA}), timeout=30).read().decode()
    match = NEXT_DATA.search(html)
    if match is None:
        raise RuntimeError(f"no __NEXT_DATA__ on {url}")
    return json.loads(match.group(1))["props"]["pageProps"]["searchResult"]


def main(offering: str, max_pages: int) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    listings: list[dict] = []
    for page in range(1, max_pages + 1):
        try:
            result = fetch_page(offering, page)
        except HTTPError as err:  # past the last page the site answers 404
            if err.code == 404:
                break
            raise
        props = [x["property"] for x in result["listings"] if x.get("property")]
        print(offering, page, len(props), result.get("meta", {}).get("total_count"), file=sys.stderr)
        if not props:
            break
        listings.extend(props)
        time.sleep(3)
    (OUT / f"{SLUG}_{offering}.json").write_text(json.dumps(listings, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8)
