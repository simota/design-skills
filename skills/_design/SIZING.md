<!-- design:contract -->
# SIZING — how much ceremony the request is worth

Ceremony **above** what a request needs is what gets a harness worked around.
Ceremony **below** it is how a decision goes unmade. Both come from the same
move — choosing the tier for comfort — so the tier is read on first match.

## The three tiers

| Tier | All of these hold | What it costs |
|---|---|---|
| `T0` | One skill obviously owns it · reversible · one bounded decision · scope and result fit in one sentence | Answer with ground and evidence. **No brief, no handoff** |
| `T1` | One skill owns it, but a `T0` condition fails | Settle the brief, then run. Handoff on return |
| `T2` | Two or more skills own parts of it, or staged deliverables need a handoff | Route it: settle the brief once, run the chain, one report covers every stage |

`T0` drops paperwork, not grounds, evidence or coverage. A screen containing
several promised decisions is not `T0` merely because it is one screen.
An internal phase list alone does not promote a run to `T2`.

**Finding mid-run that the tier was wrong means re-sizing and saying so.** A
`T0` contrast check that has turned into a palette revision is a `T1` that was
mis-sized.

## When a dialogue is required first

Read the request and existing artifacts first. Dialogue is required only when
one of these remains unresolved; do not re-ask an already authorised decision:

- The shape of the deliverable is not uniquely determined
- What counts as achieved does not fit in one sentence
- The request carries a word with no achievement condition — "make it modern",
  "cleaner", "more premium", "polish", "improve the hierarchy"
- Authority to replace a prior choice, or the guardrail for an expensive-to-undo
  change — a token grammar, navigation model, or shipped behaviour
- A term has competing meanings that change the decision or handoff, and neither
  the host's glossary nor the available context settles them

**Reading to find out is not executing.** The codebase, the existing screens,
and the current tokens answer more questions than the person can. Do not open
a dialogue over a reversible value whose scope and authority are already clear.

## The brief the dialogue produces

Conclusions recorded as data, not as an understanding. Execution reads only
this.

```yaml
goal: "<one sentence describing the state once achieved>"
delivers: "<one bounded outcome>"  # may require coordinated files
axes: [...]                       # meaningful achievement conditions; one may suffice
excludes: [...]                   # may be empty when delivers already bounds the scope
baseline: "<observed starting state, or n/a with a reason for new work>"
standard: "<applicable requirement or stated judgement basis; name any fallback>"
open_questions: []                # unresolved scope, authority or fixed constraints
terms: {}                         # the names this run uses, spelled as the glossary spells them
```

- **State the applicable standard or judgement basis.** A fallback heuristic
  supports a reasoned judgement, not an invented team requirement
- **Use meaningful `axes`, not a quota.** "Looks better" is not an achievement
  condition; a bounded token-resolution check need not invent a second axis
- **Make the boundary explicit** in `delivers` and, where needed, `excludes`
- **Resolve `open_questions` before executing.** These are scope and authority
  questions, not the design decisions the work was commissioned to make. Every
  promised decision must be settled before `DONE`, or recorded as `UNSPECIFIED`

## Terms — one name per concept, one concept per name

The host's glossary is `.agents/glossary.md` when it exists. Read it before the
brief is settled and write with its names only — tokens, components, states,
report alike. Record necessary new terms in `terms`; ask when their meaning
would change product scope or another owner's decisions.

**Do not silently resolve material ambiguity.** Ask one question with its
proposed default and record the answer in `terms`. A run with a write grant
may append the settled term to the glossary; a read-only run proposes it in the
handoff and never edits. `T0` does not create a glossary: unrelated naming debt
is `OUT-OF-SCOPE`; ambiguity blocking its own decision requires re-sizing.

## Constraints do not loosen mid-run

`axes`, `standard`, `baseline`, and `excludes` are fixed at the start. About to
break one — stop and hand back. **An axis quietly dropped to make the result
defensible is the most expensive kind of false report**, because the artifact
still looks finished.
