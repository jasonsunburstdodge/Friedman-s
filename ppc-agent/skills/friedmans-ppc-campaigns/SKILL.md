---
name: friedmans-ppc-campaigns
description: Turn the Friedman's PPC research pack into 3 to 5 test campaigns with verifiable spend, ROAS and profit projections, and run Gate 1 (pick) and Gate 2 (launch) approvals.
---

# Friedman's PPC campaign proposals and launch gates (function 5)

Use after `friedmans-ppc-research` has produced a passing research pack, when the approver asks to "Propose campaigns", and for any rework. Load `friedmans-brand-guidelines` first; every ad and landing page follows its voice, claims and channel rules.

## Step 1: Answer, then flag for confirmation

Don't stop to ask. For each input, give a working answer from the best available data, flag it to its owner for confirmation, and keep working on it. Show every flag and its status at Gate 1.

| Input | Owner | Working answer when unconfirmed |
|---|---|---|
| Stock and inbound for every hero item | Purchasing | Days of cover, suggested order and projected delivery date from open POs or vendor lead times; ads hold the item at any store that runs out before delivery |
| Test budget ceiling and window | Marketing lead | A ceiling that fits the proposed tests with at least 10% reserve |
| Gross margin by category | Finance | Industry benchmark with source (NHPA Cost of Doing Business), labeled ASSUMPTION |
| Return rate by category | Finance | Agent default, labeled ASSUMPTION |
| Approved promotions | Marketing | Current Weekly Ad only; otherwise no offer in copy |
| Customer lists with ad consent | Marketing and privacy | Not used until confirmed |
| Conversion tracking (online, pickup, store visits) | E-commerce | Flag gaps; propose a tracking fix first |

Gate 2 cannot pass until Purchasing confirms the stock flags for that campaign. Other flags can be confirmed later; until then, projections use the working answer, labeled.

## Step 2: Build candidates

Draft 5 to 8 candidates, then keep the 3 to 5 with the best evidence. Each candidate is one testable idea:
- **Bundle**: the real products (catalog names and item numbers), each passing the stock rule at the stores it targets.
- **Trigger and timing**: the buying trigger, the signal that starts and stops the burst, flight dates.
- **Audience and geo**: areas and audiences from the geo-channel scores.
- **Channels and formats**: with the job each channel does.
- **Landing page**: a product category page, a store page, or a content agent post with its estimator. Never a homepage.
- **Creative**: 2 to 3 variants to test, in brand (Barlow caps headline, plain can-do voice, SHOP + category CTA, no fixed prices in copy, no fear lines).
- **Hypothesis and success metric**: one sentence ("Storm bursts timed 48 hours before rain beat always-on by 30% on ROAS") and the metric that decides it.

## Step 3: Project, with every number traceable

For each channel line:

```
clicks          = spend / CPC
orders          = clicks x conversion rate
revenue         = orders x average order value (AOV)
ROAS            = revenue / spend
gross profit    = revenue x (1 - return rate) x gross margin
profit after ads= gross profit - spend
break-even ROAS = 1 / (gross margin x (1 - return rate))
```

- **CPC and conversion rate**: Friedman's own account history first. Without it, published benchmarks for the closest vertical and campaign type, with the source and date. Search benchmarks for "home improvement" are dominated by contractor lead generation and are not retail product clicks; use retail Home and Garden ecommerce benchmarks for product campaigns and say so.
- **AOV**: the bundle's typical basket from POS data. Without it, the sum of the bundle's real catalog prices for the typical quantity, labeled.
- Show a **range** (low, base, high) from the spread of the sources, not a single point.
- Mark each campaign's **confidence** (High, Medium, Low) by how much of it rests on Friedman's own data.
- Show **what would prove it wrong** within the test (for example, ROAS below break-even after 1,000 clicks).
- Never round a range into a promise. Write "projected" on every projected number.

## Step 4: Rank and pick 3 to 5

Rank by expected profit after ads at base case, then by confidence, then by learning value. Keep at least one low-risk campaign (high intent, Search or local inventory) and at most one exploratory channel test. Total proposed spend must fit the ceiling with at least 10% held in reserve for Gate 3 reallocations.

## Gate 1: PICK

Send the approver a one-page proposal:
- The 3 to 5 campaigns, each with bundle, trigger, geo, channels, budget, flight dates, projected ROAS range, projected profit after ads range, confidence, and hypothesis.
- The assumptions in use and the questions still open.
- What the agent recommends and why, in two sentences.

Optional buyer-segment tests from `friedmans-ppc-segments` appear below the main proposal, each with APPROVE or DECLINE.

The approver answers per campaign: **APPROVE**, **REWORK** (with notes) or **DECLINE**. On REWORK, revise only that campaign, rerun the projection and checks, bump its version, and resubmit. Nothing is built in an ad account before Gate 1.

## Build (after Gate 1, before Gate 2)

