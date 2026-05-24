from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from datetime import date

OUTPUT = "/home/user/powerhouse-fba-app/IRONCLAD_PPC_Audit.pdf"

BRAND   = colors.HexColor("#1a1a2e")
ACCENT  = colors.HexColor("#e94560")
LIGHT   = colors.HexColor("#f5f5f5")
MID     = colors.HexColor("#e0e0e0")
GREEN   = colors.HexColor("#27ae60")
ORANGE  = colors.HexColor("#e67e22")
RED     = colors.HexColor("#e74c3c")
WHITE   = colors.white
DARK    = colors.HexColor("#2c2c2c")

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm,
    topMargin=16*mm, bottomMargin=16*mm,
)

styles = getSampleStyleSheet()

def sty(name, **kw):
    base = styles["Normal"]
    return ParagraphStyle(name, parent=base, **kw)

H1   = sty("H1", fontSize=20, textColor=WHITE,      leading=26, fontName="Helvetica-Bold")
H2   = sty("H2", fontSize=13, textColor=BRAND,      leading=18, fontName="Helvetica-Bold", spaceAfter=2)
H3   = sty("H3", fontSize=10, textColor=ACCENT,     leading=14, fontName="Helvetica-Bold", spaceAfter=1)
BODY = sty("BODY", fontSize=8.5, textColor=DARK,    leading=13)
BOLD = sty("BOLD", fontSize=8.5, textColor=DARK,    leading=13, fontName="Helvetica-Bold")
SML  = sty("SML",  fontSize=7.5, textColor=colors.HexColor("#555555"), leading=11)
TH   = sty("TH",   fontSize=8,   textColor=WHITE,   leading=11, fontName="Helvetica-Bold", alignment=TA_CENTER)
TD   = sty("TD",   fontSize=7.5, textColor=DARK,    leading=11, alignment=TA_CENTER)
TDL  = sty("TDL",  fontSize=7.5, textColor=DARK,    leading=11, alignment=TA_LEFT)
NOTE = sty("NOTE", fontSize=7.5, textColor=colors.HexColor("#888888"), leading=11, leftIndent=8)

def th(t): return Paragraph(t, TH)
def td(t): return Paragraph(str(t), TD)
def tdl(t): return Paragraph(str(t), TDL)

def section(title):
    return [
        Spacer(1, 6*mm),
        HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=3),
        Paragraph(title, H2),
    ]

def tbl(data, col_widths, row_colors=None):
    t = Table(data, colWidths=col_widths)
    style = [
        ("BACKGROUND", (0,0), (-1,0), BRAND),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT]),
        ("GRID", (0,0), (-1,-1), 0.4, MID),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]
    if row_colors:
        for row_idx, col, bg in row_colors:
            style.append(("BACKGROUND", (col, row_idx), (col, row_idx), bg))
    t.setStyle(TableStyle(style))
    return t

story = []

# ── COVER HEADER ──────────────────────────────────────────────────────────────
header_data = [[
    Paragraph("IRONCLAD PPC Audit", H1),
    Paragraph(f"Amazon Australia &nbsp;|&nbsp; May 15–23, 2026<br/>"
              f"<font size=9 color='#aaaaaa'>Generated {date.today().strftime('%d %b %Y')}</font>",
              sty("hdr_sub", fontSize=9, textColor=colors.HexColor("#cccccc"), leading=14)),
]]
header_tbl = Table(header_data, colWidths=[115*mm, 57*mm])
header_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), BRAND),
    ("TOPPADDING", (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("ALIGN", (1,0), (1,0), "RIGHT"),
]))
story.append(header_tbl)
story.append(Spacer(1, 4*mm))

# ── FINANCIAL FRAMEWORK ────────────────────────────────────────────────────────
story += section("Financial Framework")
story.append(Paragraph(
    "Amazon reports sales ex-GST. Listed price A$59.99 ÷ 1.10 = <b>A$54.54 per unit</b>. "
    "Referral fee est. 15% = A$8.18. FBA est. = A$10.00. Net revenue after Amazon fees ≈ <b>A$36.36</b>.",
    BODY))
story.append(Spacer(1, 3*mm))

