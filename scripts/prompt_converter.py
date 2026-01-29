"""
Prompt conversion module

Converts image guide prompts to Gemini API optimized format.
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from .config import get_config, get_config_value


@dataclass
class TextOverlayConfig:
    """Data class for text overlay configuration"""

    main_text: str = ""
    sub_text: str = ""
    position: str = "center"  # "center", "top", "bottom", "top-left", "top-right", "bottom-left", "bottom-right"
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
class ImageGuideItem:
    """Data class for image guide items"""

    index: int
    role: str
    mode: str  # "A" (reference), "B" (AI generation), "C" (SVG)
    korean_description: str = ""
    prompt: str = ""
    style_guide: Dict[str, str] = None
    filename: str = ""
    text_overlay: TextOverlayConfig = None  # New field for text overlay config

    def __post_init__(self):
        if self.style_guide is None:
            self.style_guide = {}
        if self.text_overlay is None:
            self.text_overlay = TextOverlayConfig()


@dataclass
class GeminiPrompt:
    """Data class for Gemini prompts"""

    prompt: str
    filename: str
    aspect_ratio: str = "16:9"
    style_hints: str = ""


def strip_text_instructions(prompt: str) -> str:
    """
    Remove text-related instructions from prompt for background-only generation.

    Args:
        prompt: Original prompt string

    Returns:
        Prompt with text instructions removed

    Example:
        >>> strip_text_instructions('Blog thumbnail with "Hello World" text overlay')
        'Blog thumbnail'
    """
    # Patterns to remove
    text_patterns = [
        # Text overlay patterns
        r'[,\s]*(?:include|with|add)?[,\s]*(?:bold|large|big|small)?[,\s]*(?:Korean|English|Chinese)?[,\s]*text\s*overlay[:\s]*["\'][^"\']*["\']',
        r'[,\s]*(?:bold|large|big)?[,\s]*["\'][^"\']*["\'][,\s]*(?:Korean|English)?\s*text\s*overlay',
        r'[,\s]*text\s*overlay[:\s]*["\'][^"\']*["\']',
        r'[,\s]*["\'][^"\']*["\'][,\s]*text',
        # Text-related keywords
        r'[,\s]*include\s+(?:bold\s+)?(?:Korean\s+)?text[^,\.]*',
        r'[,\s]*(?:bold|large)\s+(?:Korean\s+)?text[^,\.]*',
        r'[,\s]*Korean\s+text[^,\.]*',
        r'[,\s]*text\s+saying[^,\.]*',
        r'[,\s]*with\s+text[^,\.]*',
        r'[,\s]*text\s+reading[^,\.]*',
        # Typography patterns
        r'[,\s]*typography[^,\.]*',
        r'[,\s]*lettering[^,\.]*',
        r'[,\s]*title\s+text[^,\.]*',
        r'[,\s]*headline[^,\.]*',
    ]

    result = prompt
    for pattern in text_patterns:
        result = re.sub(pattern, '', result, flags=re.IGNORECASE)

    # Clean up multiple commas and spaces
    result = re.sub(r',\s*,', ',', result)
    result = re.sub(r'\s+', ' ', result)
    result = re.sub(r',\s*$', '', result)
    result = re.sub(r'^\s*,', '', result)
    result = result.strip()

    return result


def extract_text_config(prompt: str, korean_desc: str = "") -> TextOverlayConfig:
    """
    Extract text overlay configuration from prompt and Korean description.

    Args:
        prompt: Original English prompt
        korean_desc: Korean description

    Returns:
        TextOverlayConfig with extracted text information
    """
    config = TextOverlayConfig()

    # Extract quoted text from prompt
    quoted_texts = re.findall(r'["\']([^"\']+)["\']', prompt)

    # Extract Korean text from Korean description
    korean_quoted = re.findall(r'["\']([^"\']+)["\']', korean_desc)

    # Prioritize Korean quoted text for main_text
    if korean_quoted:
        config.main_text = korean_quoted[0]
        if len(korean_quoted) > 1:
            config.sub_text = korean_quoted[1]
    elif quoted_texts:
        # Use English quoted text as fallback
        config.main_text = quoted_texts[0]
        if len(quoted_texts) > 1:
            config.sub_text = quoted_texts[1]

    # Detect position hints
    position_hints = {
        'center': ['center', '중앙', '가운데'],
        'top': ['top', '상단', '위'],
        'bottom': ['bottom', '하단', '아래'],
        'top-left': ['top-left', '좌상단'],
        'top-right': ['top-right', '우상단'],
        'bottom-left': ['bottom-left', '좌하단'],
        'bottom-right': ['bottom-right', '우하단'],
    }

    combined_text = f"{prompt} {korean_desc}".lower()
    for position, keywords in position_hints.items():
        if any(kw in combined_text for kw in keywords):
            config.position = position
            break

    # Detect font size hints
    if 'bold' in combined_text or '굵은' in korean_desc:
        config.font_size = 48
    if 'large' in combined_text or '큰' in korean_desc:
        config.font_size = 56
    if 'small' in combined_text or '작은' in korean_desc:
        config.font_size = 32

    # Detect shadow preference
    if 'no shadow' in combined_text or '그림자 없' in korean_desc:
        config.shadow = False

    return config


def convert_to_gemini_prompt(
    image_guide: Dict[str, Any],
    background_only: bool = False,
) -> str:
    """
    Convert image guide prompt to Gemini optimized format.

    Args:
        image_guide: Image guide dictionary
            - korean_description: Korean description
            - prompt: English prompt
            - style_guide: Style guide (colors, mood, format, ratio)
        background_only: If True, removes text-related instructions for background generation

    Returns:
        Optimized prompt string for Gemini API

    Example:
        >>> guide = {
        ...     "korean_description": "아기 손과 돼지저금통 썸네일",
        ...     "prompt": "Blog thumbnail, baby savings concept...",
        ...     "style_guide": {"색상": "따뜻한 노랑", "분위기": "친근한"}
        ... }
        >>> convert_to_gemini_prompt(guide)
        "Create a high-quality blog thumbnail image. ..."
        >>> convert_to_gemini_prompt(guide, background_only=True)
        "Create a high-quality blog background image. ..."  # No text instructions
    """
    korean_desc = image_guide.get("korean_description", "")
    original_prompt = image_guide.get("prompt", "")
    style_guide = image_guide.get("style_guide", {})

    # Prompt components
    parts = []

    # 1. Base instruction (modified for background_only mode)
    if background_only:
        parts.append("Create a high-quality background image for a Korean blog. No text, no letters, no typography, no words.")
    else:
        parts.append("Create a high-quality image for a Korean blog.")

    # 2. English prompt (use existing prompt)
    if original_prompt:
        # Remove ratio information (handled separately)
        cleaned_prompt = re.sub(r"\d+:\d+\s*ratio", "", original_prompt)

        # Remove text instructions if background_only mode
        if background_only:
            cleaned_prompt = strip_text_instructions(cleaned_prompt)

        parts.append(cleaned_prompt.strip())

    # 3. Convert style guide
    style_parts = []

    color = _get_style_value(style_guide, "색상", "Color", "Colors")
    if color:
        color_en = translate_color(color)
        style_parts.append(f"Color scheme: {color_en}")

    mood = _get_style_value(style_guide, "분위기", "Mood")
    if mood:
        mood_en = translate_mood(mood)
        style_parts.append(f"Mood: {mood_en}")

    format_type = _get_style_value(style_guide, "형식", "Format", "Style")
    if format_type:
        format_en = translate_format(format_type)
        style_parts.append(f"Style: {format_en}")

    if style_parts:
        parts.append(" ".join(style_parts))

    # 4. Quality assurance phrase (modified for background_only mode)
    if background_only:
        parts.append("High resolution, professional quality, clean background without any text or typography, suitable for text overlay later.")
    else:
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
    # Prefer the canonical heading format used by templates/writer:
    #   ## [Image 1] Role
    if re.search(r"^##\s*\[Image\s*\d+\]", content, flags=re.MULTILINE | re.IGNORECASE):
        return _parse_image_guide_heading_format(content)

    # Legacy format: blocks separated by ━━━━━━━━━ and headers like "[이미지 N]" or "[Image N]"
    return _parse_image_guide_legacy_blocks(content)


def _parse_image_guide_legacy_blocks(content: str) -> List[ImageGuideItem]:
    items: List[ImageGuideItem] = []

    blocks = re.split(r"━{20,}", content)
    for block in blocks:
        if not block.strip():
            continue
        item = _parse_image_block(block)
        if item:
            items.append(item)
    return items


def _parse_image_guide_heading_format(content: str) -> List[ImageGuideItem]:
    items: List[ImageGuideItem] = []

    pattern = re.compile(
        r"^##\s*\[Image\s*(\d+)\]\s*(.+?)\s*$",
        flags=re.MULTILINE | re.IGNORECASE,
    )
    matches = list(pattern.finditer(content))
    if not matches:
        return items

    for idx, match in enumerate(matches):
        index = int(match.group(1))
        role = match.group(2).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        section = content[start:end]

        item = _parse_image_heading_section(index=index, role=role, section=section)
        if item:
            items.append(item)

    return items


def _parse_image_heading_section(index: int, role: str, section: str) -> Optional[ImageGuideItem]:
    # Determine modes present in the section
    has_ai = "🎨" in section or re.search(r"AI\s+Generation", section, re.IGNORECASE)
    has_svg = "🔷" in section or re.search(r"SVG\s+Generation", section, re.IGNORECASE)
    has_ref = "📷" in section or re.search(r"Reference\s+Image", section, re.IGNORECASE)

    # Default mode semantics:
    # - Prefer AI when a prompt exists
    # - Else SVG when svg guide exists
    # - Else reference
    mode = "B" if has_ai else ("C" if has_svg else ("A" if has_ref else "B"))

    korean_desc = ""
    desc_match = re.search(
        r"\*\*Korean\s+Description:\*\*\s*\n(.*?)(?=\n\*\*|\n###|\n##|\Z)",
        section,
        re.DOTALL | re.IGNORECASE,
    )
    if desc_match:
        korean_desc = desc_match.group(1).strip()

    prompt = ""
    prompt_match = re.search(
        r"AI\s+Generation\s+Prompt.*?\n\s*```(?:\w+)?\s*\n(.*?)\n\s*```",
        section,
        re.DOTALL | re.IGNORECASE,
    )
    if prompt_match:
        prompt = prompt_match.group(1).strip()

    # Style guide (bullet list under "**Style:**" or "**Style Guide:**")
    style_guide: Dict[str, str] = {}
    style_match = re.search(
        r"\*\*(?:Style\s+Guide|Style):\*\*\s*\n(.*?)(?=\n###|\n##|\Z)",
        section,
        re.DOTALL | re.IGNORECASE,
    )
    if style_match:
        style_text = style_match.group(1)
        for line in style_text.split("\n"):
            line = line.strip()
            if not line.startswith("-"):
                continue
            line = line.lstrip("-").strip()
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key and value:
                style_guide[key] = value

    # Text overlay config (optional) - keep as best-effort only
    overlay = TextOverlayConfig()
    overlay_match = re.search(r"main_text[:\s]*[\"'](.+?)[\"']", section, re.IGNORECASE)
    if overlay_match:
        overlay.main_text = overlay_match.group(1)
        sub_match = re.search(r"sub_text[:\s]*[\"'](.+?)[\"']", section, re.IGNORECASE)
        if sub_match:
            overlay.sub_text = sub_match.group(1)
        pos_match = re.search(r"position[:\s]*[\"'](.+?)[\"']", section, re.IGNORECASE)
        if pos_match:
            overlay.position = pos_match.group(1)
        size_match = re.search(r"font_size[:\s]*(\d+)", section, re.IGNORECASE)
        if size_match:
            overlay.font_size = int(size_match.group(1))
        color_match = re.search(r"font_color[:\s]*[\"'](.+?)[\"']", section, re.IGNORECASE)
        if color_match:
            overlay.font_color = color_match.group(1)
        shadow_match = re.search(r"shadow[:\s]*(true|false)", section, re.IGNORECASE)
        if shadow_match:
            overlay.shadow = shadow_match.group(1).lower() == "true"
        bg_box_match = re.search(r"background_box[:\s]*(true|false)", section, re.IGNORECASE)
        if bg_box_match:
            overlay.background_box = bg_box_match.group(1).lower() == "true"
        bg_box_color_match = re.search(r"background_box_color[:\s]*[\"'](.+?)[\"']", section, re.IGNORECASE)
        if bg_box_color_match:
            overlay.background_box_color = bg_box_color_match.group(1)

    return ImageGuideItem(
        index=index,
        role=role,
        mode=mode,
        korean_description=korean_desc,
        prompt=prompt,
        style_guide=style_guide,
        text_overlay=overlay,
    )


def _parse_image_block(block: str) -> Optional[ImageGuideItem]:
    """Parse single image block"""
    lines = block.strip().split("\n")

    if not lines:
        return None

    # Extract image number and role from first line (legacy format)
    header_match = re.match(r"\[(?:이미지|Image)\s*(\d+)\]\s*(.+)", lines[0], flags=re.IGNORECASE)
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
    elif "🔷" in block or "SVG 생성" in block:
        mode = "C"
    elif "🎨" in block or "AI 생성" in block or "생성 필요" in block:
        mode = "B"

    # Skip if not AI generation mode
    if mode != "B":
        return ImageGuideItem(
            index=index,
            role=role,
            mode=mode,
        )

    # Extract Korean description (legacy label style)
    korean_desc = ""
    desc_match = re.search(r"\[(?:한글\s*설명|Korean\s*Description)\]\s*\n(.+?)(?=\n\[|$)", block, re.DOTALL | re.IGNORECASE)
    if desc_match:
        korean_desc = desc_match.group(1).strip()

    # Extract AI generation prompt (legacy label style)
    prompt = ""
    prompt_match = re.search(r"\[(?:AI\s*생성\s*프롬프트|AI\s*Generation\s*Prompt)\]\s*\n(.+?)(?=\n\[|$)", block, re.DOTALL | re.IGNORECASE)
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

        # Extract ratio (Korean/English key support)
        aspect_ratio = _get_style_value(item.style_guide, "비율", "Ratio") or "16:9"

        prompts.append(GeminiPrompt(
            prompt=optimized_prompt,
            filename=filename,
            aspect_ratio=aspect_ratio,
            style_hints=", ".join(item.style_guide.values()) if item.style_guide else "",
        ))

    return prompts


def _get_style_value(style_guide: Dict[str, str], *keys: str) -> Optional[str]:
    if not style_guide:
        return None
    for key in keys:
        if key in style_guide:
            return style_guide[key]
        lowered_key = key.lower()
        for k, v in style_guide.items():
            if isinstance(k, str) and k.lower() == lowered_key:
                return v
    return None


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
    background_only: bool = False,
) -> Tuple[str, Optional[TextOverlayConfig]]:
    """
    Generate thumbnail prompt.

    Args:
        title: Blog title
        keywords: Keyword list
        color_scheme: Color scheme
        background_only: If True, generates background-only prompt without text

    Returns:
        Tuple of (prompt_string, TextOverlayConfig or None)
        - If background_only=False: (full_prompt, None)
        - If background_only=True: (background_prompt, TextOverlayConfig)
    """
    keywords_str = ", ".join(keywords[:3])

    if background_only:
        # Background-only prompt without text instructions
        prompt = (
            f"Create a professional blog thumbnail background image. "
            f"Topic: {keywords_str}. "
            f"Use {color_scheme} color scheme. "
            f"Eye-catching, modern design, 16:9 aspect ratio. "
            f"Clean background suitable for text overlay. "
            f"No text, no letters, no typography, no words. "
            f"High resolution, professional quality."
        )

        # Create text overlay config
        text_config = TextOverlayConfig(
            main_text=title,
            sub_text="",
            position="center",
            font_size=48,
            font_color="#FFFFFF",
            shadow=True,
        )

        return (prompt, text_config)
    else:
        # Original behavior with text included
        prompt = (
            f"Create a professional blog thumbnail image. "
            f"Topic: {keywords_str}. "
            f"Include bold Korean text overlay: \"{title}\". "
            f"Use {color_scheme} color scheme. "
            f"Eye-catching, modern design, 16:9 aspect ratio. "
            f"High resolution, suitable for social media preview."
        )
        return (prompt, None)


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
