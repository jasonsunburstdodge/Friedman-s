"""Calibrated simulation (v2). What can't be read publicly is simulated, but tied to real inputs:
 - weekly unit rate per item per store = REAL on-hand (Oct 19) / 8 weeks of supply (ASSUMPTION)
 - year-to-year shape = REAL Google Trends (SF Bay Area DMA) + REAL NOAA rain and frost for the Oct 19 to Nov 15 window
 - one day of hourly ad results, plus test-to-date, with Monte Carlo odds of beating break-even
Run: python3 sim.py projections.json products_all.json trends_batch1.json real_weather.json > sim.json
"""
import json, sys, random, statistics as st
random.seed(1946)
proj = json.load(open(sys.argv[1])); PA = json.load(open(sys.argv[2])); TR = json.load(open(sys.argv[3])); WX = json.load(open(sys.argv[4]))
P = {p["item"]: p for p in PA["products"]}
STORES = ["Santa Rosa", "Petaluma", "Sonoma", "Ukiah"]
WOS = 8  # ASSUMPTION: typical weeks of supply on hand
YEARS = (2023, 2024, 2025)

def trend_window(term):
    w, v = TR["weeks"], TR["values"][term]
    return {y: st.mean([x for d, x in zip(w, v) if f"{y}-10-19" <= d <= f"{y}-11-15"]) for y in YEARS}
def ratio(d):
    m = st.mean(d.values()); return {k: v / m for k, v in d.items()}

rain = {y: st.mean([WX["STS"]["seasons"][f"{y}-{str(y+1)[2:]}"]["window_rain"], WX["UKI"]["seasons"][f"{y}-{str(y+1)[2:]}"]["window_rain"]]) for y in YEARS}
frost_early = {y: min(WX["STS"]["seasons"][f"{y}-{str(y+1)[2:]}"]["first_frost"], WX["UKI"]["seasons"][f"{y}-{str(y+1)[2:]}"]["first_frost"]) for y in YEARS}
tr_tarp, tr_comp, tr_air = ratio(trend_window("tarp")), ratio(trend_window("compost")), ratio(trend_window("air purifier"))
rr = ratio(rain)
IDX = {
 "storm": {y: round(0.6 * tr_tarp[y] + 0.4 * rr[y], 3) for y in YEARS},
 "garden": {y: round(tr_comp[y], 3) for y in YEARS},
 "air": {y: round(tr_air[y], 3) for y in YEARS},
 "frost": {y: (1.3 if frost_early[y] <= f"{y}-11-15" else 1.0 if frost_early[y] <= f"{y}-11-30" else 0.7) for y in YEARS},
}
IDX["seal"] = {y: round(0.5 + 0.5 * IDX["frost"][y], 3) for y in YEARS}
CAT = {"2298786": "storm", "2295031": "storm", "300601171": "storm", "2330121": "storm", "2000054322": "storm", "300101664": "storm",
       "4314103": "storm", "2000023006": "storm", "2000039226": "storm", "2000030180": "garden", "2000002880": "garden", "502203569": "garden",
       "2000035127": "garden", "209001271": "frost", "1575334": "frost", "209001007": "frost", "2000023397": "seal", "2000023418": "seal",
       "2000002404": "air", "2000038308": "air", "2000002407": "air"}
DRIVER = {"storm": "Google Trends 'tarp' (60%) and NOAA window rain at Santa Rosa and Ukiah airports (40%)", "garden": "Google Trends 'compost'",
          "air": "Google Trends 'air purifier'", "frost": "NOAA first frost date: before Nov 15 = 1.3, by Nov 30 = 1.0, later = 0.7",
          "seal": "Half the frost index"}

