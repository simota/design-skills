<!-- design:deferred -->
# Motion Tokens

Purpose: Named duration and easing values, plus the rule that assigns them.
Read when: choosing a value, or naming one for `design-tokens` to store.
Verified: 2026-08-21 — no automated check.

Named values, plus the rule that assigns them. Store the results via `design-tokens`.

## Duration

```css
--duration-instant: 75ms;
--duration-fast:    150ms;
--duration-base:    200ms;
--duration-slow:    300ms;
--duration-slower:  400ms;
```

Assignment rule — pick by **travel distance and area changed**, not by component type:

| Change | Token |
|--------|-------|
| Colour, opacity, ≤4px movement | `instant` |
| ≤100px travel, or a small element appearing | `fast` |
| 100–300px travel, dropdown/popover | `base` |
| Half-screen: modal, drawer, sheet | `slow` |
| Full screen: route, page-level | `slower` |

Exit duration is **one scale step below entry** — 300→200, 200→150, 150→100. Entering asks for attention; leaving should get out of the way. (Stated as a step, not a ratio: a 0.75× rule yields 225ms, which is not on the scale.)

## Easing

```css
--ease-out:      cubic-bezier(0.16, 1, 0.3, 1);
--ease-in:       cubic-bezier(0.7, 0, 0.84, 0);
--ease-in-out:   cubic-bezier(0.65, 0, 0.35, 1);
--ease-linear:   linear;
--ease-emphasis: cubic-bezier(0.34, 1.56, 0.64, 1);
```

Assignment rule:

| Situation | Easing |
|-----------|--------|
| Element enters the screen | `out` |
| Element leaves the screen | `in` |
| Element moves between two visible positions | `in-out` |
| Continuous, indeterminate | `linear` |
| One confirming or celebratory moment | `emphasis` |

`--ease-out` is the default. When unsure, use it — decelerating motion reads as responsive because most of the travel happens immediately.

## Spring alternative (native)

On iOS and Android, springs describe motion better than curves, especially for gesture-driven interaction where the spring inherits the gesture's velocity.

| Token | Response | Damping | Feels |
|-------|----------|---------|-------|
| `spring-snappy` | 0.25 | 1.0 | Crisp, no overshoot |
| `spring-default` | 0.35 | 0.9 | Slight settle |
| `spring-gentle` | 0.5 | 1.0 | Soft, deliberate |
| `spring-bouncy` | 0.4 | 0.7 | Visible overshoot; use once |

Match a curve-based web spec to a spring-based native spec by feel, not by numbers — a 300ms `ease-out` is roughly `spring-default`.

## Delay and stagger

```css
--stagger-tight: 20ms;
--stagger-base:  40ms;
--stagger-loose: 60ms;
```

Rules:
- Stagger reveals order, so use it only where order carries meaning.
- Total stagger across a group must not exceed ~200ms. Beyond that, the last item feels broken.
- Cap the staggered set at ~6 items; animate the rest as a group.
- Never stagger a list the user is scrolling through.

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
