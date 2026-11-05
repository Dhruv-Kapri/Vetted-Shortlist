# Audit: 55 live listings in Princess Tower, Dubai Marina

**Building:** Princess Tower, Dubai Marina, a single 101-storey residential tower with many
identical layouts. That makes it a fair test: same building, same layout, so price differences and
duplicates are easy to see. **Read on 5 Nov 2026** from public propertyfinder.ae pages, logged out,
read-only.

**Two depths of checking, so the numbers aren't confused:**

| Set | Listings | What was checked |
|---|---|---|
| **By hand** (the table at the end) | 55: every 2-bed in the 1,181-1,189 sqft layout, 32 rent + 23 sale | Everything below, plus every photo looked at by eye and duplicates confirmed. The prototype shows these |
| **Whole building** | 217: all Princess Tower listings, every bedroom count, 119 rent + 98 sale | The automatic checks only: price against registered deals, "available" date, badge, permit link |
| **By hand, six neighbourhoods** | 60: 10 per area, half random and half most suspicious | Photos by eye and permit cards (see "By-hand checks across neighbourhoods") |

**Audit set (the table below):** every 2-bed listing in the building's commonest layout
(1,181-1,189 sqft): **32 for rent and 23 for sale**. For each one we checked what a person
searching can see:

- **Is the price believable?** We compared it with the median of the **registered** deals for the
  same size (±10 sqft) that the listing pages themselves show. Rentals use the last 6 months, sales
  the last 12. Comparing with other ads would compare asking prices with asking prices.
- **Is it likely still available?** The agent's own "available from" date on the listing page.
- **Is the same flat listed more than once?** A photo hash across all 217 listings in the building,
  then **every audited listing's first three photos looked at by hand** on contact sheets.
- **Do the photos match the building?** By eye, from the views (Palm, Marina, JBR from a high floor)
  and the tower's standard fit-out.
- **Anything else:** the permit link, the Verified badge, the listed date, and photos that show
  nothing of the unit.

## What we found

| Check | Rent (32) | Sale (23) |
|---|---|---|
| Priced like bait (under 75% of registered deals) | **0** | **0** |
| 75-90% of registered deals | 0 | 1 (−11%, AED 1.825M) |
| Over 125% of registered deals | 3 | 4 |
| "Available from" more than 45 days ago | **13** (oldest 489 days) | n/a |
| Same flat in more than one listing, confirmed by eye | **3 flats in 11 listings**, across rent and sale (below) | |
| Verified badge | 53 of 55 | |
| DLD permit link shown | 55 of 55 | |
| First three photos show nothing of the unit (views or pool only) | 2 | 1 |
| Photos look computer-staged | 0 | 1 |

The benchmark for rent is 24 registered contracts in 6 months, with a median of **AED 118,500** and
a middle half of 103K-140K. For sale, only **4** registered sales in 12 months (median AED 2.05M),
so buy-side price judgements are weak and the assistant says so.

**So, are any of them fake?** None is *proven* fake from what a searcher can see. Proving that a
unit is gone, or that the price is not real, takes asking the agent, which is what the assistant is
for. But **23 of the 55 (19 of 32 rentals) show at least one sign of being misleading**:

- 13 say "available" long ago (R3).
- 6 are the same flat posted again (R2).
- 6 have photos that may not show the flat (R5): views or pool only, photos reused across unit
  sizes, or rooms that look computer-staged on an ad that says "Furnished". No listing in the
  building discloses staging.
- 1 sale is 11% under registered deals (R1).

What we did **not** find is the classic bait ad, a price far under the market.

**Three flats, eleven listings (confirmed by eye).**

- **Flat A:** the same balcony furniture, living room and kitchen in **5 listings**. It's for rent at
  **AED 135K (Luxfolio), 140K (Metropolitan) and 150K (EVA)**, and for sale at **AED 2.2M (EVA)
  and 2.25M (Metropolitan)**. That's one flat, three agencies, three rents. Someone calling the
  150K ad would pay 15K a year more for the same flat.
