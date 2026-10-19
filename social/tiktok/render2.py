"""v2: why / Friedman's has it / good to know / how it works, AI step images, music bed + jingle, animated logo outro.
Usage: python3 -I render.py <post_id>   (run from the tiktok folder via absolute path)"""
import json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
GREEN, CHAR, LIME, F1, E6, TITLE = "#007A33", "#222222", "#C4D82E", "#F1F1F1", "#E6E6E6", "#212427"
FD = os.path.join(D, "fonts")
def font(w, s): return ImageFont.truetype(os.path.join(FD, f"Barlow-{w}.ttf"), s)
def nc(s): return ImageFont.truetype(os.path.join(FD, "NewsCycle-Regular.ttf"), s)

S = json.load(open(os.path.join(D, "scripts2.json")))
M = json.load(open(os.path.join(D, "imgmeta.json")))
TILE = {1: ("Garden Center", "It's Time To... Plant", "Get Fall Plantings In Before The Rains"),
        2: ("Hardware", "Seal Out The Drafts", "Weatherstrip A Door In About 30 Minutes"),
        3: ("Pro Desk", "Gutter Gear", "Get Your Gutters Ready For The Rain"),
        4: ("Plumbing & Irrigation", "It's Time To... Winterize", "Protect Faucets And Pipes Before The Frost")}
HERO_ITEMS = {1: ["compost", "mulch", "veg", "garlic"], 2: ["strip", "sweep", "knife", "alcohol"],
              3: ["scoop", "ext", "ladder", "light"], 4: ["covers", "insul", "tape", "hose"]}

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

def logo_plate(base, y, h=86):
    lg = Image.open(os.path.join(D, M["logo"]["file"])).convert("RGBA")
    lw = round(lg.width * h / lg.height); lg = lg.resize((lw, h), Image.LANCZOS)
    pad = 26; x = (W - lw) // 2
    ImageDraw.Draw(base).rectangle([x - pad, y - pad, x + lw + pad, y + h + pad], fill="white")
    base.alpha_composite(lg, (x, y))

def is_photo(key): return key not in ("PRODUCTS", "CTA")
def is_gen(key): return key.startswith("g") and "_" in key
def img_file(key): return os.path.join(D, "img", "gen", key + ".png") if is_gen(key) else os.path.join(D, M[key]["file"])

def background(pid, key):
    """Returns an RGB image 10% larger than the frame (room for a slow zoom)."""
    BW, BH = int(W * 1.1), int(H * 1.1)
    if key == "CTA":
        return Image.new("RGB", (BW, BH), CHAR)
    if is_gen(key):  # 16:9 step image: full picture on a card over a blurred, darkened copy of itself
        from PIL import ImageEnhance
        im = Image.open(img_file(key)).convert("RGB")
        bg = ImageEnhance.Brightness(cover(im, BW, BH).filter(ImageFilter.GaussianBlur(38))).enhance(0.45)
        cw = BW - 70; ch = round(cw * im.height / im.width)
        card = im.resize((cw, ch), Image.LANCZOS)
        cy = 760 - ch // 2
        ImageDraw.Draw(bg).rectangle([35 - 6, cy - 6, 35 + cw + 6, cy + ch + 6], fill="white")
        bg.paste(card, (35, cy))
        return bg
    if is_photo(key):
        im = Image.open(img_file(key)).convert("RGB")
        bg = cover(im, BW, BH)
        return bg
    return Image.new("RGB", (BW, BH), F1)

