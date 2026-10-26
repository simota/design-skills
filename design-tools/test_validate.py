#!/usr/bin/env python3
"""Prove each rule in validate.py fires, and each recomputation in figures_check.py.

A check only ever seen passing may be checking nothing. Every rule below gets a
deliberate violation injected into a throwaway copy of the repo, and the test
fails if the validator stays quiet.

Run: make test
"""
from __future__ import annotations

import errno
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True                     # no __pycache__ in the tools dir
import validate                                    # noqa: E402  — for RULES only


def run(root: Path) -> str:
    r = subprocess.run([sys.executable, str(root / "design-tools" / "validate.py")],
                       capture_output=True, text=True, errors="replace")
    return r.stdout + r.stderr


S = "skills/"          # everything the CLI reads lives here


def sub(path: Path, old: str, new: str) -> None:
    t = path.read_text(encoding="utf-8")
    assert old in t, f"fixture text not found in {path.name}: {old[:60]!r}"
    path.write_text(t.replace(old, new, 1), encoding="utf-8")


# Each case mutates a copy, then expects that rule id in the output.
CASES: dict[str, callable] = {}


# A case may also name the text its branch prints. Without it a case proves
# only that the rule id appeared, and a rule with several checks passes with
# all but one of them deleted.
MESSAGES: dict[str, str] = {}


def case(rule, says: str | None = None):
    def deco(fn):
        CASES[rule] = fn
        if says:
            MESSAGES[rule] = says
        return fn
    return deco


@case("V1")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "## Owns", "## Owns\n" + "x\n" * 200)


@case("V2")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "How an interface behaves",
              "Not for design-motion. How an interface behaves")


@case("V3")
def _(r): (r / f"{S}design-ghost").mkdir(); (r / f"{S}design-ghost/SKILL.md").write_text("x")


@case("V3-name")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "name: design-ux", "name: design-behaviour")


@case("V3-yaml", "no frontmatter a YAML loader accepts")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "description: \"", "description: \"\"")


@case("V4")
def _(r): (r / f"{S}design-ux/playbooks/orphan.md").write_text("<!-- design:guidance -->\n")


@case("V5")
def _(r): (r / f"{S}design-ux/playbooks/forms.md").write_text("y\n" * 400)


@case("V6", "VALUES.md is")
def _(r): sub(r / f"{S}_design/VALUES.md", "## 1. Honesty", "z\n" * 200 + "## 1. Honesty")


@case("V7")
def _(r): sub(r / "design-registry/routes.yaml", "chain: [design-ux, design-motion]",
              "chain: [design-ux, design-nonexistent]")


@case("V8")
def _(r): sub(r / "README.md", "](skills/_design/ROUTING.md)", "](skills/_design/GONE.md)")


@case("V9")
def _(r): sub(r / "design-registry/capabilities.yaml", "signals: [motion, duration",
              "signals: [forms, duration")


@case("V10")
def _(r): sub(r / "design-registry/fixtures.yaml",
              '- ask: "give me a UI audit of this screen"\n  expect: design-critique',
              '- ask: "give me a UI audit of this screen"\n  expect: design-tokens')


@case("V10-empty", "holds no list of asks")
def _(r): (r / "design-registry/fixtures.yaml").write_text("# no asks yet\n", encoding="utf-8")


@case("V11")
def _(r):
    import shutil
    for i in range(4):
        d = r / f"{S}design-extra{i}"
        d.mkdir()
        shutil.copy(r / f"{S}design-ux/SKILL.md", d / "SKILL.md")


@case("V12")
def _(r): (r / f"{S}rogue").mkdir(); (r / f"{S}rogue/SKILL.md").write_text("x")


@case("V13")
def _(r):
    t = (r / "design-registry/routes.yaml").read_text(encoding="utf-8")
    t += "".join(f"\nfiller{i}:\n  pattern: linear\n  when: x\n  chain: [design-ux]\n"
                 for i in range(20))
    (r / "design-registry/routes.yaml").write_text(t, encoding="utf-8")


@case("V13-stages")
def _(r): sub(r / "design-registry/routes.yaml",
              "chain: [design-direction, design-ux, design-motion, design-tokens, design-a11y]",
              "chain: [design-direction, design-ux, design-motion, design-tokens, design-a11y, "
              "design-critique, design-review]")


@case("V14")
def _(r): sub(r / "design-registry/routes.yaml", "  pattern: loop", "  pattern: spiral")


@case("V15")
def _(r): sub(r / f"{S}design-critique/SKILL.md", "allowed-tools: Read, Grep, Glob, Bash",
              "allowed-tools: Read, Grep, Glob, Edit, Write, Bash")


@case("V16")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "## Done when", "## Finished when")


@case("V17")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "- **Grade each claim**", "- **Grade some claims**")


@case("V18")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "cognitive load", "mental effort")


@case("V19")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "`_design/SIZING.md`", "`../_design/SIZING.md`")


@case("V19-shared")
def _(r): sub(r / f"{S}_design/ROUTING.md", "(`_design/SIZING.md`)", "(`SIZING.md`)")


@case("V19-reference")
def _(r): sub(r / f"{S}design-tokens/reference/export-targets.md",
              "`playbooks/naming.md`", "`naming.md`")


@case("V20")
def _(r):
    """The definition row becomes a mention; the word is still on the page."""
    sub(r / f"{S}_design/CONTRACT.md", "| `asserted` |", "| asserted |")


@case("V21")
def _(r): sub(r / f"{S}design-ux/SKILL.md",
              """A state matrix is checked against the running interface where one exists
(evidence: `measured` — the states were counted, not imagined). Where nothing is
built yet, the spec is `inspected` and says so.""",
              "A state matrix is checked against the running interface.")


@case("V22")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "## Done when",
              "## Done when\n\n#" + "TODO(agent): tidy this up later\n")


@case("V23")
def _(r): sub(r / f"{S}_design/VALUES.md", "<!-- design:contract -->", "<!-- design:guidance -->")


@case("V23-undeclared")
def _(r): sub(r / "design-registry/harness.yaml",
              "document_labels: [contract, guidance, deferred]",
              "document_labels: [contract, deferred]")


@case("V24", "ROUTING.md does not list design-motion")
def _(r): sub(r / f"{S}_design/ROUTING.md", "`design-motion`", "`design-animation`")


@case("V25")
def _(r): sub(r / f"{S}design-ux/playbooks/forms.md", "# ", "# pinned at v2.14.0 — ")


@case("V26")
def _(r): sub(r / "design-registry/capabilities.yaml", "      go: design-tokens",
              "      go: design-values")


@case("V27")
def _(r):
    (r / f"{S}design-ux/_design").unlink()
    (r / f"{S}design-ux/_design").symlink_to("../_gone")


@case("V28", "set 'ui' requires")
def _(r): sub(r / "design-registry/harness.yaml", "set: design", "set: ui")


@case("V28-generic-dir")
def _(r): (r / "registry").mkdir()


@case("V29")
def _(r):
    f = r / f"{S}design-ux/reference/spec-template.md"
    f.write_text(f.read_text(encoding="utf-8").replace("Verified:", "Checked:"), encoding="utf-8")


@case("V30")
def _(r): (r / f"{S}design-ux/reference/orphan.md").write_text(
    "<!-- design:deferred -->\n# Orphan\n\nPurpose: x\nRead when: y\nVerified: 2026-08-21\n")


@case("V31")
def _(r):
    for f in sorted((r / f"{S}").glob("*/reference/*.md")):
        t = f.read_text(encoding="utf-8")
        i = t.index("Verified:")
        j = t.index("\n\n", i)
        f.write_text(t[:i] + "Verified: 2026-08-21" + t[j:], encoding="utf-8")
        return


@case("V32")
def _(r):
    sub(r / "design-registry/routes.yaml", "checker: ", "checker: claude  # ")


@case("V32-unknown")
def _(r):
    sub(r / "design-registry/routes.yaml", "checker: ", "checker: nosuchengine  # ")



@case("V32-single")
def _(r):
    sub(r / "design-registry/harness.yaml",
        "runs_on: [claude, codex, agy]", "runs_on: [claude]")



@case("V33")
def _(r):
    sub(r / "design-registry/harness.yaml", "  lens: |", "  lens: ''\n  unused: |")



@case("V34")
def _(r):
    """Reachable and runnable must move together, whichever way they are split."""
    for d in sorted((r / "skills").glob("design-*")):
        link = d / "refute.py"
        if link.is_symlink():
            link.unlink()                      # runnable, and now out of reach
            return
    # No set-wide link to remove: make a skill runnable instead, and leave it
    # unreachable. Widening a class trips V15 too, which the harness allows —
    # it only asks that V34 appear.
    sub(r / "design-registry/harness.yaml",
        "tools: \"Read, Grep, Glob, Write", "tools: \"Read, Grep, Glob, Bash, Write")


@case("V34-wrong-tool", "not the set's own")
def _(r):
    """A link to the right name that resolves to a different tool."""
    for d in sorted((r / "skills").glob("design-*")):
        link = d / "refute.py"
        if link.is_symlink():
            link.unlink()
            link.symlink_to("../../design-tools/render.py")
            return


@case("V34-undeclared")
def _(r):
    """A tool link nothing declares is a capability nobody decided to grant."""
    (r / "skills/design-ux/render.py").symlink_to("../../design-tools/render.py")


@case("V34-missing-tool")
def _(r): sub(r / "design-registry/harness.yaml",
              "  refute.py: all", "  refute.py: all\n  nosuch.py: all")


@case("V34-none-declared", "declares no linked_tools")
def _(r): sub(r / "design-registry/harness.yaml", "linked_tools:", "unlinked_tools:")


@case("V35")
def _(r): sub(r / f"{S}design-a11y/SKILL.md", "including `ARBITRARY`; record",
              "including an ungrounded one; record")


@case("V36")
def _(r): (r / f"{S}design-review/playbooks/visualise.md").unlink()


