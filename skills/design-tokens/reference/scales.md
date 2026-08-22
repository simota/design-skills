<!-- design:deferred -->
# Scales

Purpose: Generation rules for spacing, type, radius, elevation, and colour ramps.
Read when: generating any scale, so the rule is written next to the values.
Verified: 2026-08-21 — the type scale is recomputed from its own stated base and ratio by
`make figures`, including the declared clamp. The other scales on this page are conventions and
carry no check; only the type scale claims to follow from a rule, so only it can be falsified.

Every scale comes from a stated rule. Write the rule next to the values.

## Spacing

Rule: base unit × a stepping sequence. 4px base is the common default; 8px suits marketing surfaces, 2px suits very dense tools.

| Token | 4px base | Use |
|-------|----------|-----|
| `--space-0` | 0 | Reset |
| `--space-1` | 4px | Icon-to-label gaps |
| `--space-2` | 8px | Tight internal padding |
| `--space-3` | 12px | Control padding |
| `--space-4` | 16px | Default block gap |
| `--space-5` | 20px | |
| `--space-6` | 24px | Card padding |
| `--space-8` | 32px | Section gap |
| `--space-10` | 40px | |
| `--space-12` | 48px | Major section gap |
| `--space-16` | 64px | Page rhythm |
| `--space-24` | 96px | Hero spacing |

Notes:
- The sequence skips (…6, 8, 10, 12, 16, 24) once steps exceed 24px — perceptually, large gaps need larger jumps.
- Do not offer every multiple. A scale with 24 steps is a number line, not a system.
- One scale serves padding, gap, and margin. Separate scales per property is drift.

## Type

Rule: body size anchors the scale; sizes step by a chosen ratio and round to whole pixels,
**clamped below `--text-base`**. Applied downward the ratio gives 13px and 11px, and both are
worse than the values below them: 13 reads as a rendering accident next to 14, and 11 is under
the size most people will accept for anything they have to read. The clamp is a decision, so it
is stated — an unstated departure makes the rule unfalsifiable and every future row a guess.

| Token | 16px / 1.20 ratio | Line height | Use |
|-------|-------------------|-------------|-----|
| `--text-xs` | 12px | 1.5 | Metadata, legal |
| `--text-sm` | 14px | 1.5 | Secondary UI |
| `--text-base` | 16px | 1.55 | Body |
| `--text-lg` | 19px | 1.45 | Lead paragraph |
| `--text-xl` | 23px | 1.35 | Section heading |
| `--text-2xl` | 28px | 1.25 | Page heading |
| `--text-3xl` | 33px | 1.2 | Display |
| `--text-4xl` | 40px | 1.1 | Hero |

Notes:
- Line height loosens as size shrinks and tightens as size grows.
- Pair each size with a tracking value when the family needs it; display sizes usually want slightly negative tracking.
- Six to eight steps is the working range. If a design needs a ninth, question the design.

## Radius

| Token | Value | Use |
|-------|-------|-----|
| `--radius-none` | 0 | Tables, full-bleed |
| `--radius-sm` | 4px | Inputs, badges |
| `--radius-md` | 8px | Buttons, cards |
| `--radius-lg` | 12px | Panels, modals |
| `--radius-full` | 9999px | Pills, avatars |

Rule: nested corners need the inner radius to be `outer − padding`, or the concentricity reads wrong. Record that rule; do not leave it to each implementer.

## Elevation

Elevation is shadow *and* z-index describing the same layering. Keep them in one table.

| Token | Shadow | `z` | Layer |
|-------|--------|-----|-------|
| `--shadow-none` | none | `--z-base: 0` | In-flow content |
| `--shadow-sm` | `0 1px 2px rgb(0 0 0 / .06)` | `--z-raised: 10` | Cards, hover lift |
| `--shadow-md` | `0 4px 8px -2px rgb(0 0 0 / .10)` | `--z-dropdown: 100` | Menus, popovers |
| `--shadow-lg` | `0 12px 24px -6px rgb(0 0 0 / .14)` | `--z-modal: 1000` | Dialogs, sheets |
| `--shadow-overlay` | `0 24px 48px -12px rgb(0 0 0 / .20)` | `--z-toast: 1100` | Toasts, top layer |

Notes:
- Never write a raw z-index number in component code. Named layers only.
- In dark themes, shadows lose contrast; carry a paired `--color-border-*` so elevation reads via border there.

## Colour ramps

Rule: pick steps in a perceptual space (OKLCH/LCH) with even lightness spacing, then convert.

- 9–11 steps for neutrals; 9 for each chromatic ramp.
- Hold chroma roughly constant across the mid-range; taper it at the extremes or the ends look muddy.
- Number by lightness: `50` lightest → `950` darkest. Keep the direction identical across all ramps.
- Verify the ramp against both the lightest and darkest planned surface.

## Breakpoints

| Token | Value | Target |
|-------|-------|--------|
| `--screen-sm` | 640px | Large phone |
| `--screen-md` | 768px | Tablet portrait |
| `--screen-lg` | 1024px | Tablet landscape / small laptop |
| `--screen-xl` | 1280px | Desktop |
| `--screen-2xl` | 1536px | Wide desktop |

Min-width based, mobile-first. Do not add a breakpoint for a single component — use a container query instead.
