<!-- design:guidance -->
# Cognitive Load

When a screen feels heavy, the fix is usually structural, not visual.

## Diagnose the load type

| Type | Symptom | Fix |
|------|---------|-----|
| Intrinsic | The task is genuinely complex | Decompose into steps; cannot be styled away |
| Extraneous | Effort spent on the interface, not the task | Remove — this is the design's fault |
| Germane | Effort spent learning the model | Support with consistency and good naming |

Only extraneous load should be attacked directly. Reducing intrinsic load means changing the task.

## Sources of extraneous load

| Source | Fix |
|--------|-----|
| Too many equal-weight elements | Establish hierarchy; demote all but one |
| Inconsistent patterns across screens | Unify — every deviation is re-learning |
| Jargon and internal naming | Use the user's words |
| Information the user must hold in memory across screens | Carry it forward and display it |
| Ambiguous icons without labels | Label them; icon-only is for a handful of universal symbols |
| Options presented before they matter | Defer |
| Values the user must calculate | Calculate them |
| Similar-looking things that behave differently | Differentiate visually, or unify behaviour |
| Layout that shifts as content loads | Reserve space |

## Reduction, in order

1. **Remove** — does this element earn its place? Most do not.
2. **Defer** — must it be here *now*?
3. **Default** — can it be decided for the user?
4. **Group** — chunk into 3–5 meaningful clusters.
5. **Rank** — make the important thing visibly more important.
6. **Only then, restyle.**

## Recognition over recall

- Show, do not make them remember. Carry selections forward; display the object being acted on inside the confirmation.
- Recently-used and frequently-used surfaces beat search for repeat tasks.
- Keep the user's place: preserve scroll position, filter state, and expanded rows across navigation.
- Never require the user to remember an ID, code, or value from a previous screen.

## Naming

Naming is load reduction. A wrong label costs more than a wrong colour.

- Use the term the user uses, verified in their words if research exists.
- One concept, one name — everywhere, including errors and docs.
- Verbs for actions, nouns for objects. "Export" not "Exportation"; "Reports" not "Reporting".
- Avoid words that mean nothing specific: Manage, Settings-within-Settings, Tools, Misc, Other.

## Scan patterns

- Users scan headings, bold text, links, and the first two words of a line.
- Front-load meaning: "Delete workspace — removes all 12 projects" beats "This action will remove…".
- Short lines outperform paragraphs for interface text.
- Alignment creates scan paths; inconsistent left edges destroy them.

## Measuring it

If analytics exist, load shows up as: time-on-task rising, backtracking between screens, repeated opening of help, abandonment concentrated on one step, and support questions clustering around one label. Ask for that data before redesigning on intuition.

## Anti-patterns

- Adding a tooltip to explain a confusing label instead of fixing the label.
- Adding an onboarding tour to explain a confusing screen instead of fixing the screen.
- Hiding complexity behind "Advanced" without deciding whether it should exist.
- A dashboard showing everything, prioritising nothing.
- Empty states that explain the feature at the moment the user is trying to use it, rather than the interface being self-evident.
