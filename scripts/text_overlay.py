"""
Text Overlay Module

Adds text overlay to images and exports to PNG.

This is a **local raster operation** (no external API calls).

Dependency:
- Pillow (PIL): `python3 -m pip install pillow`

Workflow:
1. Load background image (PNG/JPG)
2. Draw text (optional shadow / background box)
3. Save final PNG
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import tempfile


@dataclass
class TextElement:
    """Text element configuration"""

    text: str
    x: int
    y: int
    font_size: int = 48
    font_family: str = "Pretendard, Nanum Gothic, sans-serif"
    font_weight: str = "bold"
    fill: str = "#FFFFFF"
    text_anchor: str = "middle"  # "start", "middle", "end"
    shadow: bool = True
    shadow_color: str = "rgba(0,0,0,0.5)"
    shadow_offset_x: int = 2
    shadow_offset_y: int = 2
    background_box: bool = False
    background_box_color: str = "rgba(0,0,0,0.3)"
    background_box_padding: int = 20
    background_box_radius: int = 10


@dataclass
class TextOverlayConfig:
    """Configuration for text overlay operation"""

    background_image_path: str
    output_path: str
    width: int = 0  # Auto-detect from image if 0
    height: int = 0  # Auto-detect from image if 0
    text_elements: List[TextElement] = field(default_factory=list)


class TextOverlayProcessor:
    """
    Processor for adding text overlay to images via Pillow.

    Example usage:
        processor = TextOverlayProcessor()

        config = TextOverlayConfig(
            background_image_path="./images/background.png",
            output_path="./images/final.png",
            text_elements=[
                TextElement(
                    text="제목 텍스트",
                    x=650,  # center for 1300px width
                    y=400,
                    font_size=48,
                    fill="#FFFFFF",
                    shadow=True
                )
            ]
        )

        result = processor.process(config)
    """

    def __init__(self, temp_dir: Optional[str] = None):
        """
        Initialize TextOverlayProcessor.

        Args:
            temp_dir: Directory for temporary files (default: system temp)
        """
        self.temp_dir = temp_dir or tempfile.gettempdir()

    def process(self, config: TextOverlayConfig) -> Dict[str, Any]:
        """
        Process text overlay operation.

        Args:
            config: TextOverlayConfig with all settings

        Returns:
            Dict with 'success', 'output_path', 'error' keys
        """
        try:
            Image, ImageDraw, ImageFont = _load_pillow()

            with Image.open(config.background_image_path) as img:
                base = img.convert("RGBA")

            width, height = base.size

            overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)

            for elem in config.text_elements:
                if not elem.text:
                    continue
                font = _load_font(ImageFont, elem.font_family, elem.font_size)

                max_width = int(width * 0.86)
                lines = _wrap_text(draw, elem.text, font, max_width=max_width)

                line_boxes = [_text_bbox(draw, line, font) for line in lines]
                line_widths = [b[2] - b[0] for b in line_boxes]
                line_heights = [b[3] - b[1] for b in line_boxes]
                if not line_widths or not line_heights:
                    continue

                line_spacing = max(6, int(elem.font_size * 0.18))
                block_width = max(line_widths)
                block_height = sum(line_heights) + line_spacing * (len(lines) - 1)

                if elem.text_anchor == "middle":
                    block_left = elem.x - (block_width / 2)
                elif elem.text_anchor == "end":
                    block_left = elem.x - block_width
                else:  # "start"
                    block_left = elem.x

                block_top = elem.y - (block_height / 2)

                # Background box (optional)
                if elem.background_box:
                    pad = elem.background_box_padding
                    box = (
                        int(block_left - pad),
                        int(block_top - pad),
                        int(block_left + block_width + pad),
                        int(block_top + block_height + pad),
                    )
                    _draw_rounded_rect(
                        draw=draw,
                        box=box,
                        radius=elem.background_box_radius,
                        fill=_parse_color(elem.background_box_color),
                    )

                # Draw each line
                y_cursor = float(block_top)
                for line, line_w, line_h in zip(lines, line_widths, line_heights):
                    if elem.text_anchor == "middle":
                        x_line = elem.x - (line_w / 2)
                    elif elem.text_anchor == "end":
                        x_line = elem.x - line_w
                    else:
                        x_line = elem.x

                    y_line = y_cursor

                    if elem.shadow:
                        draw.text(
                            (x_line + elem.shadow_offset_x, y_line + elem.shadow_offset_y),
                            line,
                            font=font,
                            fill=_parse_color(elem.shadow_color),
                        )

                    draw.text(
                        (x_line, y_line),
                        line,
                        font=font,
                        fill=_parse_color(elem.fill),
                    )

                    y_cursor += line_h + line_spacing

            final_img = Image.alpha_composite(base, overlay)

            output_path = Path(config.output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            final_img.save(output_path, format="PNG")

            return {"success": True, "output_path": str(output_path), "error": None}

        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "error": str(e)
            }

def create_thumbnail_with_text(
    background_image: str,
    output_path: str,
    main_text: str,
    sub_text: str = "",
    main_font_size: int = 48,
    sub_font_size: int = 24,
    text_color: str = "#FFFFFF",
    position: str = "center",
) -> Dict[str, Any]:
    """
    Convenience function to create a thumbnail with text overlay.

    Args:
        background_image: Path to background image
        output_path: Path for output PNG
        main_text: Main title text
        sub_text: Subtitle text (optional)
        main_font_size: Font size for main text
        sub_font_size: Font size for subtitle
        text_color: Text color (hex)
        position: Text position ("center", "top", "bottom")

    Returns:
        Dict with 'success', 'output_path', 'error'
    """
    try:
        Image, _, _ = _load_pillow()
    except ImportError as e:
        return {"success": False, "output_path": None, "error": str(e)}

    with Image.open(background_image) as img:
        width, height = img.size

    # Calculate positions based on position parameter
    center_x = width // 2

    if position == "top":
        main_y = height // 4
    elif position == "bottom":
        main_y = height * 3 // 4
    else:  # center
        main_y = height // 2

    sub_y = main_y + main_font_size + 20

    # Create text elements
    text_elements = [
        TextElement(
            text=main_text,
            x=center_x,
            y=main_y,
            font_size=main_font_size,
            fill=text_color,
            text_anchor="middle",
            shadow=True,
        )
    ]

    if sub_text:
        text_elements.append(
            TextElement(
                text=sub_text,
                x=center_x,
                y=sub_y,
                font_size=sub_font_size,
                fill=text_color,
                text_anchor="middle",
                shadow=True,
            )
        )

    # Process
    config = TextOverlayConfig(
        background_image_path=background_image,
        output_path=output_path,
        text_elements=text_elements,
    )

    processor = TextOverlayProcessor()
    return processor.process(config)


def _parse_y_position(y_value: str, height: int) -> int:
    """
    Parse Y position value (percentage or pixel).

    Args:
        y_value: Y position as percentage (e.g., "35%") or pixel (e.g., "310")
        height: Image height in pixels

    Returns:
        Y position in pixels
    """
    if not y_value:
        return height // 2  # default to center

    y_str = str(y_value).strip()
    if y_str.endswith("%"):
        try:
            percent = float(y_str[:-1])
            return int(height * percent / 100)
        except ValueError:
            return height // 2
    else:
        try:
            return int(y_str)
        except ValueError:
            return height // 2


def add_text_to_existing_image(
    image_path: str,
    text_config: 'TextOverlayConfig',
    output_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Add text overlay to an existing image using TextOverlayConfig from prompt_converter.

    Supports:
    - main_text with configurable Y position (main_text_y: "35%" or "310")
    - sub_text with configurable Y position (sub_text_y: "50%" or auto)
    - watermark at bottom center with margin

    Args:
        image_path: Path to source image
        text_config: TextOverlayConfig from prompt_converter module
        output_path: Output path (overwrites source if None)

    Returns:
        Dict with 'success', 'output_path', 'error'
    """
    try:
        Image, _, _ = _load_pillow()
    except ImportError as e:
        return {"success": False, "output_path": None, "error": str(e)}

    try:
        with Image.open(image_path) as img:
            width, height = img.size
    except Exception as e:
        return {"success": False, "output_path": None, "error": str(e)}

    # Calculate X position based on position parameter
    center_x = width // 2
    position_x_map = {
        "center": center_x,
        "top": center_x,
        "bottom": center_x,
        "top-left": width // 6,
        "top-right": width * 5 // 6,
        "bottom-left": width // 6,
        "bottom-right": width * 5 // 6,
        "bottom-center": center_x,
    }
    x = position_x_map.get(text_config.position, center_x)

    # Calculate main text Y position
    main_y = _parse_y_position(text_config.main_text_y, height)

    # Create text elements
    text_elements = []

    if text_config.main_text:
        text_elements.append(
            TextElement(
                text=text_config.main_text,
                x=x,
                y=main_y,
                font_size=text_config.font_size,
                font_family=text_config.font_family,
                font_weight=getattr(text_config, 'font_weight', 'bold'),
                fill=text_config.font_color,
                text_anchor="middle" if "left" not in text_config.position else "start",
                shadow=text_config.shadow,
                shadow_color=text_config.shadow_color,
                shadow_offset_x=text_config.shadow_offset,
                shadow_offset_y=text_config.shadow_offset,
                background_box=text_config.background_box,
                background_box_color=text_config.background_box_color,
                background_box_padding=text_config.background_box_padding,
            )
        )

    if text_config.sub_text:
        # Calculate sub_text Y position
        if text_config.sub_text_y:
            sub_y = _parse_y_position(text_config.sub_text_y, height)
        else:
            # Auto position: main_text + gap
            gap = max(20, int(text_config.font_size * 0.8))
            sub_y = main_y + text_config.font_size // 2 + gap

        sub_font_size = getattr(text_config, 'sub_font_size', int(text_config.font_size * 0.5))
        sub_font_color = getattr(text_config, 'sub_font_color', text_config.font_color)

        text_elements.append(
            TextElement(
                text=text_config.sub_text,
                x=x,
                y=sub_y,
                font_size=sub_font_size,
                font_family=text_config.font_family,
                font_weight="regular",
                fill=sub_font_color,
                text_anchor="middle" if "left" not in text_config.position else "start",
                shadow=text_config.shadow,
            )
        )

    # Add watermark if enabled
    watermark_enabled = getattr(text_config, 'watermark_enabled', True)
    watermark_text = getattr(text_config, 'watermark_text', '@money-lab-brian')

    if watermark_enabled and watermark_text:
        watermark_margin_bottom = getattr(text_config, 'watermark_margin_bottom', 60)
        watermark_font_size = getattr(text_config, 'watermark_font_size', 18)
        watermark_font_color = getattr(text_config, 'watermark_font_color', 'rgba(255,255,255,0.6)')

        # Watermark at bottom center
        watermark_y = height - watermark_margin_bottom

        text_elements.append(
            TextElement(
                text=watermark_text,
                x=center_x,
                y=watermark_y,
                font_size=watermark_font_size,
                font_family=text_config.font_family,
                font_weight="light",
                fill=watermark_font_color,
                text_anchor="middle",
                shadow=False,  # No shadow for watermark
            )
        )

    # Process
    final_output = output_path or image_path
    config = TextOverlayConfig(
        background_image_path=image_path,
        output_path=final_output,
        text_elements=text_elements,
    )

    processor = TextOverlayProcessor()
    return processor.process(config)


