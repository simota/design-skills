<!-- design:contract -->
# HANDOFF — passing work between design skills

Every `T1` and `T2` run returns one, whether the next reader is another skill, a
person, or a later session. It is the single place the facts live, and it is the
**record, not the report**: what a person reads is a bounded view over it
(`_design/REPORT.md`), never this object rendered field by field.

**`T0` is the exception** (`_design/SIZING.md`): a one-skill, reversible,
single-value change returns its one-line answer and no handoff. It still says
where the number came from — `T0` drops the paperwork, never the evidence.

## The object

```yaml
brief:                        # every field of the brief in _design/SIZING.md
  goal: "<one sentence describing the state once achieved>"
  delivers: "<a single artifact>"
  axes: [...]                 # every one must hold
  excludes: [...]             # may not be empty
  baseline: "<the observed starting state>"
  standard: "<what the result is judged against>"
  open_questions: []          # must be empty; a non-empty one never travels
status: DONE                  # DONE | PARTIAL | BLOCKED  (_design/CONTRACT.md)
decided: "<what this stage settled, 1-3 lines>"
evidence:
  "<decision>": { level: measured, how: "<what was measured and what it showed>" }
open:
  - { what: "...", class: UNSPECIFIED, marker: "<file>:<section>", written: true }
swept: "1 marker / 1 in open; 18 decisions / 18 graded"
next: "<the skill that should receive this, or none>"
```

- **`brief` travels whole and is not modifiable** — every field, not a subset.
  Rewriting the brief downstream is the main route by which scope creeps, and in
  design it is invisible: the artifact still looks like the thing that was asked for
- **The keys of `evidence` are decisions, not files** (`_design/CONTRACT.md`).
  A document arriving with one entry is a document whose decisions were not counted
- **`standard` travels or the receiver cannot judge anything.** A critique with
  no standard is preference; a token set with no direction behind it is
  descriptive, and the handoff says which it is
- **`open` carries a class and the class decides what happens.** `BLOCKED` and
  `UNSPECIFIED` stop the chain and go back to the human; `DEFERRED` and
  `OUT-OF-SCOPE` travel as record, so the receiver learns what was already
  decided against rather than rediscovering it
- **`written` says whether the marker is in the document yet.** A report-only
  skill sets it `false` and names where it belongs; the first receiver holding
  `Write` places it and flips the flag
- Pass the decisions, not the exploration. The options considered and rejected
  belong in the artifact if they are load-bearing, and nowhere if they are not

## What the receiver checks before starting

1. Is a whole `brief` attached, with every field present? A pointer to one is
   not one, and a subset is a brief that lost a constraint in transit
2. Is `standard` set, and is it something this stage can actually judge against?
3. Does `open` hold a `BLOCKED` or `UNSPECIFIED`? Hand back to the human
4. Is every `evidence` level above `asserted`, and is every measurable claim
   `measured` rather than `inspected`?
5. Do `swept` and `evidence` agree, and does every marker counted appear in `open`?
6. Is any `open` entry `written: false`? If you hold `Write`, placing those
   markers is part of your run
7. Does the work about to start fall under the brief's `excludes`?

## Send-backs

A send-back **names the check that failed and the field it failed on**. Without
that, the same handoff returns unchanged and the round trip bought nothing.

**After two round-trips on the same handoff, hand back to the human.** Being
rejected twice points at the brief or at how the work was divided, not at the
design.
