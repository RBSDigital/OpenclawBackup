const pptxgen = require('/tmp/ci-deck/node_modules/pptxgenjs');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Ada';
pptx.subject = 'Continuous Improvement programme showcase';
pptx.title = 'Continuous Improvement Programme | Executive Showcase';
pptx.company = 'BAT Western Europe Consumer Technology';
pptx.lang = 'en-GB';
pptx.theme = {
  headFontFace: 'Aptos Display', bodyFontFace: 'Aptos', lang: 'en-GB'
};
pptx.defineSlideMaster({
  title: 'MASTER', background: { color: 'F7F9FC' },
  objects: [
    { rect: { x: 0, y: 0, w: 13.333, h: 0.13, fill: { color: '0B1F3A' }, line: { color: '0B1F3A' } } },
    { text: { text: 'BAT | WESTERN EUROPE CONSUMER TECHNOLOGY', options: { x: 0.55, y: 7.12, w: 5.5, h: 0.18, fontFace: 'Aptos', fontSize: 7, color: '617084', margin: 0 } } },
    { text: { text: 'Continuous Improvement Programme', options: { x: 9.0, y: 7.12, w: 3.7, h: 0.18, fontFace: 'Aptos', fontSize: 7, color: '617084', align: 'right', margin: 0 } } }
  ],
  slideNumber: { x: 12.82, y: 7.08, color: '617084', fontFace: 'Aptos', fontSize: 7 }
});

const C = { navy:'0B1F3A', blue:'1B5E9E', teal:'008A8A', green:'2E8B57', amber:'D68A00', red:'B54747', ink:'172B4D', muted:'617084', pale:'EAF2F8', light:'F7F9FC', white:'FFFFFF', line:'D8E0EA' };
const addTitle = (s, kicker, title, sub='') => {
  s.addText(kicker.toUpperCase(), {x:0.65,y:0.42,w:4.8,h:0.22,fontSize:9,bold:true,color:C.teal,charSpacing:1.2,margin:0});
  s.addText(title, {x:0.65,y:0.72,w:11.8,h:0.5,fontSize:25,bold:true,color:C.navy,margin:0,breakLine:false,fit:'shrink'});
  if(sub) s.addText(sub,{x:0.67,y:1.28,w:11.5,h:0.35,fontSize:11,color:C.muted,margin:0,fit:'shrink'});
};
const box = (s,x,y,w,h,fill=C.white,line=C.line,r=0.08)=>s.addShape(pptx.ShapeType.roundRect,{x,y,w,h,rectRadius:r,fill:{color:fill},line:{color:line,width:1}});
const txt = (s,text,x,y,w,h,opts={})=>s.addText(text,{x,y,w,h,fontFace:opts.fontFace||'Aptos',fontSize:opts.fontSize||12,color:opts.color||C.ink,bold:opts.bold||false,margin:opts.margin===undefined?0.05:opts.margin,breakLine:false,fit:'shrink',valign:opts.valign||'mid',align:opts.align||'left',bullet:opts.bullet,italic:opts.italic||false});
const pill = (s,label,x,y,w,color)=>{s.addShape(pptx.ShapeType.roundRect,{x,y,w,h:0.27,rectRadius:0.12,fill:{color},line:{color}});txt(s,label,x,y+0.01,w,0.2,{fontSize:8,bold:true,color:C.white,align:'center'});};
const section = (s,n,label,x,y,w)=>{txt(s,String(n).padStart(2,'0'),x,y,w*0.2,0.25,{fontSize:13,bold:true,color:C.teal});txt(s,label,x+w*0.22,y,w*0.78,0.25,{fontSize:10,bold:true,color:C.navy});};