- **Is Flat A fraud? We checked the permits.** Each of the five ads links to its own DLD permit
  card, and all five are valid. Each matches its ad exactly: Rent at AED 135,000 (Luxfolio), 140,000
  (Metropolitan) and 150,000 (EVA), and Sell at AED 2.2M (EVA) and 2.25M (Metropolitan). All five
  give the same 110.15 sqm. So **the DLD issued three rent permits at three prices for one flat**.
  No ad breaks its permit. The likeliest story is non-exclusive mandates from the owner at
  different times or prices, which is legal. It is still misleading in practice: which number you
  pay depends on which agent you happen to call, and nothing on the portal or on the permit card,
  which has no unit number, tells you. Details: `research/permits-flat-a.json` (we deliberately
  didn't record broker names or contacts).
- **Flat B:** the same sofa, table and layout. For rent at AED 120K by White & Co and by fam
  Properties, whose ad says "available" since **489 days ago**. Also for sale at AED 2.2M by fam.
- **Flat C:** the same dining room and painting. For rent at AED 120K by Allsopp & Allsopp and by
  Royal Place, and for sale at AED 2.2M by Allsopp.
- A fourth flat (listings 165601648 / 158686028) is advertised by one agency to rent and to sell
  at the same time.

**How well the photo hash did.** It found only part of Flat A (2 of its 3 rent listings) and missed
Flats B and C, because the crops and watermarks differ. It also matched two balcony photos
(16024503 / 142855746) that may be two different flats: every balcony on that side of the tower
looks the same. So photo matching is a weak stand-in for a unit ID. That's why "unit identity" is
#2 on the can't-build list.

**Other patterns:** one Royal Place agent puts the same building-view photos on 7 listings: 1-, 2-
and 3-bed, from 862 to 2,006 sqft. The cheapest 1-beds in the building (AED 70K) are among them.
In 3 audited listings the first three photos are views or the pool, with nothing of the unit. One
sale listing looks virtually staged.

## The whole building (217 listings, same checks without the eye check)

To test whether "no bait prices" holds beyond one layout, we ran the price and availability checks
on every Princess Tower listing:

| Offering | Bedrooms | Listings | Judged (>=3 deals) | Under 75% | 75-90% | Over 125% | 'Available' >45 d ago | Verified |
|---|---|---|---|---|---|---|---|---|
| rent | 1 | 36 | 36 | 0 | 3 | 6 | 10 | 32 |
| rent | 2 | 51 | 51 | 0 | 0 | 7 | 23 | 48 |
| rent | 3 | 29 | 28 | 0 | 1 | 8 | 11 | 26 |
| rent | 4 | 3 | 0 | 0 | 0 | 0 | 3 | 3 |
| sale | 1 | 24 | 20 | 0 | 0 | 1 | - | 24 |
| sale | 2 | 50 | 38 | 0 | 1 | 6 | - | 48 |
| sale | 3 | 20 | 20 | 0 | 0 | 7 | - | 17 |
| sale | 5 | 4 | 0 | 0 | 0 | 0 | - | 4 |

Under 90% of median:
- rent 159156304 1BR 923 sqft AED 70,000 = 89% of median 79,000 (n=8)
- rent 158717420 1BR 923 sqft AED 70,000 = 89% of median 79,000 (n=8)
- rent 149564147 1BR 923 sqft AED 69,899 = 88% of median 79,000 (n=8)
- rent 114610923 3BR 2403 sqft AED 159,997 = 86% of median 187,000 (n=3)
- sale 152354392 2BR 1186 sqft AED 1,825,000 = 89% of median 2,050,000 (n=4)

**0 of 217 listings are under 75% of registered deals**, and only 5 are between 75% and 90%. But
**47 of 119 rentals (39%) give an "available from" date more than 45 days old.** In this building
the problem isn't bait prices. It's ads for flats that are probably gone, and the same flat posted
by several agencies at different prices.

## Second building

Binghatti Heights, JVC: a cheaper, busier tower, mostly 1-beds at AED 58-87K a year. We ran the
same automatic checks on all 267 listings (no eye check), to see whether bait shows up where rents
are lower:

| Offering | Bedrooms | Listings | Judged (>=3 deals) | Under 75% | 75-90% | Over 125% | 'Available' >45 d ago | Verified |
|---|---|---|---|---|---|---|---|---|
| rent | 1 | 124 | 120 | 0 | 7 | 2 | 47 | 114 |
| rent | 2 | 59 | 54 | 0 | 0 | 2 | 26 | 55 |
| rent | 3 | 35 | 15 | 0 | 0 | 3 | 6 | 32 |
| sale | 1 | 32 | 22 | 0 | 0 | 2 | - | 32 |
| sale | 2 | 7 | 0 | 0 | 0 | 0 | - | 7 |
| sale | 3 | 10 | 0 | 0 | 0 | 0 | - | 10 |

**Again, 0 listings are under 75% of registered deals.** Only 7 one-bed rentals sit at 86-89%. And
**79 of 218 rentals (36%) say "available" more than 45 days ago**, close to Princess Tower's 39%.
The pattern holds across a premium and a mid-market building. For the first photo only, 49 listings
share it with at least one other listing (22 groups). Many are probably the building's exterior shot,
so we don't count them as duplicates without an eye check.

## What counts as a bait price, and does the threshold matter?

**The rule (R1):** compare the listing with the median of *registered* contracts for the same size
(±10 sqft) shown on its own page: rentals over the last 6 months, sales over 12, with at least 3
deals. **Under 75% is likely bait** and gets hidden. **75-90%** is plausible, so the assistant asks
for the full price first. With fewer than 3 deals, the assistant asks instead of judging. We chose
75% because genuine 2-bed contracts in Princess Tower sit between 87% and 118% of the median (the
middle half).

To check that "no bait" isn't just a result of choosing 75%, here are the counts at looser
thresholds. Every rental is judged against its own page's deals:

| Rentals judged | n | under 75% | under 80% | under 85% | under 90% | cheapest vs deals |
|---|---|---|---|---|---|---|
| Palm Jumeirah | 28 | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) | -10% |
| Downtown Dubai | 43 | 0 (0%) | 1 (2%) | 2 (5%) | 6 (14%) | -24% |
| Dubai Marina | 53 | 0 (0%) | 1 (2%) | 3 (6%) | 7 (13%) | -21% |
| JVC | 29 | 0 (0%) | 0 (0%) | 0 (0%) | 2 (7%) | -13% |
| Discovery Gardens | 23 | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) | -4% |
| International City | 38 | 0 (0%) | 0 (0%) | 0 (0%) | 1 (3%) | -13% |
| Princess Tower (whole building) | 94 | 0 (0%) | 0 (0%) | 0 (0%) | 2 (2%) | -14% |
| Binghatti Heights (whole building) | 105 | 0 (0%) | 0 (0%) | 2 (2%) | 4 (4%) | -17% |

