"""Seam tests for the trust rules: each pins one rule's decision, not its wording."""

from datetime import date

from trust.models import Listing, Severity, Status, Transaction
from trust.rules import evaluate

TODAY: date = date(2026, 11, 5)
DEALS: list[Transaction] = [Transaction(date=f"2026-10-{d:02d}", amount=a, size_sqft=1189)
                            for d, a in [(1, 110000), (5, 115000), (10, 120000), (20, 115000)]]


def make(lid: str, price: int, *, available_from: str | None = "2026-11-01", hashes: list[str] | None = None,
         permit: bool = True, verified: bool = True, agency: str = "Agency") -> Listing:
    return Listing(id=lid, offering="rent", url="u", title="t", price_aed=price, bedrooms=2, bathrooms=2,
                   size_sqft=1189, furnished="YES", cheques=4, listed_date="2026-10-30", available_from=available_from,
                   agency=agency, agent_key="A1", agent_is_super=False, is_verified=verified, has_permit_link=permit,
                   images_count=10, thumb_url=None, photo_hashes=hashes or [], description="", transactions=DEALS)


def status_of(*listings: Listing) -> dict[str, Status]:
    verdicts, _ = evaluate(list(listings), TODAY)
    return {v.listing_id: v.status for v in verdicts}


def test_price_far_under_registered_deals_is_hidden_and_near_market_is_kept() -> None:
    # median of DEALS is 115,000: 80K is 30% under (bait), 100K is 13% under (ask first), 115K is in line
    assert status_of(make("bait", 80000), make("low", 100000), make("fair", 115000)) == {
        "bait": Status.HIDDEN, "low": Status.CHECK, "fair": Status.SHORTLIST}


def test_too_few_registered_deals_means_ask_not_judge() -> None:
    listing = make("x", 80000).model_copy(update={"transactions": DEALS[:2]})
    verdicts, _ = evaluate([listing], TODAY)
    assert verdicts[0].status == Status.CHECK
    assert all(f.severity != Severity.BLOCK for f in verdicts[0].flags)


def test_rental_available_long_ago_goes_to_check_with_an_availability_question() -> None:
    verdicts, _ = evaluate([make("old", 115000, available_from="2026-08-01")], TODAY)
    assert verdicts[0].status == Status.CHECK
    assert any("still available" in q for q in verdicts[0].agent_questions)


def test_missing_permit_hides_even_a_fair_price() -> None:
    assert status_of(make("p", 115000, permit=False)) == {"p": Status.HIDDEN}


def test_same_photo_on_two_listings_keeps_the_one_with_stronger_proof() -> None:
    a = make("a", 115000, hashes=["ffff0000ffff0000"], verified=False, agency="One")
    b = make("b", 112000, hashes=["ffff0000ffff0001"], agency="Two")  # 1 bit apart: same picture
    verdicts, groups = evaluate([a, b], TODAY)
    assert len(groups) == 1 and groups[0].keep_id == "b" and groups[0].agencies == 2
    assert {v.listing_id: v.status for v in verdicts} == {"a": Status.HIDDEN, "b": Status.SHORTLIST}


def test_known_same_flat_groups_listings_the_photo_hash_missed_but_never_mixes_rent_and_sale() -> None:
    a, b = make("a", 115000, agency="One"), make("b", 118000, agency="Two")  # no shared photo hashes
    sale = make("s", 2_000_000).model_copy(update={"offering": "sale"})
    _, groups = evaluate([a, b, sale], TODAY, known_same=[["a", "b", "s"]])
    assert [sorted(g.listing_ids) for g in groups] == [["a", "b"]]


def test_undisclosed_staging_on_a_furnished_ad_asks_about_the_furniture_while_disclosed_staging_only_informs() -> None:
    hidden_staging = make("u", 115000).model_copy(update={"photo_issue": "staged_undisclosed"})
    open_staging = make("d", 115000).model_copy(update={"photo_issue": "staged_disclosed"})
    verdicts, _ = evaluate([hidden_staging, open_staging], TODAY)
    by_id = {v.listing_id: v for v in verdicts}
    assert by_id["u"].status == Status.CHECK and any("furniture" in q for q in by_id["u"].agent_questions)
    assert by_id["d"].status == Status.SHORTLIST
