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
Rendering the object field by field is how one decision arrives as a paragraph.

## The moments a run speaks

Four. Each owes something different, and **what is right at one moment is
noise at the next.**

| Moment | What it owes | Shape |
|---|---|---|
| **Start** | What will be done and what is excluded, with the tier if it is not obvious | a sentence |
| **A question** | The one decision that is blocked, and the default taken if nobody answers | one question |
| **Mid-run** | What the reader can act on now: a divergence from what was agreed, a path found blocked, work that would grow the scope, a value that turns out to have no source and would land as `ARBITRARY` | one line each |
| **End** | The report below | the length below |

**The harness already shows which tool ran.** A mid-run line earns its place by
carrying something the tool call did not: what was found, what it changes, what
the reader now has to decide.

**A question is not a status update.** Ask when guessing wrong would be
expensive to undo, ask one thing, and say what happens if the answer never
comes.

## At the end — this order, every time

1. **The answer first.** The status and what was decided or produced. A
   reader who stops after this line has the result
2. **The evidence.** The sweep (`_design/CONTRACT.md`), which already
   carries the counts: `swept, 0 markers; 18 decisions / 18 graded`
3. **What is unresolved** — each residual that needs a human decision.
   `BLOCKED` and `UNSPECIFIED` always. `DEFERRED` and `OUT-OF-SCOPE` are in the
   handoff and named here only if the reader would act on them today
4. **What is next** — or nothing if the answer is nothing

A run with nothing unresolved reports items 1 and 2 and stops.

## Length

The report is as short as the four items above allow. `T0` (`_design/SIZING.md`)
is the answer alone; `T1` and `T2` add the sweep, the residuals and what is
next, and `T2` links the deliverable. Nothing else belongs in it.

**Too long means cutting content, not restructuring it.** A table earns its
place when the reader must compare rows, a heading when they must navigate;
neither is a way of making the same content look shorter.

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
- Which tool ran, in what order — the record has it, and the harness showed it
- Adjectives standing in for measurements, and confidence about things nobody
  doubted

## Asked for more

Bounding the default is not withholding. Every field lives in the handoff, and
"why", "which screens", "what else did you find" are answered from it at
whatever length the question deserves. **The long form is available on request;
it is just not the default.**
