"""The seam between the rules engine (Python) and the prototype (static web page).

`build_data.py` writes a list of `ListingCard` as JSON to web/data/listings.json; the page reads only that.
"""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

Offering = Literal["rent", "sale"]

# What is wrong with the photos, if anything. In the prototype this comes from our eye check (AUDIT.md);
# in production it would come from an image model (see ONE-PAGER, "What we could not build").
PhotoIssue = Literal["views_only", "reused_other_units", "staged_undisclosed", "staged_disclosed", "other_building"]


class Status(StrEnum):
    SHORTLIST = "shortlist"  # passes every rule; safe to contact
    CHECK = "check"  # unsure: the assistant asks the agent first, then decides
    HIDDEN = "hidden"  # likely fake or misleading; hidden by default, reason shown on tap


class Severity(StrEnum):
    BLOCK = "block"  # on its own moves the listing to HIDDEN
    WARN = "warn"  # moves the listing to CHECK
    INFO = "info"  # shown, changes nothing


class Transaction(BaseModel):
    """A registered contract or sale for the same size of unit, as shown on the listing page."""

    date: str  # ISO date
    amount: int  # AED (yearly rent, or sale price)
    size_sqft: int


class Listing(BaseModel):
    """What a person searching can see about one listing (no agent names or phone numbers)."""

    id: str
    offering: Offering
    url: str
    title: str
    price_aed: int  # yearly rent, or sale price
    bedrooms: int
    bathrooms: int
    size_sqft: int
    furnished: str  # YES / NO / PARTLY
    cheques: int | None  # rent only: number of cheques a year
    listed_date: str  # ISO date
    available_from: str | None  # rent only: the agent's own "available from" date
    agency: str
    agent_key: str  # stable anonymous id for the agent, e.g. "A17"
    agent_is_super: bool
    is_verified: bool  # Property Finder "Verified" badge
    has_permit_link: bool  # a DLD permit validation link is shown
    images_count: int
    thumb_url: str | None
    photo_hashes: list[str]  # 64-bit dHash hex of the first photos
    description: str
    transactions: list[Transaction]  # recent registered deals, same size, newest first
    photo_issue: PhotoIssue | None = None


class Flag(BaseModel):
    rule_id: str  # e.g. "R1"
    severity: Severity
    title: str  # short, for a chip: "Price 22% under recent contracts"
    reason: str  # one or two plain sentences for the person searching
    ask_agent: str | None = None  # question the assistant sends to the agent to resolve it


class DuplicateGroup(BaseModel):
    group_id: str
    listing_ids: list[str]
    price_min_aed: int
    price_max_aed: int
    agencies: int
    keep_id: str  # the one shown on the short list


class Verdict(BaseModel):
    listing_id: str
    status: Status
    flags: list[Flag]
    duplicate_group: str | None = None
    agent_questions: list[str]  # what the assistant will ask the agent on the person's behalf


class ListingCard(BaseModel):
    """One element of web/data/listings.json."""

    listing: Listing
    verdict: Verdict


class AgentReply(BaseModel):
    """A mocked agent answer used by the prototype's 'ask the agent' flow. Clearly labelled as mocked."""

    listing_id: str
    available: bool | None
    confirmed_price_aed: int | None
    terms: str
    viewing_slots: list[str]
