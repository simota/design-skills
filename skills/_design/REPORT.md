<!-- design:contract -->
# REPORT — what a person reads

Binding on every `design-*` skill. The other axes decide what must be true;
this one decides what reaches the reader. A run that satisfies all of them and
returns forty lines has still failed: **a report that gets skimmed is a report
that did not happen**, and a skimmed design decision is one that gets re-made
at build time by whoever hits it first.

## Record and view are different objects

| Object | Holds | Read by |
|---|---|---|
| The handoff (`_design/HANDOFF.md`) | Every field of the brief, every decision and its grade, the whole `open` list | The next skill, and the person when they ask |
| The report | The answer, the line of evidence under it, what is unresolved | The person, now |

The report is a **view over** the handoff, never a second copy of it in prose.
Rendering the object field by field is how one decision arrives as a paragraph,
and it is the failure this file was added to stop.

## The moments a run speaks

Four, and no others. Each owes something different, and **what is right at one moment is
noise at the next.**

| Moment | What it owes | Ceiling |
|---|---|---|
| **Start** | What will be done and what is excluded, with the tier if it is not obvious | one line |
| **A question** | The one decision that is blocked, and the default taken if nobody answers | one question, one line |
| **Mid-run** | Nothing — unless the reader must act now: a divergence from what was agreed, a path found blocked, work that would grow the scope, a value that turns out to have no source and would land as `ARBITRARY` | one line each, or silence |
| **End** | The report below | the ceiling below |

**Progress is not information.** "opening the screens", "now checking
contrast", "found it" tell the reader nothing they can act on, and they cost
the same attention as the line that matters. A tool call is already visible;
narrating it a second time is the commonest way a run fills a screen while
saying nothing.

**A question is not a status update.** Ask when guessing wrong would be
expensive to undo, ask one thing, and say what happens if the answer never
comes.

## At the end — this order, every time

1. **The answer, one line.** The status and what was decided or produced. A
   reader who stops after this line has the result
2. **The evidence, one line.** The sweep (`_design/CONTRACT.md`), which already
   carries the counts: `swept, 0 markers; 18 decisions / 18 graded`
3. **What is unresolved** — one line per residual that needs a human decision.
   `BLOCKED` and `UNSPECIFIED` always. `DEFERRED` and `OUT-OF-SCOPE` are in the
   handoff and named here only if the reader would act on them today
4. **What is next** — one line, or nothing if the answer is nothing

A run with nothing unresolved reports lines 1 and 2 and stops.

## Ceiling

| Tier (`_design/SIZING.md`) | The whole report |
|---|---|
| `T0` | one line |
| `T1` | six lines |
| `T2` | ten lines, plus the deliverable itself |

**Over the ceiling means cutting content, not reformatting it.** A table, a
nested list, and a heading per item are the three ways a report grows while
appearing to have been tightened.

## The deliverable is not the report

A brief, a token set, a flow, a critique is an artifact with a location. The
report says where it is and what it says in one line; it does not reproduce it.
Pasting the artifact into the report is how the ceiling gets defeated honestly.

## Not bigger than it is

The requested scope is the deliverable. Neighbouring concerns, future
possibilities and general principles are not folded into the answer, and a
small ask does not come back as a survey. **Being thoughtful and diverging
are not the same thing** — thought goes deeper into the one thing asked,
never wider. Option lists are given when they were asked for, or when the
choice is the reader's to make.

**A real problem is the exception.** If the request would break something,
is unsafe, or rests on a false premise, say what is wrong, why, and the
options, at whatever length that takes. **Cut noise, never risk.**

## Never in a report

- A restatement of the request, or of what the run was about to do
- A closing summary of what was just said
- Values the artifact already lists, or a walk through every token that changed
- Narration of process: what was opened, what was tried first, which tool ran
- Adjectives standing in for measurements, and confidence about things nobody
  doubted

## Asked for more

Bounding the default is not withholding. Every field lives in the handoff, and
"why", "which screens", "what else did you find" are answered from it at
whatever length the question deserves. **The long form is available on request;
it is just not the default.**
