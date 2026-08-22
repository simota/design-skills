<!-- design:contract -->
# PROVENANCE — where every value came from

Binding on every `design-*` skill. A design deliverable is a set of decisions,
and a decision nobody can trace is indistinguishable from a default. This
contract makes the difference visible: **every literal value in an output
carries one ground, and a value with no ground is named as such.**

## The failure this prevents

`16px`, `#3B82F6`, `200ms`, `border-radius: 8px`. Each looks decided. Most are
not — they are the first plausible number, carried forward until nobody
remembers whether it was chosen. The output reads as a system while being a
pile of coincidences, and the next person cannot tell which values are load
bearing, so they change none of them.

**Taste is not the problem. Untraceable taste is.** A value chosen on judgement
is grounded the moment the judgement is written next to it.

## The six grounds

Every literal value in a deliverable names exactly one.

| Ground | Means | What must appear beside the value |
|---|---|---|
| `token` | It is a named value in the system | The token name |
| `threshold` | A published requirement fixes it | Which one, and its number — `WCAG 1.4.3, 4.5:1` |
| `measured` | Read off what already exists | What was measured, and where |
| `derived` | Computed from a grounded value by a stated rule | The rule — `base x 1.25, fourth step` |
| `platform` | A platform convention, cited | The convention and its source |
| `brief` | The direction or the request fixes it | The line of the brief it comes from |

`ARBITRARY` is the seventh case and is not a ground: the value works, nothing
fixes it, and nothing above applies. It is recorded, never hidden.

## Recording it

Values travel in tables, so the ground travels in a column:

| Value | Ground | Source |
|---|---|---|
| `--space-3: 12px` | `derived` | 4px base, third step |
| `#1B4DE4` | `threshold` | 4.51:1 on `--bg-canvas` (WCAG 1.4.3) |
| `220ms` | `measured` | the existing drawer, timed |
| `radius 10px` | `ARBITRARY` | reads right at this size; nothing fixes it |

Prose deliverables carry the same thing inline. The form is not the point; the
column being impossible to leave blank is.

## What `ARBITRARY` obliges

An `ARBITRARY` value is legitimate and is **not** a residual on its own. Design
runs out of grounds long before it runs out of decisions, and pretending
otherwise produces invented justifications, which are worse than an honest
blank.

Two things follow. **Every `ARBITRARY` value is stated in the handoff**, so the
receiver knows which numbers are safe to move. And **a deliverable whose values
are mostly `ARBITRARY` is a direction problem, not a values problem** — the
grounds are missing because the brief never fixed anything, and the fix is
upstream in `design-direction`, not a row of invented rationales.

## Boundary cases

- **A ground written after the value was chosen** is still a ground, if it is
  true. The test is whether it *fixes* the value — whether a different value
  would violate it. "It felt balanced" fixes nothing and is `ARBITRARY`
- **`token` requires the token to exist.** Naming a token that has not been
  defined is `ARBITRARY` with a better-looking source
- **Copying from a reference implementation** is `measured` only when the
  reference was actually opened and read. Recalling what a well-known product
  does is `ARBITRARY`
- **A report-only skill grounds its proposed values too.** A critique that says
  "use 24px here" and cannot say why 24 has produced an opinion, not a finding
- **One value, one ground.** Where two apply, the stricter one wins: a token
  that also satisfies a threshold is `threshold`, because that is the one a
  future change can break
