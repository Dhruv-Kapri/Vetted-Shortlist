"""Compare rental listings across neighbourhoods of different price tiers.

For each area: the first PAGES result pages of apartment rentals, then each listing's detail page. Every listing
is judged against ITS OWN page's registered rents (same building and size, last 6 months), which is what a person
searching sees. Read-only, one request every 3 s. Raw data: data/raw/pf/areas/<slug>.json (git-ignored).
"""

import json
import re
import sys
import time
from datetime import date
from pathlib import Path
from statistics import median
from urllib.error import HTTPError
from urllib.request import Request, urlopen

AREAS: dict[str, str] = {
    "palm-jumeirah": "Palm Jumeirah (luxury)",
    "downtown-dubai": "Downtown Dubai (luxury)",
    "dubai-marina": "Dubai Marina (upper-mid)",
    "jumeirah-village-circle": "JVC (mid)",
    "discovery-gardens": "Discovery Gardens (budget)",
    "international-city": "International City (budget)",
}
PAGES: int = 3
PAUSE_S: float = 3.0
TODAY: date = date(2026, 11, 5)
UA: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"
NEXT_DATA: re.Pattern[str] = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL)
OUT: Path = Path("data/raw/pf/areas")


def page_props(url: str) -> dict:
    html = urlopen(Request(url, headers={"User-Agent": UA}), timeout=30).read().decode()
    return json.loads(NEXT_DATA.search(html).group(1))["props"]["pageProps"]


def fetch_area(slug: str) -> list[dict]:
    path = OUT / f"{slug}.json"
    rows: list[dict] = json.loads(path.read_text()) if path.exists() else []
    if rows:
        return rows
    seen: set[str] = set()
    for page in range(1, PAGES + 1):
        url = f"https://www.propertyfinder.ae/en/rent/dubai/apartments-for-rent-{slug}.html?page={page}"
        try:
            props = [x["property"] for x in page_props(url)["searchResult"]["listings"] if x.get("property")]
        except HTTPError:
            break
        time.sleep(PAUSE_S)
        for p in props:
            lid = str(p["id"])
            if lid in seen:
                continue
            seen.add(lid)
            try:
                prop = page_props("https://www.propertyfinder.ae" + p["details_path"])["propertyResult"]["property"]
            except (HTTPError, AttributeError, KeyError):
                continue
            finally:
                time.sleep(PAUSE_S)
            rows.append({
                "id": lid, "price": p["price"]["value"], "size": p["size"]["value"], "bedrooms": p["bedrooms"],
                "building": p["location"]["full_name"].split(",")[0], "agency": p["broker"]["name"],
                "verified": bool(p["is_verified"]), "listed": p["listed_date"][:10],
                "available_from": (prop.get("rental_availability_date") or "")[:10],
                "permit_link": bool((prop.get("rera") or {}).get("permit_validation_url")),
                "deals": [(t["date"][:10], float(t["amount"])) for t in (prop.get("similar_price_transactions") or {}).get("rent") or []],
            })
            path.write_text(json.dumps(rows))
        print(slug, page, len(rows), flush=True)
    return rows


def summarise(rows: list[dict]) -> dict[str, str]:
    ratios: list[float] = []
    for r in rows:
        recent = [a for d, a in r["deals"] if (TODAY - date.fromisoformat(d)).days <= 183 and a > 0]
        if len(recent) >= 3 and r["price"]:
            ratios.append(r["price"] / median(recent))
    judged = ratios
    stale = [r for r in rows if r["available_from"] and (TODAY - date.fromisoformat(r["available_from"])).days > 45]
    with_date = [r for r in rows if r["available_from"]]
    ppsf = [r["price"] / r["size"] for r in rows if r["price"] and r["size"]]
    n = len(rows)
    pct = lambda k, d: f"{(100 * k / d):.0f}%" if d else "-"
    return {
        "listings": str(n),
        "median AED/sqft/yr": f"{median(ppsf):.0f}" if ppsf else "-",
        "judged (>=3 deals)": str(len(judged)),
        "under 75% (bait)": pct(sum(x < 0.75 for x in judged), len(judged)),
        "75-90%": pct(sum(0.75 <= x < 0.90 for x in judged), len(judged)),
        "over 125%": pct(sum(x > 1.25 for x in judged), len(judged)),
        "median asking vs deals": f"{(median(judged) - 1) * 100:+.0f}%" if judged else "-",
        "'available' >45 d ago": pct(len(stale), len(with_date)),
        "Verified": pct(sum(r["verified"] for r in rows), n),
        "permit link": pct(sum(r["permit_link"] for r in rows), n),
        "listings per agency": f"{n / max(1, len({r['agency'] for r in rows})):.1f}",
        "buildings in sample": str(len({r["building"] for r in rows})),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    slugs = sys.argv[1:] or list(AREAS)
    table: dict[str, dict[str, str]] = {AREAS[s]: summarise(fetch_area(s)) for s in slugs}
    keys = list(next(iter(table.values())))
    print("| Area | " + " | ".join(keys) + " |")
    print("|---|" + "---|" * len(keys))
    for area, row in table.items():
        print(f"| {area} | " + " | ".join(row[k] for k in keys) + " |")


if __name__ == "__main__":
    main()
