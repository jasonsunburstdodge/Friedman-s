"""Derive geo splits, stock checks, purchasing flags (simulated POs), confirmations, segments and 8-hour reports.
Run: python3 derive.py projections.json sim.json products_all.json real_segments.json > derived.json
"""
import json, sys, math, datetime as dt
proj = json.load(open(sys.argv[1])); sim = json.load(open(sys.argv[2])); PA = json.load(open(sys.argv[3])); SEG = json.load(open(sys.argv[4]))
P = {p["item"]: p for p in PA["products"]}
STORES = sim["stores"]
DEMO = {  # REAL: Census QuickFacts, ACS 2019-2023 (city)
 "Santa Rosa": dict(owner=56.2, income=97410, value=685000, pph=2.54), "Petaluma": dict(owner=63.9, income=109823, value=834900, pph=2.43),
 "Sonoma": dict(owner=63.1, income=101281, value=954300, pph=1.98), "Ukiah": dict(owner=45.8, income=67122, value=448100, pph=2.60)}
share = {s: sim["aud"][s]["cust_share"] / 100 for s in STORES}
def norm(w): t = sum(w.values()); return {k: round(v / t * 100) for k, v in w.items()}
GEO = {
 "C1": norm({s: share[s] * DEMO[s]["owner"] for s in STORES}),
 "C2": norm({s: share[s] * (1.3 if s in ("Petaluma", "Sonoma") else 1.0) for s in STORES}),
 "C3": norm({s: share[s] * DEMO[s]["income"] / 100000 * (0.8 if s == "Ukiah" else 1) for s in STORES}),
 "C5": {s: "smoke only" for s in STORES},
 "C4": norm({s: share[s] * (1.6 if s == "Ukiah" else 1.3 if s == "Sonoma" else 1.0) for s in STORES}),
}
FLIGHT = {"C1": dt.date(2026, 10, 21), "C2": dt.date(2026, 10, 28), "C3": dt.date(2026, 10, 22), "C5": dt.date(2026, 10, 20)}
LEAD = {"Amerimax": 6, "Frost King": 5, "DAP": 4, "Atlas": 4, "Channellock": 9, "Generic": 3, "Grip-Rite": 5, "Gardner & Bloome": 3,
        "Redi-Gro": 3, "Filtrete": 7, "3M": 5}   # SIMULATED vendor lead times in days
PO_DATE = dt.date(2026, 10, 20)
def vendor(name): return name.rsplit(", ", 1)[-1]

checks, flags = [], []
for c in proj["campaigns"]:
    if c["recommend"].startswith("OWNED"): continue
    weeks = 3
    orders_wk = sum(l["proj"]["base"]["orders"] for l in c["lines"]) / weeks
    if c["id"] == "C5": orders_wk = sum(l["proj"]["base"]["orders"] for l in c["lines"]) / 1  # all spend lands in smoke weeks
    for it in c["items"]:
        row = dict(cid=c["id"], item=it["item"], name=it["name"], qty=it["qty"], stores={})
        short = []
        for s in STORES:
            g = GEO[c["id"]][s]; g = 25 if g == "smoke only" else g
            need = orders_wk * it["qty"] * g / 100
            rule = max(2, math.ceil(2 * need)); oh = P[it["item"]]["stock"][s]
            status = "PASS" if oh >= rule else ("CHECK INBOUND" if oh >= max(2, math.ceil(need)) else "SHORT")
            row["stores"][s] = dict(on_hand=oh, weekly_need=round(need, 1), rule=rule, status=status)
            if status != "PASS":
                order = math.ceil(need * (weeks + 2) - oh)
                lt = LEAD.get(vendor(it["name"]), 7)
                eta = PO_DATE + dt.timedelta(days=lt)
                cover_days = oh / (need / 7) if need > 0 else 99
                runs_out = FLIGHT[c["id"]] + dt.timedelta(days=int(cover_days))
                short.append(dict(store=s, on_hand=oh, two_week_need=rule, order=max(order, 1), eta=eta.isoformat(), lead=lt,
                                  cover_days=round(cover_days, 1), runs_out=runs_out.isoformat(), late=eta > runs_out))
        checks.append(row)
        if short:
            late = [x for x in short if x["late"]]
            plan = ("Stock runs out before delivery at " + ", ".join(x["store"] for x in late) +
                    ": the agent holds this item out of those stores' ads until the day after delivery.") if late else "On-hand covers demand until delivery at every store."
            flags.append(dict(id=f"PO-{c['id']}-{it['item']}", cid=c["id"], item=it["item"], name=it["name"], vendor=vendor(it["name"]),
                              stores=short, plan=plan, owner="Purchasing"))
