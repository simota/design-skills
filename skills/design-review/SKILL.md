---
name: design-review
description: "Judging how a rendered interface looks: first impression, visual hierarchy, and an aesthetic verdict against opened references. Renders it, or reads a screenshot. Does this look good."
allowed-tools: Read, Grep, Glob, Bash
---
<!-- design:contract -->

## Owns

Whether the built thing looks good, judged by looking at it — the artifact put
in front of its own eyes, what the eye did recorded, restated as a named
principle, and held against a reference that was actually opened.
**Report-only.** It delivers a verdict, never the redesign that would earn one.

Phases: `SEE → IMPRESSION → PRINCIPLE → REFERENCE → VERDICT`.

## Before starting

- **See the real thing.** Render it and look, or read the image you were handed
  ([seeing](playbooks/seeing.md)). A judgement from source alone is a guess
  about pixels nobody produced, and it is `asserted` however careful
- **Record the impression before reasoning about it.** The first seconds are the
  only unrepeatable evidence here, and they are gone once analysis starts
- **Name the viewport, theme and state you saw.** A verdict on one rendering is
  a verdict on one rendering
<!-- deliver:sizing -->
- **Size it before anything else**, first match wins. `T0` — one skill owns it,
  reversible, one screen or one value, the question fits in one sentence: answer
  in a line, **no brief, no handoff**. `T1` — a `T0` condition fails: settle the
  brief first. `T2` — two or more skills own parts of it: route it. `T0` drops
  the paperwork, never the evidence. Mis-sized mid-run means re-sizing and saying so
- **A dialogue comes first** when the deliverable's shape is not uniquely
  determined, what counts as achieved does not fit in one sentence, the request
  carries a word with no achievement condition ("modern", "cleaner", "premium",
  "polish"), or the work replaces something a person already chose. Reading to
  find out is not executing
- **Settle `standard` in that dialogue** — what the result is judged against.
  Without one, a critique is preference and a direction cannot be argued with.
  `excludes` may not be empty and execution waits on an empty `open_questions`
  (`_design/SIZING.md`)
<!-- /deliver:sizing -->
<!-- deliver:ground -->
- **Every literal value names its ground.** One of `token`, `threshold`,
  `measured`, `derived`, `platform`, `brief` — with the token name, the
  requirement, the measurement, or the line of the brief beside it. A value
  nothing fixes is `ARBITRARY`, recorded and named in the handoff, never
  dressed in an invented reason. **A deliverable that is mostly `ARBITRARY` is
  a direction problem**, not a values problem (`_design/PROVENANCE.md`)
<!-- /deliver:ground -->

## Decide first

- **Here the tie goes to what the eye did**, not to what a rule says it should
  have. A principle contradicting the observation is the wrong principle

| Situation | How to proceed |
|---|---|
| Getting the artifact in front of you | [seeing](playbooks/seeing.md) — render, capture, and say which conditions you saw |
| Turning an impression into something arguable | [principles](playbooks/principles.md) — the named visual principle it restates as |
| Holding it against work that already succeeds | [comparison](reference/comparison.md) — a reference proves a thing is possible, never that it fits here |
| Forming and phrasing the overall judgement | [verdict](playbooks/verdict.md) |
| A finding spans places, an order, a disagreement, or a region | [visualise](playbooks/visualise.md) — a reader who has to reassemble it will skim it. ASCII by default, and the drawing carries the finding's rung, never a better one |
| The impression restates as no principle and matches no reference | It is taste. Say so, mark it `ARBITRARY`, and never rank it as a defect |
| The problem is a value, a count, an alignment, contrast, or focus order | Measurable, so not this skill's: values and counts go to `design-critique`, conformance to `design-a11y`. This skill judges the whole, and looking wrong is a different claim from failing a criterion |
| The interface looks fine and the direction is still wrong | Say that plainly. Executing a poor brief well is a `design-direction` problem, and no amount of looking fixes it |
| Nothing renders and no image exists | Stop. Report `BLOCKED` with what was tried. A verdict on an interface nobody saw is the failure this skill exists to prevent |
| A claim here would be expensive to get wrong | [refute](refute.py) — put it to the engines that did not make it, asked to break it rather than to agree. Unrefuted is n engines finding nothing, never proof |
<!-- deliver:values -->
- Ties break by `_design/VALUES.md`, read top to bottom: honesty over speed ·
  mechanism over intent · subtraction over addition · the decision over the
  artifact · the existing system over the better system · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — when the ceremony costs more than the decision, say
  so rather than performing it