@case("V36-undefined")
def _(r):
    """A trigger the registry declares and the pages never define."""
    for g in (r / f"{S}design-review/playbooks/visualise.md",
              r / f"{S}design-review/reference/diagram-forms.md"):
        g.write_text(g.read_text(encoding="utf-8").replace("`ordering`", "sequencing"),
                     encoding="utf-8")


@case("V36-unreachable")
def _(r): sub(r / f"{S}design-review/SKILL.md",
              "[visualise](playbooks/visualise.md)", "the visualise guidance")


@case("V36-none-declared", "declares no finding_visuals")
def _(r): sub(r / "design-registry/harness.yaml", "finding_visuals:", "unused_visuals:")


@case("V38")
def _(r): sub(r / f"{S}design-a11y/playbooks/content.md", "## ", "verdict: KEEP | DROP\n\n## ")


@case("V37")
def _(r):
    """A page that leans on a declared source and does not say so."""
    sub(r / f"{S}design-a11y/reference/wcag22-checklist.md",
        'Source: WCAG 2.2 — summaries, not verbatim criteria; check applicability and exceptions.',
        "Source: none — nothing outside this page can move what it states.")


@case("V37-unused", "never uses it")
def _(r):
    """A source named in the header that the page never uses."""
    sub(r / f"{S}design-review/reference/comparison.md",
        "Source: none — nothing outside this page can move what it states.",
        'Source: WCAG 2.2 — the success criteria below are quoted from that version.')


@case("V37-silent")
def _(r):
    """Neither a source nor the admission that there is none."""
    sub(r / f"{S}design-review/reference/comparison.md",
        "Source: none — nothing outside this page can move what it states.", "Source:")


@case("V37-none-declared", "declares no source_authorities")
def _(r): sub(r / "design-registry/harness.yaml", "source_authorities:", "unused_authorities:")


# --- cycle 6: false passes an independent review reproduced -------------------

@case("V29-bold", "has no line opening with 'Source:'")
def _(r):
    """A bolded header satisfied V29's substring test, and V31 and V37, which
    look for the line that opens with it, found none and stayed quiet: a wrong
    pin and a bare date passed."""
    f = r / f"{S}design-a11y/reference/semantics.md"
    t = f.read_text(encoding="utf-8")
    t = re.sub(r"^Source: .*$", "**Source:** WCAG 2.9", t, count=1, flags=re.M)
    f.write_text(re.sub(r"^Verified: .*$", "**Verified:** 2026-08-21", t, count=1, flags=re.M),
                 encoding="utf-8")


@case("V19-link-escapes", "leaves the skill directory")
def _(r):
    """The README's own example: a Markdown link, not a backticked path, that
    climbs out of the skill. It exists in the repo, so V8 is satisfied."""
    sub(r / f"{S}design-a11y/SKILL.md", "[content](playbooks/content.md)",
        "[content](playbooks/content.md), see [contract](../_design/CONTRACT.md)")


@case("V8-outside", "outside the repository")
def _(r):
    """A sibling checkout beside this one resolves here and nowhere else."""
    (r.parent / "agent-toolkit/tools").mkdir(parents=True)
    (r.parent / "agent-toolkit/tools/pages.py").write_text("x\n", encoding="utf-8")
    sub(r / "README.md", "## Files", "[pages](../agent-toolkit/tools/pages.py)\n\n## Files")


@case("V8-reenters", "outside the repository")
def _(r):
    """Out through the parent and back in by the checkout's own name: it
    resolves inside only while the clone keeps that name."""
    sub(r / "README.md", "## Files", f"[self](../{r.name}/README.md)\n\n## Files")


@case("V27-absolute", "is an absolute link")
def _(r):
    """git commits the link's text: an absolute path into this checkout breaks
    in every other clone, and when this one moves."""
    link = r / f"{S}design-ux/_design"
    link.unlink()
    link.symlink_to((r / f"{S}_design").resolve())


# figures_check.py is held to the same standard: each recomputation is shown
# failing on a deliberately wrong page, or a green run proves nothing about it.
CONTRAST = f"{S}design-a11y/reference/contrast.md"
SCALES = f"{S}design-tokens/reference/scales.md"
SCHEMA = f"{S}design-tokens/reference/token-schema.md"
FIGURE_CASES: dict[str, callable] = {
    "contrast-ratio": lambda r: sub(r / CONTRAST, "| 17.76:1 |", "| 17.10:1 |"),
    "contrast-verdict": lambda r: sub(r / CONTRAST, "| 2.64:1 | 4.5:1 | **fail** |",
                                      "| 2.64:1 | 4.5:1 | pass |"),
    "contrast-unparsed": lambda r: sub(r / CONTRAST, "| Body on canvas | `#16181d` |",
                                       "| Body on canvas | near-black |"),
    "contrast-table-gone": lambda r: sub(r / CONTRAST, "| Pair | Foreground |",
                                         "| Pairing | Foreground |"),
    "scale-step": lambda r: sub(r / SCALES, "| `--text-lg` | 19px |", "| `--text-lg` | 20px |"),
    "scale-clamp-undeclared": lambda r: sub(r / SCALES, "clamped below `--text-base`",
                                            "kept above the ratio"),
    "scale-header-gone": lambda r: sub(r / SCALES, "| 16px / 1.20 ratio |", "| Size |"),
    "scale-unparsed": lambda r: sub(r / SCALES, "| `--text-4xl` | 40px |",
                                    "| `--text-4xl` | 52px (hero) |"),
    # A verdict is pass or fail, not any text that holds "pass" and not "fail".
    "contrast-verdict-negated": lambda r: sub(r / CONTRAST, "| 17.76:1 | 4.5:1 | pass |",
                                              "| 17.76:1 | 4.5:1 | does not pass |"),
    # A header whose separator line is gone is no longer a table, and fails
    # rather than leaving the steps under it unchecked.
    "scale-no-separator": lambda r: _scale_no_separator(r),
    # Only the separator under the header is skipped; one standing in for a row
    # removed that step and the rest still recomputed.
    "contrast-row-as-separator": lambda r: sub(
        r / CONTRAST, "| Body on canvas | `#16181d` | `#ffffff` | 17.76:1 | 4.5:1 | pass |",
        "|---|---|---|---|---|---|"),
    "scale-row-as-separator": lambda r: sub(r / SCALES, "| `--text-4xl` | 40px | 1.1 | Hero |",
                                            "|-------|-------|"),
    # A row without its outer pipes is still a row: ending the table there
    # dropped it and every row after it, and a wrong ratio below passed.
    "contrast-row-without-outer-pipe": lambda r: (
        sub(r / CONTRAST, "| `#3560d8` | 5.50:1 | 4.5:1 | pass |", "| `#3560d8` | 5.50:1 | 4.5:1 | pass"),
        sub(r / CONTRAST, "| `#3560d8` | `#ffffff` | 5.50:1 | 3:1 | pass |",
            "| `#3560d8` | `#ffffff` | 9.50:1 | 3:1 | pass |")),
    "scale-row-without-leading-pipe": lambda r: (
        sub(r / SCALES, "| `--text-2xl` | 28px |", "`--text-2xl` | 28px |"),
        sub(r / SCALES, "| `--text-3xl` | 33px |", "| `--text-3xl` | 35px |")),
    # Every recording table, not the first: a dark theme's pairs are a second one.
    "contrast-second-table": lambda r: sub(
        r / CONTRAST, "The focus ring on the accent button is",
        "| Pair | Foreground | Background | Ratio | Required | Result |\n|---|---|---|---|---|---|\n"
        "| Muted on dark | `#9aa0a6` | `#16181d` | 12.00:1 | 4.5:1 | pass |\n\nThe focus ring on the accent button is"),
    # A typo in a number is a row that does not parse, not a traceback that
    # loses every other mismatch of the run.
    "contrast-malformed-number": lambda r: sub(r / CONTRAST, "| 17.76:1 |", "| 17.76.:1 |"),
    # Tables are found through the parse, and a header Markdown does not read as
    # a table is not a table that quietly drops out: it fails, with its rows.
    "contrast-second-table-without-separator": lambda r: sub(
        r / CONTRAST, "The focus ring on the accent button is",
        "| Pair | Foreground | Background | Ratio | Required | Result |\n"
        "| Muted on dark | `#9aa0a6` | `#16181d` | 12.00:1 | 4.5:1 | pass |\n\nThe focus ring on the accent button is"),
    # A fence left open runs to the end of the page: a table after it is code,
    # and with the first table still read, its pairs left the count unnoticed.
    "contrast-table-in-unclosed-fence": lambda r: (r / CONTRAST).write_text(
        (r / CONTRAST).read_text(encoding="utf-8")
        + "\n```\n\n| Pair | Foreground | Background | Ratio | Required | Result |\n|---|---|---|---|---|---|\n"
        "| Muted on dark | `#9aa0a6` | `#16181d` | 12.00:1 | 4.5:1 | pass |\n", encoding="utf-8"),
    # The verdict is decided on the unrounded ratio. 2.995:1 is recorded as
    # 3.00:1 and still fails 3:1; deciding on the recorded figure passed it.
    "contrast-verdict-rounded-up": lambda r: sub(
        r / CONTRAST, "| 3.00:1 | 3:1 | **fail — computes 2.995:1** |", "| 3.00:1 | 3:1 | pass |"),
    # A line of prose directly under the rows is still a row, as GFM reads it.
    "contrast-prose-under-table": lambda r: sub(
        r / CONTRAST, "**fail — needs an offset ring** |\n",
        "**fail — needs an offset ring** |\nMuted on dark is roughly 2.6\n"),
    # GFM opens a table inside a blockquote and without outer pipes as well;
    # matching the raw header let either drop out while the first table kept
    # the count above zero.
    "contrast-table-in-blockquote": lambda r: sub(
        r / CONTRAST, "The focus ring on the accent button is",
        "> | Pair | Foreground | Background | Ratio | Required | Result |\n> |---|---|---|---|---|---|\n"
        "> | Muted on dark | `#9aa0a6` | `#16181d` | 12.00:1 | 4.5:1 | pass |\n\nThe focus ring on the accent button is"),
    "contrast-table-without-outer-pipes": lambda r: sub(
        r / CONTRAST, "The focus ring on the accent button is",
        "Pair | Foreground | Background | Ratio | Required | Result\n---|---|---|---|---|---\n"
        "Muted on dark | `#9aa0a6` | `#16181d` | 12.00:1 | 4.5:1 | pass\n\nThe focus ring on the accent button is"),
    # A DTCG colour states its hex and its components; edit one and not the other.
    "dtcg-components-drift": lambda r: sub(r / SCHEMA, "[0.051, 0.0588, 0.0745]",
                                           "[0.051, 0.0588, 0.0845]"),
    # The draft's bare hex string carries no components to hold against anything.
    "dtcg-colour-as-string": lambda r: sub(
        r / SCHEMA, '{ "colorSpace": "srgb", "components": [0.051, 0.0588, 0.0745], "hex": "#0d0f13" }',
        '"#0d0f13"'),
    # An example that no longer parses drops every colour in it from the count.
    "dtcg-example-not-json": lambda r: sub(r / SCHEMA, '"hex": "#f7f8fa" } }', '"hex": "#f7f8fa" } },'),
    # NaN is a float no difference ever exceeds; a component is a number from 0 to 1.
    "dtcg-components-nan": lambda r: sub(r / SCHEMA, "[0.051, 0.0588, 0.0745]", "[NaN, NaN, NaN]"),
    # A token whose type resolves to nothing is not a token with nothing wrong in it.
    "dtcg-type-removed": lambda r: sub(
        r / SCHEMA, '"950": { "$type": "color",\n               "$value": { "colorSpace": "srgb", '
                    '"components": [0.051, 0.0588, 0.0745]',
        '"950": {\n               "$value": { "colorSpace": "srgb", "components": [0.9, 0.9, 0.9]'),
    # An alias is checked where it points, so a target that is gone fails.
    "dtcg-alias-dangling": lambda r: sub(r / SCHEMA, '"{color.gray.950}"', '"{color.gray.951}"'),
    # An example relabelled out of reach is not an example with nothing wrong in it.
    "dtcg-example-gone": lambda r: sub(r / SCHEMA, "```json\n{\n  \"color\"", "```jsonc\n{\n  \"color\""),
    # The colour type set on the group, not the token, is still a colour.
    "dtcg-type-on-group": lambda r: sub(
        r / SCHEMA, '"950": { "$type": "color",\n               "$value": { "colorSpace": "srgb", '
                    '"components": [0.051, 0.0588, 0.0745]',
        '"$type": "color",\n      "950": {\n               "$value": { "colorSpace": "srgb", '
        '"components": [0.051, 0.0588, 0.0999]'),
    # Aliases that only point at each other resolve to no value at all; each
    # side read the other's type and found nothing wrong.
    "dtcg-alias-cycle": lambda r: (
        sub(r / SCHEMA, '"$value": "{color.gray.950}",', '"$value": "{color.text.loop}",'),
        sub(r / SCHEMA, '"text": {\n      "primary": {',
            '"text": {\n      "loop": { "$value": "{color.text.primary}" },\n      "primary": {')),
}

