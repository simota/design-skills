# design-skills

Seven agent skills covering design decisions, the contracts they share, and the
budgets that keep the set from growing into something nobody can route through.
Each skill owns one kind of decision and returns evidence rather than taste.

**None of them write implementation code.** A design deliverable here is a
decision with its grounds; the artifact demonstrates it.

## The skills

| Skill | Owns | Produces |
|---|---|---|
| [`design-direction`](skills/design-direction/SKILL.md) | How it should look and feel, and why | A brief |
| [`design-tokens`](skills/design-tokens/SKILL.md) | The named values the direction becomes | Token tables and exports |
| [`design-ux`](skills/design-ux/SKILL.md) | How it behaves and what states exist | A spec |
| [`design-motion`](skills/design-motion/SKILL.md) | How change over time reads | A motion spec |
| [`design-a11y`](skills/design-a11y/SKILL.md) | Whether it is operable by everyone | Findings and specified fixes |
| [`design-critique`](skills/design-critique/SKILL.md) | What is wrong with what exists | Nothing. Report-only |
| [`design-review`](skills/design-review/SKILL.md) | Whether the rendered result looks good | Nothing. Report-only |

## The idea the set is built on

**Every literal value in an output names where it came from.** `16px`,
`#3B82F6`, `200ms` — each looks decided, and most are the first plausible
number carried forward until nobody remembers whether it was chosen. So a value
carries one of six grounds: `token`, `threshold`, `measured`, `derived`,
`platform`, `brief` — the token name, the criterion and its number, what was
measured, the rule it was computed by, the cited convention, or the line of the
brief.

A value nothing fixes is `ARBITRARY`, and that is a legitimate answer recorded
in the handoff, never an invented reason — design runs out of grounds long
before it runs out of decisions. **A deliverable that is mostly `ARBITRARY` is
a direction problem**, upstream, not a row of rationales
([`_design/PROVENANCE.md`](skills/_design/PROVENANCE.md)).

## How it is put together

A skill is loaded in three stages, and each costs something different. The
**listing** carries `name` and `description` only, for every enabled skill, on
every turn. **`SKILL.md`** is read in full once a skill is chosen. Anything it
points at is read only when the situation calls for it.

**Selection happens on the description alone.** Nothing else is in front of the
engine at that moment. So every word that selects a skill appears literally in
its description, and [`design-registry/capabilities.yaml`](design-registry/capabilities.yaml)
lists those words per skill. A rule checks the two agree.

**Boundaries live in one file.** That same registry carries `not:` — what a
skill does not do and where that work goes instead. Descriptions never name a
neighbour. If they did, adding an eighth skill would mean editing the other seven,
and a description would spend its 200-character listing budget advertising a
competitor.

**Contracts are delivered, not referenced.** A rule kept in `skills/_design/` is read
on a minority of launches, so the operative part of each contract is copied
verbatim into every `SKILL.md` between `<!-- deliver:… -->` markers.
`design-registry/delivered/` holds the source, `make render` writes it back, and
a rule fails if any copy has drifted.

**Knowledge is split by whether it rots.** `playbooks/` holds judgement —
failure types, the order decisions go in, structures that stay true — and is
budgeted. `reference/` holds what goes stale — a standard's thresholds, an
export format, concrete values — carries no line budget, and states its purpose
and the date anyone last checked it instead.

**Where a number follows from another number, a date is not enough.** A
`Verified:` line records that someone looked once; it cannot fail, so it cannot
catch the value edited into a wrong one later. `make figures` recomputes what the
reference layer states from the reference layer itself — every recorded contrast
pair from its two hex values and its verdict from the requirement, and the type
scale from its own stated base and ratio. It runs in `make check` and in the
pre-commit hook, and six deliberately-introduced errors were each observed
failing it, including two that make the checks vacuous rather than wrong.

That is also how the type scale's clamp got written down: the ratio applied
downward gives 13px and 11px, the table said 14 and 12, and nothing on the page
admitted the departure. The values were right and the stated rule was not. A rule rejects a pinned version or
a cited standard inside a playbook, which is what forced two files across the
line while this was being set up.

**Budgets are enforced, not intended.**
[`design-registry/harness.yaml`](design-registry/harness.yaml) holds every
threshold. `design-tools/validate.py` decides them and CI fails on a violation.

## Evidence, for work that cannot be run

A design cannot be executed, so the grade is about **where the number came
from**. `measured` — a ratio computed, distinct values counted, a state list
checked against the running UI. `inspected` — read and reasoned over, with the
reason it could not be measured. `asserted` — the claim alone, which never
supports completion. **Estimating a measurable value is `asserted`**: contrast,
target size, scale ratios and token coverage are all countable, and a judgement
resting on a guessed number looks like a fact all the way to build.

