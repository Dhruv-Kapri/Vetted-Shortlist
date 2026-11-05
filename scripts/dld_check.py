"""Listings vs the official DLD register, for Princess Tower and Binghatti Heights.

Prints markdown. Q1: do asking prices and listing-page deals agree with DLD contracts?
Q2: are ads whose 'available from' date is >45 days old more often matched by a DLD New contract?
Q3: do asking sale prices agree with DLD registered sales, Jan to Nov 2026?
"""

import csv
import json
import os
from collections import defaultdict
from datetime import date
from pathlib import Path
from statistics import median

RAW_ROOT: Path = Path(os.environ.get("RAW_ROOT", "/Users/dhruvkapri/Desktop/Developer/sandbox-1104/data/raw"))
RENTS_CSV: Path = RAW_ROOT / "dld/rents_2026-10-04_2026-11-04.csv"
# DLD sales exports per building: slug -> file (the JVC export may not exist yet)
SALES_FILES: dict[str, Path] = {
    "princess_tower": RAW_ROOT / "dld/sales_dubai_marina_2026-01-01_2026-11-05.csv",
    "binghatti_heights": RAW_ROOT / "dld/sales_jvc_2026-01-01_2026-11-05.csv",
}
MIN_SALE_VALUE: float = 300_000  # below this a "sale" is a partial-share or odd transfer
AREA_MISMATCH: float = 0.01  # PROCEDURE_AREA vs ACTUAL_AREA gap that marks a partial share
SALE_DEAL_DAYS: int = 365  # same 12-month window as scripts/building_check.py for sales
TODAY: date = date(2026, 11, 5)
SQFT_PER_SQM: float = 10.7639
AREA_TOL: float = 0.05  # listing size within +-5% of DLD ACTUAL_AREA
PRICE_TOL: float = 0.10  # strict variant: DLD annual rent within +-10% of asking
STALE_DAYS: int = 45
AUDITED_ID: str = "169274661"  # cheapest of the 55 hand-audited Princess Tower rentals
PAGE_DEAL_DAYS: int = 183  # same 6-month window as scripts/building_check.py
# (slug, details file, DLD PROJECT_EN, label)
BUILDINGS: list[tuple[str, str, str, str]] = [
    ("princess_tower", "details.json", "PRINCESS TOWER", "Princess Tower"),
    ("binghatti_heights", "binghatti_heights_details.json", "Binghatti Heights", "Binghatti Heights"),
]


def area_match(size_sqft: float, area_sqm: float, tol: float = AREA_TOL) -> bool:
    """True if a listing size in sqft is within +-tol of a DLD area in sqm (tolerance relative to the DLD area)."""
    return area_sqm > 0 and abs(size_sqft / SQFT_PER_SQM - area_sqm) <= tol * area_sqm


def med(xs: list[float]) -> str:
    return f"{median(xs):,.0f}" if xs else "-"


def pct(a: int, b: int) -> str:
    return f"{a / b:.0%}" if b else "-"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_listings(slug: str, offering: str) -> list[dict]:
    return json.loads((RAW_ROOT / f"pf/{slug}_{offering}.json").read_text())


def page_deals(details: dict[str, dict], offering: str) -> set[tuple[str, int, int]]:
    """Unique registered deals (date, amount, size sqft) shown on listing pages."""
    key = "rent" if offering == "rent" else "buy"
    out: set[tuple[str, int, int]] = set()
    for d in details.values():
        if d["offering"] != offering:
            continue
        for t in (d.get("similar_price_transactions") or {}).get(key) or []:
            out.add((t["date"][:10], int(float(t["amount"])), int(t["size"])))
    return out


def q1_rent(label: str, listings: list[dict], dld: list[dict[str, str]], deals: set[tuple[str, int, int]]) -> list[str]:
    by_bed: dict[str, list[dict]] = defaultdict(list)
    for p in listings:
        if p["size"]["value"]:
            by_bed[str(p["bedrooms"])].append(p)
    rows: list[str] = []
    for bed, ps in sorted(by_bed.items()):
        sizes = [p["size"]["value"] for p in ps]
        hit = [r for r in dld if any(area_match(s, float(r["ACTUAL_AREA"])) for s in sizes)]
        new = [float(r["ANNUAL_AMOUNT"]) for r in hit if r["VERSION_EN"] == "New"]
        ren = [float(r["ANNUAL_AMOUNT"]) for r in hit if r["VERSION_EN"] == "Renewed"]
        pd_ = [a for dt, a, sz in deals
               if (TODAY - date.fromisoformat(dt)).days <= PAGE_DEAL_DAYS
               and any(area_match(s, sz / SQFT_PER_SQM) for s in sizes)]
        prices = [p["price"]["value"] for p in ps]
        rows.append(f"| {label} | {bed} | {len(ps)} | {med(new)} (n={len(new)}) | {med(ren)} (n={len(ren)}) "
                    f"| {med(pd_)} (n={len(pd_)}) | {med(prices)} | {min(prices):,} |")
    return rows


