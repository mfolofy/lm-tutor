"""Per-class grader for brushes — computation-heavy WCAG checks.

Phase 0 implements:
  - color-contrast: extract CSS color declarations, compute WCAG 2.2 contrast
    ratios, flag failures below 4.5:1 (normal text) / 3:1 (large text).
  - heading-order: parse <h1>-<h6> elements, detect skips and multiples.
  - typography-minimum: check font-size >= 16px, line-height >= 1.5,
    max-width <= 80ch.
  - spacing-system: check inline padding/margin for 4px scale adherence.
  - touch-target: estimate interactive element sizing via inline styles.

These checks are Layer 1.5 — deterministic but need CSS parsing and
computation. They run after the selector/regex Layer 1 checks, via the
harness hook (``tutor.eval.harness.grade`` → `import tutor.classes.brushes.grader').

Dependencies: none in Phase 0 (stdlib regex for color extraction).
Future: pillow/tinycss2 for precise color parsing in Phase 1.
"""

import logging
import math
import re
from html.parser import HTMLParser

logger = logging.getLogger(__name__)

# ── CSS Color Utilities ──────────────────────────────────────────────────────

_NAMED_COLORS = {
    "aliceblue": (240, 248, 255),
    "antiquewhite": (250, 235, 215),
    "aqua": (0, 255, 255),
    "aquamarine": (127, 255, 212),
    "azure": (240, 255, 255),
    "beige": (245, 245, 220),
    "bisque": (255, 228, 196),
    "black": (0, 0, 0),
    "blanchedalmond": (255, 235, 205),
    "blue": (0, 0, 255),
    "blueviolet": (138, 43, 226),
    "brown": (165, 42, 42),
    "burlywood": (222, 184, 135),
    "cadetblue": (95, 158, 160),
    "chartreuse": (127, 255, 0),
    "chocolate": (210, 105, 30),
    "coral": (255, 127, 80),
    "cornflowerblue": (100, 149, 237),
    "cornsilk": (255, 248, 220),
    "crimson": (220, 20, 60),
    "cyan": (0, 255, 255),
    "darkblue": (0, 0, 139),
    "darkcyan": (0, 139, 139),
    "darkgoldenrod": (184, 134, 11),
    "darkgray": (169, 169, 169),
    "darkgreen": (0, 100, 0),
    "darkgrey": (169, 169, 169),
    "darkkhaki": (189, 183, 107),
    "darkmagenta": (139, 0, 139),
    "darkolivegreen": (85, 107, 47),
    "darkorange": (255, 140, 0),
    "darkorchid": (153, 50, 204),
    "darkred": (139, 0, 0),
    "darksalmon": (233, 150, 122),
    "darkseagreen": (143, 188, 143),
    "darkslateblue": (72, 61, 139),
    "darkslategray": (47, 79, 79),
    "darkturquoise": (0, 206, 209),
    "darkviolet": (148, 0, 211),
    "deeppink": (255, 20, 147),
    "deepskyblue": (0, 191, 255),
    "dimgray": (105, 105, 105),
    "dimgrey": (105, 105, 105),
    "dodgerblue": (30, 144, 255),
    "firebrick": (178, 34, 34),
    "floralwhite": (255, 250, 240),
    "forestgreen": (34, 139, 34),
    "fuchsia": (255, 0, 255),
    "gainsboro": (220, 220, 220),
    "ghostwhite": (248, 248, 255),
    "gold": (255, 215, 0),
    "goldenrod": (218, 165, 32),
    "gray": (128, 128, 128),
    "green": (0, 128, 0),
    "greenyellow": (173, 255, 47),
    "grey": (128, 128, 128),
    "honeydew": (240, 255, 240),
    "hotpink": (255, 105, 180),
    "indianred": (205, 92, 92),
    "indigo": (75, 0, 130),
    "ivory": (255, 255, 240),
    "khaki": (240, 230, 140),
    "lavender": (230, 230, 250),
    "lavenderblush": (255, 240, 245),
    "lawngreen": (124, 252, 0),
    "lemonchiffon": (255, 250, 205),
    "lightblue": (173, 216, 230),
    "lightcoral": (240, 128, 128),
    "lightcyan": (224, 255, 255),
    "lightgoldenrodyellow": (250, 250, 210),
    "lightgray": (211, 211, 211),
    "lightgreen": (144, 238, 144),
    "lightgrey": (211, 211, 211),
    "lightpink": (255, 182, 193),
    "lightsalmon": (255, 160, 122),
    "lightseagreen": (32, 178, 170),
    "lightskyblue": (135, 206, 250),
    "lightslategray": (119, 136, 153),
    "lightsteelblue": (176, 196, 222),
    "lightyellow": (255, 255, 224),
    "lime": (0, 255, 0),
    "limegreen": (50, 205, 50),
    "linen": (250, 240, 230),
    "magenta": (255, 0, 255),
    "maroon": (128, 0, 0),
    "mediumaquamarine": (102, 205, 170),
    "mediumblue": (0, 0, 205),
    "mediumorchid": (186, 85, 211),
    "mediumpurple": (147, 112, 219),
    "mediumseagreen": (60, 179, 113),
    "mediumslateblue": (123, 104, 238),
    "mediumspringgreen": (0, 250, 154),
    "mediumturquoise": (72, 209, 204),
    "mediumvioletred": (199, 21, 133),
    "midnightblue": (25, 25, 112),
    "mintcream": (245, 255, 250),
    "mistyrose": (255, 228, 225),
    "moccasin": (255, 228, 181),
    "navajowhite": (255, 222, 173),
    "navy": (0, 0, 128),
    "oldlace": (253, 245, 230),
    "olive": (128, 128, 0),
    "olivedrab": (107, 142, 35),
    "orange": (255, 165, 0),
    "orangered": (255, 69, 0),
    "orchid": (218, 112, 214),
    "palegoldenrod": (238, 232, 170),
    "palegreen": (152, 251, 152),
    "paleturquoise": (175, 238, 238),
    "palevioletred": (219, 112, 147),
    "papayawhip": (255, 239, 213),
    "peachpuff": (255, 218, 185),
    "peru": (205, 133, 63),
    "pink": (255, 192, 203),
    "plum": (221, 160, 221),
    "powderblue": (176, 224, 230),
    "purple": (128, 0, 128),
    "rebeccapurple": (102, 51, 153),
    "red": (255, 0, 0),
    "rosybrown": (188, 143, 143),
    "royalblue": (65, 105, 225),
    "saddlebrown": (139, 69, 19),
    "salmon": (250, 128, 114),
    "sandybrown": (244, 164, 96),
    "seagreen": (46, 139, 87),
    "seashell": (255, 245, 238),
    "sienna": (160, 82, 45),
    "silver": (192, 192, 192),
    "skyblue": (135, 206, 235),
    "slateblue": (106, 90, 205),
    "slategray": (112, 128, 144),
    "snow": (255, 250, 250),
    "springgreen": (0, 255, 127),
    "steelblue": (70, 130, 180),
    "tan": (210, 180, 140),
    "teal": (0, 128, 128),
    "thistle": (216, 191, 216),
    "tomato": (255, 99, 71),
    "turquoise": (64, 224, 208),
    "violet": (238, 130, 238),
    "wheat": (245, 222, 179),
    "white": (255, 255, 255),
    "whitesmoke": (245, 245, 245),
    "yellow": (255, 255, 0),
    "yellowgreen": (154, 205, 50),
}

