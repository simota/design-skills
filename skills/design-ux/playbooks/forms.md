<!-- design:guidance -->
# Forms

Forms are where UX failures cost the most, because the user has already invested effort.

## Field spec

Specify every field this way. An unspecified field gets guessed.

| Field | Type | Required | Constraint | Default | Validate | Error copy |
|-------|------|----------|-----------|---------|----------|------------|
| Email | email | yes | RFC + MX-plausible | — | on blur | "That doesn't look like an email address." |
| Password | password | yes | ≥12 chars | — | live (strength), blur (rule) | "Use at least 12 characters." |
| Workspace | text | yes | 3–40, `[a-z0-9-]` | derived from company | on blur | "Only lowercase letters, numbers, and hyphens." |
| Plan | radio | yes | — | Team (most chosen) | — | — |
| Seats | number | no | 1–500 | 5 | on blur | "Between 1 and 500." |

## Prevention before validation

In priority order:

1. **Constrain the control** — a date picker cannot produce an invalid date; a select cannot produce an unknown value.
2. **Constrain the input** — `inputmode`, `maxlength`, masks, step values.
3. **Format as they type** — phone numbers, card numbers, currency. Never reject formatting the user could not have known about.
4. **Accept generously, normalise silently** — strip spaces from card numbers and IBANs; accept `+81`, `081`, and `81`. Rejecting a valid value over formatting is a design failure.
5. **Only then, validate and message.**

## Validation timing

| Timing | Use for | Never |
|--------|---------|-------|
| On blur | Most fields | The field they are still typing in |
| Live | Password strength, character counters, availability checks | Anything that reads as nagging mid-typing |
| On submit | Cross-field rules (dates ordering, totals) | The only validation in a long form |
| Never | Fields the user has not reached | — |

After a failed submit, switch previously-errored fields to live validation so the user sees the error clear as they fix it.

## Error presentation

- At the field, below it, associated programmatically with the input.
- Plus a summary at the top *only* for long forms — the summary links to each field.
- Move focus to the first errored field on failed submit.
- State how to fix, not what is wrong: "Use at least 12 characters" beats "Password too short".
- Never clear the field's value on error.
- Never use colour alone — pair with an icon and text.

## Labels

- Always visible. Placeholder-only labelling fails as soon as the field is filled, and fails memory and translation.
- Above the field for scannability, unless the form is a dense single-row filter bar.
- Mark optional fields rather than required ones when most are required, and vice versa. Do not mark both.
- Helper text before the field, not after — the user needs it before they type.

## Layout

- Single column. Multi-column forms break the scan path and mis-associate labels.
- Group related fields with a heading; keep groups under ~7 fields.
- Field width should signal the expected content length — a postcode field the width of an address line invites the wrong answer.
- The primary submit button sits at the start of the reading direction, aligned with the fields, not floated far right.

## Submission

| Moment | Behaviour |
|--------|-----------|
| Press | Disable the button, show pending state on it, keep fields readable |
| Slow (>1s) | Pending indicator on the button; do not block the page |
| Success | Specific confirmation and a next action |
| Failure | Re-enable, preserve every value, focus the cause |
| Double submit | Prevented by disabling plus an idempotency key server-side |

Never disable the submit button until the form is valid — the user then has no way to discover *why* it is disabled. Let them submit and show the errors.

## Multi-step forms

- Progress is explicit: step N of M with M known.
- Validate on leaving each step.
- Back never loses data.
- Save on every step transition.
- Review step before an irreversible submit, showing what will happen.

## Autofill and input hygiene

Specify `autocomplete` tokens per field (`email`, `new-password`, `current-password`, `one-time-code`, `postal-code`, `cc-number`). Specify `inputmode` for numeric and decimal fields. These are design decisions with a large measurable effect on completion, not implementation details to leave to chance.

## Anti-patterns

- Clearing the password field on a failed login.
- Rejecting a pasted value (card numbers, OTPs) — always allow paste.
- A required field the user cannot possibly know the answer to.
- Asking for the same information twice in one flow.
- "Confirm email" fields — they measure typing consistency, not correctness.
- Validation that fires on every keystroke from the first character.
- A generic top-of-form error with no indication of which field failed.
