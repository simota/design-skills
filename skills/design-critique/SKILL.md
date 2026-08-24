---
name: design-critique
description: "Reviewing an interface and reporting what to change: design review, UI audit, heuristic evaluation, craft and drift findings ranked by severity, with fixes. Report-only. Use when something feels off."
allowed-tools: Read, Grep, Glob, Bash
---
<!-- design:contract -->

## Owns

What is wrong with an interface that already exists, ranked by what it costs the
user, each finding evidenced and paired with a fix and an owner. **Report-only.**
It never produces the replacement.

Phases: `STANDARD → INVENTORY → EVALUATE → RANK → REPORT`.

## Before starting

- **Establish the standard and name it** — the brief, the token system, the
  spec, platform convention, or stated heuristics. **Critique without a standard
  is preference.** Where none exists, descend the ladder and say which rung you
  landed on rather than stalling
- **Get the artifact, not a description of it.** Reviewing a summary reviews the
  summary. Where only a screenshot exists, say so: values become estimates
- **Scope it before looking** — which screens, states, breakpoints, themes. What
  is outside that list is reported as not reviewed, never as fine
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

| Situation | How to proceed |
|---|---|
| Running the evaluation | [heuristics](playbooks/heuristics.md) — run each lens deliberately; findings from different lenses do not substitute for each other |
| Inspecting alignment, spacing, type detail, or responsive behaviour | [craft-audit](playbooks/craft-audit.md) — the measurable layer |
| Ranking what you found | [severity](playbooks/severity.md) — by user impact, never by how obvious the finding was |
| Writing the report | [report-template](reference/report-template.md) — tone rules matter as much as content; a report that reads as an attack does not get acted on |
| Only one screen of a flow is available | Review it and list the rest as not reviewed. Never infer a flow defect from one screen |
| The intent is unclear | Ask rather than assert: "if the intent was X, then Y is a problem — was it?" |
| The finding is about contrast or keyboard operation | Flag it and hand it to `design-a11y`. This skill flags; that one adjudicates |
| The whole misreads, and the itemised findings do not explain why | That is a verdict on the rendered result, and `design-review` owns it. Itemising parts does not add up to it |
| The design departs from convention deliberately | It may have a reason you cannot see. Ask before ranking it a defect |
| A claim here would be expensive to get wrong | [refute](refute.py) — put it to the engines that did not make it, asked to break it rather than to agree. Unrefuted is n engines finding nothing, never proof |
| A finding proposes a value | Ground it like any other. **A critique that says "use 24px" and cannot say why 24 has produced an opinion, not a finding** — `ARBITRARY` is the honest label when it is taste |
<!-- deliver:values -->
- Ties break by `_design/VALUES.md`, read top to bottom: honesty over speed ·
  mechanism over intent · subtraction over addition · the decision over the
  artifact · the existing system over the better system · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — when the ceremony costs more than the decision, say
  so rather than performing it
<!-- /deliver:values -->

## Always / Never

- Always: state the standard before the first finding
- Always: quote concrete evidence — values, positions, counts, the actual text —
  then the judgement. Never the judgement alone
- Always: mark each finding `defect` (measurably wrong), `inconsistency`
  (violates the system), or `judgement` (a defensible alternative view)
- Always: pair every finding with a specific, implementable fix and an owner
- Always: say what already works. Unmarked strengths get destroyed in the next
  revision — this is not politeness
- Never: edit anything. Report-only means report-only, and a review that quietly
  changed the design cannot be trusted as a review
- Never: present taste as defect, or critique against a standard the team never adopted
- Never: give feedback with no evidence — "feels cluttered", "needs polish"
- Never: list forty minor findings and bury the two that matter

## Verify with

A finding on the measurable layer carries the values it came from (evidence:
`measured`). From a screenshot alone, values are estimates — the finding is
marked "visual estimate, not measured" and is `inspected`, never dressed as fact.

- **A finding that survives no check is `asserted` and does not go in the report**
- **State the coverage**: what was read, which lenses ran, and what a review of
  this artifact cannot see — production data, real content, the deployed client
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

The standard is named, every finding carries evidence, a severity, a class, a
fix and an owner, the strengths are recorded, and everything not reviewed is
listed as not reviewed.
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
