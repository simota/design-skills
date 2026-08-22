<!-- design:guidance -->
# Information Architecture

Structure decides whether a product feels simple. Styling cannot rescue bad structure.

## Navigation models

| Model | Fits | Breaks when |
|-------|------|-------------|
| Flat top nav | ≤7 top-level areas | Sections multiply; overflow menus appear |
| Sidebar | Tools with many equal-weight areas | Depth exceeds two levels |
| Sidebar + sections | Large tools, workspace products | Section names are not user language |
| Tabs (in-page) | Peer views of one object | Views are not peers, or state is lost on switch |
| Master–detail | Lists whose items are inspected | Detail is heavy enough to deserve its own page |
| Hub and spoke | Task-oriented mobile | Users need to move laterally between spokes |
| Command palette (secondary) | Power users, deep feature sets | Used as the *only* discovery mechanism |

Rules:
- Depth over breadth costs clicks; breadth over depth costs scanning. Prefer breadth up to ~7 items, then group.
- A navigation label is a user's word, not an internal team name.
- Never make the current location ambiguous — the active state must be unmistakable.
- Search complements navigation; it does not replace it. Users who cannot browse cannot learn what exists.

## Grouping

Group by the user's mental model, not the org chart or the database schema. When unsure, run a card sort — or at minimum, name each group and ask whether a new user could predict its contents.

| Signal | Grouping is wrong |
|--------|--------------------|
| A group named "Other" or "More" | The taxonomy does not cover reality |
| A frequently-used item buried three levels deep | Frequency was ignored |
| Two groups whose names could each contain the same item | Groups overlap |
| A group with one item | Not a group |
| A group with 15 items | Needs sub-structure or ranking |

## Hierarchy on a screen

Three levels, expressed with the strongest available signal first:

1. **Position** — top-left in LTR reading order carries most weight
2. **Size** — relative scale, before colour
3. **Weight** — type weight and density
4. **Colour** — last, and never alone

One primary action per screen. Secondary actions get a lighter treatment; tertiary actions go into an overflow. If three actions look equally important, the user reads none of them as important.

## Progressive disclosure

| Technique | Use when | Cost |
|-----------|----------|------|
| Default + "Advanced" | Most users need the default | Advanced settings get missed |
| Accordion | Long forms, settings pages | Hides scannability; never nest accordions |
| Inline expand | Row detail in a list | Shifts layout below |
| Drawer / side panel | Detail without losing list context | Competes with modals |
| Separate page | Detail is substantial or deep-linkable | Loses context; needs breadcrumbs |
| Modal | A short, focused, interrupting task | Never for anything with its own sub-flow |

Modal rules: one at a time, Escape always closes, focus trapped inside, focus returns to the trigger on close, and never for a task requiring another modal or a long form.

## Density

Density is a direction decision (`design-direction`) with structural consequences here.

| Density | Row height | Fits |
|---------|-----------|------|
| Compact | 32–36px | Professional tools, data grids, users who live in the screen |
| Default | 40–48px | General product UI |
| Spacious | 56px+ | Consumer, occasional-use, touch-first |

Offer a density toggle only when the same product genuinely serves both scanning and reading modes. Otherwise it is a decision the design is avoiding.

## Lists and tables

- Decide the default sort and say why. "Most recently modified" is right more often than alphabetical.
- Show total count. A list of unknown length cannot be reasoned about.
- Pagination for stable, referenceable positions; infinite scroll only for exploratory feeds — never for anything users must return to, and never above a footer.
- Bulk selection needs: select-all-on-page vs select-all-matching disambiguated, a visible count, and an obvious clear.
- Column choices are content decisions: show what users scan for, not every field the API returns.

## Search and filter

- Filters are visible after application (chips), and clearable individually and all at once.
- Filter state belongs in the URL, so results are shareable and survive refresh.
- Empty results state names the filters that caused it (see `playbooks/state-matrix.md`).
- Search scope must be stated when it is not the whole product.