<!-- /deliver:values -->

## Always / Never

- Always: state what you saw — viewport, theme, state, and how it was rendered —
  before the first judgement
- Always: impression first, principle second. Reversed, it is a rule looking for
  evidence, and it finds it every time
- Always: say what is good, specifically. Unmarked strengths get destroyed next pass
- Always: separate **the verdict** (does this hold together) from **the finding**
  (this element is wrong). One ranks the whole; the other is a list
- Never: judge from source, a description, or a component name — rendering is the method
- Never: dress taste as defect. `ARBITRARY` is honest and cheaper than an
  invented rationale
- Never: edit, or produce the improved version. A reviewer that redesigns is no longer an observation
- Never: let a reference become the target. It is a comparison, not a requirement

## Verify with

An impression is evidence of what one viewing produced, and is `inspected` — it
names the conditions it was formed under or it is nothing. It is `measured` only
where it lands on something countable: a ratio, a size, a position, a count of
distinct values read off the render.

- **A verdict carries all three phases or says which are missing.** Impression
  alone is opinion, principle alone is a rule, reference alone is envy
- **State the coverage**: which screens, viewports, themes and states were
  rendered, and what a static view cannot show — live data, motion, real content
- **A judgement that survives no phase is `asserted`** and does not ship as a
  finding. It ships as taste, labelled
<!-- deliver:report -->
- **Grade every claim**: `measured` (a value read off the artifact) supports
  completion; `inspected` (read and reasoned over) only where nothing can be
  measured and the entry says why; `asserted` never does. **Estimating a
  measurable value is `asserted`** — contrast, target size, scale ratios and
  token coverage are all countable
- **The unit is the decision, not the document.** Each decision the deliverable
  promised carries a grade or sits in the residuals as `UNSPECIFIED`, and a
  decision in neither is what gets invented at build time by whoever hits it first
- **Report `status`**: `DONE` (every promised decision made, every measurable
  claim measured, zero `UNSPECIFIED`) / `PARTIAL` / `BLOCKED` (say what was tried)
- **Every residual is `BLOCKED` / `OUT-OF-SCOPE` / `DEFERRED` / `UNSPECIFIED`**
  and appears in the handoff's `open`; a run holding `Write` also leaves a
  `#TODO(agent):` marker carrying that class in the document it produced
- **Never omit the sweep** — markers against `open`, promised decisions against
  graded ones: `swept, 0 markers; 18 decisions / 18 graded`. While either pair
  disagrees the status is not `DONE` (`_design/CONTRACT.md`)
<!-- /deliver:report -->

## Done when

Every verdict names the conditions it was formed under, carries its impression,
its principle and its reference or says which is absent, the strengths are
recorded, taste is labelled as taste, and what was not seen is listed as such.
<!-- deliver:surface -->
- **Say only what the moment needs.** Start: one line naming what will be done and what
  is excluded. Mid-run: silence, unless the reader must act now — a divergence from what
  was agreed, a path found blocked, a value that would land with no source. Progress is not
  information, and a tool call is already visible. Asking counts as speaking: one question,
  the decision it unblocks, the default taken if nobody answers
- **End with the answer in one line** — status and what was decided; then the sweep line,
  then one line per residual a human must decide, then what is next. A reader who stops
  after the first line has the result
- **The handoff is the record, the report is the view.** The brief, the per-decision grades
  and the working log travel in the handoff and are shown when asked
- **Ceiling: `T0` one line · `T1` six · `T2` ten**, plus the deliverable itself — linked,
  never pasted. Over it means cutting content, not reformatting it: no restatement of the
  request, no closing summary, no narration of what was opened (`_design/REPORT.md`)
- **Not bigger than it is.** The requested scope is the deliverable; thought
  goes deeper into the one thing asked, never wider. **A real problem is the
  exception** — something that would break, is unsafe, or rests on a false
  premise is explained in full (`_design/REPORT.md`)
<!-- /deliver:surface -->
