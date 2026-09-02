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

- **Name the job first.** Every animation answers one of: *where did that come
  from*, *did my action register*, *what changed*, *what is happening now*.
  Motion with no answer is removed, not tuned
- **Find out what is already moving.** A new curve added beside three existing
  ones makes the interface feel less coherent, not more
- **Establish whether motion carries personality here.** If the direction has
  not been set, that is a question for a person, not a default
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
| Deciding whether an animation earns its place | [purpose](playbooks/purpose.md) |
| Specifying a concrete transition | [patterns](reference/patterns.md) — trigger, properties, values, interrupt behaviour, reduced variant |
| Choosing or naming duration and easing values | [motion-tokens](reference/motion-tokens.md) |
| Specifying the reduced-motion variant | [reduced-motion](reference/reduced-motion.md) — a designed variant, not a switch that deletes transitions |
| The change is small and local | Fast — 100-150ms. Large and full-screen — 300-400ms. **One global duration for everything is why interfaces feel wrong** |
| Something enters, leaves, or moves between | Entering decelerates, leaving accelerates, moving does both. Linear is for continuous progress only |
| Motion is being used to cover latency | Remove the latency. Where it cannot be removed, design the wait as its own state |
| A response is under 100ms | It needs no indicator at all |
| A claim here would be expensive to get wrong | [refute](refute.py) — put it to the engines that did not make it, asked to break it rather than to agree. Unrefuted is n engines finding nothing, never proof |
| Choosing a duration or an easing curve | `measured` from what exists, or `derived` from the set's scale. A curve copied from memory is `ARBITRARY` — the platform's published value is `platform`, and it has a source |
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
- Always: specify the reduced-motion variant alongside the full one
- Always: say what happens when the animation is **interrupted**. A user action
  during an animation takes precedence
- Always: preserve spatial continuity — what enters from the right leaves to the right
- Always: get permission first when a single non-looping transition would exceed
  500ms, when a gesture would override a platform-standard one, or when the
  platform is physics-based rather than curve-based
- Never: animate anything but `transform` and `opacity` without a written reason
  and a measured budget
- Never: ship an animation with no `prefers-reduced-motion` variant
- Never: block input while an animation plays
- Never: animate on load for content the user came to read
- Never: use parallax, large-scale zoom, or spinning as decoration — these are
  vestibular triggers, not style choices
- Never: animate more than roughly three elements independently in one moment
- Never: comment a keyframe with what it already does. The comment here carries
  the reason the property is animated at all, or the budget it was measured against

## Verify with

Durations, easings, and the property list are values read off the spec
(evidence: `measured`). Whether the motion *reads* as its stated job is
`inspected`, and the spec says which claim is which.

- **Every transition specifies four things or it is incomplete**: trigger,
  properties, interrupt behaviour, reduced variant. A missing one is `UNSPECIFIED`
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

Every animation names its job, carries duration and easing from the named set,
specifies its interrupt and reduced-motion behaviour, and touches only
compositor properties or explains why not.
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
