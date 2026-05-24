from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import date

OUTPUT = "/home/user/powerhouse-fba-app/IRONCLAD_PPC_Audit_v2.pdf"

BRAND  = colors.HexColor("#1a1a2e")
ACCENT = colors.HexColor("#e94560")
GOLD   = colors.HexColor("#f5a623")
GREEN  = colors.HexColor("#27ae60")
RED    = colors.HexColor("#e74c3c")
ORANGE = colors.HexColor("#e67e22")
LIGHT  = colors.HexColor("#f8f8f8")
MID    = colors.HexColor("#e0e0e0")
DARK   = colors.HexColor("#2c2c2c")
WHITE  = colors.white
LGREY  = colors.HexColor("#666666")
BGGREEN= colors.HexColor("#d5f5e3")
BGRED  = colors.HexColor("#fde8e8")
BGGOLD = colors.HexColor("#fef9e7")

doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
    leftMargin=16*mm, rightMargin=16*mm, topMargin=14*mm, bottomMargin=14*mm)
styles = getSampleStyleSheet()

def sty(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

H1   = sty("H1",  fontSize=20, textColor=WHITE,  leading=26, fontName="Helvetica-Bold")
H1s  = sty("H1s", fontSize=10, textColor=colors.HexColor("#aaaaaa"), leading=14)
H2   = sty("H2",  fontSize=12, textColor=BRAND,  leading=17, fontName="Helvetica-Bold", spaceBefore=2)
H3   = sty("H3",  fontSize=9.5,textColor=ACCENT, leading=13, fontName="Helvetica-Bold")
BODY = sty("BD",  fontSize=8.5,textColor=DARK,   leading=13)
NOTE = sty("NT",  fontSize=7.5,textColor=LGREY,  leading=11, leftIndent=6)
WARN = sty("WN",  fontSize=8,  textColor=colors.HexColor("#7d4e00"), leading=12, leftIndent=6)
TH   = sty("TH",  fontSize=8,  textColor=WHITE,  leading=11, fontName="Helvetica-Bold", alignment=TA_CENTER)
TD   = sty("TD",  fontSize=7.5,textColor=DARK,   leading=11, alignment=TA_CENTER)
TDL  = sty("TDL", fontSize=7.5,textColor=DARK,   leading=11, alignment=TA_LEFT)
TDB  = sty("TDB", fontSize=7.5,textColor=DARK,   leading=11, fontName="Helvetica-Bold", alignment=TA_CENTER)
FOOT = sty("FT",  fontSize=7,  textColor=LGREY,  leading=10, alignment=TA_CENTER)

def th(t):  return Paragraph(t, TH)
def td(t):  return Paragraph(str(t), TD)
def tdb(t): return Paragraph(str(t), TDB)
def tdl(t): return Paragraph(str(t), TDL)
def tdr(t): return Paragraph(str(t), sty("tdr", fontSize=7.5, textColor=DARK, leading=11, alignment=TA_RIGHT))

W = 178*mm  # usable width

def tbl(data, widths, extra_style=None):
    t = Table(data, colWidths=widths)
    base = [
        ("BACKGROUND",    (0,0), (-1,0),  BRAND),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.35, MID),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]
    if extra_style:
        base.extend(extra_style)
    t.setStyle(TableStyle(base))
    return t

def section(title, sub=None):
    els = [Spacer(1, 5*mm),
           HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=3),
           Paragraph(title, H2)]
    if sub:
        els.append(Paragraph(sub, NOTE))
    els.append(Spacer(1, 2*mm))
    return els

def badge(text, bg):
    t = Table([[Paragraph(f"<b>{text}</b>",
        sty("bg", fontSize=7, textColor=WHITE, leading=9, alignment=TA_CENTER))]],
        colWidths=[24*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 3), ("RIGHTPADDING", (0,0), (-1,-1), 3),
    ]))
    return t

story = []

