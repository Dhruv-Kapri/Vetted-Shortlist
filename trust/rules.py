"""The rules the assistant follows. Pure functions: listings in, verdicts out.

Every rule only uses what a person searching can see on the listing page (price, the registered deals for
the same size the portal shows, the agent's own "available from" date, the permit link, the photos).
RULES.md explains each rule, where it is wrong and who gets hurt.
"""

from collections.abc import Sequence
from datetime import date
from statistics import median

from trust.models import DuplicateGroup, Flag, Listing, Severity, Status, Verdict

# Thresholds (RULES.md says why each value).
BAIT_BLOCK: float = 0.75  # price under 75% of the registered median: likely bait, hidden
BAIT_WARN: float = 0.90  # 75-90%: plausible but ask for the full price first
ABOVE_INFO: float = 1.25  # over 125%: not fake, but say it is well above recent deals
COMPARABLE_DAYS: dict[str, int] = {"rent": 183, "sale": 365}
MIN_COMPARABLES: int = 3
STALE_DAYS: int = 45  # rent: "available from" this long ago and still advertised
SAME_PHOTO_BITS: int = 6  # dHash Hamming distance at or under which two photos are the same picture


def hamming(a: str, b: str) -> int:
    return (int(a, 16) ^ int(b, 16)).bit_count()


def market_median(listing: Listing, today: date) -> tuple[int, int] | None:
    """Median of registered deals for the same size in the comparison window, and how many there were."""
    window = COMPARABLE_DAYS[listing.offering]
    amounts = [
        t.amount
        for t in listing.transactions
        if (today - date.fromisoformat(t.date[:10])).days <= window and t.amount > 0
    ]
    if len(amounts) < MIN_COMPARABLES:
        return None
    return int(median(amounts)), len(amounts)


def price_flags(listing: Listing, today: date) -> list[Flag]:
    """R1 (too cheap to be true) and R6 (well above recent deals)."""
    found = market_median(listing, today)
    if found is None:
        return [
            Flag(
                rule_id="R1",
                severity=Severity.WARN,
                title="Not enough recent deals to judge the price",
                reason=f"Fewer than {MIN_COMPARABLES} registered deals for this size in the comparison window.",
                ask_agent="What is the full price, and what is it based on?",
            )
        ]
    med, n = found
    ratio = listing.price_aed / med
    gap = round((1 - ratio) * 100)
    what = "rents" if listing.offering == "rent" else "sales"
    basis = f"The median of {n} registered {what} for this size in the last {COMPARABLE_DAYS[listing.offering] // 30} months is AED {med:,}."
    full_price_q = (
        "Is this the full yearly rent, and for how many cheques?"
        if listing.offering == "rent"
        else "Is this the final asking price, and is the unit vacant or tenanted?"
    )
    if ratio < BAIT_BLOCK:
        return [
            Flag(
                rule_id="R1",
                severity=Severity.BLOCK,
                title=f"Price {gap}% under recent deals",
                reason=f"{basis} A price this far under is the usual sign of a bait ad.",
                ask_agent=full_price_q,
            )
        ]
    if ratio < BAIT_WARN:
        return [
            Flag(
                rule_id="R1",
                severity=Severity.WARN,
                title=f"Price {gap}% under recent deals",
                reason=f"{basis} Possible, but worth confirming before you visit.",
                ask_agent=full_price_q,
            )
        ]
    if ratio > ABOVE_INFO:
        return [
            Flag(
                rule_id="R6",
                severity=Severity.INFO,
                title=f"Price {-gap}% over recent deals",
                reason=f"{basis} Not a sign of a fake ad, but there is room to negotiate.",
            )
        ]
    return [Flag(rule_id="R6", severity=Severity.INFO, title="Price in line with recent deals", reason=basis)]


def stale_flag(listing: Listing, today: date) -> Flag | None:
    """R3: a rental the agent said was free long ago is probably gone."""
    if listing.offering != "rent" or listing.available_from is None:
        return None
    days = (today - date.fromisoformat(listing.available_from[:10])).days
    if days <= STALE_DAYS:
        return None
    return Flag(
        rule_id="R3",
        severity=Severity.WARN,
        title=f"Said 'available' {days} days ago",
        reason=f"The agent listed it as available from {listing.available_from[:10]}. Units in this tower usually let faster, so it may be gone.",
        ask_agent="Is the unit still available, and when can I view it?",
    )


def permit_flag(listing: Listing) -> Flag | None:
    """R4: every Dubai property ad needs a DLD permit; no permit link means no proof the ad is allowed."""
    if listing.has_permit_link:
        return None
    return Flag(
        rule_id="R4",
        severity=Severity.BLOCK,
        title="No DLD permit shown",
        reason="Dubai property ads need a DLD advertising permit. This one shows none.",
    )


