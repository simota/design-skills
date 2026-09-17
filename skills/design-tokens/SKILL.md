---
name: design-tokens
description: "Specifying design tokens: colour, spacing, type and elevation scales, the semantic layer, theming and dark mode, naming grammar, and export. Use when hardcoded values must become a system."
allowed-tools: Read, Grep, Glob, Bash, Write
---
<!-- design:contract -->

## Owns

The named values a design is built from, and the grammar that names them —
primitive scales, the semantic layer over them, theming, and the export the
project actually consumes. It decides what a value is *called* and where it
lives, never what aesthetic the value expresses.

Phases: `AUDIT → GRAMMAR → PRIMITIVES → SEMANTICS → THEMES → EXPORT`.

## Before starting

- **Count first.** Before proposing a system for an existing codebase, count the
  distinct hardcoded values in use. The system either covers them or explicitly
  retires them; a system that covers 60% of what is there creates a third idiom
- **Find the grammar already in the repo.** If one exists, it wins over a better
  one. Two grammars cost every future reader more than one mediocre grammar
- **Get the direction, or say you are working without one.** Semantics derived
  from existing values are descriptive, not intentional — a real difference the
  handoff must state
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
| Deciding or repairing the naming grammar | [naming](playbooks/naming.md) — decided once, before any token exists; repairing it later costs a migration |
| Generating spacing, type, radius, elevation, or colour ramps | [scales](reference/scales.md) — every scale comes from a stated rule, written next to the values |
| Needing the semantic role catalogue or interchange format | [token-schema](reference/token-schema.md) |
| Specifying dark mode, high contrast, or multi-brand | [theming](reference/theming.md) — a theme remaps semantics; it never inverts primitives |
| Emitting CSS, Tailwind, Style Dictionary, Swift, or Kotlin | [export-targets](reference/export-targets.md) — emit what the project consumes, not all of them |
| Moving an existing codebase onto tokens, or retiring old ones | [migration](reference/migration.md) |
| Two competing grammars are already in the repo | Do not run both. Take the one with more sites, say so, and put the other on the deprecation path |
| The colour space for ramps is unstated | Generate in OKLCH and say so — even lightness spacing in sRGB is not even to the eye |
| No export target named | Emit CSS custom properties and DTCG JSON; both are consumable without further tooling |
| A claim here would be expensive to get wrong | [refute](refute.py) — put it to the engines that did not make it, asked to break it rather than to agree. Unrefuted is n engines finding nothing, never proof |
| A primitive comes from a scale | `derived` only with grounded base, factor and step policy; otherwise `ARBITRARY`, with the formula retained. Naming the primitive does not erase its origin |
<!-- deliver:values -->
- Ties break by `_design/VALUES.md`, read top to bottom: honesty over speed ·
  mechanism over intent · subtraction over addition · the decision over the
  artifact · the existing system over the better system · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — when the ceremony costs more than the decision, say
  so rather than performing it
<!-- /deliver:values -->

## Always / Never

- Always: three tiers — primitive → semantic → component. **Components consume
  semantics and never reach past them to primitives**
- Always: name semantics for the job, not the look. A name that has to change
  when the value changes was never semantic
- Always: record a computed contrast ratio next to every text-bearing semantic pair
- Always: give a replaced token a deprecation path, not a silent rename
- Always: get permission first when a token system with a different grammar
  already exists, when multi-brand theming is implied but unstated, or when
  migration would change a value users can see
- Never: name a semantic token after its hue (`--color-blue-primary`)
- Never: hold one value in two tiers and update only one — declare an alias instead
- Never: invert a light palette to produce dark mode
- Never: patch a missing token with an inline value or `!important` — add the token
- Never: ship a token whose value fails its own stated contrast requirement
- Never: comment a token with what its name already says (`/* blue */` over
  `--color-blue-500`). The comment a token earns is what the name cannot carry —
  the measured ratio, the deprecation path, the constraint behind a value

## Verify with

Every ratio is computed and every theme is resolved through its own mapping
(evidence: `measured`). **A token that resolves in the default theme evidences
that theme only** — each theme is its own measurement.

- **Coverage is counted, not claimed**: distinct hardcoded values found, values
  the system covers, values deliberately retired. The three must add up
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

The grammar is stated, every scale shows its rule, every semantic pair carries a
ratio in every theme, the export is in the project's format, and the migration
names each value it retires.
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
