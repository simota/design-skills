<!-- design:deferred -->
# Migration

Purpose: Moving an existing codebase onto tokens: audit, mapping, staging, deprecation.
Read when: the values already exist and must become a system without breaking what users see.
Verified: 2026-08-21 — no automated check.

Moving an existing codebase onto tokens. Measure first; the audit determines whether the system is right.

## AUDIT

Inventory before naming anything.

```bash
# distinct hex colours, by frequency
grep -rhoE '#[0-9a-fA-F]{3,8}\b' src \
  --include='*.css' --include='*.scss' --include='*.ts' \
  --include='*.tsx' --include='*.vue' --include='*.svelte' \
  | tr 'A-F' 'a-f' | sort | uniq -c | sort -rn

# distinct px values
grep -rhoE '\b[0-9]+px\b' src \
  --include='*.css' --include='*.scss' --include='*.ts' --include='*.tsx' \
  | sort | uniq -c | sort -rn

# rgb()/rgba()/hsl() forms
grep -rhoE '(rgba?|hsla?)\([^)]*\)' src \
  --include='*.css' --include='*.scss' --include='*.ts' --include='*.tsx' \
  | sort | uniq -c | sort -rn

# existing custom properties
grep -rhoE '\-\-[a-z0-9-]+' src --include='*.css' | sort -u

# inline styles and arbitrary Tailwind values, which tokens cannot reach
grep -rn 'style={{' src --include='*.tsx' | wc -l
grep -rhoE '\[[0-9]+px\]|\[#[0-9a-fA-F]{3,8}\]' src | sort | uniq -c | sort -rn
```

`--include` takes one fnmatch glob per flag. A brace list (`'*.{css,tsx}'`) is **not** expanded inside quotes and matches nothing — the command exits 1 with no output, which reads as "no hardcoded values found". Repeat the flag, or use `rg`, which does support brace syntax. Run each command once against a directory you know has matches before trusting a zero result.

Record: distinct value count per category, the long tail (values used once), and the sites tokens cannot reach (inline styles, third-party components, email templates, canvas/SVG fills).

## Interpreting the audit

| Finding | Meaning | Action |
|---------|---------|--------|
| A grey ramp with more steps than the target scale | No system; values were eyeballed | Generate a ramp, map each old value to the nearest step, accept small visual shifts |
| Two near-identical accents | A rebrand happened halfway | Pick one, migrate, delete the other |
| Long tail of one-use values | Ad-hoc fixes | Most map to an existing step; the rest are bugs |
| Heavy inline styles | Tokens will not reach them | Include an inline-style removal pass in the plan, or scope it out explicitly |
| Existing custom properties with a different grammar | Two systems | Adopt theirs or migrate wholesale — never run both |

## Mapping

Produce an explicit table. Never a silent global replace.

| Old value | Occurrences | New token | Visual delta | Risk |
|-----------|-------------|-----------|--------------|------|
| `#333333` | 84 | `--color-text-primary` | ΔE ≈ 1.2 | none |
| `#3a3a3a` | 6 | `--color-text-primary` | ΔE ≈ 0.8 | none |
| `#767676` | 31 | `--color-text-muted` | exact | none |
| `13px` | 19 | `--text-sm` (14px) | +1px | check dense tables |

Flag any mapping with a visible delta (roughly ΔE > 3, or ≥2px) for review rather than folding it in quietly.

## Staged order

Migrate in this order — each stage is independently shippable and revertible.

1. **Introduce** — add the token file. Nothing consumes it yet. Zero risk.
2. **Colour** — highest value, most mechanical. Ship behind visual regression if available.
3. **Spacing** — riskier; layout shifts are visible. Migrate one surface at a time.
4. **Type** — riskiest; changes line breaks and content height. Do it last and check dense screens.
5. **Radius, elevation, z-index** — cleanup pass.
6. **Enforce** — add lint rules so new hardcoded values fail.
7. **Retire** — remove deprecated aliases after one release.

## Enforcement

```jsonc
// stylelint
{
  "rules": {
    "color-no-hex": true,
    "declaration-property-value-allowed-list": {
      "/^(padding|margin|gap)/": ["/^var\\(--space-/", "0", "auto"]
    }
  }
}
```

Add the rule in the same PR as the stage it protects, otherwise drift resumes immediately.

## What not to do

- Do not migrate and redesign in one change. If a value must shift for design reasons, that is a separate PR with its own review.
- Do not auto-replace by nearest colour without the mapping table — nearest is wrong for semantic pairs (a border and a muted text can share a hex and need different tokens).
- Do not leave a partially migrated file. File-level completeness makes review possible.
- Do not skip the audit because the codebase "isn't that big". The audit is where you learn the system is wrong.