# ══ COVER ════════════════════════════════════════════════════════════════════
cover = Table([[
    Paragraph("IRONCLAD PPC Audit v2", H1),
    Paragraph(
        f"Amazon Australia &nbsp;|&nbsp; May 15–23, 2026<br/>"
        f"<font size=8 color='#aaaaaa'>Based on Campaign, Search Term &amp; Advertised Product reports<br/>"
        f"Generated {date.today().strftime('%d %b %Y')}</font>", H1s),
]], colWidths=[105*mm, 73*mm])
cover.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), BRAND),
    ("TOPPADDING",    (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("ALIGN",         (1,0), (1,0),   "RIGHT"),
]))
story.append(cover)
story.append(Spacer(1, 3*mm))

# ══ BATCH ECONOMICS ══════════════════════════════════════════════════════════
story += section("Batch Economics — Verified Numbers",
    "All analysis uses these exact figures. FBA fee A$14.48 confirmed (cubiscan). No estimates.")
eco = [
    [th(""), th("Batch 1 (current)"), th("Batch 2 (pending order)")],
    [tdl("Landed cost/unit"),    td("A$30.76"),       td("A$18.66")],
    [tdl("Net payout/unit"),     td("A$35.48"),       td("A$35.48")],
    [tdl("Gross profit/unit"),   tdb("A$4.72"),       tdb("A$16.82")],
    [tdl("Break-even ACoS"),     tdb("7.9–9.6%"),     tdb("~28%")],
    [tdl("Max CPC"),             tdb("A$0.65"),       tdb("A$1.90")],
    [tdl("Stock remaining"),     td("~50 units"),     td("400 (not ordered)")],
]
story.append(tbl(eco, [60*mm, 59*mm, 59*mm],
    [("BACKGROUND",(1,3),(1,-1),colors.HexColor("#fff3cd")),
     ("BACKGROUND",(2,3),(2,-1),BGGREEN)]))
story.append(Spacer(1,2*mm))
story.append(Paragraph(
    "CRITICAL RULE: Two separate break-even thresholds. Never apply a blended ACoS target across both batches.",
    sty("cr", fontSize=8, textColor=colors.HexColor("#7d4e00"), leading=12,
        borderColor=GOLD, borderWidth=0.5, borderPadding=5, backColor=BGGOLD)))

# ══ ACCOUNT SUMMARY ══════════════════════════════════════════════════════════
story += section("Campaign Summary — May 15–23 (9 days)")
story.append(Paragraph(
    "⚠  Auto-01 shows <b>A$15/day</b> budget in the Campaign report — brief states A$10/day. "
    "Verify in Seller Central and update brief if changed.", WARN))
story.append(Spacer(1,2*mm))

camp = [
    [th("Campaign"), th("Budget"), th("Imp"), th("Clicks"), th("Spend"), th("Utilisation"), th("ACoS"), th("ROAS"), th("Units"), th("Sales")],
    [tdl("Auto-01"),  td("A$15/day"), td("9,628"),  td("86"),  td("A$81.52"),  td("60.4%"),  tdb("24.9%"), td("4.01×"), td("6"),  td("A$327.24")],
    [tdl("Exact-01"), td("A$20/day"), td("11,691"), td("97"),  td("A$114.78"), td("63.8%"),  tdb("17.5%"), td("5.70×"), td("12"), td("A$654.48")],
    [tdl("PT-01"),    td("A$5/day"),  td("128"),    td("2"),   td("A$2.36"),   td("23.6%"),  tdb("—"),     td("0×"),    td("0"),  td("A$0.00")],
    [tdb("TOTAL"),    td("A$40/day"), td("21,447"), td("185"), tdb("A$198.66"),tdb("61.1%"), tdb("20.2%"), tdb("4.94×"),tdb("18"),tdb("A$981.72")],
]
story.append(tbl(camp,
    [30*mm, 18*mm, 17*mm, 14*mm, 20*mm, 20*mm, 16*mm, 14*mm, 12*mm, 17*mm],
    [("BACKGROUND",(0,4),(-1,4), colors.HexColor("#e8eaf6")),
     ("BACKGROUND",(6,1),(6,1), BGRED),
     ("BACKGROUND",(6,2),(6,2), BGGOLD),
     ("BACKGROUND",(6,3),(6,3), BGRED)]))

