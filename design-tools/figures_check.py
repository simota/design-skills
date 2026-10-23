#!/usr/bin/env python3
"""Recompute the numbers the reference layer states, from the reference layer.

A `Verified:` date says a human looked once. It cannot fail. These checks parse
the tables out of the pages themselves and recompute them, so a value edited
into a wrong one breaks the build instead of ageing quietly.

    make figures

Add a checker here whenever a reference page states a number that follows from
another number on the same page.
"""
import json
import math
import pathlib
import re
import sys

import yaml
from markdown_it import MarkdownIt

ROOT = pathlib.Path(__file__).resolve().parent.parent
H = yaml.safe_load((ROOT / "design-registry" / "harness.yaml").read_text(encoding="utf-8"))
SKILLS = ROOT / H["skills_dir"] if H.get("skills_dir") else ROOT
failures: list[str] = []


def fail(where: str, msg: str) -> None:
    failures.append(f"  {where}: {msg}")


# --- WCAG 2.x relative luminance and contrast ------------------------------

def _channel(c: int) -> float:
    cs = c / 255
    # 0.04045 is the threshold contrast.md documents. The older 0.03928 gives the
    # same result for every 8-bit channel, but the tool and the page it checks
    # should name one formula.
    return cs / 12.92 if cs <= 0.04045 else ((cs + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# A number is digits with at most one point. `[0-9.]+` also took `17.76.` and
# then float() raised, ending the run with a traceback that lost every other
# mismatch it had found; now such a row fails to parse and is reported as one.
NUM = r"[0-9]+(?:\.[0-9]+)?"
ROW = re.compile(
    r"^\|[^|]+\|\s*`(#[0-9a-fA-F]{6})`\s*\|\s*`(#[0-9a-fA-F]{6})`\s*\|"
    rf"\s*({NUM}):1\s*\|\s*({NUM}):1[^|]*\|\s*([^|]+)\|"
)


PAIR_HEAD = re.compile(r"^\|\s*Pair\s*\|\s*Foreground\s*\|")
# validate.py reads the corpus the same way: CommonMark, plus GFM's tables.
MD = MarkdownIt("commonmark").enable("table")


def _closes(fence, lines: list[str]) -> bool:
    """Whether the fence's last line is its closing marker."""
    first, end = fence.map
    if end - first < 2:
        return False
    last = re.sub(r"^[\s>]*", "", lines[end - 1]).rstrip()
    return len(last) >= len(fence.markup) and set(last) == {fence.markup[0]}


def tables(text: str, head: re.Pattern) -> list[tuple[int, list[int]]]:
    """(header line, data row lines) for every table whose header matches `head`.

    Where a table starts and ends is the parser's call, as it is the reader's:
    a fenced example is not a recording table, and a heading or a fence under
    the rows ends one. Raw lines read both as rows and failed correct pages. A
    line of prose under the rows is still a row, as GFM reads it, and fails to
    parse like any row that does not state its values.

    A header-shaped line the parser does not open a table on — its separator
    line gone or malformed, or a fence above it left open — comes back with no
    rows, so it fails instead of taking its rows out of the check. Lines inside
    a closed fence or other code are examples, not that.
    """
    # The parser's line numbers count "\n" only; splitlines() also breaks at
    # U+2028 and its kin, and every header after one landed on the wrong line.
    lines = text.split("\n")
    found: dict[int, list[int]] = {}
    code: set[int] = set()
    table = body = None
    for tok in MD.parse(text):
        if tok.type == "table_open":
            table = found.setdefault(tok.map[0], [])
        elif tok.type == "tbody_open":
            body = table
        elif tok.type == "tr_open" and body is not None:
            body.append(tok.map[0])
        elif tok.type == "table_close":
            table = body = None
        elif tok.type in ("fence", "code_block", "html_block") and tok.map:
            # A fence never closed runs to the end of the page and swallows any
            # table after it; with another table still read, those pairs left
            # the count unnoticed. Only a closed fence is an example.
            if tok.type == "fence" and not _closes(tok, lines):
                continue
            code.update(range(*tok.map))
    return [(i, found.get(i, [])) for i, l in enumerate(lines)
            if i not in code and head.match(l.strip())]


def pair_rows(text: str) -> tuple[list[tuple[int, str]], list[int]]:
    """Every data row of every recording table, matching or not, and the
    header lines that open no table.

    Filtering to rows that already parse would enforce the page's own rule —
    "never state a pass without both source values" — only on the rows that
    already follow it. A row rewritten to say "grey on white, roughly 2.6"
    would drop out of the check and the build would stay green. So would a
    second table — the dark theme's pairs — if only the first were read.
    """
    lines = text.split("\n")
    found = tables(text, PAIR_HEAD)
    return ([(i + 1, lines[i].strip()) for _, rows in found for i in rows],
            [h + 1 for h, rows in found if not rows])


def check_contrast() -> int:
    """Every recorded pair: does the stated ratio follow from the two colours,
    and does the stated verdict follow from the ratio and the requirement?"""
    page = SKILLS / "design-a11y/reference/contrast.md"
    rows, headless = pair_rows(page.read_text(encoding="utf-8"))
    for i in headless:
        fail(f"contrast.md:{i}", "a recording table's header that opens no table "
                                 "with rows — is the separator line under it missing, "
                                 "or a code fence above it left open? Nothing under it "
                                 "is being recomputed")
    if not rows and not headless:
        fail("contrast.md", "no recording table found — "
                            "the checker has stopped checking anything")
        return 0
    n = 0
    for i, line in rows:
        m = ROW.match(line)
        if not m:
            fail(f"contrast.md:{i}",
                 "row does not state a foreground, a background, a ratio and a "
                 "requirement, so nothing about it can be recomputed — "
                 f"{line[:60]}")
            continue
        fg, bg, claimed, required, verdict = m.groups()
        n += 1
        actual = contrast(fg, bg)
        if round(actual, 2) != round(float(claimed), 2):
            fail(f"contrast.md:{i}",
                 f"{fg} on {bg} states {claimed}:1, computes {actual:.4f}:1")
        passes = actual >= float(required)
        # The verdict opens with pass or fail; "does not pass" holds "pass" and
        # not "fail", and was read as a pass.
        said = verdict.strip().strip("*").strip().lower()
        if not said.startswith(("pass", "fail")):
            fail(f"contrast.md:{i}",
                 f"result {verdict.strip()!r} is neither pass nor fail")
            continue
        says_pass = said.startswith("pass")
        if passes != says_pass:
            fail(f"contrast.md:{i}",
                 f"{actual:.2f}:1 against {required}:1 is a "
                 f"{'pass' if passes else 'fail'}, recorded as {verdict.strip()!r}")
    return n


# --- Type scale ------------------------------------------------------------

SCALE_HEAD = re.compile(rf"\|\s*Token\s*\|\s*(\d+)px\s*/\s*({NUM}) ratio\s*\|")
SCALE_ROW = re.compile(r"^\|\s*`(--text-[a-z0-9]+)`\s*\|\s*(\d+)px\s*\|")
CLAMP = re.compile(r"clamped below `(--text-[a-z0-9]+)`", re.I)


def check_type_scale() -> int:
    """The page states a base and a ratio. Every step above the base must be the
    ratio applied and rounded; steps the page declares clamped are exempt."""
    page = SKILLS / "design-tokens/reference/scales.md"
    text = page.read_text(encoding="utf-8")
    # Only the first table under such a header: a later table repeating a token
    # would otherwise shift every step index after it. A fenced example is not
    # the scale, so it is not the first.
    found = tables(text, SCALE_HEAD)
    if not found:
        fail("scales.md", "no `<base>px / <ratio> ratio` column header found")
        return 0
    lines = text.split("\n")
    start, body = found[0]
    head = SCALE_HEAD.match(lines[start].strip())
    base, ratio = int(head.group(1)), float(head.group(2))
    clamp = CLAMP.search(text)
    clamp_below = clamp.group(1) if clamp else None
    if not body:
        fail(f"scales.md:{start + 1}", "the scale's header opens no table with rows — "
                                       "is the separator line under it missing, or a "
                                       "code fence above it left open?")
        return 0
    table = [lines[i].strip() for i in body]
    # Every row is held to the form, as pair_rows does for contrast: a row
    # rewritten as `52px (hero)` or `2.5rem` used to drop out of the check, and
    # the count of steps recomputed fell by one with nothing failing.
    rows = []
    for l in table:
        m = SCALE_ROW.match(l)
        if m:
            rows.append((m.group(1), int(m.group(2))))
        else:
            fail("scales.md", f"row does not state a `--text-*` token and a px size, "
                              f"so it cannot be recomputed — {l[:60]}")
    if not rows:
        fail("scales.md", "no `--text-*` rows matched — the checker has stopped checking")
        return 0
    names = [r[0] for r in rows]
    if base not in [v for _, v in rows]:
        fail("scales.md", f"base {base}px is not one of the listed sizes")
        return len(rows)
    origin = [v for _, v in rows].index(base)
    exempt_upto = names.index(clamp_below) if clamp_below in names else -1

    n = 0
    for idx, (name, value) in enumerate(rows):
        step = idx - origin
        # Half up, as "round to whole pixels" is read; round() is half-to-even.
        expected = math.floor(base * ratio ** step + 0.5)
        n += 1
        if idx < exempt_upto:
            if value == expected:
                fail("scales.md", f"{name} is declared clamped but equals the "
                                  f"computed {expected}px — drop the exemption")
            continue
        if value != expected:
            fail("scales.md",
                 f"{name} is {value}px; {base} x {ratio}^{step} rounds to {expected}px"
                 + ("" if clamp_below else " (and no clamp is declared)"))
    return n


# --- DTCG colour values ------------------------------------------------------

def _tokens(node) -> dict[str, tuple[str | None, object]]:
    """Every token in a DTCG tree by its dot path: the $type stated on it or on
    the nearest group (None when neither states one), and its $value."""
    found: dict[str, tuple[str | None, object]] = {}

    def walk(n, p, inherited):
        if not isinstance(n, dict):
            return
        kind = n.get("$type", inherited)
        if "$value" in n:
            found[p] = (kind, n["$value"])
            return
        for k, v in n.items():
            if not k.startswith("$"):
                walk(v, f"{p}.{k}" if p else k, kind)
    walk(node, "", None)
    return found


def _resolve_type(tokens: dict, path: str) -> str | None:
    """$type from the token, else its alias target, else the nearest group —
    the order the page states. The group is already folded into the token's
    own entry, so an alias is followed only where neither stated one."""
    seen = set()
    while path in tokens and path not in seen:
        seen.add(path)
        kind, value = tokens[path]
        if kind:
            return kind
        if not (isinstance(value, str) and value.startswith("{") and value.endswith("}")):
            return None
        path = value[1:-1]
    return None


def check_dtcg_colours() -> int:
    """Every sRGB colour in the page's DTCG examples: do its components follow
    from its hex? The object form states the colour twice, and the two drift
    apart the first time someone edits one of them."""
    page = SKILLS / "design-tokens/reference/token-schema.md"
    text = page.read_text(encoding="utf-8")
    lines = text.split("\n")
    fences = [t for t in MD.parse(text) if t.type == "fence" and t.info.strip() == "json"]
    if not fences:
        fail("token-schema.md", "no ```json example found — the checker has stopped checking")
        return 0
    before, n = len(failures), 0
    for fence in fences:
        where = f"token-schema.md:{fence.map[0] + 1}"
        if not _closes(fence, lines):
            fail(where, "the json fence is never closed, so the example runs to the end of the page")
            continue
        try:
            tree = json.loads(fence.content)
        except json.JSONDecodeError as e:
            fail(where, f"the example is not JSON, so none of it can be recomputed — {e}")
            continue
        tokens = _tokens(tree)
        for path, (_, value) in tokens.items():
            kind = _resolve_type(tokens, path)
            if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                # An alias is checked where it points; a target that is gone, or
                # of another type, leaves nothing there to check.
                target = value[1:-1]
                if target not in tokens:
                    fail(where, f"{path} aliases {value}, which is not a token in the example")
                elif _resolve_type(tokens, target) != kind:
                    fail(where, f"{path} is {kind!r} and aliases {value}, which is "
                                f"{_resolve_type(tokens, target)!r}")
                continue
            if kind is None:
                # A token whose type resolves to nothing left the count unnoticed
                # while any other colour was still read.
                fail(where, f"{path} has no $type on itself, its alias target or a "
                            "group, so nothing says what its value is")
                continue
            if kind != "color":
                continue
            if not isinstance(value, dict):
                fail(where, f"{path} states {value!r}; a colour value is an object with "
                            "its colour space and components")
                continue
            hex_colour, comps = value.get("hex"), value.get("components")
            # bool is an int, and NaN a float that no difference ever exceeds.
            if (value.get("colorSpace") != "srgb" or not isinstance(hex_colour, str)
                    or not re.fullmatch(r"#[0-9a-fA-F]{6}", hex_colour)
                    or not isinstance(comps, list) or len(comps) != 3
                    or not all(isinstance(c, (int, float)) and not isinstance(c, bool)
                               and math.isfinite(c) and 0 <= c <= 1 for c in comps)):
                fail(where, f"{path} does not state an srgb colour space, three components "
                            "from 0 to 1 and a six-digit hex, so nothing about it can be "
                            "recomputed")
                continue
            n += 1
            want = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            # Components are written to four decimals; anything further off than
            # that rounding is a different colour from the hex beside it.
            if any(abs(c - w) > 0.00005 for c, w in zip(comps, want)):
                fail(where, f"{path} states components {comps}; {hex_colour} is "
                            f"{[round(w, 4) for w in want]}")
    if not n and len(failures) == before:
        fail("token-schema.md", "no srgb colour token found in the json examples — "
                                "the checker has stopped checking")
    return n


def main() -> int:
    pairs = check_contrast()
    steps = check_type_scale()
    colours = check_dtcg_colours()
    if failures:
        print(f"{len(failures)} mismatch(es):")
        print("\n".join(failures))
        return 1
    print(f"figures green - {pairs} contrast pairs recomputed, "
          f"{steps} type-scale steps recomputed, {colours} DTCG colours recomputed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
