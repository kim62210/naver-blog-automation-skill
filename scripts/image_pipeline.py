"""
Image Pipeline Module

Integrated pipeline for generating blog images with text overlay support.
Combines Gemini API image generation with SVG text composition.

Workflow:
1. Parse image guide content
2. Extract prompts and text overlay configs
3. Generate background images via Gemini API
4. Apply text overlay using SVG composition
5. Export final PNG images
"""

import asyncio
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .gemini_image import GeminiImageGenerator, ImageResult, BatchResult
from .prompt_converter import TextOverlayConfig, extract_text_config, strip_text_instructions
from .text_overlay import TextOverlayProcessor, create_thumbnail_with_text


@dataclass
class PipelineConfig:
    """Configuration for the image pipeline"""

    output_dir: str
    use_text_overlay: bool = True
    concurrent_limit: int = 2
    default_size: str = "1024x1024"
    cleanup_temp: bool = True


@dataclass
class PipelineItem:
    """Single item in the pipeline"""

    index: int
    role: str  # e.g., "Thumbnail", "Infographic", etc.
    prompt: str
    filename: str
    text_config: Optional[TextOverlayConfig] = None
    mode: str = "B"  # A: Reference, B: AI Generation, B-2: AI + Text Overlay, C: SVG


@dataclass
class PipelineResult:
    """Result of pipeline execution"""

    total: int = 0
    success_count: int = 0
    failed_count: int = 0
    text_overlay_count: int = 0
    results: List[ImageResult] = field(default_factory=list)
    total_time: float = 0.0

    def summary(self) -> str:
        """Generate summary string"""
        return (
            f"📊 Pipeline result: {self.success_count}/{self.total} succeeded "
            f"({self.text_overlay_count} with text overlay), "
            f"time elapsed: {self.total_time:.1f}s"
        )


