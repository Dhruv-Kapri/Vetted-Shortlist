# A search assistant people trust: one-pager

**What it is:** an assistant that works for one home searcher. It checks every listing they view,
hides likely fake or misleading ones and says why, and asks agents what the person would otherwise
phone about: is it free, the real price, cheques and fees, a viewing time. Viewing, negotiation and
contract stay with the agent.

## 1. The problem behind the problem

**The main lie is "available", not the price.** It wears down trust in the whole platform until
people hand everything to one agent.

**What the audit showed.** In Princess Tower, Dubai Marina, we checked 55 live 2-bed listings by
hand, photos included, and ran all 217 listings through price and availability checks. We repeated
the automatic checks in Binghatti Heights, JVC (267 listings), against registered contracts for the
same unit size.

- **Bait prices barely exist.** No listing in either building is under 75% of registered deals. The
  cheapest Princess Tower 2-bed rental is 7% under the median of 24 recent registered rents (AED
  118,500).
- **"Available" is where it goes wrong.** 13 of the 32 audited rentals show an "available from"
  date over 45 days old, one 489 days old. Across all listings: 47 of 119 rentals in Princess
  Tower, 79 of 218 in Binghatti Heights.
- **The same flat appears more than once.** By eye, 11 of the 55 audited listings belong to just 3
  flats. One 2-bed is for rent at AED 135K, 140K and 150K through three agencies, and for sale
  through two more listings. **It's not fraud: each ad matches its own valid DLD permit, price
  included.** It's legal and misleading at once, and only a comparison across listings shows it.
- **Photos may not show the flat in 6 of 55:** views or pool only, photos reused across unit sizes,
  or computer-staged rooms on a "Furnished" ad. None is disclosed.
- **53 of 55 carry the "Verified" badge**, including the 489-day one. The badge checks documents
  once. It can't tell live from let.
- **Six neighbourhoods, luxury to budget** (about 75 rentals each, first result pages):

  | Area | Under 75% (bait) | Over 125% | Stale >45 d | Verified |
  |---|---|---|---|---|
  | Palm Jumeirah | 0% | 21% | 18% | 99% |
  | Downtown Dubai | 0% | 16% | 29% | 99% |
  | Dubai Marina | 0% | 8% | 22% | 96% |
  | JVC | 0% | 10% | 11% | 84% |
  | Discovery Gardens | 0% | 0% | 21% | 95% |
  | International City | 0% | 13% | 25% | 83% |

- **140 more checked by hand** (20 per area, half random): in the random half, **0 bait, 19% stale,
  10% photos that may not show the flat**. All 22 permits checked for the cheapest ads match the ad
  price. A second same-flat-two-prices case turned up in Binghatti Heights (AED 69,999 vs 75,000,
  both with valid permits).

None is *proven* fake: only the agent can confirm a unit is gone. But **23 of the 55 show at least
one of these signs.**

**Why it exists.** A paid ad is cheap to keep up, and every call is a lead the agent can steer
elsewhere, so nobody takes a let unit down. The searcher pays with weeks of calls, honest agents with
drowned listings, and **the platform last and most.**

**What the person really wants** is **someone on their side who has already asked**: "free, at this
price, four cheques, viewing Saturday."

## 2. Where it lives

Not the homepage, but where trust breaks:

1. **Search results, under the filters.** "Your assistant checked 32 listings: 13 on your short
   list, 14 to confirm with the agent, 5 hidden. Why?" Duplicates become one card.
2. **The listing page, next to Call and WhatsApp.** "Ask the agent for me" beside "Call yourself",
   with "Before you call" showing the checks.
3. **Inside Scout.** Results pass the same rules: "I hid 3 and asked 5 agents."

**Web and app, one thread.** The short list and agent chats live in the Property Finder account.
People research on the web; replies arrive as app notifications. Logged-out sessions hand over by QR
code or link.

## 3. Why use it instead of searching and calling, and when not to

**Use it** for more than a handful of listings. It makes five calls in parallel, asks the same
questions every time, and sees across listings, as no single agent will.
**Don't use it** when you know the building and agent and need a viewing today, when negotiating or
signing, or off-plan, where the developer confirms availability.

## 4. What it means for agents and for Property Finder

- **Honest agents:** pre-qualified leads, fewer "is it still available?" calls.
- **Volume and bait agents:** stale ads stop earning calls.
- **Revenue risk:** fewer raw leads on hidden or duplicate listings, so volume-paying agents may
  complain. **Upside:** leads that become viewings are worth more, and "Verified" means something
  again. A paid "confirmed available this week" status, earned by quick answers,
  rewards clean listings.

## 5. Which metrics it moves

- **Searcher side:** active searchers, contacts per searcher, contact-to-viewing rate, repeat use.
- **Agent side:** leads per listing, lead-to-viewing rate, subscription renewal.

**It moves contact-to-viewing up and wasted contacts down.** About 4 in 10 rental listings in our
building had a stale "available" date. Suppose half are gone: roughly 1 in 5 first calls is wasted today,
and the assistant removes most. As an estimate from one building: **contact-to-viewing
up 15-25% for people who use it**, with leads per searcher flat or slightly down.

## 6. One number that proves it works

**Viewings booked per active searcher within 14 days.**

- **Test:** randomise 1% of Dubai searchers, by user. Guardrails: leads to agents whose listings
  pass every rule, and agent complaints.
- **We're wrong if:** viewings per searcher are not at least 5% higher after 4 weeks, or fewer than
  1 in 10 of the "available long ago" listings it asks about turn out gone. Then staleness isn't the
  problem.

## 7. What we could not build (priority order)

| # | Feature | Why it's needed | Why we couldn't add it |
|---|---|---|---|
| 1 | **Real messaging with agents** (send the questions, read structured replies) | The core of the product: replies drive the short list | Needs Property Finder's internal lead and messaging channel. Agent replies in the prototype are mocked |
| 2 | **Unit identity** (DLD unit or property ID behind each listing) | Exact duplicate detection instead of photo matching, which merges look-alike balconies | Not public. The listing data has an empty unit field. Needs an internal Property Finder connection |
| 3 | **Live availability signal** (has a new Ejari contract been registered on this unit?) | Turns "probably gone" into "gone" without asking the agent | Ejari data is not public at unit level. Needs government data access |
| 4 | **Permit-to-listing match at scale** (the permit's price, size and type match the ad) | Catches ads whose price or unit differs from the permit. We did it by hand for Flat A's 5 permits | Permit cards are public but have no unit number and no API; checking every listing needs DLD integration |
| 5 | **Agent track record** (how often their "available" turns out to be gone, response time) | Lets the assistant trust some agents faster | Needs Property Finder's internal lead and response data |
| 6 | **Automatic photo checks**: interior-only matching, staging and AI-image detection, "is this the right building" | Fewer false duplicates. Catches undisclosed staging and photos from another tower. In the prototype these come from our eye check | Needs engineering help (image models trained on each tower) |
| 7 | **Accounts, cross-device sync and push notifications** | The web-to-app handover in section 2 | Needs the Property Finder app and accounts. Shown as a placeholder |
