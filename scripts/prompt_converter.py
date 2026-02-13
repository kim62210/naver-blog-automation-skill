"""
Prompt conversion module

Converts image guide prompts to Gemini API optimized format.
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .config import get_config, get_config_value
from .image_guide_parser import extract_first_prompt, split_image_sections


@dataclass
class WatermarkConfig:
    """
    Data class for watermark configuration.

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


@dataclass
class ImageGuideItem:
    """Data class for image guide items"""

    index: int
    role: str
    mode: str  # "B" (AI generation)
    korean_description: str = ""
    prompt: str = ""
    style_guide: Dict[str, str] = None
    filename: str = ""

    def __post_init__(self):
        if self.style_guide is None:
            self.style_guide = {}


@dataclass
class GeminiPrompt:
    """Data class for Gemini prompts"""

    prompt: str
    filename: str
    aspect_ratio: str = "16:9"
    style_hints: str = ""


def convert_to_gemini_prompt(
    image_guide: Dict[str, Any],
    background_only: bool = False,
) -> str:
    """
    Convert image guide prompt to Gemini optimized format.

    NOTE: As of the new workflow, AI now renders text directly.
    The background_only parameter is deprecated and kept for backward compatibility.
    Text is no longer stripped from prompts.

    Args:
        image_guide: Image guide dictionary
            - korean_description: Korean description
            - prompt: English prompt
            - style_guide: Style guide (colors, mood, format, ratio)
        background_only: DEPRECATED - no longer used, kept for backward compatibility

    Returns:
        Optimized prompt string for Gemini API

    Example:
        >>> guide = {
        ...     "korean_description": "아기 손과 돼지저금통 썸네일",
        ...     "prompt": "Blog thumbnail, baby savings concept, bold Korean text '0세 적금 필수!'",
        ...     "style_guide": {"색상": "따뜻한 노랑", "분위기": "친근한"}
        ... }
        >>> convert_to_gemini_prompt(guide)
        "Create a high-quality blog image. Blog thumbnail, baby savings concept..."
    """
    korean_desc = image_guide.get("korean_description", "")
    original_prompt = image_guide.get("prompt", "")
    style_guide = image_guide.get("style_guide", {})

    # Prompt components
    parts = []

    # 1. Base instruction
    parts.append("Create a high-quality image for a Korean blog.")

    # 2. English prompt (use existing prompt as-is, including text instructions)
    if original_prompt:
        # Remove ratio information (handled separately)
        cleaned_prompt = re.sub(r"\d+:\d+\s*ratio", "", original_prompt)
        # NOTE: No longer strip text instructions - AI renders text directly
        parts.append(cleaned_prompt.strip())

    # 3. Convert style guide
    style_parts = []

    if "색상" in style_guide:
        color = style_guide["색상"]
        color_en = translate_color(color)
        style_parts.append(f"Color scheme: {color_en}")

    if "분위기" in style_guide:
        mood = style_guide["분위기"]
        mood_en = translate_mood(mood)
        style_parts.append(f"Mood: {mood_en}")

    if "형식" in style_guide:
        format_type = style_guide["형식"]
        format_en = translate_format(format_type)
        style_parts.append(f"Style: {format_en}")

    if style_parts:
        parts.append(" ".join(style_parts))

    # 4. Quality assurance phrase
    parts.append("High resolution, professional quality, suitable for blog use.")

    return " ".join(parts)


def translate_color(korean_color: str) -> str:
    """Convert Korean color description to English"""
    color_map = {
        "파스텔 블루": "soft pastel blue",
        "파스텔 핑크": "soft pastel pink",
        "민트 그린": "mint green, seafoam",
        "따뜻한 노랑": "warm yellow, golden yellow",
        "네이비": "navy blue, deep blue",
        "골드": "gold, champagne gold",
        "코랄 핑크": "coral pink, soft coral",
        "그레이": "gray, neutral gray",
        "화이트": "white, clean white",
        "블랙": "black, elegant black",
        "베이지": "beige, warm beige",
        "그린": "green, fresh green",
        "오렌지": "orange, warm orange",
        "레드": "red, vibrant red",
        "퍼플": "purple, elegant purple",
        "그라데이션": "gradient",
    }

    for kr, en in color_map.items():
        if kr in korean_color:
            return korean_color.replace(kr, en)

    return korean_color


