"""Fetch the public detail page of each audited listing and keep the parts a searcher can see.

Audit set: 2-bedroom listings in the common 1,181-1,189 sqft layout, rent and sale (like for like).
Read-only, one request every 3 s. Output: data/raw/pf/details.json (git-ignored).
"""

import json
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

RAW: Path = Path("data/raw/pf")
UA: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"
NEXT_DATA: re.Pattern[str] = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL)
SIZE_RANGE: tuple[int, int] = (1181, 1189)


def in_audit(p: dict) -> bool:
    return str(p["bedrooms"]) == "2" and SIZE_RANGE[0] <= (p["size"]["value"] or 0) <= SIZE_RANGE[1]


def main(everything: bool) -> None:
    out_path = RAW / "details.json"
    details: dict[str, dict] = json.loads(out_path.read_text()) if out_path.exists() else {}
    for offering in ("rent", "sale"):
        for p in {x["id"]: x for x in json.loads((RAW / f"princess_tower_{offering}.json").read_text())}.values():
            lid = str(p["id"])
            if (not everything and not in_audit(p)) or lid in details:
                continue
            url = "https://www.propertyfinder.ae" + p["details_path"]
            try:
                html = urlopen(Request(url, headers={"User-Agent": UA}), timeout=30).read().decode()
            except HTTPError as err:  # removed since the search was fetched
                details[lid] = {"offering": offering, "http_status": err.code}
                continue
            pp = json.loads(NEXT_DATA.search(html).group(1))["props"]["pageProps"]
            prop = pp["propertyResult"]["property"]
            details[lid] = {
                "offering": offering,
                "http_status": 200,
                "is_available_page": pp.get("isAvailable"),
                "rera": prop.get("rera"),
                "rental_availability_date": prop.get("rental_availability_date"),
                "similar_price_transactions": prop.get("similar_price_transactions"),
                "price_comparisons": pp.get("priceComparisonsData"),
                "regulatory_details": prop.get("regulatory_details"),
                "description": prop.get("description"),
            }
            out_path.write_text(json.dumps(details, ensure_ascii=False))
            print(offering, lid, flush=True)
            time.sleep(3)


if __name__ == "__main__":
    main(everything="--all" in sys.argv)
