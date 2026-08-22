<!-- design:guidance -->
# State Matrix

The full set of states a screen can occupy. Unspecified states get invented at build time, badly.

## The states

### Empty — first use

The most valuable screen in the product and the most often skipped.

Must specify: what this screen is for (one sentence), the single action that fills it, and — when useful — a sample or template. Never a bare "No data".

### Empty — filtered / searched to nothing

Distinct from first use. Must specify: what was searched, that the filter is the cause, and a one-click way to clear it. Never show the first-use onboarding here.

### Loading — initial

Skeletons that match the eventual layout, not a centred spinner, for anything with structure. Specify the delay before the skeleton appears (typically 100–200ms) so fast responses do not flash.

### Loading — refresh / background

Old content stays visible and readable. Indicate freshness subtly (an inline indicator on the refresh control). Never blank out content the user is reading.

### Loading — action pending

The indicator lives on the control that was pressed. Disable that control to prevent double submission; do not disable the whole screen.

### Partial

Some data loaded, some failed. Specify what renders, how the failed region is marked, and whether it retries independently. A single failed widget must not blank the page.

### Error — recoverable

Three required parts: what happened (in the user's terms), why if known, and the one next action. Preserve all user input. Put the retry next to the failure, not in a global banner.

| Bad | Good |
|-----|------|
| "Something went wrong" | "Couldn't save your changes — the connection dropped. Retry" |
| "Error 500" | "Our server had a problem. Your draft is saved. Try again" |
| A toast that disappears | An inline, persistent error at the point of failure |

### Error — validation

Belongs at the field, not at the top. See `playbooks/forms.md`.

### Error — permission denied

Specify: what is not permitted, who can grant it, and the action to request it. Never a generic 403 page for an in-app action.

### Error — not found

Distinguish "never existed", "was deleted", and "you cannot see it" where security allows. Offer the parent list as an exit.

### Offline

Specify what still works from cache, what is queued, and how the user knows when it syncs. A persistent, non-blocking indicator — never a modal.

### Success

Confirm what happened, specifically ("Project *Atlas* created"), and offer the natural next action. If undoable, the undo lives here with its window stated.

### Destructive pending

The undo window (5–10s typical), where the undo control lives, and what happens if the user navigates away before it expires.

## Filled example

| State | Condition | Content | Primary action | Notes |
|-------|-----------|---------|----------------|-------|
| Empty (first) | `items.length === 0 && !filters` | "Invoices you create appear here." | Create invoice | Show a sample row, greyed |
| Empty (filtered) | `items.length === 0 && filters` | "No invoices match *unpaid, Q3*." | Clear filters | Keep filter chips visible |
| Loading (initial) | first fetch pending | 6 skeleton rows | — | Appears after 150ms |
| Loading (refresh) | refetch pending | previous rows retained | — | Spinner on refresh button only |
| Partial | totals failed, rows ok | rows render; totals slot shows retry | Retry totals | Rows remain interactive |
| Error (fetch) | 5xx / timeout | "Couldn't load invoices." | Retry | Filters preserved |
| Error (permission) | 403 | "You need billing access." | Request access | Names the admin |
| Offline | `navigator.onLine === false` | cached rows + banner | — | New invoices queue |
| Success (create) | 201 | toast: "Invoice INV-104 created" | View invoice | Undo not applicable |
| Destructive pending | delete issued | row greyed, "Deleted · Undo" | Undo | 8s window; commits on navigate |

## Checklist

- [ ] Both empty states distinguished
- [ ] Skeleton matches the real layout
- [ ] Refresh does not blank existing content
- [ ] Every async action has a specified failure state
- [ ] Every error names a next action
- [ ] User input survives every failure branch
- [ ] Permission and not-found handled separately from generic error
- [ ] Offline behaviour stated
- [ ] Success is specific, not generic
- [ ] Destructive actions have an undo window with stated duration
- [ ] No state relies on colour alone
- [ ] Focus destination stated for every state transition