def translate_mood(korean_mood: str) -> str:
    """Convert Korean mood description to English"""
    mood_map = {
        "따뜻한": "warm, cozy",
        "친근한": "friendly, approachable",
        "전문적": "professional, expert",
        "신뢰감": "trustworthy, reliable",
        "깔끔한": "clean, neat",
        "모던한": "modern, contemporary",
        "세련된": "sophisticated, elegant",
        "밝은": "bright, cheerful",
        "차분한": "calm, serene",
        "활기찬": "energetic, lively",
        "감성적": "emotional, sentimental",
        "정보성": "informative, educational",
        "눈에 띄는": "eye-catching, attention-grabbing",
        "클릭 유도": "click-worthy, engaging",
        "희망적": "hopeful, optimistic",
        "사랑스러운": "lovely, adorable",
    }

    result = korean_mood
    for kr, en in mood_map.items():
        if kr in result:
            result = result.replace(kr, en)

    return result


def translate_format(korean_format: str) -> str:
    """Convert Korean format description to English"""
    format_map = {
        "인포그래픽": "infographic, data visualization",
        "일러스트": "illustration, illustrated",
        "사진풍": "photographic, photo-realistic",
        "플랫디자인": "flat design, minimalist",
        "모던 썸네일": "modern thumbnail design",
        "차트": "chart, graph",
        "다이어그램": "diagram, flowchart",
        "체크리스트": "checklist, list design",
        "비교표": "comparison table, comparison chart",
        "프로세스": "process diagram, step-by-step",
    }

    result = korean_format
    for kr, en in format_map.items():
        if kr in result:
            result = result.replace(kr, en)

    return result


def parse_image_guide_markdown(content: str) -> List[ImageGuideItem]:
    """
    Parse image guide markdown and return list of image items.

    Args:
        content: Image guide markdown content

    Returns:
        List of ImageGuideItem
    """
    items = []

    # Split image blocks (by ━ separator)
    blocks = re.split(r"━{20,}", content)

    for block in blocks:
        if not block.strip():
            continue

        item = _parse_image_block(block)
        if item:
            items.append(item)

    return items


def _parse_image_block(block: str) -> Optional[ImageGuideItem]:
    """Parse single image block"""
    lines = block.strip().split("\n")

    if not lines:
        return None

    # Extract image number and role from first line
    header_match = re.match(r"\[이미지\s*(\d+)\]\s*(.+)", lines[0])
    if not header_match:
        # Also handle [썸네일] format
        header_match = re.match(r"\[(\w+)\]\s*(.+)", lines[0])
        if not header_match:
            return None
        index = 0
        role = header_match.group(1) + " " + header_match.group(2)
    else:
        index = int(header_match.group(1))
        role = header_match.group(2)

    # Determine mode
    mode = "B"  # Default: AI generation
    if "📷" in block or "참고 이미지" in block or "다운로드된 이미지" in block:
        mode = "A"
    elif "🎨" in block or "AI 생성" in block or "생성 필요" in block:
        mode = "B"

    # Skip if not AI generation mode
    if mode != "B":
        return ImageGuideItem(
            index=index,
            role=role,
            mode=mode,
        )

    # Extract Korean description
    korean_desc = ""
    desc_match = re.search(r"\[한글 설명\]\s*\n(.+?)(?=\n\[|$)", block, re.DOTALL)
    if desc_match:
        korean_desc = desc_match.group(1).strip()

    # Extract AI generation prompt
    prompt = ""
    prompt_match = re.search(r"\[AI 생성 프롬프트\]\s*\n(.+?)(?=\n\[|$)", block, re.DOTALL)
    if prompt_match:
        prompt = prompt_match.group(1).strip()

    # Extract style guide
    style_guide = {}
    style_match = re.search(r"\[스타일 가이드\]\s*\n(.+?)(?=━|$)", block, re.DOTALL)
    if style_match:
        style_text = style_match.group(1)
        for line in style_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lstrip("-").strip()
                value = value.strip()
                if key and value:
                    style_guide[key] = value

    return ImageGuideItem(
        index=index,
        role=role,
        mode=mode,
        korean_description=korean_desc,
        prompt=prompt,
        style_guide=style_guide,
    )


