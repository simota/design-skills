#!/usr/bin/env python3
"""Write the delivered blocks back into every SKILL.md.

A contract kept only in the shared directory is not read on most launches, so the operative
part is carried verbatim in each skill. That only stays true if changing one
line does not cost eight hand edits — this is that cost, paid once.

Idempotent: run it, commit the diff.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
MISSING: list[str] = []
H = yaml.safe_load((ROOT / "design-registry" / "harness.yaml").read_text(encoding="utf-8"))
PREFIX = H["prefix"]
SKILLS_ROOT = ROOT / H["skills_dir"] if H.get("skills_dir") else ROOT
MD = MarkdownIt("commonmark")


def h2_lines(lines: list[str]) -> list[tuple[int, str]]:
    """Each `## ` heading as the parser finds it: line index and title.

    A substring search for "## Section" also found `### Section`, and a `## `
    line inside a code fence, so a new block went under the wrong heading or
    into the middle of an example — where validate read it as delivered.
    """
    toks = MD.parse("\n".join(lines))
    return [(tok.map[0], toks[i + 1].content.strip()) for i, tok in enumerate(toks)
            if tok.type == "heading_open" and tok.tag == "h2" and tok.map
            and lines[tok.map[0]].startswith("## ")]


def markers(text: str, key: str) -> tuple[list[int], list[int]]:
    """Line indices of the open and close markers, each alone on its line.

    A marker mentioned in prose is not a marker. Splitting on its first
    occurrence anywhere once rewrote everything from that sentence to the real
    block, and dropped a whole section with it.
    """
    lines = text.split("\n")
    return ([i for i, l in enumerate(lines) if l == f"<!-- deliver:{key} -->"],
            [i for i, l in enumerate(lines) if l == f"<!-- /deliver:{key} -->"])


def render(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    missing_before = len(MISSING)
    for key, spec in H["delivered"].items():
        block = (ROOT / "design-registry" / "delivered" / f"{key}.md").read_text(
            encoding="utf-8").strip("\n")
        open_m, close_m = f"<!-- deliver:{key} -->", f"<!-- /deliver:{key} -->"
        opens, closes = markers(text, key)
        if opens or closes:
            if len(opens) != 1 or len(closes) != 1 or closes[0] < opens[0]:
                # Guessing which pair is meant is how a section gets deleted.
                MISSING.append(f"{path.parent.name}: {key} needs exactly one {open_m} "
                               f"line before one {close_m} line; found "
                               f"{len(opens)} and {len(closes)}")
                continue
            lines = text.split("\n")
            text = "\n".join(lines[:opens[0] + 1] + block.split("\n") + lines[closes[0]:])
        else:
            lines = text.split("\n")
            heads = h2_lines(lines)
            at = next((n for n, (_, title) in enumerate(heads) if title == spec["section"]), None)
            if at is None:
                # A block with nowhere to go is not delivered, and saying
                # "rendered" over it would read as though it were.
                MISSING.append(f"{path.parent.name}: no section {spec['section']!r} for {key}")
                continue
            # append at the end of that section, before the next heading
            start = heads[at][0]
            end = heads[at + 1][0] if at + 1 < len(heads) else len(lines)
            body = lines[start + 1:end]
            while body and not body[-1].strip():
                body.pop()
            rest = [""] + lines[end:] if end < len(lines) else [""]
            text = "\n".join(lines[:start + 1] + body + [open_m] + block.split("\n")
                             + [close_m] + rest)
    # Any block left undelivered and the file is not written: interleaved
    # markers let one block swallow the next one's opener, and writing that
    # replaced the real cause with a different error on the next run.
    if len(MISSING) > missing_before:
        return False
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = [d.name for d in sorted(SKILLS_ROOT.glob(f"{PREFIX}*"))
               if (d / "SKILL.md").exists() and render(d / "SKILL.md")]
    print(f"rendered: {len(changed)} changed" + (f" ({', '.join(changed)})" if changed else ""))
    for m in MISSING:
        print(f"  undelivered — {m}", file=sys.stderr)
    return 1 if MISSING else 0


if __name__ == "__main__":
    sys.exit(main())