// 1 Cover
{ const s=pptx.addSlide('MASTER'); s.background={color:C.navy};
  s.addShape(pptx.ShapeType.rect,{x:0,y:0,w:13.333,h:7.5,fill:{color:C.navy},line:{color:C.navy}});
  s.addShape(pptx.ShapeType.arc,{x:8.4,y:-1.0,w:6.2,h:6.2,line:{color:'1B5E9E',transparency:20,width:3},adjustPoint:0.25});
  s.addShape(pptx.ShapeType.arc,{x:9.2,y:0.0,w:4.4,h:4.4,line:{color:'00A6A6',transparency:10,width:2},adjustPoint:0.25});
  txt(s,'BAT | WESTERN EUROPE CONSUMER TECHNOLOGY',0.72,0.7,7,0.25,{fontSize:10,bold:true,color:'A9D5E5'});
  txt(s,'Continuous Improvement\nProgramme',0.72,1.55,8.2,1.45,{fontSize:34,bold:true,color:C.white});
  txt(s,'From fragmented improvement activity to coordinated service outcomes',0.76,3.35,7.2,0.55,{fontSize:18,color:'D6E5F0'});
  txt(s,'Progress to date | value created | proof period | decisions required',0.76,4.15,7.6,0.3,{fontSize:12,color:'A9D5E5'});
  s.addShape(pptx.ShapeType.line,{x:0.76,y:5.15,w:2.0,h:0,line:{color:C.teal,width:3}});
  txt(s,'EXECUTIVE SHOWCASE',0.76,5.38,3,0.25,{fontSize:10,bold:true,color:'6FE0D0',charSpacing:1});
  txt(s,'Leadership review | 11 November 2026',0.76,6.63,5,0.22,{fontSize:9,color:'A9D5E5'});
}

// 2 executive story
{ const s=pptx.addSlide('MASTER'); addTitle(s,'Executive storyline','The programme has established control; leadership now needs to decide how to sustain it','Evidence supports a stronger operating foundation. The next step is to prove measurable service outcomes.');
  const items=[['01','Why change was needed','Fragmented delivery, knowledge gaps and inconsistent controls created avoidable coordination effort.'],['02','What has changed','A repeatable operating rhythm, clearer governance and a central knowledge environment are now in place.'],['03','What the organisation gains','Greater transparency, clearer ownership and safer technical decisions across core WE services.'],['04','What leaders must decide','Confirm the proof period, success measures and the 2027 operating and funding model.']];
  items.forEach((it,i)=>{let y=1.9+i*0.95; box(s,0.75,y,11.8,0.75,i===3?'EAF7F5':C.white); txt(s,it[0],1.0,y+0.15,0.45,0.35,{fontSize:14,bold:true,color:C.teal}); txt(s,it[1],1.65,y+0.12,3.1,0.22,{fontSize:13,bold:true,color:C.navy}); txt(s,it[2],4.9,y+0.12,7.2,0.38,{fontSize:11,color:C.ink});});
  box(s,0.75,6.05,11.8,0.55,C.navy,C.navy);txt(s,'Leadership implication',1.0,6.18,1.65,0.2,{fontSize:10,bold:true,color:'7CE3D2'});txt(s,'The programme now needs an explicit decision framework, not additional informal coordination.',2.85,6.17,9.25,0.22,{fontSize:12,bold:true,color:C.white});
}

// 3 case for change
{ const s=pptx.addSlide('MASTER'); addTitle(s,'Case for change','The service challenge was systemic, not a single defect','The source material identifies three mutually reinforcing gaps.');
  const cols=[['Fragmented delivery','Communication varied across teams\nDependencies surfaced late\nBacklog priorities were not consistently shared',C.blue],['Knowledge gaps','Architecture coverage was incomplete\nSupported-system knowledge was limited\nHandovers drove reverse engineering',C.teal],['Control gaps','Monitoring and observability were limited\nDelivery artefacts were used inconsistently\nTechnical-debt governance needed strengthening',C.amber]];
  cols.forEach((c,i)=>{let x=0.75+i*4.15;box(s,x,1.95,3.7,3.1,C.white,C.line);s.addShape(pptx.ShapeType.rect,{x,y:1.95,w:3.7,h:0.14,fill:{color:c[2]},line:{color:c[2]}});txt(s,c[0],x+0.25,2.3,3.15,0.35,{fontSize:16,bold:true,color:C.navy});txt(s,c[1],x+0.25,2.9,3.1,1.4,{fontSize:12,color:C.ink,breakLine:true});txt(s,'Business consequence',x+0.25,4.65,1.5,0.18,{fontSize:9,bold:true,color:C.muted});txt(s,i===0?'Higher coordination cost and slower dependency resolution':i===1?'Longer diagnosis cycles and person-dependency risk':'Inconsistent prioritisation and weaker prevention',x+0.25,4.9,3.1,0.45,{fontSize:11,bold:true,color:C.ink});});
  box(s,0.75,5.55,11.8,0.75,'EAF2F8','B8D4E8');txt(s,'Consulting judgement',1.0,5.73,1.55,0.18,{fontSize:10,bold:true,color:C.blue});txt(s,'A SIP Manager creates value by connecting ownership, evidence and decisions across workstreams — not by adding another reporting layer.',2.75,5.69,9.3,0.3,{fontSize:13,bold:true,color:C.navy});
}