best = {}
for s in STORES:
    rows = []
    for it, cat in CAT.items():
        p = P[it]; base_wk = max(0.5, p["stock"][s] / WOS)
        if it == "4314103": base_wk = 40  # sandbags: on-hand is pallet stock, not a weekly rate (ASSUMPTION)
        units = {y: int(round(base_wk * 4 * IDX[cat][y] * random.uniform(0.92, 1.08))) for y in YEARS}
        rev3 = round(sum(units.values()) * p["price"])
        rows.append(dict(item=it, name=p["name"], cat=cat, price=p["price"], units=units, rev3=rev3,
                         trend=round((units[2025] / max(1, units[2023]) - 1) * 100)))
    best[s] = rows

# Backtest: forecast 2025 from 2023 and 2024 only, by method, against the simulated 2025 actuals
def mape(pairs): return round(st.mean(abs(f - a) / a for f, a in pairs if a > 0) * 100, 1)
bt = {}
for name, fn in {"Last year (2024)": lambda u: u[2024], "Mean of 2023 and 2024": lambda u: (u[2023] + u[2024]) / 2,
                 "Weighted 60/40, recent first": lambda u: 0.6 * u[2024] + 0.4 * u[2023],
                 "El Niño analog (2023 x category lift)": None}.items():
    pairs_all, pairs_storm = [], []
    for s in STORES:
        for r in best[s]:
            u = r["units"]
            if fn is None:
                f = u[2023]  # 'this year looks like the El Nino year'
            else:
                f = fn(u)
            pairs_all.append((f, u[2025]))
            if r["cat"] == "storm": pairs_storm.append((f, u[2025]))
    bt[name] = dict(all=mape(pairs_all), storm=mape(pairs_storm))
# weather-adjusted: weighted baseline x (2025 window rain / mean of 2023-24 rain) for storm items, known after the fact
pairs = []
for s in STORES:
    for r in best[s]:
        if r["cat"] != "storm": continue
        u = r["units"]; f = (0.6 * u[2024] + 0.4 * u[2023]) * (IDX["storm"][2025] / st.mean([IDX["storm"][2023], IDX["storm"][2024]]))
        pairs.append((f, u[2025]))
bt["Weighted, adjusted for actual rain"] = dict(all=None, storm=mape(pairs))

# Observed one-day sell-through at Santa Rosa (REAL): Oct 18 read vs Oct 19 read; negative = receipts
sell = sorted([dict(item=p["item"], name=p["name"], oct18=p["sr_oct18"], oct19=p["stock"]["Santa Rosa"], delta=p["sr_oct18"] - p["stock"]["Santa Rosa"])
               for p in PA["products"] if p["sr_oct18"] is not None and p["sr_oct18"] != p["stock"]["Santa Rosa"]], key=lambda x: -x["delta"])

# Audiences and search interest (SIMULATED except where noted)
SIZE = {s: sum(P[i]["stock"][s] for i in CAT if i != "4314103") for s in STORES}
tot = sum(SIZE.values())
aud = {s: dict(cust_share=round(SIZE[s] / tot * 100), email=round(52000 * SIZE[s] / tot * random.uniform(.9, 1.1)),
               sms=round(16000 * SIZE[s] / tot * random.uniform(.9, 1.1)), social=round(24000 * SIZE[s] / tot * random.uniform(.9, 1.1))) for s in STORES}

# ---- Monitoring: Sat Oct 31, 2026 (SIMULATED). C1 day 11, C3 day 10, C2 day 4, C5 standby starts 1 p.m. on a smoke day ----
CURVE = [.2,.1,.1,.1,.2,.5,1.2,1.8,2.2,2.3,2.4,2.3,2.2,2.1,2.0,2.0,2.1,2.3,2.4,2.2,1.8,1.3,.8,.4]
FACT = {("C1","search"): (0.92, 1.18), ("C1","pmax"): (1.05, 0.95), ("C2","meta"): (1.0, 1.05), ("C2","nextdoor"): (1.35, 0.7),
        ("C3","meta"): (0.95, 1.1), ("C3","tiktok"): (0.85, 0.55), ("C5","search"): (1.1, 1.6), ("C5","meta"): (1.0, 1.3)}
