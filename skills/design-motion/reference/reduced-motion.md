<!-- design:deferred -->
# Reduced Motion

Purpose: What the reduced variant does, per pattern — a designed state, not an absence.
Read when: specifying the reduced-motion behaviour of anything that moves.
Source: CSS Media Queries Level 5, `prefers-reduced-motion`
Verified: 2026-08-21 — no automated check.

`prefers-reduced-motion: reduce` is a designed variant, not a switch that deletes transitions.

## What the preference means

Users set it for vestibular disorders, migraine, motion sickness, attention needs, or simple preference. The triggering factor is **large-area movement, parallax, scaling, and rotation** — not motion in general. A 100ms opacity fade is not a trigger.

## Substitution table

| Full motion | Reduced variant |
|-------------|-----------------|
| Slide in from edge | Cross-fade, 100ms |
| Scale + fade modal | Fade only, 100ms |
| Staggered list reveal | All at once, or instant |
| Skeleton shimmer | Static neutral blocks |
| Spinner | Static indicator plus text |
| Parallax | None — the layer is fixed |
| Auto-playing background video | Static poster frame, play on request |
| Carousel auto-advance | Manual control only |
| Error shake | Static error styling plus focus move |
| FLIP list reorder | Instant reposition |
| Route transition | Instant |
| Progress bar | Keep — it conveys real state; remove any shimmer on it |

## Implementation shape

Prefer a token-level override so every consumer inherits it:

```css
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-instant: 0.01ms;
    --duration-fast:    0.01ms;
    --duration-base:    0.01ms;
    --duration-slow:    0.01ms;
    --duration-slower:  0.01ms;
  }
}
```

Then re-introduce the deliberate short fades where they aid comprehension:

```css
@media (prefers-reduced-motion: reduce) {
  .modal { transition: opacity 100ms linear; transform: none; }
  .skeleton { animation: none; }
}
```

Notes:
- `0.01ms` rather than `0` keeps `transitionend` and `animationend` handlers firing, so state machines depending on them do not stall.
- Never gate functionality on an animation completing — under reduced motion the callback may effectively be immediate.
- On native, read `UIAccessibility.isReduceMotionEnabled` (iOS) or `Settings.Global.TRANSITION_ANIMATION_SCALE` (Android) and branch the same way.

## Vestibular safety (applies to everyone, not only the preference)

Two lists, because they carry different authority. This skill designs against both but **adjudicates neither** — flag anything in the first list for `design-a11y`, which owns SC 2.2.2 / 2.3.1 / 2.3.3.

**Conformance (WCAG 2.2) — flag for `design-a11y` verification:**

- Nothing may flash more than three times per second (SC 2.3.1, Level A).
- Motion that starts without user action and lasts more than 5s needs a pause, stop, or hide control (SC 2.2.2, Level A).
- Non-essential motion triggered by interaction can be disabled (SC 2.3.3, Level AAA).

**House guidance (not conformance, no citable source) — apply by default, drop when the direction argues otherwise:**

- Avoid full-bleed movement; the larger the moving area, the stronger the trigger.
- Avoid large-scale zoom and rotation on big surfaces.
- Avoid parallax between layers.

## Testing

| Platform | How to enable |
|----------|---------------|
| macOS | System Settings → Accessibility → Display → Reduce motion |
| iOS | Settings → Accessibility → Motion → Reduce Motion |
| Windows | Settings → Accessibility → Visual effects → Animation effects off |
| Android | Settings → Accessibility → Remove animations |
| Chrome DevTools | Rendering panel → Emulate CSS media `prefers-reduced-motion` |

Test both variants for every animated moment specified. A reduced variant that was never run is a guess.

## Checklist

- [ ] Every animation in the spec has a stated reduced variant
- [ ] No functionality depends on an animation completing
- [ ] No loop runs under reduced motion
- [ ] Progress indicators still convey state
- [ ] Nothing flashes more than 3×/second in either variant (SC 2.3.1 — flag for `design-a11y`)
- [ ] Auto-playing motion over 5s has a pause control (SC 2.2.2 — flag for `design-a11y`)
- [ ] Both variants tested on a real device or emulated media