Even at 90%, the share stays at 14% or less in every area. The cheapest listing anywhere is 24%
under its registered deals, in Downtown. At 75%, the count is zero everywhere.

## Six neighbourhoods, from luxury to budget

Does the pattern depend on how expensive the area is? For each of six neighbourhoods we took the
first 3 pages of apartment rentals (72-81 listings each, about 450 in all) and their detail pages.
We judged each listing against **its own page's** registered rents: same building, same size, last
6 months, at least 3 deals. Script: `scripts/compare_areas.py`.

| Area | listings | median AED/sqft/yr | judged (>=3 deals) | under 75% (bait) | 75-90% | over 125% | median asking vs deals | 'available' >45 d ago | Verified | permit link | listings per agency | buildings in sample |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Palm Jumeirah (luxury) | 78 | 155 | 28 | 0% | 0% | 21% | +10% | 18% | 99% | 100% | 1.6 | 46 |
| Downtown Dubai (luxury) | 72 | 149 | 43 | 0% | 14% | 16% | +6% | 29% | 99% | 100% | 1.7 | 45 |
| Dubai Marina (upper-mid) | 81 | 117 | 53 | 0% | 13% | 8% | +5% | 22% | 96% | 99% | 2.2 | 44 |
| JVC (mid) | 80 | 101 | 29 | 0% | 7% | 10% | +0% | 11% | 84% | 100% | 2.6 | 60 |
| Discovery Gardens (budget) | 77 | 80 | 23 | 0% | 0% | 0% | +5% | 21% | 95% | 100% | 1.8 | 47 |
| International City (budget) | 76 | 66 | 38 | 0% | 3% | 13% | +6% | 25% | 83% | 99% | 2.5 | 53 |