# The vac restock for Storm Ready is the condition on C2; make sure it is flagged even if math passes
confirm = [
 dict(id="CF-budget", owner="Marketing lead", q="Test budget ceiling", answer="$10,000 for 21 days", value=10000, kind="budget",
      basis="Sized to fit four paid tests with at least 10% held for Gate 3. Change it and every projection recalculates."),
 dict(id="CF-margin", owner="Finance", q="Gross margin on these categories", answer="38%", value=38, kind="margin",
      basis="Midpoint of NHPA's 2025 Cost of Doing Business averages: home centers 32.4%, hardware stores 42.6%. Garden and hardware consumables usually sit above lumber."),
 dict(id="CF-returns", owner="Finance", q="Return rate", answer="5%", value=5, kind="returns",
      basis="No public figure for home improvement retail was found. Agent default until Finance supplies the POS return rate."),
 dict(id="CF-lists", owner="Marketing and privacy", q="Opted-in email and SMS lists for ad audiences", answer="Not used until confirmed", value="no", kind="lists",
      basis="Lists are uploaded hashed only if their consent covers advertising. Paid tests run without them meanwhile."),
 dict(id="CF-spanish", owner="Marketing lead", q="Spanish-language variants", answer="Yes, as their own test line", value="yes", kind="spanish",
      basis="About 29% of Sonoma County and 27% of Mendocino County residents are Hispanic (Census). Never used as targeting by ethnicity."),
]

