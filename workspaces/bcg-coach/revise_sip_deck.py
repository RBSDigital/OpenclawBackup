from copy import deepcopy
from datetime import datetime, timezone
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

SRC = "/tmp/sip_review/ITC_SIP_Playback_Updated.pptx"
stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%MUTC")
OUT = f"/tmp/sip_review/BCG-CI-Presentation_SIP-Manager_{stamp}.pptx"

prs = Presentation(SRC)
NAVY = RGBColor(14, 43, 99)
BLUE = RGBColor(23, 70, 139)
GOLD = RGBColor(250, 180, 30)
INK = RGBColor(35, 45, 60)
MID = RGBColor(92, 105, 122)
PALE = RGBColor(247, 249, 252)
LIGHT_BLUE = RGBColor(230, 235, 243)
LIGHT_GOLD = RGBColor(255, 247, 222)
GREEN = RGBColor(35, 126, 91)
WHITE = RGBColor(255, 255, 255)

def all_text_shapes(slide):
    return [sh for sh in slide.shapes if hasattr(sh, "text")]

def run_colour(run):
    try:
        if run and run.font.color.type is not None and run.font.color.rgb:
            return run.font.color.rgb
    except (AttributeError, ValueError):
        pass
    return INK

def replace_exact(slide, old, new):
    for sh in all_text_shapes(slide):
        if sh.text.strip() == old.strip():
            # Preserve the first run's style while replacing the wording.
            tf = sh.text_frame
            first = tf.paragraphs[0].runs[0] if tf.paragraphs and tf.paragraphs[0].runs else None
            size = first.font.size if first and first.font.size else Pt(12)
            colour = run_colour(first)
            bold = first.font.bold if first else False
            name = first.font.name if first and first.font.name else "Aptos"
            tf.clear(); p = tf.paragraphs[0]; p.text = new
            for r in p.runs:
                r.font.name = name; r.font.size = size; r.font.bold = bold; r.font.color.rgb = colour
            return True
    return False

def replace_contains(slide, old, new):
    for sh in all_text_shapes(slide):
        if old in sh.text:
            original = sh.text
            tf = sh.text_frame
            first = tf.paragraphs[0].runs[0] if tf.paragraphs and tf.paragraphs[0].runs else None
            size = first.font.size if first and first.font.size else Pt(12)
            colour = run_colour(first)
            bold = first.font.bold if first else False
            name = first.font.name if first and first.font.name else "Aptos"
            tf.clear(); p = tf.paragraphs[0]; p.text = original.replace(old, new)
            for r in p.runs:
                r.font.name = name; r.font.size = size; r.font.bold = bold; r.font.color.rgb = colour
            return True
    return False

def add_box(slide, x, y, w, h, fill, line=LIGHT_BLUE):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = line; sh.line.width = Pt(1)
    return sh