// 4 what done
{ const s=pptx.addSlide('MASTER'); addTitle(s,'Progress to date','Four capability pillars convert recurring issues into a governed improvement system','Source evidence: action tracker, artefact register and existing SIP narrative.');
  const pillars=[['01','Architecture & integration','Landscape, WE architecture, AIS integration and CRM error-handling documentation.',C.blue],['02','Requirements & knowledge','Use cases, user journeys, data dictionary and a central knowledge environment.',C.teal],['03','Delivery governance','ADO hygiene, delivery plans, RAID, RAG, meeting discipline and retrospectives.',C.green],['04','Debt & observability','Technical-debt governance and a dashboard for D2C applications and services.',C.amber]];
  pillars.forEach((p,i)=>{let x=0.75+(i%2)*6.0,y=1.85+Math.floor(i/2)*2.05;box(s,x,y,5.55,1.55,C.white,C.line);s.addShape(pptx.ShapeType.ellipse,{x:x+0.25,y:y+0.27,w:0.65,h:0.65,fill:{color:p[3]},line:{color:p[3]}});txt(s,p[0],x+0.25,y+0.47,0.65,0.18,{fontSize:10,bold:true,color:C.white,align:'center'});txt(s,p[1],x+1.15,y+0.25,4.0,0.25,{fontSize:15,bold:true,color:C.navy});txt(s,p[2],x+1.15,y+0.72,4.0,0.5,{fontSize:11,color:C.ink});});
  box(s,0.75,6.0,11.8,0.58,C.navy,C.navy);txt(s,'Outcome',1.0,6.17,0.8,0.18,{fontSize:10,bold:true,color:'7CE3D2'});txt(s,'A documented, governed and more observable foundation for ongoing support and change.',1.95,6.13,9.8,0.25,{fontSize:13,bold:true,color:C.white});
}

// 5 evidence dashboard
{ const s=pptx.addSlide('MASTER'); addTitle(s,'Evidence of progress','The artefact register shows a foundation established, with a defined completion runway','Status counts are derived from the source spreadsheet; they are not a measure of service performance.');
  const total=19, complete=6, progress=6, notstarted=7; const segments=[['Completed',complete,C.green],['In progress',progress,C.amber],['Not started',notstarted,C.line]]; let x=1.0;
  segments.forEach(seg=>{let w=9.5*seg[1]/total;s.addShape(pptx.ShapeType.rect,{x,y:2.05,w,h:0.55,fill:{color:seg[2]},line:{color:seg[2]}});x+=w;});
  txt(s,'6',1.0,1.25,0.6,0.5,{fontSize:28,bold:true,color:C.green});txt(s,'completed',1.72,1.39,1.2,0.18,{fontSize:10,color:C.muted});txt(s,'6',4.1,1.25,0.6,0.5,{fontSize:28,bold:true,color:C.amber});txt(s,'in progress',4.82,1.39,1.4,0.18,{fontSize:10,color:C.muted});txt(s,'7',7.3,1.25,0.6,0.5,{fontSize:28,bold:true,color:C.blue});txt(s,'not started',8.02,1.39,1.4,0.18,{fontSize:10,color:C.muted});
  segments.forEach((seg,i)=>{let xx=1.0+i*3.0;s.addShape(pptx.ShapeType.ellipse,{x:xx,y:2.9,w:0.18,h:0.18,fill:{color:seg[2]},line:{color:seg[2]}});txt(s,seg[0],xx+0.3,2.88,1.4,0.2,{fontSize:10,color:C.ink});});
  box(s,0.75,3.65,5.75,2.0,C.white,C.line);txt(s,'What is evidenced',1.0,3.95,2.8,0.25,{fontSize:15,bold:true,color:C.navy});txt(s,'• Architecture landscape completed\n• Use cases and user journeys completed\n• RAID log and technical-debt governance completed\n• Meeting minutes standardised\n• Recurring demos and retrospectives established',1.0,4.4,4.9,0.95,{fontSize:11,color:C.ink});
  box(s,6.8,3.65,5.75,2.0,'FFF8E8','F0D99A');txt(s,'What still needs proof',7.05,3.95,3.0,0.25,{fontSize:15,bold:true,color:C.navy});txt(s,'• Service-level and incident outcomes\n• Reduction in aged blockers and rework\n• Adoption and currency of artefacts\n• Cost, cycle-time or productivity impact\n• Named BAU owners and review cadence',7.05,4.4,4.9,0.95,{fontSize:11,color:C.ink});
}