# The other half: a page that records every figure correctly stays green when
# what surrounds its tables changes. Reading raw lines took a fenced example
# for a second recording table, and a heading under the rows for a row.
FENCED_PAIRS = ("\n```md\n| Pair | Foreground | Background | Ratio | Required | Result |\n"
                "|---|---|---|---|---|---|\n| Example | `#777777` | `#ffffff` | 9.99:1 | 4.5:1 | pass |\n"
                "```\n")
FIGURE_GREEN_CASES: dict[str, callable] = {
    "contrast-heading-under-table": lambda r: sub(
        r / CONTRAST, "**fail — needs an offset ring** |\n\n",
        "**fail — needs an offset ring** |\n### Notes\n\n"),
    "contrast-example-in-a-fence": lambda r: sub(
        r / CONTRAST, "The focus ring on the accent button is", FENCED_PAIRS + "\nThe focus ring on the accent button is"),
    # The parser counts lines at "\n" alone; a U+2028 in prose above the table
    # moved every line number read with splitlines().
    "contrast-line-separator-above": lambda r: sub(
        r / CONTRAST, "| Pair | Foreground |", "A line\u2028inside it.\n\n| Pair | Foreground |"),
    # A row that drops only its trailing pipe is the same row to GFM.
    "contrast-row-without-trailing-pipe": lambda r: sub(
        r / CONTRAST, "| 17.76:1 | 4.5:1 | pass |", "| 17.76:1 | 4.5:1 | pass"),
    "scale-heading-under-table": lambda r: sub(r / SCALES, "| Hero |\n\n", "| Hero |\n### Notes\n\n"),
    "scale-example-in-a-fence-above": lambda r: sub(
        r / SCALES, "| Token | 16px / 1.20 ratio |",
        "```md\n| Token | 18px / 1.25 ratio |\n|---|---|\n| `--text-base` | 18px |\n```\n\n"
        "| Token | 16px / 1.20 ratio |"),
    # An alias with no $type of its own takes its target's type before its
    # group's, as the page and the format say: a colour aliased from a focus
    # group typed `dimension` is a colour, not a dimension with a wrong alias.
    "dtcg-alias-typed-before-group": lambda r: sub(
        r / SCHEMA, '  "space": {',
        '  "focus": {\n    "$type": "dimension",\n'
        '    "width": { "$value": { "value": 2, "unit": "px" } },\n'
        '    "colour": { "$value": "{color.gray.950}" }\n  },\n  "space": {'),
}


def _scale_no_separator(r: Path) -> None:
    p = r / SCALES
    lines = p.read_text(encoding="utf-8").split("\n")
    head = next(i for i, l in enumerate(lines) if "| 16px / 1.20 ratio |" in l)
    assert set(lines[head + 1].replace("|", "").strip()) <= set("-: "), lines[head + 1]
    first = lines[head + 2]
    assert "--text-" in first.split("|")[1]
    lines[head + 1:head + 3] = [first.replace(first.split("|")[2], " 0.75rem ", 1)]
    p.write_text("\n".join(lines), encoding="utf-8")


def run_figures(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(root / "design-tools" / "figures_check.py")],
                          capture_output=True, text=True)


def copy_repo(tmp: str) -> Path:
    copy = Path(tmp) / "repo"
    shutil.copytree(ROOT, copy, symlinks=True,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "node_modules"))
    return copy


def figures_fire() -> list[str]:
    if run_figures(ROOT).returncode != 0:
        return ["baseline (figures_check is already failing)"]
    bad = []
    for name, mutate in FIGURE_CASES.items():
        with tempfile.TemporaryDirectory() as tmp:
            copy = copy_repo(tmp)
            mutate(copy)
            r = run_figures(copy)
            if r.returncode == 0:
                bad.append(name)
                print(f"  figures/{name} did not fail")
            elif "Traceback" in r.stderr:
                bad.append(name)
                print(f"  figures/{name} crashed rather than reporting\n{r.stderr[-300:]}")
    return bad


def figures_green() -> list[str]:
    bad = []
    for name, mutate in FIGURE_GREEN_CASES.items():
        with tempfile.TemporaryDirectory() as tmp:
            copy = copy_repo(tmp)
            mutate(copy)
            r = run_figures(copy)
            if r.returncode != 0:
                bad.append(name)
                print(f"  figures-green/{name} failed\n{r.stdout}{r.stderr[-300:]}")
    return bad


# --- one case per branch, keyed by what that branch prints -------------------

@case("V1-description", "description is")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "How an interface behaves",
              "Designing, specifying, documenting and defending how an interface behaves")


@case("V2-terms", "contains 'rather than'")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "How an interface", "How, rather than guessing, an interface")


@case("V2-names", "names design-motion")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "How an interface", "design-motion. How an interface")


@case("V3-disk", "capabilities.yaml vs disk")
def _(r):
    p = r / "design-registry/capabilities.yaml"
    p.write_text(p.read_text(encoding="utf-8") + "\ndesign-phantom:\n  class: doc-write\n"
                 "  signals: [phantom work]\n", encoding="utf-8")


@case("V5-count", "playbooks (max")
def _(r):
    for i in range(9):
        (r / f"{S}design-ux/playbooks/extra{i}.md").write_text("<!-- design:guidance -->\n",
                                                               encoding="utf-8")


@case("V6-shared-total", "_design totals")
def _(r): sub(r / f"{S}_design/ROUTING.md", "## Rules for running a chain",
              "z\n" * 30 + "## Rules for running a chain")


@case("V6-repo-total", "repo markdown totals")
def _(r): (r / "NOTES.md").write_text("n\n" * 2000, encoding="utf-8")


@case("V10-no-signal", "no signal matches")
def _(r):
    p = r / "design-registry/fixtures.yaml"
    p.write_text(p.read_text(encoding="utf-8") + '\n- ask: "zzz qqq"\n  expect: design-ux\n',
                 encoding="utf-8")


@case("V14-loop", "is missing oracle")
def _(r): sub(r / "design-registry/routes.yaml", "  oracle:", "  oracle_was:")


@case("V14-stops", "is missing stops_at")
def _(r): sub(r / "design-registry/routes.yaml",
              '  stops_at: "each criterion passed', '  stopped: "each criterion passed')


@case("V17-section", "is not under")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "## Done when", "## Finished when")


@case("V17-duplicate", "needs exactly one")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "## Owns",
              "<!-- deliver:sizing -->\nstale\n<!-- /deliver:sizing -->\n\n## Owns")


@case("V24-readme", "README.md does not list design-motion")
def _(r):
    p = r / "README.md"
    p.write_text(p.read_text(encoding="utf-8").replace("design-motion", "the motion skill"),
                 encoding="utf-8")


@case("V24-unknown", "names design-i18n")
def _(r): sub(r / f"{S}_design/ROUTING.md", "`design-motion`", "`design-motion`, `design-i18n`")


