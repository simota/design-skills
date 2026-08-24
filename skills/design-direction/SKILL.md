---
name: design-direction
description: "Deciding how a UI should look and feel before it is built: art direction, typography, colour intent, layout system, and a written design brief. Use when output lands on a generic default."
allowed-tools: Read, Grep, Glob, Bash, Write
---
<!-- design:contract -->

## Owns

What the product should look and feel like, and **why** — the adjectives it must
convey, the typeface roles, the colour strategy, the composition system, and
what it deliberately refuses to do. The deliverable is a written brief that a
later reader can argue with. Not values, not code.

Phases: `BRIEF → REFERENCE → DIRECTION → SPEC → HANDOFF`.

## Before starting

- **Adjectives before anything.** 3-5 words the direction must convey, plus two
  it must never read as. No direction work happens before they exist
- **Name the constraints that are actually fixed** — brand assets, existing
  surfaces, platform conventions, licensing budget, locale coverage. A direction
  that discovers one of these late is rewritten, not adjusted
- **Read the product's existing surfaces** if any exist. A direction that
  ignores what is already shipped is a redesign proposal wearing a brief's name
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
| Output is drifting toward the templated look | [anti-defaults](playbooks/anti-defaults.md) — every unmade decision falls back to a default, and the defaults all look alike |
| Choosing typeface roles, pairings, or scale intent | [typography](playbooks/typography.md) |
| Building a palette or assigning colour roles | [color-strategy](playbooks/color-strategy.md) — colour goes to roles, never to favourite hues |
| Turning references into something usable | [reference-analysis](playbooks/reference-analysis.md) — extract the strategy, never the identity |
| Writing or completing the deliverable | [direction-brief](reference/direction-brief.md) |
| References conflict | Do not average them. Averaging is how directions become generic — scope each to a surface, or make them two of the three considered |
| No references were supplied | Derive them from the product category, and record in the brief that they were inferred |
| Greenfield, no brand to inherit | The normal case, not a blocker. Derive adjectives from audience and category; record the absent identity as an assumption |
| A choice has no reason attached | It is a default in disguise. Either find the reason or make a different choice |
| A claim here would be expensive to get wrong | [refute](refute.py) — put it to the engines that did not make it, asked to break it rather than to agree. Unrefuted is n engines finding nothing, never proof |
| A value in the brief has no ground | Say so as `ARBITRARY` and move on. **This set's grounds mostly originate here** — a downstream deliverable full of `ARBITRARY` is this skill's output being thin, not that skill's failure |
<!-- deliver:values -->
- Ties break by `_design/VALUES.md`, read top to bottom: honesty over speed ·
  mechanism over intent · subtraction over addition · the decision over the
  artifact · the existing system over the better system · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — when the ceremony costs more than the decision, say
  so rather than performing it
<!-- /deliver:values -->

## Always / Never

- Always: present **three genuinely distinct directions**, each with a name, a
  one-line thesis, and what it trades away. Distinct means different strategies,
  not the same layout in three hues
- Always: specify all six layers — voice, typography, colour, composition,
  surface, restraint. **Missing layers are where generic output creeps in**
- Always: check headline, body, and muted pairs against AA *before* proposing
  them. Contrast is a direction decision, not a fix-up
- Always: say what the direction is **not** — the closest look it avoids
- Always: get permission first before assuming a parent brand exists, committing
  to licensed typefaces, or replacing a design system already in use
- Never: ship "modern, clean, minimal" as the direction. Those words describe nothing
- Never: recreate an identifiable third-party identity. Abstract the principle
  and say what you did not copy
- Never: default to the templated look — one sans everywhere, a purple-blue
  gradient, uniform cards on white — unless the brief argues for it
- Never: decide token names or values here

## Verify with

Contrast pairs are computed from the two values, not judged (evidence:
`measured`). Everything else — whether the direction reads as its adjectives,
whether three options are genuinely distinct — is `inspected`, and the brief
says so rather than implying more.

- **A direction is falsifiable or it is decoration.** State what would show it
  wrong: which adjective it would fail to convey, on which surface
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

The brief exists in writing, all six layers carry a reason, every text pair has
a computed ratio, the restraint list is non-empty, and what the direction
refuses is as explicit as what it chooses.
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
