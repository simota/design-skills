<!-- design:deferred -->
# WCAG 2.2 — Design-Relevant Checklist

Purpose: The success criteria a designer can pass or fail before code exists.
Read when: running conformance against the standard, or citing a criterion in a finding.
Source: WCAG 2.2 — the success criteria below are quoted from that version.
Verified: 2026-08-21 — no automated check.

The success criteria a designer can pass or fail *before* code exists. Cite the number and level in every finding.

## Perceivable

| SC | Level | Design decision |
|----|-------|-----------------|
| 1.1.1 Non-text Content | A | Every image, icon, and chart has an intended alt text or is marked decorative |
| 1.3.1 Info and Relationships | A | Headings, lists, tables, and groups are structural, not just visually styled |
| 1.3.2 Meaningful Sequence | A | Visual order matches reading order |
| 1.3.4 Orientation | AA | Works in both portrait and landscape unless essential |
| 1.3.5 Identify Input Purpose | AA | Fields declare their purpose (`autocomplete` tokens) |
| 1.4.1 Use of Color | A | No meaning carried by colour alone |
| 1.4.3 Contrast (Minimum) | AA | 4.5:1 body, 3:1 large text |
| 1.4.4 Resize Text | AA | Usable at 200% text zoom without loss |
| 1.4.10 Reflow | AA | No horizontal scroll at 320px width / 400% zoom (except data tables, maps, code) |
| 1.4.11 Non-text Contrast | AA | 3:1 for control boundaries, states, meaningful icons, focus indicators |
| 1.4.12 Text Spacing | AA | Survives line-height 1.5×, paragraph spacing 2×, letter 0.12em, word 0.16em |
| 1.4.13 Content on Hover or Focus | AA | Hover/focus content is dismissible, hoverable, and persistent |

## Operable

| SC | Level | Design decision |
|----|-------|-----------------|
| 2.1.1 Keyboard | A | Every function is keyboard-operable |
| 2.1.2 No Keyboard Trap | A | Focus can always leave |
| 2.1.4 Character Key Shortcuts | A | Single-character shortcuts are remappable or focus-scoped |
| 2.2.1 Timing Adjustable | A | Time limits can be extended or turned off |
| 2.2.2 Pause, Stop, Hide | A | Motion or auto-update over 5s can be paused |
| 2.3.1 Three Flashes | A | Nothing flashes more than 3×/second |
| 2.3.3 Animation from Interactions | AAA | Non-essential motion can be disabled |
| 2.4.3 Focus Order | A | Focus follows a meaningful sequence |
| 2.4.6 Headings and Labels | AA | Headings and labels describe topic or purpose |
| 2.4.7 Focus Visible | AA | Keyboard focus is always visible |
| 2.4.11 Focus Not Obscured (Min) | AA | The focused element is not entirely hidden by other content |
| 2.4.12 Focus Not Obscured (Enh) | AAA | The focused element is not obscured at all |
| 2.4.13 Focus Appearance | AAA | Indicator ≥2px perimeter and ≥3:1 against the unfocused state |
| 2.5.1 Pointer Gestures | A | Multipoint or path gestures have a single-pointer alternative |
| 2.5.3 Label in Name | A | The visible label is contained in the accessible name |
| 2.5.4 Motion Actuation | A | Device-motion actions have a UI alternative |
| 2.5.7 Dragging Movements | AA | Drag operations have a non-drag alternative |
| 2.5.8 Target Size (Minimum) | AA | 24×24 CSS px, or equivalent spacing |

## Understandable

| SC | Level | Design decision |
|----|-------|-----------------|
| 3.1.1 Language of Page | A | Page language declared |
| 3.2.1 On Focus | A | Focus alone does not change context |
| 3.2.2 On Input | A | Changing a value alone does not change context |
| 3.2.3 Consistent Navigation | AA | Navigation stays in the same relative order |
| 3.2.4 Consistent Identification | AA | The same function is named the same everywhere |
| 3.2.6 Consistent Help | A | Help appears in a consistent relative position |
| 3.3.1 Error Identification | A | Errors are identified in text |
| 3.3.2 Labels or Instructions | A | Inputs have visible labels or instructions |
| 3.3.3 Error Suggestion | AA | Errors say how to fix, where known |
| 3.3.4 Error Prevention | AA | Legal, financial, and data actions are reversible, checked, or confirmed |
| 3.3.7 Redundant Entry | A | Already-entered info is auto-filled or selectable |
| 3.3.8 Accessible Authentication (Min) | AA | No cognitive function test without an alternative; paste must work |

## Robust

| SC | Level | Design decision |
|----|-------|-----------------|
| 4.1.2 Name, Role, Value | A | Every control's name, role, and state are specified |
| 4.1.3 Status Messages | AA | Status changes are announced without moving focus |

SC 4.1.1 Parsing was removed in WCAG 2.2.

## Report format

| SC | Level | Severity | Location | Fails because | Design-level fix |
|----|-------|----------|----------|---------------|------------------|
| 1.4.3 | AA | Serious | Settings → muted labels | `#9aa0a6` on `#ffffff` = 2.64:1 | Muted text must reach 4.5:1 on canvas; `#6b7280` (4.83:1) clears it. Hand the value to `design-tokens` to apply. |
| 2.4.11 | AA | Serious | Any page with sticky header | Focused row scrolls under the 64px header | Add `scroll-margin-top: 72px` to focusable rows |
| 2.5.8 | AA | Moderate | Table row action icons | 20×20 hit area, 4px apart | Enlarge hit area to 24×24 and space 8px; visual icon may stay 20px |

## Beyond the checklist

Passing every SC does not make a design usable. Also check: is the reading order sensible without vision, is the keyboard path short for frequent tasks, are error recoveries reachable, and does the product work at 320px with 200% text. Conformance is a floor.