def _load_pillow():
    try:
        from PIL import Image, ImageDraw, ImageFont  # type: ignore
        return Image, ImageDraw, ImageFont
    except ImportError as e:
        raise ImportError(
            "Pillow is required for text overlay. "
            "Install with: python3 -m pip install pillow"
        ) from e


def _parse_color(value: str) -> Tuple[int, int, int, int]:
    if not value:
        return (255, 255, 255, 255)

    value = value.strip()

    # Hex: #RRGGBB or #RRGGBBAA
    if value.startswith("#"):
        hex_value = value[1:]
        if len(hex_value) == 3:
            r = int(hex_value[0] * 2, 16)
            g = int(hex_value[1] * 2, 16)
            b = int(hex_value[2] * 2, 16)
            return (r, g, b, 255)
        if len(hex_value) == 6:
            r = int(hex_value[0:2], 16)
            g = int(hex_value[2:4], 16)
            b = int(hex_value[4:6], 16)
            return (r, g, b, 255)
        if len(hex_value) == 8:
            r = int(hex_value[0:2], 16)
            g = int(hex_value[2:4], 16)
            b = int(hex_value[4:6], 16)
            a = int(hex_value[6:8], 16)
            return (r, g, b, a)

    # rgba(r,g,b,a)
    rgba_match = re.match(
        r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([0-9.]+)\s*\)",
        value,
        flags=re.IGNORECASE,
    )
    if rgba_match:
        r = int(rgba_match.group(1))
        g = int(rgba_match.group(2))
        b = int(rgba_match.group(3))
        alpha = float(rgba_match.group(4))
        a = int(max(0.0, min(1.0, alpha)) * 255)
        return (r, g, b, a)

    # rgb(r,g,b)
    rgb_match = re.match(
        r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)",
        value,
        flags=re.IGNORECASE,
    )
    if rgb_match:
        r = int(rgb_match.group(1))
        g = int(rgb_match.group(2))
        b = int(rgb_match.group(3))
        return (r, g, b, 255)

    # Fallback: white
    return (255, 255, 255, 255)


