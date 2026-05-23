"""Renders a pixel-accurate mockup of the SMT Agentic config dialog."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 560, 720
BG       = (240, 240, 245)
TITLEBAR = (45,  95, 160)
SECTION  = (210, 220, 235)
WHITE    = (255, 255, 255)
BORDER   = (160, 170, 185)
TEXT     = (30,  30,  40)
LABEL    = (70,  80, 100)
BTN_RUN  = (45,  95, 160)
BTN_CANCEL=(150,155,165)
BTN_TEXT = (255,255,255)
ACCENT   = (45,  95, 160)
RADIO_ON = (45,  95, 160)
RED_HINT = (210,  60,  60)
PLACEHOLDER=(160,165,175)

img = Image.new("RGB", (W, H), BG)
d   = ImageDraw.Draw(img)

# ── font helpers ──────────────────────────────────────────────────────────────
def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_TITLE  = font(13, bold=True)
F_SECT   = font(10, bold=True)
F_LABEL  = font(10)
F_INPUT  = font(10)
F_BTN    = font(11, bold=True)
F_SMALL  = font(9)

# ── helpers ───────────────────────────────────────────────────────────────────
def roundrect(draw, xy, r, fill, outline=None, width=1):
    x1,y1,x2,y2 = xy
    draw.rectangle([x1+r,y1,x2-r,y2], fill=fill)
    draw.rectangle([x1,y1+r,x2,y2-r], fill=fill)
    draw.ellipse([x1,y1,x1+2*r,y1+2*r], fill=fill)
    draw.ellipse([x2-2*r,y1,x2,y1+2*r], fill=fill)
    draw.ellipse([x1,y2-2*r,x1+2*r,y2], fill=fill)
    draw.ellipse([x2-2*r,y2-2*r,x2,y2], fill=fill)
    if outline:
        draw.rectangle([x1+r,y1,x2-r,y1+width], fill=outline)
        draw.rectangle([x1+r,y2-width,x2-r,y2], fill=outline)
        draw.rectangle([x1,y1+r,x1+width,y2-r], fill=outline)
        draw.rectangle([x2-width,y1+r,x2,y2-r], fill=outline)

def text_field(draw, x, y, w, value, placeholder=False, pw=False):
    h = 26
    draw.rectangle([x,y,x+w,y+h], fill=WHITE, outline=BORDER)
    # blue bottom border (focus style)
    draw.line([x+1, y+h-1, x+w-1, y+h-1], fill=ACCENT, width=2)
    val = "●" * len(value) if pw else value
    col = PLACEHOLDER if placeholder else TEXT
    draw.text((x+6, y+6), val, font=F_INPUT, fill=col)

def dropdown(draw, x, y, w, value, placeholder=False):
    h = 26
    col = PLACEHOLDER if placeholder else TEXT
    draw.rectangle([x,y,x+w,y+h], fill=WHITE, outline=BORDER)
    draw.text((x+6, y+6), value, font=F_INPUT, fill=col)
    # arrow
    ax = x+w-18
    ay = y+10
    draw.polygon([(ax,ay),(ax+10,ay),(ax+5,ay+7)], fill=LABEL)

def button(draw, x, y, w, h, label, bg, fg=BTN_TEXT):
    roundrect(draw, [x,y,x+w,y+h], 4, bg)
    tw = draw.textlength(label, font=F_BTN)
    draw.text((x+(w-tw)//2, y+(h-14)//2), label, font=F_BTN, fill=fg)

def section_header(draw, y, label):
    draw.rectangle([0, y, W, y+24], fill=SECTION)
    draw.text((16, y+5), label, font=F_SECT, fill=ACCENT)
    return y+24

def radio(draw, x, y, label, on=False):
    cx,cy = x+7, y+7
    draw.ellipse([cx-6,cy-6,cx+6,cy+6], outline=ACCENT, width=2, fill=WHITE)
    if on:
        draw.ellipse([cx-3,cy-3,cx+3,cy+3], fill=ACCENT)
    draw.text((x+18, y), label, font=F_LABEL, fill=TEXT)

def checkbox(draw, x, y, label, checked=False):
    draw.rectangle([x,y,x+14,y+14], outline=ACCENT, fill=WHITE, width=2)
    if checked:
        draw.line([x+2,y+7,x+5,y+12], fill=ACCENT, width=2)
        draw.line([x+5,y+12,x+12,y+3], fill=ACCENT, width=2)
    draw.text((x+20, y), label, font=F_LABEL, fill=TEXT)

# ══════════════════════════════════════════════════════════════════════════════
# Title bar
d.rectangle([0,0,W,44], fill=TITLEBAR)
d.text((16,13), "SMT Agentic  —  Session Configuration", font=F_TITLE, fill=WHITE)
# close button
d.rectangle([W-36,8,W-8,36], fill=(200,60,60))
d.text((W-27,14), "✕", font=F_LABEL, fill=WHITE)

y = 44

# ── Section: Application ──────────────────────────────────────────────────────
y = section_header(d, y, "  APPLICATION")
y += 8
d.text((16, y+6), "EXE Path", font=F_LABEL, fill=LABEL)
text_field(d, 16, y+22, 400, r"C:\Users\T4060033\OneDrive - quantacn.com\Desktop\MainMenu_QMB.exe"[:46]+"…")
button(d, 424, y+22, 120, 26, "Browse…", (100,110,130))
y += 62

# ── Section: Credentials ─────────────────────────────────────────────────────
y = section_header(d, y, "  CREDENTIALS")
y += 8
# UID
d.text((16, y+6), "UID", font=F_LABEL, fill=LABEL)
text_field(d, 16, y+22, 240, "t4060033")
# Password
d.text((272, y+6), "Password", font=F_LABEL, fill=LABEL)
text_field(d, 272, y+22, 272, "••••••••••••••••••••", pw=False)
y += 62

# ── Section: Line / Station ───────────────────────────────────────────────────
y = section_header(d, y, "  LINE SETUP")
y += 8
d.text((16, y+6),  "Line",    font=F_LABEL, fill=LABEL)
dropdown(d, 16,  y+22, 240, "C20")
d.text((272, y+6), "Station", font=F_LABEL, fill=LABEL)
dropdown(d, 272, y+22, 272, "Monitor")
y += 62

# ── Section: ICT Parameters ───────────────────────────────────────────────────
y = section_header(d, y, "  ICT PARAMETERS")
y += 8
# DT1
d.text((16, y+6),  "DT1  (From)",  font=F_LABEL, fill=LABEL)
text_field(d, 16,  y+22, 160, "2026/05/23")
text_field(d, 184, y+22, 70,  "0800")
# DT2
d.text((272, y+6), "DT2  (To)",    font=F_LABEL, fill=LABEL)
text_field(d, 272, y+22, 160, "2026/05/23")
text_field(d, 440, y+22, 70,  "2000")
y += 54

# Model / WO
d.text((16, y+6),  "Model",  font=F_LABEL, fill=LABEL)
dropdown(d, 16,  y+22, 240, "— select —", placeholder=True)
d.text((272, y+6), "WO",     font=F_LABEL, fill=LABEL)
dropdown(d, 272, y+22, 272, "— select —", placeholder=True)
y += 54

# FixNO
d.text((16, y+6), "FixNO", font=F_LABEL, fill=LABEL)
dropdown(d, 16, y+22, 240, "— select —", placeholder=True)
y += 54

# ── Section: Options ─────────────────────────────────────────────────────────
y = section_header(d, y, "  OPTIONS")
y += 10

# ByModel / ByWO
d.text((16, y), "Group by", font=F_LABEL, fill=LABEL)
radio(d, 100, y, "ByModel", on=True)
radio(d, 200, y, "ByWO",    on=False)
checkbox(d, 320, y, "ShowPassDetail", checked=False)
y += 28

# Shift
d.text((16, y), "Shift", font=F_LABEL, fill=LABEL)
radio(d, 100, y, "Day Shift",    on=True)
radio(d, 210, y, "Middle Shift", on=False)
radio(d, 335, y, "Night Shift",  on=False)
y += 20

# ── Bottom bar ────────────────────────────────────────────────────────────────
y = H - 58
d.rectangle([0, y, W, H], fill=(225,228,235))
d.line([0, y, W, y], fill=BORDER, width=1)

# Auto-start toggle
checkbox(d, 16, y+18, "Auto-start on next session", checked=True)

# Buttons
button(d, W-270, y+10, 120, 36, "▶  Run", BTN_RUN)
button(d, W-138, y+10, 120, 36, "Cancel", BTN_CANCEL)

# ── Subtle drop shadow on dialog ─────────────────────────────────────────────
# (already done by BG)

out = "/home/user/SMT-Agentic/prototype/ui_mockup.png"
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, dpi=(144, 144))
print(f"Saved: {out}")
