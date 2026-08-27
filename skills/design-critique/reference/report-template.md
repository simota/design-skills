<!-- design:deferred -->
# Report Template

Purpose: The output structure and the tone rules that decide whether a report gets acted on.
Read when: writing the report.
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

The output structure. Tone rules matter as much as content — a report that reads as an attack does not get acted on.

## Structure

```markdown
# Design Review — <screen / flow / product>

## Standard
Judged against: <design brief | design system v2.1 | UX spec | platform conventions | general heuristics>
Source: <link or file>

## Scope
- Reviewed: <screens, states, breakpoints, themes>
- Not reviewed: <what, and why>
- Environment: <live URL / mockup / screenshots / code>

## Summary
1. <Blocker or top Serious finding, one line>
2. <Second, one line>
3. <Third, one line>

## What Works
- <Specific strength, and why preserving it matters>
- <…>

## Findings

### [Severity · class] <Title> — <location>

**Evidence:** <observed values, text, positions, counts>

**Impact:** <what it costs the user>

**Fix:** <specific, implementable change>

**Owner:** <design-ux | design-tokens | design-motion | design-a11y | engineering>

---

## System Drift

| Property | Used | System defines | Sites | Fix |
|----------|------|----------------|-------|-----|
| | | | | |

## Not Reviewed
| Area | Why |
|------|-----|
| | |

## Handoff
| Owner | Findings |
|-------|----------|
| design-ux | #2, #5, #9 |
| design-tokens | #3, drift table |
| design-a11y | #1, #7 |
```

## Tone rules

- Address the design, never the designer. "The two buttons compete", not "you made the buttons compete".
- State the observation before the judgement, always.
- Do not soften a Blocker. Hedging a real barrier wastes everyone's time.
- Do not inflate a Minor. Calling a 2px gap "critical" costs you credibility on the findings that matter.
- Ask rather than assert when intent is unclear: "If the intent was X, then Y is a problem — was it?"
- No sarcasm, no rhetorical questions, no "obviously".

## Evidence quality

| Weak | Strong |
|------|--------|
| "Spacing is inconsistent" | "Card padding is 16px, 20px, and 24px across three peer cards in the same grid" |
| "Poor contrast" | "`#9aa0a6` on `#ffffff` = 2.64:1; SC 1.4.3 AA requires 4.5:1" |
| "Confusing hierarchy" | "Three elements share the same 20px/600 treatment; nothing indicates which to read first" |
| "Feels cluttered" | "Nine interactive elements above the fold, five of them the same visual weight" |
| "Needs better empty state" | "No empty state exists; the table renders headers with zero rows and no explanation" |

## Fix quality

A fix is specific enough that an implementer would not need to ask a follow-up question.

| Weak | Strong |
|------|--------|
| "Improve the hierarchy" | "Demote 'Save changes' to the secondary outline style; leave 'Publish' as the only filled button" |
| "Fix the contrast" | "Change `--color-text-muted` from `#9aa0a6` to `#6b7280` (4.83:1 on canvas); re-check the dark theme" |
| "Add an empty state" | "Add a first-use empty state: one sentence of purpose plus a 'Create invoice' primary action; distinct from the filtered-empty state" |
| "Make targets bigger" | "Increase row action hit areas to 24×24 with padding (visual icon stays 20px) and space them 8px apart — SC 2.5.8" |

## When you cannot measure

Working from a screenshot with no source, mark findings honestly: "visual estimate — values not measurable from the supplied image". Do not present an estimate as a measurement. Request the source file or a live URL if precision matters to the decision.
