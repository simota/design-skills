- **Grade each claim**: `measured` supports only what was actually measured;
  `inspected` is for non-measurable judgement, with its reason and limits;
  `asserted` never supports completion. **A guessed measurable value is `asserted`**, not
  `inspected`. A count, convention or preference alone does not establish a defect
- **The unit is the decision, not the document.** Each promised decision carries
  a grade or is `UNSPECIFIED`; no silent delegation of design choices to build
- **Report `status`**: `DONE` (every promised decision made, every measurable
  claim measured, zero `UNSPECIFIED`) / `PARTIAL` / `BLOCKED` (say what was tried)
- **Classify residuals** as `BLOCKED` / `OUT-OF-SCOPE` / `DEFERRED` / `UNSPECIFIED`
  in `open`; a run holding `Write` also places a `#TODO(agent):` marker in its output.
  At `T0`, name any residual inline without creating a handoff
- **Never omit coverage**: markers against `open`, promised decisions against
  graded ones. Report the sweep at `T1`/`T2`; at `T0` evidence its one decision
  inline. A mismatch forbids `DONE` (`_design/CONTRACT.md`)