def ratios_vs_dld(listings: list[dict], dld: list[dict[str, str]], min_n: int = 3) -> list[tuple[str, float, int]]:
    """(listing id, asking / median DLD New rent for its size, n contracts) for listings with >= min_n matches."""
    out: list[tuple[str, float, int]] = []
    for p in listings:
        size = p["size"]["value"] or 0
        amts = [float(r["ANNUAL_AMOUNT"]) for r in dld
                if r["VERSION_EN"] == "New" and area_match(size, float(r["ACTUAL_AREA"]))]
        if len(amts) >= min_n:
            out.append((str(p["id"]), p["price"]["value"] / median(amts), len(amts)))
    return out


def claim_checks(label: str, listings: list[dict], dld: list[dict[str, str]], deals: set[tuple[str, int, int]]) -> list[str]:
    out: list[str] = []
    rat = ratios_vs_dld(listings, dld)
    under = [r for r in rat if r[1] < 0.75]
    out.append(f"- {label}: {len(rat)} of {len(listings)} rentals have >=3 size-matched DLD New contracts; "
               f"{len(under)} are under 75% of the DLD median (lowest ratio {min((r[1] for r in rat), default=float('nan')):.0%}).")
    for r in sorted(under, key=lambda r: r[1])[:10]:
        p = next(p for p in listings if str(p["id"]) == r[0])
        out.append(f"  - listing {r[0]}: {p['bedrooms']}BR {p['size']['value']} sqft, AED {p['price']['value']:,} = {r[1]:.0%} of DLD median (n={r[2]})")
    return out


def pt_two_bed_claim(listings: list[dict], dld: list[dict[str, str]], deals: set[tuple[str, int, int]]) -> list[str]:
    two = [p for p in listings if str(p["bedrooms"]) == "2" and p["size"]["value"]]
    cheap = min(two, key=lambda p: p["price"]["value"])
    size, price = cheap["size"]["value"], cheap["price"]["value"]
    pd_ = [a for dt, a, sz in deals if abs(sz - size) <= 10 and (TODAY - date.fromisoformat(dt)).days <= PAGE_DEAL_DAYS]
    new = [float(r["ANNUAL_AMOUNT"]) for r in dld if r["VERSION_EN"] == "New" and area_match(size, float(r["ACTUAL_AREA"]))]
    ren = [float(r["ANNUAL_AMOUNT"]) for r in dld if r["VERSION_EN"] == "Renewed" and area_match(size, float(r["ACTUAL_AREA"]))]
    out = [f"- Cheapest Princess Tower 2-bed rental (listing {cheap['id']}): {size} sqft, AED {price:,}."]
    out.append(f"  - Original claim basis (listing-page deals, +-10 sqft, 6 months): median {med(pd_)}, n={len(pd_)}; "
               f"ask is {price / median(pd_) - 1:+.0%} vs that median." if pd_ else "  - no listing-page deals for that size.")
    if new:
        out.append(f"  - Against DLD New contracts of that size (+-5%): median {med(new)}, n={len(new)}; ask is {price / median(new) - 1:+.0%}.")
    if ren:
        out.append(f"  - Against DLD Renewed contracts: median {med(ren)}, n={len(ren)}; ask is {price / median(ren) - 1:+.0%}.")
    return out


def clean_sales(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, int]]:
    """Ready flats, deduped on TRANSACTION_NUMBER, minus partial-share and odd-value transfers.

    Returns (kept rows, counts of rows dropped per reason; a row is counted under the first reason that hits).
    """
    dropped: dict[str, int] = {"not a ready flat": 0, "duplicate": 0, "partial share (areas differ >1%)": 0,
                               f"value under {MIN_SALE_VALUE:,.0f}": 0}
    kept: list[dict[str, str]] = []
    seen: set[str] = set()
    for r in rows:
        if r["PROP_SB_TYPE_EN"] != "Flat" or r["IS_OFFPLAN_EN"] != "Ready":
            dropped["not a ready flat"] += 1
        elif r["TRANSACTION_NUMBER"] in seen:
            dropped["duplicate"] += 1
        elif abs(float(r["PROCEDURE_AREA"]) - float(r["ACTUAL_AREA"])) > AREA_MISMATCH * float(r["ACTUAL_AREA"]):
            dropped["partial share (areas differ >1%)"] += 1
        elif float(r["TRANS_VALUE"]) < MIN_SALE_VALUE:
            dropped[f"value under {MIN_SALE_VALUE:,.0f}"] += 1
        else:
            kept.append(r)
        seen.add(r["TRANSACTION_NUMBER"])
    return kept, dropped