@case("V27-outside", "points outside the repo")
def _(r):
    outside = r.parent / "elsewhere"
    outside.mkdir()
    (r / f"{S}design-ux/stray").symlink_to(outside)


@case("V27-deep", "points outside the repo")
def _(r):
    # A link below the top level reaches outside just the same.
    outside = r.parent / "elsewhere.md"
    outside.write_text("x\n", encoding="utf-8")
    ref = r / f"{S}design-ux/reference/spec-template.md"
    ref.unlink()
    ref.symlink_to(outside)


@case("V0-registry", "design-registry could not be read")
def _(r): (r / "design-registry/harness.yaml").write_text("", encoding="utf-8")


@case("V2-case", "contains 'rather than'")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "How an interface behaves",
              "Rather than looks, flow. How an interface behaves")


@case("V3-ondisk", "only on disk=['design-ghost']")
def _(r):
    (r / f"{S}design-ghost").mkdir()
    (r / f"{S}design-ghost/SKILL.md").write_text(
        "---\nname: design-ghost\ndescription: \"ghost work\"\n---\n", encoding="utf-8")


@case("V3-key", "only in yaml=['phantom']")
def _(r):
    p = r / "design-registry/capabilities.yaml"
    p.write_text(p.read_text(encoding="utf-8") + "\nphantom:\n  class: doc-write\n"
                 "  signals: [phantom work]\n", encoding="utf-8")


@case("V11-packs", "packs_needed_above")
def _(r): sub(r / "design-registry/harness.yaml", "packs_needed_above: 20",
              "packs_needed_above: 5")


@case("V13-empty", "chains no stage")
def _(r):
    p = r / "design-registry/routes.yaml"
    p.write_text(p.read_text(encoding="utf-8") + "\nghost:\n  pattern: linear\n",
                 encoding="utf-8")


@case("V14-empty", "has no oracle")
def _(r): sub(r / "design-registry/routes.yaml", '  oracle: "', '  oracle: ""  # "')


@case("V14-cycles", "max_cycles")
def _(r): sub(r / "design-registry/routes.yaml", "  max_cycles: 4", "  max_cycles:")


@case("V14-stops-empty", "has no stops_at")
def _(r): sub(r / "design-registry/routes.yaml",
              '  stops_at: "each criterion passed', '  stops_at: ""  # "each criterion passed')


@case("V15-writes", "writes")
def _(r): sub(r / "design-registry/harness.yaml",
              '    tools: "Read, Grep, Glob, Bash"\n    writes: false',
              '    tools: "Read, Grep, Glob, Bash"\n    writes: true')


@case("V16-fence", "is missing section 'Always / Never'")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "## Always / Never\n",
              "## Rules\n\n```text\n## Always / Never\n```\n")


@case("V16-template", "is missing section 'Always / Never'")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "## Always / Never\n",
              "## Rules\n\n```markdown\n## Always / Never\n```\n")


@case("V20-mention", "defines 'derived'")
def _(r): sub(r / f"{S}_design/PROVENANCE.md",
              "| `derived` | Computed from grounded inputs by a stated rule |",
              "| derived (see below) | Computed from grounded inputs by a stated rule |")


@case("V32-pinned", "pins its checker")
def _(r): sub(r / "design-registry/routes.yaml", "checker: ", "checker: codex  # ")


@case("V34-no-shell", "its class grants no Bash")
def _(r):
    sub(r / "design-registry/harness.yaml", "permission_classes:\n",
        'permission_classes:\n  view-only:\n    tools: "Read, Grep, Glob"\n    writes: false\n')
    sub(r / "design-registry/capabilities.yaml", "design-review:\n  class: read-only",
        "design-review:\n  class: view-only")


@case("V34-unknown", "which are not skills")
def _(r): sub(r / "design-registry/harness.yaml", "  refute.py: all", "  refute.py: [design-ghost]")


@case("V35-vocabulary", "PROVENANCE.md never defines")
def _(r):
    p = r / f"{S}_design/PROVENANCE.md"
    p.write_text(p.read_text(encoding="utf-8").replace("`platform`", "platform"), encoding="utf-8")


@case("V36-forms", "never names the 'mermaid' form")
def _(r):
    for g in (r / f"{S}design-review/playbooks/visualise.md",
              r / f"{S}design-review/reference/diagram-forms.md"):
        g.write_text(re.sub("mermaid", "graphviz", g.read_text(encoding="utf-8"), flags=re.I),
                     encoding="utf-8")


@case("V37-pin-head", "without the pinned version")
def _(r): sub(r / f"{S}design-a11y/reference/wcag22-checklist.md",
              "Source: WCAG 2.2 —", "Source: WCAG —")


@case("V37-pin-body", "and the page never says")
def _(r): sub(r / f"{S}design-a11y/reference/contrast.md",
              "| WCAG 2.2 SC 1.4.3 AA |", "| WCAG 2.1 SC 1.4.3 AA |")


@case("V8-titled", "links to missing missing.md")
def _(r): sub(r / "README.md", "## Files", "[guide](missing.md 'caption')\n\n## Files")


@case("V8-parens", "links to missing skills/_design/a(b).md")
def _(r): sub(r / "README.md", "## Files", "[odd](skills/_design/a(b).md)\n\n## Files")


@case("V8-not-a-fence", "links to missing gone.md")
def _(r): sub(r / "README.md", "## Files", "``` aa ```\n\n[bad](gone.md)\n\n## Files")


@case("V8-encoded-hash", "links to missing skills/_design/foo#bar.md")
def _(r): sub(r / "README.md", "## Files", "[doc](skills/_design/foo%23bar.md)\n\n## Files")


@case("V8-reference", "links to missing skills/_design/GONE.md")
def _(r): sub(r / "README.md", "## Files", "[r]: <skills/_design/GONE.md>\n\n## Files")


# The other direction: valid Markdown that must stay green. A rule that only
# ever meets violations can be wrong about every form it was not shown.
GREEN_CASES: dict[str, callable] = {
    # A marker with a trailing space is still the comment it was.
    "delivery-marker-trailing-space": lambda r: sub(
        r / f"{S}design-ux/SKILL.md", "<!-- deliver:values -->\n", "<!-- deliver:values --> \n"),
    # An example of a block, fenced, is not a second copy of the real one.
    "delivery-marker-example-in-a-fence": lambda r: sub(
        r / f"{S}design-ux/SKILL.md", "## Always / Never\n",
        "## Always / Never\n\n```md\n<!-- deliver:values -->\nan example\n<!-- /deliver:values -->\n```\n"),
    # An ATX heading may close with `#`s; the section is still `Done when`.
    "heading-with-closing-sequence": lambda r: sub(
        r / f"{S}design-ux/SKILL.md", "## Done when\n", "## Done when ##\n"),
    # The repository root is inside the repository: `Path.parents` leaves the
    # path itself out, and a link to the root read as one leaving it.
    "link-to-the-root": lambda r: sub(r / "README.md", "## Files",
                                      "[repository](.) and [up](skills/..)\n\n## Files"),
    # A reference link in Decide first takes its definition from anywhere on the
    # page; the section parsed alone read it as text, and V4 called the playbook
    # an orphan.
    "reference-link-in-decide-first": lambda r: (
        sub(r / f"{S}design-ux/SKILL.md", "[flows](playbooks/flows.md)", "[flows][flows]"),
        sub(r / f"{S}design-ux/SKILL.md", "## Done when", "[flows]: playbooks/flows.md\n\n## Done when")),
    "heading-with-pipes-is-not-a-value-set": lambda r: sub(
        r / f"{S}design-tokens/reference/export-targets.md", "## ", "## CSS | JSON\n\n## "),
    "indented-heading-with-pipes": lambda r: sub(
        r / f"{S}design-tokens/reference/export-targets.md", "## ", "   # CSS | JSON\n\n## "),
    "signal-matches-a-plural": lambda r: (r / "design-registry/fixtures.yaml").write_text(
        (r / "design-registry/fixtures.yaml").read_text(encoding="utf-8")
        + '\n- ask: "the page transitions feel janky"\n  expect: design-motion\n',
        encoding="utf-8"),
    "local-tool-dir-ignored": lambda r: (
        (r / ".venv").mkdir(),
        (r / ".venv/README.md").write_text("[x](missing.md)\n", encoding="utf-8")),
    "fence-indented-and-longer-close": lambda r: sub(
        r / "README.md", "## Files",
        "   ```md\n[example](not/a/real/file.md)\n````\n\n## Files"),
    "fence-unclosed-tilde-at-end": lambda r: (r / "NOTES.md").write_text(
        "# Notes\n\n~~~\n[example](nowhere.md)\n", encoding="utf-8"),
    "angle-reference-to-real-file": lambda r: sub(
        r / "README.md", "## Files", "[routing]: <skills/_design/ROUTING.md>\n\n## Files"),
    "balanced-parens-in-destination": lambda r: (
        (r / "skills/_design/a(b).md").write_text("<!-- design:contract -->\n", encoding="utf-8"),
        sub(r / "README.md", "## Files", "[odd](skills/_design/a(b).md)\n\n## Files")),
    "multi-backtick-code-span": lambda r: sub(
        r / "README.md", "## Files", "``[demo](missing.md)`` stays an example\n\n## Files"),
    "escaped-opener-is-text": lambda r: sub(
        r / "README.md", "## Files", "\\[not a link](missing.md)\n\n## Files"),
    "escaped-parens-in-destination": lambda r: (
        (r / "skills/_design/a(b).md").write_text("<!-- design:contract -->\n", encoding="utf-8"),
        sub(r / "README.md", "## Files", "[odd](skills/_design/a\\(b\\).md)\n\n## Files")),
    "marker-quoted-in-a-fence": lambda r: sub(
        r / "README.md", "## Files",
        "```\n#" + "TODO(agent): an example with no class\n```\n\n## Files"),
    "encoded-hash-in-filename": lambda r: (
        (r / "skills/_design/foo#bar.md").write_text("<!-- design:contract -->\n", encoding="utf-8"),
        sub(r / "README.md", "## Files",
            "[doc](skills/_design/foo%23bar.md#section)\n\n## Files")),
    "marker-in-a-span-across-lines": lambda r: sub(
        r / "README.md", "## Files", "a `quoted\n#" + "TODO(agent): example` b\n\n## Files"),
    "titled-link-to-real-file": lambda r: sub(
        r / "README.md", "## Files",
        "[routing](skills/_design/ROUTING.md 'routing') [r2](skills/_design/ROUTING.md (r))"
        "\n\n## Files"),
    # The parser numbers lines at "\n" alone; a U+2028 in prose above the
    # sections moved every line splitlines() read past it off its heading, and
    # the skill lost Decide first, Verify with and the rest.
    "line-separator-above-the-sections": lambda r: sub(
        r / f"{S}design-motion/SKILL.md", "## Owns", "A line\u2028inside it.\n\n## Owns"),
}


