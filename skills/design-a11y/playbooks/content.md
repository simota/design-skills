<!-- design:guidance -->
# Accessible Content

Words are a design surface. Most accessibility content failures are copy decisions.

## Alt text (SC 1.1.1)

Decide the image's *job*, then write to it.

| Job | Alt |
|-----|-----|
| Decorative | `alt=""` — empty, not missing |
| Conveys information | Describe the information, not the picture |
| Functional (inside a link or button) | Describe the destination or action |
| Complex (chart, diagram, map) | Short alt plus a longer description nearby or linked |
| Text in an image | The text verbatim — then question why it is an image |

Rules:
- No "image of", "photo of", "icon of" — the role already says it.
- Length: usually under ~125 characters. Longer means it needs a real description elsewhere.
- Context decides. The same photograph is decorative in a hero and informative in a product listing.
- A chart's alt states the *finding* ("Revenue grew 12% quarter over quarter"), with the data available as a table.

## Labels and instructions (SC 3.3.2, 2.4.6)

- Every input has a visible label. Placeholder-only labelling fails the moment the field is filled.
- Instructions appear *before* the field, not after — the user needs them before typing.
- Format requirements are stated up front, not revealed by an error.
- Group labels (`<fieldset>/<legend>`) for radio and checkbox sets; the legend carries the question.
- Mark either required or optional fields, whichever is the minority. Never both.

## Error messages (SC 3.3.1, 3.3.3)

Three parts: what happened, why, what to do.

| Bad | Good |
|-----|------|
| "Invalid input" | "Enter a date in the future." |
| "Error" | "This email is already registered. Sign in instead." |
| "Field required" | "Enter your workspace name." |
| "Password too weak" | "Use at least 12 characters." |
| "Something went wrong" | "We couldn't save your changes — the connection dropped. Retry." |

Rules:
- Second person, active voice, no blame ("Enter a valid…" not "You entered an invalid…").
- Never rely on colour, an icon, or a border alone (SC 1.4.1) — the message is text.
- Associated with the field programmatically, and announced or focused on submit failure.
- Never remove the user's input when reporting an error.

## Link text

- Meaningful out of context — screen reader users list links independently of surrounding prose.
- "Read more" repeated ten times gives ten identical links. Use "Read the 2026 accessibility report".
- Do not use the URL as the link text.
- Warn about a new tab or a file download in the link text itself ("Annual report (PDF, 2.4 MB)").

## Reading level and plain language

- Write instructions and errors at the simplest level the content allows.
- Expand an acronym on first use.
- Prefer short sentences and one idea per sentence.
- Define required jargon inline rather than in a glossary the user must leave to find.

## Consistency (SC 3.2.4, 3.2.6)

- The same function is named the same everywhere — "Delete" is not "Remove" on the next screen.
- Help mechanisms (contact link, chat, docs) appear in the same relative position across pages (SC 3.2.6 A).
- Icons carry the same meaning throughout.

## Authentication content (SC 3.3.8 AA)

- No cognitive function test — puzzle, memory game, or transcription — without an alternative.
- Paste must work in password and one-time-code fields. Blocking paste breaks password managers and fails this criterion.
- Support `autocomplete="one-time-code"` and `autocomplete="current-password"`.
- If a CAPTCHA exists, provide a non-cognitive alternative (object recognition and personal-content recognition are permitted exceptions).

## Redundant entry (SC 3.3.7 A)

Within one process, information already entered is auto-populated or selectable — not retyped. The common failure is a billing address that must be typed again after a shipping address, with no "same as" option.

## Announcements

Write the announcement text as part of the design spec.

| Event | Announcement |
|-------|--------------|
| Filter applied | "24 results" |
| Item saved | "Invoice saved" |
| Item deleted | "Invoice INV-104 deleted. Undo available." |
| Upload progress | "Uploading, 60 percent" — throttled to a few announcements, not every tick |
| Validation failure | "3 fields need attention" plus focus moved to the first |

Specific beats generic. "Saved" tells a screen reader user less than "Invoice saved".
