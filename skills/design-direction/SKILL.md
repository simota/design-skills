---
name: design-direction
description: "Choosing a UI's look and feel: art direction, typography, colour intent, layout system and design brief. Use to set or change the intended aesthetic, including an existing product."
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
- **Size first.** `T0`: one skill, reversible, one bounded decision with a clear
  result — answer with grounds and evidence, **no brief, no handoff**. A screen
  with several promised decisions is not `T0`. `T1`: one skill, larger scope;
  settle the brief. `T2`: multiple owners or handoff stages; route once. Re-size as needed
- **Read before asking.** Dialogue is required for unresolved scope, achievement
  conditions or authority to change a prior choice, not for facts the request or
  artifacts already settle. Unresolved "premium" or "cleaner" still needs a basis
- **Bound the brief.** State `standard` or a fallback judgement basis, meaningful
  `axes` (one may suffice), and `excludes` when `delivers` does not already bound
  scope. `open_questions` holds scope/authority gaps; clear it before executing.
  Promised design decisions are made during the work, never silently left to build
- **Use the host glossary.** Ask about material ambiguity, record settled `terms`;
  read-only runs propose glossary changes, never write them (`_design/SIZING.md`)
<!-- /deliver:sizing -->
<!-- deliver:ground -->
- **Every literal value names its ground**: `token`, `threshold`, `measured`,
  `derived`, `platform`, or `brief`, with its actual source beside it. Nothing
  fixes it: `ARBITRARY`, even with a taste rationale. Record it in the handoff
  (inline at `T0`); its frequency alone never requires a direction redo
- **Origin is not conformance.** A limit constrains a choice; satisfying it does
  not ground the chosen value. Record the test separately. `derived` requires
  grounded inputs, including scale choices; naming a token or copying an example
  does not supply them (`_design/PROVENANCE.md`)
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
| A choice has no reason attached | State the intended effect and trade-off; do not invent a source that fixes its literal values |
| A claim here would be expensive to get wrong | [refute](refute.py) — put it to the engines that did not make it, asked to break it rather than to agree. Unrefuted is n engines finding nothing, never proof |
| A value in the brief has no ground | Record `ARBITRARY`. Settled intent can leave values unconstrained; their number alone is not evidence of a thin direction |
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
- **Grade each claim**: `measured` supports only what was actually measured;
  `inspected` is for non-measurable judgement, with its reason and limits;
  `asserted` never supports completion. **A guessed measurable value is `asserted`**, not
  `inspected`. A count, convention or preference alone does not establish a defect
- **The unit is the decision, not the document.** Each promised decision carries
  a grade or is `UNSPECIFIED`; no silent delegation of design choices to build
- **Report `status`**: `DONE` (every promised decision made, every measurable
  claim measured, zero `UNSPECIFIED`) / `PARTIAL` / `BLOCKED` (say what was tried)
- **Classify residuals** as `BLOCKED` / `OUT-OF-SCOPE` / `DEFERRED` / `UNSPECIFIED`
  in `open`; a run holding `Write` also places a `#TODO(agent):` marker in its output.
  At `T0`, name any residual inline without creating a handoff
- **Never omit coverage**: markers against `open`, promised decisions against
  graded ones. Report the sweep at `T1`/`T2`; at `T0` evidence its one decision
  inline. A mismatch forbids `DONE` (`_design/CONTRACT.md`)
<!-- /deliver:report -->

## Done when

The brief exists in writing, all six layers carry a reason, every text pair has
a computed ratio, the restraint list is non-empty, and what the direction
refuses is as explicit as what it chooses.
<!-- deliver:surface -->
- **Write to the reader when they can act on it.** Start: what will be done and what is
  excluded. Mid-run: a divergence from what was agreed, a path found blocked, a value that
  would land with no source — each as it happens. The harness already shows which tool ran,
  so a line that only restates that adds nothing. Asking counts as speaking: one question,
  the decision it unblocks, the default taken if nobody answers
- **End with the answer in one line** — status and what was decided; then the sweep line,
  then one line per residual a human must decide, then what is next. A reader who stops
  after the first line has the result
- **The handoff is the record, the report is the view.** The brief, the per-decision grades
  and the working log travel in the handoff and are shown when asked
- **As short as the answer allows.** `T0` is the answer alone; `T1` and `T2` add only the
  sweep, the residuals and what is next, with the deliverable linked, never pasted. Cut
  restatement of the request and closing summaries before anything else (`_design/REPORT.md`)
- **Not bigger than it is.** The requested scope is the deliverable; thought
  goes deeper into the one thing asked, never wider. **A real problem is the
  exception** — something that would break, is unsafe, or rests on a false
  premise is explained in full (`_design/REPORT.md`)
<!-- /deliver:surface -->
