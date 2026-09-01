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
| A primitive has no ground but the scale | `derived` — name the base and the step. A primitive that is neither derived nor measured is `ARBITRARY`, and a scale of arbitrary values is a list |
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

The grammar is stated, every scale shows its rule, every semantic pair carries a
ratio in every theme, the export is in the project's format, and the migration
names each value it retires.
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
