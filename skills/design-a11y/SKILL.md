---
name: design-a11y
description: "Designing for accessibility: WCAG conformance at the design layer, contrast, focus visibility, keyboard operability, target size, semantics, and inclusive content. Use to fix an issue at its root."
allowed-tools: Read, Grep, Glob, Bash, Write
---
<!-- design:contract -->

## Owns

Whether the design is operable by everyone, decided before code exists —
contrast, focus, keyboard operation, target size, the accessible name of every
control, and the content that carries meaning. It adjudicates conformance; it
does not write the markup that carries it.

Phases: `SCOPE → MEASURE → SPECIFY → REPORT`.

## Before starting

- **Establish the conformance level and say it.** Public-sector, regulated, and
  enterprise-procured products often carry a level above the default, and
  discovering that after the design is decided is a redesign
- **Get the real values, not a screenshot.** A ratio estimated from an image is
  `asserted`, whatever it looks like
- **Check both themes exist before scoping.** Each theme is verified
  independently; a pass in one says nothing about the other
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
| Checking a colour pair | [contrast](reference/contrast.md) — measure, record, repair. Never estimate |
| Specifying names, roles, and states | [semantics](reference/semantics.md) — prefer native; a custom widget is a last resort with a named pattern and a stated reason |
| Running conformance against the standard | [wcag22-checklist](reference/wcag22-checklist.md) — cite the criterion number and level in every finding |
| Specifying focus order, visibility, or key operation | [keyboard-focus](playbooks/keyboard-focus.md) — a design specification, not an implementation detail |
| The failure is in the words | [content](playbooks/content.md) — most content failures are copy decisions |
| A finding needs a redesign, not an attribute | Say so plainly. An ARIA patch over a structural problem is a second defect |
| A brand colour cannot reach the bar | A question for a person. Do not quietly lower the level or quietly change the brand |
| Something cannot be assessed before build | Name it as not assessable at design time. That is a finding, not a pass |
| A claim here would be expensive to get wrong | [refute](refute.py) — put it to the engines that did not make it, asked to break it rather than to agree. Unrefuted is n engines finding nothing, never proof |
| A fix names a value | It is almost always `threshold` — cite the criterion and its number. An accessibility fix offered as `ARBITRARY` has not been checked against anything |
<!-- deliver:values -->
- Ties break by `_design/VALUES.md`, read top to bottom: honesty over speed ·
  mechanism over intent · subtraction over addition · the decision over the
  artifact · the existing system over the better system · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — when the ceremony costs more than the decision, say
  so rather than performing it
<!-- /deliver:values -->

## Always / Never

- Always: cite the exact success criterion and level for every finding
- Always: compute the ratio and record **both source values** beside it
- Always: give every non-decorative image, icon, and control its intended
  accessible name — the name is a design decision, not a build detail
- Always: specify focus order, focus destination for every state change, and a
  visible indicator that is never obscured by sticky chrome
- Always: check target size and spacing for every interactive element, and
  verify light and dark independently
- Always: get permission first when the required level is unstated on a
  regulated product, when a fixed brand colour cannot reach the bar, or when a
  custom widget has no standard equivalent
- Never: claim conformance without measuring
- Never: use `aria-*` to paper over what native semantics would solve
- Never: remove a focus outline without an equally visible replacement
- Never: convey state, error, or category through colour alone
- Never: use placeholder text as a field's only label

## Verify with

Every contrast, target size, and spacing claim is computed from the two values
(evidence: `measured`). A criterion judged by reading the design is `inspected`
and says why it could not be measured.

- **Not assessable at design time is a third outcome**, distinct from pass and
  fail. Recording it as a pass is how conformance claims become false
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

Every criterion in scope is passed, failed, or recorded as not assessable at
design time; every failure cites its number, its measured values, and a fix at
the right layer; and both themes were checked separately.
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
