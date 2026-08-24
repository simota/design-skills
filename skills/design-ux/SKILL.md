---
name: design-ux
description: "Designing how an interface behaves: information architecture, task flows, screen states, forms, navigation, destructive actions, and cognitive load. Use when structure or interaction is undecided."
allowed-tools: Read, Grep, Glob, Bash, Write
---
<!-- design:contract -->

## Owns

How the interface behaves — the path a user takes, the states a screen can
occupy, what each control does, and what happens when it fails. It decides
structure and interaction, never how any of it looks.

Phases: `FLOW → STATES → SPEC → HANDOFF`.

## Before starting

- **Name the job the user came to do**, in their words. A structure decided
  without it optimises for the org chart
- **Draw the path before designing any screen** — entry, steps, branches, exits,
  dead ends. Screens designed before the flow are screens that do not connect
- **Find the navigation model already in use.** Changing one users have learned
  is a product decision, not a design improvement
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
| Enumerating what a screen can be | [state-matrix](playbooks/state-matrix.md) — **unspecified states get invented at build time, badly** |
| Designing the path through a task | [flows](playbooks/flows.md) |
| Structuring navigation, grouping, or labels | [ia-patterns](playbooks/ia-patterns.md) — styling cannot rescue bad structure |
| Anything with fields in it | [forms](playbooks/forms.md) — where UX failures cost most, because the user already invested effort |
| A screen feels heavy | [cognitive-load](playbooks/cognitive-load.md) — the fix is usually structural, not visual |
| Writing the deliverable | [spec-template](reference/spec-template.md) |
| Two actions compete to be primary | The screen has two jobs. It is probably two screens |
| An action is irreversible | Prefer undo. Where confirmation is genuinely required, state the consequence in specific terms and never focus the destructive button by default |
| The operation is slow | Specify 0-100ms, 100ms-1s, 1-10s, and >10s separately. Latency is a design input, not an implementation detail |
| A claim here would be expensive to get wrong | [refute](refute.py) — put it to the engines that did not make it, asked to break it rather than to agree. Unrefuted is n engines finding nothing, never proof |
| A number lands in a spec — a timeout, a page size, a character limit | Ground it in what was measured or what the brief fixes. `ARBITRARY` where nothing does, so the next person knows it is safe to move |
<!-- deliver:values -->
- Ties break by `_design/VALUES.md`, read top to bottom: honesty over speed ·
  mechanism over intent · subtraction over addition · the decision over the
  artifact · the existing system over the better system · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — when the ceremony costs more than the decision, say
  so rather than performing it
<!-- /deliver:values -->

## Always / Never

- Always: enumerate the **full state matrix** for every screen — empty, loading,
  partial, error, permission-denied, offline, success. Missing states are the
  single most common cause of shipped UX failure
- Always: name exactly one primary action per screen and demote everything else
- Always: specify validation timing per field and the error copy itself. Every
  error says what happened, why, and the single next action
- Always: specify the focus destination for every state change in a flow with
  steps or overlays, and how the user gets *out* — cancel, back, abandon
- Always: get permission first when the flow touches money, deletion, or legal
  consent with the guardrail unstated; when research contradicts the structure;
  or when a "simplification" would remove functionality someone depends on
- Never: constrain later what you can prevent now. Make the invalid case
  unenterable before writing its error message
- Never: ship "Something went wrong" as a state, or an infinite spinner with no
  timeout and no failure path
- Never: use a modal for a task that needs another modal, block the whole UI for
  a partial operation, or rely on colour alone to carry state
- Never: use placeholder text as a field's only label

## Verify with

A state matrix is checked against the running interface where one exists
(evidence: `measured` — the states were counted, not imagined). Where nothing is
built yet, the spec is `inspected` and says so.

- **A state named is not a state specified.** "Error state: handled" specifies
  nothing and counts as `UNSPECIFIED`
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

Every screen's state matrix is complete, every state has copy and a next action,
one primary action is named per screen, every exit path exists, and every state
left undesigned appears in the residuals by name.
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
