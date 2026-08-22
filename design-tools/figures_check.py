#!/usr/bin/env python3
"""Recompute the numbers the reference layer states, from the reference layer.

A `Verified:` date says a human looked once. It cannot fail. These checks parse
the tables out of the pages themselves and recompute them, so a value edited
into a wrong one breaks the build instead of ageing quietly.

    make figures

Add a checker here whenever a reference page states a number that follows from
another number on the same page.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
failures: list[str] = []


def fail(where: str, msg: str) -> None:
    failures.append(f"  {where}: {msg}")


# --- WCAG 2.x relative luminance and contrast ------------------------------

def _channel(c: int) -> float:
    cs = c / 255
    return cs / 12.92 if cs <= 0.03928 else ((cs + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


ROW = re.compile(
    r"^\|[^|]+\|\s*`(#[0-9a-fA-F]{6})`\s*\|\s*`(#[0-9a-fA-F]{6})`\s*\|"
    r"\s*([0-9.]+):1\s*\|\s*([0-9.]+):1[^|]*\|\s*([^|]+)\|"
)


PAIR_HEAD = re.compile(r"^\|\s*Pair\s*\|\s*Foreground\s*\|")
SEP = re.compile(r"^\|[\s:|-]+\|$")


def pair_rows(text: str) -> list[tuple[int, str]]:
    """Every data row of the recording table, matching or not.

    Filtering to rows that already parse would enforce the page's own rule —
    "never state a pass without both source values" — only on the rows that
    already follow it. A row rewritten to say "grey on white, roughly 2.6"
    would drop out of the check and the build would stay green.
    """
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if PAIR_HEAD.match(l.strip())), None)
    if start is None:
        return []
    out = []
    for i in range(start + 1, len(lines)):
        s = lines[i].strip()
        if SEP.match(s):
            continue
        if not (s.startswith("|") and s.endswith("|")):
            break
        out.append((i + 1, s))
    return out


def check_contrast() -> int:
    """Every recorded pair: does the stated ratio follow from the two colours,
    and does the stated verdict follow from the ratio and the requirement?"""
    page = SKILLS / "design-a11y/reference/contrast.md"
    rows = pair_rows(page.read_text())
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
        says_pass = "pass" in verdict.lower() and "fail" not in verdict.lower()
        if passes != says_pass:
            fail(f"contrast.md:{i}",
                 f"{actual:.2f}:1 against {required}:1 is a "
                 f"{'pass' if passes else 'fail'}, recorded as {verdict.strip()!r}")
    return n


# --- Type scale ------------------------------------------------------------

SCALE_HEAD = re.compile(r"\|\s*Token\s*\|\s*(\d+)px\s*/\s*([0-9.]+) ratio\s*\|")
SCALE_ROW = re.compile(r"^\|\s*`(--text-[a-z0-9]+)`\s*\|\s*(\d+)px\s*\|")
CLAMP = re.compile(r"clamped below `(--text-[a-z0-9]+)`", re.I)


def check_type_scale() -> int:
    """The page states a base and a ratio. Every step above the base must be the
    ratio applied and rounded; steps the page declares clamped are exempt."""
    page = SKILLS / "design-tokens/reference/scales.md"
    text = page.read_text()
    head = SCALE_HEAD.search(text)
    if not head:
        fail("scales.md", "no `<base>px / <ratio> ratio` column header found")
        return 0
    base, ratio = int(head.group(1)), float(head.group(2))
    clamp = CLAMP.search(text)
    clamp_below = clamp.group(1) if clamp else None

    rows = [(m.group(1), int(m.group(2)))
            for m in (SCALE_ROW.match(l) for l in text.splitlines()) if m]
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
        expected = round(base * ratio ** step)
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
