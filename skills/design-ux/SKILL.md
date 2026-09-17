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

Every screen's state matrix is complete, every state has copy and a next action,
one primary action is named per screen, every exit path exists, and every state
left undesigned appears in the residuals by name.
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
