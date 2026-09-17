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
| Checking a colour pair | [contrast](reference/contrast.md) — measure, record, repair. Never estimate |
| Specifying names, roles, and states | [semantics](reference/semantics.md) — prefer native; a custom widget is a last resort with a named pattern and a stated reason |
| Running conformance against the standard | [wcag22-checklist](reference/wcag22-checklist.md) — cite the criterion number and level in every finding |
| Specifying focus order, visibility, or key operation | [keyboard-focus](playbooks/keyboard-focus.md) — a design specification, not an implementation detail |
| The failure is in the words | [content](playbooks/content.md) — most content failures are copy decisions |
| A finding needs a redesign, not an attribute | Say so plainly. An ARIA patch over a structural problem is a second defect |
| A brand colour cannot reach the bar | A question for a person. Do not quietly lower the level or quietly change the brand |
| Something cannot be assessed before build | Name it as not assessable at design time. That is a finding, not a pass |
| A claim here would be expensive to get wrong | [refute](refute.py) — put it to the engines that did not make it, asked to break it rather than to agree. Unrefuted is n engines finding nothing, never proof |
| A fix names a value | Keep its actual ground, including `ARBITRARY`; record the applicable criterion and measured check separately. A contrast floor does not select a colour |
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

Every criterion in scope is passed, failed, or recorded as not assessable at
design time; every failure cites its number, its measured values, and a fix at
the right layer; and both themes were checked separately.
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
