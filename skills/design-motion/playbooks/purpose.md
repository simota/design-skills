<!-- design:guidance -->
# Purpose

Motion earns its place by doing a job. The job constrains values; it does not uniquely determine or ground them.

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

1. Remove the animation — does this lose necessary information or an expressly agreed expressive purpose? If neither, remove it.
2. Compare a shorter version where a prototype exists. State what was observed, not a duration justified by habit.
3. Use measured usage frequency or the brief when assessing cumulative delay; where neither exists, say it is unknown.
4. Does it delay the user's next action? If yes, it must be interruptible or removed.

## Expressive vs functional

Set the restraint level from the direction, and hold it.

| Level | Motion budget | Fits |
|-------|--------------|------|
| Functional | Feedback and orientation without delaying the next action | Professional tools, dense products, high-frequency use |
| Balanced | Adds continuity and selective emphasis where it serves the task | General product UI |
| Expressive | Choreographed entries, staggered reveals, emphasis easing | Marketing, onboarding, consumer moments |

A product may be functional in the app shell and expressive in marketing. State the boundary.

## Frequency and duration

Repeated delay accumulates, but frequency alone fixes no duration ceiling.
A project budget needs its source and conditions. Keep any remaining choice
explicitly `ARBITRARY`, and test the proposed interaction rather than inventing
usage counts or a universal timing limit.

## Anti-patterns

| Pattern | Risk to inspect, not an automatic conformance verdict |
|---------|--------------|
| Scroll-triggered fade-in on body content | Delays reading; the content is why they came |
| Loading animation longer than the load | Motion inventing latency |
| Animating a list on every data refresh | Repeats a story the user already knows |
| Bounce on every button | Emphasis everywhere is emphasis nowhere |
| Parallax hero | Vestibular trigger, low value |
| Auto-advancing carousel | Motion the user did not request and cannot predict |
| Full-page transitions in an app shell | Cost per navigation compounds |
| Animation that must finish before input is accepted | Motion taxing the user |