fin_data = [
    [th("Metric"), th("Value"), th("Notes")],
    [tdl("Listed sell price"), td("A$59.99"), tdl("GST-inclusive")],
    [tdl("Amazon-reported revenue/unit"), td("A$54.54"), tdl("Ex-GST ($59.99 ÷ 1.10)")],
    [tdl("Est. referral fee (15%)"), td("~A$8.18"), tdl("")],
    [tdl("Est. FBA fees"), td("~A$10.00"), tdl("Glass/kitchenware estimate")],
    [tdl("Est. net revenue after Amazon fees"), td("~A$36.36"), tdl("")],
    [tdl("Recommended target ACoS"), td("≤15%"), tdl("At A$10/day budget — tight margin")],
    [tdl("Max CPC at 10% CVR, 15% ACoS"), td("A$0.82"), tdl("Selling price × target ACoS × CVR")],
    [tdl("Break-even ACoS"), td("⚠️ TBC"), tdl("Provide landed product cost to calculate")],
]
story.append(tbl(fin_data, [72*mm, 30*mm, 70*mm]))

# ── PRIORITY 1: SCALE ─────────────────────────────────────────────────────────
story += section("Priority 1 — Scale These (Act Today)")
story.append(Paragraph("Proven winners. Increase bids 15–20% and protect budget allocation.", BODY))
story.append(Spacer(1, 2*mm))

p1_data = [
    [th("Search Term"), th("Campaign"), th("Spend"), th("Sales"), th("ACoS"), th("CVR"), th("Action")],
    [tdl("meal prep container glass"),    tdl("Exact-01"), td("A$25.46"), td("A$218.16"), td("11.7%"), td("13.6%"), tdl("Bid +20%")],
    [tdl("meal prep containers glass"),   tdl("Exact-01"), td("A$2.66"),  td("A$109.08"), td("2.4%"),  td("100%"),  tdl("Add as own Exact KW")],
    [tdl("glass food storage containers"),tdl("Exact-01"), td("A$55.77"), td("A$272.70"), td("20.4%"), td("9.8%"),  tdl("Maintain / slight increase")],
    [tdl("ASIN b0d9d25791"),              tdl("Auto-Subs"), td("A$0.73"), td("A$54.54"),  td("1.3%"),  td("100%"),  tdl("Keep, raise sub bid")],
    [tdl("ASIN b08sjcjnkn"),              tdl("Auto-Subs"), td("A$0.92"), td("A$54.54"),  td("1.7%"),  td("100%"),  tdl("Keep")],
    [tdl("ASIN b09ydhrn7h"),              tdl("Auto-Subs"), td("A$0.93"), td("A$54.54"),  td("1.7%"),  td("100%"),  tdl("Keep")],
]
story.append(tbl(p1_data, [52*mm, 22*mm, 17*mm, 18*mm, 14*mm, 12*mm, 37*mm],
    row_colors=[(1,4,colors.HexColor("#d5f5e3")), (2,4,colors.HexColor("#d5f5e3")),
                (4,4,colors.HexColor("#d5f5e3")), (5,4,colors.HexColor("#d5f5e3")),
                (6,4,colors.HexColor("#d5f5e3"))]))
story.append(Spacer(1, 2*mm))
story.append(Paragraph(
    "★  <b>meal prep containers glass</b> generated 93× ROAS on May 19. Add as a standalone Exact keyword in "
    "IRONCLAD-Exact-01 immediately — it is currently only caught incidentally by the 'meal prep container glass' target.",
    NOTE))

# ── PRIORITY 2: MOVE TO EXACT ─────────────────────────────────────────────────
story += section("Priority 2 — Move to Exact Match (This Week)")
story.append(Paragraph(
    "These terms converted in Auto but have no Exact keyword — budget is being wasted on "
    "loose/close matching. Add to IRONCLAD-Exact-01, then add each as Negative Exact in IRONCLAD-Auto-01.", BODY))
story.append(Spacer(1, 2*mm))

p2_data = [
    [th("Search Term"), th("Found In"), th("ACoS"), th("Action")],
    [tdl("glass containers"),                tdl("Auto close-match"),  td("3.6%"), tdl("Add Exact → Neg in Auto")],
    [tdl("large glass food storage containers"), tdl("Auto loose-match"), td("1.7%"), tdl("Add Exact → Neg in Auto")],
    [tdl("glass food containers microwave"), tdl("Auto close-match"),  td("2.2%"), tdl("Add Exact → Neg in Auto")],
    [tdl("meal prep containers glass"),      tdl("Auto via Exact target"), td("2.4%"), tdl("Add Exact → Neg in Auto")],
]
story.append(tbl(p2_data, [62*mm, 42*mm, 22*mm, 46*mm]))

# ── PRIORITY 3: NEGATIVES ─────────────────────────────────────────────────────
story += section("Priority 3 — Negative Keywords (Add Today)")

