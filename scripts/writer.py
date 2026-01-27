"""
HTML/MD 생성 모듈

Jinja2 스타일 템플릿을 렌더링하여 본문.html, 이미지 가이드.md, 참조.md를 생성합니다.
"""

import re
from datetime import datetime
from pathlib import Path
from string import Template
from typing import Dict, List, Optional, Any

from .config import get_config, get_config_value
from .utils import get_today_date, clean_text
from .validator import validate_char_count, ValidationResult
from .setup import update_metadata


def load_template(template_name: str, templates_dir: Optional[Path] = None) -> str:
    """
    템플릿 파일을 로드합니다.

    Args:
        template_name: 템플릿 파일명
        templates_dir: 템플릿 디렉토리 (없으면 기본 경로)

    Returns:
        템플릿 내용
    """
    if templates_dir is None:
        # 현재 스크립트 위치 기준으로 templates 디렉토리 찾기
        script_dir = Path(__file__).parent
        templates_dir = script_dir.parent / "templates"

    template_path = templates_dir / template_name

    if not template_path.exists():
        raise FileNotFoundError(f"템플릿을 찾을 수 없습니다: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def render_template(template_content: str, context: Dict[str, Any]) -> str:
    """
    간단한 템플릿 렌더링 (Python string.Template 사용).

    지원 문법:
    - ${variable} 또는 $variable: 변수 치환
    - 반복문은 지원하지 않음 (별도 처리 필요)

    Args:
        template_content: 템플릿 내용
        context: 컨텍스트 변수들

    Returns:
        렌더링된 내용
    """
    # 기본 치환
    template = Template(template_content)

    # safe_substitute를 사용하여 없는 변수는 그대로 유지
    result = template.safe_substitute(context)

    return result


def generate_html_content(
    title: str,
    sections: List[Dict[str, Any]],
    tags: List[str],
    config: Optional[Dict] = None
) -> str:
    """
    HTML 본문을 생성합니다.

    Args:
        title: 제목
        sections: 섹션 리스트 [{"title": str, "content": str, "has_image": bool}]
        tags: 태그 리스트
        config: 설정 딕셔너리

    Returns:
        HTML 콘텐츠
    """
    if config is None:
        config = get_config()

    # HTML 템플릿 시작
    html_parts = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '  <meta charset="UTF-8">',
        '  <style>',
        '    body { font-family: "Noto Sans KR", sans-serif; line-height: 1.8; max-width: 700px; margin: 0 auto; padding: 20px; }',
        '    h1 { font-size: 28px; font-weight: bold; margin-bottom: 20px; }',
        '    h2 { font-size: 24px; font-weight: bold; margin: 32px 0 16px; }',
        '    h3 { font-size: 18px; font-weight: bold; margin: 24px 0 12px; }',
        '    p { font-size: 16px; margin: 12px 0; }',
        '    blockquote { border-left: 4px solid #4A90D9; padding-left: 16px; color: #555; margin: 16px 0; }',
        '    .highlight-quote { background: #f0f7ff; padding: 16px; border-radius: 8px; border-left: none; }',
        '    hr { border: none; border-top: 1px solid #ddd; margin: 24px 0; }',
        '    .thick-hr { border-top: 3px solid #333; }',
        '    table { border-collapse: collapse; width: 100%; margin: 16px 0; }',
        '    th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }',
        '    th { background: #f5f5f5; font-weight: bold; }',
        '    .cta { font-size: 24px; font-weight: bold; text-align: center; margin: 32px 0; color: #4A90D9; }',
        '    .small { font-size: 12px; color: #888; }',
        '    .image-placeholder { color: #999; text-align: center; padding: 40px; background: #f9f9f9; margin: 16px 0; }',
        '    .tags { color: #4A90D9; margin-top: 32px; }',
        '  </style>',
        '</head>',
        '<body>',
        '',
        f'<h1>{title}</h1>',
        '',
        '<div class="image-placeholder">[이미지 1 삽입 - 썸네일]</div>',
        '',
        '<hr>',
    ]

    # 섹션별 콘텐츠 추가
    image_index = 2
    for section in sections:
        section_title = section.get("title", "")
        section_content = section.get("content", "")
        has_image = section.get("has_image", False)
        section_type = section.get("type", "normal")

        # 섹션 제목
        if section_title:
            html_parts.append(f'\n<h2>{section_title}</h2>\n')

        # 섹션 내용
        if section_content:
            # 내용을 단락으로 분리
            paragraphs = section_content.split('\n\n')
            for para in paragraphs:
                para = para.strip()
                if para:
                    # 인용구 처리
                    if para.startswith('"') and para.endswith('"'):
                        html_parts.append(f'<blockquote>\n{para}\n</blockquote>\n')
                    else:
                        html_parts.append(f'<p>{para}</p>\n')

        # 이미지 placeholder
        if has_image:
            html_parts.append(f'\n<div class="image-placeholder">[이미지 {image_index} 삽입]</div>\n')
            image_index += 1

        html_parts.append('\n<hr>\n')

    # 태그 추가
    tags_str = ' '.join(f'#{tag}' for tag in tags)
    html_parts.extend([
        f'\n<p class="tags">{tags_str}</p>',
        '',
        '</body>',
        '</html>',
    ])

    return '\n'.join(html_parts)


