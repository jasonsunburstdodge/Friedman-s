# Friedman's Home Improvement: AI agent concepts

Concepts by Jason Dodge. This repo holds two **separate** agents. They share only the brand guidelines skill (`skills/friedmans-brand-guidelines.md`).

| Agent | What it does | Live demo | Files |
|---|---|---|---|
| **Content agent** | Twice-weekly blog posts, product estimators, Sana staging and social | https://jasonsunburstdodge.github.io/Friedman-s/ | Repo root: `index.html`, `PROJECT_INSTRUCTIONS.md`, `skills/`, `social/` |
| **PPC campaign agent** | Plans, launches and monitors pay-per-click tests, with approval gates | https://jasonsunburstdodge.github.io/Friedman-s/ppc-agent/ | `ppc-agent/` (see its README) |

---

# Content Agent (concept demo)

A fully automated, human-approved content system for friedmanshome.com, which runs on Sana Commerce.

**Live demo:** https://jasonsunburstdodge.github.io/Friedman-s/

## What the demo shows

- **How it works.** The twice-weekly run (Tuesday seasonal, Friday DIY) from topic planning to Sana staging and scheduled social posting.
- **2-week calendar and approval queue.** Four sample posts with reviewer approvals.
- **Blog preview.** Each post is styled as it would appear on friedmanshome.com and includes:
  - plan, do and why sections with step images;
  - in-stock product callouts;
  - a project estimator with good, better and best options, order for pickup, a list by email or text, and a free 15-minute pro consult.
- **Sana feed (simulated).** Product, price and four-store stock data the agent pulls in, with a stock rule check.
- **Social media.** Ready-to-post Facebook, Instagram carousel and story, and a TikTok video for every post.
- **Ask The Pro.** A chat bubble that answers how-to, product and stock questions and books consults.

## Repository contents

| Path | What it is |
|---|---|
| `index.html` | The content agent demo: one self-contained file that works offline |
| `PROJECT_INSTRUCTIONS.md` | Agent instructions and non-negotiables |
| `skills/` | The content agent's four Claude skills: brand guidelines (shared with the PPC agent), blog production, product estimator, Sana release and social |
| `ppc-agent/` | The separate PPC campaign agent: demo, instructions, skills and build scripts |
| `social/tiktok/` | Full-quality TikTok videos (1080×1920), posting packet, scripts, build script, music bed and jingle |

## Notes

- This is a concept for discussion. It is not affiliated with or endorsed by Friedman's Home Improvement.
- Products, prices and item numbers were read from friedmanshome.com on Oct 18, 2026.
- Stock levels outside Santa Rosa are simulated.
- Department experts and authors are fictional.
- The step illustrations, voiceovers and music are AI-generated placeholders.
- Third-party photos are credited where used.
