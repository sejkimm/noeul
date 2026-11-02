"""OKLCH <-> sRGB conversion and WCAG contrast ratio."""

import math


def _to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _from_linear(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{round(min(max(c, 0), 1) * 255):02x}" for c in rgb)


def oklch_to_rgb(l: float, c: float, h: float) -> tuple[float, float, float]:
    """OKLCH to gamma-encoded sRGB, unclamped (values may fall outside 0..1)."""
    a, b = c * math.cos(math.radians(h)), c * math.sin(math.radians(h))
    l_ = (l + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (l - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (l - 0.0894841775 * a - 1.2914855480 * b) ** 3
    lin = (
        4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_,
    )
    return tuple(_from_linear(x) if x >= 0 else -_from_linear(-x) for x in lin)


def rgb_to_oklch(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = (_to_linear(x) for x in rgb)
    l_ = math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m_ = math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s_ = math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
    l = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return l, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def oklch_hex(l: float, c: float, h: float) -> str:
    """OKLCH to hex, reducing chroma in 0.001 steps until the color fits in sRGB."""
    while c > 0 and not _in_gamut(oklch_to_rgb(l, c, h)):
        c -= 0.001
    return rgb_to_hex(oklch_to_rgb(l, max(c, 0), h))


def _in_gamut(rgb: tuple[float, float, float]) -> bool:
    return all(0 <= x <= 1 for x in rgb)


def luminance(hex_color: str) -> float:
    r, g, b = (_to_linear(x) for x in hex_to_rgb(hex_color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)