def _load_font(ImageFont, font_family: str, font_size: int):
    # Allow explicit font path override
    explicit_path = os.environ.get("BLOG_FONT_PATH") or os.environ.get("FONT_PATH")
    if explicit_path:
        try:
            return ImageFont.truetype(explicit_path, font_size)
        except Exception:
            pass

    candidates: List[Tuple[str, Optional[int]]] = [
        # macOS common Korean fonts
        ("/System/Library/Fonts/AppleSDGothicNeo.ttc", 0),
        ("/System/Library/Fonts/Supplemental/AppleGothic.ttf", None),
        ("/System/Library/Fonts/Supplemental/AppleMyungjo.ttf", None),
        ("/Library/Fonts/AppleGothic.ttf", None),
        ("/Library/Fonts/NanumGothic.ttf", None),
        ("/Library/Fonts/NanumGothicBold.ttf", None),
        # Linux common locations (best-effort)
        ("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", None),
        ("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf", None),
    ]

    for path, index in candidates:
        if not Path(path).exists():
            continue
        try:
            if index is None:
                return ImageFont.truetype(path, font_size)
            return ImageFont.truetype(path, font_size, index=index)
        except Exception:
            continue

    return ImageFont.load_default()


def _text_bbox(draw, text: str, font) -> Tuple[int, int, int, int]:
    try:
        return draw.textbbox((0, 0), text, font=font)
    except Exception:
        # Very old Pillow fallback
        w, h = draw.textsize(text, font=font)  # type: ignore[attr-defined]
        return (0, 0, w, h)


def _wrap_text(draw, text: str, font, max_width: int) -> List[str]:
    if not text:
        return []
    if "\n" in text:
        return [line for line in text.splitlines() if line.strip()]

    def width_of(s: str) -> int:
        b = _text_bbox(draw, s, font)
        return int(b[2] - b[0])

    # Space-based wrap first
    if " " in text:
        words = [w for w in text.split(" ") if w]
        lines: List[str] = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip() if current else word
            if width_of(candidate) <= max_width or not current:
                current = candidate
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    # Fallback: character-based wrap (useful for Korean)
    lines = []
    current = ""
    for ch in text:
        candidate = f"{current}{ch}"
        if width_of(candidate) <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def _draw_rounded_rect(draw, box: Tuple[int, int, int, int], radius: int, fill: Tuple[int, int, int, int]):
    try:
        draw.rounded_rectangle(box, radius=radius, fill=fill)  # type: ignore[attr-defined]
    except Exception:
        # Basic fallback without rounded corners
        draw.rectangle(box, fill=fill)