**Area by area:**

- **Palm Jumeirah (luxury, AED 155/sqft/yr):** no bait, and nothing even at 75-90%. **21% ask over
  125% of registered deals**, the highest of any area. 18% stale. 99% Verified. 1.6 listings per
  agency.
- **Downtown Dubai (luxury, AED 149):** no bait, but the most "cheap" listings (14% at 75-90%) and
  the **most stale (29%)**. 16% over 125%. 99% Verified.
- **Dubai Marina (upper-mid, AED 117):** no bait. 13% at 75-90%, 8% over 125%, 22% stale, 96%
  Verified. 2.2 listings per agency.
- **JVC (mid, AED 101):** no bait. 7% at 75-90%, 10% over 125%, the least stale (11%), and **84%
  Verified**. The most listings per agency (2.6).
- **Discovery Gardens (budget, AED 80):** no bait, and nothing even at 75-90%. 0% over 125%, 21%
  stale, 95% Verified.
- **International City (budget, AED 66):** no bait. 3% at 75-90%, 13% over 125%, 25% stale, the
  **fewest Verified (83%)**, and 2.5 listings per agency.

**Across them:**

- **Bait pricing is absent in every tier.** In every area, 0% of the judged listings are under 75%
  of registered deals.
- **The tiers have different problems.**
  - **Luxury** asks far above recent deals: 21% of the Palm's judged listings are over 125%. The
    risk there is overpaying, not bait.
  - **Mid and budget** areas have fewer Verified ads (83-84% in JVC and International City, against
    99% on the Palm and in Downtown) and more listings per agency (2.5-2.6 against 1.6-1.7).
- **Stale "available" dates show up everywhere** (11-29% of these samples). They're lower here than
  in the full-building pulls (36-39%) because the first result pages favour fresh listings. The
  stale ads sit deeper in the results, where a tired searcher scrolls after weeks of looking.
- **Limits:** these are the first pages only, rentals only, and no eye check. Coverage of registered
  deals varies (23-53 judged per area), so the percentages are rough.


## The 55 listings

"vs registered median" compares the listing with registered deals for the same size (n = number of
deals). "Same photos" is the automatic hash match across the building's 217 listings. "Photos (by
eye)" is our own look at the first three photos. "Assistant" is the verdict the prototype shows,
with the reason.

