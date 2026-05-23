"""Renders a pixel-accurate mockup of the SMT Agentic config dialog."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 560, 820
BG          = (240, 240, 245)
TITLEBAR    = (45,  95, 160)
SECTION     = (210, 220, 235)
WHITE       = (255, 255, 255)
BORDER      = (160, 170, 185)
TEXT        = (30,  30,  40)
LABEL       = (70,  80, 100)
BTN_RUN     = (34, 139,  34)
BTN_CANCEL  = (150,155,165)
BTN_TEXT    = (255,255,255)
ACCENT      = (45,  95, 160)
PLACEHOLDER = (160,165,175)
GREEN_LIGHT = (220, 245, 220)
GREEN_BORDER= (100, 180, 100)
GREEN_TEXT  = (30,  110,  30)
FLOW_BG     = (248, 250, 255)
FLOW_ARROW  = (45,   95, 160)

img = Image.new("RGB", (W, H), BG)
d   = ImageDraw.Draw(img)

# ── fonts ─────────────────────────────────────────────────────────────────────
def font(size, bold=False):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_TITLE = font(13, bold=True)
F_SECT  = font(10, bold=True)
F_LABEL = font(10)
F_INPUT = font(10)
F_BTN   = font(11, bold=True)
F_SMALL = font(9)
F_FLOW  = font(9, bold=True)

# ── drawing helpers ───────────────────────────────────────────────────────────
def roundrect(draw, xy, r, fill, outline=None, lw=1):
    x1,y1,x2,y2 = xy
    draw.rectangle([x1+r,y1,x2-r,y2], fill=fill)
    draw.rectangle([x1,y1+r,x2,y2-r], fill=fill)
    for ex,ey in [(x1,y1),(x2-2*r,y1),(x1,y2-2*r),(x2-2*r,y2-2*r)]:
        draw.ellipse([ex,ey,ex+2*r,ey+2*r], fill=fill)
    if outline:
        draw.rectangle([x1+r,y1,x2-r,y1+lw], fill=outline)
        draw.rectangle([x1+r,y2-lw,x2-r,y2], fill=outline)
        draw.rectangle([x1,y1+r,x1+lw,y2-r], fill=outline)
        draw.rectangle([x2-lw,y1+r,x2,y2-r], fill=outline)

def text_field(draw, x, y, w, value, placeholder=False, pw=False):
    h = 26
    draw.rectangle([x,y,x+w,y+h], fill=WHITE, outline=BORDER)
    draw.line([x+1,y+h-1,x+w-1,y+h-1], fill=ACCENT, width=2)
    col = PLACEHOLDER if placeholder else TEXT
    draw.text((x+6, y+6), "●"*len(value) if pw else value, font=F_INPUT, fill=col)

def dropdown(draw, x, y, w, value, placeholder=False):
    col = PLACEHOLDER if placeholder else TEXT
    draw.rectangle([x,y,x+w,y+26], fill=WHITE, outline=BORDER)
    draw.text((x+6, y+6), value, font=F_INPUT, fill=col)
    ax = x+w-18; ay = y+10
    draw.polygon([(ax,ay),(ax+10,ay),(ax+5,ay+7)], fill=LABEL)

def button(draw, x, y, w, h, label, bg, fg=BTN_TEXT):
    roundrect(draw, [x,y,x+w,y+h], 4, bg)
    tw = draw.textlength(label, font=F_BTN)
    draw.text((x+(w-tw)//2, y+(h-14)//2), label, font=F_BTN, fill=fg)

def section_header(draw, y, label):
    draw.rectangle([0,y,W,y+24], fill=SECTION)
    draw.text((16,y+5), label, font=F_SECT, fill=ACCENT)
    return y+24

def radio(draw, x, y, label, on=False):
    cx,cy = x+7, y+7
    draw.ellipse([cx-6,cy-6,cx+6,cy+6], outline=ACCENT, width=2, fill=WHITE)
    if on:
        draw.ellipse([cx-3,cy-3,cx+3,cy+3], fill=ACCENT)
    draw.text((x+18, y), label, font=F_LABEL, fill=TEXT)

def checkbox(draw, x, y, label, checked=False, label_col=None):
    draw.rectangle([x,y,x+14,y+14], outline=ACCENT, fill=WHITE, width=2)
    if checked:
        draw.line([x+2,y+7,x+5,y+12], fill=ACCENT, width=2)
        draw.line([x+5,y+12,x+12,y+3], fill=ACCENT, width=2)
    draw.text((x+20, y), label, font=F_LABEL, fill=label_col or TEXT)

def flow_step(draw, x, y, w, h, icon, label, color=ACCENT):
    roundrect(draw, [x,y,x+w,y+h], 6, FLOW_BG, outline=color, lw=1)
    draw.text((x+8, y+4), icon,  font=F_FLOW, fill=color)
    draw.text((x+8, y+16), label, font=F_SMALL, fill=TEXT)

def arrow(draw, x, y):
    draw.line([x,y,x,y+10], fill=FLOW_ARROW, width=2)
    draw.polygon([(x-4,y+8),(x+4,y+8),(x,y+14)], fill=FLOW_ARROW)

# ══════════════════════════════════════════════════════════════════════════════
# Title bar
d.rectangle([0,0,W,44], fill=TITLEBAR)
d.text((16,13), "SMT Agentic  —  Session Configuration", font=F_TITLE, fill=WHITE)
d.rectangle([W-36,8,W-8,36], fill=(200,60,60))
d.text((W-29,14), "✕", font=F_LABEL, fill=WHITE)

# ── Flow strip (compact) ──────────────────────────────────────────────────────
y = 44
d.rectangle([0,y,W,y+38], fill=(230,235,245))
steps = [
    ("①","Login"),("→",None),("②","ICT Menu"),("→",None),
    ("③","Fill Form"),("→",None),("④","Refresh"),("→",None),("⑤","Report→Excel"),
]
sx = 8
sy = y+8
for icon, label in steps:
    if label is None:
        d.text((sx, sy+8), icon, font=F_SMALL, fill=FLOW_ARROW)
        sx += 18
    else:
        tw = max(draw.textlength(label, font=F_SMALL) for draw in [d]) + 16
        tw = max(tw, 62)
        col = (34,139,34) if "Excel" in label else ACCENT
        roundrect(d, [sx,sy,sx+tw,sy+22], 4, FLOW_BG, outline=col, lw=1)
        d.text((sx+4, sy+3),  icon,  font=F_FLOW,  fill=col)
        d.text((sx+4, sy+12), label, font=F_SMALL, fill=TEXT)
        sx += tw + 4

y += 42

# ── APPLICATION ───────────────────────────────────────────────────────────────
y = section_header(d, y, "  APPLICATION")
y += 8
d.text((16,y+6), "EXE Path", font=F_LABEL, fill=LABEL)
text_field(d, 16, y+22, 396, r"…\Desktop\MainMenu_QMB.exe")
button(d, 420, y+22, 124, 26, "Browse…", (100,110,130))
y += 58

# ── CREDENTIALS ───────────────────────────────────────────────────────────────
y = section_header(d, y, "  CREDENTIALS")
y += 8
d.text((16,y+6),  "UID",      font=F_LABEL, fill=LABEL)
text_field(d, 16,  y+22, 240, "t4060033")
d.text((272,y+6), "Password", font=F_LABEL, fill=LABEL)
text_field(d, 272, y+22, 272, "●●●●●●●●●●●●●●●●●●●●")
y += 58

# ── LINE SETUP ────────────────────────────────────────────────────────────────
y = section_header(d, y, "  LINE SETUP")
y += 8
d.text((16,y+6),  "Line",    font=F_LABEL, fill=LABEL)
dropdown(d, 16,  y+22, 240, "C20")
d.text((272,y+6), "Station", font=F_LABEL, fill=LABEL)
dropdown(d, 272, y+22, 272, "Monitor")
y += 58

# ── ICT PARAMETERS ────────────────────────────────────────────────────────────
y = section_header(d, y, "  ICT PARAMETERS")
y += 8
d.text((16,y+6),  "DT1  (From)", font=F_LABEL, fill=LABEL)
text_field(d, 16,  y+22, 155, "2026/05/23")
text_field(d, 178, y+22, 68,  "0800")
d.text((272,y+6), "DT2  (To)",   font=F_LABEL, fill=LABEL)
text_field(d, 272, y+22, 155, "2026/05/23")
text_field(d, 434, y+22, 68,  "2000")
y += 50

d.text((16,y+6),  "Model", font=F_LABEL, fill=LABEL)
dropdown(d, 16,  y+22, 240, "— select —", placeholder=True)
d.text((272,y+6), "WO",    font=F_LABEL, fill=LABEL)
dropdown(d, 272, y+22, 272, "— select —", placeholder=True)
y += 50

d.text((16,y+6), "FixNO", font=F_LABEL, fill=LABEL)
dropdown(d, 16, y+22, 240, "— select —", placeholder=True)
y += 50

# ── OPTIONS ───────────────────────────────────────────────────────────────────
y = section_header(d, y, "  OPTIONS")
y += 10
d.text((16,y),   "Group by", font=F_LABEL, fill=LABEL)
radio(d, 100, y, "ByModel", on=True)
radio(d, 200, y, "ByWO",    on=False)
checkbox(d, 320, y, "ShowPassDetail", checked=False)
y += 26
d.text((16,y),   "Shift",      font=F_LABEL, fill=LABEL)
radio(d, 100, y, "Day Shift",    on=True)
radio(d, 210, y, "Middle Shift", on=False)
radio(d, 335, y, "Night Shift",  on=False)
y += 18

# ── OUTPUT ────────────────────────────────────────────────────────────────────
y = section_header(d, y, "  OUTPUT")
y += 10

# Green info box
d.rectangle([16,y,W-16,y+36], fill=GREEN_LIGHT, outline=GREEN_BORDER)
d.text((26, y+5),  "📊  Report → Excel", font=F_SECT,  fill=GREEN_TEXT)
d.text((26, y+20), "Clicking Report opens Excel automatically with ICT data.", font=F_SMALL, fill=GREEN_TEXT)
y += 46

checkbox(d, 16, y, "Auto-click Report after RefreshData", checked=True)
y += 22
checkbox(d, 16, y, "Keep Excel open after export",        checked=True)
y += 14

# ── Bottom bar ────────────────────────────────────────────────────────────────
y_bar = H - 60
d.rectangle([0,y_bar,W,H], fill=(225,228,235))
d.line([0,y_bar,W,y_bar], fill=BORDER, width=1)

checkbox(d, 16, y_bar+22, "Remember settings for next session", checked=True)
button(d, W-276, y_bar+12, 128, 36, "▶  Run",  BTN_RUN)
button(d, W-136, y_bar+12, 120, 36, "Cancel", BTN_CANCEL)

out = "/home/user/SMT-Agentic/prototype/ui_mockup.png"
img.save(out, dpi=(144,144))
print(f"Saved: {out}")