def rng(xs: list[float]) -> str:
    return f"{min(xs):,.0f} to {max(xs):,.0f}" if xs else "-"


def sales_section(label: str, project: str, listings: list[dict], details: dict[str, dict],
                  sales: list[dict[str, str]] | None) -> tuple[list[str], list[str]]:
    """(table rows, notes) comparing DLD sales with live sale asks, per bedroom count."""
    if sales is None:
        return [f"| {label} | all | not exported |" + " |" * 10], [f"- {label}: DLD sales not exported."]
    rows = [r for r in sales if r["PROJECT_EN"] == project and r["GROUP_EN"] == "Sales"]
    kept, dropped = clean_sales(rows)
    notes = [f"- {label}: {len(rows)} DLD sales rows, {len(kept)} kept; dropped " +
             ", ".join(f"{n} {why}" for why, n in dropped.items()) + "."]
    all_deals = page_deals(details, "sale")
    deals = [(a, sz) for dt, a, sz in all_deals if (TODAY - date.fromisoformat(dt)).days <= SALE_DEAL_DAYS]
    by_bed: dict[str, list[dict]] = defaultdict(list)
    for p in listings:
        if p["size"]["value"]:
            by_bed[str(p["bedrooms"])].append(p)
    out: list[str] = []
    for bed, ps in sorted(by_bed.items()):
        sizes = [p["size"]["value"] for p in ps]
        dld = [r for r in kept if r["ROOMS_EN"] == f"{bed} B/R"]
        vals = [float(r["TRANS_VALUE"]) for r in dld]
        psm = [float(r["TRANS_VALUE"]) / float(r["ACTUAL_AREA"]) for r in dld]
        sized = [float(r["TRANS_VALUE"]) for r in dld
                 if any(area_match(s, float(r["ACTUAL_AREA"])) for s in sizes)]
        asks = [p["price"]["value"] for p in ps]
        ratios = [a / median(vals) for a in asks] if vals else []
        on_pages = sum(any(dt == r["INSTANCE_DATE"][:10] and abs(a - float(r["TRANS_VALUE"])) <= 1 for dt, a, _ in all_deals)
                       for r in dld)
        page_n = len([1 for a, sz in deals if any(area_match(s, sz / SQFT_PER_SQM) for s in sizes)])
        out.append(f"| {label} | {bed} | {len(dld)} | {med(vals)} | {rng(vals)} | {med(psm)} | {med(sized)} (n={len(sized)}) "
                   f"| {len(ps)} | {med(asks)} | {min(asks):,} | "
                   + (f"{min(ratios):.0%} / {sum(r < 0.75 for r in ratios)} / {sum(r > 1.25 for r in ratios)}" if ratios else "-")
                   + f" | {page_n} | {on_pages} of {len(dld)} |")
    return out, notes


def audited_claim(listings: list[dict], details: dict[str, dict], dld: list[dict[str, str]]) -> list[str]:
    """The one-pager claim: cheapest of the 55 hand-audited listings (169274661, 1,184 sqft, AED 110,000)."""
    p = next(p for p in listings if str(p["id"]) == AUDITED_ID)
    size, price = p["size"]["value"], p["price"]["value"]
    deals = page_deals(details, "rent")
    pd_ = [a for dt, a, sz in deals if abs(sz - size) <= 10 and (TODAY - date.fromisoformat(dt)).days <= PAGE_DEAL_DAYS]
    new = [float(r["ANNUAL_AMOUNT"]) for r in dld if r["VERSION_EN"] == "New" and area_match(size, float(r["ACTUAL_AREA"]))]
    ren = [float(r["ANNUAL_AMOUNT"]) for r in dld if r["VERSION_EN"] == "Renewed" and area_match(size, float(r["ACTUAL_AREA"]))]
    return [f"- Cheapest of the 55 hand-audited listings (listing {AUDITED_ID}): {size} sqft, AED {price:,}.",
            f"  - Listing-page deals (+-10 sqft, {PAGE_DEAL_DAYS} days): median {med(pd_)}, n={len(pd_)}; ask is {price / median(pd_) - 1:+.0%}.",
            f"  - DLD New contracts within +-5% of {size / SQFT_PER_SQM:.0f} sqm: n={len(new)}, median {med(new)}, values {sorted(int(x) for x in new)}.",
            f"  - DLD Renewed contracts, same size band: n={len(ren)}, median {med(ren)}, range {rng(ren)}."]


