<!-- design:deferred -->
# Interaction Spec Template

Purpose: The interaction spec's required sections, and who downstream consumes which.
Read when: writing the deliverable, or checking one for completeness.
Verified: 2026-08-21 — no automated check.

The `SPEC` phase deliverable. `design-critique` judges the built UI against this, and `design-a11y` consumes sections 6–7 — so the shape must be stable run to run. Fill every field; write "n/a — <reason>" rather than leaving a blank.

```markdown
# Interaction Spec — <flow / screen>

## 1. Goal
- User:
- Job (the task, not the feature):
- Context:            where they are, what else is happening
- Frequency:          once ever | occasional | many times per session
- Success condition:  how we know the job is done

## 2. Flow
```mermaid
flowchart TD
    A[Entry] --> B{Decision}
    B -->|yes| C[Step]
    B -->|no|  D[Alternative]
    C --> E{Server}
    E -->|success| F[Success state]
    E -->|expected failure| G[Recoverable error]
    E -->|unexpected| H[Generic error, input preserved]
```
Every network call needs three exits: success, expected failure, unexpected failure.

## 3. Screens
| Screen | Job (one sentence) | Primary action | Exits |
|--------|--------------------|----------------|-------|
| | | | cancel / back / abandon |

## 4. State Matrix — one table per screen
| State | Condition | Content | Primary action | Focus goes to | Notes |
|-------|-----------|---------|----------------|---------------|-------|
| Empty (first) | | | | | |
| Empty (filtered) | | | | | distinct from first use |
| Loading (initial) | | | — | | skeleton after Nms |
| Loading (refresh) | | | — | | old content retained |
| Partial | | | | | |
| Error (recoverable) | | | | | input preserved |
| Error (permission) | | | | | |
| Offline | | | | | |
| Success | | | | | |
| Destructive pending | | | | | undo window: Ns |

## 5. Field Spec — one row per input
| Field | Type | Required | Constraint | Default | Validate | Error copy | autocomplete / inputmode |
|-------|------|----------|-----------|---------|----------|------------|--------------------------|
| | | | | | on blur / live / submit | | |

## 6. Interaction
- Focus destination per transition: (modal open/close, step change, submit failure, item deleted, route change)
- Escape paths: what Escape, Back, and browser refresh each do
- Flow-level shortcuts:
- Preserved across navigation: scroll position, filters, expanded rows, unsent input

Per-component keyboard maps and APG conformance are `design-a11y`'s, not this section's.

## 7. Latency Plan
| Action | Expected | <100ms | 100ms–1s | 1–10s | >10s | Timeout → |
|--------|----------|--------|----------|-------|------|-----------|
| | | no indicator | inline on control | skeleton | progress + cancel | named error state |

## 8. Open Questions
| Question | Recommended default | Blocks? |
|----------|--------------------|---------|
| | | yes / no |

## 9. Handoff
- To design-motion:   transitions this flow needs
- To design-a11y:     focus destinations, live-region announcements
- To design-critique: this document, as the standard
```

## Completeness gate

The spec is not done until: every screen has a filled state matrix, every async action appears in the latency plan, every failure branch names where focus lands and confirms input is preserved, and every open question carries a recommended default. `Implementable without asking` means an implementer reading only this document raises no question it does not answer.
