- **Grade every claim**: `measured` (a value read off the artifact) supports
  completion; `inspected` (read and reasoned over) only where nothing can be
  measured and the entry says why; `asserted` never does. **Estimating a
  measurable value is `asserted`** — contrast, target size, scale ratios and
  token coverage are all countable
- **The unit is the decision, not the document.** Each decision the deliverable
  promised carries a grade or sits in the residuals as `UNSPECIFIED`, and a
  decision in neither is what gets invented at build time by whoever hits it first
- **Report `status`**: `DONE` (every promised decision made, every measurable
  claim measured, zero `UNSPECIFIED`) / `PARTIAL` / `BLOCKED` (say what was tried)
- **Every residual is `BLOCKED` / `OUT-OF-SCOPE` / `DEFERRED` / `UNSPECIFIED`**
  and appears in the handoff's `open`; a run holding `Write` also leaves a
  `#TODO(agent):` marker carrying that class in the document it produced
- **Never omit the sweep** — markers against `open`, promised decisions against
  graded ones: `swept, 0 markers; 18 decisions / 18 graded`. While either pair
  disagrees the status is not `DONE` (`_design/CONTRACT.md`)
