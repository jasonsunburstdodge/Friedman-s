---
name: friedmans-ppc-research
description: Research inputs for Friedman's PPC planning - 3-year seasonal best sellers by store, outside forces (weather, El Nino, fire and smoke, stock), demographics, psychographics, buying triggers and where to spend.
---

# Friedman's PPC research (functions 1 to 4)

Use this skill at the start of every planning cycle ("Plan the season"), at least monthly, and whenever an outside force changes (a new storm outlook, a fire, a stock problem). It produces the research pack that `friedmans-ppc-campaigns` turns into campaign proposals. Load `friedmans-brand-guidelines` first.

Every number in the pack carries three tags: **source** (system, URL or document), **as of** (date and time), and **status** (VERIFIED, ASSUMPTION or SIMULATED). Never present an assumption or simulated number as fact. If a source is unavailable, say which one and what you used instead.

## Stores and trade areas

Santa Rosa (4055 Santa Rosa Ave), Petaluma (429 N McDowell Blvd), Sonoma (1360 Broadway), Ukiah (1255 Airport Park Blvd). Always analyze all four, in that order. Default trade area: a 15-mile drive radius per store, replaced by the real customer-ZIP map once POS ZIP data is available. Where trade areas overlap, assign each ZIP to the store most of its customers use.

## Start from learnings

Before anything else, load `learnings.jsonl` and `season-lessons.md` using the matching rules in `friedmans-ppc-learnings`. Pick records for the same season window, then records with similar conditions (ENSO state, rain, smoke, promotions, stock). Use them this way:
- **Starting numbers**: for a channel and campaign type with a Success or Mixed record, start projections from its actual CPC, conversion rate and basket, not industry benchmarks. Show both, and cite the record ID.
- **Lessons**: apply each lesson that matches this season's conditions, and say which ones you applied.
- **Adjustments that worked**: build them in from day one (for example, rain-day caps or category landing pages for video).
- **Fails**: don't repeat a failed line unless conditions changed; say what changed.
If there are no matching records, say so and use benchmarks.

## Function 1: Seasonal best sellers

1. Define the season window: the next 4 to 8 weeks, plus the same weeks in each of the last 3 years.
2. Pull item sales by store by week for those windows (units, revenue, gross margin, returns). Normalize for store openings, closures and stock-outs: a week an item was out of stock understates demand, so mark it and use the in-stock weeks.
3. Rank items per store by gross margin dollars in the window, not just units. Report units and revenue too.
4. Find **project bundles**: items bought together in the same basket (co-purchase or attach rate) during the window. A bundle becomes a campaign theme ("gutter and drainage", "winterize outdoor plumbing").
5. Flag **year-over-year movers**: items up or down more than 25% in the window across the 3 years, and say what explains it (a wet year, a fire year, a promotion, a new product).
6. Compare stores. Name the items that sell much better in one store's season (for example earlier frost items in Ukiah).
7. **Forecast this season** per item per store. Never use the mode (unit sales rarely repeat) or a plain mean as the forecast.
   - **Clean first.** Fill stock-out weeks with the in-stock weekly rate and remove one-off promotion lifts.
   - **Baseline: weighted mean** of the cleaned years, 50% most recent, 30% the year before, 20% the oldest.
   - **Outlier year:** if one year is more than 25% away from the median of the three, use the median as the baseline instead.
   - **Analog year, only with evidence:** when this season's conditions match a past year (an El Niño winter, a fire year), forecast = the item's recent baseline (60% last year, 40% the year before) x the analog year's lift, measured across the item's whole category at all four stores. Use it only if (a) the measured lift differs from 1.0 by more than 10%, and (b) the driver data (search interest, rain, frost, AQI for that window) shows the condition actually moved demand. A climate label alone is not evidence. In the Oct 2026 review, the 2023 El Niño analog failed this test: Santa Rosa's 2023-24 El Niño season was drier than 2022-23, and Bay Area tarp searches didn't rise that Oct to Nov.
   - **Weather is a driver, not a forecast.** For weather-sensitive items (storm, frost, smoke), set a normal baseline, then let the NWS forecast trigger bursts. In the backtest, adjusting storm items for actual rain cut the miss from about 27% to under 10%.
   - **Pick one method per item** in that order of precedence: analog (if it passes the evidence test), then median, then weighted mean. Record the method and the reason.
   - **Backtest each cycle:** forecast last year from the two years before it with each method, and report the average miss by category, so the method choice rests on Friedman's own history.
   - **Show the range**: the lowest and highest result across mean, median, weighted mean and analog, so reviewers see the uncertainty.
   - When weekly data within each season exists, forecast from the weekly series rather than three annual totals.
   - Reviewers can override the method per item; record the override and who made it.

Output: top 25 items per store and top bundles, each with units, revenue, margin, return rate, 3-year trend, and status tag.

## Function 2: Outside forces

Check each of these, record the evidence, and state the planning adjustment it causes:

