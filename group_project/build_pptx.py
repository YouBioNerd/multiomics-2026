# Builds group_project/slides.pptx natively (editable text + tables).
# The pandoc PPTX export mangled the dense slides (split one, dropped
# Q2's answer), so this script lays out the same six slides directly.
# Run:  python3 group_project/build_pptx.py
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

DARK = RGBColor(0x22, 0x22, 0x22)
ACCENT = RGBColor(0x1A, 0x5F, 0xB4)
ANSWER_BG = RGBColor(0xEA, 0xF2, 0xFB)
GREY = RGBColor(0x55, 0x55, 0x55)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def slide(notes=""):
    s = prs.slides.add_slide(BLANK)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def title(s, text, size=28, sub=None):
    tb = s.shapes.add_textbox(Inches(0.4), Inches(0.25), Inches(12.5), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    r = tf.paragraphs[0].add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.color.rgb = DARK
    if sub:
        p = tf.add_paragraph()
        r = p.add_run()
        r.text = sub
        r.font.size = Pt(15)
        r.font.italic = True
        r.font.color.rgb = GREY
    return tb


def bullets(s, items, left, top, width, height, size=16):
    tb = s.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, (txt, lvl) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = lvl
        r = p.add_run()
        r.text = ("• " if lvl == 0 else "– ") + txt
        r.font.size = Pt(size if lvl == 0 else size - 1)
        r.font.color.rgb = DARK
    return tb


def para(s, text, left, top, width, height, size=13, bold=False,
         italic=False, color=DARK, bg=None):
    if bg is not None:
        from pptx.enum.shapes import MSO_SHAPE
        box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                 Inches(left - 0.1), Inches(top - 0.1),
                                 Inches(width + 0.2), Inches(height + 0.15))
        box.fill.solid()
        box.fill.fore_color.rgb = bg
        box.line.fill.background()
        box.shadow.inherit = False
    tb = s.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    r = tf.paragraphs[0].add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return tb


def table(s, data, left, top, width, height, col_w=None, size=12, header_bold=True):
    shp = s.shapes.add_table(len(data), len(data[0]),
                             Inches(left), Inches(top), Inches(width), Inches(height))
    t = shp.table
    if col_w:
        for c, w in enumerate(col_w):
            t.columns[c].width = Inches(w)
    for r_i, row in enumerate(data):
        for c_i, txt in enumerate(row):
            cell = t.cell(r_i, c_i)
            cell.text = txt
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(size)
                    run.font.bold = header_bold and r_i == 0
    return t


def pic_caption(s, path, caption, numbers, left, top, width):
    s.shapes.add_picture(path, Inches(left), Inches(top), width=Inches(width))
    y = top + width * 0.75 + 0.15  # figures are 4:3
    para(s, caption, left, y, width, 0.6, size=13, bold=True)
    para(s, numbers, left, y + 0.55, width, 1.2, size=12, color=GREY)


# ---------------- Slide 1: Q1 question + what we did ----------------
s = slide("The 15,000-read rule was picked from the depth histogram alone, "
          "never from the test result. Relative abundances so shallow samples "
          "are not punished for being shallow.")
title(s, "Question 1 — Do the three contraceptive methods differ "
         "in community composition?",
      sub="Study B — 93 participants, one vaginal sample each")
bullets(s, [
    ("Quality-checked both count tables (depth, zeros, batch)", 0),
    ("Filtered: nothing deleted — 9 low-depth samples (< 15,000 reads) were "
     "flagged and retested without, as a sensitivity check", 0),
    ("Main test: PCoA map + PERMANOVA on Bray-Curtis distance of relative "
     "abundances (999 permutations, seed 202)", 0),
    ("Pairwise arm comparisons with Holm correction for three tests", 0),
], 0.6, 2.0, 12.0, 3.5, size=18)

# ---------------- Slide 2: the two maps ----------------
s = slide("Left: each point is one participant's community; close points have "
          "similar communities. If the methods differed, colours would form "
          "three islands. Right: the same map coloured by BV — BV-negative top "
          "left, BV-positive bottom right.")
title(s, "Q1 — the map, and what actually separates the samples")
pic_caption(s, "figures/pcoa-arm.png",
            "\u201cThree overlapping crowds, not three islands.\u201d",
            "Arm alone: R² = 3.3%, p = 0.147. After BV, pH, STI and batch: "
            "R² = 2.7%, p = 0.108.", 0.55, 1.15, 5.9)
pic_caption(s, "figures/pcoa-bv.png",
            "\u201cWhat separates them is BV — not the method.\u201d",
            "BV: R² = 14.3%, p = 0.001. Pill vs injectable alone: "
            "R² = 3.9%, p = 0.033 (→ 0.099 Holm-corrected).",
            6.95, 1.15, 5.9)

# ---------------- Slide 3: Q1 choices + answer ----------------
s = slide("Robustness table (02 §4): raw-count Bray, Aitchison and Jaccard all "
          "leave arm at ~3%, non-significant.")
title(s, "Q1 — choices we made, and the answer")
table(s, [
    ["Choice", "Route A", "Route B", "Kept"],
    ["Distance", "Bray-Curtis on relative abundances",
     "on raw counts (draft 1)", "A — raw counts punish the 9 shallow samples"],
    ["Pairwise tests", "Holm-corrected", "raw p-values",
     "A — three tests, three chances to be fooled"],
], 0.5, 1.2, 12.3, 1.6, col_w=[2.0, 3.6, 3.0, 3.7], size=13)
para(s, "Source we opened: Anderson (2001), the PERMANOVA paper — "
        "doi.org/10.1111/j.1442-9993.2001.01070.pp.x",
     0.5, 3.1, 12.3, 0.5, size=13, italic=True, color=ACCENT)
