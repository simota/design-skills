<!-- design:deferred -->
# Theming

Purpose: How a theme remaps semantics, and what must be re-verified per theme.
Read when: specifying dark mode, high contrast, or multi-brand.
Verified: 2026-08-21 — no automated check.

A theme remaps semantic tokens onto different primitives. Nothing else changes.

## The rule

Two different switches, often confused:

```
A THEME  (light / dark / contrast / density)
  Primitives:  fixed
  Semantics:   remapped        ← the only layer a theme touches
  Components:  never theme-aware

A BRAND  (multi-brand, white-label)
  Primitives:  ramps swapped   ← the only layer a brand touches
  Semantics:   identical across brands
  Components:  never brand-aware
```

Never both in one switch. If a component needs to know the active theme or brand, a semantic token is missing.

## Dark mode

Dark is a *design*, not a transform. Inverting lightness produces muddy mid-tones, blown-out accents, and shadows that vanish.

| Concern | Light | Dark |
|---------|-------|------|
| Canvas | `--gray-0` | `--gray-950` — not `#000`; pure black kills elevation and increases halation |
| Surface | `--gray-0` on `--gray-50` canvas | *Lighter* than canvas (`--gray-900` on `--gray-950`) — elevation goes up in lightness |
| Elevation | Shadow | Shadow reads poorly; layer with lighter surfaces plus `--color-border-subtle` |
| Text primary | `--gray-950` | `--gray-100`, not `--gray-0` — full white on near-black is fatiguing |
| Accent | `--accent-600` | `--accent-400` — saturated accents that pass on white fail on dark; lighten and often desaturate |
| Semantic states | `*-700` text on `*-50` bg | `*-300` text on `*-950` bg |
| Images / illustration | as authored | may need a dimming layer or a dark variant |

Verify every text pair again after remapping. A pair passing in light says nothing about dark.

## Implementation shape

```css
:root {
  --color-bg-canvas:   var(--gray-0);
  --color-text-primary: var(--gray-950);
  --color-action-bg:    var(--accent-600);
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-bg-canvas:    var(--gray-950);
    --color-text-primary: var(--gray-100);
    --color-action-bg:    var(--accent-400);
  }
}

:root[data-theme="dark"] {
  --color-bg-canvas:    var(--gray-950);
  --color-text-primary: var(--gray-100);
  --color-action-bg:    var(--accent-400);
}
```

Rules:
- Define the complete light palette on bare `:root` so no token's only definition lives inside a media query.
- Support three states: explicit light, explicit dark, and system default. The `:not([data-theme="light"])` guard makes the toggle win in both directions.
- Set `color-scheme: light dark` so form controls and scrollbars follow.
- Avoid a flash of the wrong theme: apply the stored preference before first paint.

## Additional themes

| Theme | Trigger | What changes |
|-------|---------|--------------|
| High contrast | `prefers-contrast: more` / forced-colors | Border tokens strengthen, muted text promotes to secondary, focus ring thickens |
| Forced colors (Windows) | `forced-colors: active` | Do not fight it. Map to system keywords (`CanvasText`, `Highlight`, `ButtonBorder`) and ensure nothing relies on a background image for meaning |
| Multi-brand | Data attribute or build target | A *brand*, not a theme: the accent and neutral primitive ramps swap; the semantic layer is identical across brands |
| Density | Data attribute | Spacing and control-height semantics remap; colour untouched |

## Multi-brand structure

```
tokens/
  primitives/
    brand-a.json      ← ramps only
    brand-b.json
  semantic.json       ← one file, brand-agnostic, references {color.accent.600}
  themes/
    light.json
    dark.json
```

The semantic layer is written once. If a brand needs a semantic token the others do not, that is a signal the semantic layer is under-specified, not that the brand is special.

## Checklist before shipping a theme

- [ ] Every semantic token defined in the base theme exists in this theme
- [ ] Every text pair re-verified for contrast in this theme
- [ ] Focus ring visible against every surface in this theme
- [ ] Elevation still readable (shadow or border)
- [ ] Semantic state colours still distinguishable from each other
- [ ] Charts and data colours re-checked — categorical scales rarely survive a theme flip unchanged
- [ ] Images, logos, and illustrations have a variant or a treatment