def duplicate_groups(
    listings: Sequence[Listing], today: date, known_same: Sequence[Sequence[str]] = ()
) -> list[DuplicateGroup]:
    """R2: listings of the same size and bedrooms that share a photo are the same flat posted more than once.

    `known_same` adds groups confirmed another way (in the prototype: by eye; in production: the DLD unit id).
    """
    parent: dict[str, str] = {x.id: x.id for x in listings}

    def root(i: str) -> str:
        while parent[i] != i:
            i = parent[i]
        return i

    for i, a in enumerate(listings):
        for b in listings[i + 1 :]:
            same_kind = a.offering == b.offering and a.bedrooms == b.bedrooms and abs(a.size_sqft - b.size_sqft) <= 5
            if same_kind and any(hamming(x, y) <= SAME_PHOTO_BITS for x in a.photo_hashes for y in b.photo_hashes):
                parent[root(b.id)] = root(a.id)
    by_id = {x.id: x for x in listings}
    for ids in known_same:
        same_offer = [i for i in ids if i in by_id]
        for o in ("rent", "sale"):
            members_o = [i for i in same_offer if by_id[i].offering == o]
            for i in members_o[1:]:
                parent[root(i)] = root(members_o[0])

    members: dict[str, list[Listing]] = {}
    for x in listings:
        members.setdefault(root(x.id), []).append(x)
    groups: list[DuplicateGroup] = []
    for n, ms in enumerate(sorted((m for m in members.values() if len(m) > 1), key=lambda m: m[0].id), start=1):
        keep = max(ms, key=lambda x: (x.has_permit_link, x.is_verified, -abs(_ratio(x, today) - 1), x.listed_date))
        prices = [x.price_aed for x in ms]
        groups.append(
            DuplicateGroup(
                group_id=f"G{n}",
                listing_ids=[x.id for x in ms],
                price_min_aed=min(prices),
                price_max_aed=max(prices),
                agencies=len({x.agency for x in ms}),
                keep_id=keep.id,
            )
        )
    return groups


def _ratio(listing: Listing, today: date) -> float:
    found = market_median(listing, today)
    return listing.price_aed / found[0] if found else 1.0


def base_questions(listing: Listing) -> list[str]:
    if listing.offering == "rent":
        return [
            "Is the unit still available, and from what date?",
            "What is the full yearly rent, in how many cheques?",
            "What are the agency fee and the security deposit?",
            "Can I view it this week?",
        ]
    return [
        "Is the unit vacant or tenanted? If tenanted, when does the lease end?",
        "Is the asking price final, and what is the service charge per sqft?",
        "Is there a mortgage on the unit that needs a bank release?",
        "Can I view it this week?",
    ]


def evaluate(
    listings: Sequence[Listing], today: date, known_same: Sequence[Sequence[str]] = ()
) -> tuple[list[Verdict], list[DuplicateGroup]]:
    """Run every rule. Status: any BLOCK -> hidden; else any WARN -> check; else short list."""
    groups = duplicate_groups(listings, today, known_same)
    group_of: dict[str, DuplicateGroup] = {i: g for g in groups for i in g.listing_ids}
    verdicts: list[Verdict] = []
    for x in listings:
        flags = price_flags(x, today) + [f for f in (stale_flag(x, today), permit_flag(x)) if f]
        g = group_of.get(x.id)
        if g is not None:
            spread = f"AED {g.price_min_aed:,} to {g.price_max_aed:,}"
            if x.id == g.keep_id:
                flags.append(
                    Flag(
                        rule_id="R2",
                        severity=Severity.INFO,
                        title=f"Same flat listed {len(g.listing_ids)} times",
                        reason=f"The same photos appear on {len(g.listing_ids)} listings ({g.agencies} agencies, {spread}). We kept this one: it has the strongest proof.",
                    )
                )
            else:
                flags.append(
                    Flag(
                        rule_id="R2",
                        severity=Severity.BLOCK,
                        title="Duplicate of another listing",
                        reason=f"The same photos appear on {len(g.listing_ids)} listings ({g.agencies} agencies, {spread}). We show only the best one.",
                    )
                )
        severities = {f.severity for f in flags}
        status = (
            Status.HIDDEN
            if Severity.BLOCK in severities
            else Status.CHECK
            if Severity.WARN in severities
            else Status.SHORTLIST
        )
        asks = [f.ask_agent for f in flags if f.ask_agent and f.severity != Severity.INFO]
        # a flag's question replaces the standard question on the same topic
        topics = ("available", "full yearly rent", "final asking price")
        covered = {t for t in topics for a in asks if t in a}
        questions = asks + [q for q in base_questions(x) if not any(t in q for t in covered)]
        verdicts.append(
            Verdict(
                listing_id=x.id,
                status=status,
                flags=flags,
                duplicate_group=g.group_id if g else None,
                agent_questions=questions,
            )
        )
    return verdicts, groups
