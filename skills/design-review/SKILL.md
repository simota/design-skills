---
name: design-review
description: "Judging a rendered UI as a whole: first impression, visual hierarchy, composition and aesthetic verdict. Use to ask does this look good or whether it holds together. Report-only."
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
- **Record the initial reading before analysis**, never reconstruct it later.
  It is this reviewer's observation, not eye-tracking or evidence of user response
- **Name the viewport, theme and state you saw.** A verdict on one rendering is
  a verdict on one rendering
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

The impression and verdict are `inspected`: name the viewing conditions and
reasoning. Counts or positions actually read from the render are separate
`measured` observations; they never upgrade the aesthetic verdict or establish
an unobserved user's response. Guessed numbers are `asserted`.

- **A verdict carries all three phases or says which are missing.** Impression
  alone is opinion, principle alone is a rule, reference alone is envy
- **State the coverage**: which screens, viewports, themes and states were
  rendered, and what a static view cannot show — live data, motion, real content
- **A judgement that survives no phase is `asserted`** and does not ship as a
  finding. It ships as taste, labelled
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

Every verdict names the conditions it was formed under, carries its impression,
its principle and its reference or says which is absent, the strengths are
recorded, taste is labelled as taste, and what was not seen is listed as such.
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
