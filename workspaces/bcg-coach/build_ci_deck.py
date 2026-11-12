from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE_DASH_STYLE

OUT = "/tmp/ci2026_review/BCG-CI-Presentation.pptx"
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY = RGBColor(14, 43, 99)
BLUE = RGBColor(23, 70, 139)
GOLD = RGBColor(250, 180, 30)
INK = RGBColor(35, 45, 60)
MID = RGBColor(92, 105, 122)
PALE = RGBColor(247, 249, 252)
LIGHT_BLUE = RGBColor(230, 235, 243)
LIGHT_GOLD = RGBColor(255, 247, 222)
GREEN = RGBColor(35, 126, 91)
RED = RGBColor(176, 64, 64)
WHITE = RGBColor(255, 255, 255)

def set_bg(slide, color=PALE):
    fill = slide.background.fill
    fill.solid(); fill.fore_color.rgb = color

def box(slide, x, y, w, h, fill=WHITE, line=LIGHT_BLUE, radius=True):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                                   Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid(); shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line; shape.line.width = Pt(1)
    return shape

def text(slide, value, x, y, w, h, size=16, colour=INK, bold=False, align=PP_ALIGN.LEFT,
         font="Aptos", valign=MSO_ANCHOR.TOP, margin=0.06):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.clear(); tf.word_wrap = True
    tf.margin_left = Inches(margin); tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin); tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = value
    r.font.name = font; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = colour
    return tb

def rich_text(slide, lines, x, y, w, h, size=14, colour=INK, bullet=True, leading=1.05):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.clear(); tf.word_wrap = True
    tf.margin_left = Inches(0.08); tf.margin_right = Inches(0.08)
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.name = "Aptos"; p.font.size = Pt(size); p.font.color.rgb = colour
        p.space_after = Pt(5); p.line_spacing = leading
        if bullet: p.level = 0
    return tb

def header(slide, kicker, title, number):
    text(slide, "BAT  |  WESTERN EUROPE CONSUMER TECHNOLOGY", 0.55, 0.25, 6.5, 0.25, 9, BLUE, True)
    text(slide, kicker.upper(), 0.55, 0.73, 3.4, 0.28, 10, GOLD, True)
    text(slide, title, 0.55, 1.04, 12.1, 0.62, 25, NAVY, True)
    slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(1.78), Inches(12.2), Inches(0.03)).fill.solid()
    line = slide.shapes[-1]; line.fill.fore_color.rgb = GOLD; line.line.fill.background()
    text(slide, str(number), 12.35, 0.25, 0.35, 0.25, 10, MID, True, PP_ALIGN.RIGHT)

def footer(slide, source="Source: CI-2026 PowerPoint and action-plan workbook; status fields retained as supplied"):
    text(slide, source, 0.58, 7.12, 11.7, 0.18, 7.5, MID)
    text(slide, "CONFIDENTIAL | LEADERSHIP DISCUSSION", 10.45, 7.12, 2.3, 0.18, 7.5, MID, True, PP_ALIGN.RIGHT)

def pill(slide, label, x, y, w, fill, colour=WHITE):
    s = box(slide, x, y, w, 0.34, fill, fill, True)
    text(slide, label, x, y+0.01, w, 0.29, 9, colour, True, PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    return s

def add_slide(kicker, title, number):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(slide); header(slide, kicker, title, number); return slide

# 1
s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s, NAVY)
text(s, "BAT", 0.65, 0.55, 1.3, 0.45, 26, WHITE, True)
text(s, "WESTERN EUROPE CONSUMER TECHNOLOGY", 0.65, 1.02, 6.7, 0.25, 10, GOLD, True)
text(s, "Continuous Improvement\nProgramme", 0.65, 1.75, 8.4, 1.15, 36, WHITE, True)
text(s, "From fragmented improvement activity to coordinated service outcomes", 0.68, 3.15, 8.6, 0.65, 21, RGBColor(220,230,245))
box(s, 0.68, 4.4, 4.8, 1.22, BLUE, BLUE)
text(s, "EXECUTIVE SHOWCASE", 0.95, 4.68, 3.5, 0.25, 12, GOLD, True)
text(s, "Progress to date | value created | proof period | decisions required", 0.95, 5.02, 4.1, 0.42, 14, WHITE)
text(s, "Leadership review | 11 November 2026", 0.68, 6.7, 5.5, 0.25, 10, RGBColor(190,205,230))
text(s, "1", 12.35, 0.45, 0.35, 0.25, 10, RGBColor(190,205,230), True, PP_ALIGN.RIGHT)

