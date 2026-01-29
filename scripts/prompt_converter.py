"""
프롬프트 변환 모듈

이미지 가이드의 프롬프트를 Gemini API에 최적화된 형식으로 변환합니다.
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .config import get_config, get_config_value


@dataclass
class ImageGuideItem:
    """이미지 가이드 항목을 담는 데이터 클래스"""

    index: int
    role: str
    mode: str  # "A" (참고), "B" (AI 생성), "C" (SVG)
    korean_description: str = ""
    prompt: str = ""
    style_guide: Dict[str, str] = None
    filename: str = ""

    def __post_init__(self):
        if self.style_guide is None:
            self.style_guide = {}


@dataclass
class GeminiPrompt:
    """Gemini용 프롬프트를 담는 데이터 클래스"""

    prompt: str
    filename: str
    aspect_ratio: str = "16:9"
    style_hints: str = ""


def convert_to_gemini_prompt(image_guide: Dict[str, Any]) -> str:
    """
    이미지 가이드의 프롬프트를 Gemini 최적화 포맷으로 변환합니다

    Args:
        image_guide: 이미지 가이드 딕셔너리
            - korean_description: 한글 설명
            - prompt: 영문 프롬프트
            - style_guide: 스타일 가이드 (색상, 분위기, 형식, 비율)

    Returns:
        Gemini API용 최적화된 프롬프트 문자열

    Example:
        >>> guide = {
        ...     "korean_description": "아기 손과 돼지저금통 썸네일",
        ...     "prompt": "Blog thumbnail, baby savings concept...",
        ...     "style_guide": {"색상": "따뜻한 노랑", "분위기": "친근한"}
        ... }
        >>> convert_to_gemini_prompt(guide)
        "Create a high-quality blog thumbnail image. ..."
    """
    korean_desc = image_guide.get("korean_description", "")
    original_prompt = image_guide.get("prompt", "")
    style_guide = image_guide.get("style_guide", {})

    # 프롬프트 구성 요소
    parts = []

    # 1. 기본 지시문
    parts.append("Create a high-quality image for a Korean blog.")

    # 2. 영문 프롬프트 (기존 프롬프트 활용)
    if original_prompt:
        # 비율 정보 제거 (별도 처리)
        cleaned_prompt = re.sub(r"\d+:\d+\s*ratio", "", original_prompt)
        parts.append(cleaned_prompt.strip())

    # 3. 스타일 가이드 변환
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

    # 4. 품질 보장 문구
    parts.append("High resolution, professional quality, suitable for blog use.")

    return " ".join(parts)


def translate_color(korean_color: str) -> str:
    """한글 색상 설명을 영문으로 변환합니다"""
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
    """한글 분위기 설명을 영문으로 변환합니다"""
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
    """한글 형식 설명을 영문으로 변환합니다"""
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
    이미지 가이드 마크다운을 파싱하여 이미지 항목 목록을 반환합니다

    Args:
        content: 이미지 가이드 마크다운 내용

    Returns:
        ImageGuideItem 목록
    """
    items = []

    # 이미지 블록 분리 (━ 구분선 기준)
    blocks = re.split(r"━{20,}", content)

    for block in blocks:
        if not block.strip():
            continue

        item = _parse_image_block(block)
        if item:
            items.append(item)

    return items