# LLM-DEFAULT LOW-CONTRAST GRAYS and their ratios on white (#fff)
# These are the most common contrast failures in LLM-generated UIs.
_KNOWN_LOW_CONTRAST = {
    "#999": 2.8,
    "#999999": 2.8,
    "#aaa": 2.3,
    "#aaaaaa": 2.3,
    "#bbb": 1.8,
    "#bbbbbb": 1.8,
    "#ccc": 1.6,
    "#cccccc": 1.6,
    "#777": 4.0,
    "#777777": 4.0,
    "#888": 3.3,
    "#888888": 3.3,
}

# Named colors that fail 4.5:1 on white
_LOW_CONTRAST_NAMED = {
    "gray": 3.9,
    "grey": 3.9,
    "darkgray": 2.8,
    "darkgrey": 2.8,
    "silver": 4.0,
    "lightgray": 1.6,
    "lightgrey": 1.6,
    "gainsboro": 1.4,
}

_HEX_SHORT = re.compile(r"#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])\b")
_HEX_FULL = re.compile(r"#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})\b")
_RGB = re.compile(r"rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")


def _parse_color(value: str) -> tuple[int, int, int] | None:
    """Parse an sRGB color value to (R, G, B) int tuple, or None."""
    value = value.strip().lower()
    # Named color
    if value in _NAMED_COLORS:
        return _NAMED_COLORS[value]
    # #rgb → #rrggbb
    m = _HEX_SHORT.match(value)
    if m:
        return (
            int(m.group(1) * 2, 16),
            int(m.group(2) * 2, 16),
            int(m.group(3) * 2, 16),
        )
    # #rrggbb
    m = _HEX_FULL.match(value)
    if m:
        return (
            int(m.group(1), 16),
            int(m.group(2), 16),
            int(m.group(3), 16),
        )
    # rgb(r, g, b)
    m = _RGB.match(value)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def _srgb_to_linear(channel: float) -> float:
    """Convert a single sRGB channel (0-255) to linear luminance."""
    s = channel / 255.0
    if s <= 0.04045:
        return s / 12.92
    return ((s + 0.055) / 1.055) ** 2.4