# 2
s = add_slide("Executive storyline", "The programme has established control; leadership now needs to decide how to sustain it", 2)
text(s, "The evidence supports a stronger operating foundation. The next step is to prove measurable service outcomes.", 0.7, 2.05, 11.6, 0.35, 15, MID)
items = [("01", "Why change was needed", "Fragmented delivery, knowledge gaps and inconsistent controls created avoidable coordination effort."),
         ("02", "What has changed", "A repeatable operating rhythm, clearer governance and a central knowledge environment are now in place."),
         ("03", "What the organisation gains", "Greater transparency, clearer ownership and safer technical decisions across core WE services."),
         ("04", "What leaders must decide", "Confirm the proof period, success measures and the 2027 operating and funding model.")]
for i,(n,head,body) in enumerate(items):
    x = 0.7 + (i%2)*6.05; y = 2.65 + (i//2)*1.65
    box(s,x,y,5.55,1.25,WHITE, LIGHT_BLUE)
    text(s,n,x+0.22,y+0.18,0.45,0.35,18,GOLD,True)
    text(s,head,x+0.85,y+0.16,4.35,0.28,14,NAVY,True)
    text(s,body,x+0.85,y+0.52,4.3,0.52,11.5,INK)
box(s,0.7,6.1,11.6,0.58,LIGHT_GOLD,GOLD)
text(s,"Leadership implication: the programme now needs an explicit decision framework, not additional informal coordination.",0.95,6.25,11.1,0.25,13,NAVY,True)
footer(s)

# 3
s = add_slide("Case for change", "The service challenge was systemic, not a single defect", 3)
text(s,"Three mutually reinforcing gaps increased coordination effort and slowed diagnosis.",0.7,2.05,11.5,0.3,15,MID)
gaps=[("Fragmented delivery", ["Communication varied across teams","Dependencies surfaced late","Backlog priorities were not consistently shared"], "Higher coordination cost and slower dependency resolution"),
      ("Knowledge gaps", ["Architecture coverage was incomplete","Supported-system knowledge was limited","Handovers drove reverse engineering"], "Longer diagnosis cycles and person-dependency risk"),
      ("Control gaps", ["Monitoring and observability were limited","Delivery artefacts were used inconsistently","Technical-debt governance needed strengthening"], "Inconsistent prioritisation and weaker prevention")]
for i,(head,bullets,cons) in enumerate(gaps):
    x=0.7+i*4.05
    box(s,x,2.65,3.65,2.7,WHITE,LIGHT_BLUE)
    text(s,head,x+0.2,2.88,3.2,0.3,16,NAVY,True)
    rich_text(s,bullets,x+0.22,3.35,3.15,1.2,11.5,INK,True)
    box(s,x+0.2,4.72,3.2,0.4,LIGHT_GOLD,GOLD)
    text(s,cons,x+0.3,4.78,3.0,0.25,9.5,NAVY,True,PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
box(s,0.7,5.8,11.6,0.65,BLUE,BLUE)
text(s,"Why a SIP Manager?  One coordination point connects workstreams, makes ownership explicit and gives leadership a single view of progress and blockers.",0.95,5.98,11.1,0.3,13,WHITE,True)
footer(s)

# 4
s = add_slide("Progress to date", "Four capability pillars convert recurring issues into a governed improvement system", 4)
text(s,"The programme has created a documented, governed and more observable foundation for support and change.",0.7,2.05,11.6,0.3,15,MID)
pillars=[("01","Architecture & integration","Landscape, WE architecture, AIS integration and CRM error-handling documentation."),
         ("02","Requirements & knowledge","Use cases, user journeys, data dictionary and a central knowledge environment."),
         ("03","Delivery governance","ADO hygiene, delivery plans, RAID, RAG, meeting discipline and retrospectives."),
         ("04","Debt & observability","Technical-debt governance and a dashboard for D2C applications and services.")]
for i,(n,h,b) in enumerate(pillars):
    x=0.7+(i%2)*6.05; y=2.65+(i//2)*1.65
    box(s,x,y,5.55,1.25,WHITE,LIGHT_BLUE)
    box(s,x+0.2,y+0.2,0.62,0.62,NAVY,NAVY)
    text(s,n,x+0.2,y+0.33,0.62,0.22,12,GOLD,True,PP_ALIGN.CENTER)
    text(s,h,x+1.05,y+0.2,4.1,0.28,14,NAVY,True)
    text(s,b,x+1.05,y+0.58,4.15,0.42,11.3,INK)
box(s,0.7,6.08,11.6,0.55,LIGHT_GOLD,GOLD)
text(s,"Outcome: greater transparency, stronger governance and safer, better-informed technical decisions.",0.95,6.22,11.1,0.25,13,NAVY,True)
footer(s)

# 5
s = add_slide("Evidence of progress", "The artefact register shows a foundation established, with a defined completion runway", 5)
text(s,"Status counts are derived from the source workbook and describe artefact progress, not service performance.",0.7,2.05,11.7,0.3,14,MID)
counts=[("Completed",6,GREEN),("In progress",6,GOLD),("Not started",7,RED)]
for i,(label,count,col) in enumerate(counts):
    x=0.85+i*2.4
    c=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x),Inches(2.8),Inches(1.35),Inches(1.35)); c.fill.solid(); c.fill.fore_color.rgb=col; c.line.color.rgb=col
    text(s,str(count),x,3.08,1.35,0.5,26,WHITE,True,PP_ALIGN.CENTER)
    text(s,label,x-0.25,4.28,1.85,0.25,12,NAVY,True,PP_ALIGN.CENTER)
box(s,8.0,2.65,4.1,2.1,WHITE,LIGHT_BLUE)
text(s,"What is evidenced",8.25,2.88,3.4,0.28,14,NAVY,True)
rich_text(s,["Architecture landscape completed","Use cases and journeys completed","RAID and technical-debt governance completed","Standardised minutes, demos and retrospectives"],8.25,3.3,3.45,1.2,11.2,INK,True)
box(s,0.7,5.25,11.6,1.05,LIGHT_GOLD,GOLD)
text(s,"What still needs proof",0.95,5.48,2.4,0.25,13,NAVY,True)
text(s,"Service-level and incident outcomes | aged blockers and rework | adoption and currency | cost, cycle-time or productivity impact | BAU owners",3.0,5.45,8.8,0.4,12,INK)
footer(s,"Source: Artefacts worksheet, status snapshot supplied in CI-2026 workbook")

# 6
s = add_slide("Operating model shift", "The most material change is from reactive coordination to governed ownership", 6)
text(s,"The narrative is strong; the next step is to attach baseline and target measures.",0.7,2.05,11.5,0.3,15,MID)
headers=["DIMENSION","BEFORE","NOW"]
for i,h in enumerate(headers):
    x=[0.7,2.35,7.35][i]; w=[1.45,4.7,4.95][i]
    box(s,x,2.65,w,0.45,NAVY,NAVY,False); text(s,h,x+0.1,2.76,w-0.2,0.2,11,WHITE,True,PP_ALIGN.CENTER)
rows=[("Ownership","WE chased separate teams","SIP coordinates teams and escalations"),("Communication","Fragmented, reactive updates","Visible daily and weekly cadence"),("Diagnosis","Reverse engineering during incidents","Architecture and integration knowledge captured"),("Quality","Defects could recur after closure","UAT evidence, retrospectives and tracked actions"),("Prioritisation","Backlogs lacked shared ranking","Weekly grooming based on business impact"),("Governance","Risks and actions recorded inconsistently","RAID, RAG, due dates and named owners")]
for j,row in enumerate(rows):
    y=3.1+j*0.52
    for i,val in enumerate(row):
        x=[0.7,2.35,7.35][i]; w=[1.45,4.7,4.95][i]
        fill=WHITE if j%2==0 else RGBColor(242,246,251)
        box(s,x,y,w,0.48,fill,LIGHT_BLUE,False); text(s,val,x+0.1,y+0.1,w-0.2,0.25,10.5,NAVY if i==0 else INK,i==0)
box(s,0.7,6.35,11.6,0.45,BLUE,BLUE)
text(s,"Priority next: sustain prevention, strengthen monitoring and accelerate root-cause closure.",0.95,6.47,11.1,0.22,12.5,WHITE,True)
footer(s)

# 7
s = add_slide("Business impact", "The programme improves organisational efficiency through reduced friction and better decision quality", 7)
text(s,"Capability creation is evidenced. Quantified business impact now needs a scorecard.",0.7,2.05,11.6,0.3,15,MID)
impacts=[("Faster diagnosis","Reusable architecture, integration and configuration knowledge should reduce dependency on individuals during incidents."),
         ("Lower coordination effort","A common cadence, RAID and action discipline make blockers visible earlier and reduce follow-up effort."),
         ("Safer change","UAT evidence, retrospectives and clearer requirements strengthen learning and reduce repeat-failure risk."),
         ("Better investment choices","A governed technical-debt backlog links engineering work to product priorities and funding decisions.")]
for i,(h,b) in enumerate(impacts):
    x=0.7+(i%2)*6.05; y=2.65+(i//2)*1.55
    box(s,x,y,5.55,1.15,WHITE,LIGHT_BLUE)
    text(s,h,x+0.22,y+0.18,4.9,0.28,15,NAVY,True)
    text(s,b,x+0.22,y+0.54,4.95,0.4,11.2,INK)
box(s,0.7,5.95,11.6,0.67,LIGHT_GOLD,GOLD)
text(s,"Evidence boundary: the source files evidence capability creation; they do not yet quantify time, cost, SLA or quality improvements.",0.95,6.16,11.1,0.25,12.5,NAVY,True)
footer(s)

# 8
s = add_slide("Remaining work", "The proof period should convert activity into measurable outcomes and durable BAU ownership", 8)
text(s,"The action tracker contains a credible backlog, but priorities, owners and dates need tighter governance.",0.7,2.05,11.6,0.3,15,MID)
stages=[("NOW","Stabilise","Complete priority artefacts; confirm owners and dates; publish a single baseline scorecard.",NAVY),
        ("NEXT","Prove","Track aged blockers, diagnosis time, action closure, debt movement and stakeholder outcomes.",BLUE),
        ("THEN","Embed","Confirm BAU ownership, artefact review cadence, funding route and the 2027 operating model.",GOLD)]
for i,(tag,h,b,col) in enumerate(stages):
    x=0.7+i*4.05
    box(s,x,2.75,3.65,2.1,WHITE,LIGHT_BLUE)
    pill(s,tag,x+0.2,2.98,0.82,col,WHITE if col!=GOLD else NAVY)
    text(s,h,x+0.2,3.5,3.1,0.3,17,NAVY,True)
    text(s,b,x+0.2,3.95,3.1,0.58,11.5,INK)
box(s,0.7,5.35,11.6,0.9,LIGHT_GOLD,GOLD)
text(s,"Critical gap to close",0.95,5.55,2.1,0.25,13,NAVY,True)
text(s,"Convert the action tracker into a decision-quality portfolio: one accountable owner, one due date, one outcome measure and one escalation path per priority item.",3.0,5.52,8.9,0.4,12,INK)
footer(s)

# 9
s = add_slide("Recommendation", "Use November to January as an outcome-proof period, then confirm the 2027 model", 9)
text(s,"This preserves momentum while giving leadership evidence before making a longer-term commitment.",0.7,2.05,11.6,0.3,15,MID)
box(s,0.7,2.65,7.0,1.45,BLUE,BLUE)
text(s,"RECOMMENDATION",0.98,2.92,2.0,0.25,11,GOLD,True)
text(s,"Retain the SIP Manager role through January 2027 and use the period to prove measurable service outcomes before committing to the full-year model.",0.98,3.28,6.25,0.5,15,WHITE,True)
box(s,8.1,2.65,4.2,2.45,WHITE,LIGHT_BLUE)
text(s,"Leadership decisions required",8.38,2.92,3.5,0.28,14,NAVY,True)
rich_text(s,["Endorse the proof period","Nominate the 2027 funding owner","Choose the future operating model","Approve the outcome scorecard"],8.38,3.35,3.45,1.25,11.5,INK,True)
box(s,0.7,4.55,11.6,1.35,LIGHT_GOLD,GOLD)
text(s,"Conditions for continuation",0.98,4.82,2.6,0.25,13,NAVY,True)
text(s,"Priority artefacts completed  |  aged blockers reduced  |  service outcomes evidenced  |  BAU ownership confirmed",3.35,4.8,8.35,0.35,12,INK)
text(s,"Caveat: reconfirm commercial figures and contract dates before leadership circulation.",0.98,5.45,10.8,0.25,10.5,MID,True)
footer(s)

# 10
s = add_slide("Measurement layer", "A compact scorecard will turn a credible improvement narrative into a defensible business case", 10)
text(s,"Measure outcomes, not activity volume. Baselines and targets must be agreed before the proof period.",0.7,2.05,11.6,0.3,15,MID)
cols=[("OUTCOME",0.7,1.4), ("MEASURE",2.35,3.6), ("EVIDENCE STATUS",6.05,3.3), ("CADENCE",9.5,2.8)]
for h,x,w in cols:
    box(s,x,2.62,w,0.42,NAVY,NAVY,False); text(s,h,x+0.08,2.72,w-0.16,0.18,10,WHITE,True,PP_ALIGN.CENTER)
score=[("Diagnosis","Time to identify root cause","Baseline required","Monthly"),("Flow","Aged blockers over 30 days","Baseline required","Fortnightly"),("Delivery","Action closure by due date","Baseline required","Weekly"),("Quality","Change failure / rework rate","Validate definition of ~0%","Monthly"),("Knowledge","Priority artefacts current and owned","6 completed / 6 in progress / 7 not started","Monthly"),("Stakeholders","WE stakeholder confidence","Baseline survey required","Quarterly")]
for j,row in enumerate(score):
    y=3.04+j*0.49
    for i,(val,_,_) in enumerate([row[:3]]): pass
    vals=[row[0],row[1],row[2],row[3]]
    for i,val in enumerate(vals):
        x=[0.7,2.35,6.05,9.5][i]; w=[1.4,3.6,3.3,2.8][i]
        fill=WHITE if j%2==0 else RGBColor(242,246,251)
        box(s,x,y,w,0.45,fill,LIGHT_BLUE,False); text(s,val,x+0.08,y+0.09,w-0.16,0.25,9.5,NAVY if i==0 else INK,i==0)
box(s,0.7,6.2,11.6,0.55,BLUE,BLUE)
text(s,"Decision rule: continue where measured service outcomes improve, or leading indicators show credible progress towards them.",0.95,6.36,11.1,0.22,12,WHITE,True)
footer(s)

# 11
s = add_slide("Critical appraisal", "Strong foundation; the next version should sharpen evidence, metrics and ownership", 11)
text(s,"Assessment based on the CI-2026 PowerPoint and action-plan workbook.",0.7,2.05,11.6,0.3,15,MID)
sections=[("STRENGTHS",["Clear case for change","Coherent capability pillars","Strong governance narrative","Credible proof-period recommendation"],GREEN),
          ("WEAKNESSES",["Few quantified outcomes","Inconsistent dates and status fields","Several owners remain TBD","Duplicate or overlapping actions"],RED),
          ("PRESENTATION & FOCUS",["Keep evidence labels visible","Explain terminology at first use","Prioritise long artefact lists","Lead with decisions and outcomes"],BLUE)]
for i,(h,bullets,col) in enumerate(sections):
    x=0.7+i*4.05
    box(s,x,2.7,3.65,2.6,WHITE,LIGHT_BLUE)
    text(s,h,x+0.2,2.95,3.2,0.3,14,col,True)
    rich_text(s,bullets,x+0.2,3.45,3.15,1.35,11.5,INK,True)
box(s,0.7,5.75,11.6,0.72,LIGHT_GOLD,GOLD)
text(s,"Overall judgement: ready for a leadership discussion as a progress-and-decision deck; not yet a benefits-realisation report.",0.95,5.98,11.1,0.27,13,NAVY,True)
footer(s)

# 12
s = add_slide("Leadership close", "The programme has built the management system; leadership must now convert it into measured outcomes", 12)
text(s,"The next decision is not whether continuous improvement is needed. It is how to sustain it, measure it and assign ownership.",0.7,2.05,11.6,0.45,18,NAVY,True)
box(s,0.7,2.9,3.65,1.65,BLUE,BLUE)
text(s,"1",0.95,3.15,0.45,0.4,24,GOLD,True)
text(s,"Endorse the proof period",1.55,3.12,2.4,0.3,15,WHITE,True)
text(s,"Use the next period to evidence service outcomes.",1.55,3.55,2.35,0.45,11.5,WHITE)
box(s,4.85,2.9,3.65,1.65,NAVY,NAVY)
text(s,"2",5.1,3.15,0.45,0.4,24,GOLD,True)
text(s,"Approve the scorecard",5.7,3.12,2.4,0.3,15,WHITE,True)
text(s,"Agree baselines, targets and review cadence.",5.7,3.55,2.35,0.45,11.5,WHITE)
box(s,9.0,2.9,3.3,1.65,GOLD,GOLD)
text(s,"3",9.25,3.15,0.45,0.4,24,NAVY,True)
text(s,"Assign the 2027 owner",9.85,3.12,2.1,0.3,15,NAVY,True)
text(s,"Decide the operating and funding model.",9.85,3.55,2.1,0.45,11.5,NAVY)
box(s,0.7,5.35,11.6,0.65,LIGHT_BLUE,LIGHT_BLUE)
text(s,"Success looks like: fewer aged blockers, faster diagnosis, stronger change quality and a maintained knowledge base with clear BAU accountability.",0.95,5.55,11.1,0.25,13,NAVY,True,PP_ALIGN.CENTER)
footer(s)

prs.save(OUT)
print(OUT)
