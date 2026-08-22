<!-- design:guidance -->
# Seeing

Getting the artifact in front of your own eyes. Everything downstream is a
report on this step, so a shortcut here is not a shortcut — it is a fabrication.

## Two paths, and the honest label on each

| Path | How | What the verdict may claim |
|---|---|---|
| Rendered here | Start the app or story, open the URL, capture the view | What was on screen under the stated conditions |
| Handed to you | Read the image or export you were given | What that image shows, at its resolution, at that moment |

**A third path does not exist.** Reading CSS, a component tree, or a token file
and describing the result is inference about a render nobody performed. It is
useful for finding a cause once something is seen; it is never the seeing.

## Rendering it

Prefer what the project already uses over anything you introduce.

1. **Find the entry point** — a dev server script, a component explorer, a
   static build, an existing screenshot task. The repository usually says.
2. **Start it and confirm it is up** — a captured error page is still a capture,
   and reviewing one as if it were the design is a real failure mode.
3. **Capture, do not describe.** Write an image and open it. A rendering you
   only reasoned about is the third path wearing the first path's label.
4. **Say how.** The command, the URL, the route. A reader who cannot reproduce
   the view cannot argue with the verdict.

Where the project has no way to render, say that. It is a finding about the
project, and it downgrades everything this skill can honestly claim.

## The conditions to capture

Each is a separate view, and a verdict covers only the ones actually seen.

- **Viewport** — the narrowest supported width, one mid width, and the widest
  the layout is designed for. Composition failures live at the extremes
- **Theme** — every theme that ships. A palette that holds in one can collapse
  in another, and the collapse is visual before it is measurable
- **State** — the populated case, the empty case, the loading case, the error
  case, and the overflowing case. Design is usually reviewed populated and
  perfect, which is the one state users see least
- **Content** — real strings and real lengths where they exist. Placeholder
  copy of uniform length hides every rhythm problem there is

## Before moving on

- The captures exist as files, and each is labelled with its conditions
- Anything that could not be rendered is named, with what was tried
- Nothing has been judged yet. The impression comes next, and it comes from
  looking — not from the list of things you now know to check
