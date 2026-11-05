"""Turn the raw public pages into web/data/listings.json: listings, verdicts, duplicate groups, mocked replies.

Run after fetch_listings.py, fetch_details.py and photo_hashes.py. Agent names and phone numbers are dropped.
"""

import hashlib
import json
from datetime import date
from pathlib import Path

from scripts.fetch_details import in_audit
from trust.models import AgentReply, Listing, ListingCard, Status, Transaction
from trust.rules import evaluate

RAW: Path = Path("data/raw/pf")
OUT: Path = Path("web/data/listings.json")
TODAY: date = date(2026, 11, 5)  # the day the pages were read
SIZE_TOLERANCE: int = 10  # sqft: registered deals within this of the listing's size count as the same layout


def pooled_deals(details: dict[str, dict], offering: str) -> list[Transaction]:
    """Every registered deal shown on any audited page of this offering, de-duplicated, newest first."""
    key = "rent" if offering == "rent" else "buy"
    seen: set[tuple[str, int, int]] = set()
    for d in details.values():
        if d["offering"] != offering:
            continue
        for t in (d.get("similar_price_transactions") or {}).get(key) or []:
            seen.add((t["date"][:10], int(float(t["amount"])), int(t["size"])))
    return [Transaction(date=a, amount=b, size_sqft=c) for a, b, c in sorted(seen, reverse=True)]


def agent_key(agent_id: str) -> str:
    return "A" + hashlib.sha256(agent_id.encode()).hexdigest()[:4].upper()


def to_listing(p: dict, d: dict, offering: str, deals: list[Transaction], hashes: list[str]) -> Listing:
    size = int(p["size"]["value"])
    return Listing(
        id=str(p["id"]),
        offering=offering,
        url=p["share_url"],
        title=p["title"],
        price_aed=int(p["price"]["value"]),
        bedrooms=int(p["bedrooms"]),
        bathrooms=int(p["bathrooms"] or 0),
        size_sqft=size,
        furnished=p.get("furnished") or "",
        cheques=p.get("number_of_cheques") if offering == "rent" else None,
        listed_date=p["listed_date"][:10],
        available_from=(d.get("rental_availability_date") or "")[:10] or None if offering == "rent" else None,
        agency=p["broker"]["name"],
        agent_key=agent_key(str(p["agent"]["id"])),
        agent_is_super=bool(p["agent"].get("is_super_agent")),
        is_verified=bool(p["is_verified"]),
        has_permit_link=bool((d.get("rera") or {}).get("permit_validation_url")),
        images_count=int(p.get("images_count") or 0),
        thumb_url=None,
        photo_hashes=hashes,
        description="",  # dropped: agent text often holds names and phone numbers
        transactions=[t for t in deals if abs(t.size_sqft - size) <= SIZE_TOLERANCE],
    )


def mocked_reply(listing: Listing, status: Status, n: int) -> AgentReply | None:
    """Deterministic demo replies, so the 'ask the agent' flow has outcomes to show. Labelled as mocked in the UI."""
    if status == Status.HIDDEN:
        return AgentReply(
            listing_id=listing.id,
            available=False,
            confirmed_price_aed=None,
            terms="That unit is gone, but I have a similar one at a higher price.",
            viewing_slots=[],
        )
    if status == Status.CHECK and n % 3 == 0:
        return AgentReply(
            listing_id=listing.id,
            available=False,
            confirmed_price_aed=None,
            terms="Rented last month, sorry. The ad is being removed.",
            viewing_slots=[],
        )
    terms = (
        f"{listing.cheques or 4} cheques, 5% agency fee, 5% refundable deposit, Ejari by the agency."
        if listing.offering == "rent"
        else "Vacant on transfer. Owner open to offers; service charge figure to follow from the owner."
    )
    return AgentReply(
        listing_id=listing.id,
        available=True,
        confirmed_price_aed=listing.price_aed,
        terms=terms,
        viewing_slots=["Sat 10:00", "Sat 16:30", "Sun 11:00"],
    )


def main() -> None:
    details: dict[str, dict] = json.loads((RAW / "details.json").read_text())
    hashes: dict[str, list[str]] = json.loads((RAW / "photo_hashes.json").read_text())
    listings: list[Listing] = []
    for offering in ("rent", "sale"):
        deals = pooled_deals(details, offering)
        for p in {x["id"]: x for x in json.loads((RAW / f"princess_tower_{offering}.json").read_text())}.values():
            lid = str(p["id"])
            if lid in details and in_audit(p):  # the prototype shows the audited listings only
                listings.append(to_listing(p, details[lid], offering, deals, hashes.get(lid, [])))
    verdicts, groups = evaluate(listings, TODAY)
    by_id = {x.id: x for x in listings}
    cards = [ListingCard(listing=by_id[v.listing_id], verdict=v) for v in verdicts]
    replies = [r for n, c in enumerate(cards) if (r := mocked_reply(c.listing, c.verdict.status, n))]
    OUT.write_text(
        json.dumps(
            {
                "generated": TODAY.isoformat(),
                "groups": [g.model_dump() for g in groups],
                "cards": [c.model_dump(mode="json") for c in cards],
                "replies": [r.model_dump() for r in replies],
            },
            ensure_ascii=False,
            indent=1,
        )
    )
    counts = {s: sum(c.verdict.status == s for c in cards) for s in Status}
    print(len(cards), "cards", counts, len(groups), "duplicate groups")


if __name__ == "__main__":
    main()
