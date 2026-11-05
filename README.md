# A search assistant people trust (prototype)

An assistant inside Property Finder search that works for one person looking for a home. It hides
listings that are likely fake or misleading, says why, asks the agent the questions the person would
otherwise phone round about, and keeps a short list they can trust. It works for renters and buyers.
The agent stays in the deal.

**Live prototype (open on a phone):** https://vetted-shortlist.vercel.app

### Try it in two minutes

![Walkthrough: results, Why hidden?, ask the agent, the agent's view, buy mode, short list](docs/walkthrough.gif)

[Demo video (90 s, captions, no sound)](docs/demo.mp4). Regenerate both: `uv run --with playwright python scripts/demo_video.py` (needs the web server on port 8765, ffmpeg, and macOS `say`, which only paces the scenes).

The data is real: 55 live 2-bed listings in Princess Tower, Dubai Marina. Agent replies are mocked.

1. **Renter: results.** The bar says what the assistant did: "checked 32 listings: 13 on your short
   list, 14 to confirm with the agent, 5 hidden". Tap **Why hidden?**. Each hidden listing shows its
   evidence (here, the same flat posted twice), what would bring it back, and **Not right? Tell us**.
2. **Renter: a doubtful listing.** Open one marked "Assistant will check", e.g. one whose "available"
   date is months old. **Before you call** shows the checks, and the registered rents for that size.
3. **Ask the agent for me.** Untick or add questions, then **Send to agent**. The mocked reply comes
   back. If the flat is gone or the price is higher, the listing is removed with the reason; if not,
   it joins the short list and you can pick a viewing slot.
4. **The agent's side.** Tap **See what the agent receives**. The agent gets a pre-qualified lead
   (budget, move-in, cheques, viewing windows) and answers in one tap: available, gone, or price
   changed. The answer updates the searcher's screens.
5. **Buyer.** Switch to **Buy**. The same checks run against registered sales, with buyer questions
   (final price, service charge) instead of cheques.
6. **Short list.** Everything that passed or was confirmed, with the agent's terms and your viewing.

**Read these first:**

- [ONE-PAGER.md](ONE-PAGER.md): the problem behind the problem, where the assistant lives, metrics,
  and what we couldn't build.
- [AUDIT.md](AUDIT.md): 195 listings checked by hand (55 in Princess Tower, 140 across seven places),
  27 DLD permit cards, and automatic checks on about 950 listings. It also includes a price check of the
  whole building and a one-month cross-check against DLD's own register.
- [RULES.md](RULES.md): every rule, where it's wrong, and who gets hurt.
- [AI-LOG.md](AI-LOG.md): confident wrong AI answers about UAE real estate, and how we caught them.

## Numbers first

These come from Princess Tower, Dubai Marina, read on 5 Nov 2026. The audit covers 55 two-bed
listings in the common 1,181-1,189 sqft layout: 32 to rent and 23 for sale.

- **0 of 32 rentals priced like bait.** All are between 7% below and 52% above the median of 24
  registered rents in the last 6 months (AED 118,500). Across all 217 listings in the building, none
  is under 75% of registered deals.
- **DLD's own register agrees (one month, 4 Oct to 4 Nov).** Size-matched, no rental in either
  building is under 75%. The lowest asks are 89% (Princess Tower, 88 of 137 judgeable) and 91%
  (Binghatti Heights, 95 of 263; DLD has 27 contracts there). Of the 55 audited, the cheapest 2-bed
  rental is 7% under the 24 listing-page deals, and 13-19% under DLD at that size, on only 2 new and 5
  renewed contracts.
- **Sales, Jan to Nov 2026 (53 DLD sales in the two buildings):** no sale ask is under 75% of the DLD
  median for its bedroom count (lowest 87%). Asks run high instead: in Princess Tower 15 of 77 two-
  and three-bed asks are over 125% of what sold. The listing pages show 26 of the 31 cleaned Princess
  Tower sales, so their sample is small per size but not missing.
- **13 of 32 rentals give an "available from" date more than 45 days old.** The oldest is 489 days.
  Across the building, 47 of 119 do.
- **53 of 55 listings carry "Verified".**
- **Duplicates:** we matched photos by eye and found 11 of the 55 listings belong to 3 flats. One
  flat is for rent at AED 135K, 140K and 150K through three agencies.
- **Second building and six neighbourhoods** (about 700 more listings). None has a single listing
  under 75% of registered deals:
  - Palm Jumeirah: stale 18%, over 125% 21%
  - Downtown: stale 29%, over 125% 16%
  - Dubai Marina: stale 22%, over 125% 8%
  - JVC: stale 11%, over 125% 10%
  - Discovery Gardens: stale 21%, over 125% 0%
  - International City: stale 25%, over 125% 13%
- **140 more checked by hand** across all seven places (10 random and 10 most suspicious each). The
  random half: 0 bait, 19% stale, 10% photos that may not show the flat. All 22 permit cards checked
  match the ad price.
- **The 55 vs the 217:** 55 listings were checked by hand (one layout, photos included). All 217
  listings in the building went through the automatic checks.
- **The prototype's verdicts on the 55:** 32 on the short list, 17 for the assistant to check with
  the agent, 6 hidden. None is proven fake, but 23 show at least one sign of being misleading.

## What is real and what is mocked

| Part | Real or mocked |
|---|---|
| Listings (price, size, cheques, dates, badges, agency, permit link) | **Real**, from public listing pages, read on 5 Nov 2026 |
| Registered rents and sales for the same size | **Real**, as shown on each listing page |
| Photo matching | **Real**: a 64-bit difference hash of each listing's first 3 photos. The photos themselves are not in the repo |
| The rules and verdicts | **Real**, computed by `trust/rules.py` from the data above |
| Agent replies in "Ask the agent for me" | **Mocked**, and labelled in the app. Nothing is sent to any agent |
| Agent's view (`#/agent/<id>`): the pre-qualified lead (budget, move-in, cheques, viewing windows) and one-tap answers (available, gone, price changed) that feed the searcher's side | **Mocked** screen, no real agents |
| "Why hidden?" | Lists every hidden listing with its evidence and what would un-hide it, plus a "Not right? Tell us" control (the control sends nothing) |
| DLD register check | **Real**: official open data, one month, size-matched (`scripts/dld_check.py`) |
| Accounts, web-to-app sync, notifications, Scout integration | **Not built**. Placeholders only (see ONE-PAGER, "What we could not build") |

Left out on purpose: agent names, phone numbers and listing descriptions, because agents' text often
contains personal contact details. Each agent appears only as an anonymous key.

## Run it

```sh
uv sync                                     # Python 3.12
uv run pytest                               # the rule tests
cd web && python3 -m http.server 8765       # then open http://localhost:8765 at phone width
```

Rebuild the data from scratch. This is read-only and paced (one request every 2-3 s):

```sh
uv run python scripts/fetch_listings.py rent && uv run python scripts/fetch_listings.py sale
uv run python scripts/fetch_details.py --all        # detail pages: permit link, registered deals, availability
uv run python scripts/photo_hashes.py               # first 3 thumbnails per listing -> hashes
PYTHONPATH=. uv run python scripts/build_data.py    # -> web/data/listings.json
PYTHONPATH=. uv run python scripts/audit_table.py   # -> research/audit_table.md
PYTHONPATH=. uv run python -m scripts.dld_check     # DLD cross-check (needs the git-ignored DLD files)
```

The second building (Binghatti Heights, JVC) uses the same scripts with
`PF_LOCATION_ID=12170 PF_SLUG=binghatti_heights PF_PHOTOS=1`, then
`uv run python scripts/building_check.py`.

Raw pages and photos go to `data/raw/` (git-ignored).

## Layout

- `trust/models.py`: the data contract between the rules and the web page.
- `trust/rules.py`: the rules (R1-R6), as pure functions.
- `tests/test_rules.py`: one test per rule decision.
- `scripts/`: fetching, hashing, and building `web/data/listings.json`.
- `web/`: a static, mobile-first prototype in plain HTML and JS. No build step.

## Data sources and licence

- **Property Finder public listing pages (propertyfinder.ae):** price, size, dates, badges, permit
  link, and the registered deals each page shows. We used them for this non-commercial evaluation
  only and keep derived fields, not photos or descriptions. The content remains Property Finder's
  and the advertisers'.
- **DLD Open Data (dubailand.gov.ae open data):** one month of rent contracts and sales (4 Oct to 4
  Nov 2026), plus all 2026 sales in Dubai Marina and JVC (1 Jan to 5 Nov), used for
  `research/dld_check.md`. Terms not published. Only aggregates are committed; raw files are
  git-ignored. Earlier years are on data.dubai and were not used.
- **Model answers in `research/ai-checks/`:** generated with Claude for AI-LOG.md.

## Assumptions, and what would prove this wrong

- **Assumption:** the agent's "available from" date is roughly honest when set, so a date long past
  means the unit has probably gone. This would be proved wrong if agents confirm that most of the
  flagged units are still available. The ONE-PAGER sets the bar at fewer than 1 in 10 turning out
  to be gone.
- **Assumption:** the registered deals on a listing page are the right benchmark for a fair price.
  For sales there were only 4 in the last 12 months, so buy-side price verdicts are weak.
- **Tested against DLD, not settled:** if a stale "available" date meant the flat had gone, stale ads
  should more often have a new DLD contract of the same size in the same building. Not supported, and
  the proxy cannot tell. Princess Tower loose match 95% stale vs 100% fresh; strict (rent within
  10%) 49% vs 77%, the opposite way. Binghatti Heights no difference within bedroom counts (1-bed 89%
  vs 87%, 2-bed 52% vs 47%). It is size-level not unit-level, one month, no unit numbers. Unit-level
  Ejari access could settle it. So the assistant keeps stale dates as "ask the agent", never "hide".
- **Samples, not a census.** Rentals in six neighbourhoods and two towers. The neighbourhood samples
  are the first result pages, which favour fresh ads. Villas, off-plan and other emirates weren't
  checked.

## Cut

- A live LLM in the prototype, which would read agents' free-text replies and the descriptions.
- Interior-only photo matching.
- A mock Scout screen: the least evidence per minute.
- An eye check of every listing. 195 were checked by hand; the rest got the automatic checks only.
