# PPC visual creative standards - proposed, not approved

Status: REVIEW ONLY. This document does not override the shared brand skill or authorize publication, ad spend, campaign changes or live dashboard edits.

## Source and safeguards
- Baseline: main commit `a8ea1a939e320f0e18ec7b9c9f5fb3e692fd2267`.
- Preserve `ppc-agent/index.html`, `ppc-agent/demo-build/`, existing skills, campaign identifiers, metrics, simulations and all three approval gates unchanged.
- The existing `skills/friedmans-brand-guidelines.md` remains authoritative. In a conflict, stop and seek marketing approval.
- User provided two logo references in conversation on Oct. 19, 2026: white house/checkmark plus Friedman's lockup on green, and green horizontal Friedman's wordmark. Original, licensed, production-ready files and usage rights must be verified and stored before export. Never redraw or synthesize the logo.

## Mandatory visual quality gate
1. Every static image, carousel card and video closing frame carries one verified Friedman's logo variant. Place on a solid, quiet, high-contrast field with sufficient clear space. Use approved source artwork unchanged. If a placement cannot support a legible logo, escalate for an exception instead of squeezing or distorting it.
2. Google Search responsive text ads and other text-only placements are exempt from image-logo requirements. Use supported business-name/logo platform assets when available and approved.
3. Lead with one clear customer outcome or project need. Headline, relevant photo/product, supporting benefit and specific SHOP CTA must form a visible hierarchy.
4. Use real, attributable work-in-progress or achievable project photography; no AI-generated people, generic stock models or invented store/customer scenes. Placeholder photography must be conspicuously labeled and credited, never delivered as final.
5. Respect brand typography (Barlow display, News Cycle body), `#007A33` green, white, charcoal and approved limited accents. Keep copy readable at mobile sizes. Use dark scrims when text overlays photos. Buttons square.
6. No unsupported prices, stock, sale offers, delivery promises or claims. Dynamic inventory and current Weekly Ad remain sources of truth.
7. Design separately for each placement's safe areas, cropping, aspect ratio and text limits. Do not simply resize one layout across all platforms.
8. Provide three genuinely distinct visual approaches per campaign: outcome/lifestyle, product-in-use, and practical problem-solution. All variants need platform-appropriate copy, asset provenance, logo choice, alt text and a named reviewer.
9. Check safe areas, text legibility, brand consistency, contrast, product relevance, factual claims and CTA clarity at actual mobile display size before Gate 2.
10. Approval gate: proposed creative is DRAFT until a named Friedman's approver signs off. Any post-approval creative change follows existing Gate 3 rules.

## Suggested creative directions for review, not approved claims
- Rain/gutters: `Rain belongs outside your home.` Show real gutters and drainage in use; CTA `SHOP GUTTER SUPPLIES`. Confirm specific products and local availability.
- Fall planting: `Your spring garden starts this fall.` Show a real achievable North Bay planting project; CTA `SHOP GARDEN SOIL`. Validate horticultural applicability to promoted products and location.
- Storm supplies: `The right supplies before the rain.` Show sandbags, tarps and wet/dry vacs in a practical setting; CTA `SHOP STORM PREP`. Avoid disaster imagery and fear framing.
- Smoke/air: `Help keep indoor air cleaner.` Use approved product photography and careful qualified claims; CTA `SHOP AIR QUALITY`. Do not imply guaranteed health protection.
- Frost: `Protect outdoor faucets before the cold.` Show actual faucet covers and pipe insulation; CTA `SHOP FROST PROTECTION`. Trigger only on verified local forecasts.

## Production acceptance checklist
- [ ] Source logo files obtained and verified against supplied references
- [ ] Creative is distinct from existing demo, and source images are cleared for use
- [ ] Brand guide check passes
- [ ] Each format previewed at native size and mobile crop
- [ ] Copy and product claims validated
- [ ] Campaign ID, CTA and destination preserved
- [ ] Named reviewer approved creative
- [ ] No modifications to live branch or advertising accounts

## Integration plan after review
Update only the creative authoring instructions and presentation layer on a separate branch. Compare file-by-file against baseline, regenerate any derived HTML from its existing builder rather than hand-editing generated output, run builder checks and inspect visual diffs. Do not merge or publish without explicit approval.
