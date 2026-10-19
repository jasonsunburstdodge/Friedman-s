---
name: friedmans-product-estimator
description: Pick in-stock products for a Friedman's blog post and build its project estimator (questions, quantities, good/better/best, pickup cart, saved list, pro walkthrough) from the Sana catalog.
---

# Friedman's product picks and project estimator

Use this skill after a Friedman's blog draft exists (from `friedmans-blog-production`), whenever products are attached to a post, or when an estimator is built or rechecked. It needs read access to the Sana Commerce catalog: product ID or SKU, name, URL, image, price, attributes, and on-hand stock per store. Sales or co-purchase data improves the picks when available.

Follow `friedmans-brand-guidelines` for product naming (exactly as in the Sana catalog), claims, colors and type in callouts and the estimator.

If catalog or stock data is not available, stop at a draft product list marked NOT VERIFIED and say exactly which data is missing. Never invent SKUs, prices, specs or stock.

## Stores

Santa Rosa, Petaluma, Sonoma, Ukiah. Always show and check all four.

## Part 1: Pick products

### Eligibility (all must be true)

1. Active, sellable online, with a product image and page.
2. **In stock at all four stores** at the time of picking, with on-hand quantity at least the larger of the store's safety stock or 2x the estimator's typical quantity. Record the stock snapshot and time.
3. Fits the job described in the post (correct size, type, rating, indoor or outdoor use).
4. Not a product that requires a licensed professional to install when the post is DIY.

If a needed item fails eligibility at any store, use an eligible equivalent. If no equivalent exists, either drop the topic (tell `friedmans-blog-production`) or keep the item with a clear store-by-store availability note, and flag it for the reviewer. Never recommend an item that is out at every store.

### Rank by likelihood of need

Classify every candidate:

- **Required:** the project cannot be done without it.
- **Recommended:** most people doing this project will need it (consumables, items commonly not on hand, safety gear the work really calls for).
- **Optional:** helpful upgrades or nice-to-haves.

Rank within each class by evidence of need: attach rate or co-purchase with the core item, sales velocity in the season, and the steps in the article. Record the reason for each pick. Keep the estimator to 3 to 8 items. Do not add items to raise the basket; every item must map to a step or a stated need.

### Good, better, best

Offer tiers only when they are **genuinely** different:

- Same job, same fit, comparable quantity.
- Differences come from the product specs: material, durability, warranty, capacity, performance, features.
- Quality increases with price. "Best" is not just the most expensive item.
- Each tier gets one plain line explaining what you get for the step up, taken from the specs.
- Size or quantity differences are not tiers; handle them with questions and quantities.
- Every tier product must itself meet eligibility (stocked at all four stores).
- If only one sensible product exists, show one option. If only two are meaningful, show two. Never pad a tier.

Default selection in the estimator is "Better" where it exists, otherwise the nearest available tier.

### Items that need a choice

Flag any item where the customer must choose color, finish, texture, species or variety, size or fit to their existing fixture, or type when the right type depends on what they have. Do not choose for them. These items show "Needs a choice" and offer the free pro walkthrough.

### Product callouts in the article

Place 2 to 4 product callouts inside the post at the step where each product is used. Each shows: catalog image, product name, one-line reason it is needed at this step, live price, tier price range when tiers exist, live stock chips for all four stores, a "View product" link, and "Need help choosing?" when the item needs a choice.

## Part 2: Build the estimator

### Questions

- Ask only questions that change which items appear, the tier options, or quantities. Usually 2 to 5.
- Plain language, with a short hint on how to measure or check ("Pull back the old strip to see if there's a groove").
- Sensible defaults for a typical North Bay home.
- Include "Not sure" where a wrong answer would change the product; "Not sure" routes that item to "Needs a choice."

### Quantities

- Use manufacturer coverage or spec data (square feet per gallon, cubic feet per bag, feet per roll, units per pack).
- Show the formula and assumptions in the config (for example, depth 2 inches, or 3 inches for clay; 10 percent waste for cut materials).
- Round up to sellable units. Never over-quantify to upsell.

### The list the customer sees

For each item: checkbox (Required and Recommended start checked, Optional unchecked; customers uncheck what they already have), name and need label, quantity times product, unit price, tier selector when tiers exist, the one-line tier difference, stock chips for all four stores, "Needs a choice" when flagged, and the line total. A "Set all to Good, Better, Best" control applies the nearest available tier to every item. Show a running estimated total of checked items.

### Three actions

1. **Order for pickup.** Customer chooses a store. Show whether every checked item is in stock there, and flag low or out items before they commit. "Add to cart" sends the checked SKUs, quantities and chosen tiers to the Sana cart with in-store pickup at that store.
2. **Send me my list.** The customer chooses email or text and enters an address or mobile number. The list arrives with checkboxes, quantities, tiers, item numbers, product links, store stock and the post link; a text sends a short summary with a link to the full list. Project tips or other marketing go out only if the customer ticks a separate, unchecked opt-in, and every text includes opt-out instructions.
3. **Book 15 minutes with a pro.** A free 15-minute project consultation. The customer picks a department expert (the post's department is marked Best fit, related departments Good fit), how to meet (in store at the expert's store, video or phone), a day and an open 15-minute slot. The request carries the items that need a choice, so the expert can have samples ready. Uses Friedman's real scheduling tool; never promise a time that the tool has not confirmed.

### Live data rules

- Prices, sale prices and stock render live from Sana when the page loads. Never write them into article copy or the config as fixed values (sample values are allowed only in a clearly labeled demo).
- If an item goes out of stock at a store after publishing, the live chips show it. The weekly recheck (in `friedmans-sana-release`) proposes a swap if it is out at two or more stores or out anywhere for more than 7 days.

## Outputs

Saved under the post's content ID:

- `products.json`: each pick with SKU, class, reason, step it maps to, tier products and their one-line differences, choice flag, stock snapshot per store with timestamp.
- `estimator-config.json`: questions (id, label, hint, type, options, default, show-when), items (id, name, need, why, show-when, quantity formula with assumptions, tiers mapped to SKUs, choice text), and the three actions. Keep formulas as simple expressions a developer can implement safely; no executable code.
- `placement-map.json`: which `{{product:ID}}` placeholder goes after which step.
- `estimator-review.json`: PASS or REVISE with reasons for eligibility at all four stores, likelihood ranking, honest tiers, choice flags, quantity math (test with defaults and with one edge case), and no prices in copy.

Fix any REVISE before handoff to `friedmans-sana-release`.