// 6 before after
{ const s=pptx.addSlide('MASTER'); addTitle(s,'Operating model shift','The most material change is from reactive coordination to governed ownership','The narrative is strong; the next step is to attach baseline and target measures.');
  const rows=[['Ownership','WE chased separate teams','SIP coordinates teams and escalations'],['Communication','Fragmented, reactive updates','Visible daily and weekly cadence'],['Diagnosis','Reverse engineering during incidents','Architecture and integration knowledge captured'],['Quality','Defects could recur after closure','UAT evidence, retrospectives and tracked actions'],['Prioritisation','Backlogs lacked shared ranking','Weekly grooming based on business impact'],['Governance','Risks and actions recorded inconsistently','RAID, RAG, due dates and named owners']];
  txt(s,'DIMENSION',0.9,1.75,1.6,0.2,{fontSize:9,bold:true,color:C.muted});txt(s,'BEFORE',3.2,1.75,3.5,0.2,{fontSize:9,bold:true,color:C.red});txt(s,'NOW',8.0,1.75,4,0.2,{fontSize:9,bold:true,color:C.green});
  rows.forEach((r,i)=>{let y=2.05+i*0.63; if(i%2===0)s.addShape(pptx.ShapeType.rect,{x:0.75,y:y-0.05,w:11.8,h:0.55,fill:{color:'F0F4F8'},line:{color:'F0F4F8'}});txt(s,r[0],0.9,y,1.9,0.25,{fontSize:11,bold:true,color:C.navy});txt(s,r[1],3.2,y,4.05,0.25,{fontSize:11,color:C.ink});txt(s,r[2],8.0,y,4.2,0.25,{fontSize:11,bold:true,color:C.ink});});
  box(s,0.75,6.25,11.8,0.42,'EAF7F5','B8E5DD');txt(s,'Priority next',1.0,6.36,1.1,0.18,{fontSize:10,bold:true,color:C.teal});txt(s,'Sustain prevention, strengthen monitoring and accelerate root-cause closure.',2.25,6.33,9.5,0.22,{fontSize:12,bold:true,color:C.navy});
}

// 7 business impact
{ const s=pptx.addSlide('MASTER'); addTitle(s,'Business impact','The programme improves organisational efficiency through reduced friction and better decision quality','Impact claims should now move from qualitative narrative to measured scorecard.');
  const impacts=[['Faster diagnosis','Reusable architecture, integration and configuration knowledge should reduce dependency on individuals during incidents.',C.blue],['Lower coordination effort','A common cadence, RAID and action discipline make blockers visible earlier and reduce follow-up effort.',C.teal],['Safer change','UAT evidence, retrospectives and clearer requirements strengthen learning and reduce repeat failure risk.',C.green],['Better investment choices','A governed technical-debt backlog links engineering work to product priorities and funding decisions.',C.amber]];
  impacts.forEach((a,i)=>{let y=1.85+i*1.08;box(s,0.8,y,11.6,0.83,C.white,C.line);s.addShape(pptx.ShapeType.rect,{x:0.8,y,w:0.12,h:0.83,fill:{color:a[2]},line:{color:a[2]}});txt(s,a[0],1.15,y+0.17,2.2,0.23,{fontSize:14,bold:true,color:C.navy});txt(s,a[1],3.55,y+0.14,8.25,0.38,{fontSize:11,color:C.ink});});
  box(s,0.8,6.25,11.6,0.42,'FFF8E8','F0D99A');txt(s,'Evidence boundary',1.05,6.36,1.4,0.18,{fontSize:10,bold:true,color:C.amber});txt(s,'The source files evidence capability creation; they do not yet quantify time, cost, SLA or quality improvements.',2.65,6.33,9.4,0.22,{fontSize:11,bold:true,color:C.navy});
}