CTR = {"search": .061, "pmax": .014, "meta": .018, "nextdoor": .009, "tiktok": .024}
lines = []
for c in proj["campaigns"]:
    if c["recommend"].startswith("OWNED"): continue
    for l in c["lines"]:
        daily = l["spend"] / 21 if c["id"] != "C5" else l["spend"] / 6   # C5 budget sized for about 6 smoke days
        lines.append(dict(cid=c["id"], ch=l["ch"], label=l["label"], daily=round(daily, 2), cpc=l["proj"]["base"]["cpc"], cvr=l["proj"]["base"]["cvr"], aov=c["aov"]))
hours = []
for h in range(24):
    row = dict(h=h, lines=[])
    for L in lines:
        f_cpc, f_cvr = FACT[(L["cid"], L["ch"])]
        w = CURVE[h] / sum(CURVE); spend = L["daily"] * w * random.uniform(.85, 1.15); event = None
        if L["cid"] == "C5":
            if h < 13 or h > 21: spend = 0
            else: spend = L["daily"] * CURVE[h] / sum(CURVE[13:22]) * random.uniform(.85, 1.15); event = "smoke standby live (Ukiah area)"
        if L["cid"] == "C3" and 13 <= h <= 21: spend *= 0.78; event = "smoke pause (Ukiah area)"
        cpc = L["cpc"] * f_cpc * random.uniform(.92, 1.08); clicks = spend / cpc if spend else 0
        views = clicks * (0.82 if L["ch"] != "tiktok" else 0.71)
        orders = clicks * L["cvr"] * f_cvr
        carts = views * 0.045 if L["ch"] == "tiktok" else views * 0.11 if L["ch"] == "nextdoor" else orders / 0.40
        row["lines"].append(dict(cid=L["cid"], ch=L["ch"], spend=round(spend, 2), impr=round(clicks / (CTR[L["ch"]] * random.uniform(.9, 1.1))) if clicks else 0,
                                 clicks=round(clicks, 2), views=round(views, 2), carts=round(carts, 3), orders=round(orders, 3), revenue=round(orders * L["aov"], 2), event=event))
    hours.append(row)
LIVE = {"C1": 11, "C2": 4, "C3": 10, "C5": 1}
ttd = []
for i, L in enumerate(lines):
    totd = {f: 0.0 for f in ("spend", "impr", "clicks", "views", "carts", "orders", "revenue")}
    day = {f: sum(h["lines"][i][f] for h in hours) for f in totd}
    for d in range(LIVE[L["cid"]]):
        k = random.uniform(.8, 1.2)
        for f in totd: totd[f] += day[f] * (k if f != "spend" else random.uniform(.93, 1.02))
    ttd.append(dict(cid=L["cid"], ch=L["ch"], days=LIVE[L["cid"]], aov=L["aov"], **{f: round(v, 2) for f, v in totd.items()}))

# Monte Carlo: chance each line's true ROAS beats break-even, given clicks and orders so far
BE = 1 / (proj["margin"] * (1 - proj["returns"]))
for t in ttd:
    C, O, cpc = t["clicks"], round(t["orders"]), t["spend"] / max(1, t["clicks"])
    wins = 0
    for _ in range(4000):
        prior_cvr = [l for l in lines if l["cid"] == t["cid"] and l["ch"] == t["ch"]][0]["cvr"]
        cvr = random.gammavariate(O + 100 * prior_cvr, 1 / (C + 100))   # posterior: benchmark rate worth 100 clicks of prior
        aov = t["aov"] * random.uniform(0.85, 1.15)
        if cvr * aov / cpc > BE: wins += 1
    t["p_above_be"] = round(wins / 4000 * 100)

json.dump(dict(stores=STORES, best=best, idx=IDX, driver=DRIVER, trend_window={k: trend_window(k) for k in ("tarp", "compost", "air purifier")},
               rain=rain, frost=frost_early, backtest=bt, sell=sell, aud=aud, stock={p["item"]: p["stock"] for p in PA["products"]},
               lines=lines, hours=hours, ttd=ttd, wos=WOS), sys.stdout)
