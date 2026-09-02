<!-- design:contract -->
# CONTRACT — what counts as done

Binding on every `design-*` skill. A skill that reports completion without
satisfying this has reported a wish.

## Evidence grades

Design output cannot be run, so the grade is about **where the number came
from**, not whether a program executed.

| Grade | Means | Supports `DONE`? |
|---|---|---|
| `measured` | A value was read off the artifact — a contrast ratio computed, distinct values counted in the codebase, a state list checked against the running UI, a token resolved through its theme | Yes |
| `inspected` | The artifact was read and reasoned over, but nothing was measured | Only where nothing can be measured, and the entry says why |
| `asserted` | The claim stands alone | Never |

**`inspected` without a stated reason is `asserted` wearing a better name.**
"It reads as balanced", "the hierarchy is clear", and "that should pass" are not
reasons — they are the absence of one.

**Estimating a measurable value is `asserted`, not `measured`.** Contrast,
target size, type scale ratios, and token coverage are all countable. A design
judgement resting on a guessed number is the most expensive kind, because it
looks like a fact all the way to build.

## The unit of evidence is the decision

Not the document. A brief, a token table, or a spec is one file and twenty
decisions, and a file-level grade hides the nineteen that were never made.

Every decision the deliverable promised either carries a grade or appears in
the residuals as `UNSPECIFIED`. **A decision in neither is what gets invented
at build time**, by whoever hits it first, without knowing it was a decision.

## Status

| Status | Condition |
|---|---|
| `DONE` | Every promised decision made, every measurable claim measured, zero `UNSPECIFIED` |
| `PARTIAL` | Everything else that produced work — a single `UNSPECIFIED` lands here |
| `BLOCKED` | Could not proceed. Say what was tried and what stopped it |

Falling short is reported as falling short. A brief that quietly drops a
decision reads identical to one that made it.

## Residuals

Anything left behind is classified and recorded in the handoff's `open` list
with the place a reader would next look for it.

| Class | Means |
|---|---|
| `BLOCKED` | Wanted, attempted, prevented |
| `OUT-OF-SCOPE` | Found during the work, outside what was agreed. Named, not decided |
| `DEFERRED` | In scope, deliberately postponed, with the condition to resume named |
| `UNSPECIFIED` | Promised, and not decided |

**Who writes the marker depends on the tool grant.** A skill holding `Write`
puts a `#TODO(agent): <class> — <action>` line in the document it produced.
`design-critique` holds no write grant: it records the entry in `open` alone
and names where the marker belongs. **A report-only skill never edits to
satisfy this rule** — that would break the guarantee that makes it trustworthy.

The report closes and is gone. The marker stays. **A problem found outside the
scope is named, not fixed** — absorbing it is how a colour-role decision becomes
a redesign nobody agreed to.

## The completion sweep — never omitted

Before reporting, run both halves and state both results:

1. **Markers introduced by this run** — every one appears in `open` with a
   matching class
2. **Coverage** — the decisions the deliverable promised, against the decisions
   that carry a grade

Report it as: `swept, 2 markers / 2 in open; 18 decisions / 18 graded`.
**While either pair fails to match, the status is not `DONE`.**

## Comments — the value says what, a comment says why

A comment restating the declaration under it is a defect in the declaration,
not a sentence missing from it: `/* blue */` over `--color-blue-500`, `/* fades
in */` over an opacity keyframe. **The test is mechanical: cover the comment and
read the declaration.** Nothing lost — delete the comment. Something lost — put
it in the name, until the comment has become the name, and delete it anyway.

What survives is what a value cannot carry, and this set already names most of
it: **the computed contrast ratio beside a semantic pair, the deprecation
path of a replaced token, the written reason for animating anything but
`transform` and `opacity`**, and the outside constraint behind a number that
looks arbitrary. Those are the record rather than commentary, and **deleting
them is the opposite failure and costs more**. A `#TODO(agent):` marker and a
licence header stay.

**Nothing checks this automatically** — the sweep counts decisions, and the
unit of evidence here is the decision, not the file. It is a reading pass over
the files this run wrote, made before the sweep is reported.

## Boundary cases

- **A contrast pair not computed** is `asserted`, whatever the palette looks like
- **A token that resolves in the default theme** evidences that theme only. Each
  theme is its own measurement
- **A state named but not specified** is `UNSPECIFIED`, not covered. "Error
  state: handled" specifies nothing
- **Deferring to the implementer** is `UNSPECIFIED` unless the handoff names who
  decides and on what basis
- **A reference screenshot** evidences that something exists somewhere. It is
  never evidence that it fits this product
