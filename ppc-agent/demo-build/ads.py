"""Ad samples for every proposed venue, checked against platform limits and brand rules.
Run: python3 ads.py > ads.json   (exits non-zero if any hard limit or brand rule fails)"""
import json, sys, re

LIMITS = {  # hard limits (Google Ads RSA; TikTok ad text); others are recommended lengths
 "rsa_headline": 30, "rsa_description": 90, "rsa_path": 15, "pmax_headline": 30, "pmax_long_headline": 90, "pmax_description": 90,
 "tiktok_text": 100, "meta_headline": 40, "meta_primary": 125, "sms": 160}
HARD = {"rsa_headline", "rsa_description", "rsa_path", "pmax_headline", "pmax_long_headline", "pmax_description", "tiktok_text", "sms"}

ADS = [
 # ---------------- C1 Gutter Gear ----------------
 dict(id="C1-SEARCH", cid="C1", venue="Google Search", fmt="rsa", url="friedmanshome.com", paths=["Gutters", "Drainage"],
      headlines=["Gutter Guard In Stock", "Get Gutters Ready For Rain", "Pickup Today At Friedman's", "Downspout Extensions",
                 "Stop Gutter Overflow", "Local Since 1946", "Drive-Thru Pickup Available", "Santa Rosa, Petaluma, Sonoma",
                 "Gutter Gear For The North Bay", "Clear Gutters Before Storms"],
      descriptions=["Gutter guard, downspout extensions and gutter scoops. Order online and pick up today.",
                    "Rain is on the way. Get gutter gear at Friedman's Santa Rosa, Petaluma, Sonoma or Ukiah.",
                    "Send roof water away from your foundation. Family-owned and local since 1946.",
                    "Need help choosing? Book a free 15-minute call with a Friedman's project pro."],
      sitelinks=["Gutter Guard", "Downspout Extensions", "Store Pickup", "Book A Free Pro Call"]),
 dict(id="C1-PMAX", cid="C1", venue="Performance Max + local inventory", fmt="pmax",
      headlines=["Gutter Gear For Rain Season", "In Stock Near You", "Pickup Today", "Downspout Extensions"],
      long_headlines=["Get gutters ready for the rain with gutter guard and downspout extensions from Friedman's"],
      descriptions=["Gutter guard, downspout extensions and sealant, in stock at your nearest Friedman's.",
                    "Local since 1946. Order online for pickup at Santa Rosa, Petaluma, Sonoma or Ukiah."],
      products=["2298786", "2295031", "2000023006", "300101664"],
      note="Local inventory ads pull price and stock live from the product feed, so they never show an item a store is out of.",
      creative=[['c1-square', 'Square 1:1 (feed)'], ['c1-wide', 'Landscape 1.91:1 (Display, Discover)'], ['c1-vertical', 'Vertical 9:16 (YouTube Shorts, Stories)']]),
 dict(id="C1-SEARCH-ES", cid="C1", venue="Google Search (Spanish line)", fmt="rsa", url="friedmanshome.com", paths=["Canaletas", "Drenaje"],
      headlines=["Prepárese Para La Lluvia", "Protector De Canaletas", "Recoja Hoy En Friedman's", "Extensiones Para Bajantes"],
      descriptions=["Protector de canaletas y extensiones para bajantes. Ordene en línea y recoja hoy.",
                    "Friedman's Santa Rosa, Petaluma, Sonoma y Ukiah. Negocio familiar y local desde 1946."],
      sitelinks=["Canaletas", "Recoger En Tienda"], note="Spanish copy goes to a fluent team member for review before approval."),
 # ---------------- C2 Storm Ready ----------------
 dict(id="C2-META", cid="C2", venue="Meta (Facebook and Instagram)", fmt="meta",
      primary="Big storms are in the forecast. Grab sandbags, heavy-duty tarps and a wet/dry vac now, ready for pickup at Friedman's.",
      headline="Be Storm Ready", description="Pickup at 4 North Bay stores", cta="Shop Now",
      tile=dict(h="BE STORM READY", s="Sandbags, Tarps And A Wet/Dry Vac", b="SHOP STORM PREP"), products=["4314103", "300601171", "2000054322"],
      creative=[['c2-square', 'Feed 1:1']]),
 dict(id="C2-NEXTDOOR", cid="C2", venue="Nextdoor", fmt="nextdoor",
      headline="Sandbags are in stock at Friedman's Petaluma",
      body="Neighbors, with rain in the forecast, here's a quick tip from your local hardware store: fill sandbags only half to two-thirds full, lay them like bricks, and tuck plastic sheeting underneath. Sandbags, tarps and wet/dry vacs are ready for pickup at 429 N McDowell Blvd. Questions? Our team is happy to help.",
      cta="Shop Storm Prep", note="Store-specific version for each affected store; this Petaluma post is the ADJ-4 test.",
      creative=[['c2-wide', 'Image 1.91:1']]),
 # ---------------- C3 Fall Planting ----------------
 dict(id="C3-META", cid="C3", venue="Meta (Facebook and Instagram)", fmt="meta",
      primary="Fall beats spring for planting in the North Bay. Warm soil and winter rain do the work. Build your bed in a weekend.",
      headline="It's Time To Plant", description="Compost and mulch, pickup today", cta="Shop Now",
      tile=dict(h="IT'S TIME TO... PLANT", s="Fall Beats Spring In The North Bay", b="SHOP GARDEN SOIL"), products=["2000030180", "2000002880", "2000035127"],
      creative=[['c3-square', 'Feed 1:1'], ['c3-vertical', 'Stories and Reels 9:16']]),
 dict(id="C3-TIKTOK", cid="C3", venue="TikTok", fmt="tiktok",
      text="Fall beats spring for planting here. Compost, plant, mulch. Pickup today at Friedman's.",
      hook="0 to 3 s: 'Planting in fall? Here's why it wins in the North Bay.'",
      beats=["3 to 12 s: why fall: warm soil and winter rain, roots grow all winter, less water next summer",
             "12 to 24 s: three steps on screen: 3 inches of compost, plant at pot depth and water in, 3 inches of mulch pulled back from stems",
             "24 to 28 s: the products on a card: compost, bark mulch, fertilizer, ready for pickup (no prices)",
             "28 to 37 s: come in, order online for pickup, or book a free 15-minute consult with a project pro",
             "37 to 42 s: animated Friedman's logo end card with the jingle"],
      cta="Shop Now", note="Built for this campaign: scene images generated in ChatGPT, voiceover by ElevenLabs (Nicole), Friedman's logo, captions and product card added in post. Turn on TikTok's AI-generated content label.",
      creative=[['c3-tiktok', 'Video 9:16, 42 s']]),
 dict(id="C3-META-ES", cid="C3", venue="Meta (Spanish line)", fmt="meta",
      primary="En el norte de la bahía, el otoño es mejor para sembrar. Composta y mulch listos para recoger en Friedman's.",
      headline="Es Hora De Sembrar", description="Recoja hoy en su tienda", cta="Comprar",
      tile=dict(h="ES HORA DE SEMBRAR", s="El Otoño Es Para Sembrar", b="SHOP GARDEN SOIL"), products=["2000030180", "2000002880"],
      note="Spanish copy goes to a fluent team member for review before approval.",
      creative=[['c3-square-es', 'Feed 1:1 (Spanish)']]),
 # ---------------- C5 Clean Air (standby) ----------------
 dict(id="C5-SEARCH", cid="C5", venue="Google Search (smoke days only)", fmt="rsa", url="friedmanshome.com", paths=["Air-Quality", "Purifiers"],
      headlines=["HEPA Air Purifiers In Stock", "N95 Masks Ready For Pickup", "Breathe Easier Inside", "Pickup Today At Friedman's",
                 "Replacement HEPA Filters", "Furnace Filters In Stock"],
      descriptions=["HEPA purifiers, replacement filters and N95 masks, ready for pickup at Friedman's today.",
                    "Keep indoor air cleaner on smoky days. Four North Bay stores, family-owned since 1946."],
      sitelinks=["Air Purifiers", "N95 Masks", "Store Pickup"]),
 dict(id="C5-META", cid="C5", venue="Meta (smoke days only)", fmt="meta",
      primary="On smoky days, cleaner air starts inside. HEPA purifiers, filters and N95 masks are ready for pickup at Friedman's.",
      headline="Breathe Easier Inside", description="Ready for pickup today", cta="Shop Now",
      tile=dict(h="BREATHE EASIER INSIDE", s="HEPA Purifiers And N95 Masks", b="SHOP AIR QUALITY"), products=["2000002404", "2000038308"],
      note="No fire imagery and no fear lines. Runs only in areas where AQI is unhealthy.",
      creative=[['c5-square', 'Feed 1:1']]),
 # ---------------- C4 Winterize (owned only) ----------------
 dict(id="C4-SMS", cid="C4", venue="SMS (opted-in only)", fmt="sms",
      text="Friedman's: Frost tonight in the valley. Cover faucets and wrap pipes before dark. Pickup ready at your store: [link] Reply STOP to opt out.",
      note="[link] is a short tracked link to the frost collection with the customer's store selected."),
 dict(id="C4-EMAIL", cid="C4", venue="Email (opted-in only)", fmt="email",
      subject="Frost tonight: 3 quick ways to protect your pipes", preheader="Faucet covers, pipe insulation and frost blankets, ready for pickup.",
      body=["Frost is in tonight's forecast for the inland valleys. Three steps take about 20 minutes:",
            "1. Disconnect hoses and cover outdoor faucets.", "2. Wrap exposed pipes with foam pipe insulation.", "3. Cover tender plants with a frost blanket before dark."],
      cta="SHOP FROST PROTECTION", footer="Questions? Book a free 15-minute call with a Friedman's project pro.",
      creative=[['c4-email', 'Email header']]),
]

