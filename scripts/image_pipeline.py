"""
Image Pipeline Module

Integrated pipeline for generating blog images with watermark support.
Combines Gemini API image generation with PIL watermark application.

Workflow:
1. Parse image guide content
2. Extract prompts and watermark configs
3. Generate images via Gemini API (AI renders text directly)
4. Apply watermark via PIL
5. Export final PNG images
"""

import asyncio
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .config import get_config, get_config_value
from .gemini_image import GeminiImageGenerator, ImageResult, BatchResult
from .image_guide_parser import extract_first_prompt, split_image_sections
from .prompt_converter import (
    WatermarkConfig,
    extract_watermark_config,
)
from .text_overlay import TextOverlayProcessor, add_watermark_to_image


@dataclass
class PipelineConfig:
    """Configuration for the image pipeline"""

    output_dir: str
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
    watermark_config: Optional[WatermarkConfig] = None
    mode: str = "B"  # B: AI Generation (with text), B-3: AI + Watermark Only


@dataclass
class PipelineResult:
    """Result of pipeline execution"""

    total: int = 0
    success_count: int = 0
    failed_count: int = 0
    results: List[ImageResult] = field(default_factory=list)
    total_time: float = 0.0

    def summary(self) -> str:
        """Generate summary string"""
        return (
            f"Pipeline result: {self.success_count}/{self.total} succeeded, "
            f"time elapsed: {self.total_time:.1f}s"
        )