def greens_hold() -> list[str]:
    bad = []
    for name, mutate in GREEN_CASES.items():
        with tempfile.TemporaryDirectory() as tmp:
            copy = copy_repo(tmp)
            mutate(copy)
            out = run(copy)
            if "green" not in out.splitlines()[-1:][0]:
                bad.append(name)
                print(f"  green/{name} failed\n{out}")
    return bad


# --- cycle 4: branches no case isolated, and the false passes found at efbad21 ---

@case("V15-unknown", "declares unknown class")
def _(r): sub(r / "design-registry/capabilities.yaml", "design-ux:\n  class: doc-write",
              "design-ux:\n  class: superuser")


@case("V17-missing", "is missing the values delivery block")
def _(r):
    p = r / f"{S}design-ux/SKILL.md"
    p.write_text(re.sub(r"<!-- deliver:values -->.*?<!-- /deliver:values -->\n", "",
                        p.read_text(encoding="utf-8"), flags=re.S), encoding="utf-8")


@case("V28-prefix", "prefix is")
def _(r): sub(r / "design-registry/harness.yaml", "prefix: design-", "prefix: dsn-")


@case("V28-shared-name", "shared_dir is")
def _(r): sub(r / "design-registry/harness.yaml", "shared_dir: _design", "shared_dir: _shared")


@case("V28-shared-missing", "_shared/ does not exist")
def _(r): sub(r / "design-registry/harness.yaml", "shared_dir: _design", "shared_dir: _shared")


@case("V28-dot-dir", ".claude-plugin/ carries no set name")
def _(r): (r / ".claude-plugin").mkdir()


@case("V8-absolute", "an absolute path")
def _(r): sub(r / "README.md", "## Files", "[host](/etc/hostname)\n\n## Files")


@case("V8-name-too-long", "links to missing " + "a" * 300)
def _(r): sub(r / "README.md", "## Files", f"[long]({'a' * 300}.md)\n\n## Files")


@case("V10-whole-word", "no signal matches 'the emotional tone")
def _(r):
    p = r / "design-registry/fixtures.yaml"
    p.write_text(p.read_text(encoding="utf-8") + '\n- ask: "the emotional tone is wrong"\n'
                 "  expect: design-motion\n", encoding="utf-8")


@case("V22-template", "spec-template.md:")
def _(r): sub(r / f"{S}design-ux/reference/spec-template.md", "## 1. Goal\n",
              "## 1. Goal\n#" + "TODO(agent): fill the goal before handoff\n")


@case("V22-escaped-backtick", "README.md:")
def _(r): sub(r / "README.md", "## Files", "\\`#" + "TODO(agent): x\\`\n\n## Files")


@case("V22-line-separator", "README.md:")
def _(r): sub(r / "README.md", "## Files",
              "A line\u2028inside it.\n\n#" + "TODO(agent): unclassified\n```\nx\n```\n\n## Files")


@case("V22-line-after-multiline-span", "README.md:")
def _(r):
    p = r / "README.md"
    t = p.read_text(encoding="utf-8")
    marker = "#" + "TODO(agent): unclassified"
    t = t.replace("## Files", "a `code\nspan` b\n" + marker + "\n\n## Files", 1)
    p.write_text(t, encoding="utf-8")
    line = t.splitlines().index(marker) + 1
    MESSAGES["V22-line-after-multiline-span"] = f"README.md:{line} marker"


@case("V22-link-title", "README.md:")
def _(r): sub(r / "README.md", "## Files", '[x](README.md "#' + 'TODO(agent): note")\n\n## Files')


@case("V22-capitalised-template", "spec-template.md:")
def _(r):
    p = r / f"{S}design-ux/reference/spec-template.md"
    p.write_text(p.read_text(encoding="utf-8").replace("````markdown", "````Markdown", 1)
                 .replace("## 1. Goal\n", "## 1. Goal\n#" + "TODO(agent): fill\n", 1),
                 encoding="utf-8")


@case("V32-duplicate", "fewer than two distinct engines")
def _(r): sub(r / "design-registry/harness.yaml", "runs_on: [claude, codex, agy]",
              "runs_on: [claude, claude]")


@case("V38-comment", "switches on STUCK")
def _(r): sub(r / f"{S}_design/HANDOFF.md", "# DONE | PARTIAL | BLOCKED", "# DONE | PARTIAL | STUCK")


# A comment in a fence starts with "#" at column 0, as a heading does; only the
# parser knows which one it is.
@case("V38-comment-at-column-0", "switches on STUCK")
def _(r): sub(r / f"{S}design-tokens/reference/export-targets.md", "## ",
              "```yaml\n# DONE | PARTIAL | STUCK\n```\n\n## ")


# A signal starts a word, as V10 matches it; `forms` inside "platforms" is not it.
@case("V18-word-start", "signal 'forms' is not literal")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "loading states, forms, navigation,",
              "loading states, navigation on platforms,")


# A block inside a code fence is an example of one, not a delivered contract.
@case("V17-in-fence", "report block sits inside a code fence")
def _(r):
    sub(r / f"{S}design-ux/SKILL.md", "<!-- deliver:report -->", "~~~~text\n<!-- deliver:report -->")
    sub(r / f"{S}design-ux/SKILL.md", "<!-- /deliver:report -->", "<!-- /deliver:report -->\n~~~~")


# A marker sharing its line with anything else is neither the block nor absent.
@case("V17-marker-not-alone", "holds a values marker that is not alone on its line")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "<!-- deliver:values -->", "<!-- deliver:values --> see VALUES")


@case("V22-image-title", "README.md:")
def _(r): sub(r / "README.md", "## Files", '![x](a.png "#' + 'TODO(agent): note")\n\n## Files')


# The marker reported at its own line, not the first line that happens to hold
# the same words in a code span.
@case("V22-reference-title-line", "README.md:")
def _(r):
    p = r / "README.md"
    t = p.read_text(encoding="utf-8")
    marker = "#" + "TODO(agent): note"
    ref = f'[r]: README.md "{marker}"'
    t = t.replace("## Files", f"`{marker}`\n\n{ref}\n\n## Files", 1)
    p.write_text(t, encoding="utf-8")
    MESSAGES["V22-reference-title-line"] = f"README.md:{t.split(chr(10)).index(ref) + 1} marker"


# `make hooks` owns only the exact shim it writes. Anything else in git's
# pre-commit slot is the contributor's, including a hook that chains ours by
# hand — the earlier ownership test (a grep) overwrote that one on reinstall.
CHAINED = '#!/bin/sh\necho MINE\n"$(git rev-parse --show-toplevel)/design-tools/githooks/pre-commit" || exit 1\n'
FOREIGN = "#!/bin/sh\necho OTHER\n"
MENTION_ONLY = "#!/bin/sh\n# later: design-tools/githooks/pre-commit\nexit 0\n"
# What an earlier `make hooks` wrote: ours, so replaced by the current shim.
LEGACY = '#!/bin/sh\nexec "$(git rev-parse --show-toplevel)/design-tools/githooks/pre-commit" "$@"\n'
# What the first `make hooks` copied in (013f05b): ours too, and it checks the
# working tree, so a staged violation passed it.
COPIED = ('#!/bin/sh\n# Budgets enforced by a mechanism rather than by remembering.\n'
          '# Install with: make hooks\nset -e\n'
          'python3 "$(git rev-parse --show-toplevel)/design-tools/validate.py"\n'
          'python3 "$(git rev-parse --show-toplevel)/design-tools/figures_check.py"\n')