# ---- Buyer segments: REAL sizes where public, SIMULATED Friedman's reach ----
Q = SEG["qcew"]; H = SEG["homes"]
def est(k): return Q["Sonoma"].get(k, [0, 0])[0] + Q["Mendocino"].get(k, [0, 0])[0]
def emp(k): return Q["Sonoma"].get(k, [0, 0])[1] + Q["Mendocino"].get(k, [0, 0])[1]
segments = [
 dict(id="S1", name="Contractors and trades", kind="Known: Pro Advantage and Contractor Services", flag="EXPLORE",
      real=[f"{est('236 Building construction'):,} building contractors and {est('238 Specialty trade contractors'):,} specialty trade contractors in Sonoma and Mendocino counties, {emp('236 Building construction') + emp('238 Specialty trade contractors'):,} employees (BLS, Q1 2025)",
            "Pro Tool Days runs Oct 19 to 25 with vendor demos Oct 22 to 24 at Santa Rosa, Petaluma and Ukiah (friedmanshome.com Weekly Ad)"],
      sim=["Pro Advantage accounts: 2,140; 31% of them bought in the last 90 days", "Pro accounts average 3.4 visits a month"],
      why="A large, nearby trade base plus a real event this week. El Niño storm repairs (roof patch, sealant, tarps, sandbags by the pallet) fit pro baskets.",
      products=["2000031875", "2000023006", "300601171", "4314103", "2000038308"],
      test="Customer Match on the Pro Advantage list (if consent covers ads) plus Search on contractor terms, $600 for 14 days, landing on Contractor Services.",
      confirm="Pro list match rate over 50% and cost per pro order under $25."),
 dict(id="S2", name="Property managers and building maintenance", kind="Known when they have accounts; findable by business listings", flag="EXPLORE",
      real=[f"{est('531311 Residential property managers') + est('531312 Nonresidential property managers'):,} property management firms and {est('561720 Janitorial services') + est('561790 Other building services'):,} janitorial and building-service firms in the two counties (BLS, Q1 2025)",
            "N95 10-packs are deep at every store: 123 Santa Rosa, 80 Petaluma, 109 Sonoma, 59 Ukiah (Oct 19)"],
      sim=["Business accounts tagged as property management: 186", "Average business order: $412"],
      why="Storm prep and smoke duty of care across many units at once: filters, N95s, sandbags, gutter guard. Bigger orders per decision maker.",
      products=["2000038308", "273401136", "2000002407", "4314103", "2298786"],
      test="Search plus a Meta lead form for property managers in the four trade areas, $500 for 21 days, offering a bulk quote from the Pro Desk.",
      confirm="10 or more bulk quote requests, with at least 3 converting."),
 dict(id="S3", name="Landscapers and gardeners (pro)", kind="Known: pro accounts; findable by business listings", flag="EXPLORE",
      real=[f"{est('561730 Landscaping services'):,} landscaping firms with {emp('561730 Landscaping services'):,} employees, plus {est('111421 Nursery and tree production')} nurseries (BLS, Q1 2025)",
            "Soil stock is deep: Redi-Gro planting mix 158 at Santa Rosa and 109 at Ukiah; Redi-Gro bark mulch 93 to 147 per store (Oct 19)"],
      sim=["Landscaper accounts: 410", "Fall soil purchases by landscapers: 22% of soil units"],
      why="Fall planting is their busy season and soil is the deepest stock Friedman's carries. Drive-thru yard pickup suits pro volume.",
      products=["502203569", "2000002880", "2000030180", "2000035127"],
      test="Customer Match plus Meta to landscaping businesses, $400 for 21 days, with a pallet-quantity offer if the Weekly Ad allows.",
      confirm="Average order of 20 or more bags; cost per order under $30."),
 dict(id="S4", name="Home gardeners", kind="Known: Get Growing and email subscribers", flag="COVERED",
      real=["Google Trends 'compost' in the Bay Area holds steady at 10 to 11 each Oct to Nov, peaking in spring (Trends, 2023 to 2026)"],
      sim=["Email subscribers who opened a garden email in the last 90 days: 9,800"],
      why="Already the core of Fall Planting (C3). Adding a lookalike of engaged garden subscribers is the only new idea here.",
      products=["2000030180", "2000002880", "2000035127"],
      test="Fold into C3 as a lookalike audience line; no separate budget.", confirm="Lookalike ROAS within 15% of C3's Meta line."),
 dict(id="S5", name="Frequent DIYers", kind="Known: loyalty and email purchase history", flag="WATCH",
      real=["No public data identifies frequent DIYers; this one rests entirely on Friedman's own purchase history"],
      sim=["Households with 6 or more visits in 12 months: 7,300", "They buy across 4.1 departments on average"],
      why="Likely the best responders to every campaign, but sizing and targeting depend on POS data the demo doesn't have.",
      products=["2000023397", "2000023418", "1575334", "209001271"],
      test="When POS data is connected: a retargeting line across C1 to C3 for this group, measured against everyone else.",
      confirm="Needs real visit-frequency data before it can be scored."),
 dict(id="S6", name="New home buyers", kind="Findable: new movers", flag="EXPLORE",
      real=[f"{H['attom']['sales_12mo']:,} Sonoma County home sales in the 12 months to mid-2025, about {round(H['attom']['sales_12mo']/12):,} a month; {H['attom']['june_2025_purchase_loans']} purchase loans in June 2025 alone (ATTOM)",
            f"{round(100 - H['census']['same_house_1yr_pct'], 1)}% of Sonoma County residents moved in the past year (Census, ACS 2020 to 2024)",
            "Google Ads and Meta both offer 'recently moved' audiences, and USPS new-mover lists are sold commercially"],
      sim=["New-mover households in the four trade areas this fall: about 1,100", "First-year movers spend 2.2x the average on home improvement"],
      why="First winter in an unfamiliar house: weatherstripping, faucet covers, filters, gutter guard. A welcome-to-the-neighborhood offer builds a long relationship.",
      products=["2000023397", "2000023418", "209001271", "273401136", "2298786"],
      test="Search and Meta 'recently moved' audiences in the four trade areas, $500 for 30 days, landing on a First Winter checklist built by the content agent.",
      confirm="Cost per first order under $35, and 20% of buyers return within 60 days."),
]
for sg in segments:
    sg["items"] = [dict(item=i, name=P[i]["name"], price=P[i]["price"], stock=P[i]["stock"]) for i in sg["products"]]
    sg["thin"] = [i["name"] for i in sg["items"] if min(i["stock"].values()) < 5]

