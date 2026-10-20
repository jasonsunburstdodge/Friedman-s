---
name: friedmans-ppc-monitoring
description: Hourly monitoring of Friedman's live PPC campaigns (ads, social and purchase analytics), the 8-hour report, funnel diagnosis, protective auto-pauses and the Gate 3 adjustment queue.
---

# Friedman's PPC monitoring and reporting (function 6)

Runs once campaigns pass Gate 2. Load `friedmans-brand-guidelines` for report and ad copy.

## Hourly check (every hour, on the hour, Pacific time)

Pull, per campaign, ad group, ad, store area and hour:
- **Ad platforms**: spend, impressions, clicks, CTR, CPC, CPM, frequency, conversions, conversion value, search terms, disapprovals.
- **Social**: reach, engagement, saves, shares, comments (read sentiment and questions; never reply without approval), video hold rate.
- **Site analytics (GA4)**: sessions by UTM, product views, add to cart, checkout, pickup orders, estimator starts and completions, bounce on landing page.
- **Purchases**: online orders, pickup orders, and in-store sales matched to the bundle by store (POS), returns.
- **Catalog**: on-hand by store for every advertised item.
- **Outside forces**: NWS alerts for each store zone, AQI, fire incidents, PSPS notices.

Compare each metric to the approved projection and to the last 7 days. Log every check. Do not alert on noise: a signal needs at least 100 clicks or 2 hours of data, unless it is a safety, stock or spend-cap event.

## Protective actions the agent may take without approval

Only these, each logged and reported within the hour. Starting a pre-approved standby campaign (such as Clean Air on a smoke day) when its approved trigger fires is not a new decision; it runs within its approved caps and is reported the same way.
1. **Stock-out**: pause the product, ad or local inventory listing for a store where the item falls below the stock rule. Resume automatically when stock returns above it.
2. **Spend guard**: if a campaign will exceed its approved daily cap or total budget, pause it at the cap.
3. **Safety or sensitivity**: pause outdoor-work or preparedness creative in an area under an evacuation order, a red-flag fire event or unhealthy AQI, and any ad that reads as exploiting an emergency.
4. **Broken landing page or tracking**: pause the ad pointing to a page returning errors, or a campaign whose conversion tracking stops recording for 2 hours.
5. **Disapproved ad**: leave it paused and queue a fix for approval.

Resuming after a safety or sensitivity pause, a broken page or a disapproval goes to Gate 3; only stock-out pauses resume on their own. Everything else goes to Gate 3. The agent never raises a budget, bid or cap, never adds a channel, audience or ad, and never resumes something an approver paused.

## The 8-hour report (6 a.m., 2 p.m. and 10 p.m. Pacific)

One page, in this order:
1. **Headline**: one sentence on how the test is going against plan.
2. **Scoreboard** per campaign: spend vs plan, ROAS vs projected range and break-even, profit after ads, conversions, CPC, CTR, and the **chance the line is truly above break-even** (simulate the true conversion rate from clicks and orders so far, starting from the benchmark rate weighted as 100 clicks). Mark ON TRACK (90% or more), WATCH (60% to 89%) or OFF TRACK; any line under 100 clicks or 3 days is TOO EARLY.
3. **What's working**: the top 3 ads, audiences, areas or search terms, with the numbers.
4. **What isn't**: the bottom 3, with the numbers.
5. **What seems effective** and **what seems ineffective**: early signals not yet significant, labeled "early."
6. **Funnel**: impressions → clicks → product views → add to cart → order or pickup → picked up. Name the step with the biggest drop against its benchmark, the likely cause, and the fix.
7. **Outside forces since the last report** and what they changed.
8. **Protective actions taken** in the period.
9. **Recommended adjustments** for Gate 3, each with the expected effect and the data behind it.
10. **Data gaps**: anything that couldn't be pulled.

Separate correlation from cause: say "rose while" rather than "rose because" unless a controlled test shows it. Never claim a sale was caused by an ad without the attribution method named.

## The dashboard (always current)