def hooks_hold() -> list[str]:
    bad = []
    with tempfile.TemporaryDirectory() as tmp:
        # A core.hooksPath someone else set — a global hooks directory — is
        # refused: a shim written there would run in every repository.
        repo = copy_repo(tmp)
        elsewhere = Path(tmp) / "global-hooks"
        elsewhere.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "core.hooksPath", str(elsewhere)],
                       check=True)
        r = subprocess.run(["make", "-s", "-C", str(repo), "hooks"], capture_output=True, text=True)
        if r.returncode == 0 or any(elsewhere.iterdir()):
            bad.append("foreign core.hooksPath written to")
        # ...and validate.py does not send the contributor to make hooks, which refuses.
        if "managed by core.hooksPath" not in run(repo):
            bad.append("foreign core.hooksPath status points at make hooks")
        # The old setting in the user's global config is not this checkout's to
        # unset: no claim that it was removed, and nothing installed.
        glob = Path(tmp) / "gitconfig"
        glob.write_text("[core]\n\thooksPath = design-tools/githooks\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "config", "--unset", "core.hooksPath"], check=True)
        r = subprocess.run(["make", "-s", "-C", str(repo), "hooks"], capture_output=True, text=True,
                           env={**os.environ, "GIT_CONFIG_GLOBAL": str(glob)})
        if r.returncode == 0 or "removed core.hooksPath" in r.stdout:
            bad.append("global legacy core.hooksPath reported as removed")
        subprocess.run(["git", "-C", str(repo), "config", "core.hooksPath", str(elsewhere)],
                       check=True)
        # The shim does nothing where the tracked hook is absent (an orphan branch).
        subprocess.run(["git", "-C", str(repo), "config", "--unset", "core.hooksPath"], check=True)
        subprocess.run(["make", "-s", "-C", str(repo), "hooks"], capture_output=True, check=True)
        (repo / "design-tools" / "githooks" / "pre-commit").unlink()
        shim = subprocess.run(["sh", str(repo / ".git" / "hooks" / "pre-commit")], cwd=repo,
                              capture_output=True, text=True)
        if shim.returncode != 0:
            bad.append(f"shim fails without the tracked hook ({shim.stderr.strip()[:60]})")
    # Any hook that is not exactly the shim is left alone and the target fails:
    # nothing was installed, and whether that hook runs the rules is not knowable
    # from its text (a comment can name the path; a 0644 file is skipped by git).
    for name, before, want_rc, keep in (("fresh", None, 0, False), ("chained", CHAINED, 2, True),
                                        ("chained-not-executable", CHAINED, 2, True),
                                        ("mention-only", MENTION_ONLY, 2, True),
                                        ("foreign", FOREIGN, 2, True), ("hookspath", None, 0, False),
                                        ("legacy-shim", LEGACY, 0, False),
                                        ("legacy-copy", COPIED, 0, False)):
        with tempfile.TemporaryDirectory() as tmp:
            repo = copy_repo(tmp)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            hook = repo / ".git" / "hooks" / "pre-commit"
            hook.parent.mkdir(parents=True, exist_ok=True)
            if before is not None:
                hook.write_text(before, encoding="utf-8")
                hook.chmod(0o644 if name == "chained-not-executable" else 0o755)
            if name == "hookspath":
                subprocess.run(["git", "-C", str(repo), "config", "core.hooksPath",
                                "design-tools/githooks"], check=True)
            r = subprocess.run(["make", "-s", "-C", str(repo), "hooks"],
                               capture_output=True, text=True)
            after = hook.read_text(encoding="utf-8") if hook.exists() else ""
            left = subprocess.run(["git", "-C", str(repo), "config", "--get", "core.hooksPath"],
                                  capture_output=True, text=True).stdout.strip()
            ok = r.returncode == want_rc and not left
            ok = ok and (after == before if keep else
                         "design-tools/githooks/pre-commit" in after and after != before)
            if not ok:
                bad.append(f"{name} (exit {r.returncode}, hooksPath {left!r})")
            # validate.py says "hooks on" for the shim make hooks writes, and for
            # nothing else: a stale copy reported as on was trusted for months.
            if ("hooks on" in run(repo)) == keep:
                bad.append(f"{name} (validate reports hooks {'on' if keep else 'not on'})")
    # git skips a shim it cannot execute and lets the commit through, so a
    # shim without its executable bit is not "on".
    with tempfile.TemporaryDirectory() as tmp:
        repo = copy_repo(tmp)
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(["make", "-s", "-C", str(repo), "hooks"], capture_output=True, check=True)
        (repo / ".git" / "hooks" / "pre-commit").chmod(0o644)
        if "hooks on" in run(repo):
            bad.append("non-executable shim reported as on")
    # A dangling link in the slot is someone's hook manager whose target is not
    # there yet; writing through it puts the shim outside .git.
    with tempfile.TemporaryDirectory() as tmp:
        repo = copy_repo(tmp)
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        hook = repo / ".git" / "hooks" / "pre-commit"
        hook.parent.mkdir(parents=True, exist_ok=True)
        target = Path(tmp) / "managed" / "team-hook"
        target.parent.mkdir()
        hook.symlink_to(target)
        r = subprocess.run(["make", "-s", "-C", str(repo), "hooks"], capture_output=True, text=True)
        if r.returncode == 0 or target.exists() or not hook.is_symlink():
            bad.append(f"dangling-link (exit {r.returncode}, written through {target.exists()})")
        # The status reads the slot, not what it points at: a link is someone
        # else's whether its target is missing or holds the shim word for word.
        if "managed by a symlink" not in run(repo):
            bad.append("dangling-link status")
        target.write_text(validate.HOOK_SHIM, encoding="utf-8")
        if "managed by a symlink" not in run(repo):
            bad.append("link-to-shim status")
    return bad


def engine_holds() -> list[str]:
    """engine.py, against a stand-in codex on PATH: a request without
    --running is refused rather than answered with a selftest, an engine that
    exits non-zero has not answered, and a prompt is never read as an option."""
    bad = []
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        log = d / "argv"
        stub = d / "bin" / "codex"
        stub.parent.mkdir()
        # Writes a valid answer to the -o path, logs its argv, exits $CODE.
        stub.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$LOG"\n'
                        'while [ $# -gt 0 ]; do [ "$1" = -o ] && out="$2"; shift; done\n'
                        'printf \'{"ok": true}\' > "$out"\nexit "$CODE"\n', encoding="utf-8")
        stub.chmod(0o755)
        (d / "p.txt").write_text("--help me\n", encoding="utf-8")
        (d / "s.json").write_text(json.dumps(
            {"type": "object", "properties": {"ok": {"type": "boolean"}},
             "required": ["ok"]}), encoding="utf-8")
        # Only the stand-in and the system shell tools: a real engine CLI on the
        # contributor's PATH is never started, whatever engine.py does.
        env = {**os.environ, "PATH": os.pathsep.join([str(stub.parent), "/usr/bin", "/bin"]),
               "LOG": str(log)}

        def ask(code: str, *extra: str) -> subprocess.CompletedProcess:
            return subprocess.run([sys.executable, str(ROOT / "design-tools" / "engine.py"),
                                   *extra, "--prompt-file", str(d / "p.txt"),
                                   "--schema", str(d / "s.json")],
                                  capture_output=True, text=True, env={**env, "CODE": code})

        r = ask("0")
        if r.returncode != 2:
            bad.append(f"no --running (exit {r.returncode})")
        r = ask("0", "codex", "--running", "claude")
        if r.returncode != 0:
            bad.append(f"stand-in answer refused (exit {r.returncode}: {r.stderr[-120:]})")
        else:
            argv = log.read_text(encoding="utf-8").split("\n")
            if "--help me" not in argv:
                bad.append("prompt never reached codex")
            elif argv[argv.index("--help me") - 1] != "--":
                bad.append("prompt passed where codex reads options")
        r = ask("2", "codex", "--running", "claude")
        if r.returncode != 1:
            bad.append(f"engine exited 2 and was taken as answering (exit {r.returncode})")
        # Input that cannot be read is refused (2), never reported as an engine
        # that did not answer (1) by way of a traceback.
        (d / "s.json").write_text("{not json", encoding="utf-8")
        r = ask("0", "codex", "--running", "claude")
        if r.returncode != 2 or "Traceback" in r.stderr:
            bad.append(f"unreadable schema (exit {r.returncode})")
        # A schema that parses but cannot be checked is refused input too: a
        # list of properties was a traceback, and an unsupported keyword exit 1.
        for name, schema in {"properties-list": {"type": "object", "properties": [{"type": "string"}]},
                             "required-string": {"type": "object", "required": "ok"},
                             "enum": {"type": "object", "properties":
                                      {"a": {"type": "string", "enum": ["x"]}}}}.items():
            (d / "s.json").write_text(json.dumps(schema), encoding="utf-8")
            r = ask("0", "codex", "--running", "claude")
            if r.returncode != 2 or "Traceback" in r.stderr:
                bad.append(f"uncheckable schema {name} (exit {r.returncode})")
        # A checker that is not an engine is refused input, not one that failed to
        # answer. The schema is a checkable one again, or the refusal is the schema's.
        (d / "s.json").write_text(json.dumps(
            {"type": "object", "properties": {"ok": {"type": "boolean"}},
             "required": ["ok"]}), encoding="utf-8")
        r = ask("0", "nosuch", "--running", "claude")
        if r.returncode != 2 or "Traceback" in r.stderr:
            bad.append(f"unknown checker (exit {r.returncode})")
        # So is naming the running engine as its own checker: nothing was asked.
        r = ask("0", "codex", "--running", "codex")
        if r.returncode != 2 or "Traceback" in r.stderr:
            bad.append(f"checker is the running engine (exit {r.returncode})")
    bad += _engine_in_process()
    return bad


def _alive(pid: int) -> bool:
    """Running, not merely a zombie no init has reaped yet."""
    try:
        stat = Path(f"/proc/{pid}/stat").read_text()
    except OSError:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        return True
    return stat.rsplit(")", 1)[1].split()[0] != "Z"


def _outlives(pid: int) -> bool:
    """Still running three seconds on: SIGKILL lands asynchronously."""
    for _ in range(30):
        if not _alive(pid):
            return False
        time.sleep(0.1)
    return True