| Force | Where to check | Typical adjustment |
|---|---|---|
| Climate pattern (El Niño, La Niña) | NOAA CPC ENSO discussion (monthly), CPC seasonal outlooks; check against local NOAA station history and Google Trends | Keep storm bundles ready and budget reserved for bursts; adjust volume only if local history shows the pattern moved demand |
| 7 to 14 day weather | NWS forecasts for each store's zone | Time bursts 24 to 72 hours before rain, frost or wind; hold outdoor-work ads during storms |
| Fire, smoke, air quality | CAL FIRE incidents, local news, AirNow AQI | Pause outdoor-work creative where AQI is unhealthy; never advertise into an evacuation zone; offer indoor projects |
| Power shutoffs | Utility PSPS notices | Lead with lighting and outage kits only in a helpful tone |
| Emergencies | Governor and county proclamations | Note the context; never use it as a scare line |
| Stock | Catalog on-hand by store, inbound POs | Exclude low items from hero ads; push overstock |
| Promotions and events | Weekly Ad, events calendar | Use only approved offers; align bursts |
| Calendar | Holidays, daylight saving, paydays, school breaks | Shift timing and messaging |
| Competition and cost | Auction insights, CPC trends | Adjust bids and channel mix (never name competitors in ads) |

**Live stock.** Read on-hand for every advertised item at all four stores from the Sana catalog (in the demo, the same warehouse data is visible on friedmanshome.com). Compare day over day for a sell-through signal before POS data is connected.

**Stock rules for ads.** Expected weekly ad-driven units per store = projected orders per week x units per basket x the store's share of orders. An item can be a hero product in an ad only when on-hand plus confirmed inbound within 7 days, at the target store, is at least the larger of safety stock or 2 times that number. If on-hand falls short, don't stop to ask: calculate how many days on-hand covers, the suggested order and the projected delivery date (open PO or vendor lead time), and flag it to Purchasing for confirmation. If stock runs out before the projected delivery, hold that item out of that store's ads until the day after delivery, or swap an in-stock equivalent. Gate 2 waits for Purchasing to confirm. Overstock is on-hand above 8 weeks of forecast demand, or an amount Friedman's buyers name. Report both lists per store.

## Function 3: Demographics, psychographics and buying triggers

- **Demographics** (Census ACS 5-year, by city and ZIP): population, households, owner-occupied rate, median household income, median home value, persons per household, median age, Hispanic share, broadband share. Owner rate and home value predict project spend; renters buy smaller fixes.
- **Psychographics**: describe likely motivations and values, labeled as inferences, from evidence such as local history (recent wildfires, floods), climate exposure (inland frost, clay soil, atmospheric rivers), lifestyle (gardening, wine country, ranch and rural properties), and first-party survey or loyalty data when available. Never infer traits about individuals.
- **Buying triggers**: events that move a household from "someday" to "this weekend": first rain of the season, a storm warning, first frost, a smoke day, a power outage, moving in, daylight saving ending, holidays, a promotion. For each trigger record the signal the agent can watch, the lead time, the products, and the stores affected.
- **Language**: where a trade area has a large Spanish-speaking share, propose a Spanish-language variant as a separate test with its own budget line.

## Function 4: Where to spend

Score each ZIP or area per store on:
1. **Customer density**: share of the store's past customers (from POS ZIPs).
2. **Reachable first-party audience**: opted-in email, SMS and social followers in the area. Only lists with advertising consent count.
3. **Search demand**: query volume for the season's terms (Google Ads Keyword Planner, Search Console, Google Trends for the region).
4. **Fit**: owner rate, income and home value for the products in the bundle.
5. **Trigger exposure**: how strongly the area is hit by the trigger (inland frost, flood-prone streets, smoke).

Allocate the test budget to channels by job:
- **Google Search and Performance Max with local inventory**: people already looking; first call for any bundle with search demand.
- **Meta**: reach and retargeting in the trade area; first-party custom audiences and lookalikes.
- **Nextdoor**: neighborhood-level reach for preparedness and community messages. No reliable public benchmark exists; treat costs as a test to learn.
- **TikTok**: short how-to video for younger homeowners and renters; reuse the content agent's approved videos.
- **Email and SMS** (owned, no media cost): sequenced with paid bursts, opted-in only.

## Output: the research pack

Save under the cycle ID `PPC-YYYYMMDD`:
- `best-sellers.json` (function 1 tables and bundles)
- `forces.json` (each force, evidence, as-of, adjustment)
- `audience.json` (demographics, psychographic notes labeled as inferences, triggers)
- `geo-channel.json` (area scores and channel allocation)
- `research-review.json`: PASS or REVISE for: every number tagged; no simulated data shown as real; all four stores covered; stock rules applied; triggers tied to watchable signals; sensitivity check on fire, flood and outage messaging.

Fix any REVISE before handing to `friedmans-ppc-campaigns`.
