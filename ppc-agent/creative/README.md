# PPC ad creative (concept demo)

AI-generated placeholder creative for the proposed campaigns, embedded in `../index.html` (Campaigns, Ad samples).

| File | Campaign · venue | Made with |
|---|---|---|
| c1-square, c1-wide, c1-vertical | C1 Gutter Gear · Performance Max | ChatGPT image generation |
| c2-square | C2 Storm Ready · Meta | ChatGPT |
| c2-wide | C2 Storm Ready · Nextdoor | ChatGPT |
| c3-square, c3-vertical | C3 Fall Planting · Meta feed, Stories and Reels | ChatGPT |
| c3-square-es | C3 Fall Planting · Meta (Spanish line) | ChatGPT |
| c3-tiktok.mp4 | C3 Fall Planting · TikTok, 42 s | ChatGPT scenes, ElevenLabs voiceover (Nicole), `tiktok/render_ppc.py` |
| c5-square | C5 Clean Air · Meta | ChatGPT |
| c4-email | C4 Winterize · email header | ChatGPT |

- **Inputs:** the Friedman's wordmark and a campaign layout reference sheet supplied by Jason Dodge.
- **Before launch:** check the logo and every word on each image, have a fluent team member review the Spanish, and turn on TikTok's AI-generated content label. Swap in Friedman's own photos when they exist.
- **Rebuild the demo:** `cd ../demo-build && python3 ads.py > ads.json && python3 build.py assets.json > ../index.html`
- **Renderer:** needs Barlow and News Cycle TTFs in `tiktok/fonts/`, the wordmark, the voiceover and music files, and `assets.json` beside it. These aren't committed.