def generate_image_guide(
    topic: str,
    images: List[Dict[str, Any]],
    color_palette: Dict[str, str],
    date: Optional[str] = None
) -> str:
    """
    이미지 가이드 마크다운을 생성합니다.

    Args:
        topic: 주제
        images: 이미지 가이드 리스트
        color_palette: 색상 팔레트
        date: 날짜

    Returns:
        마크다운 콘텐츠
    """
    if date is None:
        date = get_today_date()

    md_parts = [
        '# 이미지 가이드',
        '',
        '## 기본 정보',
        f'- 주제: {topic}',
        f'- 작성일: {date}',
        f'- 총 이미지 수: {len(images)}개',
        '',
        '## 색상 팔레트',
        f'- 메인: {color_palette.get("main", "#1a365d")}',
        f'- 포인트: {color_palette.get("accent", "#d69e2e")}',
        f'- 배경: {color_palette.get("background", "#ffffff")}',
        f'- 텍스트: {color_palette.get("text", "#333333")}',
        '',
        '---',
        '',
    ]

    for idx, img in enumerate(images, 1):
        role = img.get("role", f"이미지 {idx}")
        mode = img.get("mode", "ai_generate")

        md_parts.append(f'## [이미지 {idx}] {role}')
        md_parts.append('')

        if mode == "reference":
            # 참고 이미지 모드
            md_parts.extend([
                '### 📷 참고 이미지',
                f'**파일:** {img.get("filename", "N/A")}',
                f'**출처:** {img.get("source_url", "N/A")}',
                f'**활용:** {img.get("usage", "직접 사용 / 레이아웃 참고")}',
                '',
            ])

        if mode in ("ai_generate", "both"):
            # AI 이미지 생성 프롬프트
            md_parts.extend([
                '### 🎨 AI 생성 프롬프트',
                '',
                '**한글 설명:**',
                img.get("description_kr", "이미지 설명을 입력하세요."),
                '',
                '**AI 생성 프롬프트:**',
                '```',
                img.get("prompt_en", "Image generation prompt here"),
                '```',
                '',
                '**스타일:**',
                f'- 색상: {img.get("colors", color_palette.get("main"))}',
                f'- 분위기: {img.get("mood", "전문적")}',
                f'- 형식: {img.get("format", "인포그래픽")}',
                '',
            ])

        if mode in ("svg", "both"):
            # SVG 생성 가이드
            md_parts.extend([
                '### 🔷 SVG 생성 가이드',
                '',
                f'**캔버스:** {img.get("canvas_width", 800)}x{img.get("canvas_height", 450)}px',
                f'**배경:** {img.get("background", color_palette.get("background", "#ffffff"))}',
                '',
                '**요소:**',
            ])

            elements = img.get("svg_elements", [])
            for i, elem in enumerate(elements, 1):
                md_parts.append(f'{i}. {elem}')

            md_parts.append('')

        md_parts.extend([
            '---',
            '',
        ])

    return '\n'.join(md_parts)


