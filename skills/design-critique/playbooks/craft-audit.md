<!-- design:guidance -->
# Craft Audit

Inspect the artifact, then classify the claim. A measurable property is not
necessarily a measurable defect. These lenses do not create product requirements.

## What the evidence supports

| Kind | Required basis | Treatment |
|---|---|---|
| Measurable defect | Observed functional failure or a measured violation of an applicable requirement | `defect`; name the failure, source and conditions |
| System inconsistency | Actual departure from an adopted token, component or documented convention | `inconsistency`; cite the system and check deliberate exceptions |
| Conformance question | A suspected accessibility failure with its available evidence | Flag for `design-a11y`; it adjudicates the applicable criterion and exceptions |
| Defensible judgement | Concrete observation, task or intent, reasoning and trade-off | `judgement`, `inspected`; naming a heuristic does not turn it into a defect |
| Pure taste | Preference with no product-specific basis | Label taste; do not rank it as a defect or require its preferred replacement |

No adopted system? Use the judgement lens without inventing one. A numerical
difference becomes an inconsistency only when the system requires agreement.
The evidence for a problem and the ground of a proposed replacement are separate.

## Craft lenses

| Area | Measure or inspect | Boundary to respect |
|---|---|---|
| Alignment | Actual positions, baselines and adopted grid; visible offsets | Optical centring is judgement unless a required alignment is demonstrably broken |
| Spacing | Resolved values, off-system sites, grouping of related content | Symmetry, tighter grouping and regular rhythm are not universal requirements |
| Typography | Resolved family, size, weight, line height; clipping with real content | Line length, weight count, tracking and heading wraps depend on script, typeface and task |
| Colour | Actual source pairs and role mappings in each in-scope theme | Contrast adjudication belongs to `design-a11y`; hue preference and ramp evenness are not conformance |
| Composition and density | What competes or groups in the observed view, against the intended task | Dense comparison tools need not become sparse; "clean", "modern" and "premium" are not defect classes |
| Surfaces | Adopted radii, shadows, borders and layering; visible occlusion | Concentric corners and stronger shadows on higher layers are choices, not universal geometry rules |
| Icons | Adopted library conventions, accessible purpose and actual rendering | Mixed sources or optical sizes alone do not prove a defect |
| Responsive behaviour | Real content, in-scope viewports, zoom and input modes | Do not infer behaviour at unobserved sizes or turn a screenshot's image pixels into CSS dimensions |

Record the property, actual values, source location, relevant system definition
and site count before judging. Count only what was inspected; do not invent a
coverage percentage. A missing source means the measurement is unavailable.

## Screenshot-only work

Actual image-pixel measurements and visible counts may be `measured`, scoped to
that image and method. They do not establish computed CSS, true contrast pairs,
keyboard operation, motion, other themes or other viewports.

A guessed spacing, size or ratio is `asserted`, not `inspected`. Request the
source or mark the numerical question not assessable. A qualitative grouping or
hierarchy concern can still be `inspected` when its observation and reasoning
are stated. Do not pad it with invented numbers.

## State and accessibility checks

For applicable states, inspect feedback, recovery, retained input, exits and
partial failure. Missing promised behaviour is `UNSPECIFIED`; enumerate it and
route design decisions to `design-ux`. Passive screens need not gain actions,
and a spinner is not defective merely because a skeleton is another option.

Raise observed or suspected accessibility concerns with their evidence, then
hand conformance to `design-a11y`. It checks the criterion, level, applicability
and exceptions. Do not maintain a second threshold table here or call an
unavailable build-time test a pass.

## Reporting

Use the existing finding classes, severity by supported user impact, evidence,
and an owner. Preserve useful strengths. A judgement remains open to disagreement;
pure taste does not enter a defect-closing loop as a release blocker.
