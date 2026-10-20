"""Friedman's PPC TikTok (C3 Fall Planting): ChatGPT scene images + ElevenLabs Nicole voiceover.
Same system as social/tiktok/render2.py (content TikToks): zoom backgrounds, logo plate, green labels,
progress dashes, charcoal captions timed to voice pauses, product card, CTA card, animated logo outro,
music bed ducked under the voice and a jingle sting.
Usage: python3 render_ppc.py <out.mp4>"""
import base64, io, json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

D = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
GREEN, CHAR, LIME, F1, E6, TITLE, YEL = "#007A33", "#222222", "#C4D82E", "#F1F1F1", "#E6E6E6", "#212427", "#FFE500"
FD = os.path.join(D, "fonts")
def font(w, s): return ImageFont.truetype(os.path.join(FD, f"Barlow-{w}.ttf"), s)
def nc(s): return ImageFont.truetype(os.path.join(FD, "NewsCycle-Regular.ttf"), s)

LOGO = os.path.join(D, "logo-wordmark.png")
VO = os.path.join(D, "audio", "vo.mp3")
BED = os.path.join(D, "audio", "music_bed.mp3")
STING = os.path.join(D, "audio", "music_sting.mp3")
ASSETS = json.load(open(os.path.join(D, "assets.json")))["imgs"]
PRODUCTS = [("2000030180", "Purely Compost", "1.5 cu ft · Gardner & Bloome"),
            ("502204910", "Biodynamic Compost", "1 cu ft · Malibu Compost"),
            ("2000002880", "Bark Mulch", "2 cu ft · Redi-Gro"),
            ("2000035127", "Tomato, Veg & Herb Fertilizer", "4 lb · Gardner & Bloome")]

SEGS = [
    dict(img="tt-1", label=None, title=None, t="Planting in fall? Here's why it wins in the North Bay."),
    dict(img="tt-2", label="Why fall", title="Rain does the work", t="Warm soil and winter rain do the work. Roots grow all winter, so your plants are ready for spring, and need less water next summer."),
    dict(img="tt-3", label="Step 1", title="Compost", t="Here's the plan. Spread three inches of compost, and work it into the soil."),
    dict(img="tt-4", label="Step 2", title="Plant", t="Plant at the same depth as the pot, and water it in."),
    dict(img="tt-5", label="Step 3", title="Mulch", t="Finish with three inches of mulch, pulled back from the stems."),
    dict(img="PRODUCTS", label="Ready for pickup", title="Fall bed basics", t="Compost, mulch and fertilizer are ready for pickup at Friedman's."),
    dict(img="CTA", label=None, title=None, t="Order online for pickup, visit us in Santa Rosa, Petaluma, Sonoma or Ukiah, or book a free fifteen minute consult with a project pro."),
]

def wrap(d, text, f, maxw):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) > maxw and line: out.append(line); line = w
        else: line = t
    if line: out.append(line)
    return out

def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    l, t = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((l, t, l + w, t + h))

def pimg(item):
    b = ASSETS[item].split(",", 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(b))).convert("RGBA")

def logo_plate(base, y, h=86):
    lg = Image.open(LOGO).convert("RGBA")
    lw = round(lg.width * h / lg.height); lg = lg.resize((lw, h), Image.LANCZOS)
    pad = 26; x = (W - lw) // 2
    ImageDraw.Draw(base).rectangle([x - pad, y - pad, x + lw + pad, y + h + pad], fill="white")
    base.alpha_composite(lg, (x, y))

def background(key):
    BW, BH = int(W * 1.1), int(H * 1.1)
    if key == "CTA": return Image.new("RGB", (BW, BH), CHAR)
    if key == "PRODUCTS": return Image.new("RGB", (BW, BH), F1)
    return cover(Image.open(os.path.join(D, "scenes", key + ".png")).convert("RGB"), BW, BH)

