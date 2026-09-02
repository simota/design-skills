<!-- design:guidance -->
# Severity

Rank by user impact, never by how obvious the finding was.

## Scale

| Level | Definition | Test |
|-------|-----------|------|
| Blocker | The user cannot complete the task | Would a real user get stuck? |
| Serious | Completable, but materially harder or riskier | Does it cost time, cause errors, or risk data? |
| Moderate | Confusion or friction | Would a user pause, or ask a question? |
| Minor | Craft gap with no functional barrier | Would a designer notice, but a user not? |
| Note | Observation or a defensible alternative | Is this taste rather than a defect? |

## Impact factors

Score each finding on three axes, then place it.

| Factor | High | Low |
|--------|------|-----|
| Frequency | Every session, every user | Rare path, few users |
| Consequence | Data loss, money, irreversible action | Cosmetic |
| Recoverability | No undo, no way back | Trivially reversible |

Rules of thumb:
- High consequence + no recovery = Blocker, even if rare.
- High frequency + low consequence = Serious if it costs time on every use; Moderate otherwise.
- Low frequency + low consequence + reversible = Minor at most.

## Classification

Independent of severity, mark each finding:

| Class | Meaning |
|-------|---------|
| `defect` | Measurably wrong against a stated standard — contrast ratio, missing state, broken layout |
| `inconsistency` | Violates the project's own system or its own prior decisions |
| `judgement` | A defensible alternative view; the current choice is not wrong |

A `judgement` finding is never above Moderate. If you cannot classify a finding as defect or inconsistency, it is a judgement — say so rather than inflating it.

## Tie-breaks

When two findings share a severity:

1. The one affecting more users ranks higher.
2. The one on a primary flow outranks one on a settings screen.
3. The one with a cheaper fix ranks higher (equal impact, less cost).
4. The one that blocks other fixes ranks higher.

## Report volume

A report nobody acts on has failed, and a report is acted on when each finding
is one decision. Aggregate repeats: "Spacing values off the scale at 14 sites —
see drift table" is one finding, not fourteen, and a whole-product review
carries its drift as a table rather than as findings. Blockers and Serious
findings are never folded away to make the list shorter.

## Common mis-rankings

| Mistake | Correction |
|---------|-----------|
| A 2px misalignment as Serious | Minor — no user is blocked |
| A confusing primary action as Moderate | Serious or Blocker — it is the screen's job |
| A missing empty state as Minor | Moderate at least — it is a state real users will hit first |
| Failing contrast on body text as Minor | Serious — it excludes users |
| Personal taste as a defect | Note, classified `judgement` |
| Twelve instances of one problem as twelve findings | One aggregated finding with a count |
