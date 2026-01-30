"""
Shared type definitions for the naver-blog-automation project.

Centralizes common dataclasses to avoid duplication across modules.
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
# Text Overlay Types
# ==============================================================================


@dataclass
class TextStyleConfig:
    """Style configuration for text overlay (font, color, position)"""

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
    """Single text element for overlay"""

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
    """Result of content validation"""

    is_valid: bool
    char_count: int = 0
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


# ==============================================================================
# Collection Types
# ==============================================================================


@dataclass
class ImageInfo:
    """Information about a collected image"""

    url: str
    source_url: str = ""
    description: str = ""
    image_type: str = ""
    local_path: str = ""
    success: bool = False
    error: str = ""


@dataclass
class CollectionResult:
    """Result of image collection operation"""

    total: int = 0
    success_count: int = 0
    failed_count: int = 0
    images: List[ImageInfo] = field(default_factory=list)
    output_dir: str = ""

    @property
    def success_rate(self) -> float:
        return (self.success_count / self.total * 100) if self.total else 0.0
