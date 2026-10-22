#!/usr/bin/env python3
"""Recompute the numbers the reference layer states, from the reference layer.

A `Verified:` date says a human looked once. It cannot fail. These checks parse
the tables out of the pages themselves and recompute them, so a value edited
into a wrong one breaks the build instead of ageing quietly.

    make figures

Add a checker here whenever a reference page states a number that follows from
another number on the same page.
"""
import math
import pathlib
import re
import sys

import yaml

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
SEP = re.compile(r"^\|[\s:|-]+\|$")


def table_body(lines: list[str], start: int) -> list[int]:
    """Indices of the rows under the header at `start`, up to where the table ends.

    A table runs to the first blank line, as GFM reads it. A row without its
    outer pipes is still a row there; ending the table on it dropped that row
    and every one after it from the check, and the count of pairs recomputed
    fell with nothing failing. Such a row is now returned, and fails to parse
    like any other row that does not state its values.
    """
    first = start + 1
    # Only the line under the header is a separator; one further down stands
    # where a recorded pair was, and dropping it silently is the vacuous pass.
    if first < len(lines) and SEP.match(lines[first].strip()):
        first += 1
    out = []
    for i in range(first, len(lines)):
        if not lines[i].strip():
            break
        out.append(i)
    return out


def pair_rows(text: str) -> list[tuple[int, str]]:
    """Every data row of every recording table, matching or not.

    Filtering to rows that already parse would enforce the page's own rule —
    "never state a pass without both source values" — only on the rows that
    already follow it. A row rewritten to say "grey on white, roughly 2.6"
    would drop out of the check and the build would stay green. So would a
    second table — the dark theme's pairs — if only the first were read.
    """
    lines = text.splitlines()
    return [(i + 1, lines[i].strip())
            for start, l in enumerate(lines) if PAIR_HEAD.match(l.strip())
            for i in table_body(lines, start)]


def check_contrast() -> int:
    """Every recorded pair: does the stated ratio follow from the two colours,
    and does the stated verdict follow from the ratio and the requirement?"""
    page = SKILLS / "design-a11y/reference/contrast.md"
    rows = pair_rows(page.read_text(encoding="utf-8"))
    if not rows:
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
    head = SCALE_HEAD.search(text)
    if not head:
        fail("scales.md", "no `<base>px / <ratio> ratio` column header found")
        return 0
    base, ratio = int(head.group(1)), float(head.group(2))
    clamp = CLAMP.search(text)
    clamp_below = clamp.group(1) if clamp else None

    # Only the table under the header: a later table repeating a token would
    # otherwise shift every step index after it.
    lines = text[head.start():].splitlines()
    # The separator is optional and only ever the line under the header: assuming
    # it by position skipped the first row when it was missing, and skipping it
    # by form anywhere let a separator-shaped line stand in for a removed row.
    table = [lines[i] for i in table_body(lines, 0)]
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


def main() -> int:
    pairs = check_contrast()
    steps = check_type_scale()
    if failures:
        print(f"{len(failures)} mismatch(es):")
        print("\n".join(failures))
        return 1
    print(f"figures green - {pairs} contrast pairs recomputed, "
          f"{steps} type-scale steps recomputed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