def add_text(slide, value, x, y, w, h, size=12, colour=INK, bold=False, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.clear(); tf.word_wrap = True
    tf.margin_left = Inches(0.08); tf.margin_right = Inches(0.08); tf.margin_top = Inches(0.05); tf.margin_bottom = Inches(0.05)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    p = tf.paragraphs[0]; p.alignment = align; p.text = value
    for r in p.runs:
        r.font.name = "Aptos"; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = colour
    return tb

# Slide 1
s = prs.slides[0]
replace_exact(s, "WESTERN EUROPE  |  CONSUMER TECHNOLOGY  |  SIP PLAYBACK", "WESTERN EUROPE  |  CONSUMER TECHNOLOGY  |  SIP PLAYBACK")
add_text(s, "Leadership review | 25 November 2026", 0.8, 6.6, 5.5, 0.25, 10, MID, True)

# Slide 2: wording and punctuation
s = prs.slides[1]
replacements = {
    "The SIP At a Glance – Where we started": "The SIP at a glance: where we started",
    "Together, BAT WE IDT and ITC Infotech have moved from a reactive service to one that is coordinated, governed and visible.": "Together, BAT WE IDT and ITC Infotech have moved from reactive service management towards a more coordinated, governed and visible model.",
    "Due dates and commitments were not consistently enforced\nMissed commitments were not routinely escalate\nImprovements are reactive, and not proactive": "Due dates and commitments were not consistently enforced\nMissed commitments were not routinely escalated\nImprovements were reactive, not proactive",
    "CRM, AIS and Data Platform teams rarely planned dependencies collectively\nDependencies frequently required escalation to resolve\nThere was no shared plan or end-to-end ownership": "CRM, AIS and Data Platform teams rarely planned dependencies collectively\nDependencies frequently required escalation to resolve\nThere was no shared plan or end-to-end ownership",
    "Documentation lacked clear ownership, maintenance controls and common standards\nKnowledge transfer was difficult and, in some cases, not feasible\nCritical knowledge was fragmented across teams and individuals": "Documentation lacked clear ownership, maintenance controls and common standards\nKnowledge transfer was difficult and, in some cases, not feasible\nCritical knowledge was fragmented across teams and individuals",
    "Multiple": "Multiple",
    "point of ownership": "points of ownership",
    "teams alignment": "team alignment",
    "Zero\nartefacts in one WE home": "No\nartefacts in one WE home",
}
for old,new in replacements.items(): replace_exact(s, old, new)
replace_exact(s, "1\npoint of ownership", "One\npoint of ownership")
replace_exact(s, "4\nteams aligned", "Four\nteams aligned")
replace_exact(s, "17\nartefacts in one WE home", "17\nartefacts in one WE home")
for sh in list(all_text_shapes(s)):
    if sh.text.strip() == "1": replace_exact(s, "1", "One")
    if sh.text.strip() == "Zero": replace_exact(s, "Zero", "No")

# Slide 3
s = prs.slides[2]
replace_exact(s, "A fast-growing, multi-market D2C estate, supported by several teams, had naturally outgrown informal ways of working.", "A fast-growing, multi-market D2C estate, supported by several teams, had outgrown informal ways of working.")
replace_exact(s, "WE IDT were spending valuable time aligning teams, diagnosing root cause and following issues through to closure – taking them away from their day jobs", "WE IDT teams were spending valuable time aligning teams, diagnosing root causes and following issues through to closure, reducing capacity for planned delivery.")
replace_exact(s, "BAT WE and ITC Infotech set up the Service Improvement Programme, with a dedicated SIP Manager to own it day to day.", "BAT WE and ITC Infotech established the Service Improvement Programme, with a dedicated SIP Manager responsible for day-to-day coordination.")

# Slide 4
s = prs.slides[3]
replace_exact(s, "Based onsite with BAT WE, the SIP Manager joins up the teams and markets and keeps the programme moving.", "Working closely with BAT WE, the SIP Manager joins up teams and markets and keeps the programme moving.")
replace_exact(s, "Internal scrums, daily end-market touchpoints, bi-weekly impact assessment and CI sessions.", "Internal scrums, daily end-market touchpoints, fortnightly impact assessments and CI sessions.")
replace_exact(s, "17 artefacts in one WE home, kept current and owned, from architecture to data.", "17 artefacts in one WE home, with named ownership and a planned refresh cycle, spanning architecture to data.")

# Slide 5
s = prs.slides[4]
replace_exact(s, "Brought together and kept current by the SIP Manager in one WE Documentation Hub. Each artefact answers one question.", "Brought together by the SIP Manager in one WE Documentation Hub. Each artefact should answer a defined operational or delivery question and have a named owner.")
replace_exact(s, "Where does it break, and who owns it?", "Where can it break, and who owns it?")
replace_exact(s, "Are we on track, and what is at risk?", "Are we on track, and what is at risk?")
replace_exact(s, "Is it healthy, and what do we fix next?", "Is it healthy, and what should we fix next?")

# Slide 6: replace TBC content with a clear evidence-gap slide.
s = prs.slides[5]
replace_exact(s, "Western Europe: Incident / Issue stats TBC", "Western Europe: service-performance baseline to be established")
replace_exact(s, "TBC – Still collecting data", "The programme has strengthened governance and knowledge, but the source material does not yet provide an agreed baseline for incident volume, diagnosis time or root-cause closure.")
add_box(s, 0.75, 2.25, 3.7, 2.25, WHITE, LIGHT_BLUE)
add_text(s, "Current position", 1.0, 2.55, 3.15, 0.3, 16, NAVY, True)
add_text(s, "Governance and artefacts are improving. Quantified service-performance evidence is not yet available in the source pack.", 1.0, 3.05, 3.15, 0.95, 12, INK)
add_box(s, 4.8, 2.25, 3.7, 2.25, WHITE, LIGHT_BLUE)
add_text(s, "Why it matters", 5.05, 2.55, 3.15, 0.3, 16, NAVY, True)
add_text(s, "Without a baseline, leadership cannot yet quantify the programme's effect on service quality, responsiveness or efficiency.", 5.05, 3.05, 3.15, 0.95, 12, INK)
add_box(s, 8.85, 2.25, 3.7, 2.25, LIGHT_GOLD, GOLD)
add_text(s, "Next measurement step", 9.1, 2.55, 3.15, 0.3, 16, NAVY, True)
add_text(s, "Agree definitions and capture a baseline for aged blockers, diagnosis time, action closure, change failure and stakeholder confidence.", 9.1, 3.05, 3.15, 0.95, 12, INK)
add_box(s, 0.75, 5.0, 11.8, 0.72, BLUE, BLUE)
add_text(s, "Evidence gap to close during the proof period: move from activity reporting to measured service outcomes.", 1.0, 5.22, 11.3, 0.25, 13, WHITE, True, PP_ALIGN.CENTER)

# Slide 7
s = prs.slides[6]
replace_exact(s, "The journey from fragmented… to the end goal of fully governed", "The journey from fragmented coordination to governed service management")
replace_exact(s, "The service is easier to navigate and manage, for BAT WE and for the ITC teams alike.", "The service is easier to navigate and manage for BAT WE and the ITC teams.")
replace_exact(s, "Architecture and integration knowledge captured\n(Work In Progress)", "Architecture and integration knowledge captured\n(In progress)")
replace_exact(s, "UAT evidence, retrospectives and tracked actions\n(Work In Progress)", "UAT evidence, retrospectives and tracked actions\n(In progress)")
replace_exact(s, "Weekly grooming based on business impact*\n(Work In Progress)", "Weekly grooming based on business impact*\n(In progress)")
replace_exact(s, "RAID, due dates, RAG and named owners\n(Work In Progress)", "RAID, due dates, RAG and named owners\n(In progress)")
replace_exact(s, "Next horizon:  coordination and transparency have stepped up. The joint focus now moves to prevention, monitoring and faster root-cause closure.", "Next horizon: coordination and transparency have improved. The joint focus now moves to prevention, monitoring and faster root-cause closure.")
replace_exact(s, "*Early 2027 to revisit – WE POD reinstatement / clearer governance on Global Pod capacity & prioritisation", "*Review in early 2027: WE POD reinstatement and clearer governance of Global POD capacity and prioritisation.")

# Slide 8
s = prs.slides[7]
replace_exact(s, "Led day to day by the SIP Manager, working closely with BAT WE IDT and the ITC teams.", "Led day to day by the SIP Manager, working closely with BAT WE IDT and the ITC teams.")
replace_exact(s, "Bi-weekly CI sessions now focus on progress, blockers, escalation and guidance.", "Fortnightly CI sessions now focus on progress, blockers, escalation and guidance.")
replace_contains(s, "bi-weekly", "fortnightly")
replace_exact(s, "One WE wiki / SharePoint space for every maintained artefact.", "One WE wiki and SharePoint space for maintained artefacts.")
replace_exact(s, "Behaviour & Mindset Shift from REACTIVE to PROACTIVE", "Behaviour and mindset shift: reactive to proactive")

# Slide 9
s = prs.slides[8]
replace_exact(s, "The current SOW ends in January 2027. We recommend building on these foundations rather than pausing them.", "The current SOW is understood to end in January 2027. We recommend building on these foundations rather than pausing them, subject to commercial confirmation.")
replace_exact(s, "Keeps the rhythm, governance and documentation live, with one point of ownership for WE, and shifts the 2027 focus to prevention and monitoring.", "Keeps the rhythm, governance and documentation live, with one point of ownership for WE. The 2027 focus then shifts to prevention and monitoring.")
replace_exact(s, "Observability / monitoring tool\n\nAutomation testing", "Observability and monitoring\nAutomation testing")
replace_exact(s, "What benefits will the above bring?", "Expected benefits to validate")
replace_exact(s, "benefits", "Fewer aged blockers and less rework")
replace_exact(s, "benefits", "Earlier visibility of service risk and incidents")

# The two identical placeholder strings above are intentionally replaced sequentially by
# targeting the remaining shapes on the slide.
remaining = [sh for sh in all_text_shapes(s) if sh.text.strip() == "benefits"]
if remaining:
    replace_exact(s, "benefits", "A scalable BAU governance model")
if not any("BAU governance model" in sh.text for sh in all_text_shapes(s)):
    add_text(s, "A scalable BAU governance model", 7.52, 6.28, 5.1, 0.38, 11, INK)

# Slide 10: remove ambiguity and improve the leadership ask.
s = prs.slides[9]
replace_exact(s, "Where we stand commercially today, and the three decisions that set up 2027.", "The commercial position and three decisions required to set up 2027.")
replace_exact(s, "Shifting behaviors and unlocking the tools which can accelerate this", "Shifting behaviours and unlocking tools that can accelerate this")
replace_exact(s, "Endorse the period to May 2027", "Endorse a proposed extension through May 2027")
replace_exact(s, "Extend SOW to see through original SIP scope", "Extend the SOW to complete the original SIP scope, subject to contractual confirmation")
replace_exact(s, "Agree to a discovery for what Phase 2 could look like", "Agree a discovery phase for the next operating model")
replace_exact(s, "Come back in Jan/Feb with proposal", "Return in January or February with an evidence-based proposal")
replace_exact(s, "Agree Team Structure and transform “SIP Manager” to BAU", "Agree the team structure and transition SIP Manager activity into BAU")
replace_exact(s, "Agree in principle the need, and align in early 2027 on commercials / proposal for WoW", "Agree the principle and align in early 2027 on commercials and the proposed way of working")

# Slide 11
s = prs.slides[10]
replace_exact(s, "For the partnership, the openness and the support of the BAT Western Europe IDT team.", "Thank you for the partnership, openness and support of the BAT Western Europe IDT team.")

# Global typography and alignment hygiene for existing text boxes.
for slide in prs.slides:
    for sh in all_text_shapes(slide):
        if sh.left < Inches(0.3):
            sh.left = Inches(0.55)
        if sh.left + sh.width > prs.slide_width:
            sh.width = prs.slide_width - sh.left - Inches(0.35)
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if r.font.name is None:
                    r.font.name = "Aptos"

prs.save(OUT)
print(OUT)