BANNED = [r"—", r"–", r"\$\d", r"\blowest\b", r"\bbest\b", r"\bguarantee", r"Learn More"]
problems = []
def chk(kind, text, ad):
    n = len(text); lim = LIMITS.get(kind)
    for b in BANNED:
        if re.search(b, text, re.I): problems.append(f"{ad['id']}: brand rule '{b}' in '{text}'")
    if lim and n > lim and kind in HARD: problems.append(f"{ad['id']}: {kind} {n}>{lim}: {text}")
    return dict(text=text, n=n, lim=lim, hard=kind in HARD, over=bool(lim and n > lim))
out = []
for ad in ADS:
    a = dict(ad); f = ad["fmt"]
    if f == "rsa":
        a["headlines"] = [chk("rsa_headline", h, ad) for h in ad["headlines"]]
        a["descriptions"] = [chk("rsa_description", d, ad) for d in ad["descriptions"]]
        a["paths"] = [chk("rsa_path", p, ad) for p in ad["paths"]]
    elif f == "pmax":
        a["headlines"] = [chk("pmax_headline", h, ad) for h in ad["headlines"]]
        a["long_headlines"] = [chk("pmax_long_headline", h, ad) for h in ad["long_headlines"]]
        a["descriptions"] = [chk("pmax_description", d, ad) for d in ad["descriptions"]]
    elif f == "meta":
        a["primary"] = chk("meta_primary", ad["primary"], ad); a["headline"] = chk("meta_headline", ad["headline"], ad)
    elif f == "tiktok":
        a["text"] = chk("tiktok_text", ad["text"], ad)
    elif f == "sms":
        a["text"] = chk("sms", ad["text"], ad)
        if not ad["text"].endswith("Reply STOP to opt out."): problems.append(f"{ad['id']}: SMS must end with the STOP opt-out")
    elif f == "nextdoor":
        chk("x", ad["body"], ad); chk("x", ad["headline"], ad)
    out.append(a)
if problems:
    print("\n".join(problems), file=sys.stderr); sys.exit(1)
print(json.dumps(dict(ads=out, limits=LIMITS)))