def overlay(i, seg, n):
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o); key = seg["img"]
    if key == "CTA":
        logo_plate(o, 170, 92); y = 380
        for ln in ["VISIT", "FRIEDMAN'S"]:
            d.text((80, y), ln, font=font("ExtraBold", 150), fill="white"); y += 150
        d.text((84, y + 10), "Your Fall Bed, Ready For Pickup", font=font("Medium", 46), fill=LIME)
        y += 100; tx = 80; tw = (W - 160 - 3 * 24) // 4
        for it, _, _ in PRODUCTS:
            d.rectangle([tx, y, tx + tw, y + tw], fill="white")
            im = pimg(it); s = min((tw - 24) / im.width, (tw - 24) / im.height)
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); o.alpha_composite(im, (tx + (tw - im.width) // 2, y + (tw - im.height) // 2))
            tx += tw + 24
        y += tw + 60
        for a, b in [("COME IN", "Santa Rosa · Petaluma · Sonoma · Ukiah"), ("ORDER ONLINE", "friedmanshome.com · Pick up in store"), ("ASK A PROJECT PRO", "Book a free 15-minute consult")]:
            d.rectangle([80, y, W - 80, y + 150], fill="white"); d.rectangle([80, y, 96, y + 150], fill=GREEN)
            d.text((128, y + 22), a, font=font("ExtraBold", 56), fill=CHAR); d.text((128, y + 90), b, font=nc(36), fill="#333333")
            y += 174
        return o
    photo = key.startswith("tt-")
    if photo:  # scrim: top for the logo, lower half for text
        sc = Image.new("L", (1, H))
        for yy in range(H):
            a = int(150 * (1 - yy / 360)) if yy < 360 else 0
            if yy > 760: a = max(a, int(215 * min(1, (yy - 760) / 420)))
            sc.putpixel((0, yy), a)
        o.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 0)] * 3 + [sc.resize((W, H))]))
    logo_plate(o, 150, 76)
    steps = n - 2; bx = 120; bw = (W - 240 - (steps - 1) * 12) / steps
    for k in range(steps):
        fill = GREEN if k < i else (255, 255, 255, 120) if photo else (0, 0, 0, 40)
        d.rectangle([bx + k * (bw + 12), 300, bx + k * (bw + 12) + bw, 310], fill=fill)
    if photo:
        d.text((W - 120, 326), "AI-generated image · placeholder", font=nc(24), fill=(255, 255, 255, 210), anchor="ra")
    if i == 0:  # promo-tile opener, same copy system as the C3 ads
        y = 760; f = font("Bold", 40); k_ = "GARDEN CENTER"; kw = d.textlength(k_, font=f) + 48
        d.rectangle([80, y, 80 + kw, y + 66], fill=GREEN); d.text((104, y + 9), k_, font=f, fill="white")
        y += 96; f = font("ExtraBold", 122)
        for ln, col in [("YOUR SPRING", "white"), ("GARDEN STARTS", "white"), ("THIS FALL", YEL)]:
            d.text((80, y), ln, font=f, fill=col); y += 122
        d.text((84, y + 24), "Fall Beats Spring In The North Bay", font=font("Medium", 50), fill="white")
        return o
    y = 880 if photo else 360
    if seg["label"]:
        f = font("Bold", 42); lw = d.textlength(seg["label"].upper(), font=f) + 48
        d.rectangle([80, y, 80 + lw, y + 68], fill=GREEN); d.text((104, y + 10), seg["label"].upper(), font=f, fill="white")
    y += 90; f = font("ExtraBold", 96 if photo else 80)
    for ln in wrap(d, seg["title"].upper(), f, W - 220)[:2]:
        d.text((80, y), ln, font=f, fill="white" if photo else TITLE); y += 96 if photo else 82
    if key == "PRODUCTS":
        y += 30; gap = 24; cw = (W - 160 - gap) // 2; ch = 380
        for j, (it, name, sub) in enumerate(PRODUCTS):
            x = 80 + (j % 2) * (cw + gap); yy = y + (j // 2) * (ch + gap)
            d.rounded_rectangle([x, yy, x + cw, yy + ch], 6, fill="white", outline=E6, width=3)
            im = pimg(it); s_ = min((cw - 60) / im.width, (ch - 150) / im.height)
            im = im.resize((round(im.width * s_), round(im.height * s_)), Image.LANCZOS)
            o.alpha_composite(im, (x + (cw - im.width) // 2, yy + 18 + (ch - 150 - im.height) // 2))
            f2 = font("Bold", 34)
            for li, ln in enumerate(wrap(d, name.upper(), f2, cw - 40)[:2]): d.text((x + 20, yy + ch - 124 + li * 36), ln, font=f2, fill=TITLE)
            d.text((x + 20, yy + ch - 46), sub, font=nc(24), fill="#595959")
        d.text((80, y + 2 * (ch + gap) + 6), "Pickup at your store · stock checked live before launch", font=nc(28), fill=GREEN)
    return o

def caption(text):
    o = Image.new("RGBA", (W, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    f = font("SemiBold", 50); lines = wrap(d, text, f, W - 280)[:3]
    lh = 64; h = len(lines) * lh + 40; y0 = 330 - h
    wmax = max(d.textlength(l, font=f) for l in lines)
    d.rectangle([80, y0, 80 + wmax + 56, 330], fill=(34, 34, 34, 225))
    for j, l in enumerate(lines): d.text((108, y0 + 20 + j * lh), l, font=f, fill="white")
    return o

def sentences(t):
    parts = re.split(r"(?<=[.?!])\s+", t.strip()); out = []
    for p in parts:
        if out and len(p.split()) <= 3: out[-1] += " " + p
        else: out.append(p)
    chunks = []
    for p in out:
        w = p.split()
        if len(w) <= 13: chunks.append(p); continue
        cur, parts2 = [], []
        for word in w:
            cur.append(word)
            if (word.endswith(",") and len(cur) >= 5) or len(cur) >= 12: parts2.append(" ".join(cur)); cur = []
        if cur:
            if len(cur) <= 2 and parts2: parts2[-1] += " " + " ".join(cur)
            else: parts2.append(" ".join(cur))
        chunks += parts2
    return chunks

def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())

def silences(f):
    r = subprocess.run(["ffmpeg", "-i", f, "-af", "silencedetect=noise=-35dB:d=0.25", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    return [((a + b) / 2, b - a) for a, b in zip(st, en)]

def boundaries(texts, total, sil):
    w = [len(t) for t in texts]; tot = sum(w); est, acc = [], 0
    for x in w[:-1]: acc += x; est.append(total * acc / tot)
    out, used = [], set()
    for e in est:
        best = min((s for s in sil if s[0] not in used and abs(s[0] - e) < 1.6), key=lambda s: abs(s[0] - e) - s[1] * 0.8, default=None)
        if best: used.add(best[0]); out.append(best[0])
        else: out.append(e)
    return [0.0] + sorted(out) + [total]

def ease_back(t):
    c1 = 1.70158; c3 = c1 + 1; t = min(max(t, 0), 1)
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def ease_out(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3

def outro(wd, L):
    lg = Image.open(LOGO).convert("RGBA")
    lh = 96; lw = round(lg.width * lh / lg.height); lg = lg.resize((lw, lh), Image.LANCZOS)
    pad = 44; plate = Image.new("RGBA", (lw + 2 * pad, lh + 2 * pad), "white"); plate.alpha_composite(lg, (pad, pad))
    fdir = os.path.join(wd, "outro"); os.makedirs(fdir, exist_ok=True)
    N = round(L * 30); cy = 820
    for fi in range(N):
        t = fi / 30; fr = Image.new("RGBA", (W, H), CHAR); d = ImageDraw.Draw(fr)
        bw = int(W * ease_out(t / 0.45)); d.rectangle([0, cy + 170, bw, cy + 186], fill=GREEN)
        k = ease_back((t - 0.1) / 0.6)
        if k > 0.01:
            pw, ph = max(1, int(plate.width * k)), max(1, int(plate.height * k)); p = plate.resize((pw, ph), Image.LANCZOS)
            a = min(1, (t - 0.1) / 0.25); p.putalpha(p.getchannel("A").point(lambda v: int(v * a)))
            fr.alpha_composite(p, ((W - pw) // 2, cy - ph // 2))
        for (txt, f, col, t0, y0) in [("THE HUMAN SIDE OF HOME IMPROVEMENT", font("Bold", 46), LIME, 0.7, cy + 250),
                                      ("friedmanshome.com", font("SemiBold", 54), "white", 1.0, cy + 340),
                                      ("Santa Rosa · Petaluma · Sonoma · Ukiah", nc(38), (220, 220, 220), 1.2, cy + 420)]:
            e = ease_out((t - t0) / 0.5)
            if e > 0:
                layer = Image.new("RGBA", (W, 90), (0, 0, 0, 0)); ImageDraw.Draw(layer).text((W // 2, 45), txt, font=f, fill=col, anchor="mm")
                layer.putalpha(layer.getchannel("A").point(lambda v: int(v * e))); fr.alpha_composite(layer, (0, int(y0 + (1 - e) * 40)))
        fr.convert("RGB").save(f"{fdir}/f{fi:04d}.jpg", quality=92)
    out = f"{wd}/outro.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", f"{fdir}/f%04d.jpg", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", out], check=True)
    return out

def build(out):
    n = len(SEGS); wd = os.path.join(D, "build"); os.makedirs(wd, exist_ok=True)
    vlen = dur(VO); HOLD = 1.0; OUT_L = max(4.0, min(6.0, dur(STING)))
    b = boundaries([s["t"] for s in SEGS], vlen, silences(VO)); b[-1] = vlen + HOLD
    parts = []
    for i, seg in enumerate(SEGS):
        t0, t1 = b[i], b[i + 1]; L = t1 - t0
        background(seg["img"]).save(f"{wd}/bg{i}.jpg", quality=92); overlay(i, seg, n).save(f"{wd}/ov{i}.png")
        inputs = ["-loop", "1", "-framerate", "30", "-t", f"{L:.3f}", "-i", f"{wd}/bg{i}.jpg", "-i", f"{wd}/ov{i}.png"]
        fr = round(L * 30); z = ("1.0+0.09*on/%d" if i % 2 == 0 else "1.09-0.09*on/%d") % max(fr, 1)
        filt = f"[0:v]scale={int(W*1.1)}:{int(H*1.1)},zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30[bg];[bg][1:v]overlay=0:0[v0]"
        last = "v0"
        if seg["img"] not in ("CTA", "PRODUCTS"):
            sents = sentences(seg["t"]); lens = [len(s) for s in sents]; acc = 0
            for j, s_ in enumerate(sents):
                a = L * acc / sum(lens); acc += lens[j]; e = L * acc / sum(lens) if j < len(sents) - 1 else L
                caption(s_).save(f"{wd}/cap{i}_{j}.png"); inputs += ["-i", f"{wd}/cap{i}_{j}.png"]
                filt += f";[{last}][{2+j}:v]overlay=0:1220:enable='between(t,{a:.3f},{e:.3f})'[c{j}]"; last = f"c{j}"
        so = f"{wd}/seg{i}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", filt, "-map", f"[{last}]", "-t", f"{L:.3f}", "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20", so], check=True)
        parts.append(so)
    parts.append(outro(wd, OUT_L))
    open(f"{wd}/list.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{wd}/list.txt", "-c", "copy", f"{wd}/video.mp4"], check=True)
    T = dur(f"{wd}/video.mp4"); oa = vlen + HOLD
    fc = (f"[1:a]aresample=44100,aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-1.5:LRA=11,apad=whole_dur={T:.3f}[vx];[vx]asplit=2[vmix][vsc];"
          f"[2:a]aresample=44100,aformat=channel_layouts=stereo,atrim=0:{oa+0.6:.3f},volume=0.30,afade=t=in:d=0.6,afade=t=out:st={oa-0.6:.3f}:d=1.2[bed0];"
          f"[bed0][vsc]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=350:makeup=1[bed];"
          f"[3:a]aresample=44100,aformat=channel_layouts=stereo,volume=0.9,adelay={int(oa*1000)}|{int(oa*1000)},afade=t=out:st={T-0.8:.3f}:d=0.8[st];"
          f"[vmix][bed][st]amix=inputs=3:normalize=0:duration=first[mx];[mx]alimiter=limit=0.89,atrim=0:{T:.3f}[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{wd}/video.mp4", "-i", VO, "-i", BED, "-i", STING, "-filter_complex", fc,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print("segments", [round(x, 2) for x in b], "->", out, round(dur(out), 1), "s")

if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, "friedmans-ppc-c3-tiktok.mp4"))
