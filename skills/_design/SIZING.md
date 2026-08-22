<!-- design:contract -->
# SIZING — how much ceremony the request is worth

Ceremony **above** what a request needs is what gets a harness worked around.
Ceremony **below** it is how a decision goes unmade. Both come from the same
move — choosing the tier for comfort — so the tier is read on first match.

## The three tiers

| Tier | All of these hold | What it costs |
|---|---|---|
| `T0` | One skill obviously owns it · reversible · one screen or one value · the question fits in one sentence | Answer in a line. **No brief, no handoff** |
| `T1` | One skill owns it, but a `T0` condition fails | Settle the brief, then run. Handoff on return |
| `T2` | Two or more skills own parts of it, or the work spans phases | Route it: settle the brief once, run the chain, one report covers every stage |

`T0` drops the paperwork. It never drops the evidence grades — a one-line answer
still says whether the number was measured or guessed.

**Finding mid-run that the tier was wrong means re-sizing and saying so.** A
`T0` contrast check that has turned into a palette revision is a `T1` that was
mis-sized.

## When a dialogue is required first

Design work fires this gate more often than most, because the deliverable's
shape is usually not determined by the request. Before executing, any of these
makes the dialogue mandatory:

- The shape of the deliverable is not uniquely determined
- What counts as achieved does not fit in one sentence
- The request carries a word with no achievement condition — "make it modern",
  "cleaner", "more premium", "polish", "improve the hierarchy"
- The work would replace something a person already chose
- Doing it wrong would be expensive to undo — a token grammar, a naming scheme,
  a navigation model, anything already shipped to users

**Reading to find out is not executing.** The codebase, the existing screens,
and the current tokens answer more questions than the person can. And never
open a dialogue over one reversible value.

## The brief the dialogue produces

Conclusions recorded as data, not as an understanding. Execution reads only
this.

```yaml
goal: "<one sentence describing the state once achieved>"
delivers: "<a single artifact>"   # split the work if this goes plural
axes: [...]                       # what counts as achieved. Never one axis
excludes: [...]                   # what will not be decided. May not be empty
baseline: "<the observed starting state the result is measured against>"
standard: "<what the result is judged against>"   # brief, tokens, platform, heuristics
open_questions: []                # execution does not begin until empty
```

- **`standard` is design's baseline for judgement.** Critique without a stated
  standard is preference, and a direction without one cannot be argued with.
  Where none exists, say which rung you fell back to
- **`axes` may not collapse to one.** "Looks better" is a single oracle, and
  there is always a reading of it that can be declared satisfied
- **`excludes` may not be empty.** Writing down what will not be decided is the
  only thing a downstream skill can check itself against
- **Execution does not begin while `open_questions` is non-empty.** Deferring an
  unknown to "I'll decide while designing" is the shared entrance to both rework
  and scope creep

## Constraints do not loosen mid-run

`axes`, `standard`, `baseline`, and `excludes` are fixed at the start. About to
break one — stop and hand back. **An axis quietly dropped to make the result
defensible is the most expensive kind of false report**, because the artifact
still looks finished.
