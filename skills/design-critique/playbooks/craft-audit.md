<!-- design:guidance -->
# Craft Audit

The measurable layer. Findings here are evidenced by values, not impressions.

## Alignment

| Check | Failure |
|-------|---------|
| Shared left edge | Elements in a column starting at 16px, 17px, and 20px |
| Optical vs geometric | Icons centred geometrically that read off-centre; circles and triangles need optical adjustment |
| Baseline alignment | Text and icons in a row sitting on different baselines |
| Grid adherence | Elements off the column grid without a reason |
| Edge consistency | Card content insets differing across peer cards |

## Spacing rhythm

- Spacing values should come from the scale. List every off-scale value found, with its count.
- Related elements sit closer than unrelated ones. If the gap above a label equals the gap below it, the grouping is ambiguous.
- Vertical rhythm should be consistent between peer sections.
- Padding is symmetric unless there is a stated optical reason.
- Nested radii: inner radius should equal outer minus padding, or the corners read wrong.

## Typography detail

| Check | Failure |
|-------|---------|
| Scale adherence | Sizes off the type scale |
| Line length | Body copy beyond ~75 characters, or UI text below ~45 |
| Line height | Same value across very different sizes |
| Weight range | More than three or four weights in use |
| Synthetic styling | Faux bold or faux italic on a family lacking the cut |
| Tracking | Display sizes at default tracking, reading loose |
| Orphans and widows | A single word on the last line of a heading |
| Numerals | Proportional figures in a table column that should be tabular |
| Case | ALL CAPS in long strings; small-caps faked by scaling |

## Colour and contrast

- Every text pair measured (hand off to `design-a11y` for adjudication).
- Semantic colours consistently applied — danger never used for emphasis.
- Neutral ramp perceptually even; no step that jumps.
- Accent used for one job.
- Both themes checked independently.

## Elevation and depth

- Shadow values from the scale, not one-offs.
- Elevation is consistent with the z-order: a higher layer never has a lighter shadow.
- In dark themes, elevation reads via surface lightness or borders, not shadow alone.
- Borders and shadows are not both doing the same job on one element.

## Iconography

- Consistent stroke width, corner radius, and grid across the set.
- Consistent optical size — a 24px circle icon reads larger than a 24px square one.
- Meaningful icons reach 3:1 contrast.
- Icon-only controls have labels or tooltips.
- Mixed icon libraries in one interface is a finding.

## Responsive and zoom

| Test | Check |
|------|-------|
| 320px width | No horizontal scroll (SC 1.4.10); nothing clipped |
| 400% browser zoom | Content reflows rather than scrolling in two directions |
| 200% text zoom | No clipping or overlap (SC 1.4.4) |
| Text spacing override | Survives line-height 1.5×, letter 0.12em, word 0.16em (SC 1.4.12) |
| Landscape phone | Usable; modals not taller than the viewport |
| Very wide | Content does not stretch to unreadable line lengths |
| Touch vs pointer | Hover-only affordances have a touch equivalent |

## Inventory method

Record before judging. A table of observed values makes drift undeniable.

| Property | Values observed | System defines | Off-system count |
|----------|-----------------|----------------|------------------|
| Card padding | 16, 20, 24 | 16, 24 | 1 (20px, 3 sites) |
| Border radius | 4, 6, 8, 12 | 4, 8, 12 | 1 (6px, 2 sites) |
| Text sizes | 12, 13, 14, 16, 20 | 12, 14, 16, 19, 23 | 2 (13px, 20px) |
| Greys | 6 distinct | 4 in ramp | 2 |
| Shadows | 4 distinct | 3 in scale | 1 |

From a live UI, gather this with DevTools or by scanning the stylesheet; from a mockup, by inspecting the source file. If you cannot measure, say the finding is visual-only and mark it a `judgement`.

## State checks

Standalone list — sufficient without `design-ux` installed. Hand off to it when it is available.

| State | Fails when |
|-------|-----------|
| Empty (first use) | Absent, or a bare "No data" with no explanation and no action |
| Empty (filtered) | Not distinguished from first use; no way to clear the filter |
| Loading (initial) | Spinner where a skeleton belongs; layout jumps when content arrives |
| Loading (refresh) | Existing content blanked while refetching |
| Partial | One failed region blanks the whole screen |
| Error | Generic text; no cause, no next action; user input discarded |
| Permission denied | Rendered as a generic error; no route to request access |
| Offline | Undefined, or a blocking modal |
| Success | Generic ("Saved") where the specific object was available |
| Destructive pending | No undo, or an undo window with no stated duration |

## Accessibility checks

Standalone list — enough to raise a finding without `design-a11y` installed. Route anything found to it for adjudication; it owns the SC-level verdict.

| Check | Threshold |
|-------|-----------|
| Body text contrast | 4.5:1 (SC 1.4.3 AA) |
| Large text (≥24px, or ≥18.66px bold) | 3:1 |
| Control boundaries, meaningful icons, focus ring | 3:1 (SC 1.4.11 AA) |
| Colour independence | Every meaning carried by colour has a second channel (SC 1.4.1 A) |
| Focus visible | Every interactive element has a designed focus state (SC 2.4.7 AA) |
| Focus not obscured | Focused element not hidden behind sticky headers (SC 2.4.11 AA) |
| Target size | 24×24 CSS px, or 24px spacing (SC 2.5.8 AA) |
| Labels | Every input has a visible label; placeholder is not the label (SC 3.3.2 A) |
| Reflow | No horizontal scroll at 320px / 400% zoom (SC 1.4.10 AA) |

Compute contrast, never estimate it: convert each channel to linear (`c/12.92` if `c<=0.04045`, else `((c+0.055)/1.055)^2.4`), take `L = 0.2126R + 0.7152G + 0.0722B`, then `(L_light+0.05)/(L_dark+0.05)`. Record both source values beside the result.

## Detail checks

Fast checks that catch a surprising amount:

- [ ] Focus states designed for every interactive element
- [ ] Hover states not the only affordance
- [ ] Disabled states visually distinct and explained
- [ ] Loading states present and layout-stable
- [ ] Long content truncation designed (with the full value reachable)
- [ ] Images have defined aspect ratios so layout does not shift
- [ ] Scrollable regions have visible boundaries
- [ ] Sticky elements do not obscure focused content
- [ ] Nothing depends on a hover to be discoverable
- [ ] The design shows real content, not lorem ipsum
