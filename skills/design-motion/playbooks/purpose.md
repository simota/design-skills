<!-- design:guidance -->
# Purpose

Motion earns its place by doing a job. Name the job first; the values follow from it.

## The four jobs

| Job | Question it answers | Typical motion |
|-----|--------------------|----------------|
| Orientation | Where did this come from, where did it go? | Panel slides from the edge it belongs to; modal scales from its trigger |
| Feedback | Did my action register? | Press depression, toggle travel, ripple, button pending state |
| Continuity | What changed, and how does it relate to before? | Shared-element transition, list reorder, expanding row |
| Status | What is happening now? | Progress, skeleton shimmer, sync indicator |

If a proposed animation does not map to one of these, it is decoration. Decoration is allowed only where the direction explicitly calls for expressiveness, and only in moments the user is not trying to work through.

## The removal test

Ask, in order:

1. Remove the animation entirely — is anything now confusing? If no, remove it.
2. Halve the duration — is anything lost? If no, keep the shorter one.
3. State the interaction's per-session frequency and check it against the Frequency table below — animations are designed once and experienced thousands of times, so frequency sets the duration ceiling.
4. Does it delay the user's next action? If yes, it must be interruptible or removed.

## Expressive vs functional

Set the restraint level from the direction, and hold it.

| Level | Motion budget | Fits |
|-------|--------------|------|
| Functional | Feedback and orientation only; ≤200ms typical | Professional tools, dense products, high-frequency use |
| Balanced | Adds continuity transitions; one emphasis moment per flow | General product UI |
| Expressive | Choreographed entries, staggered reveals, emphasis easing | Marketing, onboarding, consumer moments |

A product may be functional in the app shell and expressive in marketing. State the boundary.

## Frequency governs duration

| Frequency | Duration ceiling |
|-----------|-----------------|
| Many times per session (toggles, hovers, rows) | 150ms |
| Several times per session (modals, drawers) | 300ms |
| Once per session (onboarding, first success) | 400ms, expressive permitted |
| Once ever (first-run celebration) | Longer permitted, must be skippable |

## Anti-patterns

| Pattern | Why it fails |
|---------|--------------|
| Scroll-triggered fade-in on body content | Delays reading; the content is why they came |
| Loading animation longer than the load | Motion inventing latency |
| Animating a list on every data refresh | Repeats a story the user already knows |
| Bounce on every button | Emphasis everywhere is emphasis nowhere |
| Parallax hero | Vestibular trigger, low value |
| Auto-advancing carousel | Motion the user did not request and cannot predict |
| Full-page transitions in an app shell | Cost per navigation compounds |
| Animation that must finish before input is accepted | Motion taxing the user |
