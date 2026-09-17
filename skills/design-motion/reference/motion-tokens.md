<!-- design:deferred -->
# Motion Tokens

Purpose: Named duration and easing values, plus the rule that assigns them.
Read when: choosing a value, or naming one for `design-tokens` to store.
Source: none — nothing outside this page can move what it states.
Verified: 2026-09-17 — reviewed as illustrative values, not external authority; no automated check.

Illustrative house values, not universal limits or published platform values.
Choosing these examples is `ARBITRARY` unless an independent source fixes the
choice. A calculated step still needs grounded base and step policy. Select and
record concrete values, then use `design-tokens` for naming and storage.

## Duration

```css
--duration-instant: 75ms;
--duration-fast:    150ms;
--duration-base:    200ms;
--duration-slow:    300ms;
--duration-slower:  400ms;
```

Illustrative associations to compare in context; travel distance and area do not uniquely fix timing:

| Change | Token |
|--------|-------|
| Colour, opacity, ≤4px movement | `instant` |
| ≤100px travel, or a small element appearing | `fast` |
| 100–300px travel, dropdown/popover | `base` |
| Half-screen: modal, drawer, sheet | `slow` |
| Full screen: route, page-level | `slower` |

Choose exit behaviour for the interaction, including reversal and interruption. No universal step-down or entry/exit ratio is implied by this example scale.

## Easing

```css
--ease-out:      cubic-bezier(0.16, 1, 0.3, 1);
--ease-in:       cubic-bezier(0.7, 0, 0.84, 0);
--ease-in-out:   cubic-bezier(0.65, 0, 0.35, 1);
--ease-linear:   linear;
--ease-emphasis: cubic-bezier(0.34, 1.56, 0.64, 1);
```

Illustrative pairings, not restrictions on other curves or physics-based responses:

| Situation | Easing |
|-----------|--------|
| Element enters the screen | `out` |
| Element leaves the screen | `in` |
| Element moves between two visible positions | `in-out` |
| Continuous, indeterminate | `linear` |
| One confirming or celebratory moment | `emphasis` |

Use the existing response model where applicable. A reference pairing is not evidence that it suits this interaction.

## Spring alternative (native)

A velocity-driven gesture may need a spring model. Name the actual platform API,
parameter meanings, units and source. A curve duration has no universal conversion
to a spring's parameters. Compare rendered behaviour, then record the concrete
chosen model and parameters; do not leave the conversion to the implementer.

## Delay and stagger

```css
--stagger-tight: 20ms;
--stagger-base:  40ms;
--stagger-loose: 60ms;
```

Rules:
- Stagger reveals order, so use it only where order carries meaning.
- Measure total group delay and input availability where an artifact runs.
- Choose the grouping for the task; there is no universal element-count cap.
- Do not delay access to content the user is already scrolling through.

## Loop durations

| Use | Duration |
|-----|----------|
| Spinner rotation | 800ms–1s, `linear` |
| Skeleton shimmer | 1.5–2s, `linear`, low contrast |
| Pulse / breathing indicator | 2s, `ease-in-out` |

All loops stop under reduced motion; replace with a static indicator.

## Composite tokens

Where the export format supports it, store trigger-level composites so implementers do not re-derive the pairing:

```json
{
  "motion": {
    "modal-enter": {
      "$type": "transition",
      "$value": { "duration": "{duration.slow}", "timingFunction": "{ease.out}", "delay": "0ms" }
    },
    "modal-exit": {
      "$type": "transition",
      "$value": { "duration": "{duration.base}", "timingFunction": "{ease.in}", "delay": "0ms" }
    }
  }
}
```
