"""
Text Overlay Module

Adds text overlay to images using SVG composition and exports to PNG.
Uses svg-canvas MCP tools for SVG generation.

Workflow:
1. Load background image (PNG/JPG)
2. Create SVG canvas with same dimensions
3. Insert background image
4. Add text elements with styling
5. Export to PNG
"""

import base64
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image
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
    Processor for adding text overlay to images via SVG composition.

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
            # 1. Get image dimensions
            width, height = self._get_image_dimensions(
                config.background_image_path,
                config.width,
                config.height
            )

            # 2. Generate SVG content
            svg_content = self._generate_svg(
                config.background_image_path,
                width,
                height,
                config.text_elements
            )

            # 3. Save temporary SVG
            svg_path = Path(self.temp_dir) / f"overlay_{os.getpid()}.svg"
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(svg_content)

            # 4. Convert SVG to PNG
            output_path = Path(config.output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            success = self._convert_svg_to_png(str(svg_path), str(output_path), width, height)

            # 5. Cleanup
            if svg_path.exists():
                svg_path.unlink()

            if success:
                return {
                    "success": True,
                    "output_path": str(output_path),
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "output_path": None,
                    "error": "SVG to PNG conversion failed"
                }

        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "error": str(e)
            }

    def _get_image_dimensions(
        self,
        image_path: str,
        override_width: int = 0,
        override_height: int = 0
    ) -> Tuple[int, int]:
        """Get image dimensions, using overrides if provided."""
        if override_width > 0 and override_height > 0:
            return override_width, override_height

        with Image.open(image_path) as img:
            return img.size

    def _generate_svg(
        self,
        background_path: str,
        width: int,
        height: int,
        text_elements: List[TextElement]
    ) -> str:
        """Generate SVG content with background image and text overlay."""
        # Convert background image to base64 data URI
        image_data_uri = self._image_to_data_uri(background_path)

        # Build SVG content
        svg_parts = [
            f'<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'  <defs>',
            f'    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">',
            f'      <feDropShadow dx="2" dy="2" stdDeviation="2" flood-color="rgba(0,0,0,0.5)" flood-opacity="0.5"/>',
            f'    </filter>',
            f'  </defs>',
            f'  <!-- Background Image -->',
            f'  <image href="{image_data_uri}" x="0" y="0" width="{width}" height="{height}" preserveAspectRatio="xMidYMid slice"/>',
        ]

        # Add text elements
        for i, elem in enumerate(text_elements):
            svg_parts.append(f'  <!-- Text Element {i + 1} -->')

            # Add background box if enabled
            if elem.background_box:
                # Estimate text width (rough approximation)
                text_width = len(elem.text) * elem.font_size * 0.6
                text_height = elem.font_size * 1.2

                box_x = elem.x - text_width / 2 - elem.background_box_padding if elem.text_anchor == "middle" else elem.x - elem.background_box_padding
                box_y = elem.y - elem.font_size - elem.background_box_padding

                svg_parts.append(
                    f'  <rect x="{box_x}" y="{box_y}" '
                    f'width="{text_width + elem.background_box_padding * 2}" '
                    f'height="{text_height + elem.background_box_padding * 2}" '
                    f'rx="{elem.background_box_radius}" '
                    f'fill="{elem.background_box_color}"/>'
                )

            # Add shadow text if enabled
            if elem.shadow:
                svg_parts.append(
                    f'  <text x="{elem.x + elem.shadow_offset_x}" y="{elem.y + elem.shadow_offset_y}" '
                    f'font-family="{elem.font_family}" font-size="{elem.font_size}px" '
                    f'font-weight="{elem.font_weight}" fill="{elem.shadow_color}" '
                    f'text-anchor="{elem.text_anchor}">{self._escape_xml(elem.text)}</text>'
                )

            # Add main text
            svg_parts.append(
                f'  <text x="{elem.x}" y="{elem.y}" '
                f'font-family="{elem.font_family}" font-size="{elem.font_size}px" '
                f'font-weight="{elem.font_weight}" fill="{elem.fill}" '
                f'text-anchor="{elem.text_anchor}">{self._escape_xml(elem.text)}</text>'
            )

        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)

    def _image_to_data_uri(self, image_path: str) -> str:
        """Convert image file to base64 data URI."""
        with open(image_path, "rb") as f:
            image_data = f.read()

        # Detect MIME type
        ext = Path(image_path).suffix.lower()
        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        mime_type = mime_types.get(ext, "image/png")

        # Encode to base64
        b64_data = base64.b64encode(image_data).decode("utf-8")
        return f"data:{mime_type};base64,{b64_data}"

    def _escape_xml(self, text: str) -> str:
        """Escape special XML characters."""
        return (
            text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )

    def _convert_svg_to_png(
        self,
        svg_path: str,
        output_path: str,
        width: int,
        height: int
    ) -> bool:
        """
        Convert SVG to PNG using available tools.

        Tries multiple methods in order:
        1. cairosvg (Python library)
        2. rsvg-convert (command line)
        3. inkscape (command line)
        """
        # Method 1: cairosvg
        try:
            import cairosvg
            cairosvg.svg2png(
                url=svg_path,
                write_to=output_path,
                output_width=width,
                output_height=height
            )
            return True
        except ImportError:
            pass
        except Exception:
            pass

        # Method 2: rsvg-convert
        try:
            result = subprocess.run(
                [
                    "rsvg-convert",
                    "-w", str(width),
                    "-h", str(height),
                    "-o", output_path,
                    svg_path
                ],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True
        except FileNotFoundError:
            pass
        except Exception:
            pass

        # Method 3: inkscape
        try:
            result = subprocess.run(
                [
                    "inkscape",
                    svg_path,
                    "--export-type=png",
                    f"--export-filename={output_path}",
                    f"--export-width={width}",
                    f"--export-height={height}"
                ],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True
        except FileNotFoundError:
            pass
        except Exception:
            pass

        # Method 4: Pillow with svglib (fallback)
        try:
            from svglib.svglib import svg2rlg
            from reportlab.graphics import renderPM

            drawing = svg2rlg(svg_path)
            renderPM.drawToFile(drawing, output_path, fmt="PNG")
            return True
        except ImportError:
            pass
        except Exception:
            pass

        return False


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
    # Get image dimensions
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


def add_text_to_existing_image(
    image_path: str,
    text_config: 'TextOverlayConfig',
    output_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Add text overlay to an existing image using TextOverlayConfig from prompt_converter.

    Args:
        image_path: Path to source image
        text_config: TextOverlayConfig from prompt_converter module
        output_path: Output path (overwrites source if None)

    Returns:
        Dict with 'success', 'output_path', 'error'
    """
    from .prompt_converter import TextOverlayConfig as PromptTextConfig

    # Get image dimensions
    with Image.open(image_path) as img:
        width, height = img.size

    # Calculate position
    center_x = width // 2
    positions = {
        "center": (center_x, height // 2),
        "top": (center_x, height // 4),
        "bottom": (center_x, height * 3 // 4),
        "top-left": (width // 6, height // 4),
        "top-right": (width * 5 // 6, height // 4),
        "bottom-left": (width // 6, height * 3 // 4),
        "bottom-right": (width * 5 // 6, height * 3 // 4),
    }

    x, y = positions.get(text_config.position, positions["center"])

    # Create text elements
    text_elements = []

    if text_config.main_text:
        text_elements.append(
            TextElement(
                text=text_config.main_text,
                x=x,
                y=y,
                font_size=text_config.font_size,
                font_family=text_config.font_family,
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
        sub_y = y + text_config.font_size + 20
        text_elements.append(
            TextElement(
                text=text_config.sub_text,
                x=x,
                y=sub_y,
                font_size=int(text_config.font_size * 0.5),
                font_family=text_config.font_family,
                fill=text_config.font_color,
                text_anchor="middle" if "left" not in text_config.position else "start",
                shadow=text_config.shadow,
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
