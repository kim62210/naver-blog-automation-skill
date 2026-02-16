"""HTML/MD generation -- renders templates to produce blog HTML, image guide, and references."""

from pathlib import Path
from string import Template
from typing import Dict, List, Optional, Any

from .config import get_config, get_config_value
from .utils import get_today_date
from .validator import validate_char_count, validate_draft_char_count, ValidationResult
from .setup import update_metadata

_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def _normalize_image_sources(image_sources: Optional[Any]) -> Dict[int, str]:
    """Normalize different image source formats into a slot-based dict."""
    if not image_sources:
        return {}

    if isinstance(image_sources, dict):
        raw_items = image_sources.items()
    else:
        raw_items = enumerate(image_sources, start=1)

    normalized: Dict[int, str] = {}
    for raw_index, raw_value in raw_items:  # type: ignore[assignment]
        try:
            index = int(raw_index)
        except (TypeError, ValueError):
            continue

        if raw_value is None:
            continue

        value: Any = raw_value
        if isinstance(raw_value, dict):
            value = raw_value.get("file_path") or raw_value.get("src") or raw_value.get("path")
        elif not isinstance(raw_value, str) and hasattr(raw_value, "file_path"):
            value = getattr(raw_value, "file_path")

        if not isinstance(value, str):
            continue

        normalized[index] = value.strip()

    return normalized


def _to_image_data_uri(image_path: str) -> Optional[str]:
    """Convert local image file path to data URI for safe paste."""
    candidate = image_path.strip()
    if not candidate:
        return None

    path = Path(candidate)
    if not path.is_absolute():
        # Keep working path behavior for relative references if it exists
        try:
            if not path.exists():
                return None
        except OSError:
            return None

    try:
        with open(path, "rb") as image_file:
            image_data = image_file.read()

        mime_type, _ = mimetypes.guess_type(str(path))
        if not mime_type:
            mime_type = "image/png"

        encoded = base64.b64encode(image_data).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"
    except Exception:
        return None


def _build_image_html(index: int, image_source: Optional[str], embed_images: bool = True) -> str:
    """Build a single image block HTML string for a given slot."""
    placeholder = (
        f'\n<div class="image-placeholder">[이미지 {index} 삽입]'
        f"</div>\n"
    )

    if not image_source:
        return placeholder

    src = image_source.strip()
    if not src:
        return placeholder

    if embed_images and not (src.startswith("http://") or src.startswith("https://") or src.startswith("data:")):
        data_uri = _to_image_data_uri(src)
        if data_uri:
            src = data_uri

    return (
        f"\n<div class='image-wrap'>\n"
        f"  <img class='blog-image' src=\"{src}\" alt=\"이미지 {index}\" loading=\"lazy\">\n"
        f"</div>\n"
    )


def load_template(template_name: str, templates_dir: Optional[Path] = None) -> str:
    """Load a template file by name. Returns the raw template string."""
    templates_dir = templates_dir or _TEMPLATES_DIR
    template_path = templates_dir / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def render_template(template_content: str, context: Dict[str, Any]) -> str:
    """Render a string.Template with *context*. Missing keys are left as-is."""
    return Template(template_content).safe_substitute(context)


def _build_naver_subtitle_html(subtitle: str, line_height: float = 1.8) -> str:
    paragraph_id = f"SE-{uuid.uuid4()}"
    span_id = f"SE-{uuid.uuid4()}"
    escaped_subtitle = html.escape(subtitle, quote=False)
    return (
        f'\n<p id="{paragraph_id}" class="se-text-paragraph se-text-paragraph-align-left" '
        f'style="line-height: {line_height};">'
        f'<span id="{span_id}" class="se-ff-system se-fs30 __se-node" '
        f'style="color: rgb(0, 0, 0);"><b>{escaped_subtitle}</b></span></p>\n'
    )