// 8 what remains
{ const s=pptx.addSlide('MASTER'); addTitle(s,'Remaining work','The proof period should convert activity into measurable outcomes and durable BAU ownership','The action tracker contains a credible backlog, but priorities, owners and dates need tighter governance.');
  const phases=[['NOW','Stabilise','Complete priority artefacts; confirm owners and dates; publish a single baseline scorecard.',C.blue],['NEXT','Prove','Track aged blockers, incident diagnosis time, action closure, debt movement and stakeholder outcomes.',C.teal],['THEN','Embed','Confirm BAU ownership, artefact review cadence, funding route and operating model for 2027.',C.green]];
  phases.forEach((p,i)=>{let x=0.75+i*4.1;box(s,x,2.0,3.7,2.4,C.white,C.line);pill(s,p[0],x+0.25,2.25,0.7,p[3]);txt(s,p[1],x+0.25,2.75,3.0,0.3,{fontSize:18,bold:true,color:C.navy});txt(s,p[2],x+0.25,3.35,3.05,0.65,{fontSize:11,color:C.ink});if(i<2)s.addShape(pptx.ShapeType.chevron,{x:x+3.78,y:2.93,w:0.28,h:0.35,fill:{color:C.line},line:{color:C.line}});});
  box(s,0.75,5.15,11.8,1.0,'F0F4F8','D8E0EA');txt(s,'Critical gap to close',1.0,5.38,2.0,0.22,{fontSize:12,bold:true,color:C.navy});txt(s,'Convert the action tracker from a list of activities into a decision-quality portfolio: one accountable owner, one due date, one outcome measure and one escalation path per priority item.',3.15,5.32,8.9,0.4,{fontSize:12,color:C.ink});
}

// 9 decisions
{ const s=pptx.addSlide('MASTER'); addTitle(s,'Recommendation','Use November–January as an outcome-proof period, then confirm the 2027 model','This preserves momentum while giving leadership evidence before making a longer-term commitment.');
  box(s,0.75,1.85,7.25,3.9,C.navy,C.navy);txt(s,'Recommendation',1.1,2.2,2,0.25,{fontSize:11,bold:true,color:'7CE3D2'});txt(s,'Retain the SIP Manager role through January 2027 and use the period to prove measurable service outcomes before committing to the full-year model.',1.1,2.75,6.25,1.1,{fontSize:22,bold:true,color:C.white});txt(s,'Conditions for continuation',1.1,4.35,2.5,0.2,{fontSize:10,bold:true,color:'A9D5E5'});txt(s,'• Priority artefacts completed\n• Aged blockers reduced\n• Service outcomes evidenced\n• BAU ownership confirmed',1.1,4.7,5.8,0.7,{fontSize:12,color:C.white});
  box(s,8.35,1.85,4.2,3.9,C.white,C.line);txt(s,'Leadership decisions required',8.7,2.2,3.3,0.3,{fontSize:16,bold:true,color:C.navy});txt(s,'1. Endorse the proof period\n\n2. Nominate the 2027 funding owner\n\n3. Choose the future operating model\n\n4. Approve the outcome scorecard',8.7,2.85,3.25,1.85,{fontSize:12,color:C.ink});
  box(s,0.75,6.15,11.8,0.45,'FFF8E8','F0D99A');txt(s,'Caveat',1.0,6.27,0.7,0.18,{fontSize:10,bold:true,color:C.amber});txt(s,'Reconfirm commercial figures and contract dates before leadership circulation.',1.95,6.24,9.4,0.2,{fontSize:11,bold:true,color:C.navy});
}