Build each approved campaign **paused** (or as a draft) in the platform:
- Daily caps set at or below the approved budget; account-level and campaign-level limits both set.
- Geo targeting by ZIP or radius exactly as approved; exclusions for areas outside the trade area.
- Product feeds filtered to items that pass the stock rule per store; local inventory ads only for stores with stock.
- UTM tags on every URL (`utm_source`, `utm_medium=cpc` or `paid_social`, `utm_campaign=<campaign ID>`, `utm_content=<variant>`).
- Conversion events verified firing (purchase, pickup order, add to cart, store-visit or offline import).
- Negative keywords (jobs, free, DIY videos unrelated to products, competitor names).
- Creative checked against the brand check in `friedmans-brand-guidelines` section 13.

## Ad samples (approved before Gate 2)

Write the actual ads for every venue in each approved campaign, shown as they'll appear:
- **Google Search**: responsive search ad with up to 15 headlines (30 characters), 4 descriptions (90), 2 paths (15) and sitelinks.
- **Performance Max and local inventory**: headlines (30), long headline (90), descriptions (90), the ad image in 1:1, 1.91:1 and 9:16, plus real product images from the catalog.
- **Meta**: primary text (125 recommended), headline (40 recommended) and the ad image in each placement size (see Ad images below).
- **Nextdoor**: a neighborly, store-specific post with a useful tip.
- **TikTok**: ad text (100), a hook in the first 3 seconds, the script beats, the finished video (see TikTok video below) and the AI-generated content label.
- **SMS**: one segment (160), ends with "Reply STOP to opt out." **Email**: subject, preheader, body, CTA.
- Spanish variants are reviewed by a fluent team member before approval.

### Ad images (ChatGPT)

Generate the post images in ChatGPT image generation, in the approver's browser, from two references: the Friedman's wordmark (green on white, unaltered) and the campaign layout sheet (photo under a dark scrim, logo top left, white headline with the last words in yellow `#FFE500`, white subhead, rounded yellow button with dark text and an arrow).
- **Sizes per venue:** Meta feed 1:1 plus Stories and Reels 9:16; Performance Max 1:1, 1.91:1 and 9:16; Nextdoor 1.91:1; email header 1.91:1. For 9:16, keep the top 250 px and bottom 350 px free of text.
- **Prompt rules, every image:** exact headline, subhead and button text in quotes; no prices; unbranded products; no faces (gloved hands are fine); no fire, smoke, flooding or damage; calm, prepared mood for weather campaigns.
- **One image per message** in a single ChatGPT thread, so the look stays consistent. Download each to a named file (`friedmans-<campaign>-<format>.png`), then compress to WebP at 1080 px on the long side.
- **Check before approval:** logo matches the reference exactly, every word is spelled right (accents in Spanish), the button says SHOP plus a category, and nothing in the image breaks the brand rules. If the logo is wrong, regenerate or overlay the real logo file on a white plate.
- **Label:** "AI-generated image (ChatGPT), placeholder until Friedman's photography." Swap in Friedman's own photos when they exist.

### TikTok video (ElevenLabs)

Same system as the content agent's TikToks:
- **Voiceover:** ElevenLabs, eleven_v4, Nicole (warm, conversational) for garden and storm campaigns. Generate once with the default 4 takes; never re-run to retry. Pick a take and keep its generation ID.
- **Scenes:** 4 to 5 text-free 9:16 scenes from ChatGPT, one per beat (hook, why, each step).
- **Assembly:** the renderer (`creative/tiktok/render_ppc.py`) adds the logo plate, step labels, progress dashes and captions timed to the pauses in the voice, a product card from the catalog, the come in / order online / book a pro card, the animated logo end card, a music bed ducked under the voice, and the jingle.
- **Rules:** no prices or stock counts in the voice or captions; don't say "all four stores" unless every hero item is in stock at all four; turn on TikTok's AI-generated content label.

Check every ad automatically: platform hard limits, no prices in copy, no em or en dashes, no "best", "lowest" or "guarantee", no "Learn More", SHOP plus a category. Show character counts. Each ad gets **APPROVE**, **REWORK** (notes required) or **DECLINE**. Gate 2 lists ads approved vs total and cannot pass until every ad in that campaign's launch packet is approved or removed.

## Gate 2: LAUNCH

Send the launch packet: exact budgets and caps, flight dates and time zone, geo list, audiences, every ad variant as it will appear, landing pages, tracking checks with results, and the stop rules. The approver answers **APPROVE** (for that exact version), **REWORK** or **DECLINE**. Only then set the campaign live. Verify within one hour that it is serving as built, spend is pacing under the cap, and conversions are recording. Report the verification.

## Outputs (under the cycle ID)

- `proposal.json` and `proposal.md` (Gate 1 page), with every projection's inputs and sources
- `build-spec.json` per campaign (Gate 2 packet)
- `approvals.json`: who approved what version and when
- `campaign-review.json`: PASS or REVISE for: products real and in stock; numbers traceable; ranges not promises; budget within ceiling with reserve; brand check passed; tracking verified; sensitivity check passed.
