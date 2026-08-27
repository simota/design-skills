<!-- design:deferred -->
# Direction Brief Template

Purpose: The brief's required fields, and what a blank one costs.
Read when: starting the brief, or completing it for handoff.
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

The brief is the deliverable. Fill every field; write "n/a — <reason>" rather than leaving a blank.

```markdown
# Design Direction — <product / surface>

## 1. Context
- Product:
- Audience (primary, secondary):
- Surfaces in scope:            e.g. marketing site, app shell, settings
- Surfaces explicitly out:
- Hard constraints:             brand assets, platform, locale coverage, engineering budget
- Existing system:              none | partial | full (link)

## 2. Adjectives
- Must feel:   <3–5 words>
- Must never feel: <2 words>
- One-sentence thesis:

## 3. Directions Considered
| Name | Thesis | Trades away | Verdict |
|------|--------|-------------|---------|
| A —  |        |             | chosen / rejected because … |
| B —  |        |             | |
| C —  |        |             | |

## 4. Chosen Direction
| Layer | Decision | Rationale |
|-------|----------|-----------|
| Voice | | |
| Typography | | |
| Colour | | |
| Composition | | |
| Surface | | |
| Restraint | | |

## 5. Type Spec
| Role | Family | Fallback stack | Weights | Notes |
|------|--------|----------------|---------|-------|
| Display | | | | |
| UI / body | | | | |
| Mono / numeric | | | | |

- Scale ratio and reasoning:
- Minimum body size:
- Licensing status:

## 6. Colour Spec
| Role | Value | On (background) | Contrast | Passes |
|------|-------|-----------------|----------|--------|
| Text primary | | | | AA / AAA |
| Text muted | | | | |
| Accent | | | | |
| Surface / canvas | | | | |
| Border | | | | (3:1 non-text) |

## 7. Composition Spec
- Grid:                 columns, gutter, breakpoints
- Max content width:
- Density:              compact | default | spacious — and why
- Spacing rhythm:       base unit and intended stepping
- Alignment strategy:

## 8. Restraint List
- This direction will not use: …

## 9. Handoff
- To design-tokens:
- To design-ux:
- To design-motion:
- To design-a11y:
- To design-critique:   (what this brief is the standard for)
```

## Required fields

A brief is incomplete without: adjectives, ≥3 considered directions, per-choice rationale, contrast results, and the restraint list. These five are what make it reviewable later by `design-critique`.
