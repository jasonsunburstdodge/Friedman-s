---
name: friedmans-ppc-segments
description: Find and size targeted buyer segments for Friedman's PPC (contractors, property and building maintenance, landscapers, gardeners, frequent DIYers, new home buyers), flag the ones the data supports, and offer them as optional Gate 1 tests.
---

# Friedman's buyer segments (optional, flagged opportunities)

Use this skill in each planning cycle after `friedmans-ppc-research`, and whenever the approver asks for more targeted campaigns. Segments are **optional**: the agent flags opportunities, and nothing joins a campaign unless the approver adds it at Gate 1. Load `friedmans-brand-guidelines` first.

## Segments to assess every cycle

| Segment | Known or findable | Real public sizing | Friedman's data |
|---|---|---|---|
| Contractors and trades | Known: Pro Advantage, Contractor Services | BLS QCEW establishments and employment, NAICS 236 and 238, Sonoma and Mendocino counties | Pro account count, recency, visit frequency, basket |
| Property managers and building maintenance | Known if they hold accounts; findable via business listings | QCEW NAICS 531311, 531312, 561720, 561790 | Business accounts by type, order size |
| Landscapers and pro gardeners | Known: pro accounts; findable via listings | QCEW NAICS 561730, 111421 | Landscaper accounts, soil and bulk share |
| Home gardeners | Known: Get Growing and garden email subscribers | Google Trends for garden terms in the region | Garden email engagement |
| Frequent DIYers | Known: loyalty and purchase history | None public | Visit frequency, departments per customer |
| New home buyers | Findable: new movers | County home sales (ATTOM or recorder), Census "same house 1 year ago" | First-year mover spend, if a mover list is matched |

Add a segment when the data shows one (for example wineries or ranches for farm and ranch supplies), using the same fields.

## For each segment, record

- **Real data**, with the source and as-of date, kept separate from **Friedman's data** (POS, loyalty, Pro accounts). Mark Friedman's data SIMULATED in demos.
- **Why it's an opportunity**, tied to this season's forces (storms, smoke, fall planting, an event such as Pro Tool Days).
- **Products**: real catalog items with live stock at all four stores. Note any thin stock and check Purchasing before featuring it.
- **Reach**: how to reach the segment within the consent rules. Customer Match or custom audiences only from lists whose consent covers advertising; platform audiences such as "recently moved"; business-interest targeting; Search on segment terms. Never target or exclude by protected traits.
- **Suggested test**: channel, budget cap, duration, landing page, and **what would confirm it** (the metric and threshold that makes it worth scaling).

## Flags

- **EXPLORE**: real sizing shows a meaningful audience, products are in stock, and the segment can be reached within consent rules. Offer it as an optional Gate 1 test.
- **WATCH**: the opportunity depends on Friedman's data that isn't connected yet (for example frequent DIYers without POS visit data). Say what data would unlock it.
- **COVERED**: already reached by a proposed campaign; note any small add (such as a lookalike line) instead of a new test.
- **NOT NOW**: the stock, consent or season doesn't support it; say why.

## Projections

Segments rarely have public benchmarks. Don't invent CPC or conversion rates for them. Run them as capped learning tests with a stated confirm metric, and project only once Friedman's own results exist. If a channel benchmark applies (for example Meta for new movers), show it with its source and label the segment fit as an assumption.

## Gate 1

Optional segment tests appear below the main proposal at Gate 1, each with APPROVE or DECLINE. Approval follows the same Gate 2 launch rules: stock confirmed by Purchasing, caps set, tracking verified, consent confirmed for any customer list.

## Outputs (under the cycle ID)

- `segments.json`: each segment with real data and sources, Friedman's data, flag and reason, products with stock, reach, suggested test, confirm metric.
- A result record in `learnings.jsonl` for each segment test when it ends (see `friedmans-ppc-learnings`). Once a segment has a Success or Mixed record, use its actual numbers as that segment's projection next time.
- `segments-review.json`: PASS or REVISE for: real and simulated data separated; consent rules met; no protected-trait targeting; stock checked; no invented benchmarks.
