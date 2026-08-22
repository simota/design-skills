<!-- design:deferred -->
# Semantics, Names, and Roles

Purpose: Names, roles, and states as design decisions, and which native element carries each.
Read when: specifying what a control is called and announced as, or considering a custom widget.
Source: WCAG 2.2 SC 4.1.2; WAI-ARIA Authoring Practices
Verified: 2026-08-21 — no automated check.

Structure and naming are design decisions. Specify them; do not leave them to be guessed at build time.

## Native first

| Need | Use | Not |
|------|-----|-----|
| Action | `<button>` | `<div role="button" tabindex="0">` |
| Navigation | `<a href>` | `<button onclick=navigate>` |
| Choice from a short list | `<input type="radio">` | Custom cards with click handlers |
| Choice from a long list | `<select>` | Custom listbox, unless styling is essential |
| Expandable section | `<details>/<summary>` | Custom accordion |
| Modal | `<dialog>` | Custom overlay div |
| Progress | `<progress>` | Animated div |

Every native element replacement must state: which APG pattern it follows, why the native element was insufficient, and the full keyboard model. "It didn't match the design" is a reason to restyle, not to rebuild.

## Headings (SC 1.3.1, 2.4.6)

- One `<h1>` per page, naming the page's subject.
- No skipped levels. `h2` follows `h1`; a jump to `h4` breaks the outline.
- Headings describe content, not decoration. If text is large but is not a heading, style it — do not mark it up as one.
- Every distinct region of a complex screen deserves a heading, even if visually hidden.

## Landmarks

| Landmark | Contains | Count |
|----------|----------|-------|
| `banner` (`<header>`) | Site header | 1 per page |
| `navigation` (`<nav>`) | Nav groups | Multiple; each needs a distinguishing label |
| `main` | The primary content | Exactly 1 |
| `complementary` (`<aside>`) | Related but separate content | Multiple |
| `contentinfo` (`<footer>`) | Site footer | 1 per page |
| `search` | Search form | Usually 1 |
| `form` | A form with a label | As needed |

Multiple landmarks of the same type each need `aria-label` distinguishing them ("Primary", "Breadcrumb", "Footer").

## Accessible names (SC 4.1.2, 2.5.3)

Specify a name for every control in the design spec.

| Control | Name comes from | Design specifies |
|---------|-----------------|------------------|
| Button with text | Its text | The text |
| Icon-only button | `aria-label` | The label text |
| Input | `<label for>` | The visible label |
| Image | `alt` | The alt text or "decorative" |
| Link | Its text | Meaningful text — never "click here" or a bare "Read more" repeated |
| Region | `aria-label` / `aria-labelledby` | The region name |
| Dialog | `aria-labelledby` pointing at its title | The title |

**Label in Name (SC 2.5.3):** when a control has a visible label, the accessible name must contain that visible text. A button reading "Save" must not have `aria-label="Submit form"` — voice control users say what they see.

Icon-only controls: the label describes the *action*, not the glyph. "Delete invoice", not "Trash icon".

## States and properties

Design specifies which states exist; the spec names them.

| State | Attribute | Design must decide |
|-------|-----------|--------------------|
| Pressed / toggled | `aria-pressed` | Whether it is a toggle or an action |
| Expanded | `aria-expanded` | What it controls |
| Selected | `aria-selected` | Single or multiple selection |
| Checked | `aria-checked` | Whether an indeterminate state exists |
| Disabled | `disabled` / `aria-disabled` | Whether it should remain focusable and explain itself |
| Current | `aria-current` | Page, step, or location |
| Invalid | `aria-invalid` | When it becomes true, and what describes the error |
| Busy | `aria-busy` | Which region is loading |

Disabled vs `aria-disabled`: a truly disabled control is unreachable and unexplained. Often better is a focusable control that explains why it cannot be used. Decide deliberately.

## Live regions (SC 4.1.3)

Specify what should be announced without moving focus.

| Change | Politeness |
|--------|-----------|
| Search results updated | `polite` |
| Item saved | `polite` |
| Validation error on submit | `assertive`, or move focus to the field |
| Session about to expire | `assertive` |
| Background sync finished | `polite` |
| Progress percentage | `polite`, throttled — do not announce every tick |

Rules:
- The live region exists in the DOM before the content changes; injecting the region and its content together may not announce.
- One `assertive` region at most; overuse makes the product unusable with a screen reader.
- Never use a live region for something focus movement would communicate better.

## Common ARIA mistakes

| Mistake | Correct |
|---------|---------|
| `role="button"` on a `<div>` | Use `<button>` |
| `aria-label` on a non-interactive `<div>` | Labels apply to elements with roles |
| `aria-hidden="true"` on something focusable | Never — it produces a "ghost" tab stop |
| Redundant role (`<nav role="navigation">`) | Drop the role |
| `aria-describedby` pointing at a missing id | Verify every reference |
| `role="presentation"` on a table with data | Only for genuinely layout tables |
| ARIA added to fix a contrast or structure problem | Fix the structure |

**No ARIA is better than bad ARIA.** An incorrect role actively misleads, where a plain element merely under-describes.