# ---- Reports ----
def agg(hrs):
    out = {}
    for h in sim["hours"]:
        if h["h"] not in hrs: continue
        for l in h["lines"]:
            k = l["cid"] + "|" + l["ch"]; o = out.setdefault(k, dict(cid=l["cid"], ch=l["ch"], spend=0, impr=0, clicks=0, views=0, carts=0, orders=0, revenue=0))
            for f in ("spend", "impr", "clicks", "views", "carts", "orders", "revenue"): o[f] += l[f]
    return [o for o in out.values() if o["spend"] > 0]
PERIODS = [("6 a.m. report", "10 p.m. Fri to 6 a.m. Sat", [22, 23, 0, 1, 2, 3, 4, 5]), ("2 p.m. report", "6 a.m. to 2 p.m. Sat", list(range(6, 14))),
           ("10 p.m. report", "2 p.m. to 10 p.m. Sat", list(range(14, 22)))]
reports = [dict(title=t, window=w, rows=agg(set(h))) for t, w, h in PERIODS]
ttd = {t["cid"] + "|" + t["ch"]: t for t in sim["ttd"]}
BE = 1 / (proj["margin"] * (1 - proj["returns"]))
def r(k): t = ttd[k]; return t["revenue"] / t["spend"]
def ac(k): t = ttd[k]; return t["carts"] / t["clicks"] * 100
def base(cid, ch): c = [x for x in proj["campaigns"] if x["id"] == cid][0]; return [l for l in c["lines"] if l["ch"] == ch][0]["proj"]["base"]["roas"]
NARR = dict(
 headline=[
  "Overnight was quiet as expected. Gutter Gear and Fall Planting are ahead of plan on test-to-date ROAS; Storm Ready Meta is on plan; Nextdoor is below break-even but still too small to judge.",
  "Morning traffic came in on plan. Gutter Gear Search is the strongest line in the test. A smoke advisory for the Ukiah area is expected this afternoon; the agent is watching AQI.",
  "AQI turned unhealthy in the Ukiah area at 1 p.m. The approved Clean Air standby went live there, and Fall Planting outdoor creative paused there. Spend stayed under every cap. Three adjustments are waiting for your approval."],
 working=[
  f"Gutter Gear, Google Search: ROAS {r('C1|search'):.2f} on {ttd['C1|search']['clicks']:.0f} clicks vs projected base {base('C1','search'):.2f}; {ttd['C1|search']['p_above_be']}% chance it's truly above break-even.",
  f"Fall Planting, Meta: ROAS {r('C3|meta'):.2f} on {ttd['C3|meta']['clicks']:.0f} clicks; {ttd['C3|meta']['p_above_be']}% chance above break-even.",
  f"Storm Ready, Meta: ROAS {r('C2|meta'):.2f} in its first 4 days, on plan."],
 notworking=[
  f"Storm Ready, Nextdoor: ROAS {r('C2|nextdoor'):.2f} on {ttd['C2|nextdoor']['clicks']:.0f} clicks, below break-even ({BE:.2f}). Under 100 clicks, so this is early, not a verdict.",
  f"Fall Planting, TikTok: only {ac('C3|tiktok'):.1f}% of clicks add to cart vs {ac('C3|meta'):.1f}% on Meta; {ttd['C3|tiktok']['p_above_be']}% chance above break-even."],
 funnel=f"Biggest leak: Fall Planting TikTok, click to add to cart ({ac('C3|tiktok'):.1f}% vs {ac('C3|meta'):.1f}% on Meta). Likely cause: the video sends people to a long blog post on a phone; Meta's top variant links straight to the estimator. Fix: point TikTok to the Garden Soil category with store pickup (ADJ-2).",
 forces=["Ukiah area AQI reached Unhealthy at 1 p.m. (SIMULATED event, modeled on the Oct 16 to 19 Cooley Fire smoke).",
         "NWS: dry through Monday, next rain chance midweek (SIMULATED for Oct 31). Gutter Gear and Storm Ready bursts set to start 48 hours before the next rain."],
 protective=[
  dict(time="9:00 a.m.", action="Stock-out pause: Frost King gutter scoop removed from Sonoma ads (0 on hand). Resumes on its own when restocked.", camp="C1"),
  dict(time="1:00 p.m.", action="Safety pause: Fall Planting outdoor creative paused in the Ukiah area while AQI is Unhealthy. Resuming needs approval (ADJ-3). The pre-approved Clean Air standby (C5) started in the same area under its approved trigger and caps.", camp="C3, C5")],
)
CTRB = {"search": (6.47, "WordStream 2026, Home & Home Improvement"), "pmax": (1.41, "FoundryCRO 2026, Home & Garden Shopping"),
        "meta": (1.76, "WordStream 2026 via Coupler.io, Home & Home Improvement"), "tiktok": (1.77, "Whatagraph 2026"), "nextdoor": (None, "No public benchmark")}
