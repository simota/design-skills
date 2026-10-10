#!/usr/bin/env python3
"""Prove each rule in validate.py fires, and each recomputation in figures_check.py.

A check only ever seen passing may be checking nothing. Every rule below gets a
deliberate violation injected into a throwaway copy of the repo, and the test
fails if the validator stays quiet.

Run: make test
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True                     # no __pycache__ in the tools dir
import validate                                    # noqa: E402  — for RULES only


def run(root: Path) -> str:
    r = subprocess.run([sys.executable, str(root / "design-tools" / "validate.py")],
                       capture_output=True, text=True)
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
def _(r): sub(r / f"{S}design-ux/SKILL.md", "Designing how an interface behaves",
              "Not for design-motion. Designing how an interface behaves")


@case("V3")
def _(r): (r / f"{S}design-ghost").mkdir(); (r / f"{S}design-ghost/SKILL.md").write_text("x")


@case("V3-name")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "name: design-ux", "name: design-behaviour")


@case("V3-yaml")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "description: \"", "description: \"\"")


@case("V4")
def _(r): (r / f"{S}design-ux/playbooks/orphan.md").write_text("<!-- design:guidance -->\n")


@case("V5")
def _(r): (r / f"{S}design-ux/playbooks/forms.md").write_text("y\n" * 400)


@case("V6")
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


@case("V10-empty")
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


@case("V24")
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


@case("V28")
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


@case("V34-none-declared")
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


@case("V36-none-declared")
def _(r): sub(r / "design-registry/harness.yaml", "finding_visuals:", "unused_visuals:")


@case("V38")
def _(r): sub(r / f"{S}design-a11y/playbooks/content.md", "## ", "verdict: KEEP | DROP\n\n## ")


@case("V37")
def _(r):
    """A page that leans on a declared source and does not say so."""
    sub(r / f"{S}design-a11y/reference/wcag22-checklist.md",
        'Source: WCAG 2.2 — summaries, not verbatim criteria; check applicability and exceptions.',
        "Source: none — nothing outside this page can move what it states.")


@case("V37-unused")
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


@case("V37-none-declared")
def _(r): sub(r / "design-registry/harness.yaml", "source_authorities:", "unused_authorities:")


# figures_check.py is held to the same standard: each recomputation is shown
# failing on a deliberately wrong page, or a green run proves nothing about it.
CONTRAST = f"{S}design-a11y/reference/contrast.md"
SCALES = f"{S}design-tokens/reference/scales.md"
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
}


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
            if run_figures(copy).returncode == 0:
                bad.append(name)
                print(f"  figures/{name} did not fail")
    return bad


# --- one case per branch, keyed by what that branch prints -------------------

@case("V1-description", "description is")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "Designing how an interface behaves",
              "Designing, specifying, documenting and defending how an interface behaves")


@case("V2-terms", "contains 'rather than'")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "Designing how", "Designing, rather than guessing, how")


@case("V2-names", "names design-motion")
def _(r): sub(r / f"{S}design-ux/SKILL.md", "Designing how", "design-motion. Designing how")


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


@case("V8-reference", "links to missing skills/_design/GONE.md")
def _(r): sub(r / "README.md", "## Files", "[r]: <skills/_design/GONE.md>\n\n## Files")


# The other direction: valid Markdown that must stay green. A rule that only
# ever meets violations can be wrong about every form it was not shown.
GREEN_CASES: dict[str, callable] = {
    "fence-indented-and-longer-close": lambda r: sub(
        r / "README.md", "## Files",
        "   ```md\n[example](not/a/real/file.md)\n````\n\n## Files"),
    "fence-unclosed-tilde-at-end": lambda r: (r / "NOTES.md").write_text(
        "# Notes\n\n~~~\n[example](nowhere.md)\n", encoding="utf-8"),
    "angle-reference-to-real-file": lambda r: sub(
        r / "README.md", "## Files", "[routing]: <skills/_design/ROUTING.md>\n\n## Files"),
    "titled-link-to-real-file": lambda r: sub(
        r / "README.md", "## Files",
        "[routing](skills/_design/ROUTING.md 'routing') [r2](skills/_design/ROUTING.md (r))"
        "\n\n## Files"),
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
            if not re.search(rf"^\s*{expect}: .*{says}", out, re.M):
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
    ]
    wrong = [i for i, (v, s, ok) in enumerate(schema_cases)
             if (engine.mismatch(v, s) is None) != ok]
    if wrong:
        print(f"engine.mismatch decided wrongly on schema cases {wrong}")
        return 1
    print(f"engine answers are held to their schema ({len(schema_cases)} cases)")

    silent_figures = figures_fire()
    if silent_figures:
        print("figures_check stayed green on: " + ", ".join(silent_figures))
        return 1
    print(f"every figure check fails when it should ({len(FIGURE_CASES)} cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
