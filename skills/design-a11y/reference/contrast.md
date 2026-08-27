<!-- design:deferred -->
# Contrast

Purpose: The ratios the standard requires, how to compute them, and what to do when a pair fails.
Read when: checking any colour pair, or repairing one that fails.
Source: WCAG 2.2 SC 1.4.3, 1.4.11 — the ratios below are that version's; the luminance formula is unchanged since 2.0.
Verified: 2026-08-21 — and re-verified by `make figures` on every run. Each recorded pair below is
recomputed from its two hex values against the WCAG relative-luminance formula, and its pass/fail is
recomputed from the ratio and the requirement. A wrong number here fails the build; it does not age.

Measure, record, repair. Never estimate.

## Ratios required

| Content | Ratio | SC |
|---------|-------|-----|
| Text under 24px (or under 18.66px bold) | 4.5:1 | WCAG 2.2 SC 1.4.3 AA |
| Text 24px+ (or 18.66px+ bold) | 3:1 | 1.4.3 AA |
| Control boundaries, focus rings, meaningful icons, graph elements | 3:1 | 1.4.11 AA |
| AAA body text | 7:1 | 1.4.6 AAA |
| Disabled controls, logotypes, decorative content | exempt | — |

Note that 24px/18.66px correspond to 18pt/14pt bold in the spec's wording.

## Recording format

Never state a pass without both source values.

| Pair | Foreground | Background | Ratio | Required | Result |
|------|-----------|------------|-------|----------|--------|
| Body on canvas | `#16181d` | `#ffffff` | 17.76:1 | 4.5:1 | pass |
| Muted on canvas | `#9aa0a6` | `#ffffff` | 2.64:1 | 4.5:1 | **fail** |
| On-accent on accent | `#ffffff` | `#3560d8` | 5.50:1 | 4.5:1 | pass |
| Border on canvas | `#d4d7dd` | `#ffffff` | 1.44:1 | 3:1 (control) | **fail if it is a control boundary** |
| Focus ring on canvas | `#3560d8` | `#ffffff` | 5.50:1 | 3:1 | pass |
| Focus ring on accent button | `#3560d8` | `#3560d8` | 1:1 | 3:1 | **fail — needs an offset ring** |

That last row is the most-missed case: a focus ring the same colour as the element it surrounds. Use an offset ring plus a contrasting outer ring, or invert the ring on coloured surfaces.

## Repairing a failing pair

In priority order:

1. **Darken or lighten the foreground.** Cheapest, least visible change. Step along the existing ramp rather than inventing a value.
2. **Adjust the background.** Only if the surface is not carrying brand meaning.
3. **Increase the size or weight.** Crossing into the large-text threshold drops the requirement to 3:1 — legitimate for headings, not for body copy.
4. **Change the role.** If muted text cannot reach 4.5:1 without becoming secondary text, the design may be asking for a distinction the palette cannot carry.
5. **Add a non-colour signal.** Does not fix contrast, but often the real problem was relying on colour for meaning in the first place.

When a fixed brand colour cannot pass: keep it for large display text, backgrounds, and non-text elements, and use a darkened variant for body text. Record this as a deliberate split and hand the two required roles to `design-tokens` to name — this skill states the roles and the ratios they must reach, not the token names.

## Common failures

| Failure | Fix |
|---------|-----|
| Placeholder text as content | Placeholders are hints, not labels; the label carries the meaning and must pass |
| Light grey secondary text | Most "elegant grey" values sit between 2.5:1 and 4:1; step darker |
| White text on a mid-saturation brand colour | Usually 3–4:1; darken the surface or use dark text |
| Text over an image or gradient | Add a scrim, and measure against the *lightest* pixel behind the text |
| Icon-only buttons | Meaningful icons need 3:1 (SC 1.4.11) |
| Chart series | Adjacent series need 3:1 from each other and a non-colour distinction |
| Focus ring on a coloured button | Offset ring or inverted ring colour |
| Dark theme accent | Accents passing on white commonly fail on near-black; lighten per theme |
| Disabled styling used to dodge contrast | Disabled is exempt only when genuinely non-interactive |

## Colour independence (SC 1.4.1)

Contrast is not the whole of colour accessibility. Every meaning carried by colour needs a second channel:

| Meaning | Second channel |
|---------|----------------|
| Error / success | Icon plus text |
| Required field | Text label or asterisk with a legend |
| Link in body text | Underline, or 3:1 against surrounding text *and* a non-colour cue on hover/focus |
| Chart series | Direct labels, patterns, or distinct markers |
| Status | Text label, not just a coloured dot |
| Selected state | Border, checkmark, or weight change |

Test by rendering in greyscale. If any meaning disappears, SC 1.4.1 fails.

## Per-theme verification

Every pair is re-measured in every theme. A pass in light says nothing about dark.

Also check:
- `forced-colors: active` (Windows High Contrast) — nothing may depend on a background image or a custom colour for meaning.
- `prefers-contrast: more` — if supported, border tokens strengthen and muted text promotes.

## How to compute

Compute every ratio. Do not read one off a swatch, and do not carry one forward from another document.

WCAG 2.x relative luminance, for each of R, G, B expressed as 0–1:

```
c_lin = c / 12.92                    if c <= 0.04045
c_lin = ((c + 0.055) / 1.055) ^ 2.4  otherwise

L     = 0.2126 * R_lin + 0.7152 * G_lin + 0.0722 * B_lin
ratio = (L_lighter + 0.05) / (L_darker + 0.05)
```

Runnable form — pass hex pairs, get ratios:

```python
def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def luminance(hex_colour):
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def ratio(fg, bg):
    a, b = luminance(fg), luminance(bg)
    if a < b:
        a, b = b, a
    return (a + 0.05) / (b + 0.05)

for fg, bg in [("#16181d", "#ffffff"), ("#9aa0a6", "#ffffff")]:
    print(f"{fg} on {bg}: {ratio(fg, bg):.2f}:1")
```

Notes:
- Semi-transparent foregrounds must be composited against the actual backdrop first; the formula takes opaque values only.
- Text over a gradient or image is measured against the **lightest** pixel behind the text, not the average.
- Round to two decimals and record the two source values beside the result. A ratio without its inputs cannot be re-checked.

Every example ratio in this package was produced by the snippet above, not typed by hand.

## Tools

Browser DevTools' contrast readout, the WebAIM contrast checker, and APCA (used by WCAG 3 drafts) for perceptual accuracy — all three are interactive and are for a human reviewer to confirm your computed value, never a substitute for computing it. APCA is informative only; conformance claims are made against WCAG 2.x ratios.