def _build_sections_html(
    sections: List[Dict[str, Any]],
    image_sources: Optional[Dict[int, str]] = None,
    embed_images: bool = True,
    line_height: float = 1.8,
) -> str:
    resolved_images = _normalize_image_sources(image_sources)

    parts: List[str] = []
    image_index = 2
    for section in sections:
        title = section.get("title", "")
        content = section.get("content", "")
        if title:
            parts.append(_build_naver_subtitle_html(title, line_height=line_height))
        if content:
            for para in content.split('\n\n'):
                para = para.strip()
                if not para:
                    continue
                if para.startswith('"') and para.endswith('"'):
                    parts.append(f'<blockquote>\n{para}\n</blockquote>\n')
                else:
                    parts.append(f'<p>{para}</p>\n')
        if section.get("has_image", False):
            parts.append(_build_image_html(image_index, resolved_images.get(image_index), embed_images=embed_images))
            image_index += 1
        parts.append('\n<hr>\n')
    return '\n'.join(parts)


def generate_html_content(
    title: str,
    sections: List[Dict[str, Any]],
    tags: List[str],
    config: Optional[Dict] = None,
    image_sources: Optional[Any] = None,
    embed_images: bool = True,
) -> str:
    """Generate full blog HTML by rendering the blog-post template with *sections*."""
    if config is None:
        config = get_config()

    resolved_images = _normalize_image_sources(image_sources)

    font_family = get_config_value(
        config, "typography", "font_family",
        default="Nanum Gothic, Pretendard, sans-serif",
    )
    line_height = get_config_value(config, "typography", "line_height", default=1.8)
    sizes = get_config_value(config, "typography", "blog_sizes", default={}) or {}

    return render_template(load_template("blog-post.html"), {
        "font_family": font_family,
        "line_height": line_height,
        "title_size": int(sizes.get("title", 28)),
        "title_medium_size": int(sizes.get("title_medium", 24)),
        "title_small_size": int(sizes.get("title_small", 19)),
        "body_size": int(sizes.get("body", 16)),
        "footnote_size": int(sizes.get("footnote", 11)),
        "title": title,
        "thumbnail_html": _build_image_html(1, resolved_images.get(1), embed_images=embed_images),
        "sections_html": _build_sections_html(
            sections,
            image_sources=resolved_images,
            embed_images=embed_images,
            line_height=float(line_height),
        ),
        "tags": ' '.join(f'#{tag}' for tag in tags),
    })


def replace_image_placeholders_in_html(
    html_content: str,
    image_sources: Optional[Any] = None,
    embed_images: bool = True,
) -> str:
    """Replace placeholder blocks in existing HTML with generated image tags."""
    resolved_images = _normalize_image_sources(image_sources)

    def _repl(match: re.Match[str]) -> str:
        index = int(match.group(1))
        return _build_image_html(index, resolved_images.get(index), embed_images=embed_images)

    return re.sub(
        r'<div class="image-placeholder">\s*\[이미지\s*(\d+)\s*삽입[^<]*\]\s*</div>',
        _repl,
        html_content,
    )


def _build_text_rendering_lines(title: str, subtitle: str = "") -> List[str]:
    """Return markdown lines with AI text-rendering instructions for *title*/*subtitle*."""
    if not title:
        return []
    lines = [
        '',
        '**TEXT RENDERING (CRITICAL)**:',
        f'- Main title: "{title}"',
        '  - Position: upper-center (y: 25-30% from top)',
        '  - Font: Extra bold Korean sans-serif (Pretendard or similar), 48-52px',
        '  - Color: #FFFFFF with subtle drop shadow for depth',
        '  - Style: Clear, readable, high contrast against background',
    ]
    if subtitle:
        lines.extend([
            f'- Subtitle: "{subtitle}"',
            '  - Position: center (y: 50% from top)',
            '  - Font: Bold sans-serif, 28-32px',
            '  - Color: White (#FFFFFF) with 90% opacity',
        ])
    lines.extend(['', 'IMPORTANT: Render the exact Korean text characters as specified above.', ''])
    return lines


