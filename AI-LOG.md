# AI log: confident wrong answers about UAE real estate, and how we caught them

Method: we asked Claude (`claude-sonnet-5-5`, through the API, no web access) the questions a person
searching in Princess Tower would ask. The script is `scripts/ask_model.py` and the verbatim answers
are in `research/ai-checks/claude-sonnet-answers.json`. We then checked each answer against what the
listing pages themselves show: the registered rents and sales for the same unit size, the agent's
"available from" date, and the listing data from our audit (`AUDIT.md`). We also log the mistakes
our coding assistant made while building this.

## 1. "A 2-bed in Princess Tower rents for AED 135,000-165,000 a year"

- **What it said (Q1):** "Roughly AED 135,000-165,000 per year." In a separate answer (Q3) it said
  2-beds "have recently rented for roughly AED 120,000-170,000+ a year".
- **What the evidence says:** the listing pages show the registered rents for the same size. Pooled
  across our 32 audited listings, there are 24 registered contracts from the last 6 months for this
  2-bed layout (±10 sqft). Their median is **AED 118,500**, and the middle half falls between AED
  103,000 and 140,000. The model's low end is above the median of real contracts, and the middle of
  its range (150K) is above three-quarters of them.
- **How we caught it:** we compared every number against `similar_price_transactions` on the listing
  pages, never against other listings' asking prices.
- **Why it matters:** an assistant that trusts this range would mark honest AED 110-120K listings as
  "suspiciously cheap". That hurts honest agents, and it pushes the person toward the overpriced ones.

## 2. "Verified means the property is real and available"

- **What it said (Q4):** the Verified badge means "the property appears to be real and available,
  with photos, location, and price matching what's advertised".
- **What the evidence says:** Property Finder describes Verified Listings as a document check by its
  quality team (an advertising agreement and the owner's ID), done once the documents are in. It
  doesn't re-check availability every day. In our audit, **53 of 55** listings carry the badge,
  including one whose own "available from" date is **489 days** old (listing 162770873). Another
  Verified ad at AED 180,000 has been up since June and is priced 57% above recent contracts
  (listing 104675044).
- **How we caught it:** we counted the badge across the audit and set it against each listing's own
  "available from" date. Source for what the badge means: Property Finder's announcement,
  <https://www.propertyfinder.ae/blog/propertyfinder-ae-sets-industry-benchmarks-with-the-release-of-verified-listings>.
- **Why it matters:** this shaped our rules. The badge is treated as proof of authority to advertise,
  never as proof of availability (see RULES.md, R3).

## 3. "Paying in fewer cheques means a higher yearly rent"

- **What it said (Q1):** "Fewer cheques (e.g., 1-2 payments) often means a higher annual price than
  4 or more."
- **What the evidence says:** in our 32 audited rentals, the median asking rent is **AED 120,000 for 1
  cheque (11 listings) and AED 130,000 for 4 cheques (7 listings)**. The same holds among furnished
  units only (120,000 vs 127,500). That's the usual Dubai pattern: landlords give a discount for
  payment upfront. The sample is small, but it points the opposite way from the model.
- **How we caught it:** we grouped the audit's asking rents by `number_of_cheques`.
- **Why it matters:** the assistant compares prices "for how many cheques". Getting the direction
  wrong would make a fair 4-cheque price look padded.

## 4. Our own coding assistant: an invented service charge

- **What happened:** while writing the mocked agent replies for the prototype, the coding assistant
  (Claude Code) wrote "Service charge about AED 19/sqft" for Princess Tower buyers. It had no source
  for that number.
- **How we caught it:** we reviewed every number in the mocked data against a source before
  committing. This one had none, so it was replaced with "service charge figure to follow from the
  owner". It's now one of the questions the assistant asks the agent.
- **Lesson:** mocked data must contain no made-up facts. The prototype labels every agent reply as
  mocked.

## 5. A subagent's DLD check: the wrong listing, and a stale date

- **What happened:** we delegated the DLD cross-check and the stale-vs-fresh test to a subagent. It
  reported it "could not reproduce n=24". The orchestrator found why: it had tested a different
  listing, the cheapest of all 217 (AED 105,000, 1,298 sqft), not the cheapest of the 55 audited. The
  n=24 claim was about the audited ones. Note that `research/dld_check.md` still carries the
  subagent's wording on this point.
- **A second catch:** the new agent view mocked the searcher's move-in date from the listing's own
  stale "available from" date. It was fixed so the mocked move-in no longer reuses that date.
- **Lesson:** check which object a subagent's "could not reproduce" was run on before believing it.

## What the model got right (so we don't overstate the log)

The 5% / 10% security deposit, the 5% agency fee, the Trakheesi permit requirement and the 4% DLD
transfer fee all match public guidance. Its sale range for a 2-bed (AED 2.0-2.5M) covers the
four registered sales from the last 12 months (AED 1.8M-2.6M, median 2.05M). Four sales is a thin
base, so we say that wherever the assistant uses it.
