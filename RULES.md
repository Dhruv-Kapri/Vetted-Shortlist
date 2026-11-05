# The rules the assistant follows

The assistant works for the person searching. It only uses what that person could see themselves on
the listing page. It reads it all, for every listing, and compares listings with each other. That
covers the price, the registered rents and sales for the same unit size that the page shows, the
agent's own "available from" date, the DLD permit link, the badges and the photos. The code is in
`trust/rules.py`, and `tests/test_rules.py` pins each decision.

**Three outcomes, never more:**

| Outcome | When | What the person sees |
|---|---|---|
| **Short list** | No rule raises a warning or a block | The listing, with the checks it passed |
| **Assistant will check** | Any warning, and no block | The listing, with the open question. The assistant asks the agent first, and the answer decides |
| **Hidden** | Any block | Not in the list by default. "Why hidden?" shows the reason, one tap away |

**When it is not sure, it asks rather than judges.** Missing data never hides a listing. It turns
into a question to the agent (R1b). Hiding is only for strong evidence that a searcher can check
for themselves.

---

## R1: Too cheap to be true (bait price)

- **Rule:** compare the price with the median of the registered deals for the same size (±10 sqft).
  For rentals, the deals come from the last 6 months. For sales, the last 12 months. The deals are
  pooled from every audited page in the building. Under 75% of the median → **hidden**. From 75% to
  90% → **check**: the assistant asks for the full price and the number of cheques (for rent) or
  for the final price and whether the unit is tenanted (for sale).
- **R1b:** fewer than 3 registered deals → **check**, never hidden. Not enough evidence to judge.
- **Why these numbers:** in Princess Tower, the middle half of 2-bed contracts lies between 87% and
  118% of the median (AED 103-140K around 118.5K). Under 75% is outside anything we saw, apart from
  one AED 50K contract that looks like a special case.
- **Does the threshold matter?** Hardly. Even at 90%, at most 14% of an area's rentals count as cheap.
  At 75%, none do in any of the 8 places we checked (AUDIT.md, "What counts as a bait price").
- **Where it's wrong:** a landlord who needs a tenant this week, a unit on a low floor with a bad
  view, or a sale by an owner who has to sell (divorce, leaving the country, a bank sale).
- **Who gets hurt:** **an honest agent**, whose genuine deal gets hidden, and **the person
  searching**, who misses it. To soften that, a hidden listing stays one tap away with its reason,
  and the person can still say "ask anyway".

## R2: Same flat, listed more than once

- **Rule:** two listings with the same offering, the same number of bedrooms, sizes within 5 sqft,
  and at least one matching photo count as one flat. A photo matches when its 64-bit difference
  hash is no more than 6 bits from the other. All matching listings are grouped. The assistant
  keeps one: the one with a permit link, then the Verified badge, then the price closest to
  registered deals, then the newest. The others are **hidden** as duplicates. The kept card says
  "Same flat listed N times by K agencies at AED min-max", because that price spread is useful
  information in itself.
- **Where it's wrong:**
  - Agencies reuse photos from the developer or the building's common areas (lobby, pool, the
    view) for different units. In a 101-storey tower with identical layouts, two genuinely different
    flats can share a pool photo.
  - Two agents may both hold a real mandate for the same flat. That's legal in Dubai, because owners
    often give several agencies the right to advertise. Hiding one is then a choice, not a judgement
    of fraud.
- **Seen in the audit:** Flat A's three rent ads (AED 135K, 140K, 150K) each match their own valid
  DLD permit. A duplicate is not proof of wrongdoing. That's why the kept card shows the price
  spread instead of accusing anyone.
- **Who gets hurt:** **an honest agent** whose different unit is folded under someone else's card,
  or whose real mandate loses to a competitor's. The person searching loses little, because the flat
  is still on the list.
- **What we'd change with more time:** match on interior photos only, and leave out exterior and
  amenity shots.

## R3: "Available" long ago (stale rental)

- **Rule:** for rentals, if the agent's own "available from" date is more than 45 days in the past
  and the ad is still up → **check**. The assistant asks "Is it still available, and when can I view
  it?" before the person spends a call.
- **Why:** this was the commonest problem in the audit. It's also invisible in search results,
  because the date only shows on the listing page. The Verified badge doesn't help, because it is a
  document check and not a daily availability check.
