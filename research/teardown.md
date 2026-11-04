# Property Finder product teardown

Observed on 4 Nov 2026, desktop Chrome, English site (propertyfinder.ae), Dubai searches. Read-only:
no enquiries, no sign-ups. **O:** is what I saw on the page; **Opinion:** is my reading of it.

## Who pays, and for what

- **O:** Listing badges in search results: `Premium`, `Featured` (default sort is "Featured"),
  `Spotlight`, `Verified`, `SUPERAGENT`. New-projects results mix in "New Projects Expert" agent cards
  between project cards.
- **O (public partner pages, not verified in product):** agencies buy listing credits (PF Flex packs
  covering standard, featured and premium exposure). Spotlight takes the top three slots through
  bidding. SuperAgent is a monthly-refreshed badge based on listing quality, responsiveness,
  transactions and ratings.
- **O:** Other revenue lines visible on the site: mortgage brokerage ("Get a mortgage", with lead forms
  on the home page, the mortgage page and the rent-vs-buy page), developer projects (2,985 off-plan
  projects, with developer pages such as Emaar 214 projects and Damac 161), and "Sell your property"
  leads routed to SuperAgents.
- **Opinion:** Consumers pay nothing. The product sells agent and developer exposure and leads. So
  every consumer feature has two jobs: help the seeker, and send a higher-quality lead (call or
  WhatsApp) to a paying agent. Lead quality and listing trust are the levers both sides care about.

## Funnel map

search -> listing view -> lead (Call / WhatsApp / form) -> transaction (off-platform, recorded later
in DLD data, which Property Finder shows back as "Transactions").

## Surfaces

### Home (`/en`)
- **User / job:** any seeker. "Start somewhere."
- **Funnel step:** search entry.
- **O:** The hero search has tabs `Rent | Buy | Sell | New projects | Transactions | Agents`. Chips
  below it: `Rent in 12 (New)`, `Property type`, `Beds & Baths`, `Price`, `Amenities`, `Residential`.
- **O:** A "Browse property transactions" widget says "Powered by Dubai Land Department transaction
  data". It shows New rentals 140,632 AED, Renewed rentals 96,409 AED, and Transactions 265.4K
  (-26.03%). No period or unit type is shown next to these averages.
- **O:** "Search by top communities" with lifestyle tabs (Budget-Friendly, Family Friendly,
  Pet-Friendly, and others) and community star ratings, e.g. Dubai Marina 3.9 from 1,163 reviews.
- **O:** A mortgage pre-approval callback form, new-project carousels, and a developer grid.
- **O:** A "Your property's future? Let's find out" block for the AI valuation. The web version only
  offers a QR code and store badges, so the tool itself is app-only.
- **Opinion:** The DLD averages without a period, segment or comparison base are easy to misread.
  Rent gap: new rentals average 140.6K against 96.4K for renewals, a 46% premium. That premium is a
  real insight for renters, but the page doesn't explain it.

### Search results (rent: `/en/rent/dubai/apartments-for-rent.html`)
- **User / job:** a renter or buyer narrowing to a shortlist.
- **O:** "Apartments & Flats for rent in Dubai, 89,786 properties". Community chips show counts
  (Jumeirah Village Circle 13,742, Business Bay 8,286, and so on).
- **O:** Controls are `Filters`, a sort icon, a bell icon ("Create alert") and `Map`. Sort options:
  Featured, Newest, Price (low), Price (high), Beds (least), Beds (most). There is **no
  price-per-sqft sort and no "best value" sort**.