def _engine_in_process() -> list[str]:
    """What only the module can show: output nested past the decoder is an
    engine that did not answer, never a traceback that loses the rest of a
    refute run; and a timeout ends what the engine started, not only the
    engine, so a child holding its output cannot outlive the run."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("engine", ROOT / "design-tools" / "engine.py")
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    bad = []
    deep = '{"structured_output": ' + "[" * 200000 + "]" * 200000 + "}"
    try:
        engine._parse("claude", deep)
        bad.append("output nested past the decoder parsed")
    except engine.EngineError:
        pass
    except RecursionError:
        bad.append("output nested past the decoder raised RecursionError")
    with tempfile.TemporaryDirectory() as tmp:
        pidfile = Path(tmp) / "pid"
        engine.TIMEOUT = 5         # room for a loaded runner to start the stand-in
        try:
            engine._spawn("claude", ["sh", "-c", f'sleep 60 & echo $! > "{pidfile}"; sleep 60'],
                          Path(tmp))
            bad.append("a run past its timeout returned")
        except engine.EngineError:
            pass
        pid = int(pidfile.read_text().strip()) if pidfile.exists() else None
        if pid is None:
            bad.append("the timeout stand-in never started its child")
        elif _outlives(pid):
            os.kill(pid, 9)
            bad.append("a timed-out engine's child kept running")
    return bad


def render_holds() -> list[str]:
    """render.py leaves a file alone when any of its blocks cannot be delivered.
    Interleaved markers let the first block swallow the second's opener, and the
    file was written while the run reported failure — hiding the cause from the
    next run."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = copy_repo(tmp)
        page = repo / f"{S}design-ux/SKILL.md"
        sub(page, "<!-- /deliver:sizing -->\n<!-- deliver:ground -->",
            "<!-- deliver:ground -->\n<!-- /deliver:sizing -->")
        before = page.read_text(encoding="utf-8")
        r = subprocess.run([sys.executable, str(repo / "design-tools" / "render.py")],
                           capture_output=True, text=True)
        if r.returncode == 0 or page.read_text(encoding="utf-8") != before:
            return [f"interleaved markers (exit {r.returncode}, file rewritten "
                    f"{page.read_text(encoding='utf-8') != before})"]
    bad = []
    # An existing pair is rewritten in place only where validate accepts it:
    # markers inside a fence are an example, and a block under another heading
    # is not delivered. Both printed "rendered" and exited 0 over a file validate
    # then failed, and no later run could change that.
    for name, mutate in (
            ("markers-in-a-fence", lambda text: re.sub(
                r"<!-- deliver:surface -->.*?<!-- /deliver:surface -->\n", "", text, flags=re.S
            ).replace("## Done when\n", "## Done when\n\n```md\n<!-- deliver:surface -->\n"
                      "old words\n<!-- /deliver:surface -->\n```\n", 1)),
            ("block-under-another-heading", lambda text: (lambda m: text.replace(m, "").replace(
                "## Verify with\n", "## Verify with\n" + m, 1))(
                re.search(r"<!-- deliver:surface -->.*?<!-- /deliver:surface -->\n", text, re.S).group(0)))):
        with tempfile.TemporaryDirectory() as tmp:
            repo = copy_repo(tmp)
            page = repo / f"{S}design-ux/SKILL.md"
            page.write_text(mutate(page.read_text(encoding="utf-8")), encoding="utf-8")
            before = page.read_text(encoding="utf-8")
            r = subprocess.run([sys.executable, str(repo / "design-tools" / "render.py")],
                               capture_output=True, text=True)
            if r.returncode == 0 or page.read_text(encoding="utf-8") != before:
                bad.append(f"{name} (exit {r.returncode}, file rewritten "
                           f"{page.read_text(encoding='utf-8') != before})")
    # A trailing space leaves a marker the comment it was: reading it as absent
    # appended a second block and left the first, stale, where nothing looked.
    with tempfile.TemporaryDirectory() as tmp:
        repo = copy_repo(tmp)
        page = repo / f"{S}design-ux/SKILL.md"
        clean = page.read_text(encoding="utf-8")
        page.write_text(clean.replace("<!-- deliver:values -->\n", "<!-- deliver:values --> \n", 1)
                        .replace("<!-- /deliver:values -->\n", "<!-- /deliver:values -->\t\n", 1),
                        encoding="utf-8")
        r = subprocess.run([sys.executable, str(repo / "design-tools" / "render.py")],
                           capture_output=True, text=True)
        if r.returncode != 0 or page.read_text(encoding="utf-8") != clean:
            bad.append(f"marker-with-trailing-space (exit {r.returncode}, "
                       f"{page.read_text(encoding='utf-8').count('<!-- deliver:values')} blocks)")
    # A marker sharing its line is refused, and one fenced beside the real block
    # is an example the real block does not clash with.
    for name, old, new, refused in (
            ("marker-not-alone", "<!-- deliver:values -->\n", "<!-- deliver:values --> see VALUES\n", True),
            ("example-beside-the-block", "## Always / Never\n",
             "## Always / Never\n\n```md\n<!-- deliver:values -->\nan example\n<!-- /deliver:values -->\n```\n",
             False)):
        with tempfile.TemporaryDirectory() as tmp:
            repo = copy_repo(tmp)
            page = repo / f"{S}design-ux/SKILL.md"
            sub(page, old, new)
            before = page.read_text(encoding="utf-8")
            r = subprocess.run([sys.executable, str(repo / "design-tools" / "render.py")],
                               capture_output=True, text=True)
            if (r.returncode == 0) == refused or page.read_text(encoding="utf-8") != before:
                bad.append(f"{name} (exit {r.returncode}, file rewritten "
                           f"{page.read_text(encoding='utf-8') != before})")
    # A new block goes under the section's own `## ` heading, at its end: not
    # under a `### ` line with the same title, and not into a code fence whose
    # example holds a `## ` line. Either way the result has to be what
    # validate accepts, and the block has to be outside the fence.
    for name, extra, where in (
            ("h3-of-the-same-name", "### Verify with\n", "## Owns\n"),
            ("heading-in-a-fence", "```text\n## Findings\nstatus: DONE\n```\n", "## Verify with\n")):
        with tempfile.TemporaryDirectory() as tmp:
            repo = copy_repo(tmp)
            page = repo / f"{S}design-ux/SKILL.md"
            text = re.sub(r"<!-- deliver:report -->.*?<!-- /deliver:report -->\n", "",
                          page.read_text(encoding="utf-8"), flags=re.S)
            page.write_text(text.replace(where, where + "\n" + extra, 1), encoding="utf-8")
            r = subprocess.run([sys.executable, str(repo / "design-tools" / "render.py")],
                               capture_output=True, text=True)
            out = run(repo)
            if r.returncode != 0 or "green" not in out.splitlines()[-1]:
                bad.append(f"{name} (exit {r.returncode}): {out.strip().splitlines()[-2:]}")
    return bad


