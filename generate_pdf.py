from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# ------------------------------------------------------------
# University of Calgary Dinos | Position Action Exposure
# Source: values and wording in the supplied index.html
# Image: assets/UofC_All_Position_Comparisons.png
# ------------------------------------------------------------

ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "assets"
OUTPUT_DIR = ROOT / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PDF = OUTPUT_DIR / "Dinos_Position_Action_Exposure.pdf"

NAVY = colors.HexColor("#173B66")
BLUE = colors.HexColor("#3478A8")
PALE = colors.HexColor("#E6F1FA")
ORANGE = colors.HexColor("#EF9638")
INK = colors.HexColor("#243447")
MUTED = colors.HexColor("#667789")
LIGHT = colors.HexColor("#F4F7FB")
LINE = colors.HexColor("#DCE5EE")
WHITE = colors.white

# Exact displayed values transcribed from the supplied HTML.
# Rates are actions per team set.
POSITIONS = [
    ("Setter", [
        ("Attack", "1.72", "1.36"),
        ("Block",  "2.07", "1.74"),
        ("Serve",  "3.54", "3.97"),
        ("Set",    "23.94", "25.84"),
    ]),
    ("Outside Hitter", [
        ("Attack", "22.04", "20.14"),
        ("Block",  "4.38", "4.31"),
        ("Serve",  "11.18", "9.57"),
        ("Set",    "2.64", "2.45"),
    ]),
    ("Middle Blocker", [
        ("Attack", "5.46", "7.41"),
        ("Block",  "4.96", "6.03"),
        ("Serve",  "5.03", "6.13"),
        ("Set",    "0.75", "1.09"),
    ]),
    ("Libero", [
        ("Attack", "0.00", "0.03"),
        ("Block",  "0.01", "0.01"),
        ("Serve",  "1.04", "0.62"),
        ("Set",    "3.25", "2.44"),
    ]),
]

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverKicker", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=9, leading=12, textColor=colors.HexColor("#BFD8EC"),
    tracking=1.5, alignment=TA_LEFT, spaceAfter=12
))
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=27, leading=31, textColor=WHITE, alignment=TA_LEFT,
    spaceAfter=13
))
styles.add(ParagraphStyle(
    name="CoverSub", parent=styles["Normal"], fontName="Helvetica",
    fontSize=11, leading=17, textColor=colors.HexColor("#E1EDF7")
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=18, leading=22, textColor=NAVY, spaceBefore=2, spaceAfter=8
))
styles.add(ParagraphStyle(
    name="Subhead", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=12, leading=15, textColor=NAVY, spaceBefore=7, spaceAfter=5
))
styles.add(ParagraphStyle(
    name="BodyCustom", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.2, leading=14, textColor=INK, spaceAfter=7
))
styles.add(ParagraphStyle(
    name="SmallCustom", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=8, leading=11, textColor=MUTED, spaceAfter=4
))
styles.add(ParagraphStyle(
    name="Callout", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9, leading=13, textColor=INK
))
styles.add(ParagraphStyle(
    name="TableTitle", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=12, leading=15, textColor=NAVY, spaceAfter=5
))

def footer(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(0.62*inch, 0.52*inch, w-0.62*inch, 0.52*inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.65*inch, 0.34*inch, "UNIVERSITY OF CALGARY DINOS  |  POSITION ACTION EXPOSURE")
    canvas.drawRightString(w-0.65*inch, 0.34*inch, f"{doc.page}")
    canvas.restoreState()

def make_table(rows, col_widths):
    t = Table(rows, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PALE),
        ("TEXTCOLOR", (0,0), (-1,0), NAVY),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 8),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 8.5),
        ("TEXTCOLOR", (0,1), (-1,-1), INK),
        ("ALIGN", (1,1), (-1,-1), "RIGHT"),
        ("ALIGN", (0,0), (0,-1), "LEFT"),
        ("LINEBELOW", (0,0), (-1,0), 0.8, BLUE),
        ("LINEBELOW", (0,1), (-1,-1), 0.35, LINE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT]),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ]))
    return t

story = []