// 10 critique
{ const s=pptx.addSlide('MASTER'); addTitle(s,'Critical assessment','Strong foundation; the next version should sharpen evidence, metrics and ownership','This assessment is based on the source PowerPoint and action-tracker workbook.');
  const cols=[['Strengths','Clear case for change\nCoherent capability pillars\nStrong governance narrative\nCredible proof-period recommendation',C.green],['Weaknesses','Few quantified outcomes\nInconsistent dates/status fields\nSeveral owners/TBD fields\nDuplicate or overlapping actions',C.amber],['Presentation issues','Original story is strong but dense\nSome terminology is unexplained\nImpact claims need evidence labels\nLong artefact lists need prioritisation',C.red],['Robustness & focus','Good strategic direction\nModerate evidence robustness\nNeeds baseline/target measures\nKeep C-level focus on decisions and outcomes',C.blue]];
  cols.forEach((c,i)=>{let x=0.75+(i%2)*6.0,y=1.8+Math.floor(i/2)*2.2;box(s,x,y,5.55,1.75,C.white,C.line);s.addShape(pptx.ShapeType.rect,{x,y,w:5.55,h:0.12,fill:{color:c[2]},line:{color:c[2]}});txt(s,c[0],x+0.25,y+0.3,4.8,0.25,{fontSize:15,bold:true,color:C.navy});txt(s,c[1],x+0.25,y+0.75,4.85,0.72,{fontSize:11,color:C.ink});});
  box(s,0.75,6.25,11.8,0.42,C.navy,C.navy);txt(s,'Overall judgement',1.0,6.36,1.35,0.18,{fontSize:10,bold:true,color:'7CE3D2'});txt(s,'Ready for a leadership discussion as a progress-and-decision deck; not yet a benefits-realisation report.',2.6,6.33,9.3,0.22,{fontSize:12,bold:true,color:C.white});
}

// 11 scorecard
{ const s=pptx.addSlide('MASTER'); addTitle(s,'Next measurement layer','A compact scorecard will turn a credible improvement narrative into a defensible business case','Measure outcomes, not activity volume. Baselines and targets must be agreed before the proof period.');
  const rows=[['Diagnosis','Time to identify root cause','Baseline required','Monthly'],['Flow','Aged blockers over 30 days','Baseline required','Fortnightly'],['Delivery','Action closure by due date','Baseline required','Weekly'],['Quality','Change failure / rework rate','Source indicates ~0% change failure; validate definition','Monthly'],['Knowledge','Priority artefacts current and owned','6 completed / 6 in progress / 7 not started','Monthly'],['Stakeholders','WE stakeholder confidence','Baseline survey required','Quarterly']];
  txt(s,'OUTCOME',0.9,1.7,1.6,0.2,{fontSize:9,bold:true,color:C.muted});txt(s,'MEASURE',3.0,1.7,3.1,0.2,{fontSize:9,bold:true,color:C.muted});txt(s,'EVIDENCE STATUS',7.0,1.7,3.3,0.2,{fontSize:9,bold:true,color:C.muted});txt(s,'CADENCE',11.0,1.7,1,0.2,{fontSize:9,bold:true,color:C.muted});
  rows.forEach((r,i)=>{let y=2.02+i*0.62;if(i%2===0)s.addShape(pptx.ShapeType.rect,{x:0.75,y:y-0.08,w:11.8,h:0.52,fill:{color:'F0F4F8'},line:{color:'F0F4F8'}});txt(s,r[0],0.9,y,1.8,0.22,{fontSize:10,bold:true,color:C.navy});txt(s,r[1],3.0,y,3.5,0.22,{fontSize:10,color:C.ink});txt(s,r[2],7.0,y,3.55,0.22,{fontSize:10,color:C.ink});txt(s,r[3],11.0,y,1.0,0.22,{fontSize:10,bold:true,color:C.teal});});
  box(s,0.75,6.15,11.8,0.45,'EAF7F5','B8E5DD');txt(s,'Decision rule',1.0,6.27,1.1,0.18,{fontSize:10,bold:true,color:C.teal});txt(s,'Continue the model where measured service outcomes improve or where leading indicators show credible progress towards them.',2.25,6.24,9.8,0.22,{fontSize:11,bold:true,color:C.navy});
}

pptx.writeFile({ fileName: '/tmp/CI-2026-Executive-Showcase.pptx' });