# ══ PROFITABILITY REALITY ════════════════════════════════════════════════════
story += section("Profitability Reality — 18 PPC Units")
pl = [
    [th(""), th("Batch 1 (current)"), th("Batch 2 (future)")],
    [tdl("18 units × gross profit"),       td("18 × A$4.72  = A$84.96"),  td("18 × A$16.82 = A$302.76")],
    [tdl("Less PPC spend"),                td("− A$198.66"),               td("− A$198.66")],
    [tdl("Net P&L this period"),           tdb("− A$113.70  LOSS"),        tdb("+ A$104.10  PROFIT")],
    [tdl("Opportunity cost of B1 vs B2"),  td(""),                         tdb("+ A$217.80 per 9-day period")],
]
story.append(tbl(pl, [55*mm, 62*mm, 61*mm],
    [("BACKGROUND",(1,3),(1,3), BGRED),
     ("BACKGROUND",(2,3),(2,3), BGGREEN),
     ("BACKGROUND",(2,4),(2,4), BGGREEN)]))
story.append(Spacer(1,2*mm))
story.append(Paragraph(
    "The ads are generating real sales and rank signal. "
    "The A$113.70 loss per 9 days is the deliberate cost of rank-building on Batch 1 economics. "
    "Every day Batch 2 is delayed costs ~A$24 in opportunity profit. Place the order.",
    BODY))

# ══ EXACT-01 CLEAN BASELINE ══════════════════════════════════════════════════
story += section("Exact-01 — Clean Baseline (May 21–23 only)",
    "May 15–20 data DISCARDED. +20% Product Pages adjustment active that period inflated spend and suppressed CVR.")

story.append(Paragraph(
    "<b>Under-spend alert:</b> Clean period average spend A$9.18/day vs A$20 budget = <b>46% utilisation</b>. "
    "Removing the +20% product pages adj on May 21 cut impressions on 'glass food storage containers' "
    "from ~1,000/day → ~440/day. Budget headroom is real — the new Rank campaign fills it correctly.",
    WARN))
story.append(Spacer(1,2*mm))

ex = [
    [th("Keyword"), th("Clicks"), th("Spend"), th("Sales"), th("ACoS"), th("CVR"), th("vs B1 9.6%"), th("vs B2 28%"), th("Verdict")],
    [tdl("glass food storage containers"), td("13"), td("A$13.08"), td("A$163.62"), tdb("8.0%"),  td("23%"), tdb("✓ INSIDE"), td("✓"), tdl("SCALE — at B1 ceiling, monitor daily")],
    [tdl("meal prep container glass"),     td("6"),  td("A$7.98"),  td("A$163.62"), tdb("4.9%"),  td("33%"), tdb("✓ STRONG"),td("✓"), tdl("SCALE — earmarked for Rank campaign")],
    [tdl("glass meal prep containers"),    td("1"),  td("A$1.48"),  td("A$0"),      tdb("∞"),     td("0%"),  tdb("✗"),       td("✗"), tdl("WATCH — cut bid to A$1.10, pause at 5+ clean clicks / 0 sale")],
    [tdl("borosilicate glass containers"), td("2"),  td("A$2.71"),  td("A$0"),      tdb("∞"),     td("0%"),  tdb("✗"),       td("✗"), tdl("CUT URGENT — bid A$1.50→A$0.65 today")],
    [tdl("meal prep containers glass"),    td("1"),  td("A$1.49"),  td("A$0"),      tdb("∞"),     td("0%"),  tdb("—"),       td("—"), tdl("TOO EARLY — new KW at A$1.20, wait 10+ clicks")],
    [tdl("glass food containers with lids"),td("1"), td("A$0.80"),  td("A$0"),      tdb("∞"),     td("0%"),  tdb("—"),       td("—"), tdl("TOO EARLY — 1 click only")],
]
story.append(tbl(ex, [44*mm, 12*mm, 16*mm, 16*mm, 13*mm, 10*mm, 18*mm, 12*mm, 37*mm],
    [("BACKGROUND",(4,1),(4,1), BGGOLD),
     ("BACKGROUND",(4,2),(4,2), BGGREEN),
     ("BACKGROUND",(4,3),(4,3), BGRED),
     ("BACKGROUND",(4,4),(4,4), BGRED)]))

