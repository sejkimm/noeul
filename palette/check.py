"""Print contrast ratios against bg1 and fail if a text color is below WCAG AA (4.5:1)."""

import sys

from build import load_palette
from oklch import contrast

MIN_TEXT = 4.5
HUES = ("red", "green", "yellow", "blue", "magenta", "cyan")
TEXT = (
    "tx1",
    "tx2",
    "tx3",
    "ax1",
    "ax2",
    "caramel",
    "brown",
    *HUES,
    *(f"bright_{h}" for h in HUES),
)
DECORATIVE = ("ui3", "ax3")  # line numbers, rules, cursor, focus ring: dim on purpose


def main() -> int:
    palette = load_palette()
    failures = []
    print(f"{'token':<16}{'light':>8}{'dark':>8}")
    for name in TEXT + DECORATIVE:
        ratios = [
            contrast(palette[m][name], palette[m]["bg1"]) for m in ("light", "dark")
        ]
        note = "  (decorative)" if name in DECORATIVE else ""
        print(f"{name:<16}{ratios[0]:>8.1f}{ratios[1]:>8.1f}{note}")
        if name in TEXT and min(ratios) < MIN_TEXT:
            failures.append(name)
    if failures:
        print(f"FAIL: below {MIN_TEXT}:1: {', '.join(failures)}")
        return 1
    print(f"OK: all text colors >= {MIN_TEXT}:1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