def _relative_luminance(r: int, g: int, b: int) -> float:
    """WCAG relative luminance from sRGB values."""
    return (
        0.2126 * _srgb_to_linear(r)
        + 0.7152 * _srgb_to_linear(g)
        + 0.0722 * _srgb_to_linear(b)
    )


def _contrast_ratio(c1: tuple[int, int, int], c2: tuple[int, int, int]) -> float:
    """WCAG contrast ratio between two sRGB colors."""
    l1 = _relative_luminance(*c1)
    l2 = _relative_luminance(*c2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ── HTML Parsing for grader-specific needs ───────────────────────────────────

class _GraderParser(HTMLParser):
    """Extended parser that collects heading elements, style blocks, and inline styles."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.headings: list[dict] = []  # {tag, text}
        self.style_blocks: list[str] = []
        self.inline_styles: list[dict] = []  # {tag, text, style_str, ...}
        self._in_style = False
        self._current_tag = ""
        self._current_attrs: dict[str, str] = {}

    def handle_starttag(self, tag, attrs):
        self._current_tag = tag
        self._current_attrs = {k: v for k, v in attrs if v is not None}
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append({"tag": tag, "text": ""})
        if tag == "style":
            self._in_style = True
        style = dict(attrs).get("style", "")
        if style and tag in (
            "button", "a", "input", "select", "textarea",
            "p", "h1", "h2", "h3", "h4", "h5", "h6",
            "div", "span", "li", "td", "th",
        ):
            self.inline_styles.append({
                "tag": tag,
                "style": style,
                "attrs": self._current_attrs,
            })

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.style_blocks.append(data)
        elif self.headings and data.strip():
            self.headings[-1]["text"] += data


def _parse(submission: str) -> _GraderParser:
    parser = _GraderParser()
    try:
        parser.feed(submission)
        parser.close()
    except Exception:
        logger.debug("grader.py HTML parse error (grading partial)", exc_info=True)
    return parser


# ── Rule-specific graders ────────────────────────────────────────────────────

def _grade_color_contrast(submission: str) -> list[dict]:
    """Check WCAG 1.4.3 contrast minimum.

    Phase 0 implementation: extract all color declarations from inline styles
    and <style> blocks, compute contrast ratios against assumed white background
    (#fff) — the most common LLM use case. Flag known-low-contrast grays directly.

    Returns list of violation dicts.
    """
    violations: list[dict] = []

    # Quick check: known low-contrast grays in the raw submission.
    for gray, ratio in _KNOWN_LOW_CONTRAST.items():
        if gray in submission.lower():
            if ratio < 4.5:
                violations.append({
                    "rule": "color-contrast",
                    "severity": "fundamental",
                    "message": f"low contrast",
                    "wcag": "1.4.3",
                    "matched": f"Color {gray} has only {ratio}:1 contrast on white (need 4.5:1)",
                })

    # Parse inline styles for color declarations.
    parser = _parse(submission)
    white = (255, 255, 255)

    for entry in parser.inline_styles:
        style = entry["style"]
        colors_found = _extract_colors_from_style(style)
        for prop, color_value in colors_found.items():
            rgb = _parse_color(color_value)
            if rgb and prop in ("color",):
                ratio = _contrast_ratio(rgb, white)
                if ratio < 4.5:
                    violations.append({
                        "rule": "color-contrast",
                        "severity": "fundamental",
                        "message": "low contrast",
                        "wcag": "1.4.3",
                        "matched": (
                            f"<{entry['tag']}> color ({color_value}) "
                            f"has {ratio:.1f}:1 contrast on white (need 4.5:1)"
                        ),
                    })

    # Check <style> blocks for low-contrast color declarations.
    style_text = " ".join(parser.style_blocks)
    color_decls = re.findall(
        r"color\s*:\s*(#[0-9a-fA-F]{3,6}|[a-zA-Z]+)\s*(?:!important)?\s*[;}]",
        style_text,
    )
    for decl in color_decls:
        decl_lower = decl.lower()
        if decl_lower in _KNOWN_LOW_CONTRAST:
            ratio = _KNOWN_LOW_CONTRAST[decl_lower]
            if ratio < 4.5:
                violations.append({
                    "rule": "color-contrast",
                    "severity": "fundamental",
                    "message": "low contrast",
                    "wcag": "1.4.3",
                    "matched": f"Style block color: {decl} has {ratio}:1 contrast on white",
                })
        elif decl_lower in _LOW_CONTRAST_NAMED:
            ratio = _LOW_CONTRAST_NAMED[decl_lower]
            if ratio < 4.5:
                violations.append({
                    "rule": "color-contrast",
                    "severity": "fundamental",
                    "message": "low contrast",
                    "wcag": "1.4.3",
                    "matched": f"Style block color: {decl} has ~{ratio}:1 contrast on white",
                })

    # Deduplicate by matched message.
    seen = set()
    unique = []
    for v in violations:
        key = v["matched"]
        if key not in seen:
            seen.add(key)
            unique.append(v)
    return unique


_COLOR_PROPS = re.compile(
    r"(?P<prop>color|background-color|background)\s*:\s*(?P<value>[^;]+?)\s*(?:!important)?\s*(?:;|$)",
    re.IGNORECASE,
)


def _extract_colors_from_style(style: str) -> dict[str, str]:
    """Extract color: and background-color: declarations from a CSS string."""
    result: dict[str, str] = {}
    for m in _COLOR_PROPS.finditer(style):
        prop = m.group("prop").lower()
        value = m.group("value").strip()
        # Skip url() or complex background values.
        if prop == "background" and ("url(" in value or "linear-gradient" in value):
            continue
        result[prop] = value
    return result


def _grade_heading_order(submission: str) -> list[dict]:
    """Check heading hierarchy:
    - Exactly one h1
    - No skipped levels (h1 → h3)
    """
    violations: list[dict] = []
    parser = _parse(submission)

    if not parser.headings:
        return violations

    # Check for multiple h1s.
    h1_count = sum(1 for h in parser.headings if h["tag"] == "h1")
    if h1_count > 1:
        violations.append({
            "rule": "heading-order",
            "severity": "fundamental",
            "message": "multiple h1 elements",
            "wcag": "1.3.1",
            "matched": f"Page has {h1_count} <h1> elements (max 1 allowed)",
        })

    # Check for skipped levels.
    levels = [int(h["tag"][1]) for h in parser.headings]
    for i in range(1, len(levels)):
        if levels[i] - levels[i - 1] > 1:
            violations.append({
                "rule": "heading-order",
                "severity": "fundamental",
                "message": "heading level skipped",
                "wcag": "1.3.1",
                "matched": (
                    f"<h{levels[i-1]}> → <h{levels[i]}> skips "
                    f"<h{levels[i-1] + 1}>"
                ),
            })

    return violations


def _grade_typography_minimums(submission: str) -> list[dict]:
    """Check typography minimums:
    - Body text font-size >= 16px
    - Line-height >= 1.5
    - Max-width <= 80ch
    """
    violations: list[dict] = []
    parser = _parse(submission)

    for entry in parser.inline_styles:
        style = entry["style"]
        font_size = re.search(r"font-size\s*:\s*(\d+)px", style)
        line_height = re.search(r"line-height\s*:\s*([\d.]+)", style)
        max_width = re.search(r"max-width\s*:\s*(\d+)(ch|px)", style)

        if font_size and int(font_size.group(1)) < 16:
            violations.append({
                "rule": "typography-minimum",
                "severity": "warning",
                "message": "body font below 16px",
                "wcag": "1.4.4",
                "matched": (
                    f"<{entry['tag']}> font-size: {font_size.group(0)} "
                    f"(minimum 16px for body text)"
                ),
            })

        if line_height:
            lh = float(line_height.group(1))
            if lh < 1.5:
                violations.append({
                    "rule": "typography-minimum",
                    "severity": "warning",
                    "message": "line-height below 1.5",
                    "wcag": "1.4.12",
                    "matched": (
                        f"<{entry['tag']}> line-height: {lh} "
                        f"(minimum 1.5 for readability)"
                    ),
                })

        if max_width:
            val = int(max_width.group(1))
            unit = max_width.group(2)
            if unit == "px":
                if val > 640:  # 640px ≈ 80ch at 16px
                    violations.append({
                        "rule": "typography-minimum",
                        "severity": "warning",
                        "message": "text line too wide",
                        "wcag": "1.4.8",
                        "matched": (
                            f"<{entry['tag']}> max-width: {val}px "
                            f"(prefer 60-80ch)"
                        ),
                    })
            elif unit == "ch" and val > 80:
                violations.append({
                    "rule": "typography-minimum",
                    "severity": "warning",
                    "message": "text line too wide",
                    "wcag": "1.4.8",
                    "matched": (
                        f"<{entry['tag']}> max-width: {val}ch "
                        f"(recommended max: 80ch)"
                    ),
                })

    # Also check <style> blocks for font-size below 16px on body/p.
    style_text = " ".join(parser.style_blocks)
    body_font = re.findall(
        r"(?:body|p|html)\s*\{[^}]*font-size\s*:\s*(\d+)px",
        style_text,
        re.IGNORECASE,
    )
    for px in body_font:
        if int(px) < 16:
            violations.append({
                "rule": "typography-minimum",
                "severity": "warning",
                "message": "body font below 16px",
                "wcag": "1.4.4",
                "matched": f"CSS body/p font-size: {px}px (minimum 16px)",
            })

    return violations


def _grade_spacing_system(submission: str) -> list[dict]:
    """Check spacing system:
    - Inline padding and margin values should be multiples of 4px.
    """
    violations: list[dict] = []
    # Check inline styles
    parser = _parse(submission)

    VALID_SPACING = {0, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96}
    SPACING_PROPS = re.compile(
        r"(padding|margin)(?:-(?:top|right|bottom|left))?\s*:\s*(\d+)px",
        re.IGNORECASE,
    )

    for entry in parser.inline_styles:
        for m in SPACING_PROPS.finditer(entry["style"]):
            px = int(m.group(2))
            if px > 0 and px not in VALID_SPACING:
                violations.append({
                    "rule": "spacing-system",
                    "severity": "warning",
                    "message": "non-standard spacing",
                    "wcag": "1.4.8",
                    "matched": (
                        f"<{entry['tag']}> {m.group(1)}: {px}px "
                        f"(use 4px-based scale: 4, 8, 12, 16, 24, 32, 48, 64)"
                    ),
                })

    return violations


def _grade_touch_target(submission: str) -> list[dict]:
    """Check touch target minimums:
    - Interactive elements should have adequate padding for 24x24px minimum target.
    """
    violations: list[dict] = []

    # Parse interactive elements with inline padding
    parser = _parse(submission)

    for entry in parser.inline_styles:
        if entry["tag"] not in ("button", "a", "input", "select"):
            continue

        style = entry["style"]
        pady = _extract_padding_dimension(style, vertical=True)
        padx = _extract_padding_dimension(style, vertical=False)

        # If no explicit padding, the element likely has browser default
        if pady is None:
            continue

        # WCAG 2.5.8 minimum: 24x24 CSS px
        if pady < 3:  # ~3px padding on each side + content height ≈ 24px minimum
            violations.append({
                "rule": "touch-target",
                "severity": "warning",
                "message": "touch target too small",
                "wcag": "2.5.8",
                "matched": (
                    f"<{entry['tag']}> vertical padding: {pady}px "
                    f"(minimum 24x24px target recommended; "
                    f"add more padding)"
                ),
            })

    return violations


def _extract_padding_dimension(style: str, vertical: bool = True) -> int | None:
    """Extract vertical (top/bottom) or horizontal (left/right) padding px value."""
    if vertical:
        # Check padding-top, padding-bottom, or shorthand.
        top_m = re.search(r"padding-top\s*:\s*(\d+)px", style)
        bot_m = re.search(r"padding-bottom\s*:\s*(\d+)px", style)
        shorthand = re.search(r"padding\s*:\s*(\d+)px", style)
        if top_m or bot_m:
            vals = []
            if top_m:
                vals.append(int(top_m.group(1)))
            if bot_m:
                vals.append(int(bot_m.group(1)))
            return max(vals) if vals else None
        if shorthand:
            return int(shorthand.group(1))
        return None
    else:
        left_m = re.search(r"padding-left\s*:\s*(\d+)px", style)
        right_m = re.search(r"padding-right\s*:\s*(\d+)px", style)
        shorthand = re.search(r"padding\s*:\s*\d+px\s+(\d+)px", style)
        if left_m or right_m:
            vals = []
            if left_m:
                vals.append(int(left_m.group(1)))
            if right_m:
                vals.append(int(right_m.group(1)))
            return max(vals) if vals else None
        if shorthand:
            return int(shorthand.group(1))
        return None


# ── Public API ───────────────────────────────────────────────────────────────

def grade(submission: str, rules: list[dict]) -> list[dict]:
    """Run all computation-heavy checks for the brushes class.

    Called by the harness after Layer 1 selector/regex checks.
    Only checks rules where ``deep_check: true`` in class.yaml.
    """
    violations: list[dict] = []
    rule_ids = {r.get("id") for r in (rules or [])}

    if "color-contrast" in rule_ids:
        violations.extend(_grade_color_contrast(submission))

    if "heading-order" in rule_ids:
        violations.extend(_grade_heading_order(submission))

    if "typography-minimum" in rule_ids:
        violations.extend(_grade_typography_minimums(submission))

    if "spacing-system" in rule_ids:
        violations.extend(_grade_spacing_system(submission))

    if "touch-target" in rule_ids:
        violations.extend(_grade_touch_target(submission))

    return violations