story.append(Spacer(1,2*mm))
story.append(Paragraph(
    "<b>glass food storage containers ACoS trend (clean days):</b>  "
    "May 21: 3.1%  →  May 22: 7.8%  →  May 23: 13.1%.  "
    "3-day average 8.0% is inside B1 break-even, but the May 23 single-day breach (13.1%) is a warning. "
    "If ACoS exceeds 12% for 2 consecutive clean days, reduce bid 10–15%.", BODY))

# ══ AUTO-01 ANALYSIS ═════════════════════════════════════════════════════════
story += section("Auto-01 — Search Term Analysis (all dates valid)")

story.append(Paragraph("<b>Converting Terms</b>", H3))
story.append(Spacer(1,1*mm))
auto_conv = [
    [th("Search Term"), th("Clicks"), th("Spend"), th("ACoS"), th("Date"), th("Action")],
    [tdl("b08sjcjnkn (substitute)"), td("1"), td("A$0.92"), tdb("1.7%"), td("May 22"), tdl("Add to PT-01 at A$0.75 ← (not A$0.85, see note)")],
    [tdl("b09ydhrn7h (substitute)"), td("1"), td("A$0.93"), tdb("1.7%"), td("May 17"), tdl("Already moved to PT-01 ✓")],
    [tdl("b0d9d25791 (substitute)"), td("1"), td("A$0.73"), tdb("1.3%"), td("May 22"), tdl("Add to PT-01 at A$0.75 ← (not A$0.85, see note)")],
    [tdl("glass containers"),        td("2"), td("A$1.96"), tdb("3.6%"), td("May 17"), tdl("WATCH — 1 conversion. Harvest to Exact at A$0.65 if converts again")],
    [tdl("glass food containers microwave"), td("1"), td("A$1.18"), tdb("2.2%"), td("May 22"), tdl("WATCH — 1 conversion only. Monitor")],
    [tdl("large glass food storage containers"), td("1"), td("A$0.95"), tdb("1.7%"), td("May 21"), tdl("WATCH — harvest at A$0.65 if converts again")],
]
story.append(tbl(auto_conv, [48*mm, 13*mm, 16*mm, 14*mm, 16*mm, 71*mm],
    [("BACKGROUND",(3,1),(3,-1), BGGREEN)]))

story.append(Spacer(1,3*mm))
story.append(Paragraph("<b>ASIN Substitutes: Negate These Now (2+ clicks, A$0 sales)</b>", H3))
story.append(Spacer(1,1*mm))
neg_asin = [
    [th("ASIN"), th("Clicks"), th("Spend"), th("Sales"), th("Action")],
    [tdl("b0fhjqhth7"), td("3"), td("A$2.34"), td("A$0"), tdl("Negative ASIN in Auto-01")],
    [tdl("b0f53ln66s"),  td("2"), td("A$1.42"), td("A$0"), tdl("Negative ASIN in Auto-01")],
    [tdl("b0crrpcjvh"),  td("2"), td("A$1.37"), td("A$0"), tdl("Negative ASIN in Auto-01  ← already in pending list")],
    [tdl("b0dxkvtk65"),  td("2"), td("A$1.94"), td("A$0"), tdl("Negative ASIN in Auto-01  ← NEW, not in pending list")],
    [tdl("b0fy2pwcbv"),  td("2"), td("A$1.42"), td("A$0"), tdl("Negative ASIN in Auto-01  ← NEW, not in pending list")],
    [tdl("b0flz54km5"),  td("2"), td("A$1.35"), td("A$0"), tdl("Negative ASIN in Auto-01  ← NEW, not in pending list")],
    [tdb("Total waste"), td(""), tdb("A$9.84"), td("A$0"), tdl("")],
]
story.append(tbl(neg_asin, [32*mm, 16*mm, 20*mm, 20*mm, 90*mm],
    [("BACKGROUND",(0,7),(-1,7), colors.HexColor("#f0f0f0"))]))