def hook_reads_the_index() -> list[str]:
    """The pre-commit hook checks every staged file, including the ones a sparse
    checkout marks skip-worktree and leaves out of the working tree. Exporting
    the index without them failed every commit on files nobody had touched."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = copy_repo(tmp)
        git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], check=True,
                                         capture_output=True, text=True)
        git("init", "-q")
        git("add", "-A")
        page = f"{S}design-ux/SKILL.md"
        git("update-index", "--skip-worktree", page)
        (repo / page).unlink()
        r = subprocess.run(["sh", str(repo / "design-tools/githooks/pre-commit")],
                           cwd=repo, capture_output=True, text=True)
        if r.returncode != 0:
            return [f"a skip-worktree file left out (exit {r.returncode}): "
                    f"{(r.stdout + r.stderr).strip().splitlines()[-1:]}"]
    return []


def hooks_fail_closed() -> tuple[list[str], int]:
    """`make hooks` says it installed only what it wrote, where git looks.

    Outside a checkout `--git-path` printed nothing and the hook path became
    `/pre-commit`: the failed write still printed "installed" and exited 0, and
    as root it was written. That case writes to `/` if it regresses, so it is
    run only where a write there is refused."""
    bad, ran = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        # A hooks directory that cannot be made: the write fails, and says so.
        repo = copy_repo(tmp + "/blocked")
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        hooks = repo / ".git/hooks"
        shutil.rmtree(hooks, ignore_errors=True)
        hooks.write_text("", encoding="utf-8")
        r = subprocess.run(["make", "-s", "-C", str(repo), "hooks"], capture_output=True, text=True)
        ran += 1
        if r.returncode == 0 or "installed at" in r.stdout:
            bad.append("an unwritable hook reported as installed")
        if os.geteuid() == 0:
            print("  not run here: as root, a regressed make hooks outside a checkout writes /pre-commit")
            return bad, ran
        bare = copy_repo(tmp + "/archive")
        r = subprocess.run(["make", "-s", "-C", str(bare), "hooks"], capture_output=True, text=True,
                           env={**os.environ, "GIT_CEILING_DIRECTORIES": tmp})
        ran += 1
        if r.returncode == 0 or "installed at" in r.stdout:
            bad.append("make hooks outside a checkout reported success")
    return bad, ran


def link_holds() -> list[str]:
    """`make link` and `make unlink` fail when a link could not be made or
    removed, rather than printing the success line over the error. A read-only
    directory does not stop root, so as root the case cannot be made."""
    bad = []
    if os.geteuid() == 0:
        print("  not run here: root writes into a read-only directory")
        return bad
    with tempfile.TemporaryDirectory() as tmp:
        dirs = {v: str(Path(tmp) / v.lower() / "skills") for v in
                ("CLAUDE_DIR", "CODEX_DIR", "AGY_DIR")}
        args = [f"{k}={v}" for k, v in dirs.items()]
        locked = Path(dirs["CLAUDE_DIR"])
        locked.mkdir(parents=True)
        for target in ("link", "unlink"):
            if target == "unlink":
                locked.chmod(0o755)
                subprocess.run(["make", "-s", "-C", str(ROOT), "link", *args],
                               capture_output=True, check=True)
            locked.chmod(0o555)
            r = subprocess.run(["make", "-s", "-C", str(ROOT), target, *args],
                               capture_output=True, text=True)
            locked.chmod(0o755)
            if r.returncode == 0:
                bad.append(f"{target} into a read-only directory exited 0")
    return bad


def git_corpus_holds() -> tuple[list[str], int]:
    """In a checkout the corpus is what git would commit: a contributor's empty
    `.cache/`, an ignored `.venv/` or a worktree nested under the checkout stays
    out, and a dot-directory git would commit stays in. Returns the failures and
    how many cases ran."""
    bad, ran = [], 3
    with tempfile.TemporaryDirectory() as tmp:
        repo = copy_repo(tmp)
        git = ["git", "-C", str(repo)]
        subprocess.run(git[:1] + ["init", "-q", str(repo)], check=True)
        subprocess.run(git + ["add", "-A"], check=True)
        (repo / ".cache").mkdir()
        (repo / ".venv").mkdir()
        (repo / ".venv" / "README.md").write_text("[x](missing.md)\n", encoding="utf-8")
        nested = repo / ".worktrees" / "feat"
        nested.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(nested)], check=True)
        (nested / "NOTES.md").write_text("[x](missing.md)\n" * 3000, encoding="utf-8")
        # A tool directory nobody ignored is still the contributor's.
        (repo / "node_modules" / "pkg").mkdir(parents=True)
        (repo / "node_modules" / "pkg" / "README.md").write_text("[x](missing.md)\n",
                                                                 encoding="utf-8")
        if "green" not in run(repo):
            bad.append("contributor-local directories counted")
        # A name that is not UTF-8 is still a file git would commit. A filesystem
        # that refuses such a name (APFS: EILSEQ) cannot hold one to drop, so the
        # case is reported as not run there rather than crashing every case after it.
        odd = Path(os.fsdecode(os.fsencode(repo) + b"/NOTES-\xff.md"))
        try:
            odd.write_text("[x](missing.md)\n", encoding="utf-8")
        except OSError as e:
            if e.errno != errno.EILSEQ:
                raise
            print("  not run here: this filesystem refuses non-UTF-8 file names")
            ran -= 1
        else:
            if "V8: NOTES-" not in run(repo):
                bad.append("a non-UTF-8 file name dropped out of the corpus")
            odd.unlink()
        plugin = repo / ".claude-plugin"
        plugin.mkdir()
        (plugin / "README.md").write_text("[x](missing.md)\n", encoding="utf-8")
        out = run(repo)
        if "V28: .claude-plugin/" not in out or "V8: .claude-plugin/README.md" not in out:
            bad.append("a committable dot-directory escaped the checks")
    return bad, ran


def main() -> int:
    baseline = run(ROOT)
    if "green" not in baseline:
        print("the working tree is already failing; fix that first:\n" + baseline)
        return 1

    bad: list[str] = []
    for rule, mutate in CASES.items():
        with tempfile.TemporaryDirectory() as tmp:
            copy = copy_repo(tmp)
            mutate(copy)
            out = run(copy)
            expect = rule.split("-")[0]
            says = re.escape(MESSAGES.get(rule, ""))
            # A rule that crashed is not a rule that fired: "could not run" also
            # carries the rule id, and a deleted guard ends in exactly that.
            if not re.search(rf"^\s*{expect}: (?!could not run).*{says}", out, re.M):
                bad.append(rule)
                print(f"  {rule} did not fire\n{out}")

    print(f"{len(CASES)} rules exercised, {len(bad)} silent")
    if bad:
        print("silent: " + ", ".join(bad))
        return 1

    # Counting the cases that exist says nothing about the rules that do. A rule
    # added without a case left this printing "every rule fires" about it.
    covered = {c.split("-")[0] for c in CASES}
    declared = {fn.__name__.split("_")[0].upper() for fn in validate.RULES}
    untested = sorted(declared - covered, key=lambda r: int(r[1:]))
    if untested:
        print("no deliberate violation is injected for: " + ", ".join(untested))
        return 1
    print(f"every rule fires ({len(declared)} rules, {len(CASES)} cases)")

    broken = greens_hold()
    if broken:
        print("valid input rejected: " + ", ".join(broken))
        return 1
    print(f"every valid form stays green ({len(GREEN_CASES)} cases)")

    import engine
    schema_cases = [  # (value, schema, should it pass)
        (None, {"type": ["string", "null"]}, True),
        (3, {"type": ["string", "null"]}, False),
        (True, {"type": "integer"}, False),
        ({"refuted": "false"}, {"type": "object", "required": ["refuted"],
                                "properties": {"refuted": {"type": "boolean"}}}, False),
        ({}, {"type": "object", "required": ["refuted"]}, False),
        ({"a": 1}, {"type": "object", "properties": {"a": {"type": "weird"}}}, False),
        ({"ok": True, "extra": 1}, engine.strict(
            {"type": "object", "properties": {"ok": {"type": "boolean"}}}), False),
        ({"ok": True}, engine.strict(
            {"type": "object", "properties": {"ok": {"type": "boolean"}}}), True),
        ({"ok": True, "extra": 1}, engine.strict(
            {"type": ["object", "null"], "properties": {"ok": {"type": "boolean"}}}), False),
        (None, engine.strict(
            {"type": ["object", "null"], "properties": {"ok": {"type": "boolean"}}}), True),
    ]
    wrong = [i for i, (v, s, ok) in enumerate(schema_cases)
             if (engine.mismatch(v, s) is None) != ok]
    # Schemas mismatch() cannot hold an answer to are refused, not half-checked.
    unread = [{"anyOf": [{"type": "boolean"}]}, {"type": "string", "enum": ["A"]},
              {"$ref": "#/x"}, {"type": "object", "additionalProperties": {"type": "number"}},
              {"type": "object", "properties": {"v": {"oneOf": []}}},
              {"properties": {"ok": {"type": "boolean"}}, "required": ["ok"]},   # no type
              {"type": "objekt"}, {"type": ["string", ["null"]]}, {"type": {"a": 1}}]
    wrong += [f"unsupported:{i}" for i, s in enumerate(unread) if engine.unsupported(s) is None]
    if engine.unsupported({"type": "object", "required": ["ok"], "properties":
                           {"ok": {"type": "boolean", "description": "d"}}}) is not None:
        wrong.append("supported schema refused")
    if wrong:
        print(f"engine.mismatch decided wrongly on schema cases {wrong}")
        return 1
    print(f"engine answers are held to their schema ({len(schema_cases)} cases)")

    import refute
    full, part = 2, 1
    exit_cases = [  # (verdicts with readings, expected exit status)
        ([("STANDS", full)], 0),
        ([("STANDS", part)], 1),
        ([("UNCHECKED", 0)], 1),
        ([("STANDS", full), ("REFUTED", full)], 3),
        ([("CONTESTED", full), ("UNCHECKED", 0)], 3),
    ]
    # An empty pool asked nobody: that is never "every claim stands".
    if refute.exit_status([{"verdict": "UNCHECKED", "independent_readings": 0}], 0) != 1:
        exit_cases.append(([], -1))
    off = [i for i, (rs, want) in enumerate(exit_cases)
           if refute.exit_status([{"verdict": v, "independent_readings": n} for v, n in rs],
                                 full) != want]
    if off:
        print(f"refute exit status wrong on cases {off}")
        return 1
    # Refused input exits 2 before any engine is asked, whatever is wrong with it.
    with tempfile.TemporaryDirectory() as tmp:
        bad_inputs = {"missing": Path(tmp) / "none.json", "not-json": Path(tmp) / "bad.json",
                      "not-utf8": Path(tmp) / "bin.json", "no-claim": Path(tmp) / "empty.json"}
        bad_inputs["not-json"].write_text("{bad", encoding="utf-8")
        bad_inputs["not-utf8"].write_bytes(b"\xff\xfe\x00")
        bad_inputs["no-claim"].write_text('[{"id": "x"}]', encoding="utf-8")
        bad_inputs["too-deep"] = Path(tmp) / "deep.json"
        bad_inputs["too-deep"].write_text("[" * 100000 + "]" * 100000, encoding="utf-8")
        for name, path in bad_inputs.items():
            r = subprocess.run([sys.executable, str(ROOT / "design-tools" / "refute.py"),
                                "--running", "claude", str(path)], capture_output=True, text=True)
            if r.returncode != 2 or "Traceback" in r.stderr:
                off.append(f"input:{name}={r.returncode}")
        # One engine declared leaves nobody to refute with: refused, exit 2.
        lone = copy_repo(tmp + "/lone")
        sub(lone / "design-registry/harness.yaml", "runs_on: [claude, codex, agy]",
            "runs_on: [claude]")
        (lone / "c.json").write_text('[{"id": "x", "claim": "y"}]', encoding="utf-8")
        r = subprocess.run([sys.executable, str(lone / "design-tools" / "refute.py"),
                            "--running", "claude", str(lone / "c.json")],
                           capture_output=True, text=True)
        if r.returncode != 2 or "no engine but" not in r.stderr:
            off.append(f"empty-pool={r.returncode}")
    if off:
        print(f"refute refused input wrongly: {off}")
        return 1
    print(f"refute's exit status says what happened ({len(exit_cases)} cases, "
          f"{len(bad_inputs)} refused inputs, empty pool)")

    git_bad, git_ran = git_corpus_holds()
    if git_bad:
        print("git-visible corpus wrong: " + ", ".join(git_bad))
        return 1
    print(f"in a checkout, the corpus is what git would commit ({git_ran} cases)")

    broken_hooks = hooks_hold()
    if broken_hooks:
        print("make hooks mishandled: " + ", ".join(broken_hooks))
        return 1
    print("make hooks leaves every hook but its own shim alone (13 cases)")

    hooks_open, hooks_ran = hooks_fail_closed()
    if hooks_open:
        print("make hooks claimed an install: " + ", ".join(hooks_open))
        return 1
    print(f"make hooks fails where it wrote nothing ({hooks_ran} cases)")

    broken_hook = hook_reads_the_index()
    if broken_hook:
        print("the pre-commit hook mishandled: " + ", ".join(broken_hook))
        return 1
    print("the pre-commit hook checks every staged file, sparse or not (1 case)")

    broken_engine = engine_holds()
    if broken_engine:
        print("engine.py mishandled: " + ", ".join(broken_engine))
        return 1
    print("engine.py refuses what it cannot check, against a stand-in engine (11 cases)")

    broken_render = render_holds()
    if broken_render:
        print("render.py mishandled: " + ", ".join(broken_render))
        return 1
    print("render.py writes nothing it could not fully deliver, and only under the real heading (8 cases)")

    broken_link = link_holds()
    if broken_link:
        print("make link mishandled: " + ", ".join(broken_link))
        return 1
    print("make link and unlink fail when a link cannot be made or removed (2 cases)")

    silent_figures = figures_fire()
    if silent_figures:
        print("figures_check stayed green on: " + ", ".join(silent_figures))
        return 1
    print(f"every figure check fails when it should ({len(FIGURE_CASES)} cases)")

    red_figures = figures_green()
    if red_figures:
        print("figures_check failed a correct page: " + ", ".join(red_figures))
        return 1
    print(f"a correct page stays green whatever surrounds its tables "
          f"({len(FIGURE_GREEN_CASES)} cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
