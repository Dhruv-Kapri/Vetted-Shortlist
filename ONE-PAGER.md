# A search assistant people trust: one-pager

**What it is:** an assistant that works for one person searching for a home. It checks every listing
they're looking at, hides the ones that are likely fake or misleading and says why. It asks the
agents the questions the person would otherwise phone round about: is it still free, the real price,
the cheques and fees, a viewing time. Then it brings back a short list the person can trust. The
agent stays in the deal: the viewing, the negotiation and the contract are theirs.

## 1. The problem behind the problem

**Our audit says the main lie is "available", not the price.** We checked 55 live 2-bed listings in
one building, Princess Tower in Dubai Marina, and compared them with registered contracts for the
same unit size, which the listing pages show:

- **Zero of 32 rentals were priced like bait.** The cheapest was 7% under the median of 24
  registered rents in the last 6 months (AED 118,500). Across the whole building, 0 of 217 listings
  were under 75% of registered deals.
- **13 of 32 rentals give an "available from" date more than 45 days old**, and 47 of 119 across the
  building. One is 489 days old.
  The ads are still up and still collecting calls.
- **53 of 55 carry the "Verified" badge**, including that 489-day one. The badge checks documents
  once. It can't tell a live unit from a let one.
- **The same flat appears more than once.** We matched photos by eye and found one 2-bed in five
  listings: for rent at AED 135K, 140K and 150K through three agencies, and for sale through two.
  Of the 55 audited listings, 11 belong to just 3 flats.

**Why it exists.** An ad costs little to keep up once it's paid for, and every call is a lead. A
let unit keeps producing calls the agent can steer to other units, so the agent has no reason to
take it down. Volume agents gain. The person searching pays with weeks of calls. Honest agents pay
too, because their real listings drown among zombies. **The platform pays last and most.** People
don't just lose trust in one agent. They get tired of the whole portal and hand everything to one
agent they met, so the portal loses the searcher.

**What the person really wants** isn't fewer listings or a different kind of listing. They want
**someone on their side who has already asked**: "this one is free, at this price, in four cheques,
and you can see it Saturday." That's the assistant.

## 2. Where it lives

Not on the homepage. It appears at the three moments when trust breaks:

1. **Search results, under the filters.** "Your assistant checked 32 listings: 16 on your short
   list, 11 to confirm with the agent, 5 hidden. Why?" Duplicates collapse into one card that shows
   the price spread.
2. **The listing page, next to Call and WhatsApp.** This is the moment the person is about to spend
   a call. "Ask the agent for me" sits beside "Call yourself", and "Before you call" shows the
   checks.
3. **Inside Scout.** When someone types "2-bed in Princess Tower under 130K", Scout's results go
   through the same rules: "I hid 3 and asked 5 agents."

**Web and app, one thread.** The short list and the agent conversations belong to the person's
Property Finder account. People research on the web at their desk, and the replies arrive as app
notifications ("The Princess Tower 2-bed is free from 1 Dec, viewing Saturday 10:00?"). A logged-out
web session can hand over with a QR code or link.

## 3. Why use it instead of searching and calling, and when not to

**Use it** when you're looking at more than a handful of listings. It makes the five calls in
parallel, asks the same questions every time, and compares the answers (cheques, fees, deposit,
availability date), which a person on the phone rarely does. It also sees across listings in a way
no single agent will: the same flat at three prices.
**Don't use it** when you already know the building and the agent and just need a viewing slot today
(call), or when you're negotiating or signing (that's the agent's job). It also adds little for
off-plan purchases from a developer, where availability is the developer's to confirm.

## 4. What it means for agents and for Property Finder

- **Honest agents get easier work.** Their leads arrive pre-qualified: dates, budget and cheques are
  already asked, and they spend less time on "is it still available?" calls. Their real listings
  stop competing with zombies.
- **Volume and bait agents get harder work.** Stale ads stop generating calls, and duplicates fold
  into one card.
- **Revenue risk:** fewer raw leads on hidden or duplicate listings, so agents who pay for volume may
  complain. **Revenue upside:** leads that turn into viewings are worth more, and "Verified" can mean
  something again. A paid "confirmed available this week" status, earned by answering the
  assistant quickly, gives agents a reason to keep listings clean.

## 5. Which metrics it moves

The big metrics of a portal:

- **Searcher side:** active searchers, contacts per searcher, the share of contacts that reach a
  viewing, and repeat use.
- **Agent side:** leads per listing, lead-to-viewing rate, and renewal of their subscriptions.

**This moves the contact-to-viewing rate up and wasted contacts down.** In our building, about 4 in
10 rental listings carried a stale "available" date. Suppose half of those are really gone. Then
roughly 1 in 5 first calls is wasted today, and the assistant removes most of those. As an estimate
from one building, that means **contact-to-viewing up by 15-25% for people who use it**, with total
leads per searcher flat or slightly down.

## 6. One number that proves it works

**Viewings booked per active searcher within 14 days.**

- **Test:** randomise 1% of Dubai searchers, at the user level, to see the assistant. Watch two
  guardrails: leads to agents whose listings pass every rule, and agent complaints.
- **What proves us wrong:**
  - Viewings per searcher are not at least 5% higher after 4 weeks.
  - Or, our core belief fails: fewer than 1 in 10 of the "available long ago" listings the
    assistant asks about turn out to be gone. Then staleness is not the problem, and we built the
    wrong thing.

## 7. What we could not build (priority order)

| # | Feature | Why it's needed | Why we couldn't add it |
|---|---|---|---|
| 1 | **Real messaging with agents** (send the questions, read structured replies) | The core of the product: replies drive the short list | Needs Property Finder's internal lead and messaging channel. Agent replies in the prototype are mocked |
| 2 | **Unit identity** (DLD unit or property ID behind each listing) | Exact duplicate detection instead of photo matching, which merges look-alike balconies | Not public. The listing data has an empty unit field. Needs an internal Property Finder connection |
| 3 | **Live availability signal** (has a new Ejari contract been registered on this unit?) | Turns "probably gone" into "gone" without asking the agent | Ejari data is not public at unit level. Needs government data access |
| 4 | **Permit-to-listing match** (the Trakheesi permit is valid for this unit and this price) | Catches ads with a real permit for a different unit | Only the validation link is public. Needs DLD integration |
| 5 | **Agent track record** (how often their "available" turns out to be gone, response time) | Lets the assistant trust some agents faster | Needs Property Finder's internal lead and response data |
| 6 | **Interior-only photo matching and "is this the right building"** | Fewer false duplicates. Catches photos from another tower | Needs engineering help (image models trained on each tower) |
| 7 | **Accounts, cross-device sync and push notifications** | The web-to-app handover in section 2 | Needs the Property Finder app and accounts. Shown as a placeholder |
