# Manager-Bot Memory

## Reusable Discord Research Tasking Template

Vincent wants a comprehensive template for tasking research work to Discord agents, especially `researcher-bot` through `#research-lab` or routed via `#manager-hq`.

Use this structure when drafting or refining research tasks:

```markdown
**Research Task**
Owner: @researcher-bot
Priority: P1 / P2 / P3
Deadline: YYYY-MM-DD HH:MM UTC, or "no hard deadline"
Requester: Vincent
Report back in: #research-lab / #manager-hq / thread link

**Objective**
Find out: <one clear sentence describing the question to answer>
Decision this supports: <what Vincent will decide or do with the answer>

**Context**
Background:
- <short context the agent needs>
- <known constraints, prior assumptions, or current hypothesis>

Why this matters:
- <business/product/personal/technical reason>

**Scope**
Include:
- <topic/source/geography/company/timeframe to include>
- <specific angles to investigate>
- <specific entities, products, papers, laws, repos, people, or claims>

Exclude:
- <what not to spend time on>
- <sources or angles that are irrelevant>

Timeframe:
- Current as of: <today / specific date>
- Historical range if relevant: <e.g. 2022-2026>

Geography / jurisdiction:
- <global / US / UK / EU / specific market>

**Source Requirements**
Use primary sources first:
- Official docs, company filings, regulator pages, standards bodies, academic papers, public datasets, GitHub repos, changelogs, court/legal docs where relevant.

Use secondary sources only to add context:
- Reputable journalism, analyst notes, expert blogs, trade publications.

Avoid:
- SEO spam, unsourced summaries, content farms, low-quality affiliate pages, hallucinated citations.

Minimum source bar:
- At least <N> high-quality sources.
- Cite every non-obvious factual claim.
- Include links for all cited sources.
- Note publication/update dates when recency matters.

**Research Questions**
Answer these directly:
1. <Question 1>
2. <Question 2>
3. <Question 3>

Also look for:
- Contradictions between sources.
- Recent changes or pending changes.
- Important caveats.
- What is unknown or unverifiable.

**Output Format**
Return:
1. **Executive Summary** - 5-10 bullets, answer first.
2. **Key Findings** - grouped by theme, with citations.
3. **Evidence Table** - source, date, claim supported, reliability note.
4. **Open Questions** - what remains uncertain and why.
5. **Recommendation / Implication** - what Vincent should do next, if applicable.
6. **Appendix** - raw links, search queries used, useful excerpts if short and compliant.

**Quality Bar**
- Separate facts, estimates, and opinions.
- Do not overstate certainty.
- If sources disagree, explain the disagreement.
- Prefer exact dates, numbers, names, and version identifiers.
- If the answer depends on current information, verify it during the task.
- If enough reliable evidence cannot be found, say so clearly and summarize what was checked.

**Stopping Conditions**
Stop when:
- The main questions are answered with sufficient evidence, or
- The deadline is reached, or
- A blocker requires access, credentials, payment, or clarification.

If blocked:
- Report the blocker.
- List what was tried.
- Suggest the smallest next action needed from Vincent.
```

Short version:

```markdown
@researcher-bot please research: <question>

Goal: <decision this supports>
Deadline: <time/date or no hard deadline>
Scope: <include/exclude/timeframe/geography>
Sources: primary sources first; cite every important claim; avoid SEO/content farms.
Deliverable: executive summary, key findings with citations, source reliability notes, open questions, and recommended next action.
Report back in this thread.
```

Manager-bot routing wrapper:

```markdown
**Route Research Task**
Target owner: researcher-bot
Priority: P1 / P2 / P3
Goal: <what needs to be learned>
Why: <decision or action this supports>
Deadline: <date/time>
Report destination: <channel/thread>
Constraints: <source quality, geography, timeframe, exclusions>
Deliverable: <summary / memo / ranked options / evidence pack / recommendation>
Blockers to flag: <credentials, paywalls, missing context, ambiguous scope>
```

Good research prompts include the decision supported, exact question, timeframe, geography, reliable source criteria, exclusions, desired output format, deadline, and blocker handling.