class ImagePipeline:
    """
    Integrated image generation pipeline.

    Combines:
    - Gemini API for background image generation
    - SVG composition for text overlay
    - PNG export for final output

    Usage:
        pipeline = ImagePipeline()

        # Option 1: Generate single image with text overlay
        result = await pipeline.generate_with_text_overlay(
            prompt="Blog thumbnail, finance concept...",
            output_path="./images/01_썸네일.png",
            text_config=TextOverlayConfig(
                main_text="제목 텍스트",
                sub_text="부제목"
            )
        )

        # Option 2: Process entire image guide
        with open("이미지 가이드.md", "r") as f:
            content = f.read()

        result = await pipeline.process_image_guide(
            image_guide_content=content,
            output_dir="./images/",
            use_text_overlay=True
        )
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize ImagePipeline.

        Args:
            api_key: Google API key (optional, loads from env if not provided)
        """
        self.generator = GeminiImageGenerator(api_key=api_key)
        self.overlay_processor = TextOverlayProcessor()

    async def generate_with_text_overlay(
        self,
        prompt: str,
        output_path: str,
        text_config: TextOverlayConfig,
        size: str = "1024x1024",
    ) -> ImageResult:
        """
        Generate a single image with text overlay.

        Args:
            prompt: Image generation prompt (text will be stripped)
            output_path: Final output path for PNG
            text_config: Text overlay configuration
            size: Image size

        Returns:
            ImageResult: Generation result
        """
        return await self.generator.generate_with_text_overlay(
            prompt=prompt,
            output_path=output_path,
            text_config=text_config,
            size=size,
        )

    async def process_image_guide(
        self,
        image_guide_content: str,
        output_dir: str,
        use_text_overlay: bool = True,
        concurrent_limit: int = 2,
    ) -> PipelineResult:
        """
        Process an entire image guide file and generate all images.

        Args:
            image_guide_content: Content of the image guide markdown
            output_dir: Output directory for generated images
            use_text_overlay: Whether to use text overlay for Mode B-2 items
            concurrent_limit: Concurrent generation limit

        Returns:
            PipelineResult: Pipeline execution result
        """
        start_time = datetime.now()

        # Parse image guide to extract items
        items = self._parse_image_guide(image_guide_content)

        if not items:
            return PipelineResult(
                total=0,
                success_count=0,
                failed_count=0,
                results=[],
                total_time=0.0,
            )

        # Prepare output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Build batch items
        batch_items = []
        for item in items:
            batch_item = {
                "prompt": item.prompt,
                "filename": item.filename,
                "text_config": item.text_config if use_text_overlay else None,
            }
            batch_items.append(batch_item)

        # Execute batch generation
        batch_result = await self.generator.generate_batch_with_text_overlay(
            items=batch_items,
            output_dir=output_dir,
            concurrent_limit=concurrent_limit,
        )

        # Count text overlay items
        text_overlay_count = sum(1 for item in items if item.text_config is not None)

        total_time = (datetime.now() - start_time).total_seconds()

        return PipelineResult(
            total=batch_result.total,
            success_count=batch_result.success_count,
            failed_count=batch_result.failed_count,
            text_overlay_count=text_overlay_count,
            results=batch_result.results,
            total_time=total_time,
        )

    def _parse_image_guide(self, content: str) -> List[PipelineItem]:
        """
        Parse image guide markdown to extract pipeline items.

        Supports formats:
        - Mode A: 📷 Reference Image
        - Mode B: 🎨 AI Generation
        - Mode B-2: 🎨 AI Generation (Background Only) + Text Overlay
        - Mode C: 🔷 SVG Generation

        Args:
            content: Image guide markdown content

        Returns:
            List of PipelineItem
        """
        items = []

        # Split by image sections
        image_pattern = r"##\s*\[Image\s*(\d+)\]\s*(.+?)(?=##\s*\[Image|\Z)"
        matches = re.findall(image_pattern, content, re.DOTALL | re.IGNORECASE)

        for match in matches:
            index = int(match[0])
            section_content = match[1]

            # Extract role (first line after the header)
            role_match = re.search(r"^\s*(.+?)\s*$", section_content.split("\n")[0])
            role = role_match.group(1) if role_match else f"Image {index}"

            # Determine mode and extract relevant data
            item = self._parse_image_section(index, role, section_content)
            if item:
                items.append(item)

        return items

    def _parse_image_section(
        self, index: int, role: str, content: str
    ) -> Optional[PipelineItem]:
        """
        Parse a single image section from the guide.

        Args:
            index: Image index
            role: Image role description
            content: Section content

        Returns:
            PipelineItem or None if parsing fails
        """
        # Check for Mode B-2 (Background Only + Text Overlay)
        if "AI Generation (Background Only)" in content or "Background Only" in content:
            return self._parse_mode_b2(index, role, content)

        # Check for Mode B (Regular AI Generation)
        if "🎨 AI Generation" in content or "AI Generation Prompt" in content:
            return self._parse_mode_b(index, role, content)

        # Check for Mode A (Reference Image)
        if "📷" in content or "Reference Image" in content or "Downloaded image" in content:
            return self._parse_mode_a(index, role, content)

        # Check for Mode C (SVG Generation)
        if "🔷" in content or "SVG Generation" in content:
            return self._parse_mode_c(index, role, content)

        return None

    def _parse_mode_a(
        self, index: int, role: str, content: str
    ) -> Optional[PipelineItem]:
        """Parse Mode A (Reference Image) section"""
        # Mode A uses downloaded reference images, not generated
        # Return None as we don't generate these
        return None

    def _parse_mode_b(
        self, index: int, role: str, content: str
    ) -> Optional[PipelineItem]:
        """Parse Mode B (AI Generation) section"""
        # Extract prompt from code block
        prompt_match = re.search(
            r"AI Generation Prompt[:\s]*\n```\n?(.*?)\n?```",
            content,
            re.DOTALL | re.IGNORECASE
        )
        if not prompt_match:
            # Try alternative format
            prompt_match = re.search(
                r"\*\*AI Generation Prompt[:\s]*\*\*\s*\n```\n?(.*?)\n?```",
                content,
                re.DOTALL | re.IGNORECASE
            )

        if not prompt_match:
            return None

        prompt = prompt_match.group(1).strip()

        # Generate filename
        filename = self._generate_filename(index, role)

        return PipelineItem(
            index=index,
            role=role,
            prompt=prompt,
            filename=filename,
            text_config=None,
            mode="B",
        )

    def _parse_mode_b2(
        self, index: int, role: str, content: str
    ) -> Optional[PipelineItem]:
        """Parse Mode B-2 (AI Generation + Text Overlay) section"""
        # Extract background-only prompt
        prompt_match = re.search(
            r"(?:AI Generation Prompt|Background Only)[:\s]*\n```\n?(.*?)\n?```",
            content,
            re.DOTALL | re.IGNORECASE
        )
        if not prompt_match:
            return None

        prompt = prompt_match.group(1).strip()

        # Extract text overlay config
        text_config = self._extract_text_overlay_config(content)

        # Generate filename
        filename = self._generate_filename(index, role)

        return PipelineItem(
            index=index,
            role=role,
            prompt=prompt,
            filename=filename,
            text_config=text_config,
            mode="B-2",
        )

    def _parse_mode_c(
        self, index: int, role: str, content: str
    ) -> Optional[PipelineItem]:
        """Parse Mode C (SVG Generation) section"""
        # Mode C uses SVG generation, not Gemini API
        # Return None as this requires different handling
        return None

    def _extract_text_overlay_config(self, content: str) -> Optional[TextOverlayConfig]:
        """
        Extract TextOverlayConfig from section content.

        Looks for patterns like:
        - main_text: "..."
        - sub_text: "..."
        - position: "center"
        - font_size: 48
        etc.
        """
        config_kwargs = {}

        # Extract main_text
        main_text_match = re.search(
            r"main_text[:\s]*[\"'](.+?)[\"']",
            content,
            re.IGNORECASE
        )
        if main_text_match:
            config_kwargs["main_text"] = main_text_match.group(1)

        # Extract sub_text
        sub_text_match = re.search(
            r"sub_text[:\s]*[\"'](.+?)[\"']",
            content,
            re.IGNORECASE
        )
        if sub_text_match:
            config_kwargs["sub_text"] = sub_text_match.group(1)

        # Extract position
        position_match = re.search(
            r"position[:\s]*[\"'](.+?)[\"']",
            content,
            re.IGNORECASE
        )
        if position_match:
            config_kwargs["position"] = position_match.group(1)

        # Extract font_size
        font_size_match = re.search(
            r"font_size[:\s]*(\d+)",
            content,
            re.IGNORECASE
        )
        if font_size_match:
            config_kwargs["font_size"] = int(font_size_match.group(1))

        # Extract font_color
        font_color_match = re.search(
            r"font_color[:\s]*[\"'](.+?)[\"']",
            content,
            re.IGNORECASE
        )
        if font_color_match:
            config_kwargs["font_color"] = font_color_match.group(1)

        # Extract shadow
        shadow_match = re.search(
            r"shadow[:\s]*(true|false)",
            content,
            re.IGNORECASE
        )
        if shadow_match:
            config_kwargs["shadow"] = shadow_match.group(1).lower() == "true"

        # Extract background_box
        bg_box_match = re.search(
            r"background_box[:\s]*(true|false)",
            content,
            re.IGNORECASE
        )
        if bg_box_match:
            config_kwargs["background_box"] = bg_box_match.group(1).lower() == "true"

        # Only return config if we have at least main_text
        if "main_text" in config_kwargs:
            return TextOverlayConfig(**config_kwargs)

        return None

    def _generate_filename(self, index: int, role: str) -> str:
        """
        Generate filename from index and role.

        Args:
            index: Image index
            role: Image role description

        Returns:
            Filename string (e.g., "01_썸네일.png")
        """
        # Clean role for filename
        clean_role = re.sub(r"[^\w가-힣\s]", "", role)
        clean_role = clean_role.strip().replace(" ", "_")[:20]

        if not clean_role:
            clean_role = "image"

        return f"{index:02d}_{clean_role}.png"