STAGEB = {"view": 82, "order": 40}   # ASSUMPTION benchmarks for click->product view and cart->order
CVRB = {l["ch"]: l["proj"]["base"]["cvr"] for c in proj["campaigns"] for l in c["lines"]}
def funnel(k):
    t = ttd[k]; ch = t["ch"]
    rows = [("Impression to click (CTR)", t["clicks"] / t["impr"] * 100, CTRB[ch][0], CTRB[ch][1]),
            ("Click to product view", t["views"] / t["clicks"] * 100, STAGEB["view"], "Agent assumption"),
            ("Product view to add to cart", t["carts"] / t["views"] * 100, round(CVRB[ch] / (0.82 * 0.40) * 100, 1), "Implied by the channel's conversion benchmark"),
            ("Add to cart to order", t["orders"] / max(t["carts"], .1) * 100, STAGEB["order"], "Agent assumption")]
    out = []
    for name, act, bench, src in rows:
        st = "n/a" if bench is None else ("OK" if act >= bench * 0.9 else "LOW" if act >= bench * 0.6 else "PROBLEM")
        out.append(dict(stage=name, actual=round(act, 2), bench=bench, src=src, status=st))
    return out
ADJ = [
 dict(id="ADJ-1", camp="C1", line="C1|search", change="Raise Gutter Gear Search daily cap 15% (about $14 a day) for the remaining 10 days, from the reserve.",
      why=f"ROAS {r('C1|search'):.2f} on {ttd['C1|search']['clicks']:.0f} clicks vs break-even {BE:.2f}; {ttd['C1|search']['p_above_be']}% chance above break-even.",
      stage="None: every stage is at or above benchmark. The limit is budget.",
      diagnosis="Budget-limited, not demand-limited. Ads stop serving by mid-afternoon on rain-forecast days while searches keep coming (simulated: 38% of impressions lost to budget on those days).",
      causes=["Daily cap sized for an average day, but rain days bring two to three times the searches", "Strong conversion (above the 3.5% benchmark) means each extra click is likely profitable"],
      remediation=["Raise the Search daily cap 15% from the reserve for 10 days", "Shift spend toward 6 a.m. to 9 p.m. when pickup is possible", "Keep the 48-hour rain bursts; the extra cap only applies on forecast days",
                   "Hold the raise at any store where Amerimax gutter guard delivery isn't confirmed by Purchasing"],
      success="ROAS stays above 3.3x (1.2x break-even) and impression share lost to budget falls under 15%.",
      confidence="High", effect="About $143 more spend; projected extra revenue $500 to $640 at current ROAS.", undo="Return the cap to the approved amount."),
 dict(id="ADJ-2", camp="C3", line="C3|tiktok", change="Point Fall Planting TikTok ads to the Garden Soil category page with store pickup, instead of the blog post, for a 3-day test.",
      why=f"Add-to-cart rate {ac('C3|tiktok'):.1f}% of clicks vs {ac('C3|meta'):.1f}% on Meta.",
      stage="Product view to add to cart (and some loss from click to view).",
      diagnosis="Landing page mismatch on phones. People tap a short video and land on a long blog post; few scroll to the products, and some leave before it loads.",
      causes=["The blog post is long on a phone; products sit below several screens of how-to", "Video viewers expect a shopping page, not an article", "Slower page load than the category page (simulated)"],
      remediation=["Send TikTok clicks to the Garden Soil category page with store pickup selected", "Add on-screen text in the last 3 seconds: 'Pickup today at your Friedman's'",
                   "Split 50/50 for 3 days: category page vs the blog post's estimator section", "Keep the blog post for Meta, where it converts"],
      success="Add-to-cart rate of 5% or more of clicks, and ROAS above 2.77x after 150 more clicks.",
      confidence="Medium", effect="No added spend. If add-to-cart doubles, TikTok ROAS projects above break-even.", undo="Switch the URL back."),
 dict(id="ADJ-3", camp="C3", line="C3|meta", change="Resume Fall Planting outdoor creative in the Ukiah area once AQI is back to Moderate for 6 hours in a row.",
      why="Protective pause at 1 p.m. for unhealthy air. Resuming after a safety pause needs your approval.",
      stage="None: a safety pause, not a funnel problem.",
      diagnosis="Smoke, not performance. The line was healthy before the pause; Clean Air Indoors is covering the Ukiah area meanwhile.",
      causes=["AQI reached Unhealthy in the Ukiah area at 1 p.m. (simulated)"],
      remediation=["Resume automatically once AQI is Moderate for 6 hours in a row", "Open with indoor-friendly creative first (soil and mulch for when the air clears)",
                   "Optional: move Ukiah's paused share to the other three stores until it resumes (adds no spend)"],
      success="Ukiah's Fall Planting ROAS returns to within 15% of its pre-pause level within 2 days.",
      confidence="High", effect="Restores about 22% of the line's daily reach.", undo="Pause again."),
 dict(id="ADJ-4", camp="C2", line="C2|nextdoor", change="Hold Nextdoor at current budget until it passes 100 clicks, then decide. Approve the new store-specific post to test meanwhile.",
      why=f"Below break-even, with a {ttd['C2|nextdoor']['p_above_be']}% chance it's truly above, but on only {ttd['C2|nextdoor']['clicks']:.0f} clicks.",
      stage="Impression to click, then add to cart to order.",
      diagnosis="Weak hook and a thin sample. Click rate is about half of Meta's for the same offer, and only 1 order so far, so the data can't separate a bad channel from a bad post.",
      causes=["Generic preparedness copy reads like an ad, not a neighbor's tip", "No store name or local detail; Nextdoor rewards local relevance", "Too few clicks to judge conversion"],
      remediation=["Keep the budget flat; no added spend", "Swap in a store-specific post: 'Sandbags are in stock at Friedman's Petaluma' with a fill-and-stack tip (see Ad samples)",
                   "Decide at 100 clicks: keep if ROAS is at or above 2.77x, otherwise move the remaining Nextdoor budget to Storm Ready Meta"],
      success="Click rate above 1.3% and ROAS at or above 2.77x by 100 clicks.",
      confidence="Low (small sample)", effect="No change in spend.", undo="Not applicable."),
]
for a in ADJ: a["funnel"] = funnel(a["line"])
# ---- Store-level split of test-to-date results (SIMULATED), for the dashboard ----
import random as _r
_r.seed(80)
STORE_F = {("C1","Petaluma"):1.15,("C1","Ukiah"):0.85,("C3","Sonoma"):0.75,("C3","Ukiah"):0.8,("C3","Petaluma"):1.1,("C2","Santa Rosa"):1.1,("C2","Ukiah"):0.9}
store_perf = []
for t in sim["ttd"]:
    g = GEO[t["cid"]]
    shares = {s: (1.0 if s == "Ukiah" else 0.0) for s in STORES} if t["cid"] == "C5" else {s: g[s] / 100 * _r.uniform(.9, 1.1) for s in STORES}
    tot = sum(shares.values()); shares = {s: v / tot for s, v in shares.items()}
    raw = {s: shares[s] * STORE_F.get((t["cid"], s), 1.0) * _r.uniform(.92, 1.08) for s in STORES}
    rtot = sum(raw.values())
    for s in STORES:
        if shares[s] == 0: continue
        store_perf.append(dict(cid=t["cid"], ch=t["ch"], store=s, spend=round(t["spend"] * shares[s], 2), clicks=round(t["clicks"] * shares[s], 1),
                               orders=round(t["orders"] * raw[s] / rtot, 2), revenue=round(t["revenue"] * raw[s] / rtot, 2)))

