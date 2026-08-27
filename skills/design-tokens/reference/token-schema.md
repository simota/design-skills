<!-- design:deferred -->
# Token Schema

Purpose: The semantic role catalogue and the interchange format.
Read when: deciding which roles exist, or emitting structured token data.
Source: DTCG, Tailwind, WCAG 2.2 — the format and the contrast exemption both move without this page.
Verified: 2026-08-21 — no automated check.

The semantic catalogue, plus the interchange format.

## Semantic colour catalogue

Fill this table for every project. `Resolves to` names a primitive; `Contrast` is measured, not assumed.

| Semantic token | Role | Resolves to | On | Contrast | Requirement |
|----------------|------|-------------|----|----------|-------------|
| `--color-text-primary` | Default reading text | `--gray-950` | `bg-canvas` | | ≥4.5:1 |
| `--color-text-secondary` | Supporting text | `--gray-700` | `bg-canvas` | | ≥4.5:1 |
| `--color-text-muted` | Metadata | `--gray-500` | `bg-canvas` | | ≥4.5:1 |
| `--color-text-inverse` | Text on inverted surface | `--gray-50` | `bg-inverse` | | ≥4.5:1 |
| `--color-text-link` | Hyperlink | `--accent-700` | `bg-canvas` | | ≥4.5:1 |
| `--color-bg-canvas` | Page background | `--gray-0` | — | — | — |
| `--color-bg-surface` | Raised container | `--gray-0` | — | — | — |
| `--color-bg-subtle` | Inset area | `--gray-50` | — | — | — |
| `--color-bg-inverse` | Inverted surface | `--gray-950` | — | — | — |
| `--color-border-subtle` | Divider | `--gray-200` | `bg-canvas` | | decorative |
| `--color-border-strong` | Control boundary | `--gray-400` | `bg-canvas` | | ≥3:1 |
| `--color-action-bg` | Primary action fill | `--accent-600` | — | — | — |
| `--color-on-action` | Text on action fill | `--gray-0` | `action-bg` | | ≥4.5:1 |
| `--color-action-bg-hover` | Action hover | `--accent-700` | — | — | — |
| `--color-focus-ring` | Focus indicator | `--accent-500` | adjacent | | ≥3:1 |
| `--color-danger-text` | Error text | `--red-700` | `bg-canvas` | | ≥4.5:1 |
| `--color-danger-bg` | Error surface | `--red-50` | — | — | — |
| `--color-danger-border` | Error boundary | `--red-300` | `danger-bg` | | ≥3:1 |
| `--color-success-*` | Success set | | | | mirror danger |
| `--color-warning-*` | Warning set | | | | mirror danger |
| `--color-info-*` | Info set | | | | mirror danger |

Rules:
- Every semantic state set (`danger`, `success`, `warning`, `info`) carries `text`, `bg`, and `border`. A set with only `text` forces implementers to invent the rest.
- `--color-focus-ring` is never optional and is never `transparent` in any theme.
- Disabled styling is a semantic pair too (`--color-text-disabled`, `--color-bg-disabled`); it is contrast-exempt under WCAG 2.2 but must still be visibly distinct from enabled.

## Typography semantics

| Token | Composes |
|-------|----------|
| `--text-body-*` | `size`, `line-height`, `weight`, `tracking`, `family` |
| `--text-heading-{1..4}-*` | same five properties |
| `--text-label-*` | Form labels, table headers |
| `--text-code-*` | Mono family, tabular figures |

Group the five properties as a composite token where the export format supports it (DTCG `typography` type, Tailwind `fontSize` tuple); otherwise emit them as a named cluster.

## W3C DTCG format

The interchange format for tool-agnostic token files.

```json
{
  "$schema": "https://tr.designtokens.org/format/",
  "color": {
    "gray": {
      "950": { "$type": "color", "$value": "#0d0f13" },
      "50":  { "$type": "color", "$value": "#f7f8fa" }
    },
    "text": {
      "primary": {
        "$type": "color",
        "$value": "{color.gray.950}",
        "$description": "Default reading text. 19.18:1 on bg.canvas."
      }
    }
  },
  "space": {
    "4": { "$type": "dimension", "$value": { "value": 16, "unit": "px" } }
  },
  "text": {
    "body": {
      "$type": "typography",
      "$value": {
        "fontFamily": "{font.ui}",
        "fontSize":   { "value": 16, "unit": "px" },
        "fontWeight": 400,
        "lineHeight": 1.55,
        "letterSpacing": { "value": 0, "unit": "px" }
      }
    }
  }
}
```

Rules:
- `$value` references use `{dot.path}` — that is how the alias graph stays machine-checkable.
- `$description` carries the contrast result and usage note. Do not let it degrade into a restatement of the name.
- `$type` is required on leaves; group-level `$type` inheritance is allowed but state it once at the group.

## Validation checks

Run these before export:

1. No semantic token resolves to a literal — every one references a primitive.
2. No component token references a primitive.
3. No unreferenced primitives (dead ramp steps) — either use or drop them.
4. No two semantic tokens with identical value *and* identical role (one should be an alias).
5. Every `text`/`bg` pair in the catalogue has a recorded ratio meeting its requirement.
6. Every semantic token that exists in one theme exists in all themes.