class ImagePipeline:
    """
    Integrated image generation pipeline.

    Combines:
    - Gemini API for image generation (AI renders text directly)
    - PIL for watermark application
    - PNG export for final output

    Usage:
        pipeline = ImagePipeline()

        # Option 1: Generate single image with watermark
        result = await pipeline.generate_with_watermark(
            prompt="Blog thumbnail, bold Korean text '...' in upper third...",
            output_path="./images/01_thumbnail.png",
            watermark_config=WatermarkConfig(watermark_text="@money-lab-brian")
        )

        # Option 2: Process entire image guide
        with open("image_guide.md", "r") as f:
            content = f.read()

        result = await pipeline.process_image_guide(
            image_guide_content=content,
            output_dir="./images/"
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

    def _get_default_watermark_config(self) -> WatermarkConfig:
        config = get_config()
        return WatermarkConfig(
            watermark_text=get_config_value(config, "watermark", "text", default="@money-lab-brian"),
            watermark_position=get_config_value(config, "watermark", "position", default="bottom-center"),
            watermark_margin_bottom=int(get_config_value(config, "watermark", "margin_bottom", default=60)),
            watermark_font_size=int(get_config_value(config, "watermark", "font_size", default=18)),
            watermark_font_color=get_config_value(config, "watermark", "font_color", default="rgba(255,255,255,0.6)"),
            watermark_font_family=get_config_value(config, "watermark", "font_family", default="Pretendard, Nanum Gothic, sans-serif"),
            watermark_enabled=bool(get_config_value(config, "watermark", "enabled", default=True)),
        )

    async def generate_with_watermark(
        self,
        prompt: str,
        output_path: str,
        watermark_config: Optional[WatermarkConfig] = None,
        size: str = "1024x1024",
    ) -> ImageResult:
        """
        Generate a single image with AI-rendered text + watermark only.

        AI renders all text directly in the image (main_text, sub_text in prompt).
        PIL only adds watermark at bottom-center.

        Args:
            prompt: Image generation prompt (including text instructions for AI)
            output_path: Final output path for PNG
            watermark_config: Watermark configuration (optional, uses default if None)
            size: Image size

        Returns:
            ImageResult: Generation result

        Example:
            result = await pipeline.generate_with_watermark(
                prompt="Blog thumbnail, bold Korean text '...' in upper third...",
                output_path="./images/01_thumbnail.png",
                watermark_config=WatermarkConfig(watermark_text="@money-lab-brian")
            )
        """
        # Use default watermark config if not provided
        if watermark_config is None:
            watermark_config = self._get_default_watermark_config()

        return await self.generator.generate_with_watermark(
            prompt=prompt,
            output_path=output_path,
            watermark_config=watermark_config,
            size=size,
        )

    async def process_image_guide(
        self,
        image_guide_content: str,
        output_dir: str,
        concurrent_limit: int = 2,
    ) -> PipelineResult:
        """
        Process an entire image guide file and generate all images.

        Args:
            image_guide_content: Content of the image guide markdown
            output_dir: Output directory for generated images
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

        # Default watermark config - applied to all images
        default_watermark = self._get_default_watermark_config()

        # Build batch items
        batch_items = []
        for item in items:
            # Determine watermark config: explicit config > default (always apply)
            effective_watermark = item.watermark_config if item.watermark_config else default_watermark

            batch_item = {
                "prompt": item.prompt,
                "filename": item.filename,
                # Apply watermark to all modes (Mode B, B-3)
                "watermark_config": effective_watermark,
            }
            batch_items.append(batch_item)

        # Execute batch generation
        batch_result = await self.generator.generate_batch_with_text_overlay(
            items=batch_items,
            output_dir=output_dir,
            concurrent_limit=concurrent_limit,
        )

        total_time = (datetime.now() - start_time).total_seconds()

        return PipelineResult(
            total=batch_result.total,
            success_count=batch_result.success_count,
            failed_count=batch_result.failed_count,
            results=batch_result.results,
            total_time=total_time,
        )

    def _parse_image_guide(self, content: str) -> List[PipelineItem]:
        """
        Parse image guide markdown to extract pipeline items.

        Supports formats:
        - Mode B: AI Generation (text rendered by AI)
        - Mode B-3: AI Generation + explicit Watermark Config

        Args:
            content: Image guide markdown content

        Returns:
            List of PipelineItem
        """
        items: List[PipelineItem] = []

        for section in split_image_sections(content):
            item = self._parse_image_section(section.index, section.role, section.body)
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
        # Check for Mode B-3 (AI renders text + Watermark Only) - preferred format
        if "[Watermark Config]" in content or "watermark config" in content.lower():
            return self._parse_mode_b3(index, role, content)

        # Check for Mode B (Regular AI Generation with text in prompt)
        if "AI Generation" in content or "AI Generation Prompt" in content:
            return self._parse_mode_b(index, role, content)

        # Fallback: try to extract a prompt from any section with a fenced code block
        prompt = extract_first_prompt(content)
        if prompt:
            return PipelineItem(
                index=index,
                role=role,
                prompt=prompt,
                filename=self._generate_filename(index, role),
                mode="B",
            )

        return None

    def _parse_mode_b(
        self, index: int, role: str, content: str
    ) -> Optional[PipelineItem]:
        """Parse Mode B (AI Generation) section"""
        # Extract prompt (first fenced code block)
        prompt = extract_first_prompt(content)
        if not prompt:
            return None

        # Generate filename
        filename = self._generate_filename(index, role)

        return PipelineItem(
            index=index,
            role=role,
            prompt=prompt,
            filename=filename,
            mode="B",
        )

    def _parse_mode_b3(
        self, index: int, role: str, content: str
    ) -> Optional[PipelineItem]:
        """
        Parse Mode B-3 (AI renders text + Watermark Only) section.

        This is the preferred format where:
        - AI prompt includes text rendering instructions
        - PIL only adds watermark to the final image
        """
        # Extract prompt (includes text instructions for AI)
        prompt = extract_first_prompt(content)
        if not prompt:
            return None

        # Extract watermark config
        watermark_config = extract_watermark_config(content)

        # Generate filename
        filename = self._generate_filename(index, role)

        return PipelineItem(
            index=index,
            role=role,
            prompt=prompt,
            filename=filename,
            watermark_config=watermark_config,
            mode="B-3",
        )

    def _generate_filename(self, index: int, role: str) -> str:
        """
        Generate filename from index and role.

        Args:
            index: Image index
            role: Image role description

        Returns:
            Filename string (e.g., "01_thumbnail.png")
        """
        # Clean role for filename
        clean_role = re.sub(r"[^\w가-힣\s]", "", role)
        clean_role = clean_role.strip().replace(" ", "_")[:20]

        if not clean_role:
            clean_role = "image"

        return f"{index:02d}_{clean_role}.png"


# Convenience functions for direct usage

async def process_image_guide_file(
    guide_path: str,
    output_dir: str,
    api_key: Optional[str] = None,
) -> PipelineResult:
    """
    Convenience function to process an image guide file.

    Args:
        guide_path: Path to the image guide markdown file
        output_dir: Output directory for generated images
        api_key: Google API key (optional)

    Returns:
        PipelineResult: Pipeline execution result

    Example:
        result = await process_image_guide_file(
            guide_path="./image_guide.md",
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
    )


def process_image_guide_file_sync(
    guide_path: str,
    output_dir: str,
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
            api_key=api_key,
        )
    )