story.append(Spacer(1,2*mm))
story.append(Paragraph(
    "Note: Pending list only included b0fhjqhth7, b0f53ln66s, b0crrpcjvh. "
    "Add b0dxkvtk65, b0fy2pwcbv, b0flz54km5 as well — all 2 clicks, A$0 sales.", NOTE))

# ══ PT-01 ════════════════════════════════════════════════════════════════════
story += section("PT-01 — Product Targeting",
    "Only 2 days of data (May 22–23). 128 impressions, 2 clicks, A$2.36 spend, A$0 sales.")
pt = [
    [th("Target"), th("Status"), th("Data"), th("Action")],
    [tdl("B0F3WV3GWW (Feshory)"), tdl("ACTIVE — should be removed"), tdl("10 imp, 1 click, A$0.97, A$0"),        tdl("REMOVE immediately — before budget increase")],
    [tdl("B09YDHRN7H (Igluu)"),   tdl("ACTIVE ✓"),                   tdl("2 imp, 1 click, A$1.39 CPC, A$0"), tdl("Keep. Verify bid — CPC A$1.39 > B1 max A$0.65")],
    [tdl("B0D9D25791"),           tdl("PENDING — add"),               tdl("Auto: 1 click, A$0.73, 1.3% ACoS"), tdl("Add at A$0.75 (not A$0.85) — above B1 max CPC")],
    [tdl("B08SJCJNKN"),           tdl("PENDING — add"),               tdl("Auto: 1 click, A$0.92, 1.7% ACoS"), tdl("Add at A$0.75 (not A$0.85) — above B1 max CPC")],
]
story.append(tbl(pt, [34*mm, 30*mm, 48*mm, 66*mm],
    [("BACKGROUND",(0,1),(0,1), BGRED),
     ("BACKGROUND",(0,2),(0,2), BGGREEN),
     ("BACKGROUND",(0,3),(0,3), BGGOLD),
     ("BACKGROUND",(0,4),(0,4), BGGOLD)]))
story.append(Spacer(1,2*mm))
story.append(Paragraph(
    "<b>Bid challenge on B0D9D25791 and B08SJCJNKN:</b> "
    "Both converted in Auto at A$0.73 and A$0.92 CPC respectively, producing 1.3–1.7% ACoS. "
    "Pending list suggests A$0.85. Since PT CPCs tend to match the set bid closely on fixed-bid campaigns, "
    "A$0.85 is 31% above B1 max CPC of A$0.65. "
    "Recommend starting at <b>A$0.75</b> and reviewing after 5 clicks. If ACoS stays under 9.6%, raise to A$0.85.", BODY))
story.append(Spacer(1,2*mm))
story.append(Paragraph(
    "<b>Igluu CPC flag:</b> May 23 search term 'glass food storage containers meal prep' "
    "from PT-01 b09ydhrn7h shows CPC A$1.39 — well above B1 max A$0.65. "
    "If PT-01 is on Dynamic Bids, a placement modifier may be amplifying the bid. "
    "Verify PT-01 is on <b>Fixed Bids</b> in Seller Central.", BODY))

# ══ PENDING CHANGES VERDICT ══════════════════════════════════════════════════
story.append(PageBreak())
story += section("Pending Changes — Confirmed, Challenged, or Upgraded")

