"""
HTML/MD generation module

Renders Jinja2-style templates to generate 본문.html, image guide.md, and references.md.
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
    Load template file.

    Args:
        template_name: Template filename
        templates_dir: Template directory (uses default path if not provided)

    Returns:
        Template content
    """
    if templates_dir is None:
        # Find templates directory relative to current script location
        script_dir = Path(__file__).parent
        templates_dir = script_dir.parent / "templates"

    template_path = templates_dir / template_name

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def render_template(template_content: str, context: Dict[str, Any]) -> str:
    """
    Simple template rendering (using Python string.Template).

    Supported syntax:
    - ${variable} or $variable: Variable substitution
    - Loops not supported (requires separate handling)

    Args:
        template_content: Template content
        context: Context variables

    Returns:
        Rendered content
    """
    # Basic substitution
    template = Template(template_content)

    # Use safe_substitute to keep missing variables as-is
    result = template.safe_substitute(context)

    return result


def generate_html_content(
    title: str,
    sections: List[Dict[str, Any]],
    tags: List[str],
    config: Optional[Dict] = None
) -> str:
    """
    Generate HTML content.

    Args:
        title: Title
        sections: Section list [{"title": str, "content": str, "has_image": bool}]
        tags: Tag list
        config: Configuration dictionary

    Returns:
        HTML content
    """
    if config is None:
        config = get_config()

    # HTML template start
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

    # Add section content
    image_index = 2
    for section in sections:
        section_title = section.get("title", "")
        section_content = section.get("content", "")
        has_image = section.get("has_image", False)
        section_type = section.get("type", "normal")

        # Section title
        if section_title:
            html_parts.append(f'\n<h2>{section_title}</h2>\n')

        # Section content
        if section_content:
            # Split content into paragraphs
            paragraphs = section_content.split('\n\n')
            for para in paragraphs:
                para = para.strip()
                if para:
                    # Handle quotes
                    if para.startswith('"') and para.endswith('"'):
                        html_parts.append(f'<blockquote>\n{para}\n</blockquote>\n')
                    else:
                        html_parts.append(f'<p>{para}</p>\n')

        # Image placeholder
        if has_image:
            html_parts.append(f'\n<div class="image-placeholder">[이미지 {image_index} 삽입]</div>\n')
            image_index += 1

        html_parts.append('\n<hr>\n')

    # Add tags
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
    Generate image guide markdown.

    Args:
        topic: Topic
        images: Image guide list
        color_palette: Color palette
        date: Date

    Returns:
        Markdown content
    """
    if date is None:
        date = get_today_date()

    md_parts = [
        '# Image Guide',
        '',
        '## Basic Information',
        f'- Topic: {topic}',
        f'- Created: {date}',
        f'- Total images: {len(images)}',
        '',
        '## Color Palette',
        f'- Main: {color_palette.get("main", "#1a365d")}',
        f'- Accent: {color_palette.get("accent", "#d69e2e")}',
        f'- Background: {color_palette.get("background", "#ffffff")}',
        f'- Text: {color_palette.get("text", "#333333")}',
        '',
        '---',
        '',
    ]

    for idx, img in enumerate(images, 1):
        role = img.get("role", f"Image {idx}")
        mode = img.get("mode", "ai_generate")

        md_parts.append(f'## [Image {idx}] {role}')
        md_parts.append('')

        if mode == "reference":
            # Reference image mode
            md_parts.extend([
                '### 📷 Reference Image',
                f'**File:** {img.get("filename", "N/A")}',
                f'**Source:** {img.get("source_url", "N/A")}',
                f'**Usage:** {img.get("usage", "Direct use / Layout reference")}',
                '',
            ])

        if mode in ("ai_generate", "both"):
            # AI image generation prompt
            md_parts.extend([
                '### 🎨 AI Generation Prompt',
                '',
                '**Korean Description:**',
                img.get("description_kr", "Enter image description."),
                '',
                '**AI Generation Prompt:**',
                '```',
                img.get("prompt_en", "Image generation prompt here"),
                '```',
                '',
                '**Style:**',
                f'- Color: {img.get("colors", color_palette.get("main"))}',
                f'- Mood: {img.get("mood", "Professional")}',
                f'- Format: {img.get("format", "Infographic")}',
                '',
            ])

        if mode in ("svg", "both"):
            # SVG generation guide
            md_parts.extend([
                '### 🔷 SVG Generation Guide',
                '',
                f'**Canvas:** {img.get("canvas_width", 800)}x{img.get("canvas_height", 450)}px',
                f'**Background:** {img.get("background", color_palette.get("background", "#ffffff"))}',
                '',
                '**Elements:**',
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
    Generate references markdown document.

    Args:
        topic: Topic
        text_sources: Text sources {"네이버 뉴스": [...], "네이버 블로그": [...]}
        images: Image information list
        date: Date

    Returns:
        Markdown content
    """
    if date is None:
        date = get_today_date()

    md_parts = [
        '# References',
        '',
        '## Date',
        date,
        '',
        '## Topic',
        topic,
        '',
        '---',
        '',
        '## Text Sources',
        '',
    ]

    total_sources = 0

    for source_name, sources in text_sources.items():
        if sources:
            md_parts.append(f'### {source_name}')

            for idx, source in enumerate(sources, 1):
                title = source.get("title", "No title")
                url = source.get("url", "#")
                summary = source.get("summary", "")

                md_parts.append(f'{idx}. [{title}]({url})')
                if summary:
                    md_parts.append(f'   - Summary: {summary}')

                total_sources += 1

            md_parts.append('')

    md_parts.extend([
        '---',
        '',
        '## Downloaded Images',
        '',
        'Location: `./images/`',
        '',
        '| # | Filename | Description | Source |',
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
            '### Download Failed (URL only)',
            '',
            '| # | Description | Image URL | Failure Reason |',
            '|---|------|-----------|----------|',
        ])

        for idx, img in enumerate(failed_images, 1):
            description = img.get("description", "")
            url = img.get("url", "")[:50] + "..."
            error = img.get("error", "Unknown")

            md_parts.append(f'| {idx} | {description} | {url} | {error} |')

        md_parts.append('')

    md_parts.extend([
        '---',
        '',
        '## Notes',
        f'- Collection date: {date}',
        f'- Text sources: {total_sources}',
        f'- Downloaded images: {downloaded_count}',
        f'- Failed downloads: {len(failed_images)}',
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
    Save blog-related files.

    Args:
        project_path: Project directory path
        html_content: HTML content
        image_guide: Image guide markdown
        references: References markdown
        validate: Whether to validate character count

    Returns:
        Saved file paths
    """
    files = {}

    # Save 본문.html
    html_path = project_path / "본문.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    files["html"] = html_path

    # Validate character count
    if validate:
        result = validate_char_count(html_content)
        if not result.is_valid:
            print(result.message)

    # Save 이미지 가이드.md
    guide_path = project_path / "이미지 가이드.md"
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(image_guide)
    files["image_guide"] = guide_path

    # Save 참조.md
    ref_path = project_path / "참조.md"
    with open(ref_path, "w", encoding="utf-8") as f:
        f.write(references)
    files["references"] = ref_path

    # Update metadata
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
    Print completion summary.

    Args:
        project_path: Project directory path
        files: Saved files
        validation_result: Character count validation result
    """
    print("=" * 50)
    print("✅ Blog post creation complete!")
    print("=" * 50)
    print(f"\n📁 Location: {project_path}")
    print("")

    for file_type, file_path in files.items():
        print(f"  ├── {file_path.name}")

    images_dir = project_path / "images"
    if images_dir.exists():
        image_count = len(list(images_dir.iterdir()))
        print(f"  └── images/ ({image_count} files)")

    print("")
    print("📋 How to paste into Naver Blog")
    print("  1. Open 본문.html file in browser")
    print("  2. Cmd+A (Select all) → Cmd+C (Copy)")
    print("  3. Cmd+V (Paste) in Naver Blog editor")
    print("  4. Upload actual images at [이미지 N 삽입] positions")

    if validation_result:
        print("")
        print(f"📊 Character count: {validation_result.char_count}")
        print(f"   {validation_result.message}")

    print("=" * 50)