Keep one simple page that anyone can read in a minute, refreshed every hourly check:
- **Totals** for all stores or one store: spend to date vs plan, revenue and orders, return on ad spend vs break-even, profit after ads, and a health status.
- **Needs attention**: items waiting at Gate 1 and Gate 3, delivery flags waiting on Purchasing, opportunity alerts waiting, and any live line under 60% likely to beat break-even. Each links to where it's handled.
- **Insights**: three to five plain sentences: the best line, the leading and trailing store, the biggest funnel leak, the main stock issue, and the weather outlook.
- **Store cards** for Santa Rosa, Petaluma, Sonoma and Ukiah: spend, revenue, return, orders, strongest campaign, tonight's forecast, and the reasons behind the store's health. Selecting a store filters the whole page.
- **Campaign table**: health, spend, revenue, return, chance above break-even, and best and weakest store.

Health: Healthy when return is at least 1.15x break-even with no stock or weather issues; Watch when return is between break-even and 1.15x, an advertised item is short, or a weather watch is active; Needs attention when return is below break-even or an advertised item is out of stock at that store. Lines under 100 clicks or 3 days show Too early.

## Funnel diagnosis guide

| Leak | Likely causes | Typical fix |
|---|---|---|
| Low CTR | Weak hook, wrong audience, ad fatigue (frequency over 4) | New creative variant, narrower audience |
| High CTR, low product views | Slow or mismatched landing page | Point to the bundle's category or post |
| Views, low add to cart | Out of stock at nearest store, unclear choice, no local pickup info | Fix feed and store selector; add estimator |
| Cart, low orders | Pickup slot or checkout friction | Flag to e-commerce team |
| Orders, low pickups | Pickup reminders, store hours | Reminder text (opt-in only) |

## Gate 3: ADJUST

Each recommended adjustment goes to the approval queue with: the change, the reason and data, the expected effect, the cost impact, and how to undo it. Every adjustment also carries a **diagnosis and fix**:
- **Funnel table**: impression to click, click to product view, product view to add to cart, add to cart to order, each with the actual rate, its benchmark and source, and a status (OK, Below, Problem). Mark a stage Below at under 85% of benchmark and Problem at under 60%.
- **Funnel stage**: where the leak is, or "None" when the limit is budget or a safety pause.
- **Likely diagnosis** in one or two sentences, and **likely causes** (use the funnel diagnosis guide above; say which causes are confirmed by data and which are hypotheses).
- **Remediation**: numbered steps, smallest first, that fix the cause rather than only adding spend.
- **Success looks like**: a measurable target and the number of clicks or days needed to judge it.
- **Confidence**: High (the data points one way on 100 or more clicks), Medium, or Low (too early; prefer a no-cost test). The approver answers **APPROVE**, **REWORK** (with notes) or **DECLINE**. Approve per change; one approval never covers later changes. Apply only the approved version, then verify within one hour and report it.

Changes that always need Gate 3: any budget or bid increase; moving more than 20% of a campaign's budget; new audiences, areas, keywords or channels; new or edited creative; extending flight dates; ending a test early for any reason other than the protective actions.

## End of test and learnings

At the end of each flight, report the result against the hypothesis, the actual vs projected range, what to keep, what to stop, and what to test next.

Then append one record per campaign line to `learnings.jsonl`, the planning memory for future seasons (schema and verdict rules in `friedmans-ppc-learnings`):
- `id`, `campaign`, `channel`, `season` (window dates and season name), `stores`
- `conditions`: ENSO state, rain in the window, frost nights, smoke days, promotions running, stock constraints
- `projected` (ROAS, CPC, conversion rate, basket) and `actual` (days, spend, clicks, orders, revenue, ROAS, CPC, conversion rate, basket, chance above break-even)
- `verdict`: Success (chance above break-even 90% or more), Mixed (60% to 89%, or above break-even but under projection), Fail (under 60% on enough data), Too early (under 100 clicks or 3 days), Not started
- `adjustments`: each Gate 3 ID with its decision and whether it hit its success target
- `lessons`: one or two plain sentences, and `reuse`: what the next plan should start from

Also append every decision (Gate 1, 2 and 3, ad approvals, alert approvals and pre-approvals, forecast overrides, Purchasing confirmations) with who, when and any notes, as it happens. Write `season-lessons.md` with three to five lessons that hold across lines. Never edit or delete past records; correct with a new record that points to the old one.

## Outputs

- `hourly-log.jsonl` (every check and every protective action)
- `report-YYYYMMDD-HH.md` (each 8-hour report)
- `adjustments.json` (Gate 3 queue with decisions)
- `test-results.md` per campaign
- `learnings.jsonl` (results, adjustments, decisions) and `season-lessons.md`