| # | Listing | Price (AED) | sqft | Furn. | Cheques | Listed | Available from | vs registered median | Same photos on other listings | Photos (by eye) | Assistant |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [rent 161902017](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-161902017.html) | 109,777 | 1183 | N | - | 2026-10-20 | 2026-06-11 (147 d ago) | -7% (n=24) | none found | First three photos are aerial views only; nothing of the unit | **check** — Said 'available' 147 days ago |
| 2 | [rent 158224698](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-158224698.html) | 109,888 | 1189 | Y | 1 | 2026-10-12 | 2026-10-15 (21 d ago) | -7% (n=24) | none found | First photos are the building pool, not the unit | **shortlist**  |
| 3 | [rent 158717394](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-158717394.html) | 109,970 | 1189 | Y | 1 | 2026-10-13 | 2026-10-15 (21 d ago) | -7% (n=24) | none found | Royal Place: same reused view photos as its other listings; one bedroom shot | **shortlist**  |
| 4 | [rent 168361070](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-168361070.html) | 110,000 | 1189 | Y | 4 | 2026-11-03 | 2026-09-16 (50 d ago) | -7% (n=24) | none found | View of Marina towers from a mid floor; consistent with the tower | **check** — Said 'available' 50 days ago |
| 5 | [rent 167870490](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-167870490.html) | 110,000 | 1181 | N | 3 | 2026-11-02 | 2026-11-02 (3 d ago) | -7% (n=24) | none found | Balcony view; consistent | **shortlist**  |
| 6 | [rent 169274661](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-169274661.html) | 110,000 | 1184 | N | 1 | 2026-11-05 | 2026-11-05 (0 d ago) | -7% (n=24) | 158717420 (Royal Place Real E, AED 70,000, 1BR 923 sqft); 159156304 (Royal Place Real E, AED 70,000, 1BR 923 sqft); 159662647 (Royal Place Real E, AED 105,000, 2BR 1298 sqft); 169274610 (Royal Place Real E, AED 159,999, 3BR 2006 sqft); 169274924 (Royal Place Real E, AED 69,990, 1BR 862 sqft) | Royal Place: first photos are building-level Palm/Marina views reused on this agent's 1-, 2- and 3-bed listings; no proof of this unit | **shortlist**  |
| 7 | [rent 168792326](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-168792326.html) | 110,000 | 1189 | Y | 2 | 2026-11-04 | 2026-10-27 (9 d ago) | -7% (n=24) | none found | Interiors and balcony; consistent | **shortlist**  |
| 8 | [rent 164607175](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-164607175.html) | 115,000 | 1185 | P | - | 2026-10-26 | 2026-10-24 (12 d ago) | -3% (n=24) | none found | Empty interiors; can't place | **shortlist**  |
| 9 | [rent 165601648](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-165601648.html) | 118,999 | 1189 | Y | 4 | 2026-10-28 | 2026-06-23 (135 d ago) | +0% (n=24) | none found | Interiors; the same photos are on a sale listing (158686028, same agency), so the flat is advertised to rent and to sell at once | **check** — Said 'available' 135 days ago |
| 10 | [rent 146422045](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-146422045.html) | 120,000 | 1185 | Y | 1 | 2026-09-18 | 2026-11-02 (3 d ago) | +1% (n=24) | none found | Interiors only; can't place the building from photos | **shortlist**  |
| 11 | [rent 16024503](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-16024503.html) | 120,000 | 1181 | N | 3 | 2026-01-09 | 2026-10-01 (35 d ago) | +1% (n=24) | 142855746 (White & Co Real Es, AED 120,000, same size) | High-floor Palm/Marina balcony view; consistent. Balcony looks like 142855746 but from a different angle, so we can't tell if it's the same flat | **hidden** — Duplicate of another listing |
| 12 | [rent 168366670](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-168366670.html) | 120,000 | 1182 | Y | 1 | 2026-11-03 | 2026-10-08 (28 d ago) | +1% (n=24) | none found | High-floor Palm view; consistent | **shortlist**  |
| 13 | [rent 142855746](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-142855746.html) | 120,000 | 1181 | N | 1 | 2026-09-10 | 2026-09-10 (56 d ago) | +1% (n=24) | 16024503 (haus & haus, AED 120,000, same size) | High-floor view; see 16024503 | **check** — Said 'available' 56 days ago |
| 14 | [rent 162788781](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-162788781.html) | 120,000 | 1189 | Y | 1 | 2026-10-22 | 2026-06-25 (133 d ago) | +1% (n=24) | none found | Flat B (by eye: same grey sofa, table, layout): rent 162788781 White & Co 120K, 162770873 fam 120K ('available' 489 d ago); sale 98681358 fam 2.2M | **check** — Said 'available' 133 days ago |
| 15 | [rent 162770873](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-162770873.html) | 120,000 | 1188 | Y | 1 | 2026-10-22 | 2025-07-04 (489 d ago) | +1% (n=24) | none found | Flat B (by eye: same grey sofa, table, layout): rent 162788781 White & Co 120K, 162770873 fam 120K ('available' 489 d ago); sale 98681358 fam 2.2M | **hidden** — Said 'available' 489 days ago, Duplicate of another listing |
| 16 | [rent 166541246](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-166541246.html) | 120,000 | 1183 | N | 2 | 2026-10-30 | 2026-06-01 (157 d ago) | +1% (n=24) | none found | Dusk view over Marina; consistent | **check** — Said 'available' 157 days ago |
| 17 | [rent 161881119](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-161881119.html) | 120,000 | 1181 | N | 2 | 2026-10-20 | 2026-10-20 (16 d ago) | +1% (n=24) | none found | Empty interiors; can't place | **shortlist**  |
| 18 | [rent 131574377](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-131574377.html) | 120,000 | 1189 | Y | 1 | 2026-08-17 | 2026-10-21 (15 d ago) | +1% (n=24) | none found | Flat C (by eye: same dining room and orange painting): rent 131574377 Allsopp 120K, 167007072 Royal Place 120K; sale 158698070 Allsopp 2.2M | **hidden** — Duplicate of another listing |
| 19 | [rent 154609767](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-154609767.html) | 120,000 | 1188 | Y | 4 | 2026-10-05 | 2026-06-01 (157 d ago) | +1% (n=24) | none found | Construction-view shot and bedroom; consistent with the tower | **check** — Said 'available' 157 days ago |
| 20 | [rent 167007072](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-167007072.html) | 120,000 | 1189 | N | 2 | 2026-10-31 | 2026-10-31 (5 d ago) | +1% (n=24) | none found | Flat C (by eye: same dining room and orange painting): rent 131574377 Allsopp 120K, 167007072 Royal Place 120K; sale 158698070 Allsopp 2.2M | **shortlist**  |
| 21 | [rent 156916361](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-156916361.html) | 124,888 | 1183 | Y | - | 2026-10-09 | 2026-10-09 (27 d ago) | +5% (n=24) | none found | Interiors; can't place | **shortlist**  |
| 22 | [rent 168809700](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-168809700.html) | 124,999 | 1181 | N | 1 | 2026-11-04 | 2026-11-04 (1 d ago) | +5% (n=24) | none found | Palm/Marina views; consistent | **shortlist**  |
| 23 | [rent 168328487](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-168328487.html) | 125,000 | 1185 | Y | 2 | 2026-11-03 | 2026-11-03 (2 d ago) | +5% (n=24) | none found | Balcony view of Marina towers; consistent | **shortlist**  |
| 24 | [rent 168365745](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-168365745.html) | 125,000 | 1186 | Y | 2 | 2026-11-03 | 2026-09-15 (51 d ago) | +5% (n=24) | none found | Interiors; can't place | **check** — Said 'available' 51 days ago |
| 25 | [rent 161854932](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-161854932.html) | 129,900 | 1185 | Y | 1 | 2026-10-20 | 2026-10-17 (19 d ago) | +10% (n=24) | none found | Interiors; can't place | **shortlist**  |
| 26 | [rent 165044257](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-165044257.html) | 130,000 | 1181 | N | - | 2026-10-27 | 2026-10-28 (8 d ago) | +10% (n=24) | none found | High-floor Palm view; consistent | **shortlist**  |
| 27 | [rent 141465422](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-141465422.html) | 130,000 | 1181 | N | 4 | 2026-09-07 | 2026-09-07 (59 d ago) | +10% (n=24) | none found | Palm view and empty rooms; consistent | **check** — Said 'available' 59 days ago |
| 28 | [rent 146425500](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-146425500.html) | 135,000 | 1186 | Y | 4 | 2026-09-18 | 2026-08-11 (86 d ago) | +14% (n=24) | 147762008 (EVA Real Estate LL, AED 150,000, same size) | Flat A (by eye: same balcony furniture, living room, kitchen): rent 146425500 Luxfolio 135K, 163694214 Metropolitan 140K, 147762008 EVA 150K; sale 147781701 EVA 2.2M, 144602929 Metropolitan 2.25M | **check** — Said 'available' 86 days ago |
| 29 | [rent 163694214](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-163694214.html) | 140,000 | 1186 | Y | 4 | 2026-10-24 | 2026-09-15 (51 d ago) | +18% (n=24) | none found | Flat A (by eye: same balcony furniture, living room, kitchen): rent 146425500 Luxfolio 135K, 163694214 Metropolitan 140K, 147762008 EVA 150K; sale 147781701 EVA 2.2M, 144602929 Metropolitan 2.25M | **hidden** — Said 'available' 51 days ago, Duplicate of another listing |
| 30 | [rent 147762008](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-147762008.html) | 150,000 | 1186 | Y | 2 | 2026-09-21 | 2026-09-21 (45 d ago) | +27% (n=24) | 146425500 (Luxfolio Real Esta, AED 135,000, same size) | Flat A (by eye: same balcony furniture, living room, kitchen): rent 146425500 Luxfolio 135K, 163694214 Metropolitan 140K, 147762008 EVA 150K; sale 147781701 EVA 2.2M, 144602929 Metropolitan 2.25M | **hidden** — Duplicate of another listing |
| 31 | [rent 138777963](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-138777963.html) | 156,000 | 1181 | Y | - | 2026-09-01 | 2026-10-16 (20 d ago) | +32% (n=24) | none found | High-floor Palm view; consistent | **shortlist**  |
| 32 | [rent 104675044](https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-princess-tower-104675044.html) | 180,000 | 1181 | Y | 4 | 2026-06-19 | 2026-06-19 (139 d ago) | +52% (n=24) | none found | Views and a bedroom; consistent | **check** — Said 'available' 139 days ago |
| 33 | [sale 152354392](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-152354392.html) | 1,825,000 | 1186 | P | - | 2026-09-30 | - | -11% (n=4) | none found | Renovated modern kitchen, different from the tower's standard fit-out; plausible upgrade | **check** — Price 11% under recent deals |
| 34 | [sale 149100966](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-149100966.html) | 1,990,000 | 1188 | N | - | 2026-09-23 | - | -3% (n=4) | none found | Interiors; can't place | **shortlist**  |
| 35 | [sale 164562185](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-164562185.html) | 2,000,000 | 1188 | Y | - | 2026-10-26 | - | -2% (n=4) | none found | Interiors and balcony view; consistent | **shortlist**  |
| 36 | [sale 167431760](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-167431760.html) | 2,000,000 | 1189 | Y | - | 2026-11-01 | - | -2% (n=4) | none found | Views only in the first three photos | **shortlist**  |
| 37 | [sale 158249720](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-158249720.html) | 2,000,000 | 1189 | Y | - | 2026-10-12 | - | -2% (n=4) | none found | Night views and interiors; consistent | **shortlist**  |
| 38 | [sale 150009971](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-150009971.html) | 2,000,000 | 1189 | Y | - | 2026-09-25 | - | -2% (n=4) | none found | Interiors and balcony; consistent | **shortlist**  |
| 39 | [sale 135143057](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-135143057.html) | 2,080,000 | 1189 | Y | - | 2026-08-24 | - | +1% (n=4) | none found | Looks virtually staged (computer-generated furniture): the photos don't show the real unit | **shortlist**  |
| 40 | [sale 158686028](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-158686028.html) | 2,200,000 | 1189 | Y | - | 2026-10-13 | - | +7% (n=4) | none found | Interiors; the same photos are on rent listing 165601648 (same agency): one flat advertised to rent and to sell | **shortlist**  |
| 41 | [sale 158698070](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-158698070.html) | 2,200,000 | 1188 | Y | - | 2026-10-13 | - | +7% (n=4) | none found | Flat C (by eye: same dining room and orange painting): rent 131574377 Allsopp 120K, 167007072 Royal Place 120K; sale 158698070 Allsopp 2.2M | **shortlist**  |
| 42 | [sale 98681358](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-98681358.html) | 2,200,000 | 1188 | Y | - | 2026-06-05 | - | +7% (n=4) | none found | Flat B (by eye: same grey sofa, table, layout): rent 162788781 White & Co 120K, 162770873 fam 120K ('available' 489 d ago); sale 98681358 fam 2.2M | **shortlist**  |
| 43 | [sale 147781701](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-147781701.html) | 2,200,000 | 1186 | Y | - | 2026-09-21 | - | +7% (n=4) | none found | Flat A (by eye: same balcony furniture, living room, kitchen): rent 146425500 Luxfolio 135K, 163694214 Metropolitan 140K, 147762008 EVA 150K; sale 147781701 EVA 2.2M, 144602929 Metropolitan 2.25M | **shortlist**  |
| 44 | [sale 144602929](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-144602929.html) | 2,250,000 | 1186 | Y | - | 2026-09-14 | - | +10% (n=4) | none found | Flat A (by eye: same balcony furniture, living room, kitchen): rent 146425500 Luxfolio 135K, 163694214 Metropolitan 140K, 147762008 EVA 150K; sale 147781701 EVA 2.2M, 144602929 Metropolitan 2.25M | **hidden** — Duplicate of another listing |
| 45 | [sale 162781538](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-162781538.html) | 2,250,000 | 1186 | Y | - | 2026-10-22 | - | +10% (n=4) | none found | Balcony with chairs and the same view as Flat A; possibly Flat A again (not confirmed) | **shortlist**  |
| 46 | [sale 121118406](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-121118406.html) | 2,350,000 | 1183 | Y | - | 2026-07-25 | - | +15% (n=4) | none found | Views and interiors; consistent | **shortlist**  |
| 47 | [sale 158244486](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-158244486.html) | 2,450,000 | 1185 | N | - | 2026-10-12 | - | +20% (n=4) | none found | View and kitchen; consistent | **shortlist**  |
| 48 | [sale 156936676](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-156936676.html) | 2,450,000 | 1185 | N | - | 2026-10-09 | - | +20% (n=4) | none found | Palm view, empty rooms; consistent | **shortlist**  |
| 49 | [sale 169247428](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-169247428.html) | 2,549,000 | 1183 | N | - | 2026-11-05 | - | +24% (n=4) | none found | Renovated interiors (Luxfolio); consistent | **shortlist**  |
| 50 | [sale 162770382](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-162770382.html) | 2,549,000 | 1183 | Y | - | 2026-10-22 | - | +24% (n=4) | none found | Palm view and interiors; consistent | **shortlist**  |
| 51 | [sale 75411271](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-75411271.html) | 2,549,000 | 1183 | Y | - | 2026-04-11 | - | +24% (n=4) | none found | High-floor view, renovated interiors; listed in April (7 months) | **shortlist**  |
| 52 | [sale 158703922](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-158703922.html) | 2,700,000 | 1181 | N | - | 2026-10-13 | - | +32% (n=4) | none found | Palm view and interiors; consistent | **shortlist**  |
| 53 | [sale 165571403](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-165571403.html) | 2,700,000 | 1181 | N | - | 2026-10-28 | - | +32% (n=4) | none found | High-floor Palm view and empty rooms; consistent | **shortlist**  |
| 54 | [sale 155062404](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-155062404.html) | 2,850,000 | 1181 | Y | - | 2026-10-06 | - | +39% (n=4) | none found | Interiors; can't place | **shortlist**  |
| 55 | [sale 136072118](https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-princess-tower-136072118.html) | 2,895,000 | 1181 | Y | - | 2026-08-26 | - | +41% (n=4) | none found | Views and interiors; consistent | **shortlist**  |