# PAGE 1 — Cover and study snapshot
cover = Table([
    [Paragraph("2025–26 SEASON  ·  WOMEN'S VOLLEYBALL", styles["CoverKicker"])],
    [Paragraph("University of Calgary<br/>Dinos", styles["CoverTitle"])],
    [Paragraph("Position-Specific Action Exposure", styles["CoverSub"])],
    [Spacer(1, 15)],
    [Paragraph(
        "A focused comparison of Calgary's Setter, Outside Hitter, "
        "Middle Blocker and Libero action rates against the pooled "
        "Canada West benchmark.",
        styles["CoverSub"]
    )],
], colWidths=[7.15*inch])
cover.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), NAVY),
    ("BOX", (0,0), (-1,-1), 0, NAVY),
    ("LEFTPADDING", (0,0), (-1,-1), 25),
    ("RIGHTPADDING", (0,0), (-1,-1), 25),
    ("TOPPADDING", (0,0), (-1,0), 23),
    ("BOTTOMPADDING", (0,-1), (-1,-1), 25),
]))
story.append(Spacer(1, 0.35*inch))
story.append(cover)
story.append(Spacer(1, 22))
story.append(Paragraph("Study at a glance", styles["Section"]))

stats = [
    [Paragraph("<b>14</b><br/><font size='8'>Canada West teams</font>", styles["BodyCustom"]),
     Paragraph("<b>140</b><br/><font size='8'>DVW match files</font>", styles["BodyCustom"]),
     Paragraph("<b>1,038</b><br/><font size='8'>Team-set appearances</font>", styles["BodyCustom"])],
]
st = Table(stats, colWidths=[2.25*inch]*3, rowHeights=[0.68*inch])
st.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), PALE),
    ("BOX", (0,0), (-1,-1), 0.7, LINE),
    ("INNERGRID", (0,0), (-1,-1), 0.5, LINE),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("TOPPADDING", (0,0), (-1,-1), 10),
]))
story.append(st)
story.append(Spacer(1, 15))
story.append(Paragraph("Purpose", styles["Subhead"]))
story.append(Paragraph(
    "This report presents University of Calgary position-specific coded action "
    "rates per team set and compares them with the pooled Canada West average. "
    "Normalizing by sets played provides a common basis for comparing teams "
    "that completed different numbers of sets.",
    styles["BodyCustom"]))
story.append(Paragraph("How to interpret the estimate", styles["Subhead"]))
call = Table([[
    Paragraph(
        "<b>Study-defined jump/action estimate.</b> Each coded Attack, Block, "
        "Serve and Set action is counted as one jump-equivalent action. This is "
        "the study's operational assumption, not a directly observed physical "
        "jump count.",
        styles["Callout"]
    )
]], colWidths=[7.0*inch])
call.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FFF8EF")),
    ("BOX", (0,0), (-1,-1), 0.7, ORANGE),
    ("LEFTPADDING", (0,0), (-1,-1), 12),
    ("RIGHTPADDING", (0,0), (-1,-1), 12),
    ("TOPPADDING", (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
]))
story.append(call)
story.append(Spacer(1, 12))
story.append(Paragraph(
    "Prepared from the supplied 2025–26 Canada West DVW analysis webpage "
    "and its University of Calgary comparison values.",
    styles["SmallCustom"]
))
story.append(PageBreak())

# PAGE 2 — Dinos graphic
story.append(Paragraph("University of Calgary position profile", styles["Section"]))
story.append(Paragraph(
    "The figure compares Calgary's position-specific action rates with the "
    "pooled Canada West benchmark. Blue bars represent Calgary; the orange "
    "dashed line represents the conference average.",
    styles["BodyCustom"]))
chart_path = ASSET_DIR / "UofC_All_Position_Comparisons.png"
if chart_path.exists():
    img = Image(str(chart_path))
    max_w, max_h = 7.05*inch, 7.3*inch
    scale = min(max_w / img.imageWidth, max_h / img.imageHeight)
    img.drawWidth = img.imageWidth * scale
    img.drawHeight = img.imageHeight * scale
    story.append(img)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Rates are expressed as coded actions per team set. The benchmark is "
        "pooled across 1,038 team-set appearances.",
        styles["SmallCustom"]
    ))
else:
    story.append(Paragraph(
        "The chart image was not found. Confirm that "
        "<b>assets/UofC_All_Position_Comparisons.png</b> exists in the repository.",
        styles["Callout"]
    ))
story.append(PageBreak())

# PAGE 3 — Setter and Outside Hitter
story.append(Paragraph("Position comparisons", styles["Section"]))
story.append(Paragraph(
    "Values are actions per team set. The difference column is Calgary minus "
    "the pooled Canada West average.",
    styles["BodyCustom"]))

