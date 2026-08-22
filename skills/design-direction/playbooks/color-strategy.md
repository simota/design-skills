<!-- design:guidance -->
# Colour Strategy

Colour is assigned to *roles*, never picked as a set of favourite hues.

## Order of operations

1. Choose the strategy mode (monochrome+accent, duotone, full semantic, neutral+imagery).
2. Build the neutral ramp first — most of the interface is neutral.
3. Add the accent, and decide the one job it does.
4. Add semantic colours only if the product has state that needs them.
5. Verify contrast for every text pair before the palette leaves this skill.

## Neutral ramp

Neutrals carry surface, border, and text. A ramp of 9–11 steps is standard.

- Do not use pure `#000` for text or pure `#FFF` for canvas unless the direction argues for that starkness; slight warmth or coolness in the neutrals is where the direction lives.
- Keep the ramp perceptually even. Pick steps in OKLCH or LCH and hold lightness spacing constant, then convert to hex; even spacing in sRGB is not even to the eye.
- Give the ramp a temperature and state it ("neutrals carry a +8° warm shift; the product should feel like paper, not glass").

## Accent

One accent, one job. Common jobs:

| Job | Consequence |
|-----|-------------|
| Primary action only | Highest clarity; accent becomes a wayfinding signal |
| Brand presence | Appears in nav, marks, empty states; weaker action signal |
| Data / category | Needs a full categorical scale; do not overload with action meaning |

If the accent does more than one job, users cannot learn what it means.

## Semantic colours

Only introduce success / warning / danger / info when the product genuinely has those states. Each needs:
- a foreground that passes AA on the app canvas,
- a subtle background that passes 3:1 against its border,
- a non-colour redundancy (icon, label) — colour must never be the sole carrier of meaning.

## Contrast verification (before proposing)

Every palette is checked against the bar *before* it is proposed, not repaired
after. The thresholds themselves belong to `design-a11y`, which owns the
standard and tracks it as it moves — restating them here would put a second
copy in a file nobody updates when the standard does.

Check, at minimum: body text on its background, large text, icons and component
boundaries, and the focus indicator against what sits next to it. Disabled text
is exempt, and using that exemption to dodge a contrast problem is not a pass.

Record the measured ratio in the brief. "Should be fine" is not a result.

## Dark mode as a direction question

Decide *whether* dark mode is in scope here; specify *how* in `design-tokens`. Two things must be settled at direction time:

- Is dark the primary surface or the alternate? Products designed light-first and inverted later look inverted.
- Does the accent survive the flip? Highly saturated accents that pass on white often fail on near-black and need a lighter variant.

## Anti-patterns

- Picking hues before the neutral ramp exists.
- A gradient used as the identity, with nothing underneath it.
- More than one accent, each equally loud.
- Semantic colours borrowed from a framework's defaults with no relation to the neutrals.
- Palettes tuned only against white; check against the darkest surface too.
