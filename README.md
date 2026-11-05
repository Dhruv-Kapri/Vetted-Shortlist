# A search assistant people trust (prototype)

An assistant inside Property Finder search that works for one person looking for a home. It hides
listings that are likely fake or misleading, says why, asks the agent the questions the person would
otherwise phone round about, and keeps a short list they can trust. It works for renters and buyers.
The agent stays in the deal.

**Live prototype (open on a phone):** https://vetted-shortlist.vercel.app

**Read these first:**

- [ONE-PAGER.md](ONE-PAGER.md): the problem behind the problem, where the assistant lives, metrics,
  and what we couldn't build.
- [AUDIT.md](AUDIT.md): 55 live Princess Tower listings checked one by one, plus a price check of the
  whole building.
- [RULES.md](RULES.md): every rule, where it's wrong, and who gets hurt.
- [AI-LOG.md](AI-LOG.md): confident wrong AI answers about UAE real estate, and how we caught them.

## Numbers first

These come from Princess Tower, Dubai Marina, read on 5 Nov 2026. The audit covers 55 two-bed
listings in the common 1,181-1,189 sqft layout: 32 to rent and 23 for sale.

- **0 of 32 rentals priced like bait.** All are within 5% below to 57% above the median of 21 recent
  registered rents (AED 115K).
- **14 of 32 rentals give an "available from" date more than 45 days old.** The oldest is 489 days.
- **54 of 55 listings carry "Verified".**
- **Duplicates:** see AUDIT.md for the groups confirmed by eye and by photo hash.
- **The prototype's verdicts on the 55:** 39 on the short list, 14 for the assistant to check with
  the agent, 2 hidden.

## What is real and what is mocked

| Part | Real or mocked |
|---|---|
| Listings (price, size, cheques, dates, badges, agency, permit link) | **Real**, from public listing pages, read on 5 Nov 2026 |
| Registered rents and sales for the same size | **Real**, as shown on each listing page |
| Photo matching | **Real**: a 64-bit difference hash of each listing's first 3 photos. The photos themselves are not in the repo |
| The rules and verdicts | **Real**, computed by `trust/rules.py` from the data above |
| Agent replies in "Ask the agent for me" | **Mocked**, and labelled in the app. Nothing is sent to any agent |
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
```

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
- **Model answers in `research/ai-checks/`:** generated with Claude for AI-LOG.md.

## Assumptions, and what would prove this wrong

- **Assumption:** the agent's "available from" date is roughly honest when set, so a date long past
  means the unit has probably gone. This would be proved wrong if agents confirm that most of the
  flagged units are still available. The ONE-PAGER sets the bar at fewer than 1 in 10 turning out
  to be gone.
- **Assumption:** the registered deals on a listing page are the right benchmark for a fair price.
  For sales there were only 4 in the last 12 months, so buy-side price verdicts are weak.
- **One building, one layout.** Bait pricing may be common elsewhere, in cheaper communities. We
  checked the rest of Princess Tower (see AUDIT.md), but no other building.

## Cut

- A live LLM in the prototype, which would read agents' free-text replies and the descriptions.
- Interior-only photo matching.
- A second building.