pending_rows = [
    [th("Change"), th("Verdict"), th("Notes")],
    [tdl("glass meal prep containers\nbid A$1.50 → A$1.10"),
     tdb("CONFIRM"),
     tdl("12+ total clicks, 1 sale in distorted period only. "
         "Clean: 1 click, A$0 sales. Upgrade: pause if 5 more clean clicks yield no sale.")],
    [tdl("borosilicate glass containers\nbid A$1.50 → A$0.65"),
     tdb("CONFIRM\nURGENT"),
     tdl("4 clicks, A$4.83, A$0. Avg CPC A$1.21 = 86% above B1 max. Do this today.")],
    [tdl("Create IRONCLAD-Exact-Rank-01\n[meal prep container glass], A$1.30, A$10/day"),
     tdb("CONFIRM\nSTRONGEST"),
     tdl("Clean ACoS 4.88%, CVR 33%, May 23: 3 units/4 clicks. "
         "At A$1.30 + 33% CVR expected ACoS = 7.1% — inside B1 break-even. "
         "Exact-01 is under-spending (46% util) so no budget conflict.")],
    [tdl("PT-01: add B0D9D25791 at A$0.85"),
     tdb("CHALLENGE\n→ A$0.75"),
     tdl("Bid confirmed correct in principle. But A$0.85 > B1 max CPC A$0.65. "
         "Start at A$0.75, review after 5 clicks.")],
    [tdl("PT-01: add B08SJCJNKN at A$0.85"),
     tdb("CHALLENGE\n→ A$0.75"),
     tdl("Same rationale as above. A$0.75 is safer on B1 stock.")],
    [tdl("PT-01 budget A$5 → A$8/day"),
     tdb("CONFIRM"),
     tdl("Do AFTER: remove Feshory → add 2 new targets → then raise budget.")],
    [tdl("Remove Feshory B0F3WV3GWW"),
     tdb("CONFIRM"),
     tdl("10 imp, 1 click, A$0.97, A$0. First action before anything else in PT-01.")],
    [tdl("Neg Exact Auto-01:\nglass food storage containers"),
     tdb("CONFIRM"),
     tdl("5 Auto clicks, A$4.15, A$0. In Exact-01. Confirmed cannibalism.")],
    [tdl("Neg Exact Auto-01:\nmeal prep container glass"),
     tdb("CONFIRM"),
     tdl("1 click, A$1.21, A$0. Will be in new Rank campaign too.")],
    [tdl("Neg Exact Auto-01:\nglass meal prep containers"),
     tdb("CONFIRM"),
     tdl("1 click, A$1.10, A$0. In Exact-01.")],
    [tdl("Neg ASIN Auto-01:\nb0fhjqhth7, b0f53ln66s, b0crrpcjvh"),
     tdb("CONFIRM\n+ EXPAND"),
     tdl("Also add b0dxkvtk65 (2 clicks A$1.94), b0fy2pwcbv (2 clicks A$1.42), "
         "b0flz54km5 (2 clicks A$1.35). All A$0 sales. Total extra waste: A$4.71.")],
]

for i, row in enumerate(pending_rows):
    if i == 0:
        pass
    elif pending_rows[i][1].text in ["CONFIRM\nURGENT", "CONFIRM\nSTRONGEST"]:
        pass

vs = []
for i, row in enumerate(pending_rows[1:], 1):
    verdict = row[1].text if hasattr(row[1], 'text') else ""
    if "URGENT" in str(row[1].getPlainText() if hasattr(row[1],'getPlainText') else ""):
        vs.append(("BACKGROUND", (1,i),(1,i), BGRED))
    elif "CHALLENGE" in str(row[1].getPlainText() if hasattr(row[1],'getPlainText') else ""):
        vs.append(("BACKGROUND", (1,i),(1,i), BGGOLD))
    elif "STRONGEST" in str(row[1].getPlainText() if hasattr(row[1],'getPlainText') else ""):
        vs.append(("BACKGROUND", (1,i),(1,i), BGGREEN))

