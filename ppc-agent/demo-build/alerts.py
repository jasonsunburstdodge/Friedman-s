"""Opportunity alert rules + a live scan of the real NWS forecasts/alerts captured Oct 19 2026.
Run: python3 alerts.py > alerts.json"""
import json
AL = json.load(open("real_alert_inputs.json"))

OWNED = dict(  # ASSUMPTIONS until Friedman's own SMS/email results exist
    sms=dict(label="SMS to opted-in customers", click=0.04, conv=0.06, cost_per_msg=0.015),
    email=dict(label="Email to opted-in customers", click=0.015, conv=0.03, cost_per_msg=0.0))

RULES = {
 "frost": dict(name="Frost Tonight", icon="FROST", lift=1.5,
   triggers=["NWS Frost Advisory or Freeze Warning for a store's zone", "Forecast low of 34°F or colder at a store (watch level at 35 to 36°F)"],
   basket=[["209001271", 2], ["2000020586", 1], ["1575334", 4]],
   alts={"2000020586": "2000048801", "1575334": "205801070", "209001271": "209001007"},
   paid=[["search", 150], ["meta", 100]], owned=["sms", "email"],
   terms=["frost cloth", "plant frost cover", "faucet cover", "pipe insulation", "protect pipes from freezing"],
   creative=["FROST TONIGHT / Cover Faucets And Tender Plants Before Dark / SHOP FROST PROTECTION",
             "SMS: Frost tonight in {area}. Cover outdoor faucets and tender plants before dark. Pickup ready at Friedman's {store}: [link] Reply STOP to opt out."],
   window="From approval (target 2 p.m.) until 10 a.m. the next morning",
   safety=["Never suggest open flames, grills or unvented heaters to warm pipes or plants", "Point to the main water shutoff only in a calm how-to tone, linking the winterize post"],
   ops=["Move faucet covers, frost blankets and pipe insulation to the front endcap at affected stores by 3 p.m.",
        "Google Business Profile post for each affected store (no prices)",
        "Ask the content agent for a 3-step 'frost tonight' tip for Ask The Pro and the homepage banner"]),
 "storm": dict(name="Severe Storm Prep", icon="STORM", lift=1.3,
   triggers=["NWS Severe Thunderstorm Watch or Warning, High Wind Warning or Wind Advisory for a store's zone", "Forecast mentions thunderstorms with a 40% or higher chance (watch level)"],
   basket=[["300601171", 2], ["2000034790", 1], ["158601804", 1], ["2000031875", 1]],
   alts={"2000034790": "2000000712", "300601171": "2330121"},
   paid=[["search", 250], ["meta", 200]], owned=["sms", "email"],
   terms=["tarp", "battery lantern", "roof leak patch", "storm supplies", "flashlight batteries"],
   creative=["STORMS ON THE WAY / Tarps, Lanterns And Batteries Ready For Pickup / SHOP STORM PREP",
             "After the storm: CLEANUP STARTS HERE / Tarps, Roof Patch And Wet/Dry Vacs / SHOP STORM CLEANUP"],
   window="Prep phase from approval until the warning starts; paused during the warning; cleanup phase for 48 hours after",
   safety=["Pause all ads while a Severe Thunderstorm Warning is in effect: people should be sheltering, not shopping",
           "Never show anyone on a roof or ladder in wind or rain; roof repairs at height go to a licensed roofer",
           "No fear lines; calm, helpful tone only"],
   ops=["Stage tarps, lanterns and batteries near the front at affected stores",
        "Pro Desk heads-up: contractors will call for tarps and roof patch after the storm",
        "GBP post for each affected store; cleanup phase post after the storm"]),
 "flood": dict(name="Flood Watch Ready", icon="FLOOD", lift=1.4,
   triggers=["NWS Flood Watch or Flash Flood Watch for a store's zone", "Forecast of 1 inch or more of rain in 24 hours"],
   basket=[["4314103", 20], ["2000054322", 1], ["2295031", 2], ["300601171", 1]],
   alts={"300601171": "2330121"},
   paid=[["search", 250], ["meta", 200], ["nextdoor", 100]], owned=["sms", "email"],
   terms=["sandbags near me", "wet dry vac", "downspout extension", "flood prep supplies"],
   creative=["BEFORE THE WATER RISES / Sandbags, Drainage And Wet/Dry Vacs / SHOP FLOOD PREP",
             "Nextdoor: Sandbags are in stock at Friedman's {store}. Fill them 1/2 to 2/3 full and lay them like bricks."],
   window="From approval until the watch ends; stops automatically if it becomes a Flood Warning in that zone",
   safety=["Never advertise into an area under a Flood Warning or evacuation order",
           "Include 'Turn around, don't drown' in any flood content; never suggest driving through water"],
   ops=["Sandbag pallets to the front lot at affected stores", "Check Drive-Thru Pickup staffing for the watch window", "GBP post per affected store"]),
 "outage": dict(name="Power Outage Ready", icon="OUTAGE", lift=1.3,
   triggers=["NWS Red Flag Warning or High Wind Warning with a utility Public Safety Power Shutoff notice for a store's area"],
   basket=[["2000034790", 1], ["158601804", 1], ["2000049272", 1]],
   alts={"2000034790": "2000000712"},
   paid=[["search", 150], ["meta", 150]], owned=["sms", "email"],
   terms=["battery lantern", "rechargeable flashlight", "AA batteries", "power outage supplies"],
   creative=["READY FOR AN OUTAGE / Lanterns, Flashlights And Batteries / SHOP OUTAGE PREP"],
   window="From the shutoff notice until power is restored",
   safety=["No fire imagery and no fear lines", "Never advertise into an evacuation zone", "If generators are added, every ad and post carries carbon monoxide safety: outdoors only, away from windows"],
   ops=["Lanterns and batteries to the registers at affected stores", "GBP post per affected store with store hours if they change"]),
 "smoke": dict(name="Smoke Day", icon="SMOKE", routed="C5",
   triggers=["AirNow AQI Unhealthy for Sensitive Groups or worse in a trade area"],
   note="Handled by the pre-approved Clean Air Indoors standby (C5), within its approved caps."),
 "rain": dict(name="Rain In The Forecast", icon="RAIN", routed="C1",
   triggers=["Rain chance of 40% or higher within 72 hours after a dry stretch"],
   note="Handled by Gutter Gear's approved 48-hour burst trigger (C1), within its approved caps."),
}