def product_grid(o, d, pid, y):
    items = [f"{pid}:{it}" for it in HERO_ITEMS[pid] if M.get(f"{pid}:{it}", {}).get("file")][:4]
    gap = 24; cw = (W - 160 - gap) // 2; ch = 330
    d.text((80, y - 6), "In stock at all 4 stores", font=font("Bold", 38), fill=GREEN); y += 56
    for j, k in enumerate(items):
        x = 80 + (j % 2) * (cw + gap); yy = y + (j // 2) * (ch + gap); meta = M[k]
        d.rounded_rectangle([x, yy, x + cw, yy + ch], 6, fill="white", outline=E6, width=3)
        im = Image.open(os.path.join(D, meta["file"])).convert("RGBA")
        s_ = min((cw - 60) / im.width, (ch - 150) / im.height); im = im.resize((round(im.width * s_), round(im.height * s_)), Image.LANCZOS)
        o.alpha_composite(im, (x + (cw - im.width) // 2, yy + 18 + (ch - 150 - im.height) // 2))
        f = font("Bold", 34)
        for li, ln in enumerate(wrap(d, meta["name"].upper(), f, cw - 40)[:2]): d.text((x + 20, yy + ch - 120 + li * 36), ln, font=f, fill=TITLE)
        sub = "In-store Garden Center" if meta["instore"] else f"Item #{meta['item']}"
        d.text((x + 20, yy + ch - 42), sub, font=nc(24), fill="#595959")

def product_card(o, d, pid, key, y):
    k = f"{pid}:{key[5:]}"; im = Image.open(os.path.join(D, M[k]["file"])).convert("RGBA"); meta = M[k]
    cx, cw, ch = 80, W - 160, 470
    d.rounded_rectangle([cx, y, cx + cw, y + ch], 6, fill="white", outline=E6, width=3)
    s_ = min((cw - 100) / im.width, (ch - 80) / im.height); im = im.resize((round(im.width * s_), round(im.height * s_)), Image.LANCZOS)
    o.alpha_composite(im, (cx + (cw - im.width) // 2, y + (ch - im.height) // 2))
    y += ch + 26; f = font("Bold", 44)
    for ln in wrap(d, meta["pn"], f, cw)[:2]:
        d.text((cx, y), ln, font=f, fill=TITLE); y += 52
    sub = ("In-store Garden Center item" if meta["instore"] else f"Item #{meta['item']}") + " · In stock at all 4 stores"
    d.text((cx, y + 4), sub, font=nc(32), fill=GREEN)

def overlay(pid, i, seg, n):
    """Static branded layer (RGBA): logo, step label, title, progress, credit."""
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    key = seg["img"]
    if key == "CTA":
        logo_plate(o, 170, 92)
        y = 380
        for ln in ["VISIT", "FRIEDMAN'S"]:
            d.text((80, y), ln, font=font("ExtraBold", 150), fill="white"); y += 150
        d.text((84, y + 10), "Everything For This Project, In Stock", font=font("Medium", 46), fill=LIME)
        # product strip
        y += 100; tx = 80; tw = (W - 160 - 3 * 24) // 4
        for it in HERO_ITEMS[pid]:
            k = f"{pid}:{it}"
            if k not in M or not M[k]["file"]: continue
            d.rectangle([tx, y, tx + tw, y + tw], fill="white")
            im = Image.open(os.path.join(D, M[k]["file"])).convert("RGBA"); s = min((tw - 24) / im.width, (tw - 24) / im.height)
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); o.alpha_composite(im, (tx + (tw - im.width) // 2, y + (tw - im.height) // 2))
            tx += tw + 24
        y += tw + 60
        rows = [("COME IN", "Santa Rosa · Petaluma · Sonoma · Ukiah"),
                ("ORDER ONLINE", "friedmanshome.com · Pick up in store"),
                ("ASK A PROJECT PRO", "Book a free 15-minute consult")]
        for a, b in rows:
            d.rectangle([80, y, W - 80, y + 150], fill="white")
            d.rectangle([80, y, 96, y + 150], fill=GREEN)
            d.text((128, y + 22), a, font=font("ExtraBold", 56), fill=CHAR)
            d.text((128, y + 90), b, font=nc(36), fill="#333333")
            y += 174
        return o
    # gradient scrim for legibility (top + lower third)
    sc = Image.new("L", (1, H))
    for yy in range(H):
        a = 0
        if yy < 360: a = int(150 * (1 - yy / 360))
        g0 = 1010 if is_gen(key) else 820
        if yy > g0: a = max(a, int(215 * min(1, (yy - g0) / 400)))
        sc.putpixel((0, yy), a)
    if is_photo(key):
        o.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 0)] * 3 + [sc.resize((W, H))]))
    logo_plate(o, 150, 76)
    # progress dashes under the logo
    steps = n - 2; bx = 120; bw = (W - 240 - (steps - 1) * 12) / steps
    for k in range(steps):
        fill = GREEN if k < i else (255, 255, 255, 120) if is_photo(key) else (0, 0, 0, 40)
        d.rectangle([bx + k * (bw + 12), 300, bx + k * (bw + 12) + bw, 310], fill=fill)
    txt = "white" if is_photo(key) else TITLE
    if i == 0:
        k_, h_, s_ = TILE[pid]
        y = 700
        f = font("Bold", 40); kw = d.textlength(k_.upper(), font=f) + 48
        d.rectangle([80, y, 80 + kw, y + 66], fill=GREEN); d.text((104, y + 9), k_.upper(), font=f, fill="white")
        y += 96; f = font("ExtraBold", 130)
        for ln in wrap(d, h_.upper(), f, W - 200):
            d.text((80, y), ln, font=f, fill="white"); y += 128
        d.text((84, y + 30), s_, font=font("Medium", 50), fill="white")
    else:
        y = (1040 if is_gen(key) else 880) if is_photo(key) else 340
        if seg["label"]:
            f = font("Bold", 42); lw = d.textlength(seg["label"].upper(), font=f) + 48
            d.rectangle([80, y, 80 + lw, y + 68], fill=GREEN); d.text((104, y + 10), seg["label"].upper(), font=f, fill="white")
        y += 90; f = font("ExtraBold", 96)
        if not is_photo(key): f = font("ExtraBold", 80)
        for ln in wrap(d, seg["title"].upper(), f, W - 220)[:2]:
            d.text((80, y), ln, font=f, fill=txt); y += 96 if is_photo(key) else 82
        if key == "PRODUCTS": product_grid(o, d, pid, y + 20)
    if is_gen(key):
        d.text((W - 120, 326), "Illustration · placeholder", font=nc(24), fill=(255, 255, 255, 210), anchor="ra")
    cred = M["credits"].get(key)
    if cred and not cred.startswith("Photo: friedmanshome"):
            d.text((W - 120, 326), cred, font=nc(24), fill=(255, 255, 255, 200), anchor="ra")
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
    parts = re.split(r"(?<=[.?!])\s+", t.strip())
    out = []
    for p in parts:  # merge very short sentences into the previous one
        if out and len(p.split()) <= 3: out[-1] += " " + p
        else: out.append(p)
    chunks = []
    for p in out:  # keep each caption to 3 lines: split long sentences at commas, then by words
        w = p.split()
        if len(w) <= 13: chunks.append(p); continue
        parts, cur = [], []
        for word in w:
            cur.append(word)
            if (word.endswith(",") and len(cur) >= 5) or len(cur) >= 12: parts.append(" ".join(cur)); cur = []
        if cur:
            if len(cur) <= 2 and parts: parts[-1] += " " + " ".join(cur)
            else: parts.append(" ".join(cur))
        chunks += parts
    return chunks

def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())

def silences(f):
    r = subprocess.run(["ffmpeg", "-i", f, "-af", "silencedetect=noise=-35dB:d=0.25", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    return [((a + b) / 2, b - a) for a, b in zip(st, en)]

def boundaries(texts, total, sil):
    """Segment start times: estimate by character share, snap to the nearest pause."""
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
    """Animated Friedman's logo end card, rendered frame by frame."""
    lg = Image.open(os.path.join(D, M["logo"]["file"])).convert("RGBA")
    lh = 96; lw = round(lg.width * lh / lg.height); lg = lg.resize((lw, lh), Image.LANCZOS)
    pad = 44; plate = Image.new("RGBA", (lw + 2 * pad, lh + 2 * pad), "white"); plate.alpha_composite(lg, (pad, pad))
    fdir = os.path.join(wd, "outro"); os.makedirs(fdir, exist_ok=True)
    N = round(L * 30); cy = 820
    for fi in range(N):
        t = fi / 30
        fr = Image.new("RGBA", (W, H), CHAR); d = ImageDraw.Draw(fr)
        # green bar wipe
        bw = int(W * ease_out(t / 0.45)); d.rectangle([0, cy + 170, bw, cy + 186], fill=GREEN)
        # logo plate pops in
        k = ease_back((t - 0.1) / 0.6)
        if k > 0.01:
            pw, ph = max(1, int(plate.width * k)), max(1, int(plate.height * k))
            p = plate.resize((pw, ph), Image.LANCZOS)
            a = min(1, (t - 0.1) / 0.25); p.putalpha(p.getchannel("A").point(lambda v: int(v * a)))
            fr.alpha_composite(p, ((W - pw) // 2, cy - ph // 2))
        # tagline and site slide up
        for (txt, f, col, t0, y0) in [("THE HUMAN SIDE OF HOME IMPROVEMENT", font("Bold", 46), LIME, 0.7, cy + 250),
                                      ("friedmanshome.com", font("SemiBold", 54), "white", 1.0, cy + 340),
                                      ("Santa Rosa · Petaluma · Sonoma · Ukiah", nc(38), (220, 220, 220), 1.2, cy + 420)]:
            e = ease_out((t - t0) / 0.5)
            if e > 0:
                layer = Image.new("RGBA", (W, 90), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
                ld.text((W // 2, 45), txt, font=f, fill=col, anchor="mm")
                layer.putalpha(layer.getchannel("A").point(lambda v: int(v * e)))
                fr.alpha_composite(layer, (0, int(y0 + (1 - e) * 40)))
        fr.convert("RGB").save(f"{fdir}/f{fi:04d}.jpg", quality=92)
    out = f"{wd}/outro.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", f"{fdir}/f%04d.jpg", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", out], check=True)
    return out

def build(pid):
    pid = int(pid); P = S[str(pid)]; segs = P["segs"]; n = len(segs)
    wd = os.path.join(D, f"build2_{pid}"); os.makedirs(wd, exist_ok=True)
    vo = os.path.join(D, f"v2vo{pid}.mp3"); bed = os.path.join(D, "music_bed.mp3"); sting = os.path.join(D, "music_sting.mp3")
    vlen = dur(vo); HOLD = 1.0
    OUT_L = max(4.0, min(6.0, dur(sting))) if os.path.exists(sting) else 4.0
    b = boundaries([s["t"] for s in segs], vlen, silences(vo)); b[-1] = vlen + HOLD
    parts = []
    for i, seg in enumerate(segs):
        t0, t1 = b[i], b[i + 1]; L = t1 - t0
        bg = background(pid, seg["img"]); bg.save(f"{wd}/bg{i}.jpg", quality=92)
        overlay(pid, i, seg, n).save(f"{wd}/ov{i}.png")
        inputs = ["-loop", "1", "-framerate", "30", "-t", f"{L:.3f}", "-i", f"{wd}/bg{i}.jpg", "-i", f"{wd}/ov{i}.png"]
        fr = round(L * 30); z = "1.0+0.09*on/%d" % max(fr, 1)
        if i % 2: z = "1.09-0.09*on/%d" % max(fr, 1)
        filt = f"[0:v]scale={int(W*1.1)}:{int(H*1.1)},zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30[bg];[bg][1:v]overlay=0:0[v0]"
        last = "v0"
        if seg["img"] not in ("CTA", "PRODUCTS"):
            sents = sentences(seg["t"]); lens = [len(s) for s in sents]; acc = 0
            for j, s_ in enumerate(sents):
                a = (t1 - t0) * acc / sum(lens); acc += lens[j]; e = (t1 - t0) * acc / sum(lens) if j < len(sents) - 1 else L
                caption(s_).save(f"{wd}/cap{i}_{j}.png"); inputs += ["-i", f"{wd}/cap{i}_{j}.png"]
                filt += f";[{last}][{2+j}:v]overlay=0:1220:enable='between(t,{a:.3f},{e:.3f})'[c{j}]"; last = f"c{j}"
        out = f"{wd}/seg{i}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", filt, "-map", f"[{last}]", "-t", f"{L:.3f}", "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20", out], check=True)
        parts.append(out)
    parts.append(outro(wd, OUT_L))
    open(f"{wd}/list.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{wd}/list.txt", "-c", "copy", f"{wd}/video.mp4"], check=True)
    T = dur(f"{wd}/video.mp4"); outro_at = vlen + HOLD
    # mix: voice (normalized) + music bed ducked under the voice, faded before the outro + jingle sting on the logo
    fc = (f"[1:a]aresample=44100,aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-1.5:LRA=11,apad=whole_dur={T:.3f}[vx];"
          f"[vx]asplit=2[vmix][vsc];"
          f"[2:a]aresample=44100,aformat=channel_layouts=stereo,atrim=0:{outro_at+0.6:.3f},volume=0.30,afade=t=in:d=0.6,afade=t=out:st={outro_at-0.6:.3f}:d=1.2[bed0];"
          f"[bed0][vsc]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=350:makeup=1[bed];")
    inputs = ["-i", f"{wd}/video.mp4", "-i", vo, "-i", bed]
    if os.path.exists(sting):
        inputs += ["-i", sting]
        fc += f"[3:a]aresample=44100,aformat=channel_layouts=stereo,volume=0.9,adelay={int(outro_at*1000)}|{int(outro_at*1000)},afade=t=out:st={T-0.8:.3f}:d=0.8[st];[vmix][bed][st]amix=inputs=3:normalize=0:duration=first[mx];"
    else:
        fc += "[vmix][bed]amix=inputs=2:normalize=0:duration=first[mx];"
    fc += f"[mx]alimiter=limit=0.89,atrim=0:{T:.3f}[a]"
    out = os.path.join(D, f"friedmans-tiktok-v2-{pid}.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print(pid, "segments", [round(x, 2) for x in b], "->", out, round(dur(out), 1), "s")

if __name__ == "__main__":
    for p in sys.argv[1:]: build(p)