# Convenience functions for direct usage

async def generate_blog_image(
    prompt: str,
    output_path: str,
    main_text: str,
    sub_text: str = "",
    position: str = "center",
    font_size: int = 48,
    font_color: str = "#FFFFFF",
    shadow: bool = True,
    api_key: Optional[str] = None,
) -> ImageResult:
    """
    Convenience function to generate a single blog image with text overlay.

    Args:
        prompt: Background image generation prompt
        output_path: Output file path
        main_text: Main title text
        sub_text: Subtitle text (optional)
        position: Text position
        font_size: Font size
        font_color: Font color (hex)
        shadow: Whether to add text shadow
        api_key: Google API key (optional)

    Returns:
        ImageResult: Generation result

    Example:
        result = await generate_blog_image(
            prompt="Finance blog thumbnail, money growing concept, green gradient",
            output_path="./images/thumbnail.png",
            main_text="2026년 적금 가이드",
            sub_text="연 5% 고금리 상품 총정리"
        )
    """
    pipeline = ImagePipeline(api_key=api_key)

    text_config = TextOverlayConfig(
        main_text=main_text,
        sub_text=sub_text,
        position=position,
        font_size=font_size,
        font_color=font_color,
        shadow=shadow,
    )

    return await pipeline.generate_with_text_overlay(
        prompt=prompt,
        output_path=output_path,
        text_config=text_config,
    )