story.append(Paragraph("<b>3A. Irrelevant Terms — Negative in IRONCLAD-Auto-01</b>", H3))
story.append(Spacer(1, 1*mm))

neg_data = [
    [th("Term"), th("Match Type"), th("Spend"), th("Reason")],
    [tdl("snapware"),       td("Negative Exact"),  td("A$0.66"), tdl("Competitor brand name")],
    [tdl("tupperware"),     td("Negative Phrase"), td("A$1.25"), tdl("Brand name, wrong product")],
    [tdl("bento"),          td("Negative Phrase"), td("A$0.77"), tdl("Wrong product category")],
    [tdl("silicone"),       td("Negative Phrase"), td("A$0.66"), tdl("Wrong material")],
    [tdl("lunchbox"),       td("Negative Exact"),  td("A$0.74"), tdl("Wrong product")],
    [tdl("meal prep"),      td("Negative Exact"),  td("A$1.25"), tdl("Too broad, 0 conversions")],
    [tdl("containers"),     td("Negative Exact"),  td("A$0.74"), tdl("Too generic")],
    [tdl("food containers"),td("Negative Exact"),  td("A$0.92"), tdl("Too broad, 0 conversions")],
]
story.append(tbl(neg_data, [46*mm, 36*mm, 20*mm, 70*mm]))
story.append(Spacer(1, 3*mm))

story.append(Paragraph("<b>3B. Non-Converting ASIN Substitutes — Remove from Auto</b>", H3))
story.append(Spacer(1, 1*mm))
story.append(Paragraph(
    "The substitute strategy works (b0d9d25791, b08sjcjnkn, b09ydhrn7h all converted at &lt;2% ACoS). "
    "These specific ASINs are not converting — remove them from substitutes targeting.", BODY))
story.append(Spacer(1, 2*mm))

asin_data = [
    [th("ASIN"), th("Clicks"), th("Spend"), th("Sales"), th("Action")],
    [tdl("b0f53ln66s"), td("2"), td("A$1.42"), td("A$0.00"), tdl("Remove from substitutes")],
    [tdl("b0fhjqhth7"), td("3"), td("A$2.34"), td("A$0.00"), tdl("Remove from substitutes")],
    [tdl("b0crrpcjvh"), td("2"), td("A$1.37"), td("A$0.00"), tdl("Remove from substitutes")],
    [tdl("b0157g34ay"), td("1"), td("A$1.09"), td("A$0.00"), tdl("Remove from substitutes")],
    [tdl("b0fr4d5lbr"), td("1"), td("A$1.23"), td("A$0.00"), tdl("Remove from substitutes")],
]
story.append(tbl(asin_data, [40*mm, 20*mm, 22*mm, 22*mm, 68*mm]))
story.append(Spacer(1, 3*mm))

story.append(Paragraph("<b>3C. Cross-Campaign Isolation — Add as Negative Exact in IRONCLAD-Auto-01</b>", H3))
story.append(Paragraph(
    "Auto is double-serving on terms already in your Exact campaign, splitting attribution and wasting budget. "
    "Add each of these as Negative Exact in IRONCLAD-Auto-01:", BODY))
story.append(Spacer(1, 2*mm))

iso_terms = [
    "glass food storage containers",
    "meal prep container glass",
    "glass meal prep containers",
    "borosilicate glass containers",
    "glass food containers with lids",
]
iso_data = [[th("Term"), th("Match Type"), th("Why")]]
for t in iso_terms:
    iso_data.append([tdl(t), td("Negative Exact"), tdl("Already in Exact — stop Auto competing")])
story.append(tbl(iso_data, [72*mm, 30*mm, 70*mm]))

# ── PRIORITY 4: WATCH LIST ────────────────────────────────────────────────────
story += section("Priority 4 — Watch List (Insufficient Data)")
story.append(Paragraph("Do not cut yet. Review again after 3–5 more days of data.", BODY))
story.append(Spacer(1, 2*mm))

watch_data = [
    [th("Term"), th("Clicks"), th("Spend"), th("ACoS"), th("Notes")],
    [tdl("borosilicate glass containers"),   td("4"),  td("A$4.83"),  td("∞"),     tdl("CPC A$1.24–1.36. Cut at 8+ clicks, 0 sales")],
    [tdl("glass meal prep containers (Exact)"),td("12"),td("A$17.89"),td("32.8%"), tdl("Borderline. Reduce bid to A$0.90")],
    [tdl("glass meal prep container (singular)"),td("3"),td("A$4.63"),td("∞"),    tdl("CPC A$1.74 too high. Drop bid to A$1.00")],
    [tdl("fridge storage containers"),       td("3"),  td("A$3.04"),  td("∞"),     tdl("Could be plastic seekers. Watch 2 more days")],
    [tdl("glass containers with lids"),      td("1"),  td("A$1.24"),  td("∞"),     tdl("Insufficient data")],
    [tdl("glass food containers with lids"), td("1"),  td("A$0.80"),  td("∞"),     tdl("Insufficient data")],
]
story.append(tbl(watch_data, [56*mm, 14*mm, 18*mm, 16*mm, 68*mm]))

