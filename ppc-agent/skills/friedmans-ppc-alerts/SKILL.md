---
name: friedmans-ppc-alerts
description: Watch NWS and AirNow for each Friedman's store hourly and, when a rule fires (frost, severe storms, flood, power shutoff, smoke, first rain), auto-draft a flash campaign with goals, projections, targeting, stock checks, safety notes and an expiry, for fast-track approval.
---

# Friedman's opportunity alerts (flash campaigns)

Runs every hour alongside `friedmans-ppc-monitoring`. Load `friedmans-brand-guidelines` first. Uses the benchmarks and break-even math in `friedmans-ppc-campaigns` and the live stock rules in `friedmans-ppc-research`.

## What to check, every hour

For each store (Santa Rosa, Petaluma, Sonoma, Ukiah), using the store's coordinates:
- **NWS active alerts** (`api.weather.gov/alerts/active?point=lat,lon`): Frost Advisory, Freeze Warning, Severe Thunderstorm Watch or Warning, Wind Advisory, High Wind Warning, Flood Watch or Warning, Red Flag Warning.
- **NWS forecast** for the point (`api.weather.gov/points/lat,lon`, then its forecast): overnight lows, precipitation chance, thunderstorm mentions, wind.
- **AirNow AQI** for each trade area.
- **Utility shutoff notices** (PSPS) for each trade area.

Record the source, issue time, zone and text for every trigger.

## Rules

| Alert | Fires when | Level |
|---|---|---|
| Frost Tonight | NWS Frost Advisory or Freeze Warning, or a forecast low of 34°F or colder | Alert; 35 to 36°F is Watch |
| Severe Storm Prep | Severe Thunderstorm Watch or Warning, Wind Advisory or High Wind Warning | Alert; thunderstorms forecast at 40% or more is Watch |
| Flood Watch Ready | Flood Watch, or 1 inch or more of rain forecast in 24 hours | Alert |
| Power Outage Ready | Red Flag or High Wind Warning with a utility shutoff notice | Alert |
| Smoke Day | AQI Unhealthy for Sensitive Groups or worse | Routed to the approved Clean Air standby |
| Rain In The Forecast | 40% or more chance of rain within 72 hours after a dry stretch | Routed to Gutter Gear's approved burst |

Routed alerts don't create new drafts: they run inside an already-approved campaign's trigger and caps, and are reported within the hour. Watch-level drafts use half the paid budget.

## Every draft includes

1. **Trigger evidence**: the alert or forecast text, source, zone and time.
2. **Affected stores** and the window (start, phases, end). For storms: a prep phase, a pause while any warning is in effect, and a cleanup phase after.
3. **Products**: real catalog items with live stock at each affected store. If an item covers under half the expected need at a store, swap in an in-stock alternative or hold it out of that store's ads and flag Purchasing. If it covers half or more, sell what's there and pace that store's paid spend to stock.
4. **Goals**: orders, revenue and profit after costs (base case), a stretch goal (high case), and paid ROAS of at least 1.2 times break-even. **Goals are capped by what the lead item can actually fill** at the affected stores.
5. **Projections** (low, base, high) for each channel:
   - Paid: campaign benchmarks with an alert-intent lift on conversion, labeled ASSUMPTION until Friedman's own alert results exist. A paid line projected below break-even is left out of the budget.
   - Owned: SMS and email to opted-in customers of the affected stores, with conservative response rates labeled ASSUMPTION until Friedman's own results exist.
6. **Budget** from the reserve only, never beyond what's left.
7. **Targeting**: affected trade areas, opted-in lists of those stores, alert-specific search terms, a Meta radius around each store. Exclude any area under an evacuation order, and any area under a warning that pauses ads. No targeting by protected traits.
8. **Creative** in brand: Barlow caps headline, Title Case subhead, SHOP plus a category, no prices in copy, no fear lines.
9. **Safety and sensitivity notes** specific to the alert (for example: pause during a Severe Thunderstorm Warning; no open flames for pipes; "Turn around, don't drown"; carbon monoxide warnings with any generator).
10. **Also do**: store-ops tasks (endcaps, staging, Drive-Thru Pickup staffing), Google Business Profile posts per store, a quick tip from the content agent, and Pro Desk heads-ups.
11. **Expiry**: the draft expires when the alert ends, or at a set time (2 p.m. for frost), if it isn't approved.

## Approval

- **Fast-track approve** covers Gate 1 and Gate 2 together, because the packet, caps, tracking and stock checks are prebuilt. Verify that it is serving within one hour and report.
- **Approve owned channels only**, **Rework** (with notes) or **Decline** are always available.
- **Standing pre-approval**: an approver may pre-approve an alert type up to a set amount per event. Matching drafts within that cap launch automatically and are reported within the hour. Pre-approval is recorded with who and when, never extends beyond its cap, and can be revoked at any time. Without it, nothing launches on its own.

## Outputs

- `alerts-log.jsonl`: every hourly scan, what fired and why.
- `alert-<id>.json`: each draft with all fields above and the decision.
- In the next 8-hour report: alerts drafted, approved, auto-launched under pre-approval, expired, and results against goals.
- Ad samples for every channel in the draft, written and checked by the rules in `friedmans-ppc-campaigns` (Ad samples). Fast-track approval covers these ads.
- A result record in `learnings.jsonl` when the alert campaign ends (see `friedmans-ppc-learnings`), with the alert type and conditions, so the next alert of that type starts from Friedman's own response rates instead of the assumptions above.