def extract_gemini_prompts(
    image_guide_content: str,
    output_dir: str = "./images",
) -> List[GeminiPrompt]:
    """
    Extract Gemini prompts from image guide.

    Args:
        image_guide_content: Image guide markdown content
        output_dir: Image save directory

    Returns:
        List of GeminiPrompt (AI generation mode only)
    """
    # New format (v2): Markdown sections with fenced code blocks (``` ... ```)
    sections = split_image_sections(image_guide_content)
    if sections:
        prompts: List[GeminiPrompt] = []
        for section in sections:
            prompt = extract_first_prompt(section.body)
            if not prompt:
                continue

            filename = f"{section.index:02d}_{sanitize_filename(section.role)}.png"
            prompts.append(
                GeminiPrompt(
                    prompt=prompt,
                    filename=filename,
                    aspect_ratio="16:9",
                    style_hints="",
                )
            )
        return prompts

    # Legacy format (v1): "━" blocks with [한글 설명]/[AI 생성 프롬프트]/[스타일 가이드]
    items = parse_image_guide_markdown(image_guide_content)
    prompts = []

    for item in items:
        if item.mode != "B":
            continue

        if not item.prompt:
            continue

        # Generate Gemini optimized prompt
        optimized_prompt = convert_to_gemini_prompt({
            "korean_description": item.korean_description,
            "prompt": item.prompt,
            "style_guide": item.style_guide,
        })

        # Generate filename
        filename = f"{item.index:02d}_{sanitize_filename(item.role)}.png"

        # Extract ratio
        aspect_ratio = item.style_guide.get("비율", "16:9")

        prompts.append(GeminiPrompt(
            prompt=optimized_prompt,
            filename=filename,
            aspect_ratio=aspect_ratio,
            style_hints=", ".join(item.style_guide.values()) if item.style_guide else "",
        ))

    return prompts


def sanitize_filename(name: str) -> str:
    """Remove characters not allowed in filenames"""
    # Remove special characters
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    # Replace spaces with underscores
    name = re.sub(r"\s+", "_", name)
    # Truncate long names
    if len(name) > 50:
        name = name[:50]
    return name


def generate_image_prompts_for_batch(
    image_guide_content: str,
) -> List[Dict[str, str]]:
    """
    Generate prompt list for batch image generation.

    Args:
        image_guide_content: Image guide markdown content

    Returns:
        List in format [{"prompt": "...", "filename": "..."}, ...]
    """
    gemini_prompts = extract_gemini_prompts(image_guide_content)

    return [
        {
            "prompt": gp.prompt,
            "filename": gp.filename,
        }
        for gp in gemini_prompts
    ]


def get_prompt_for_thumbnail(
    title: str,
    keywords: List[str],
    color_scheme: str = "modern gradient",
    sub_text: str = "",
    background_only: bool = False,  # DEPRECATED - kept for backward compatibility
) -> Tuple[str, Optional[WatermarkConfig]]:
    """
    Generate thumbnail prompt with AI-rendered text.

    As of the new workflow, AI now renders text directly in the image.
    Only watermark is added via PIL overlay.

    Args:
        title: Blog title (rendered by AI)
        keywords: Keyword list
        color_scheme: Color scheme
        sub_text: Optional subtitle (rendered by AI)
        background_only: DEPRECATED - no longer used

    Returns:
        Tuple of (prompt_string, WatermarkConfig)
        - prompt includes text rendering instructions for AI
        - WatermarkConfig for adding watermark only
    """
    keywords_str = ", ".join(keywords[:3])

    # Build prompt with text instructions for AI
    text_instruction = f'bold Korean text "{title}" in upper third'
    if sub_text:
        text_instruction += f', subtitle "{sub_text}" in center'

    prompt = (
        f"Create a professional blog thumbnail image. "
        f"Topic: {keywords_str}. "
        f"{text_instruction}. "
        f"Use {color_scheme} color scheme. "
        f"Eye-catching, modern design, 16:9 aspect ratio. "
        f"High resolution, suitable for social media preview."
    )

    # Watermark config (only watermark, no text overlay)
    watermark_config = WatermarkConfig(
        watermark_text="@money-lab-brian",
        watermark_position="bottom-center",
        watermark_margin_bottom=60,
        watermark_font_size=18,
        watermark_font_color="rgba(255,255,255,0.6)",
        watermark_enabled=True,
    )

    return (prompt, watermark_config)