# ---- Learnings library: one record per campaign line, for next season's planning (SIMULATED results, REAL conditions) ----
LESSONS = {
 "C1|search": ["Rain-timed bursts drove the best returns of the test; on forecast days the daily cap, not demand, was the limit.",
               "Gutter guard sells fast right before the first rain (Santa Rosa sold 13 sections between Oct 18 and 19). Confirm inbound before the first storm."],
 "C1|pmax": ["Local inventory ads kept out-of-stock items out of ads automatically (gutter scoop at Sonoma)."],
 "C2|meta": ["Waiting for the wet/dry vac restock pushed launch to Oct 28 with no loss of return. Next fall, order vacs by early October."],
 "C2|nextdoor": ["Generic preparedness copy drew half of Meta's click rate. Test store-specific posts from day one."],
 "C3|meta": ["The estimator link was the top variant. Sonoma's compost stockout cut reach there; stock Sonoma compost before the season starts."],
 "C3|tiktok": ["Video traffic sent to a long blog post lost shoppers on the phone. Send video clicks to a category page with store pickup."],
 "C5|search": ["The smoke standby went live within the hour of the trigger. Early returns were strong but on a small sample."],
 "C5|meta": ["Calm, no-fire creative worked on smoke days. Keep the standby every fire season."],
}
ADJMAP = {"C1|search": ["ADJ-1"], "C3|tiktok": ["ADJ-2"], "C3|meta": ["ADJ-3"], "C2|nextdoor": ["ADJ-4"]}
learn = []
for k, t in ttd.items():
    c = [x for x in proj["campaigns"] if x["id"] == t["cid"]][0]; l = [x for x in c["lines"] if x["ch"] == t["ch"]][0]
    roas = t["revenue"] / t["spend"]; p = t["p_above_be"]
    verdict = "Too early" if t["clicks"] < 100 or t["days"] < 3 else "Success" if p >= 90 else "Mixed" if p >= 60 else "Fail"
    learn.append(dict(id=f"L-{t['cid']}-{t['ch']}", cid=t["cid"], campaign=c["name"], channel=l["label"], season="Fall, Oct 19 to Nov 15",
        conditions=dict(enso="Very strong El Niño (NOAA CPC)", window_rain="Forecast: showers Oct 20 to 22 (NWS); season result recorded at the end",
                        smoke_days="1 (simulated, Oct 31)", promo="Pro Tool Days Oct 19 to 25 (Weekly Ad)",
                        stock=[f"{f['name'].split(',')[0]} ran short before delivery at " + ", ".join(x["store"] for x in f["stores"] if x["late"]) for f in flags if f["cid"] == t["cid"] and any(x["late"] for x in f["stores"])]),
        projected=dict(roas=l["proj"]["base"]["roas"], cpc=l["proj"]["base"]["cpc"], cvr=round(l["proj"]["base"]["cvr"] * 100, 2), aov=c["aov"]),
        actual=dict(days=t["days"], spend=round(t["spend"]), clicks=round(t["clicks"]), orders=round(t["orders"], 1), revenue=round(t["revenue"]), roas=round(roas, 2),
                    cpc=round(t["spend"] / t["clicks"], 2), cvr=round(t["orders"] / t["clicks"] * 100, 2), aov=round(t["revenue"] / max(t["orders"], .1), 2), p_above_be=p),
        verdict=verdict, adjustments=ADJMAP.get(k, []), lessons=LESSONS.get(k, []),
        reuse=("Start next fall from these actual CPC, conversion and basket numbers instead of benchmarks" if verdict in ("Success", "Mixed")
               else "Don't reuse as a starting point yet; rerun as a test with the fix applied")))
