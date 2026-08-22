<!-- design:guidance -->
# Naming Grammar

The grammar is decided once, before any token exists. Repairing a grammar later costs a migration.

## Pattern

```
--<category>-<role>-<variant>-<state>
```

| Slot | Required | Examples |
|------|----------|----------|
| category | yes | `color`, `space`, `text`, `radius`, `shadow`, `z`, `duration`, `ease` |
| role | yes | `text`, `bg`, `border`, `icon`, `action`, `danger` |
| variant | no | `primary`, `muted`, `subtle`, `inverse`, `on-accent` |
| state | no | `hover`, `active`, `focus`, `disabled`, `visited` |

Examples:

```
--color-text-primary
--color-text-muted
--color-bg-surface
--color-border-subtle
--color-action-bg-hover
--color-danger-text
--space-4
--text-body-size
--radius-md
--shadow-overlay
--z-modal
```

## Tier signals

| Tier | Signal | Example |
|------|--------|---------|
| Primitive | Bare scale name with a numeric step | `--gray-700`, `--blue-500` |
| Semantic | Category + role, no hue name, no number | `--color-text-primary` |
| Component | Component name leads | `--button-bg-hover`, `--table-row-bg-striped` |

Reading a name should tell you its tier without opening the file.

## Rules

1. **No hue words at the semantic tier.** `--color-accent-bg` survives a rebrand; `--color-purple-bg` does not.
2. **No numbers at the semantic tier.** A number is a position in a ramp, which is a primitive concern. Exception: spacing and type scales, where the number *is* the semantic (`--space-4`).
3. **State is always the last segment.** This makes state variants sortable and greppable.
4. **`default` is never written.** `--color-text-primary` is the default state.
5. **Foreground on a coloured surface uses `on-`.** `--color-on-accent`, `--color-on-danger`.
6. **Never abbreviate below four characters.** `bg` and `fg` are the accepted exceptions; `clr`, `bdr`, `sz` are not.
7. **Singular category, plural never.** `--color-*`, not `--colors-*`.
8. **One grammar per repository.** If a framework imposes its own (Tailwind, MUI), adopt theirs rather than running two.

## Role catalogue (colour)

| Role | Meaning |
|------|---------|
| `text-primary` | Default reading text |
| `text-secondary` | Supporting text, still fully legible |
| `text-muted` | De-emphasised metadata |
| `text-inverse` | Text on inverted surfaces |
| `bg-canvas` | Page background |
| `bg-surface` | Raised container (cards, panels) |
| `bg-subtle` | Inset or striped areas |
| `border-subtle` | Low-emphasis dividers |
| `border-strong` | Control boundaries; must reach 3:1 |
| `action-bg` / `action-text` | Primary action |
| `danger` / `success` / `warning` / `info` | Semantic states |
| `focus-ring` | Focus indicator |

## Anti-patterns

| Name | Problem |
|------|---------|
| `--color-primary` | Primary *what*? Text, background, border all differ. **Exception:** under Tailwind's `--color-*` namespace the utility name supplies the missing role (`text-primary`, `bg-primary`) — rule 8 governs; see `reference/export-targets.md`. |
| `--color-gray-text` | Mixes tier and role |
| `--blue` | No category, no role, no ramp position |
| `--color-text-primary-2` | A number appended to dodge a naming decision |
| `--btn-clr` | Abbreviation soup |
| `--color-text-dark` | Encodes the theme into the name; breaks under theming |

## Deprecation

Never silently rename. Keep the old name as an alias for one release, mark it, and record the replacement.

```css
/* @deprecated → --color-text-muted. Remove after the next major. */
--color-text-tertiary: var(--color-text-muted);
```

Ship the find/replace mapping alongside.
