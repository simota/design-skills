<!-- design:deferred -->
# Motion Patterns

Purpose: Concrete transition specifications: trigger, properties, values, interrupt, reduced variant.
Read when: specifying a named transition rather than inventing one.
Source: none — nothing outside this page can move what it states.
Verified: 2026-09-17 — reviewed the example/requirement boundary; no automated check.

Illustrative specifications, not universal defaults. Their literal choices are
`ARBITRARY` when copied without an independent ground. Adapt and explicitly settle
trigger, properties, concrete values, interruption and reduced behaviour; static
feedback is allowed. UX owns the underlying states and feedback semantics.

## Spec format

| Field | Example |
|-------|---------|
| Trigger | User clicks "New project" |
| Target | Modal panel + backdrop |
| Properties | `transform: translateY / scale`, `opacity` |
| Enter | 300ms `ease-out` |
| Exit | 200ms `ease-in` |
| Interrupt | Reverse from current position; never restart |
| Reduced | Opacity only, 100ms |
| Focus | Moves to modal on open, returns to trigger on close |

## Overlays

### Modal / dialog
- Backdrop: `opacity` 0→1, 200ms `ease-out`.
- Panel: `opacity` 0→1 and `scale` 0.97→1 with `translateY` 8px→0, 300ms `ease-out`.
- Exit: reverse, 200ms `ease-in`.
- Prefer sizing the panel before it appears; a purposeful resize needs a measured layout-cost check on a running artifact.
- Focus moves in on open, returns to the trigger on close. Escape closes at any point during the animation.

### Drawer / sheet
- `translateX` (or `translateY` for bottom sheets) from the edge it belongs to, 300ms `ease-out`.
- For a fixed-edge sheet, use its anchored edge on entry and exit. Other navigation models may require different paths.
- Gesture-driven drawers follow the finger 1:1, then complete with velocity-matched motion on release.

### Dropdown / popover
- `opacity` 0→1, `scale` 0.96→1, `translateY` 4px→0, 150ms `ease-out`.
- `transform-origin` set toward the trigger, so it appears to grow from it.
- Exit 100ms `ease-in`, or instant if another dropdown opens immediately.

### Tooltip
- `opacity` only, 75ms, with a 400–600ms open delay and ~100ms close delay.
- No delay when moving between adjacent tooltips in the same group.

## In-place changes

### Accordion / expand
- Height is the honest property but is layout-triggering. Use `grid-template-rows: 0fr → 1fr` (with `overflow: hidden`), or measure and animate `max-height` for short content.
- 200ms `ease-out` in, 150ms `ease-in` out.
- Content `opacity` fades slightly behind the height change (~50ms delay in, none out).

### Tab switch
- Content cross-fades, 150ms. The indicator slides, 200ms `ease-in-out`.
- Do not slide panel content horizontally unless the tabs are genuinely spatial (a carousel of peers).

### List add / remove / reorder
- Add: `opacity` 0→1 and `translateY` −8px→0, 200ms `ease-out`.
- Remove: `opacity` 1→0 and height collapse, 150ms `ease-in`.
- Reorder: FLIP — measure first and last positions, animate the delta with `transform`, 250ms `ease-in-out`.
- On a bulk data refresh, do not animate. The user did not cause each change and does not need to watch it.

### Optimistic update
- Apply the change instantly at 100% opacity; mark pending with a subtle inline indicator, not reduced opacity of the whole row.
- On failure, revert with a 150ms cross-fade plus an inline error. Never silently.

## Feedback

### Press
- `scale` 0.97, 75ms. Release returns over 150ms `ease-out`.
- Touch targets get the press state on `pointerdown`, not on `click`.

### Toggle / switch
- Thumb `translateX`, 150ms `ease-out`. Track colour over the same duration.
- Compare coordinated thumb and colour changes; simultaneity is not inherently a defect.

### Success confirmation
- One `emphasis`-eased moment, ≤400ms, then settle. Checkmark draw or scale-in.
- Once per action, never looping.

### Error shake
- ±4px `translateX`, 3 oscillations, 300ms total.
- Only for input rejection where the field stays put. Never for a page-level error.
- Removed entirely under reduced motion — replaced by a static error style plus focus.

## Loading

### Skeleton
- Shape must match the eventual content, or the layout jumps.
- Shimmer: `translateX` on a gradient overlay, 1.5s `linear`, low contrast.
- Appears only after ~150ms of pending, so fast responses do not flash.
- Under reduced motion: static neutral blocks, no shimmer.

### Spinner
- The loop above is an illustrative choice, not a wait-duration requirement.
- UX owns the waiting state. Elapsed time does not make unknown progress measurable;
  show a percentage only when actual progress data supports it.

### Progress
- Present actual progress, which need not advance uniformly with time.
- Do not hide a correction or rollback to preserve an animation. Reflect the state
  and explain it; motion must not fabricate completion or a percentage.

## Gestures

| Gesture | Response |
|---------|----------|
| Drag | 1:1 with the finger, no easing while held |
| Release | Velocity-matched completion; a spring on native, ~250ms `ease-out` on web |
| Swipe to dismiss | Threshold ~40% of travel or a velocity cut-off; below it, snap back |
| Pull to refresh | Resistance curve so travel decelerates; a clear commit threshold |
| Rubber-band | Resistance at bounds, snap back 300ms `ease-out` |

Gesture-driven motion must be reversible mid-gesture. If the user changes their mind at 60% travel, the element follows back.

## Route transitions

- In an app shell, prefer no route transition. The cost is paid on every navigation.
- Where used: cross-fade 150ms, or a shared-element transition when a specific object persists across the two views.
- Choose a path that matches the actual navigation model; lateral peers can be spatial without implying a parent/child hierarchy.