learn.append(dict(id="L-C4-owned", cid="C4", campaign="Winterize Before The Frost", channel="Email and SMS", season="Fall, Nov 1 to Dec 15",
    conditions=dict(note="Runs on frost forecasts; first frost history: Oct 27 (2023), Nov 16 (2024), Dec 12 (2025) at Ukiah or Santa Rosa (NOAA)"),
    projected=dict(note="Paid search projected below break-even (1.33x), so owned channels only"), actual=None, verdict="Not started",
    adjustments=[], lessons=["Low-basket seasonal items belong in owned channels unless paid return clears break-even."],
    reuse="Record SMS and email response rates to replace the alert assumptions (4% and 1.5% click, 6% and 3% conversion)."))
season = ["El Niño alone did not predict Oct to Nov demand in 2023; actual rain did. Plan a normal baseline and trigger bursts from forecasts.",
          "Stock was the binding constraint more often than budget: gutter guard everywhere, compost at Sonoma, vacs and lanterns at every store.",
          "Store-specific, local copy beat generic copy where tested (Nextdoor test pending)."]

json.dump(dict(learn=learn, season_lessons=season, store_perf=store_perf, geo=GEO, demo=DEMO, checks=checks, flags=flags, confirm=confirm, segments=segments, reports=reports, narr=NARR, adj=ADJ, be=BE), sys.stdout)