**The unit is the decision, not the document.** A brief is one file and twenty
decisions, and a file-level grade hides the nineteen that were never made. Each
promised decision carries a grade or appears as `UNSPECIFIED` — which is what
gets invented at build time by whoever hits it first, without knowing it was a
decision.

## Names, and why none of them are generic

A skills directory is flat and shared with every other set installed on the
machine. A generic name placed there is a silent collision: `_common` in that
directory already belongs to an unrelated set.

**One declaration.** `set: design` in `design-registry/harness.yaml` is the only
place the name is written. The prefix (`design-`), the shared directory
(`skills/_design/`), and the label every document carries all derive from it.

**Every directory this set owns carries the set name** — `design-*` or
`_design`, with only the platform's own directories exempt. Carrying the prefix
is not what makes something installable: a skill is a directory holding a
`SKILL.md`, and only those are linked.

**Everything a skill reads lives inside the skill**, reached through symlinks
named `_design` and `registry`. A skill is handed its own directory as the base
for relative paths, and those are normalised *lexically*, so `../_design/X.md`
does not travel back through the install symlink. A shell follows the link and
finds the file, which is what makes this fail quietly.

## Files

| File | What it fixes |
|---|---|
| [`skills/_design/CONTRACT.md`](skills/_design/CONTRACT.md) | Evidence grades, status, residual classes, the completion sweep |
| [`skills/_design/SIZING.md`](skills/_design/SIZING.md) | How much ceremony a request is worth; when a dialogue is mandatory; the brief |
| [`skills/_design/HANDOFF.md`](skills/_design/HANDOFF.md) | What passes between skills, and the seven checks the receiver runs |
| [`skills/_design/VALUES.md`](skills/_design/VALUES.md) | The order that decides when two goods conflict, and the escape hatch |
| [`skills/_design/ROUTING.md`](skills/_design/ROUTING.md) | Guidance. Read when the owner is unclear or the work spans several |

## Layout

```
design-skills/
├── README.md
├── Makefile
├── design-registry/            # budgets, boundaries, routes, delivered blocks
├── design-tools/               # validate · test_validate · render · pre-commit
└── skills/                     # everything the CLI reads
    ├── _design/                # contracts in force on every run
    └── design-<facet>/         # a SKILL.md is what makes this a skill, and
        │                       # only skills are installed
        ├── SKILL.md            # Owns / Before starting / Decide first /
        │                       # Always·Never / Verify with / Done when
        ├── _design   -> ../_design       # short names: the parent scopes them
        ├── registry  -> ../../design-registry
        ├── playbooks/          # judgement. Budgeted, and must not rot
        └── reference/          # what goes stale. No line budget, dated instead
```

## Working on it

```sh
make check      # what CI runs: the rules, then proof the rules still fire
make render     # after editing anything in design-registry/delivered/
make hooks      # run the rules on every commit
```

Adding a rule means adding a deliberate violation to
`design-tools/test_validate.py` and watching it fail. A check only ever seen
passing may be checking nothing.

## Installing

```sh
make link                       # into ~/.claude/skills
make link CLAUDE_DIR=.claude/skills
```

Each `design-*` skill is linked individually, so a skills directory keeps
whatever else it already carries, and a name already taken by a real directory
is skipped rather than overwritten.

## What this does not guarantee

- **`allowed-tools` is one CLI's mechanism.** Where a tool grant is not
  enforced, the `Never` lines are discipline and nothing more
- **Read-only is not "sends nothing".** The permission class governs local
  writes. Anything leaving the machine is a separate question and needs asking
- **The fixtures do not model how a model chooses.** They catch a missing or
  duplicated signal. Passing them is not evidence that nothing will be misrouted
- **`Verified:` dates are not checked against anything.** A stale reference file
  with a fresh date passes. The date makes the staleness visible to a reader; it
  does not detect it
- **No rule here measures whether the right skill was picked.** That needs usage
  data this repo does not collect yet
- **Seven skills need no pack machinery.** Selection degrades as a listing
  grows; at this size the whole set is the working set. `packs_needed_above` in
  `design-registry/harness.yaml` names the point where that stops being true.
  Installed *beside* other sets it is a different question, and one this
  repository does not get to answer: all seven at once fills a shared listing to
  its ceiling, so what reaches an engine is a subset chosen out there

## The published overview

[`docs/index.html`](docs/index.html) is a generated page — every figure on it is
read off this repository, the way `make figures` recomputes what the reference
layer states. **Do not edit it by hand**: `tools/pages.py` in the `agent-toolkit`
repository writes it, `tools/pages.py --check` fails when it is behind, and
`.github/workflows/pages.yml` here only publishes what is committed.

