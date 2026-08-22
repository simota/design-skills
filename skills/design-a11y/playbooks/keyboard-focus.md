<!-- design:guidance -->
# Keyboard and Focus

Keyboard operation is a design specification, not an implementation detail.

## Focus order (SC 2.4.3)

- Focus follows the visual reading order. If the two disagree, the layout is wrong, not the tab order.
- Specify the order explicitly per screen. Ambiguity here becomes a defect.
- Never use a positive `tabindex`; it creates an order nobody can maintain.
- Skip links come first on pages with repeated navigation.
- Elements that are visually hidden must also be removed from the tab order.

Specify the destination for every state change:

| Event | Focus goes to |
|-------|---------------|
| Modal opens | The modal — its first focusable element, or the dialog container |
| Modal closes | The element that opened it |
| Drawer opens / closes | Same rule as modal |
| Step advances | The new step's heading |
| Form submit fails | The first errored field |
| Item deleted from a list | The next item, or the list container if empty |
| Content loads into a region | Stays put; announce via a live region instead (SC 4.1.3) |
| Route change (SPA) | The new page's `<h1>` or main landmark |

## Focus visibility (SC 2.4.7, 1.4.11, 2.4.11)

Requirements:
- Always visible on keyboard focus. Never `outline: none` without a replacement.
- At least 3:1 against adjacent colours (SC 1.4.11).
- Not entirely obscured by sticky headers, footers, or overlays (SC 2.4.11 AA).
- AAA target (SC 2.4.13): at least a 2px perimeter and 3:1 against the unfocused state.

Design shape that works on any surface:

```css
:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
  border-radius: inherit;
}
```

The offset creates a gap so the ring reads against both the element and the background. On coloured surfaces, add a contrasting inner ring (`box-shadow: 0 0 0 2px var(--color-bg-canvas)`) so it is visible against both.

Use `:focus-visible`, not `:focus`, so mouse users do not see rings — but verify the browser's heuristic covers your custom widgets.

Sticky headers: give focusable content `scroll-margin-top` equal to the header height plus a little, or SC 2.4.11 fails on every scrolled-into-view focus.

## Keyboard models

Specify keys per component. Follow the WAI-ARIA Authoring Practices Guide rather than inventing.

| Component | Keys |
|-----------|------|
| Button | Enter, Space |
| Link | Enter |
| Checkbox | Space |
| Radio group | Arrows move and select; Tab enters/leaves the group as one stop |
| Select / listbox | Arrows, Home/End, type-ahead, Enter, Escape |
| Combobox | Arrows open and move, Enter selects, Escape closes then clears |
| Tabs | Arrows move between tabs; Tab moves into the panel |
| Menu / menubar | Arrows, Home/End, Escape, type-ahead |
| Dialog | Escape closes; focus trapped inside while open |
| Tree | Arrows navigate, Right/Left expand/collapse |
| Data grid | Arrows move cell to cell; Tab leaves the grid |
| Slider | Arrows step, Home/End to bounds, PageUp/Down for larger steps |
| Disclosure | Enter/Space toggles |

Rules:
- A composite widget is one tab stop; arrows move within it. Making every cell or tab a tab stop makes the component unusable.
- Escape always cancels the most recent layer.
- Single-character shortcuts must be remappable or only active when a component has focus (SC 2.1.4).

## Focus traps

Legitimate in exactly one place: a modal dialog, which must be escapable via Escape and via a visible close control. Everything else that traps focus is a defect (SC 2.1.2).

Check specifically: embedded media players, third-party widgets, iframes, and custom editors.

## Target size (SC 2.5.8 AA)

Minimum 24×24 CSS px, **or** 24px of spacing between adjacent target centres.

| Exception | Applies when |
|-----------|--------------|
| Spacing | Targets are ≥24px apart |
| Inline | The target is inside a sentence or text block |
| Essential | The size is legally required or essential to the information (e.g. a map pin) |
| User agent control | Size is browser-determined and unstyled |
| Equivalent | The same function is available at a conforming size elsewhere |

Practical guidance beyond AA: 44×44 CSS px for touch (matching iOS HIG); Material recommends 48×48 dp. The *visual* control may be smaller — enlarge the hit area with padding or a pseudo-element instead of growing the icon.

Adjacent targets must not overlap. Table row action icons at 20px, 4px apart, is the single most common 2.5.8 failure.

## Pointer and gesture (SC 2.5.1, 2.5.7)

| Requirement | Design implication |
|-------------|--------------------|
| Path-based gestures need an alternative | A swipe-to-delete row also needs a visible delete action |
| Multipoint gestures need an alternative | Pinch-zoom on a map needs +/− buttons |
| Dragging needs a non-drag alternative (2.5.7 AA) | Drag-to-reorder also needs "Move up/Move down" or a position field |
| Down-event actuation | Actions fire on up-event, so a mispress can be aborted by moving off |
| Motion actuation needs an alternative (2.5.4) | Shake-to-undo also needs an undo control |

## Testing

1. Unplug the mouse. Complete each primary task.
2. Tab through every screen; confirm order matches reading order and focus is always visible.
3. Scroll so a focused element sits under a sticky header; confirm it is not hidden.
4. Open and close every overlay; confirm focus returns to its trigger.
5. Zoom text to 200% and the page to 400% at 320px width; confirm nothing is lost.
6. Run a screen reader through one full flow — VoiceOver (macOS/iOS), NVDA (Windows), TalkBack (Android).
