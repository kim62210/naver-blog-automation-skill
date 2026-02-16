"""
Shared type definitions for the search-blogging project.

Centralizes common dataclasses to avoid duplication across modules.
All modules should import types from here instead of defining their own.

Usage:
    from scripts.shared_types import ImageResult, BatchResult, ValidationResult
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ==============================================================================
# Image Generation Types
# ==============================================================================


@dataclass
class ImageResult:
    """Result of a single image generation operation"""

    success: bool
    file_path: Optional[str] = None
    prompt: str = ""
    model_used: str = ""
    error_message: Optional[str] = None
    generation_time: float = 0.0

    def __str__(self) -> str:
        if self.success:
            return f"✅ {self.file_path} ({self.model_used})"
        return f"❌ {self.error_message}"


@dataclass
class BatchResult:
    """Result of batch image generation"""

    total: int = 0
    success_count: int = 0
    failed_count: int = 0
    results: List[ImageResult] = field(default_factory=list)
    total_time: float = 0.0

    @property
    def success_rate(self) -> float:
        return (self.success_count / self.total * 100) if self.total else 0.0

    def summary(self) -> str:
        return f"📊 {self.success_count}/{self.total} ({self.success_rate:.1f}%), {self.total_time:.1f}s"


# ==============================================================================
# Watermark Types (NEW - recommended for AI text rendering workflow)
# ==============================================================================


@dataclass
class WatermarkConfig:
    """
    Configuration for watermark overlay.

    Used for adding watermark only to AI-generated images.
    Text rendering is now handled by AI, not PIL overlay.
    """

    watermark_text: str = "@money-lab-brian"
    watermark_position: str = "bottom-center"  # "bottom-center", "bottom-left", "bottom-right"
    watermark_margin_bottom: int = 60
    watermark_font_size: int = 18
    watermark_font_color: str = "rgba(255,255,255,0.6)"
    watermark_font_family: str = "Pretendard, Nanum Gothic, sans-serif"
    watermark_enabled: bool = True


# ==============================================================================
# Text Overlay Types (DEPRECATED - kept for backward compatibility)
# ==============================================================================


@dataclass
class TextStyleConfig:
    """
    DEPRECATED: Use WatermarkConfig instead.

    Style configuration for text overlay (font, color, position).
    This is kept for backward compatibility only.
    """

    main_text: str = ""
    sub_text: str = ""
    position: str = "center"  # center, top, bottom, top-left, etc.
    font_size: int = 48
    font_color: str = "#FFFFFF"
    font_family: str = "Pretendard, Nanum Gothic, sans-serif"
    shadow: bool = True
    shadow_color: str = "rgba(0,0,0,0.5)"
    shadow_offset: int = 2
    background_box: bool = False
    background_box_color: str = "rgba(0,0,0,0.3)"
    background_box_padding: int = 20


@dataclass
class TextElement:
    """Single text element for SVG overlay"""

    text: str
    x: int
    y: int
    font_size: int = 48
    font_family: str = "Pretendard, Nanum Gothic, sans-serif"
    font_weight: str = "bold"
    fill: str = "#FFFFFF"
    text_anchor: str = "middle"
    shadow: bool = True
    shadow_color: str = "rgba(0,0,0,0.5)"
    shadow_offset_x: int = 2
    shadow_offset_y: int = 2
    background_box: bool = False
    background_box_color: str = "rgba(0,0,0,0.3)"
    background_box_padding: int = 20
    background_box_radius: int = 10


@dataclass
class OverlayConfig:
    """Configuration for text overlay operation (paths, dimensions)"""

    background_image_path: str
    output_path: str
    width: int = 0  # Auto-detect from image if 0
    height: int = 0
    text_elements: List[TextElement] = field(default_factory=list)


# ==============================================================================
# Validation Types
# ==============================================================================


@dataclass
class ValidationResult:
    """Result of content validation (character count, etc.)"""

    is_valid: bool
    char_count: int = 0
    target: int = 1900
    min_chars: int = 1850
    max_chars: int = 1950
    status: str = "ok"  # "ok", "under", "over"
    difference: int = 0
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


# ==============================================================================
# Collection Types
# ==============================================================================


@dataclass
class ImageInfo:
    """Information about a collected/downloaded image"""

    url: str
    source_url: str = ""
    source_name: str = ""
    description: str = ""
    image_type: str = ""
    filename: Optional[str] = None
    local_path: Optional[str] = None
    downloaded: bool = False
    success: bool = False
    error: str = ""


@dataclass
class CollectionResult:
    """Result of image collection operation"""

    total: int = 0
    success_count: int = 0
    failed_count: int = 0
    success: int = 0  # Alias for success_count (backward compatibility)
    failed: int = 0   # Alias for failed_count (backward compatibility)
    images: List[ImageInfo] = field(default_factory=list)
    output_dir: str = ""

    def __post_init__(self):
        # Sync alias fields
        if self.success_count == 0 and self.success > 0:
            self.success_count = self.success
        elif self.success == 0 and self.success_count > 0:
            self.success = self.success_count

        if self.failed_count == 0 and self.failed > 0:
            self.failed_count = self.failed
        elif self.failed == 0 and self.failed_count > 0:
            self.failed = self.failed_count

    @property
    def success_rate(self) -> float:
        return (self.success_count / self.total * 100) if self.total else 0.0


# ==============================================================================
# Prompt Conversion Types
# ==============================================================================


@dataclass
class ImageGuideItem:
    """Data class for parsed image guide items"""

    index: int
    role: str
    mode: str  # "A" (reference), "B" (AI generation), "B-3" (AI + watermark)
    korean_description: str = ""
    prompt: str = ""
    style_guide: Dict[str, str] = field(default_factory=dict)
    filename: str = ""
    watermark_config: Optional[WatermarkConfig] = None
    # Deprecated: kept for backward compatibility
    text_overlay: Optional[TextStyleConfig] = None


@dataclass
class GeminiPrompt:
    """Data class for Gemini API prompts"""

    prompt: str
    filename: str
    aspect_ratio: str = "16:9"
    style_hints: str = ""


# ==============================================================================
# Pipeline Types
# ==============================================================================


@dataclass
class PipelineConfig:
    """Configuration for the image pipeline"""

    output_dir: str
    use_text_overlay: bool = True
    concurrent_limit: int = 2
    default_size: str = "500x500"
    cleanup_temp: bool = True


@dataclass
class PipelineItem:
    """Single item in the image generation pipeline"""

    index: int
    role: str
    prompt: str
    filename: str
    watermark_config: Optional[WatermarkConfig] = None
    text_config: Optional[TextStyleConfig] = None  # Deprecated
    mode: str = "B"  # A: Reference, B: AI Generation, B-3: AI + Watermark


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
        return (
            f"📊 Pipeline result: {self.success_count}/{self.total} succeeded "
            f"({self.text_overlay_count} with text overlay), "
            f"time elapsed: {self.total_time:.1f}s"
        )
