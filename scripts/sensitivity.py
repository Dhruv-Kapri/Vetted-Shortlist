"""How many listings would count as 'bait' at different thresholds, per area and building.

Each listing is judged against its own page's registered rents (same building and size, last 6 months, >= 3 deals).
"""

import json
from datetime import date
from pathlib import Path
from statistics import median

TODAY: date = date(2026, 11, 5)
THRESHOLDS: list[float] = [0.75, 0.80, 0.85, 0.90]
SOURCES: dict[str, str] = {
    "Palm Jumeirah": "areas/palm-jumeirah.json", "Downtown Dubai": "areas/downtown-dubai.json",
    "Dubai Marina": "areas/dubai-marina.json", "JVC": "areas/jumeirah-village-circle.json",
    "Discovery Gardens": "areas/discovery-gardens.json", "International City": "areas/international-city.json",
}


def ratios_from_areas(path: Path) -> list[float]:
    out: list[float] = []
    for r in json.loads(path.read_text()):
        recent = [a for d, a in r["deals"] if (TODAY - date.fromisoformat(d)).days <= 183 and a > 0]
        if len(recent) >= 3 and r["price"]:
            out.append(r["price"] / median(recent))
    return out


def ratios_from_building(slug: str) -> list[float]:
    raw = Path("data/raw/pf")
    details = json.loads((raw / ("details.json" if slug == "princess_tower" else f"{slug}_details.json")).read_text())
    out: list[float] = []
    for p in {x["id"]: x for x in json.loads((raw / f"{slug}_rent.json").read_text())}.values():
        d = details.get(str(p["id"])) or {}
        recent = [float(t["amount"]) for t in (d.get("similar_price_transactions") or {}).get("rent") or []
                  if (TODAY - date.fromisoformat(t["date"][:10])).days <= 183 and float(t["amount"]) > 0]
        if len(recent) >= 3 and p["price"]["value"]:
            out.append(p["price"]["value"] / median(recent))
    return out


def main() -> None:
    rows: dict[str, list[float]] = {k: ratios_from_areas(Path("data/raw/pf") / v) for k, v in SOURCES.items()}
    rows["Princess Tower (whole building)"] = ratios_from_building("princess_tower")
    rows["Binghatti Heights (whole building)"] = ratios_from_building("binghatti_heights")
    head = " | ".join(f"under {int(t * 100)}%" for t in THRESHOLDS)
    print(f"| Rentals judged | n | {head} | cheapest vs deals |")
    print("|---|---|" + "---|" * (len(THRESHOLDS) + 1))
    for name, rs in rows.items():
        cells = " | ".join(f"{sum(r < t for r in rs)} ({100 * sum(r < t for r in rs) / len(rs):.0f}%)" for t in THRESHOLDS)
        print(f"| {name} | {len(rs)} | {cells} | {(min(rs) - 1) * 100:+.0f}% |")


if __name__ == "__main__":
    main()
