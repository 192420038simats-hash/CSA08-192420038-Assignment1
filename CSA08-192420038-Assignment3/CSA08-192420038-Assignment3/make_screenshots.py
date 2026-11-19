"""Renders each program's captured output as a terminal-style PNG into <Task>/screenshots/.
NOTE: these are rendered images of the captured output. Replace them with your own screenshots from your own runs."""
import glob, os, subprocess
from PIL import Image, ImageDraw, ImageFont

FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
BOLD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 15)
LH, PAD, BAR = 21, 16, 34
BG, FG, GREEN, BARC = (30, 30, 30), (220, 220, 220), (120, 220, 120), (60, 60, 60)
count = 0
for task in sorted(glob.glob("Q*")):
    os.makedirs(f"{task}/screenshots", exist_ok=True)
    for out in sorted(glob.glob(f"{task}/output_*.txt")):
        prog = os.path.basename(out)[len("output_"):-4] + ".py"
        if prog == "make_session.py": continue
        lines = open(out, encoding="utf-8").read().rstrip("\n").split("\n")
        lines = [l.replace("\t", "    ") for l in lines]
        if len(lines) > 60: lines = lines[:60] + ["... (output continues in the output_*.txt file)"]
        header = f"~/CSA08-Assignment3/{task}$ python3 {prog}"
        width = max(FONT.getlength(l) for l in lines + [header]) + 2 * PAD
        height = BAR + PAD + LH * (len(lines) + 1) + PAD
        img = Image.new("RGB", (int(max(width, 640)), height), BG)
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, img.width, BAR], fill=BARC)
        for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
            d.ellipse([12 + i * 22, 10, 24 + i * 22, 22], fill=c)
        d.text((90, 8), f"{task} - terminal", font=FONT, fill=FG)
        y = BAR + PAD
        d.text((PAD, y), header, font=BOLD, fill=GREEN); y += LH
        for l in lines:
            d.text((PAD, y), l, font=FONT, fill=FG); y += LH
        name = f"{task}/screenshots/{prog[:-3]}.png"
        img.save(name); count += 1
print("screenshots created:", count)