def generate_blog_image_sync(
    prompt: str,
    output_path: str,
    main_text: str,
    sub_text: str = "",
    position: str = "center",
    font_size: int = 48,
    font_color: str = "#FFFFFF",
    shadow: bool = True,
    api_key: Optional[str] = None,
) -> ImageResult:
    """
    Synchronous wrapper for generate_blog_image.

    See generate_blog_image for arguments.
    """
    return asyncio.run(
        generate_blog_image(
            prompt=prompt,
            output_path=output_path,
            main_text=main_text,
            sub_text=sub_text,
            position=position,
            font_size=font_size,
            font_color=font_color,
            shadow=shadow,
            api_key=api_key,
        )
    )


async def process_image_guide_file(
    guide_path: str,
    output_dir: str,
    use_text_overlay: bool = True,
    api_key: Optional[str] = None,
) -> PipelineResult:
    """
    Convenience function to process an image guide file.

    Args:
        guide_path: Path to the image guide markdown file
        output_dir: Output directory for generated images
        use_text_overlay: Whether to use text overlay
        api_key: Google API key (optional)

    Returns:
        PipelineResult: Pipeline execution result

    Example:
        result = await process_image_guide_file(
            guide_path="./이미지 가이드.md",
            output_dir="./images/"
        )
        print(result.summary())
    """
    with open(guide_path, "r", encoding="utf-8") as f:
        content = f.read()

    pipeline = ImagePipeline(api_key=api_key)
    return await pipeline.process_image_guide(
        image_guide_content=content,
        output_dir=output_dir,
        use_text_overlay=use_text_overlay,
    )


def process_image_guide_file_sync(
    guide_path: str,
    output_dir: str,
    use_text_overlay: bool = True,
    api_key: Optional[str] = None,
) -> PipelineResult:
    """
    Synchronous wrapper for process_image_guide_file.

    See process_image_guide_file for arguments.
    """
    return asyncio.run(
        process_image_guide_file(
            guide_path=guide_path,
            output_dir=output_dir,
            use_text_overlay=use_text_overlay,
            api_key=api_key,
        )
    )
