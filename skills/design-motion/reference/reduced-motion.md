<!-- design:deferred -->
# Reduced Motion

Purpose: Preserve state and information when reducing or removing motion.
Read when: specifying reduced-motion behaviour, including a static variant.
Source: WCAG 2.2 SC 2.3.3; CSS Media Queries Level 5 `prefers-reduced-motion`.
Verified: 2026-09-17 — checked the named sources for reduced behaviour; no automated check.

A reduced variant is a decided behaviour, not necessarily another animation.
Instant changes and static feedback are valid when information and operation survive.
No duration or opacity effect is guaranteed suitable for every user.

## Substitution choices

| Full motion | Reduced behaviour to decide |
|-------------|-----------------------------|
| Slide, zoom or scale | Instant placement, or a justified reduced effect |
| Staggered reveal | Content available together |
| Skeleton shimmer | Static placeholders |
| Spinner | Static indicator and status text |
| Parallax | Fixed layers |
| Background video | Poster frame, play on request |
| Auto-advance | Manual control |
| Error shake | Static error indication; retain the UX-specified focus behaviour |
| List reorder or route transition | Immediate final state with any required context |
| Progress | Actual state without decorative motion |

Use the preference exposed by the target platform. On the web, CSS Media Queries
Level 5 defines `prefers-reduced-motion`; on native platforms, consult the actual
platform documentation before naming an API or treating a setting as equivalent.

## State must not depend on animation completion

Removing an animation must not strand the UI. State transitions and completion
of work are independent of animation-end events. Do not rely on an almost-zero
duration to guarantee callbacks. Specify what cancellation, interruption and
instant completion do, including any announcement or focus destination owned by UX.

## Conformance and guidance have different authority

WCAG 2.2 SC 2.3.3 addresses disabling non-essential interaction-triggered motion
at Level AAA. It does not prescribe an alternative animation or a safe duration.
Ask `design-a11y` to adjudicate applicable criteria, including pausing movement
and flash limits, with their conditions and exceptions. A reduced-motion variant
alone is not a conformance verdict.

Large moving areas, parallax, zoom and rotation deserve particular scrutiny;
this is risk guidance, not permission to fabricate a criterion failure or a
universal safety threshold. Prefer a static choice where motion adds no needed information.

## Verify

Exercise full and reduced behaviour on the target platform or an appropriate
emulation. Record the artifact, preference, state changes and input tested.
A design-only spec can be inspected for completeness; runtime behaviour remains
unverified until exercised. Neither a screenshot nor a stated variant proves it runs.

- Retain all required states, information and controls.
- Specify interruption and the instant path without animation-end dependencies.
- Keep progress tied to actual work, not elapsed animation time.
- Record missing runtime tests rather than reporting a pass.

Sources checked: [WCAG SC 2.3.3 explanation](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
and [CSS preference definition](https://www.w3.org/TR/mediaqueries-5/#prefers-reduced-motion).
