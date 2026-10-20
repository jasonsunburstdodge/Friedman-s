"""Projection model for the Friedman's PPC agent demo.

Every input is tagged VERIFIED (real, with source), ASSUMPTION (agent default, asked at Gate 1)
or SIMULATED (stands in for Friedman's internal data). Run: python3 model.py > data.json
"""
import json, math

P = {p["item"]: p for p in json.load(open(__import__("sys").argv[1]))["products"]}

MARGIN = 0.38      # ASSUMPTION, flagged to Finance: midpoint of NHPA 2025 home center (32.4%) and hardware store (42.6%) gross margins
RETURNS = 0.05     # ASSUMPTION: return rate, asked at Gate 1
BREAKEVEN = 1 / (MARGIN * (1 - RETURNS))

# Channel benchmarks: (low, base, high) for CPC and conversion rate, with sources.
BENCH = {
  "search": dict(label="Google Search", cpc=(3.00, 1.75, 1.28), cvr=(0.029, 0.035, 0.055), status="VERIFIED range",
      src="Retail Home & Garden Search CPC $1.28 (COREPPC via Webtonic, 2026); $1.50 to $3.00 CPC, 3.5% to 5.5% CVR (Webtonic, 2026). Base CPC $1.75 is the agent's midpoint. Not the $8.33 'home improvement' figure, which is contractor lead gen."),
  "pmax": dict(label="Performance Max + local inventory", cpc=(1.20, 1.05, 0.61), cvr=(0.021, 0.029, 0.035), status="VERIFIED range",
      src="Shopping Home & Garden CPC $1.05, CVR 2.9% (FoundryCRO 2026); Shopping CPC $0.61 (COREPPC 2026); CVR 2.1% (OwlClaw); PMax runs about 14% above Shopping CPC (FoundryCRO). High CVR 3.5% is an agent assumption."),
  "meta": dict(label="Meta (Facebook, Instagram)", cpc=(1.10, 0.63, 0.60), cvr=(0.012, 0.015, 0.020), status="Base VERIFIED, spread ASSUMPTION",
      src="Home & Home Improvement traffic CPC $0.63 (WordStream 2026 via Coupler.io); Home & Garden CPC $1.10 (ContentStudio 2026); purchase CVR median about 1.5% (ContentStudio 2026). CVR spread is the agent's."),
  "tiktok": dict(label="TikTok", cpc=(0.98, 0.75, 0.52), cvr=(0.014, 0.0201, 0.026), status="Base VERIFIED, spread ASSUMPTION",
      src="TikTok CTR 1.77%, CPM $13.26, CVR 2.01% (Whatagraph 2026). CPC = CPM / (1,000 x CTR) = $0.75. Spread of 30% is the agent's."),
  "nextdoor": dict(label="Nextdoor", cpc=(1.50, 1.00, 0.70), cvr=(0.008, 0.012, 0.018), status="ASSUMPTION",
      src="No public Nextdoor benchmark found (searched Oct 19, 2026). Treated as a learning test; numbers are agent assumptions."),
}

def basket(lines):
    out, tot = [], 0.0
    for item, qty in lines:
        p = P[item]; t = round(p["price"] * qty, 2); tot += t
        out.append(dict(item=item, name=p["name"], qty=qty, price=p["price"], line=t, stock=p["stock"], new=p["new"]))
    return out, round(tot, 2)

def project(ch, spend, aov):
    b = BENCH[ch]; res = {}
    for k, i in (("low", 0), ("base", 1), ("high", 2)):
        cpc, cvr = b["cpc"][i], b["cvr"][i]
        clicks = spend / cpc; orders = clicks * cvr; rev = orders * aov
        gp = rev * (1 - RETURNS) * MARGIN
        res[k] = dict(cpc=cpc, cvr=cvr, clicks=round(clicks), orders=round(orders, 1), revenue=round(rev),
                      roas=round(rev / spend, 2), gross_profit=round(gp), profit_after_ads=round(gp - spend))
    return res

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from campaigns import CAMPAIGNS

out = dict(margin=MARGIN, returns=RETURNS, breakeven=round(BREAKEVEN, 2), bench=BENCH, campaigns=[])
for c in CAMPAIGNS:
    items, aov = basket(c["basket"])
    c2 = {k: v for k, v in c.items() if k not in ("basket", "lines")}
    c2["items"], c2["aov"] = items, aov
    c2["lines"] = [dict(ch=ch, label=BENCH[ch]["label"], spend=s, proj=project(ch, s, aov)) for ch, s in c["lines"]]
    tot = dict(spend=sum(l["spend"] for l in c2["lines"]))
    for k in ("low", "base", "high"):
        rev = sum(l["proj"][k]["revenue"] for l in c2["lines"])
        pa = sum(l["proj"][k]["profit_after_ads"] for l in c2["lines"])
        tot[k] = dict(revenue=rev, roas=round(rev / tot["spend"], 2), profit_after_ads=pa)
    c2["total"] = tot
    out["campaigns"].append(c2)
print(json.dumps(out, indent=1))