def q2(label: str, listings: list[dict], details: dict[str, dict], dld: list[dict[str, str]]) -> tuple[list[str], list[str]]:
    new = [r for r in dld if r["VERSION_EN"] == "New"]
    # group -> [n, loose matches, strict matches]
    tot: dict[str, list[int]] = {"stale": [0, 0, 0], "fresh": [0, 0, 0]}
    bed: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0, 0])
    for p in listings:
        av = ((details.get(str(p["id"])) or {}).get("rental_availability_date") or "")[:10]
        size = p["size"]["value"] or 0
        if not av or not size:
            continue
        g = "stale" if (TODAY - date.fromisoformat(av)).days > STALE_DAYS else "fresh"
        m = [r for r in new if area_match(size, float(r["ACTUAL_AREA"]))]
        strict = [r for r in m if abs(float(r["ANNUAL_AMOUNT"]) / p["price"]["value"] - 1) <= PRICE_TOL]
        for c in (tot[g], bed[(str(p["bedrooms"]), g)]):
            c[0] += 1
            c[1] += bool(m)
            c[2] += bool(strict)
    summary = [f"| {label} | {g} | {c[0]} | {c[1]} ({pct(c[1], c[0])}) | {c[2]} ({pct(c[2], c[0])}) |" for g, c in tot.items()]
    detail = [f"| {label} | {b} | {g} | {c[0]} | {c[1]} ({pct(c[1], c[0])}) | {c[2]} ({pct(c[2], c[0])}) |"
              for (b, g), c in sorted(bed.items())]
    return summary, detail


def main() -> None:
    rents = read_csv(RENTS_CSV)
    sales_by_slug: dict[str, list[dict[str, str]] | None] = {
        slug: read_csv(f) if f.exists() else None for slug, f in SALES_FILES.items()}
    q1_rows: list[str] = []
    claims: list[str] = []
    sale_rows: list[str] = []
    sale_notes: list[str] = []
    q2_sum: list[str] = []
    q2_det: list[str] = []
    for slug, dfile, project, label in BUILDINGS:
        details = json.loads((RAW_ROOT / f"pf/{dfile}").read_text())
        rent = load_listings(slug, "rent")
        dld = [r for r in rents if r["PROJECT_EN"] == project and r["PROP_SUB_TYPE_EN"] == "Flat"]
        deals = page_deals(details, "rent")
        q1_rows += q1_rent(label, rent, dld, deals)
        claims += claim_checks(label, rent, dld, deals)
        if slug == "princess_tower":
            claims += pt_two_bed_claim(rent, dld, deals)
            claims += audited_claim(rent, details, dld)
        t, n = sales_section(label, project, load_listings(slug, "sale"), details, sales_by_slug[slug])
        sale_rows += t
        sale_notes += n
        s, d = q2(label, rent, details, dld)
        q2_sum += s
        q2_det += d
    print("## Q1. Rents: DLD register vs listing pages vs live asking (AED per year)\n")
    print("| Building | Bedrooms | Live listings | DLD New median | DLD Renewed median | Listing-page deals median (6 mo) | Asking median | Asking min |")
    print("|---|---|---|---|---|---|---|---|")
    print("\n".join(q1_rows))
    print("\nDLD rows are Flats whose area matches any listing of that bedroom count (+-5%).\n")
    print("### Claim checks\n")
    print("\n".join(claims))
    print("\n## Q3. Sales, Jan to Nov 2026: DLD registered sales vs live asking (AED)\n")
    print("\n".join(sale_notes))
    print("\n| Building | Bedrooms | DLD sales | DLD median | DLD min to max | DLD median per sqm | DLD median, size-matched | "
          "Live sale listings | Ask median | Ask min | Ask % of DLD median: lowest / n under 75% / n over 125% | Sales on listing pages (12 mo) | DLD sales also on listing pages |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    print("\n".join(sale_rows))
    print("\nDLD columns: ready flats of that bedroom count (ROOMS_EN) in the building, 2026-01-01 to 2026-11-05, "
          "cleaned as above. Size-matched: only DLD flats within +-5% of a live listing size. "
          "Listing-page sales: unique (date, amount, size) 'buy' deals in the details files, last 365 days, size within +-5% of a listing of that bedroom count. Last column: DLD sale with the same date and amount (+-1) among all listing-page deals.\n")
    print("\n## Q2. Stale vs fresh ads: share with a size-matched DLD New contract in the window\n")
    print("Stale = 'available from' more than 45 days before 2026-11-05; fresh = 45 days or less, or in the future. "
          "Loose = New contract in the same building, area within +-5%. Strict = loose and annual rent within +-10% of asking.\n")
    print("| Building | Group | Listings | Loose match | Strict match |")
    print("|---|---|---|---|---|")
    print("\n".join(q2_sum))
    print("\nBy bedroom count (same-size stratification, to expose the common-size confound):\n")
    print("| Building | Bedrooms | Group | Listings | Loose match | Strict match |")
    print("|---|---|---|---|---|---|")
    print("\n".join(q2_det))


if __name__ == "__main__":
    main()