- **O:** The "More Filters" panel offers Furnishing, Property Size, **Number Of Cheques**, Property
  Enhancements (Upgraded/Extended/Landscaped), about 20 amenities, Keywords, Agency, and Floor Plan /
  360 / Video / Live Viewings. On web there is no commute, school or "price vs market" filter. (The
  Play Store listing says the app's filters include commute.)
- **O:** A listing card shows price, a tagline written by the agent ("Fully Furnished | Prime
  Location | Ain View"), beds/baths/area, the building, the agent's name and photo, and `Call` and
  `WhatsApp` buttons. The agency logo shows on Premium cards.
- **O:** `Rent in 12` cuts the results to 9,629 listings and shows a monthly price, e.g. 95,000
  yearly shown as "Rent in 12 8,851/mo". That works out to 106,212 a year, about 11.8% more than the
  yearly price. The App Store "What's new" (v14.62.0, 4 days old) describes this as "Rent now, pay
  monthly", with income verification and in-app rent tracking.
- **Opinion:** The default sort is "Featured", which is the paid order. Seekers have no way to sort by
  value, and that is exactly where "is this a good price?" goes unanswered.

### Map view (`/en/map-search`)
- **O:** Google Maps with pins that show either a price ("265K") or a cluster ("84 units"), a draw
  tool and a Map/Satellite toggle. I saw no layers for schools, metro or commute time.
- **Opinion:** It works for "where", but not for "what's near my office or my kids' school".

### Listing page (`/en/plp/rent/...`, a 1-bed in Dubai Marina at 135,000/yr)
- **User / job:** decide whether to contact the agent.
- **Funnel step:** listing view to lead. This is the money page.
- **O:** A gallery (32 photos, `Verified` tag), the price, and buttons for `Estimated upfront costs`,
  `Compare rent vs buy`, `View on map` and `Floor plan`.
- **O:** Property details: listed 7 days ago, type, beds, baths, cheques, furnishing, area 694 ft²,
  available from date. The description is free text written by the agent.
- **O:** A building block, "About [building]", showing 92 properties listed, a price range of
  105K-360K/year, and building reviews ("Be the first to review").
- **O:** **"Transactions for Similar Properties"** (DLD). It lists sold prices for 1-beds in the same
  building, e.g. 2.4M on 28 Nov 2025, and rented prices with dates, e.g. 130,000 on 20 Aug 2026 and
  155,000 on 18 Apr 2026. It credits "Powered by DataGuru".
- **O:** **"Prices & trends"**: a 1Y/2Y/5Y chart comparing the building with the community, plus
  "This property costs 31% more than the average. Average Rent is 103,312 AED" and "This property is
  19% smaller than the average. Average size is 854 sqft".
- **O:** An agent card (ratings, "Usually responds within 15 minutes", Call / WhatsApp), the agency
  (1,045 listings, 70 SuperAgents), and a mortgage cross-sell ("Talk to an expert").
- **O:** A regulatory block with the permit reference, broker licence, **licensed agency name**, zone
  and agent licence. The licensed agency name differed from the brand shown on the card (a trade name
  versus the licensed entity).
- **O:** The "Estimated payment breakdown" modal shows annual rent 135,000; agency fee 7,088 (5% +
  VAT); security deposit 13,500; DEWA deposit 2,130; Ejari fee 220; **total upfront 22,938**. It notes
  that rent "may increase when paying with multiple cheques".
- **O:** `Compare rent vs buy` opens a **generic** calculator (`/en/rent-vs-buy-calculator`)
  pre-filled with 140,000 rent and a 1,200,000 purchase price. It does not use this listing's 135,000
  or the 2.25-2.4M sold prices in the same building. Its result says "Buying becomes better than
  renting after 2 years", next to a Name/Email lead form.
- **Opinion:** The data is excellent: DLD history for the same building, right on the page. The
  synthesis is weak. "31% more than the average" compares a furnished, sea-view unit with every
  1-bed in the community, without adjusting for size, furnishing or view. Meanwhile the same
  building's recent rents (130-155K) suggest the price is fair. The page shows the numbers and leaves
  the renter to work out the verdict. The rent-vs-buy handoff loses all of the listing's context. The
  upfront-cost total leaves out the first rent cheque, which is what a renter actually has to find.

### Transactions (`/en/transactions/sold/dubai`)
- **User / job:** a buyer or investor checking the market.
- **O:** Sold/Rented toggle, period ("Last year"), usage, type, beds, completion. Header tiles: Avg.
  price 2,586,861 (-3.8%), Avg. price/sqft 1,897 (+3.4%), Avg. rental yield 5.71%, Transactions
  161,865 (-18.5%). "Sourced from" the DLD logo.
- **O:** An **AI-written summary card**: "Prices per square foot are up 3.42% to AED 1,897 even as
  transaction volumes fell 18.51%…" and a button, "Ask more about Dubai prices", that leads into Scout.
- **O:** A table with registered date, location, price, price/ft², completion (Ready/Off-plan), plot
  and built-up area, and specs. Some rows are flagged "Bulk transaction". Paging stops at "Page 1 of
  50" with 10 rows per page, so only 500 of 161,865 rows are visible. There is no export.
- **Opinion:** The averages mix land deals (one row: 34.8M, 12,211 ft² land in Al Wasl), bulk deals
  and off-plan units. A median, or a segment-level figure, would be more honest. The AI summary
  rewords the tiles. It doesn't tell me what to do.

### Area insights (`/en/area-insights/dubai`)
- **O:** "Best Areas to Live in Dubai", with lifestyle tabs (Family Friendly, Pet-Friendly, Proximity,
  and others). Community cards show a rating, the property-type mix and "Apartment prices starting
  from". For Palm Jumeirah it says "For rent: 74,890 AED/year, for sale: 590,000 AED, *Based on
  listing prices in last 3 months".
- **Opinion:** "Starting from" prices are skewed by outliers. 590K for a Palm apartment is almost
  certainly a hotel studio or a data quirk. It tells a seeker little about what a typical home costs.

### New projects (`/en/new-projects`)
- **User / job:** an off-plan buyer or investor comparing launches.
- **O:** "2985 New Off-Plan Projects in UAE", "1517 projects with developer stock". Filters include
  `Payment plan`. There is a `Projects | Units (New)` toggle, `Compare`, `Map`, and a floating
  **"Ask AI" (BETA)** button. Each card shows delivery date, launch price, payment plan count and
  WhatsApp, plus a sparkle icon that opens a Scout side drawer. Logged out, the drawer stayed on a
  loading skeleton.
- **Opinion:** This is where developer money is, and where AI is most visibly invested.

### Scout, the AI assistant (`/scout/v2`)
- **O:** "Welcome to PF Scout" (BETA). The greeting rotates through languages ("Search in the
  language you think in"). Quick searches: "New launches this month", "Under 20% down payment",
  "Post-handover plans", "Highest appreciation potential", "Emaar & DAMAC launches", "Ready in 2027
  under 2M". A "Market Pulse" strip shows New Launches This Month, Avg Down Payment 13%, Hottest
  Community "Dubai South (24 hot projects)", Off-Plan Momentum 67%, and Primary Market Share 58%.
- **O:** Logged out, a typed query (a renter's question) would not send. The sidebar says "Log in to
  explore UAE property values, trends, and personalised recommendations". **I did not get to test a
  conversation. Try it yourself while logged in.**
- **Opinion:** Scout is positioned for off-plan investors (payment plans, appreciation), not renters.
  Renters are the bigger audience: 89,786 rental apartments in Dubai alone. That makes them the gap.

### Agents (`/en/find-agent`)
- **O:** "Find your agent to find a home", with Agents/Companies tabs and filters for location or
  name, purpose, property type, language and nationality. Agent cards show the SuperAgent badge,
  rating, languages, and for-sale/for-rent counts. A "List your home with top SuperAgents" banner sits
  on the page.
- **Opinion:** Seekers choose agents by language and nationality, not by track record. Nothing on
  the card shows "deals closed in this building" or response rate, even though the listing page has
  "responds within 15 minutes".

### Mortgage (`/en/mortgage`, `/en/eligibility-calculator`)
- **O:** A calculator (purchase price, residency status, down payment 20%, 25 years, 3.75%, giving
  4,936 AED/month), a lead form (Name, Email, Phone, "Get a mortgage quote"), "We found 52,654
  properties within your budget", and claims of "90% … receive a call within 10 minutes" and
  "5,000 AED average savings".

### App (from store listings; I didn't run the app)
- **App Store:** 4.7 from 9.1K ratings, No. 8 in Lifestyle, v14.62.0 (4 days ago). It lists Home
  Valuation ("how much your property is worth today, follow price trends, and even get forecasts").
  Public press puts the launch at Dec 2025: Dubai residential only, a six-month outlook, a confidence
  score, and tracking of up to 10 properties.
- **Google Play:** 4.3 from 8.85K reviews, 1M+ downloads, updated 28 Oct 2026, "Contains ads".
  Filters are described as covering "location, budget, lifestyle, commute".
- **Recurring themes in recent reviews:** fake or bait listings and duplicates, with one review
  noting 45 people found it helpful. "AI imaging is also misleading in some cases". Listings in
  emirates other than Dubai (Sharjah) seen as low quality. Agents re-routing callers to other agents.
- **Mobile web:** not tested. The window resize didn't take, and DevTools device emulation isn't
  available through the browser tool I used. Open propertyfinder.ae on your phone for 5 minutes; you
  don't need to install an emulator.

### Bayut (competitor), from public press only
- **O:** bayut.com showed a human-verification check, so I didn't go further. Public sources say
  Bayut has **BayutGPT** (a conversational assistant, from about 2023-24), **TruEstimate** (an AI
  valuation on DLD data, Jun 2024, on web and app), and **AI Search** (conversational search with
  follow-up refinement, Aug 2026, which it bills as the only one in the UAE). Its roadmap mentions
  property search inside ChatGPT.
- **Opinion:** Bayut shipped valuation on the web about 18 months before Property Finder's app-only
  launch. Property Finder looks ahead on DLD-backed data placed in context (building-level
  transactions on the listing page, the AI summary on Transactions) and on fintech (Rent in 12).
  Conversational search for everyday renters looks like the competitive gap.

## Opportunities (ranked)

Score = user value × feasibility in about 3 h with public or provided data × measurability (1-5 each).
The task text is hidden until Start, so "fit" assumes it's an AI product build on the consumer
funnel. Re-rank once you've read it.

| # | Idea | V | F | M | Score |
|---|---|---|---|---|---|
| 1 | Fair-price verdict on a listing | 5 | 4 | 5 | 100 |
| 2 | Natural-language search for renters (Scout for renters) | 5 | 4 | 4 | 80 |
| 3 | True cost to move in, and Rent in 12 vs cheques | 4 | 5 | 4 | 80 |
| 4 | Listing trust score (bait price, duplicates, mismatches) | 5 | 3 | 4 | 60 |
| 5 | Rent vs buy using this listing's own data | 4 | 4 | 3 | 48 |
| 6 | Lead brief for agents (structured enquiry) | 4 | 3 | 4 | 48 |
| 7 | Plain-English market summary that says what to do | 3 | 4 | 3 | 36 |

**1. Fair-price verdict ("Is this a good price?")**: best fit
- **Problem:** The listing page shows the building's DLD rents and a crude "31% more than the
  average", but leaves the judgement to the renter. Fear of overpaying slows the decision to contact
  the agent.
- **Metric:** listing-view → lead conversion. Secondary: share of leads on listings with a "fair"
  verdict.
- **3-h prototype:** take a listing (URL or typed fields). Find comparables in the same building and
  community from transaction data, matched on size band, beds and furnishing. Produce a verdict
  (below / fair / above) with a range and a confidence level, plus an LLM explanation in two sentences
  that cites the comparables. Streamlit UI. Evaluate on a held-out set: does the predicted range
  contain the actual rent?
- **Data:** DLD rent contracts (Ejari) and transactions. A manual export is possible but needs a
  captcha (see the setup checklist), or use data they provide. Plus a handful of example listings
  typed in by hand.
- **Proved wrong if:** the held-out range coverage is poor (say under 70% of actual rents fall inside
  the band), or most listings land at "fair" so the verdict tells nobody anything.

**2. Scout for renters: natural-language search into structured filters**
- **Problem:** Scout leans to off-plan. Renters' needs ("2-bed near Dubai Internet City, school
  nearby, pets, under 150K, 4 cheques") don't map onto the filter panel.
- **Metric:** search → listing-view click-through; fewer zero-result or refined searches.
- **3-h prototype:** an LLM turns a free-text query into the site's filter schema (cheques,
  furnishing, amenities, budget, community), asks one clarifying question if needed, and runs it
  against a small fixture of listings. Evaluate parsing accuracy on 30 hand-labelled queries.
- **Data:** a synthetic or hand-built listing fixture (about 200 rows). No scraping (robots.txt blocks
  search URLs). The filter vocabulary comes from this teardown.
- **Proved wrong if:** parsing accuracy is under about 85%, or users mostly ask for things the
  inventory data can't answer (commute, school quality).

**3. True cost to move in, and Rent in 12 vs cheques**
- **Problem:** The upfront modal leaves out the first rent cheque, and it doesn't compare 1, 4 or 12
  payments against Rent in 12 (about +11.8% here).
- **Metric:** Rent in 12 uptake, or lead rate on eligible listings.
- **3-h prototype:** a pure calculator plus an LLM explanation. Low risk, but thin on AI and on data.
- **Proved wrong if:** renters already understand these costs (check whether "hidden cost" complaints
  show up in reviews).

**4. Listing trust score**
- **Problem:** The most common complaint in app reviews is fake or bait listings and duplicates. That
  hurts trust and wastes paying agents' leads.
- **Metric:** reports per 1,000 listing views; leads that go nowhere.
- **3-h prototype:** rules plus an LLM over a fixture. Flag prices far below the building's DLD
  range, near-duplicate descriptions, and mismatches between the brand and the licensed agency.
- **Data:** needs real listing data, which isn't public. A synthetic fixture weakens the demo.
- **Proved wrong if:** flagged listings get no more reports than unflagged ones.

**5. Rent vs buy, seeded from the listing**: pass the listing's rent and the building's DLD sale
prices into the calculator. Mostly front-end wiring, so less AI. Metric: mortgage-lead conversion
from the listing page.

**6. Lead brief for agents**: before WhatsApp opens, ask the seeker 3 questions (move date, cheques,
budget) and send the agent a structured brief. This helps the paying side. Measure agent response
time and lead-to-viewing rate. Hard to show without agents.

**7. Market summary that says what to do**: turn the Transactions tiles into advice for one segment
("1-bed JVC rents up X%, renew now rather than move"). Hard to measure in 3 hours.

**Best fit, pending the brief:** #1 (uses DLD data in a place it already appears, tied to the lead
metric that pays the bills, and the evaluation is clear). Then #2, if the brief is about Scout or
search. #4 if the brief is about quality or trust.
