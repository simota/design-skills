---
name: design-motion
description: "Designing motion and micro-interaction: duration and easing, transition choreography, state-change feedback, loading, gesture response, and reduced motion. Use when a UI feels static or janky."
allowed-tools: Read, Grep, Glob, Bash, Write
---
<!-- design:contract -->

## Owns

How change over time reads — what moves, for how long, on what curve, and what
happens when the user interrupts it. It decides the values; naming and storing
them is someone else's.

Phases: `PURPOSE → CHOREOGRAPHY → VALUES → REDUCED → HANDOFF`.

## Before starting

- **Name the job first**: orientation, feedback, continuity, status, or an
  expressive purpose the brief actually authorises. Remove motion with no purpose
- **Find out what is already moving.** A new curve added beside three existing
  ones makes the interface feel less coherent, not more
- **Establish whether motion carries personality here.** If the direction has
  not been set, that is a question for a person, not a default
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
| Deciding whether an animation earns its place | [purpose](playbooks/purpose.md) |
| Specifying a concrete transition | [patterns](reference/patterns.md) — trigger, properties, values, interrupt behaviour, reduced variant |
| Choosing or naming duration and easing values | [motion-tokens](reference/motion-tokens.md) |
| Specifying reduced motion | [reduced-motion](reference/reduced-motion.md) — static or instant may be the designed variant; preserve the state and information |
| Choosing timing or response | Start from the existing set or a cited platform specification; duration, curve or spring parameters follow the interaction, not a universal band |
| Waiting or feedback states are undecided | `design-ux` decides them; specify their transitions only after that decision, without inventing progress or hiding latency |
| A claim here would be expensive to get wrong | [refute](refute.py) — put it to the engines that did not make it, asked to break it rather than to agree. Unrefuted is n engines finding nothing, never proof |
| Choosing concrete motion values | Cite the actual source. A scale needs grounded inputs; copied examples or recalled curves are `ARBITRARY`. Specify the chosen values anyway; do not leave them to implementation |
<!-- deliver:values -->
- Ties break by `_design/VALUES.md`, read top to bottom: honesty over speed ·
  mechanism over intent · subtraction over addition · the decision over the
  artifact · the existing system over the better system · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — when the ceremony costs more than the decision, say
  so rather than performing it
<!-- /deliver:values -->

## Always / Never

- Always: state the job of an animation before specifying any value
- Always: specify reduced behaviour alongside full motion; static feedback may suffice
- Always: say what happens when the animation is **interrupted**. A user action
  during an animation takes precedence
- Always: preserve the navigation or gesture's spatial model; a fixed-edge sheet
  and a forward/back route transition need not have the same exit rule
- Always: get permission before overriding a platform gesture or an agreed
  motion identity; physics-based motion alone is not an approval gate
- Prefer `transform` and `opacity`; other properties need a reason and a cost
  check on a running artifact. A design-only spec states that check is still pending
- Never: block input while an animation plays
- Never: delay access to requested reading content for an entrance animation
- Treat parallax, large-scale zoom and spinning as risks to assess, not a
  conformance verdict; prefer static decoration and route adjudication to `design-a11y`
- Never: comment a keyframe with what it already does. The comment here carries
  the reason the property is animated at all, or the budget it was measured against

## Verify with

Reading declared values from the spec is `measured` evidence of those declarations,
not their suitability or runtime performance. Judge the stated purpose as
`inspected`; measure runtime claims on a running artifact or mark them unverified.

- **Every transition specifies four things or it is incomplete**: trigger,
  properties, interrupt behaviour, reduced variant. A missing one is `UNSPECIFIED`
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

Every animation names its job and concrete timing/curve or spring parameters
with grounds, specifies interruption and reduced behaviour, and records the
reason and verification status for any non-compositor properties.
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
