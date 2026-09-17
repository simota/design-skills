---
name: design-critique
description: "Itemising UI issues: defects, inconsistencies and judgement calls; list differences with evidence, severity, fixes and owners. Use for a UI audit of craft or drift. Report-only."
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
  spec, platform convention, or stated heuristics. Without an adopted standard,
  name the fallback lens and report reasoned judgements, not invented requirements
- **Get the artifact, not a description of it.** Reviewing a summary reviews the
  summary. Where only a screenshot exists, say so: values become estimates
- **Scope it before looking** — which screens, states, breakpoints, themes. What
  is outside that list is reported as not reviewed, never as fine
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
| Running the evaluation | [heuristics](playbooks/heuristics.md) — run each lens deliberately; findings from different lenses do not substitute for each other |
| Inspecting alignment, spacing, type detail, or responsive behaviour | [craft-audit](playbooks/craft-audit.md) — distinguish measured observations, system departures and judgement |
| Ranking what you found | [severity](playbooks/severity.md) — by user impact, never by how obvious the finding was |
| Writing the report | [report-template](reference/report-template.md) — tone rules matter as much as content; a report that reads as an attack does not get acted on |
| Only one screen of a flow is available | Review it and list the rest as not reviewed. Never infer a flow defect from one screen |
| The intent is unclear | Ask rather than assert: "if the intent was X, then Y is a problem — was it?" |
| The finding is about contrast or keyboard operation | Flag it and hand it to `design-a11y`. This skill flags; that one adjudicates |
| The whole misreads, and the itemised findings do not explain why | That is a verdict on the rendered result, and `design-review` owns it. Itemising parts does not add up to it |
| The design departs from convention deliberately | It may have a reason you cannot see. Ask before ranking it a defect |
| A claim here would be expensive to get wrong | [refute](refute.py) — put it to the engines that did not make it, asked to break it rather than to agree. Unrefuted is n engines finding nothing, never proof |
| A finding proposes a value | Ground the replacement separately from the finding. An `ARBITRARY` proposed value neither proves nor invalidates the evidenced problem |
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
- Never: present taste as defect, or a fallback heuristic as a standard the team adopted
- Never: give feedback with no evidence — "feels cluttered", "needs polish"
- Never: list forty minor findings and bury the two that matter

## Verify with

Measure countable claims from an available source and name its scope (`measured`).
Guessed screenshot values are `asserted`, not `inspected`; unavailable values are
not assessable. A reasoned qualitative concern may be `inspected` without numbers.
A measured difference is a defect only with evidence of failure, not just difference.

- **A finding that survives no check is `asserted` and does not go in the report**
- **State the coverage**: what was read, which lenses ran, and what a review of
  this artifact cannot see — production data, real content, the deployed client
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

The standard is named, every finding carries evidence, a severity, a class, a
fix and an owner, the strengths are recorded, and everything not reviewed is
listed as not reviewed.
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