def generate_image_guide(
    topic: str,
    images: List[Dict[str, Any]],
    color_palette: Dict[str, str],
    date: Optional[str] = None,
    blog_title: Optional[str] = None,
    blog_subtitle: Optional[str] = None,
    key_points: Optional[List[str]] = None,
    config: Optional[Dict] = None,
) -> str:
    """Generate image guide markdown with per-image prompts, style guides, and watermark config."""
    config = config or get_config()
    date = date or get_today_date()

    wm = get_config_value(config, "watermark", default={}) or {}
    wm_vars = {
        "text": wm.get("text", "@money-lab-brian"),
        "position": wm.get("position", "bottom-center"),
        "margin_bottom": wm.get("margin_bottom", 60),
        "font_size": wm.get("font_size", 18),
        "font_color": wm.get("font_color", "rgba(255,255,255,0.6)"),
        "font_family": wm.get("font_family", "Pretendard, Nanum Gothic, sans-serif"),
    }

    md_parts = [
        '# Image Guide', '',
        '## Basic Information',
        f'- Topic: {topic}',
        f'- Created: {date}',
        f'- Total images: {len(images)}', '',
        '## Color Palette',
        f'- Main: {color_palette.get("main", "#1a365d")}',
        f'- Accent: {color_palette.get("accent", "#d69e2e")}',
        f'- Background: {color_palette.get("background", "#ffffff")}',
        f'- Text: {color_palette.get("text", "#333333")}', '',
        '---', '',
    ]

    for idx, img in enumerate(images, 1):
        role = img.get("role", f"Image {idx}")
        mode = img.get("mode", "ai_generate")
        md_parts.extend([f'## [Image {idx}] {role}', ''])

        if mode == "reference":
            md_parts.extend([
                '### 📷 Reference Image',
                f'**File:** {img.get("filename", "N/A")}',
                f'**Source:** {img.get("source_url", "N/A")}',
                f'**Usage:** {img.get("usage", "Direct use / Layout reference")}', '',
            ])

        if mode in ("ai_generate", "both"):
            md_parts.extend([
                '### AI Generation (With Text)', '',
                '## [Korean Description]',
                img.get("description_kr", "Enter image description."), '',
            ])

            is_thumbnail = (
                idx == 1 or role.lower() in ("thumbnail", "썸네일", "대표 이미지", "메인 이미지")
            )
            if is_thumbnail and blog_title:
                md_parts.extend(['## [AI Generation Prompt]', '```', img.get("prompt_en", "")])
                md_parts.extend(_build_text_rendering_lines(blog_title, blog_subtitle or ""))
                md_parts.append('```')
            else:
                md_parts.extend([
                    '## [AI Generation Prompt]', '```',
                    img.get("prompt_en", "Image generation prompt here"), '```',
                ])

            md_parts.extend([
                '', '## [Style Guide]',
                f'- Color: {img.get("colors", color_palette.get("main"))}',
                f'- Mood: {img.get("mood", "Professional")}',
                f'- Format: {img.get("format", "Infographic")}',
                '- Ratio: 1:1 (1024x1024)', '',
                '[Watermark Config]',
                f'- watermark_text: "{wm_vars["text"]}"',
                f'- watermark_position: "{wm_vars["position"]}"',
                f'- watermark_margin_bottom: {wm_vars["margin_bottom"]}',
                f'- watermark_font_size: {wm_vars["font_size"]}',
                f'- watermark_font_color: "{wm_vars["font_color"]}"',
                f'- watermark_font_family: "{wm_vars["font_family"]}"', '',
            ])

        md_parts.extend(['---', ''])

    return '\n'.join(md_parts)


