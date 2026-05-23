"""Renders the SMT Agentic full process flowchart."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 680, 1420
BG          = (248, 249, 252)
WHITE       = (255, 255, 255)

# colour palette per lane
C_START     = (34,  139,  34)   # green  – start/end
C_CONFIG    = (45,   95, 160)   # blue   – config / user action
C_APP       = (130,  70, 180)   # purple – app launch
C_LOGIN     = (200,  90,  20)   # orange – login steps
C_NAV       = (20,  140, 160)   # teal   – navigation
C_FORM      = (160,  40,  80)   # rose   – form filling
C_OUTPUT    = (34,  139,  34)   # green  – output
C_DECISION  = (210, 150,  10)   # amber  – decision diamonds
C_ERROR     = (190,  40,  40)   # red    – error path

ARROW       = (80,  90, 110)
TEXT_DARK   = (20,  22,  30)
TEXT_LIGHT  = (255, 255, 255)

img = Image.new("RGB", (W, H), BG)
d   = ImageDraw.Draw(img)

# ── fonts ─────────────────────────────────────────────────────────────────────
def font(size, bold=False):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

FB  = font(11, bold=True)
FR  = font(10)
FS  = font(9)
FT  = font(14, bold=True)
FL  = font(9)

# ── helpers ───────────────────────────────────────────────────────────────────
def rrect(xy, color, r=8):
    x1,y1,x2,y2 = xy
    d.rectangle([x1+r,y1,x2-r,y2], fill=color)
    d.rectangle([x1,y1+r,x2,y2-r], fill=color)
    for ex,ey in [(x1,y1),(x2-2*r,y1),(x1,y2-2*r),(x2-2*r,y2-2*r)]:
        d.ellipse([ex,ey,ex+2*r,ey+2*r], fill=color)

def box(cx, y, w, h, color, lines, small=False):
    """Draw a process box centred at cx."""
    x1,y1,x2,y2 = cx-w//2, y, cx+w//2, y+h
    # shadow
    d.rectangle([x1+3,y1+3,x2+3,y2+3], fill=(200,202,210))
    rrect([x1,y1,x2,y2], color)
    # text
    ff = FS if small else FR
    total = len(lines)
    line_h = 13 if small else 15
    start_y = y1 + (h - total*line_h)//2
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=ff)
        d.text((cx - tw//2, start_y + i*line_h), ln, font=ff, fill=TEXT_LIGHT)
    return (x1, y1, x2, y2)

def diamond(cx, y, w, h, color, lines):
    """Draw a decision diamond."""
    mx, my = cx, y+h//2
    pts = [(cx, y), (cx+w//2, y+h//2), (cx, y+h), (cx-w//2, y+h//2)]
    # shadow
    spts = [(x+3,yy+3) for x,yy in pts]
    d.polygon(spts, fill=(200,202,210))
    d.polygon(pts, fill=color)
    total = len(lines)
    line_h = 13
    start_y = my - (total*line_h)//2
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=FS)
        d.text((cx-tw//2, start_y+i*line_h), ln, font=FS, fill=TEXT_LIGHT)
    return pts

def arrow_down(cx, y1, y2, label=None):
    d.line([(cx,y1),(cx,y2-6)], fill=ARROW, width=2)
    d.polygon([(cx-5,y2-8),(cx+5,y2-8),(cx,y2)], fill=ARROW)
    if label:
        tw = d.textlength(label, font=FL)
        d.text((cx+6, (y1+y2)//2 - 6), label, font=FL, fill=(80,90,110))

def arrow_side(x1, y, x2, label=None, color=ARROW):
    d.line([(x1,y),(x2-6,y)], fill=color, width=2)
    d.polygon([(x2-8,y-4),(x2-8,y+4),(x2,y)], fill=color)
    if label:
        d.text(((x1+x2)//2-10, y-14), label, font=FL, fill=color)

def label_box(cx, y, text, color):
    tw = d.textlength(text, font=FL)
    pad = 6
    x1,x2 = cx-tw//2-pad, cx+tw//2+pad
    d.rectangle([x1,y,x2,y+14], fill=color)
    d.text((x1+pad, y+1), text, font=FL, fill=TEXT_LIGHT)

# ══════════════════════════════════════════════════════════════════════════════
CX  = W // 2      # main centre x
SW  = 380         # standard box width
SH  = 40          # standard box height
DW  = 200         # diamond width
DH  = 52          # diamond height

# ── Title ─────────────────────────────────────────────────────────────────────
d.rectangle([0,0,W,50], fill=(30,50,90))
title = "SMT Agentic — Automation Process Flow"
tw = d.textlength(title, font=FT)
d.text(((W-tw)//2, 15), title, font=FT, fill=WHITE)

# lane backgrounds
d.rectangle([0,50,W,H], fill=BG)

y = 68

# ─────────────────────────────────────────────────────────────────────────────
# 1. START
box(CX, y, 160, SH, C_START, ["▶  START"])
y += SH
arrow_down(CX, y, y+24)
y += 24

# ─────────────────────────────────────────────────────────────────────────────
# 2. Config dialog
box(CX, y, SW, SH, C_CONFIG, ["Open Config Dialog", "(pre-filled from last session)"])
y += SH
arrow_down(CX, y, y+24)
y += 24

box(CX, y, SW, SH, C_CONFIG, ["User sets parameters:", "Line, Station, DT1/DT2, Model, WO, FixNO, Shift"])
y += SH
arrow_down(CX, y, y+24)
y += 24

# Decision: Run or Cancel?
diamond(CX, y, DW, DH, C_DECISION, ["Click", "Run or Cancel?"])
dm_y = y
dm_h = DH
y += DH
arrow_down(CX, y, y+20, "Run")
y += 20

# Cancel path (right side exit)
cancel_x = CX + DW//2
cancel_y = dm_y + DH//2
d.line([(cancel_x, cancel_y),(cancel_x+70, cancel_y)], fill=C_ERROR, width=2)
d.line([(cancel_x+70, cancel_y),(cancel_x+70, cancel_y+30)], fill=C_ERROR, width=2)
d.polygon([(cancel_x+64,cancel_y+28),(cancel_x+76,cancel_y+28),(cancel_x+70,cancel_y+36)], fill=C_ERROR)
label_box(cancel_x+70, cancel_y-16, "Cancel", C_ERROR)
box(cancel_x+70-60, cancel_y+36, 120, 30, C_ERROR, ["Exit"])

# ─────────────────────────────────────────────────────────────────────────────
# 3. App launch
box(CX, y, SW, SH, C_APP, ["Launch MainMenu_QMB.exe", "(skip if already running)"])
y += SH
arrow_down(CX, y, y+20)
y += 20

# Decision: app running?
diamond(CX, y, DW+20, DH, C_DECISION, ["SMT window", "visible?"])
already_y = y + DH//2
already_x = CX - (DW+20)//2
d.line([(already_x, already_y),(already_x-50, already_y)], fill=(60,160,60), width=2)
d.line([(already_x-50, already_y),(already_x-50, already_y+DH//2+SH//2)], fill=(60,160,60), width=2)
label_box(already_x-50, already_y-14, "Yes → skip", (60,160,60))
y += DH
arrow_down(CX, y, y+20, "No → wait")
y += 20

# ─────────────────────────────────────────────────────────────────────────────
# 4. LOGIN STEP 1
d.line([0, y-4, W, y-4], fill=(220,225,235), width=1)
label_box(CX, y-4, " LOGIN STEP 1 ", C_LOGIN)
y += 10
box(CX, y, SW, SH, C_LOGIN, ["Dialog 1: SMT Shop Floor Mgmt V3.4 PU9"])
y += SH
box(CX, y, SW, SH, C_LOGIN, ["Select  Line = C20", "Select  Station = Monitor"])
y += SH
box(CX, y, SW, 32, C_LOGIN, ["Click  Login"])
y += 32
arrow_down(CX, y, y+20)
y += 20

# ─────────────────────────────────────────────────────────────────────────────
# 5. LOGIN STEP 2
label_box(CX, y-4, " LOGIN STEP 2 ", C_LOGIN)
y += 10
box(CX, y, SW, SH, C_LOGIN, ["Dialog 2: Credential Login"])
y += SH
box(CX, y, SW, SH, C_LOGIN, ["Enter  UID  (from config)", "Enter  Password  (from Windows Credential Mgr)"])
y += SH
box(CX, y, SW, 32, C_LOGIN, ["Click  Login"])
y += 32
arrow_down(CX, y, y+20)
y += 20

# ─────────────────────────────────────────────────────────────────────────────
# 6. RTMS main window
d.line([0, y-4, W, y-4], fill=(220,225,235), width=1)
label_box(CX, y-4, " NAVIGATION ", C_NAV)
y += 10
box(CX, y, SW, SH, C_NAV, ["RTMS Main Window appears", "(Real Time Monitor System)"])
y += SH
arrow_down(CX, y, y+20)
y += 20

box(CX, y, SW, 32, C_NAV, ["Click menu:  ICT  →  ICTMoniter"])
y += 32
arrow_down(CX, y, y+20)
y += 20

box(CX, y, SW, SH, C_NAV, ["ICT Status window opens", "[ICT Status[2011/01/12]]"])
y += SH
arrow_down(CX, y, y+20)
y += 20

# ─────────────────────────────────────────────────────────────────────────────
# 7. FILL FORM
d.line([0, y-4, W, y-4], fill=(220,225,235), width=1)
label_box(CX, y-4, " FORM FILL ", C_FORM)
y += 10

form_fields = [
    "Set  DT1  date + time  (e.g. 2026/05/23  0800)",
    "Set  DT2  date + time  (e.g. 2026/05/23  2000)",
    "Select  Line   dropdown",
    "Select  Station  dropdown",
    "Select  Model  dropdown",
    "Select  WO  dropdown",
    "Select  FixNO  dropdown",
    "Set  Shift  (Day / Middle / Night)",
    "Set  Group  (ByModel / ByWO)",
]
for field in form_fields:
    box(CX, y, SW, 28, C_FORM, [field], small=True)
    y += 28

arrow_down(CX, y, y+20)
y += 20

# ─────────────────────────────────────────────────────────────────────────────
# 8. REFRESH
d.line([0, y-4, W, y-4], fill=(220,225,235), width=1)
label_box(CX, y-4, " REFRESH & EXPORT ", C_OUTPUT)
y += 10

box(CX, y, SW, 32, (20,140,160), ["Click  RefreshStation  →  wait for station list"])
y += 32
arrow_down(CX, y, y+16)
y += 16

box(CX, y, SW, 32, (20,140,160), ["Click  RefreshData   →  wait for data load"])
y += 32
arrow_down(CX, y, y+16)
y += 16

box(CX, y, SW, 32, (20,140,160), ["Click  Report"])
y += 32
arrow_down(CX, y, y+20)
y += 20

# ─────────────────────────────────────────────────────────────────────────────
# 9. OUTPUT
box(CX, y, SW, SH, C_OUTPUT, ["📊  Excel opens automatically", "ICT Status report ready for review"])
y += SH
arrow_down(CX, y, y+20)
y += 20

# ─────────────────────────────────────────────────────────────────────────────
# 10. Log + END
box(CX, y, SW, 32, (80,90,110), ["Log result to  smt_agent.log"])
y += 32
arrow_down(CX, y, y+20)
y += 20

box(CX, y, 160, SH, C_START, ["■  END"])

# ── Legend ────────────────────────────────────────────────────────────────────
leg_y = H - 86
d.rectangle([12, leg_y, W-12, H-12], fill=(235,237,245), outline=(180,185,200))
d.text((24, leg_y+6), "Legend:", font=FB, fill=TEXT_DARK)
items = [
    (C_CONFIG, "User / Config action"),
    (C_APP,    "App launch"),
    (C_LOGIN,  "Login steps"),
    (C_NAV,    "Navigation"),
    (C_FORM,   "Form fill"),
    (C_OUTPUT, "Output / Export"),
    (C_DECISION,"Decision"),
]
lx = 24
for color, label in items:
    rrect([lx, leg_y+22, lx+16, leg_y+36], color, r=3)
    d.text((lx+20, leg_y+23), label, font=FL, fill=TEXT_DARK)
    lx += d.textlength(label, font=FL) + 36

out = "/home/user/SMT-Agentic/prototype/flowchart.png"
img.save(out, dpi=(144,144))
print(f"Saved: {out}  (size {W}x{H})")
