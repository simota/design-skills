<!-- design:guidance -->
# Heuristics

The evaluation set. Run each deliberately; do not stop at the first finding.

## Establishing the standard

Before evaluating, name what the design is judged against, in this order of preference:

1. The design brief from `design-direction` — explicit intent, best standard
2. The project's design system and tokens — measurable consistency
3. The `design-ux` spec — states and flows that were agreed
4. Platform conventions (HIG, Material, web norms)
5. General heuristics (below) — the weakest standard, used when nothing else exists

If only (5) is available, say so. It changes how much weight the findings carry.

## Core heuristics

Nielsen's ten, applied concretely.

| Heuristic | Check | Common failure |
|-----------|-------|----------------|
| Visibility of system status | Does the user always know what is happening? | Silent failures; unbounded spinners; no save indication |
| Match to the real world | Is the language the user's? | Internal jargon; database field names as labels |
| User control and freedom | Can they undo, cancel, or back out? | Irreversible actions with no undo; modals with no cancel |
| Consistency and standards | Same thing, same name, same look? | "Delete" here, "Remove" there; three button styles |
| Error prevention | Is the invalid case impossible? | Free-text where a picker belongs; destructive action as default focus |
| Recognition over recall | Is needed info visible? | An ID to remember across screens; unlabelled icons |
| Flexibility and efficiency | Are frequent tasks fast? | No keyboard path; no bulk action on a list built for bulk work |
| Aesthetic and minimalist design | Does every element earn its place? | Dashboards showing everything, ranking nothing |
| Error recovery | Do errors say what to do? | "Something went wrong"; errors far from their cause |
| Help and documentation | Is help findable in context? | Help only in a separate site; tooltips explaining bad labels |

## Purpose lens

- Can you state the screen's job in one sentence after five seconds?
- Is there exactly one primary action? If two look equal, the screen has two jobs.
- Is the most important information the most visually prominent?
- Would a first-time user know what to do next? Would a hundredth-time user be slowed by anything?

## Content lens

| Check | Fail signal |
|-------|-------------|
| Specificity | "Item saved" where "Invoice INV-104 saved" was available |
| Honesty | Progress bars that do not reflect progress; "instant" that takes 4s |
| Consistency of naming | One concept, several names |
| Voice | Blaming the user; passive constructions in errors |
| Density | Paragraphs where a sentence works; instructions after the field |
| Truncation | Labels that clip in the design's own examples; no plan for long content |
| Localisation | Layouts assuming English length; concatenated sentence fragments |
| Numbers | Unformatted, unrounded, or unit-less values |

## Realistic content check

Designs pass review on ideal content and fail in production. Check against:

- The longest realistic name, title, and address
- A single character, and an empty value
- Zero items, one item, and ten thousand items
- A locale with longer words (German) and one with different script metrics (Japanese, Arabic)
- Right-to-left, if in scope
- Missing avatars, broken images, and absent optional fields
- A user with one permission level lower

Any of these breaking the layout is a finding, not an edge case.

## System drift

Compare what is used against what the system defines.

| Drift | How to spot |
|-------|-------------|
| Off-scale spacing | Values not on the spacing scale (e.g. 13px, 18px, 22px) |
| Off-ramp colours | Hex values not in the palette |
| Ad-hoc type sizes | Sizes outside the type scale |
| Reinvented component | A local implementation of something the system provides |
| Inconsistent radius | Two or three radii on peer elements |
| One-off shadow | An elevation not in the elevation scale |
| Local overrides | `!important`, inline styles, arbitrary utility values |

Record drift in its own table with the used value, the system value, and the count.

## What works

Every report includes this. Name specifically what is right — a clear hierarchy, a well-designed empty state, consistent spacing, a good error message. Unmarked strengths get removed in the next revision by someone who did not know they were deliberate.