def get_prompt_for_infographic(
    title: str,
    data_points: List[str],
    chart_type: str = "bar chart",
) -> str:
    """
    Generate infographic prompt.

    Args:
        title: Infographic title
        data_points: Data point list
        chart_type: Chart type

    Returns:
        Infographic prompt
    """
    data_str = ", ".join(data_points[:5])

    return (
        f"Create a clean, professional infographic. "
        f"Title: {title}. "
        f"Visualize data as {chart_type}: {data_str}. "
        f"Use flat design, minimal style. "
        f"White background, clear data labels. "
        f"16:9 aspect ratio, high resolution."
    )


def get_prompt_for_process(
    title: str,
    steps: List[str],
) -> str:
    """
    Generate process diagram prompt.

    Args:
        title: Process title
        steps: Step list

    Returns:
        Process diagram prompt
    """
    steps_str = " → ".join([f"Step {i+1}: {s}" for i, s in enumerate(steps[:5])])

    return (
        f"Create a step-by-step process diagram. "
        f"Title: {title}. "
        f"Show {len(steps)} steps in horizontal flow: {steps_str}. "
        f"Use numbered circles, connected by arrows. "
        f"Clean, minimal style with icons for each step. "
        f"16:9 aspect ratio, professional look."
    )


def extract_watermark_config(content: str) -> Optional[WatermarkConfig]:
    """
    Extract WatermarkConfig from markdown section content.

    Looks for patterns like:
    - watermark_text: "@money-lab-brian"
    - watermark_position: "bottom-center"
    - watermark_margin_bottom: 60
    - watermark_font_size: 18
    - watermark_font_color: "rgba(255,255,255,0.6)"
    - watermark_enabled: true

    Args:
        content: Markdown section content

    Returns:
        WatermarkConfig if watermark settings found, else None
    """
    config_kwargs = {}

    # Extract watermark_text
    text_match = re.search(
        r"watermark_text[:\s]*[\"'](.+?)[\"']",
        content,
        re.IGNORECASE
    )
    if text_match:
        config_kwargs["watermark_text"] = text_match.group(1)

    # Extract watermark_position
    position_match = re.search(
        r"watermark_position[:\s]*[\"'](.+?)[\"']",
        content,
        re.IGNORECASE
    )
    if position_match:
        config_kwargs["watermark_position"] = position_match.group(1)

    # Extract watermark_margin_bottom
    margin_match = re.search(
        r"watermark_margin_bottom[:\s]*(\d+)",
        content,
        re.IGNORECASE
    )
    if margin_match:
        config_kwargs["watermark_margin_bottom"] = int(margin_match.group(1))

    # Extract watermark_font_size
    font_size_match = re.search(
        r"watermark_font_size[:\s]*(\d+)",
        content,
        re.IGNORECASE
    )
    if font_size_match:
        config_kwargs["watermark_font_size"] = int(font_size_match.group(1))

    # Extract watermark_font_color
    color_match = re.search(
        r"watermark_font_color[:\s]*[\"'](.+?)[\"']",
        content,
        re.IGNORECASE
    )
    if color_match:
        config_kwargs["watermark_font_color"] = color_match.group(1)

    # Extract watermark_enabled
    enabled_match = re.search(
        r"watermark_enabled[:\s]*(true|false)",
        content,
        re.IGNORECASE
    )
    if enabled_match:
        config_kwargs["watermark_enabled"] = enabled_match.group(1).lower() == "true"

    # Return config if any watermark settings found, otherwise return default
    if config_kwargs:
        return WatermarkConfig(**config_kwargs)

    # Return default watermark config if [Watermark Config] section exists
    if "[Watermark Config]" in content or "[watermark config]" in content.lower():
        return WatermarkConfig()

    return None