# Simpler approach for row colours
def make_pending_tbl(data):
    t = Table(data, colWidths=[48*mm, 22*mm, 108*mm])
    verdicts = {2: BGRED, 4: BGGREEN, 5: BGGOLD, 6: BGGOLD}
    style = [
        ("BACKGROUND",    (0,0), (-1,0),  BRAND),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.35, MID),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("BACKGROUND",    (1,2), (1,2),   BGRED),   # URGENT
        ("BACKGROUND",    (1,3), (1,3),   BGGREEN), # STRONGEST
        ("BACKGROUND",    (1,4), (1,4),   BGGOLD),  # CHALLENGE
        ("BACKGROUND",    (1,5), (1,5),   BGGOLD),  # CHALLENGE
        ("BACKGROUND",    (1,12),(1,12),  BGGOLD),  # EXPAND
    ]
    t.setStyle(TableStyle(style))
    return t

story.append(make_pending_tbl(pending_rows))

# ══ NEW FINDINGS ═════════════════════════════════════════════════════════════
story += section("New Findings — Not in Pending Changes List")
new_rows = [
    [th("Finding"), th("Priority"), th("Action Required")],
    [tdl("Auto-01 budget = A$15/day in file (brief says A$10/day)"),
     tdb("FLAG"),
     tdl("Verify in Seller Central. Update brief. Avg daily spend A$9.06 — not maxing out at either figure.")],
    [tdl("Exact-01 under-spending: 46% utilisation on clean days"),
     tdb("NOTE"),
     tdl("Caused by removing placement adj. Budget headroom is real. New Rank campaign fills it correctly.")],
    [tdl("'leakproof container' — not negated (2 clicks, A$2.37, A$0)"),
     tdb("ACT"),
     tdl("Add Negative Exact 'leakproof container' to Auto-01. Not caught by 'leakproof bento boxes'.")],
    [tdl("'meal prep' — not negated (1 click, A$1.25 CPC, A$0)"),
     tdb("ACT"),
     tdl("Add Negative Exact 'meal prep' to Auto-01. Too broad. CPC A$1.25 > B1 max A$0.65.")],
    [tdl("3 extra ASIN substitutes need negating (b0dxkvtk65, b0fy2pwcbv, b0flz54km5)"),
     tdb("ACT"),
     tdl("All 2 clicks, A$0 sales, total A$4.71 waste. Not in pending list but should be negated now.")],
    [tdl("PT-01 on Dynamic Bids? Igluu CPC A$1.39 vs B1 max A$0.65"),
     tdb("CHECK"),
     tdl("Confirm PT-01 is on Fixed Bids in Seller Central. Dynamic bids can amplify CPC above set bid.")],
    [tdl("0 other-SKU sales (Advertised Product report)"),
     tdb("NOTE"),
     tdl("All conversions are direct. No halo effect yet. Normal at 2 reviews. Improves with Vine reviews.")],
    [tdl("glass containers — Auto harvest candidate (3.6% ACoS, 50% CVR)"),
     tdb("WATCH"),
     tdl("2 clicks, 1 conversion, May 17. Harvest to Exact at A$0.65 bid if it converts again.")],
    [tdl("glass food containers microwave — harvest candidate (2.2% ACoS)"),
     tdb("WATCH"),
     tdl("1 click, 1 conversion. Monitor. Harvest if converts again.")],
    [tdl("large glass food storage containers — harvest candidate (1.7% ACoS)"),
     tdb("WATCH"),
     tdl("1 click, 1 conversion. Harvest to Exact at A$0.65 (not A$0.95 — B1 max applies).")],
]
def make_new_tbl(data):
    t = Table(data, colWidths=[68*mm, 16*mm, 94*mm])
    style = [
        ("BACKGROUND",    (0,0), (-1,0),  BRAND),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.35, MID),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("BACKGROUND",    (1,1),(1,1), colors.HexColor("#fde8e8")),  # FLAG
        ("BACKGROUND",    (1,3),(1,3), BGRED),   # ACT
        ("BACKGROUND",    (1,4),(1,4), BGRED),   # ACT
        ("BACKGROUND",    (1,5),(1,5), BGRED),   # ACT
        ("BACKGROUND",    (1,6),(1,6), BGGOLD),  # CHECK
        ("BACKGROUND",    (1,8),(1,8), BGGOLD),  # WATCH
        ("BACKGROUND",    (1,9),(1,9), BGGOLD),  # WATCH
        ("BACKGROUND",    (1,10),(1,10),BGGOLD), # WATCH
    ]
    t.setStyle(TableStyle(style))
    return t
