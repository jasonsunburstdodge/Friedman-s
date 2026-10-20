# Friedman's Home Improvement: PPC Campaign Agent (concept demo)

A concept by Jason Dodge for an AI agent that plans, launches and manages pay-per-click campaigns for Friedman's four stores, with a person approving every dollar it spends. This is a **separate agent** from the content agent at the root of this repo. The two share only the brand guidelines skill.

**Live demo:** https://jasonsunburstdodge.github.io/Friedman-s/ppc-agent/

## What the demo shows

Open the Overview tab first. It explains every part and has a five-minute walkthrough.

- **Dashboard.** All campaigns at a glance, what needs a decision, insights, and health by store.
- **Plan.**
  - Best sellers from 3 seasons with a reviewable forecast.
  - Outside forces: El Niño, rain, frost, smoke and stock.
  - Audience and buying triggers, and where to spend.
  - Optional buyer segments, such as contractors, property maintenance, landscapers, frequent DIYers and new homeowners.
- **Campaigns.**
  - 3 to 5 test campaigns with traceable projections: spend, ROAS, and profit after cost and returns.
  - Ready-to-approve ads for Google Search, Performance Max, Meta, Nextdoor, TikTok, SMS and email.
  - Purchasing and finance confirmations.
- **Monitor.**
  - Hourly results and 8-hour reports.
  - Adjustments, each with a funnel diagnosis, likely causes and a fix.
  - Weather opportunity alerts that draft flash campaigns.
- **Learnings.** Results, adjustments and every decision, saved as starting numbers for the next same-season plan.
- **Three approval gates.** Pick, Launch and Adjust, with Approve, Rework (with notes) or Decline at each.

## Folder contents

| Path | What it is |
|---|---|
| `index.html` | The full demo: one self-contained file that works offline |
| `PROJECT_INSTRUCTIONS.md` | PPC agent instructions, gates, non-negotiables, and the data needed to go live |
| `skills/` | The six PPC skills: research, campaigns, monitoring, segments, alerts, learnings |
| `../skills/friedmans-brand-guidelines.md` | Brand skill, shared with the content agent |
| `demo-build/` | Data and scripts that build the demo (`python3 build.py assets.json > ../index.html`) |

## Real, assumed and simulated

- **Real:**
  - 66 Friedman's products, prices and on-hand stock at all four stores, read from friedmanshome.com on Oct 18 to 19, 2026.
  - The Weekly Ad.
  - NWS forecasts and alerts, and NOAA weather history.
  - Google Trends, Census, BLS and home-sales data.
  - Industry margins and 2026 ad benchmarks.
- **Assumption:** margin, returns, test budget, alert response rates and lead times. Each is flagged to its owner.
- **Simulated:** sales history, purchase orders, opted-in audiences, business accounts and all campaign results.

## Notes

- This is a concept for discussion. It is not affiliated with or endorsed by Friedman's Home Improvement.
- No ad account, POS or customer data is connected. Nothing in the demo spends money or sends a message.
