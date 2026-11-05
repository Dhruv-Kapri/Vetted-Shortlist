"""Write the per-listing audit table (AUDIT_TABLE.md fragment) from the raw public pages and the verdicts.

Columns are what a person searching can see, plus what the assistant concluded. Eye-check notes for the
photos come from EYE_NOTES (looked at by hand on contact sheets of the first three photos).
"""

import json
import statistics as st
from datetime import date
from pathlib import Path

from trust.rules import SAME_PHOTO_BITS, hamming

RAW: Path = Path("data/raw/pf")
TODAY: date = date(2026, 11, 5)
EYE_NOTES: dict[str, str] = {}  # filled from research/eye-checks.json if present


def load_all() -> dict[str, tuple[str, dict]]:
    out: dict[str, tuple[str, dict]] = {}
    for o in ("rent", "sale"):
        for p in json.loads((RAW / f"princess_tower_{o}.json").read_text()):
            out[str(p["id"])] = (o, p)
    return out


def photo_twins(lid: str, everything: dict[str, tuple[str, dict]], hashes: dict[str, list[str]]) -> list[str]:
    """Other listings (anywhere in the building, same offering) sharing a photo with this one."""
    o, p = everything[lid]
    twins: list[str] = []
    for other, (o2, p2) in everything.items():
        if other == lid or o2 != o:
            continue
        if any(hamming(a, b) <= SAME_PHOTO_BITS for a in hashes.get(lid, []) for b in hashes.get(other, [])):
            same = p2["bedrooms"] == p["bedrooms"] and abs((p2["size"]["value"] or 0) - (p["size"]["value"] or 0)) <= 5
            kind = "same size" if same else f"{p2['bedrooms']}BR {p2['size']['value']} sqft"
            twins.append(f"{other} ({p2['broker']['name'][:18]}, AED {p2['price']['value']:,}, {kind})")
    return sorted(set(twins))


def main() -> None:
    eye_path = Path("research/eye-checks.json")
    EYE_NOTES.update(json.loads(eye_path.read_text()) if eye_path.exists() else {})
    everything = load_all()
    hashes: dict[str, list[str]] = json.loads((RAW / "photo_hashes.json").read_text())
    data = json.loads(Path("web/data/listings.json").read_text())
    rows: list[str] = [
        "| # | Listing | Price (AED) | sqft | Furn. | Cheques | Listed | Available from | vs registered median | Same photos on other listings | Photos (by eye) | Assistant |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    cards = sorted(data["cards"], key=lambda c: (c["listing"]["offering"], c["listing"]["price_aed"]))
    for n, c in enumerate(cards, start=1):
        x, v = c["listing"], c["verdict"]
        window = 183 if x["offering"] == "rent" else 365
        deals = [t["amount"] for t in x["transactions"] if (TODAY - date.fromisoformat(t["date"])).days <= window]
        vs = f"{round((x['price_aed'] / st.median(deals) - 1) * 100):+d}% (n={len(deals)})" if len(deals) >= 3 else "too few deals"
        avail = x["available_from"] or "-"
        if x["available_from"]:
            avail += f" ({(TODAY - date.fromisoformat(x['available_from'])).days} d ago)"
        twins = "; ".join(photo_twins(x["id"], everything, hashes)) or "none found"
        flags = ", ".join(f["title"] for f in v["flags"] if f["severity"] != "info") or "-"
        rows.append(
            f"| {n} | [{x['offering']} {x['id']}]({x['url']}) | {x['price_aed']:,} | {x['size_sqft']} | {x['furnished'][:1]} "
            f"| {x['cheques'] or '-'} | {x['listed_date']} | {avail} | {vs} | {twins} | {EYE_NOTES.get(x['id'], 'not checked')} "
            f"| **{v['status']}** {('— ' + flags) if flags != '-' else ''} |"
        )
    Path("research/audit_table.md").write_text("\n".join(rows) + "\n")
    print(len(cards), "rows")


if __name__ == "__main__":
    main()
