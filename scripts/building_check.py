"""Building-wide check: every Princess Tower listing against registered deals for its own size (±10 sqft).

Prints a markdown table per offering and bedroom count, used in AUDIT.md.
"""

import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from statistics import median

RAW: Path = Path("data/raw/pf")
TODAY: date = date(2026, 11, 5)
WINDOW: dict[str, int] = {"rent": 183, "sale": 365}


def main() -> None:
    details: dict[str, dict] = json.loads((RAW / "details.json").read_text())
    deals: dict[str, set[tuple[str, int, int]]] = defaultdict(set)
    for d in details.values():
        key = "rent" if d["offering"] == "rent" else "buy"
        for t in (d.get("similar_price_transactions") or {}).get(key) or []:
            deals[d["offering"]].add((t["date"][:10], int(float(t["amount"])), int(t["size"])))
    stats: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: defaultdict(int))
    odd: list[str] = []
    for o in ("rent", "sale"):
        listings = {str(p["id"]): p for p in json.loads((RAW / f"princess_tower_{o}.json").read_text())}
        for lid, p in listings.items():
            s = stats[(o, str(p["bedrooms"]))]
            s["listings"] += 1
            size = p["size"]["value"] or 0
            d = details.get(lid) or {}
            av = (d.get("rental_availability_date") or "")[:10]
            if o == "rent" and av and (TODAY - date.fromisoformat(av)).days > 45:
                s["stale_45"] += 1
            s["verified"] += bool(p["is_verified"])
            amounts = [a for dt, a, sz in deals[o] if abs(sz - size) <= 10 and (TODAY - date.fromisoformat(dt)).days <= WINDOW[o]]
            if len(amounts) < 3:
                s["too_few_deals"] += 1
                continue
            ratio = p["price"]["value"] / median(amounts)
            s["under_75"] += ratio < 0.75
            s["75_90"] += 0.75 <= ratio < 0.90
            s["over_125"] += ratio > 1.25
            if ratio < 0.90:
                odd.append(f"{o} {lid} {p['bedrooms']}BR {size} sqft AED {p['price']['value']:,} = {ratio:.0%} of median {median(amounts):,.0f} (n={len(amounts)})")
    print("| Offering | Bedrooms | Listings | Judged (>=3 deals) | Under 75% | 75-90% | Over 125% | 'Available' >45 d ago | Verified |")
    print("|---|---|---|---|---|---|---|---|---|")
    for (o, b), s in sorted(stats.items()):
        judged = s["listings"] - s["too_few_deals"]
        stale = s["stale_45"] if o == "rent" else "-"
        print(f"| {o} | {b} | {s['listings']} | {judged} | {s['under_75']} | {s['75_90']} | {s['over_125']} | {stale} | {s['verified']} |")
    print("\nUnder 90% of median:")
    for line in odd:
        print("-", line)


if __name__ == "__main__":
    main()
