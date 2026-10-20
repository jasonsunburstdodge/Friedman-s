"""Assemble the demo: python3 build.py assets.json > ../index.html"""
import json, sys
A = json.load(open(sys.argv[1]))
proj = json.load(open("projections.json")); sim = json.load(open("sim.json")); der = json.load(open("derived.json"))
prods = json.load(open("products_all.json"))["products"]
trends = json.load(open("trends_batch1.json"))
alerts = json.load(open("alerts.json"))
used = {p["item"] for p in prods}
imgs = {k: v for k, v in A["imgs"].items() if k in used}

CPC = "https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso_disc_oct2026/ensodisc.shtml"
GOV = "https://www.gov.ca.gov/2026/09/21/governor-newsom-proclaims-state-of-emergency-to-bolster-statewide-el-nino-preparedness-protect-california/"
WINTER = "https://watchers.news/2026/10/16/very-strong-el-nino-favors-wetter-south-and-warmer-north-in-noaas-2026-27-winter-outlook-u-s/"
NWS = "https://forecast.weather.gov/product.php?site=mtr&issuedby=MTR&product=AFD"
SFC = "https://www.sfchronicle.com/weather-forecast/article/bay-area-rain-cold-22482791.php"
COOLEY = "https://www.pressdemocrat.com/2026/10/16/cooley-fire-prescribed-burn-sonoma-mendocino/"
COOLEY2 = "https://www.sonomanews.com/2026/10/19/cooley-fire-smoke-sonoma/"
CARR = "https://www.pressdemocrat.com/2026/10/10/sonoma-county-prescribed-burn-explainer/"

