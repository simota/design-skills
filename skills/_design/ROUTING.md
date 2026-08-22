<!-- design:guidance -->
# ROUTING — which design skill owns this

A request with an obvious owner calls that skill directly. This is the fallback
and the ordering guide, not a gate.

**Boundaries are defined in `registry/capabilities.yaml`, not here and
not in any skill's description.** Each entry carries what a skill does, what it
does not (`not:`, with where that work goes instead), and the words that select
it. Writing an exclusion into a description makes every skill added rewrite its
neighbours; keeping it in one file makes an addition cost O(1). The table below
is a reading of that file, not a second copy of it.

## Ownership

| Skill | Owns | Writes? |
|---|---|---|
| `design-direction` | How it should look and feel, and why | A brief |
| `design-tokens` | The named values the direction becomes | Token tables and exports |
| `design-ux` | How the interface behaves and what states exist | A spec |
| `design-motion` | How change over time reads | A motion spec |
| `design-a11y` | Whether it is operable by everyone, decided at design time | Findings and specified fixes |
| `design-critique` | What is wrong with what exists | Nothing. Report-only |
| `design-review` | Whether the rendered result looks good | Nothing. Report-only |

**None of these write implementation code.** A design deliverable is a decision
with its grounds; the build belongs to a skill outside this set.

**Who decides a value.** Four skills produce numbers, so one rule settles it:
*the skill that decides a value owns it until it is named*, and **`design-tokens`
owns any value that outlives one screen**. A duration chosen while specifying a
transition is `design-motion`'s; the same duration stored as `motion.duration.fast`
is `design-tokens`'.

## Disambiguation

Where two skills are both plausible, `not:` in the registry says where the work
goes. These rows say *how to tell which case you are in*.

| Both plausible | Decided by |
|---|---|
| direction vs tokens | Is the aesthetic settled? Unsettled → direction. Settled, needs values → tokens |
| direction vs critique | Does the thing exist yet? Exists → critique. Being decided → direction |
| ux vs motion | Does the question name a state, or the passage between two? State → ux. Passage → motion |
| ux vs a11y | Is the failure "nobody can use this" or "some people cannot"? Everyone → ux. Some → a11y |
| a11y vs critique | **critique flags, a11y adjudicates.** A review may note a contrast risk; whether it conforms is a11y's to decide |
| critique vs anything | critique never produces the replacement. It says what is wrong and hands the fix to the owner |
| review vs critique | **review judges the whole, critique itemises the parts.** Is the question "does this hold together" or "what is wrong here"? |
| review vs direction | Does something rendered exist? Rendered → review. Being decided → direction. A verdict of `holds, thin` is review handing it back to direction |
| tokens vs motion | Motion decides the value; tokens decide its name and where it lives |

## Chains

The chains that recur are in `registry/routes.yaml`, with their control
structure rather than as prose: which stages, in what order, and what has to
hold before the next one starts.

A chain of names expresses linear work only. Where a stage repeats until a
condition holds — `critique-to-zero` is the one that does — the entry carries
the stopping condition, the judge, and a hard cycle limit. **The judge is never
the skill that produced the design.** Without those three, "until it looks
right" has no stopping rule and the loop ends when someone gets tired.

## Rules for running a chain

- **Settle the brief before the first stage**, including `standard`. Every stage
  receives it whole and it does not change mid-run (`_design/SIZING.md`)
- **A stage's output is a handoff** (`_design/HANDOFF.md`), and the next stage
  runs the seven receiver checks before starting
- **Never run a deciding skill on work classified as report-only.** "Review this"
  does not authorise a redesign, and neither does finding something obviously wrong
- **A chain wanting a seventh stage is mis-scoped.** Split the request instead
- Stages run in order. Two skills deciding the same values concurrently produces
  a contradiction, not a design