def generate_references(
    topic: str,
    text_sources: Dict[str, List[Dict[str, str]]],
    images: List[Dict[str, Any]],
    date: Optional[str] = None,
) -> str:
    """Generate references markdown listing text sources and downloaded images."""
    date = date or get_today_date()
    md_parts = [
        '# References', '',
        '## Date', date, '',
        '## Topic', topic, '',
        '---', '', '## Text Sources', '',
    ]

    total_sources = 0
    for source_name, sources in text_sources.items():
        if not sources:
            continue
        md_parts.append(f'### {source_name}')
        for idx, source in enumerate(sources, 1):
            md_parts.append(f'{idx}. [{source.get("title", "No title")}]({source.get("url", "#")})')
            if source.get("summary"):
                md_parts.append(f'   - Summary: {source["summary"]}')
            total_sources += 1
        md_parts.append('')

    md_parts.extend([
        '---', '', '## Downloaded Images', '', 'Location: `./images/`', '',
        '| # | Filename | Description | Source |',
        '|---|--------|------|------|',
    ])

    downloaded_count = 0
    failed_images: List[Dict[str, Any]] = []
    for idx, img in enumerate(images, 1):
        if img.get("downloaded", False):
            md_parts.append(
                f'| {idx} | {img.get("filename", "N/A")} | {img.get("description", "")} '
                f'| [{img.get("source_name", "")}]({img.get("source_url", "#")}) |'
            )
            downloaded_count += 1
        else:
            failed_images.append(img)
    md_parts.append('')

    if failed_images:
        md_parts.extend([
            '### Download Failed (URL only)', '',
            '| # | Description | Image URL | Failure Reason |',
            '|---|------|-----------|----------|',
        ])
        for idx, img in enumerate(failed_images, 1):
            md_parts.append(
                f'| {idx} | {img.get("description", "")} '
                f'| {img.get("url", "")[:50]}... | {img.get("error", "Unknown")} |'
            )
        md_parts.append('')

    md_parts.extend([
        '---', '', '## Notes',
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
    validate: bool = True,
) -> Dict[str, Path]:
    """Save 본문.html, 이미지 가이드.md, and 참조.md to *project_path*."""
    file_map = {
        "html": ("본문.html", html_content),
        "image_guide": ("이미지 가이드.md", image_guide),
        "references": ("참조.md", references),
    }
    files: Dict[str, Path] = {}
    for key, (name, content) in file_map.items():
        path = project_path / name
        path.write_text(content, encoding="utf-8")
        files[key] = path

    if validate:
        result = validate_char_count(html_content)
        if not result.is_valid:
            print(f"⚠️ Character count validation warning:\n   {result.message}")
            print(f"   Current: {result.char_count} chars, "
                  f"Target: {result.target} chars ({result.min_chars}-{result.max_chars})")

    update_metadata(project_path, {
        "files": {k: str(v) for k, v in files.items()},
        "status": "completed",
    })
    return files


def save_draft_file(
    project_path: Path,
    draft_text: str,
    validate: bool = True,
) -> Path:
    """Save *draft_text* as 원본.txt in *project_path* and optionally validate char count."""
    draft_path = project_path / "원본.txt"
    draft_path.write_text(draft_text, encoding="utf-8")

    if validate:
        result = validate_draft_char_count(draft_text)
        if not result.is_valid:
            print(f"⚠️ Draft character count validation warning:\n   {result.message}")
            print(f"   Current: {result.char_count} chars, "
                  f"Target: {result.target} chars ({result.min_chars}-{result.max_chars})")

    update_metadata(project_path, {"files": {"draft": str(draft_path)}, "status": "draft_ready"})
    return draft_path


def print_completion_summary(
    project_path: Path,
    files: Dict[str, Path],
    validation_result: Optional[ValidationResult] = None,
) -> None:
    """Print a completion summary with file listing and paste instructions."""
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
"""HTML/MD generation -- renders templates to produce blog HTML, image guide, and references."""

import base64
import html
import mimetypes
import re
import uuid