- **Where it's wrong:** an agent who never updates the date after re-listing a unit that really is
  available, or a landlord holding out for a high price, so the flat really has been empty for
  months.
- **Who gets hurt:** **an honest agent** gets one extra question before the lead reaches them. Nobody
  is hidden by this rule, because staleness is a question, not proof.

## R4: No permit shown

- **Rule:** no DLD permit validation link on the listing → **hidden**. In Dubai, a property ad needs
  a DLD advertising permit (Trakheesi).
- **Where it's wrong:** a portal display bug, or a permit that exists but wasn't linked.
- **Who gets hurt:** **an honest agent**. In our audit, all 55 listings showed a permit link, so this
  rule never fired here. It guards the floor, not the building we checked.
- **Limit:** we can see that a link is present, but not that the permit matches this unit and this
  price. That check needs the DLD's systems (see the one-pager, "What we could not build").

## R5: Photos that may not show the real flat

Not every edited photo is a lie, so the assistant grades them:

| What we see | Example | Outcome |
|---|---|---|
| Touch-up: brightness, sky, lens correction | Most listings | Nothing. It's normal |
| Virtual staging, **disclosed** in the ad | "Furniture digitally added" | **Information** chip. It helps you imagine an empty flat |
| Staging or AI-generated rooms, **not disclosed** | 135143057: rooms look rendered, with wooden floors where the tower's standard is tiles | **Check**: "Are the photos of this flat as it is today?" |
| The same, and the ad says **"Furnished"** | 135143057 again | **Check**, adding: "Is the furniture shown in the flat?" Furniture that isn't there is part of the price |
| First photos show only the view or the pool | 161902017, 158224698 | **Check**: "Can you send photos or a video of this exact flat?" |
| The same photos on the agent's 1-, 2- and 3-bed listings | 169274661, 158717394 | **Check**, with the same question |
| Photos of a different building (forgery) | None found | **Hidden** |

- **Where it's wrong:** an honest agent using a professional 3D render of a flat that really is being
  furnished to that design, or a real flat renovated so well it looks rendered. They get one
  question. Nobody is hidden unless the photos are of a different building.
- **Who gets hurt:** **an honest agent**, delayed by a question. If the assistant misses undisclosed
  staging, **the person searching** gets hurt: they visit and find an empty flat.
- **Limit:** in the prototype, the photo issues come from our own eye check (AUDIT.md). None of the
  217 listings in the building disclosed staging in its text. In production, this needs an image
  model (see the one-pager).

## R6: Well above recent deals (information only)

- **Rule:** over 125% of the registered median → an **information** chip ("Price 32% over recent
  deals"). The status doesn't change.
- **Why only information:** an overpriced ad is not a fake ad. The person should know, because it
  gives them room to negotiate, but the agent did nothing wrong.
- **Where it's wrong:** an upgraded unit, a high floor with a full sea view, or furniture included.
  Those are real reasons for a premium, and the registered deals don't record them.
- **Who gets hurt:** **an honest agent** with a premium unit looks expensive. The chip says "over
  recent deals", never "overpriced".

---

## What the assistant asks the agent, on the person's behalf

Every message starts from the open flags (the warning questions above). Then come the standard
questions, which the person can untick before sending:

- **Renting:** Is it still available, and from what date? What is the full yearly rent, and in how
  many cheques? What are the agency fee and the security deposit? Can I view it this week?
- **Buying:** Is it vacant or tenanted, and if tenanted, when does the lease end? Is the asking price
  final, and what is the service charge? Is there a mortgage that needs a bank release? Can I view
  it this week?

**The answer moves the listing.** If the unit is available at the advertised price, it goes onto the
short list with viewing slots. If it's gone, or the price is higher than advertised, it's removed,
and the assistant records why. In a real product, an agent who repeatedly replies "gone, but I have
another one" would be a signal about that agent (see the one-pager).

## Rules we considered and did not ship

- **Automatic photo checks:** R5 runs on our eye check. Doing it automatically needs an image model
  that knows each tower and can tell staging from a touch-up. We list it as a missing feature rather
  than fake it.
- **Agent track record** (how often their listings turn out to be gone): this needs Property
  Finder's own lead and response data.