story.append(make_new_tbl(new_rows))

# ══ MASTER ACTION CHECKLIST ══════════════════════════════════════════════════
story += section("Master Action Checklist")
story.append(Paragraph("<b>TODAY</b>", H3))
today = [
    "□  Borosilicate glass containers: cut bid A$1.50 → A$0.65",
    "□  Remove Feshory B0F3WV3GWW from PT-01",
    "□  Add Negative Exact in Auto-01: 'leakproof container'",
    "□  Add Negative Exact in Auto-01: 'meal prep'",
    "□  Add Negative ASIN in Auto-01: b0fhjqhth7, b0f53ln66s, b0crrpcjvh, b0dxkvtk65, b0fy2pwcbv, b0flz54km5",
    "□  Add Negative Exact in Auto-01: 'glass food storage containers', 'meal prep container glass', 'glass meal prep containers'",
    "□  Verify Auto-01 budget in Seller Central (file shows A$15/day, brief says A$10)",
    "□  Verify PT-01 is on Fixed Bids (not Dynamic) in Seller Central",
]
for item in today:
    story.append(Paragraph(item, BODY))
story.append(Spacer(1,3*mm))

story.append(Paragraph("<b>THIS WEEK</b>", H3))
week = [
    "□  Glass meal prep containers: cut bid A$1.50 → A$1.10",
    "□  Create IRONCLAD-Exact-Rank-01: [meal prep container glass] Exact, bid A$1.30, A$10/day budget",
    "□  PT-01: Add B0D9D25791 at A$0.75 (start lower than planned A$0.85)",
    "□  PT-01: Add B08SJCJNKN at A$0.75 (start lower than planned A$0.85)",
    "□  PT-01: Increase budget A$5 → A$8/day (after Feshory removed + new targets added)",
    "□  Monitor glass food storage containers ACoS daily — reduce bid if >12% for 2 consecutive days",
]
for item in week:
    story.append(Paragraph(item, BODY))
story.append(Spacer(1,3*mm))

story.append(Paragraph("<b>ONGOING HARVEST WATCH (harvest to Exact if converts again)</b>", H3))
watch = [
    "□  glass containers (Auto) — 1 conversion, 3.6% ACoS → harvest at A$0.65 bid if converts again",
    "□  glass food containers microwave (Auto) — 1 conversion, 2.2% ACoS → watch",
    "□  large glass food storage containers (Auto) — 1 conversion, 1.7% ACoS → harvest at A$0.65",
    "□  glass meal prep containers (Exact) — pause if 5 more clean clicks yield no sale",
    "□  borosilicate glass containers (Exact) — if still no conversion at A$0.65 after 10 clicks, pause",
]
for item in watch:
    story.append(Paragraph(item, BODY))
story.append(Spacer(1,3*mm))

story.append(Paragraph("<b>STRATEGIC — ORDER BATCH 2</b>", H3))
story.append(Paragraph(
    "□  Every 9-day period on Batch 1 = A$217.80 forgone profit vs Batch 2 economics. "
    "The ads are working (20.2% ACoS, well within B2 break-even). "
    "Order Batch 2 (400 units, Hongqingyi) as soon as cash permits.", BODY))

story.append(Spacer(1,5*mm))
story.append(HRFlowable(width="100%", thickness=0.5, color=MID))
story.append(Spacer(1,2*mm))
story.append(Paragraph(
    "Report generated by Powerhouse FBA App  |  IRONCLAD campaigns  |  Amazon Australia  |  "
    f"Data: May 15–23, 2026  |  Generated {date.today().strftime('%d %b %Y')}",
    FOOT))

doc.build(story)
print(f"PDF saved: {OUTPUT}")