for pos_name, rows in POSITIONS[:2]:
    story.append(Paragraph(pos_name, styles["TableTitle"]))
    table_rows = [["Action", "Calgary", "Conf. avg.", "Difference"]]
    for action, cal, conf in rows:
        diff = float(cal) - float(conf)
        table_rows.append([action, cal, conf, f"{diff:+.2f}"])
    story.append(make_table(table_rows, [2.0*inch, 1.35*inch, 1.35*inch, 1.35*inch]))
    story.append(Spacer(1, 17))

story.append(Paragraph(
    "<b>Reading the comparison:</b> A positive difference indicates a higher "
    "coded action rate than the pooled conference benchmark; a negative "
    "difference indicates a lower rate. These are descriptive differences, "
    "not performance grades or workload thresholds.",
    styles["SmallCustom"]
))
story.append(PageBreak())

# PAGE 4 — Middle Blocker and Libero
story.append(Paragraph("Position comparisons", styles["Section"]))
for pos_name, rows in POSITIONS[2:]:
    story.append(Paragraph(pos_name, styles["TableTitle"]))
    table_rows = [["Action", "Calgary", "Conf. avg.", "Difference"]]
    for action, cal, conf in rows:
        diff = float(cal) - float(conf)
        table_rows.append([action, cal, conf, f"{diff:+.2f}"])
    story.append(make_table(table_rows, [2.0*inch, 1.35*inch, 1.35*inch, 1.35*inch]))
    story.append(Spacer(1, 17))

story.append(Paragraph("Position-level context", styles["Subhead"]))
story.append(Paragraph(
    "The four position profiles should be interpreted within their technical "
    "roles. Attack, block, serve and set involvement naturally differ by "
    "position, so comparisons are most useful within the same position and "
    "action category.",
    styles["BodyCustom"]))
story.append(PageBreak())

# PAGE 5 — Methodology, limitations and conclusion
story.append(Paragraph("Methodology and interpretation", styles["Section"]))
story.append(Paragraph(
    "The analysis was built from coded play-by-play actions in 140 Canada West "
    "DVW files. Team rates use each team's total sets played as the denominator.",
    styles["BodyCustom"]))
method_rows = [
    ["Component", "Definition"],
    ["Team rate", "Team action total ÷ team sets played"],
    ["Pooled conference benchmark", "Conference action total ÷ 1,038 team-set appearances"],
    ["Positions", "Setter · Outside Hitter · Middle Blocker · Libero"],
    ["Counted action classes", "Attack · Block · Serve · Set"],
    ["Position grouping", "Opposite/right-side roles are grouped with Outside Hitter"],
]
story.append(make_table(method_rows, [2.1*inch, 4.75*inch]))
story.append(Spacer(1, 15))
story.append(Paragraph("Important limitations", styles["Subhead"]))
limitations = [
    "<b>Operational assumption:</b> This report counts each coded Attack, Block, "
    "Serve and Set as one jump-equivalent action to create a consistent "
    "study-defined workload estimate.",
    "<b>Not verified physical jumps:</b> DVW action codes do not confirm that "
    "every attack or block involved a jump, that a set was a jump set, or that "
    "a serve was a jump serve.",
    "<b>Block participation:</b> One coded block action may involve multiple "
    "blockers; the data do not establish how many athletes jumped on each play.",
    "<b>Team rates are not individual athlete loads:</b> Substitutions, "
    "player-specific court time and individual participation are not reflected "
    "in the team-set denominator.",
    "<b>Benchmark is descriptive:</b> The pooled average is weighted by "
    "team-set appearances and is not a recommended workload threshold.",
]
for item in limitations:
    story.append(Paragraph("• " + item, styles["BodyCustom"]))

story.append(Spacer(1, 7))
story.append(Paragraph("Conclusion", styles["Subhead"]))
story.append(Paragraph(
    "This analysis provides a position-specific view of Calgary's coded action "
    "profile relative to the Canada West pattern. It can support workload "
    "discussions and help identify where more detailed video review or "
    "athlete-level jump monitoring would add value. The results should be "
    "treated as a study-defined action-exposure estimate rather than a direct "
    "measurement of physical jumps.",
    styles["BodyCustom"]))

doc = SimpleDocTemplate(
    str(OUTPUT_PDF), pagesize=letter,
    rightMargin=0.72*inch, leftMargin=0.72*inch,
    topMargin=0.62*inch, bottomMargin=0.72*inch,
    title="University of Calgary Dinos - Position Action Exposure",
    author="Canada West Position Action Exposure Study"
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"Created: {OUTPUT_PDF}")