def generate_references(
    topic: str,
    text_sources: Dict[str, List[Dict[str, str]]],
    images: List[Dict[str, Any]],
    date: Optional[str] = None
) -> str:
    """
    참조 문서 마크다운을 생성합니다.

    Args:
        topic: 주제
        text_sources: 텍스트 자료 {"네이버 뉴스": [...], "네이버 블로그": [...]}
        images: 이미지 정보 리스트
        date: 날짜

    Returns:
        마크다운 콘텐츠
    """
    if date is None:
        date = get_today_date()

    md_parts = [
        '# 참조 자료',
        '',
        '## 작성일',
        date,
        '',
        '## 주제',
        topic,
        '',
        '---',
        '',
        '## 텍스트 자료',
        '',
    ]

    total_sources = 0

    for source_name, sources in text_sources.items():
        if sources:
            md_parts.append(f'### {source_name}')

            for idx, source in enumerate(sources, 1):
                title = source.get("title", "제목 없음")
                url = source.get("url", "#")
                summary = source.get("summary", "")

                md_parts.append(f'{idx}. [{title}]({url})')
                if summary:
                    md_parts.append(f'   - 요약: {summary}')

                total_sources += 1

            md_parts.append('')

    md_parts.extend([
        '---',
        '',
        '## 다운로드된 이미지',
        '',
        '저장 위치: `./images/`',
        '',
        '| # | 파일명 | 설명 | 출처 |',
        '|---|--------|------|------|',
    ])

    downloaded_count = 0
    failed_images = []

    for idx, img in enumerate(images, 1):
        if img.get("downloaded", False):
            filename = img.get("filename", "N/A")
            description = img.get("description", "")
            source_name = img.get("source_name", "")
            source_url = img.get("source_url", "#")

            md_parts.append(f'| {idx} | {filename} | {description} | [{source_name}]({source_url}) |')
            downloaded_count += 1
        else:
            failed_images.append(img)

    md_parts.append('')

    if failed_images:
        md_parts.extend([
            '### 다운로드 실패 (URL만 기록)',
            '',
            '| # | 설명 | 이미지 URL | 실패 사유 |',
            '|---|------|-----------|----------|',
        ])

        for idx, img in enumerate(failed_images, 1):
            description = img.get("description", "")
            url = img.get("url", "")[:50] + "..."
            error = img.get("error", "알 수 없음")

            md_parts.append(f'| {idx} | {description} | {url} | {error} |')

        md_parts.append('')

    md_parts.extend([
        '---',
        '',
        '## 참고 사항',
        f'- 자료 수집일: {date}',
        f'- 텍스트 자료: {total_sources}건',
        f'- 다운로드 이미지: {downloaded_count}건',
        f'- 다운로드 실패: {len(failed_images)}건',
    ])

    return '\n'.join(md_parts)


def save_blog_files(
    project_path: Path,
    html_content: str,
    image_guide: str,
    references: str,
    validate: bool = True
) -> Dict[str, Path]:
    """
    블로그 관련 파일들을 저장합니다.

    Args:
        project_path: 프로젝트 디렉토리 경로
        html_content: HTML 본문 내용
        image_guide: 이미지 가이드 마크다운
        references: 참조 마크다운
        validate: 글자수 검증 여부

    Returns:
        저장된 파일 경로들
    """
    files = {}

    # 본문.html 저장
    html_path = project_path / "본문.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    files["html"] = html_path

    # 글자수 검증
    if validate:
        result = validate_char_count(html_content)
        if not result.is_valid:
            print(result.message)

    # 이미지 가이드.md 저장
    guide_path = project_path / "이미지 가이드.md"
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(image_guide)
    files["image_guide"] = guide_path

    # 참조.md 저장
    ref_path = project_path / "참조.md"
    with open(ref_path, "w", encoding="utf-8") as f:
        f.write(references)
    files["references"] = ref_path

    # 메타데이터 업데이트
    update_metadata(project_path, {
        "files": {
            "html": str(html_path),
            "image_guide": str(guide_path),
            "references": str(ref_path),
        },
        "status": "completed",
    })

    return files


def print_completion_summary(
    project_path: Path,
    files: Dict[str, Path],
    validation_result: Optional[ValidationResult] = None
) -> None:
    """
    완료 요약을 출력합니다.

    Args:
        project_path: 프로젝트 디렉토리 경로
        files: 저장된 파일들
        validation_result: 글자수 검증 결과
    """
    print("=" * 50)
    print("✅ 블로그 글 작성 완료!")
    print("=" * 50)
    print(f"\n📁 저장 위치: {project_path}")
    print("")

    for file_type, file_path in files.items():
        print(f"  ├── {file_path.name}")

    images_dir = project_path / "images"
    if images_dir.exists():
        image_count = len(list(images_dir.iterdir()))
        print(f"  └── images/ ({image_count}개)")

    print("")
    print("📋 네이버 블로그에 붙여넣기 방법")
    print("  1. 본문.html 파일을 브라우저에서 열기")
    print("  2. Cmd+A (전체 선택) → Cmd+C (복사)")
    print("  3. 네이버 블로그 에디터에서 Cmd+V (붙여넣기)")
    print("  4. [이미지 N 삽입] 위치에 실제 이미지 업로드")

    if validation_result:
        print("")
        print(f"📊 글자수: {validation_result.char_count}자")
        print(f"   {validation_result.message}")

    print("=" * 50)
