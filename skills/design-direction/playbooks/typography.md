<!-- design:guidance -->
# Typography Direction

Typography carries more of the direction than colour does. Decide roles first, families second.

## Roles

| Role | Job | Selection pressure |
|------|-----|--------------------|
| Display | Headlines, hero, marketing moments | Personality; can be idiosyncratic |
| UI / body | Everything the user reads to work | Legibility at 14–16px, wide weight range, good hinting |
| Mono / numeric | Code, IDs, tabular figures | Tabular lining figures, unambiguous `0/O` `1/l/I` |

A direction may fuse Display and UI into one family — that is a decision, and it needs a reason ("one family keeps the tool feeling like a single surface").

## Pairing strategies

| Strategy | Pairing | Reads as |
|----------|---------|----------|
| Contrast | Serif display + sans UI | Editorial, authoritative |
| Superfamily | One family's serif and sans cuts | Cohesive, systematic |
| Single voice | One family across all roles, weight does the work | Restrained, tool-like |
| Expressive display | Distinctive display + neutral UI | Brand-forward marketing |

Avoid pairing two neutral sans families — the difference is invisible and the extra load buys nothing.

## Scale

Pick a ratio, then round to whole pixels. Ratios are intent; the rounded values are the spec.

| Ratio | Name | Feels | Good for |
|-------|------|-------|----------|
| 1.125 | Major second | Tight, uniform | Dense tools, dashboards |
| 1.200 | Minor third | Balanced | General product UI |
| 1.250 | Major third | Clear hierarchy | Content products |
| 1.333 | Perfect fourth | Dramatic | Marketing, editorial |

Rules:
- Body size is the scale's anchor, not the smallest step. Set body first (16px web default; 14px only for genuinely dense professional tools).
- Cap the number of steps. Six to eight sizes covers almost every product; more is drift.
- Long-form line length: 60–75 characters. UI line length: 45–75.
- Line height loosens as size shrinks: ~1.5–1.6 for body, ~1.1–1.25 for display.

## Fallback stacks

Every family needs a stack that degrades sanely and matches metrics closely enough to avoid layout shift.

State the stack per role, as plain text. Token names are `design-tokens`' output, not this skill's — do not invent them here.

| Role | Stack after the chosen family |
|------|-------------------------------|
| UI / body | `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif` |
| Display | `Georgia, "Times New Roman", serif` |
| Mono | `ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace` |

Specify `font-display: swap` intent and note whether a metric-compatible fallback (`size-adjust`) is required.

## Weight discipline

- Choose a weight range, not "all of them". Three weights (e.g. 400/500/700) covers most products.
- Variable fonts allow finer control but do not license you to use nine weights.
- Never fake weight with `font-weight: bold` on a family lacking the cut — synthetic bold is a craft failure.

## Licensing

Record for each family: licence type (open / desktop / webfont / app), whether self-hosting is permitted, pageview limits, and whether embedding in a native app or PDF export is covered. Flag any family the user cannot legally ship before it enters the brief.

## Non-Latin coverage

If the product ships beyond Latin, check the family covers the required scripts (CJK, Cyrillic, Arabic, Devanagari) — or specify a per-script family with matched optical size. Do not discover this after the direction is approved.