# ── PRIORITY 5: CUT ───────────────────────────────────────────────────────────
story += section("Priority 5 — Cut Now")
story.append(Spacer(1, 1*mm))

cut_data = [
    [th("Term"), th("Type"), th("Spend"), th("Reason")],
    [tdl("b0f3wv3gww (PT)"),              tdl("Competitor PT"),  td("A$0.97"), tdl("10 impressions, 1 click, 0 sales")],
    [tdl("glass containers amazon"),       tdl("Auto loose"),     td("A$1.24"), tdl('"amazon" prefix = browsing, not buying intent')],
    [tdl("borosilicate glass storage for freezer"), tdl("Auto"), td("A$0.02"), tdl("Negligible spend, not relevant")],
]
story.append(tbl(cut_data, [62*mm, 28*mm, 20*mm, 62*mm]))

# ── WEEK-BY-WEEK PLAN ─────────────────────────────────────────────────────────
story += section("Week-by-Week Action Plan")

plan_data = [
    [th("Week"), th("Actions"), th("Expected Outcome")],
    [
        td("Week 1\nNow"),
        tdl("• Add all negatives from Priority 3A & 3B\n"
            "• Add meal prep containers glass as Exact KW\n"
            "• Add glass containers, large glass food storage\n  containers, glass food containers microwave to Exact\n"
            "• Add cross-campaign isolation negatives (3C)\n"
            "• Reduce glass meal prep containers bid → A$0.90"),
        tdl("Reduce wasted spend ~A$12–15/period\nFree A$2–3/day budget for winners"),
    ],
    [
        td("Week 2"),
        tdl("• Review borosilicate glass containers\n  (cut if 8+ clicks, 0 sales)\n"
            "• Review glass meal prep container singular\n  (pause at 6 clicks, 0 sales)\n"
            "• Review fridge storage containers\n"
            "• Increase meal prep container glass bid +15–20%"),
        tdl("Further waste elimination\nScale best exact match terms"),
    ],
    [
        td("Week 3"),
        tdl("• Full search term audit on new Auto discoveries\n"
            "• Evaluate dedicated exact campaign/ad group\n  for glass meal prep containers\n"
            "• Review ASIN substitute list for new converters"),
        tdl("Consolidated budget into high-ROAS terms\nTarget ACoS ≤13%"),
    ],
]
story.append(tbl(plan_data, [20*mm, 90*mm, 62*mm]))

# ── EXPECTED IMPACT ───────────────────────────────────────────────────────────
story += section("Expected Impact After Optimisation")
story.append(Spacer(1, 1*mm))

impact_data = [
    [th("Metric"), th("Current (Est.)"), th("After Optimisation")],
    [tdl("Wasted spend on irrelevant Auto terms"), td("~A$12–15/period"), td("~A$2–3")],
    [tdl("Budget allocated to converting Exact terms"), td("Diluted"), td("Concentrated")],
    [tdl("Overall ACoS (est.)"),                    td("~17%"),         td("≤13%")],
    [tdl("Daily budget headroom for scaling winners"), td("None"),       td("A$2–3/day freed")],
]
story.append(tbl(impact_data, [80*mm, 42*mm, 50*mm]))

story.append(Spacer(1, 5*mm))
story.append(HRFlowable(width="100%", thickness=0.5, color=MID))
story.append(Spacer(1, 2*mm))
story.append(Paragraph(
    "⚠️  Provide your landed product cost to calculate exact break-even ACoS and refine bid ceilings. "
    "All ACOS targets are based on an estimated 15% target ACoS at A$10/day daily budget.",
    NOTE))
story.append(Spacer(1, 1*mm))
story.append(Paragraph(
    "Report generated by Powerhouse FBA App &nbsp;|&nbsp; IRONCLAD campaigns &nbsp;|&nbsp; Amazon Australia",
    sty("footer", fontSize=7, textColor=colors.HexColor("#aaaaaa"), alignment=TA_CENTER)))

doc.build(story)
print(f"PDF saved to {OUTPUT}")