# ---- live scan of the real Oct 19 NWS data ----
live = []
rain_hits, storm_hits, lows = [], [], {}
for store, d in AL["nws"].items():
    lows[store] = min(p[2] for p in d["periods"] if "Night" in p[0] or p[0] == "Tonight")
    for name, day, temp, pop, short in d["periods"]:
        if pop and pop >= 40 and "Rain" in short or (pop and pop >= 40 and "Showers" in short):
            rain_hits.append((store, name, pop))
        if "Thunderstorm" in short and (pop or 0) >= 40:
            storm_hits.append((store, name, pop, short))
    if d["alerts"]:
        live.append(dict(kind="nws", store=store, alerts=d["alerts"]))
first = {}
for s, n, p in rain_hits: first.setdefault(s, (n, p))
live.append(dict(rule="rain", level="Routed", stores=sorted(first),
                 evidence=[f"{s}: {n} {p}% chance of showers (NWS {AL['nws'][s]['office']} zone {AL['nws'][s]['zone']})" for s, (n, p) in first.items()]))
for s, n, p, short in storm_hits:
    live.append(dict(rule="storm", level="Watch", stores=[s], evidence=[f"{s}: {n}, {short}, {p}% chance (NWS {AL['nws'][s]['office']} zone {AL['nws'][s]['zone']})", "No Severe Thunderstorm Watch or Warning is in effect"],
                     when=n))
minlow = min(lows.values())
live.append(dict(rule="frost", level="None", stores=[], evidence=[f"Coldest forecast low through Sunday: {minlow}°F ({', '.join(f'{k} {v}°F' for k, v in lows.items())}). Frost rule needs 34°F or colder."]))
live.append(dict(rule="nws_alerts", level="None", stores=[], evidence=["No active NWS alerts for any of the four stores' points as of the scan"]))

SIMS = [
 dict(rule="frost", level="Alert", stores=["Ukiah", "Sonoma"], label="Frost Advisory tonight: Ukiah and Sonoma Valley",
      evidence=["SIMULATED: NWS Frost Advisory, 1 a.m. to 9 a.m., lows 30 to 34°F in Southern Mendocino Interior and North Bay Interior Valleys"]),
 dict(rule="storm", level="Alert", stores=["Santa Rosa", "Petaluma"], label="Severe Thunderstorm Watch: Santa Rosa and Petaluma",
      evidence=["SIMULATED: NWS Severe Thunderstorm Watch until 10 p.m., gusts to 60 mph and small hail possible"]),
 dict(rule="flood", level="Alert", stores=["Petaluma", "Sonoma"], label="Flood Watch: Petaluma and Sonoma",
      evidence=["SIMULATED: NWS Flood Watch Thursday night through Saturday, 2 to 4 inches of rain with an atmospheric river"]),
 dict(rule="outage", level="Alert", stores=["Ukiah", "Santa Rosa"], label="Red Flag Warning and power shutoff notice: Ukiah and Santa Rosa",
      evidence=["SIMULATED: NWS Red Flag Warning with a utility Public Safety Power Shutoff notice for parts of both trade areas"]),
 dict(rule="smoke", level="Alert", stores=["Ukiah"], label="Smoke: AQI Unhealthy in the Ukiah area", evidence=["SIMULATED: AirNow AQI 158 (Unhealthy)"]),
]
print(json.dumps(dict(rules=RULES, owned=OWNED, live=live, sims=SIMS, scanned=AL["asof"], nws_source=AL["nws_source"], forecasts=AL["nws"])))