forces = [
 dict(t="A very strong El Niño", hl=True, status="Real", asof="Oct 8, 2026 (NOAA CPC); Oct 15 winter outlook",
      ev="NOAA's Climate Prediction Center keeps an El Niño Advisory: a strong-to-very strong event is likely through January to March 2027, with an 83% chance October to December reaches record strength. NOAA's winter outlook favors a wetter-than-average California.",
      adj="Real local data says El Niño alone doesn't lift fall sales: the 2023-24 El Niño season was drier at Santa Rosa than 2022-23, and Bay Area tarp searches didn't rise that Oct to Nov. Storm bundles stay ready, and each forecast storm triggers a 48-hour burst instead of front-loading spend.",
      src=[["NOAA CPC ENSO discussion, Oct 8", CPC], ["NOAA winter outlook coverage, Oct 16", WINTER], ["NOAA ACIS station data", "https://data.rcc-acis.org/"], ["Google Trends, Bay Area", "https://trends.google.com/trends/explore?date=2023-01-01%202026-10-18&geo=US-CA-807&q=gutter%20guard,tarp,compost,sandbags,air%20purifier"]]),
 dict(t="State of emergency for El Niño", status="Real", asof="Sep 21, 2026",
      ev="Governor Newsom proclaimed a statewide emergency to prepare for El Niño storms, flooding and landslides, and urged Californians to make plans.",
      adj="Context only. Ads stay helpful and calm; the agent never uses the emergency as a scare line.",
      src=[["Governor's office, Sep 21", GOV]]),
 dict(t="First rain this week", status="Real", asof="Oct 18 to 19, 2026",
      ev="NWS expects light showers Tuesday through Thursday; the North Bay may see up to a quarter inch, less than the rest of the Bay Area. It may be the most rain since April.",
      adj="Gutter Gear's first burst starts Oct 21, ahead of the showers, and pauses during heavy rain. Fall Planting targets the weekend after, when soil is workable.",
      src=[["NWS Bay Area forecast discussion, Oct 19", NWS], ["SF Chronicle, Oct 18", SFC]]),
 dict(t="Fire and smoke", status="Real", asof="Oct 19, 2026",
      ev="The Cooley Fire, a prescribed burn north of Lake Sonoma that escaped its boundaries Oct 16, sent smoke across Sonoma County through Oct 19. An Oct 6 burn near Bodega Bay also prompted air quality warnings.",
      adj="Clean Air Indoors (C5) waits on standby and runs only where AQI turns unhealthy, while outdoor-work creative pauses there. Never advertise into an evacuation zone.",
      src=[["Press Democrat, Oct 16", COOLEY], ["Sonoma Index-Tribune, Oct 19", COOLEY2], ["Press Democrat, Oct 10", CARR]]),
 dict(t="Stock gaps at specific stores", hl=True, status="Real", asof="Oct 19, 2026, 4:12 p.m., all four stores",
      ev="Purely Compost and Malibu Compost: 0 at Sonoma. Gutter scoop: 0 at Sonoma. Wet/dry vac: 3 to 6 per store. Blue tarp: 1 at Petaluma vs 152 at Ukiah. Space heaters: 0 everywhere but Petaluma (25). Amerimax gutter guard fell from 84 to 71 at Santa Rosa in one day.",
      adj="Short items go to Purchasing with a projected delivery date. Ads hold any item at a store until stock covers demand; Sonoma's planting ads swap to Redi-Gro planting mix.",
      src=[["friedmanshome.com store inventory, read Oct 19", "https://www.friedmanshome.com/"]]),
 dict(t="Deep stock to push", status="Real", asof="Oct 19, 2026, all four stores",
      ev="Redi-Gro bark mulch 93 to 147 per store, planting mix 158 at Santa Rosa, copper pipe insulation 71 to 104, 3M N95 10-packs 59 to 123, sandbags in the thousands at every store.",
      adj="Soil and mulch lead Fall Planting; N95s lead Clean Air where purifiers run thin; sandbags join Storm Ready. Whether these are true overstock needs the buyers' forecast.",
      src=[["friedmanshome.com store inventory, read Oct 19", "https://www.friedmanshome.com/"]]),
 dict(t="Pro Tool Days this week", status="Real", asof="Weekly Ad, Oct 19 to 25, 2026",
      ev="Friedman's biggest tool sale of the year runs Oct 19 to 25, with vendor demos Oct 22 to 24 from 9 a.m. to 3 p.m. Not available at the Sonoma store.",
      adj="Brand search will rise; the agent protects brand terms and keeps storm and garden copy off tool offers. A contractor segment test (Buyer Segments) can ride the event.",
      src=[["Friedman's Weekly Ads", "https://www.friedmanshome.com/weekly-ads"]]),
 dict(t="Calendar", status="Real", asof="Oct 19, 2026",
      ev="Daylight saving time ends Sunday, Nov 1: darker evenings start the next day. Halloween is Saturday, Oct 31.",
      adj="Outdoor lighting and flashlight ideas held until stock allows. Weekend bursts for planting avoid Halloween evening.",
      src=[]),
]
triggers = [
 ["First rain of the season", "NWS rain in the 72-hour forecast for a store zone", "48 to 72 hours", "Gutter guard, downspout extensions, gutter scoop", "All four"],
 ["Storm or flood watch", "NWS flood, wind or high-surf watch; county alerts", "24 to 72 hours", "Tarps, wet/dry vac, drainage", "Petaluma, Sonoma first"],
 ["First inland frost", "NWS frost advisory, North Bay interior valleys and Ukiah", "24 to 48 hours", "Faucet covers, pipe insulation", "Ukiah, Sonoma"],
 ["Smoke day", "AirNow AQI Unhealthy for Sensitive Groups or worse in a trade area", "Immediate", "Clean Air standby: HEPA purifiers, filters, N95 masks; pause outdoor creative", "Affected area"],
 ["Moving in", "Recently-moved audiences on Google and Meta; about 460 Sonoma County home sales a month", "First 90 days", "Weatherstripping, faucet covers, furnace filters", "All four"],
 ["Weekend after rain", "Rain total over 0.1 in. in the prior 72 hours, dry weekend forecast", "2 to 3 days", "Compost, mulch, fertilizer", "Santa Rosa, Petaluma, Sonoma"],
 ["Clocks fall back", "Daylight saving ends Nov 1", "1 week", "Flashlights and lighting (held: low stock)", "All four"],
 ["Power shutoff notice", "Utility PSPS or outage notices", "12 to 48 hours", "Flashlights, outage kit (held: low stock)", "Affected area"],
]
sources = [
 ["NOAA CPC ENSO Diagnostic Discussion, Oct 8, 2026", CPC], ["NOAA 2026-27 winter outlook coverage, The Watchers, Oct 16", WINTER],
 ["Governor of California, El Niño emergency proclamation, Sep 21, 2026", GOV], ["NWS San Francisco Bay Area forecast discussion, Oct 19", NWS], ["SF Chronicle, Bay Area rain forecast, Oct 18", SFC],
 ["Press Democrat, Cooley Fire, Oct 16", COOLEY], ["Sonoma Index-Tribune, Cooley Fire smoke, Oct 19", COOLEY2], ["Press Democrat, prescribed burn smoke, Oct 10", CARR],
 ["Census QuickFacts, Santa Rosa", "https://census.gov/quickfacts/fact/table/santarosacitycalifornia,scottsvalleycitycalifornia,lamesacitycalifornia/AGE775223"],
 ["Census QuickFacts, Petaluma", "https://census.gov/quickfacts/fact/table/petalumacitycalifornia/RHI225223"],
 ["Census QuickFacts, Sonoma city", "https://census.gov/quickfacts/fact/table/sonomacitycalifornia,sandimascitycalifornia/PST045224"],
 ["Census QuickFacts, Ukiah", "https://census.gov/quickfacts/fact/table/ukiahcitycalifornia,mountainhousecdpcalifornia/PST045224"],
 ["Census QuickFacts, Sonoma County", "https://www.census.gov/quickfacts/fact/table/sonomacountycalifornia/INC110219"],
 ["Census QuickFacts, Mendocino County", "https://census.gov/quickfacts/fact/table/mendocinocountycalifornia/HSG651223"],
 ["Data USA, Sonoma County", "https://datausa.io/profile/geo/05000US06097"], ["Data USA, Mendocino County", "https://datausa.io/profile/geo/05000US06045"],
 ["Kincade Fire evacuation", "https://en.wikipedia.org/wiki/Kincade_Fire"],
 ["Friedman's store addresses (Locally)", "https://www.locally.com/store/89299/friedmans-home-improvement"],
 ["Webtonic, e-commerce Google Ads benchmarks 2026", "https://www.webtonic.io/blog/e-commerce-google-ads-statistics"],
 ["Webtonic, Home & Garden Search ranges 2026", "https://www.webtonic.io/blog/phone-tech-retail-google-ads-statistics"],
 ["FoundryCRO, Google Shopping benchmarks by category 2026", "https://foundrycro.com/blog/google-shopping-benchmarks-by-category-2026/"],
 ["OwlClaw, Google Shopping benchmarks", "https://owlclaw.com/benchmarks/google-shopping-benchmarks/"],
 ["WordStream, 2026 Google Ads benchmarks", "https://www.wordstream.com/blog/2026-google-ads-benchmarks"],
 ["Coupler.io, Facebook Ads statistics 2026 (WordStream data)", "https://blog.coupler.io/facebook-ads-statistics/"],
 ["ContentStudio, Meta ads benchmarks 2026", "https://contentstudio.io/blog/meta-ads-benchmarks"],
 ["Whatagraph, PPC benchmarks 2026 (TikTok)", "https://whatagraph.com/blog/articles/ppc-benchmarks"],
 ["Triple Whale, Google Ads benchmarks (Home & Garden median ROAS)", "https://triplewhale.com/blog/google-ads-benchmarks"],
 ["Google Trends, San Francisco-Oakland-San Jose market, 2023 to 2026", "https://trends.google.com/trends/explore?date=2023-01-01%202026-10-18&geo=US-CA-807&q=gutter%20guard,tarp,compost,sandbags,air%20purifier"],
 ["NOAA ACIS, Santa Rosa and Ukiah airport daily data", "https://data.rcc-acis.org/"],
 ["BLS QCEW, Sonoma and Mendocino counties, Q1 2025", "https://data.bls.gov/cew/apps/data_views/data_views.htm"],
 ["ATTOM, Sonoma County sales", "https://attomdata.com/data/us-real-estate/ca/sonoma-county"],
 ["Census QuickFacts, Sonoma County, ACS 2020 to 2024", "https://www.census.gov/quickfacts/fact/table/sonomacountycalifornia/INC110219"],
 ["NHPA 2025 Cost of Doing Business Study highlights", "https://hardwareretailing.com/staying-on-par-highlights-from-the-2025-cost-of-doing-business-study/"],
 ["Friedman's Weekly Ads, Pro Tool Days", "https://www.friedmanshome.com/weekly-ads"],
 ["National Weather Service API, forecasts and active alerts per store", "https://api.weather.gov/"],
]
data = dict(ads=json.load(open("ads.json")), proj=proj, sim=sim, der=der, products=prods, imgs=imgs, trends=trends, alerts=alerts, forces=forces, triggers=triggers, sources=sources)
html = open("template.html").read().replace("/*__FONTS__*/", open("fonts.css").read()).replace("__LOGO__", A["logo"]).replace("__DATA__", json.dumps(data).replace("</", "<\\/"))
sys.stdout.write(html)
