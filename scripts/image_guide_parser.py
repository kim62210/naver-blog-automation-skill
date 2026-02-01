"""
Image guide markdown parser.

This module provides a single, shared parser for `이미지 가이드.md` so that:
- `scripts.image_pipeline` and `scripts.prompt_converter` stay in sync
- small formatting variations in the guide don't break automation

Supported section headers:
- "## [Image 1] Role"
- "## [이미지 1] 역할"
- "━━━ [Image 1] Role" / "━━━ [이미지 1] 역할" (legacy delimiter style)

Supported prompt extraction:
- First fenced code block (``` ... ```) inside each image section.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class ImageGuideSection:
    index: int
    role: str
    body: str


_SECTION_HEADER_RE = re.compile(
    r"(?:(?:^|\n)##\s*\[(?:Image|이미지)\s*(\d+)\]\s*(.*)$)"
    r"|(?:(?:^|\n)━+\s*\[(?:Image|이미지)\s*(\d+)\]\s*(.*)$)",
    re.IGNORECASE | re.MULTILINE,
)

_FENCED_CODE_BLOCK_RE = re.compile(
    r"```(?:[^\n`]*)\n(.*?)\n```",
    re.DOTALL,
)


def split_image_sections(markdown: str) -> List[ImageGuideSection]:
    """
    Split an image guide markdown into per-image sections.

    Returns:
        List[ImageGuideSection] ordered by appearance.
    """
    matches = list(_SECTION_HEADER_RE.finditer(markdown))
    if not matches:
        return []

    sections: List[ImageGuideSection] = []

    for i, m in enumerate(matches):
        # Two alternative capture groups depending on header style.
        idx = int(m.group(1) or m.group(3))
        role = (m.group(2) or m.group(4) or "").strip() or f"Image {idx}"

        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)
        body = markdown[start:end].strip()

        sections.append(ImageGuideSection(index=idx, role=role, body=body))

    return sections


def extract_first_prompt(section_body: str) -> Optional[str]:
    """
    Extract the first fenced code block from a section body.

    The image pipeline treats this code block as the final prompt string.
    """
    m = _FENCED_CODE_BLOCK_RE.search(section_body)
    if not m:
        return None
    prompt = m.group(1).strip()
    return prompt or None