def _parse_image_block(block: str) -> Optional[ImageGuideItem]:
    """단일 이미지 블록을 파싱합니다"""
    lines = block.strip().split("\n")

    if not lines:
        return None

    # 첫 줄에서 이미지 번호와 역할 추출
    header_match = re.match(r"\[이미지\s*(\d+)\]\s*(.+)", lines[0])
    if not header_match:
        # [썸네일] 형식도 처리
        header_match = re.match(r"\[(\w+)\]\s*(.+)", lines[0])
        if not header_match:
            return None
        index = 0
        role = header_match.group(1) + " " + header_match.group(2)
    else:
        index = int(header_match.group(1))
        role = header_match.group(2)

    # 모드 결정
    mode = "B"  # 기본값: AI 생성
    if "📷" in block or "참고 이미지" in block or "다운로드된 이미지" in block:
        mode = "A"
    elif "🔷" in block or "SVG 생성" in block:
        mode = "C"
    elif "🎨" in block or "AI 생성" in block or "생성 필요" in block:
        mode = "B"

    # AI 생성 모드가 아니면 건너뛰기
    if mode != "B":
        return ImageGuideItem(
            index=index,
            role=role,
            mode=mode,
        )

    # 한글 설명 추출
    korean_desc = ""
    desc_match = re.search(r"\[한글 설명\]\s*\n(.+?)(?=\n\[|$)", block, re.DOTALL)
    if desc_match:
        korean_desc = desc_match.group(1).strip()

    # AI 생성 프롬프트 추출
    prompt = ""
    prompt_match = re.search(r"\[AI 생성 프롬프트\]\s*\n(.+?)(?=\n\[|$)", block, re.DOTALL)
    if prompt_match:
        prompt = prompt_match.group(1).strip()

    # 스타일 가이드 추출
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
    이미지 가이드에서 Gemini 프롬프트를 추출합니다

    Args:
        image_guide_content: 이미지 가이드 마크다운 내용
        output_dir: 이미지 저장 디렉토리

    Returns:
        GeminiPrompt 목록 (AI 생성 모드만 포함)
    """
    items = parse_image_guide_markdown(image_guide_content)
    prompts = []

    for item in items:
        if item.mode != "B":
            continue

        if not item.prompt:
            continue

        # Gemini 최적화 프롬프트 생성
        optimized_prompt = convert_to_gemini_prompt({
            "korean_description": item.korean_description,
            "prompt": item.prompt,
            "style_guide": item.style_guide,
        })

        # 파일명 생성
        filename = f"{item.index:02d}_{sanitize_filename(item.role)}.png"

        # 비율 추출
        aspect_ratio = item.style_guide.get("비율", "16:9")

        prompts.append(GeminiPrompt(
            prompt=optimized_prompt,
            filename=filename,
            aspect_ratio=aspect_ratio,
            style_hints=", ".join(item.style_guide.values()) if item.style_guide else "",
        ))

    return prompts


def sanitize_filename(name: str) -> str:
    """파일명에 사용할 수 없는 문자를 제거합니다"""
    # 특수문자 제거
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    # 공백을 언더스코어로
    name = re.sub(r"\s+", "_", name)
    # 너무 긴 이름 자르기
    if len(name) > 50:
        name = name[:50]
    return name


def generate_image_prompts_for_batch(
    image_guide_content: str,
) -> List[Dict[str, str]]:
    """
    배치 이미지 생성을 위한 프롬프트 목록을 생성합니다

    Args:
        image_guide_content: 이미지 가이드 마크다운 내용

    Returns:
        [{"prompt": "...", "filename": "..."}, ...] 형식의 목록
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
) -> str:
    """
    썸네일용 프롬프트를 생성합니다

    Args:
        title: 블로그 제목
        keywords: 키워드 목록
        color_scheme: 색상 스키마

    Returns:
        썸네일용 프롬프트
    """
    keywords_str = ", ".join(keywords[:3])

    return (
        f"Create a professional blog thumbnail image. "
        f"Topic: {keywords_str}. "
        f"Include bold Korean text overlay: \"{title}\". "
        f"Use {color_scheme} color scheme. "
        f"Eye-catching, modern design, 16:9 aspect ratio. "
        f"High resolution, suitable for social media preview."
    )


def get_prompt_for_infographic(
    title: str,
    data_points: List[str],
    chart_type: str = "bar chart",
) -> str:
    """
    인포그래픽용 프롬프트를 생성합니다

    Args:
        title: 인포그래픽 제목
        data_points: 데이터 포인트 목록
        chart_type: 차트 유형

    Returns:
        인포그래픽용 프롬프트
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
    프로세스 다이어그램용 프롬프트를 생성합니다

    Args:
        title: 프로세스 제목
        steps: 단계 목록

    Returns:
        프로세스 다이어그램용 프롬프트
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
