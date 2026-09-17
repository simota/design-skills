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

**Taste is not the problem. Untraceable taste is.** Recording a judgement makes
it traceable, not grounded: if nothing fixes the value, it remains `ARBITRARY`.

## The six grounds

Every literal value in a deliverable names exactly one.

| Ground | Means | What must appear beside the value |
|---|---|---|
| `token` | It resolves to an existing system value | The token name, definition and theme |
| `threshold` | The value is a published requirement's limit | The source, criterion, limit and applicable case |
| `measured` | As the evidence grade of that name (`_design/CONTRACT.md`): read off what already exists | What was measured, and where |
| `derived` | Computed from grounded inputs by a stated rule | Input sources, including scale factor, step and rounding policy, and the calculation |
| `platform` | A platform source actually specifies the value | The opened source, version where relevant, and applicable context |
| `brief` | The direction or request explicitly fixes the value | The originating line; writing a chosen value into the brief is not an independent source |

`ARBITRARY` is the seventh case and is not a ground: the value works, nothing
fixes it, and nothing above applies. It is recorded, never hidden.

## Recording it

Values travel in tables, so the ground travels in a column:

| Value | Ground | Source |
|---|---|---|
| computed scale step | `derived` | grounded base and step policy, source locations, calculation |
| chosen colour | `ARBITRARY` | no source fixes this colour; record its measured contrast separately |
| observed duration | `measured` | the actual timed transition, conditions and result |
| `radius 10px` | `ARBITRARY` | reads right at this size; nothing fixes it |

Prose deliverables carry the same thing inline. The form is not the point; the
column being impossible to leave blank is.

## What `ARBITRARY` obliges

An `ARBITRARY` value is legitimate and is **not** a residual on its own. Design
runs out of grounds long before it runs out of decisions, and pretending
otherwise produces invented justifications, which are worse than an honest
blank.

**Record every `ARBITRARY` value in the handoff, or inline at `T0`.** It is a
settled choice, not automatically an unresolved decision or permission to ignore
constraints. Its frequency alone is not a direction problem. Return upstream
only when an intent needed for this work is actually undecided.

## Boundary cases

- **A ground written after the value was chosen** is still a ground, if it is
  true. The test is whether it *fixes* the value — whether a different value
  would violate it. "It felt balanced" fixes nothing and is `ARBITRARY`
- **`token` requires a resolvable definition.** Naming a new primitive does not
  ground its underlying value; preserve that value's origin through aliases
- **`derived` does not launder a choice.** An ungrounded base, factor or policy
  leaves the proposed value `ARBITRARY`; record the formula anyway
- **Copying from a reference implementation** is `measured` only when the
  reference was actually opened and read. Recalling what a well-known product
  does is `ARBITRARY`
- **A report-only skill grounds its proposed values too.** The evidence for a
  finding and the origin of its proposed replacement value are separate claims
- **One value, one ground; constraints are separate.** Meeting a contrast floor
  does not fix a colour. Keep its actual origin (including `token` or `ARBITRARY`)
  and record the applicable limit and computed test separately. A later true
  source may be recorded; a rationale that merely permits the value is not one