para(s, "Answer to Question 1: No. Method explains 3.3% (p = 0.147); every "
        "alternative distance agrees. The one hint — pill vs injectable, "
        "p = 0.033 — falls to 0.099 after correction. Sanity check agrees: "
        "median Lactobacillus share 84.8% pill vs 45.3% injectable / 44.7% ring.",
     0.6, 3.9, 12.1, 1.6, size=17, bold=True, bg=ANSWER_BG)

# ---------------- Slide 4: Q2 question + what we did ----------------
s = slide("Both BV definitions were run so the verdict does not hinge on where "
          "'BV' is drawn.")
title(s, "Question 2 — Is bacterial vaginosis more common in one arm?",
      sub="Tuesday's anatomy module: look at the table before testing it")
bullets(s, [
    ("Validated the bv column first: label vs Nugent score agreed in 93/93 "
     "samples — safe to use", 0),
    ("Kept all 93 samples — BV status comes from the Nugent score, not "
     "sequencing depth, so shallow samples are still valid rows here", 0),
    ("Tested: Fisher's exact test (two cells held < 5 samples, so chi-square "
     "was unreliable), three BV categories AND collapsed to any-BV-vs-none", 0),
    ("Sanity check from biology: BV-positive samples should carry more "
     "Gardnerella", 0),
], 0.6, 1.9, 12.0, 2.6, size=16)
table(s, [
    ["Choice", "Route A", "Route B", "Kept"],
    ["Test", "Fisher's exact test", "chi-square (unreliable with cells < 5)", "A"],
    ["BV definition", "three categories", "collapsed to any-BV",
     "both — p = 0.45 and p = 0.90, same verdict twice"],
], 0.5, 4.8, 12.3, 1.5, col_w=[2.2, 3.2, 3.4, 3.5], size=13)
para(s, "Source we opened: the R documentation for fisher.test (?fisher.test)",
     0.5, 6.6, 12.3, 0.4, size=13, italic=True, color=ACCENT)

# ---------------- Slide 5: Q2 figure + numbers + answer ----------------
s = slide("With 26–39 per arm, even the largest gap (13 points) is within "
          "chance.")
title(s, "Q2 — the figure, the numbers, and the answer")
s.shapes.add_picture("figures/bv-by-arm.png", Inches(0.45), Inches(1.15),
                     width=Inches(4.9))
para(s, "The share of each arm that is BV-negative, intermediate or positive.",
     0.45, 4.95, 4.9, 0.6, size=12, italic=True, color=GREY)
table(s, [
    ["Arm", "any BV", "positive only"],
    ["injectable", "48.7%", "48.7%"],
    ["pill", "42.9%", "35.7%"],
    ["ring", "42.3%", "38.5%"],
], 5.85, 1.25, 4.0, 1.4, col_w=[1.6, 1.2, 1.2], size=14)
para(s, "Fisher's exact test: p = 0.454 (3 categories), p = 0.897 "
        "(any BV vs none).", 5.85, 3.0, 7.0, 0.7, size=14)
para(s, "Sanity check: median Gardnerella share — 24.6% in BV-positive vs "
        "1.1% in BV-negative. The labels mean something.",
     5.85, 3.8, 7.0, 0.8, size=14)
para(s, "Answer to Question 2: No. BV is common (~42–49%) everywhere; no arm "
        "is protected or penalised. BV dominates the communities (Q1: "
        "R² = 14.3%) but is a rival explanation, not a confounder.",
     0.6, 5.9, 12.1, 1.2, size=16, bold=True, bg=ANSWER_BG)

# ---------------- Slide 6: doubts + next questions ----------------
s = slide("The two 'checked now' answers are looks at the data, not tests — "
          "they still need formal analysis. Cross-table habit applies "
          "throughout: define the group from one table, test the other.")
title(s, "What we do not believe — and the questions we ask next")
para(s, "We do not believe: \u201cno difference\u201d means no difference exists "
        "(26–39 per arm can miss a modest effect); the pill-vs-injectable hint "
        "(it does not survive correction); that our distance sees everything "
        "(arm effects could hide under the BV signal); or that the arms were "
        "comparable at baseline (observational, not randomised).",
     0.5, 1.05, 12.4, 0.9, size=13, italic=True)
table(s, [
    ["Question", "Answer"],
    ["Do the gene differences match the pill-vs-injectable hint?",
     "Not tested yet — we expect mostly no, since the hint fell to p ≈ 0.10"],
    ["Does BV leave a mark on the immune data (cytokines)?",
     "We expect yes — BV-positive samples already carry 24.6% Gardnerella "
     "vs 1.1%"],
    ["Do cytokines differ by arm?",
     "Open — the immune readout is where an arm effect could still hide"],
    ["Which Lactobacillus dominates, crispatus or iners?",
     "Checked now: iners peaks in the pill arm (17.3% vs 9.0% ring, 1.8% "
     "injectable); crispatus tracks BV (28.2% vs 0.1%), not arm"],
    ["Does composition shift gradually with Nugent 0–10?",
     "Expected yes — three categories may hide a dose–response"],
    ["Is pH the middleman?",
     "Checked now: pill's median pH is 4.55 vs 5.0 in the other arms, and pH "
     "tracks BV (4.4 negative → 5.0 positive) — a look, not a test"],
], 0.5, 2.15, 12.4, 4.4, col_w=[5.4, 7.0], size=11)

prs.save("slides.pptx")
print("Saved slides.pptx with", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
