"""
Common utility functions

Provides common functionality for filename normalization, date handling, text cleanup, etc.
"""

import re
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Optional


def normalize_filename(text: str, max_length: int = 50) -> str:
    """
    Normalize text for use as a filename.

    Args:
        text: Text to normalize
        max_length: Maximum length (default: 50)

    Returns:
        Normalized filename

    Example:
        >>> normalize_filename("2026년 육아휴직 변경 사항!")
        '2026년-육아휴직-변경-사항'
    """
    # Unicode normalization (NFC)
    text = unicodedata.normalize("NFC", text)

    # Remove special characters not allowed in filenames
    # Allowed: Korean, English, numbers, hyphens, underscores
    text = re.sub(r'[^\w가-힣\s-]', '', text)

    # Convert consecutive spaces to hyphens
    text = re.sub(r'\s+', '-', text.strip())

    # Remove consecutive hyphens
    text = re.sub(r'-+', '-', text)

    # Remove leading/trailing hyphens
    text = text.strip('-')

    # Apply maximum length limit
    if len(text) > max_length:
        text = text[:max_length].rstrip('-')

    return text


def get_today_date(format_str: str = "%Y-%m-%d") -> str:
    """
    Return today's date in the specified format.

    Args:
        format_str: Date format (default: "%Y-%m-%d")

    Returns:
        Formatted date string
    """
    return datetime.now().strftime(format_str)


def create_output_path(
    base_dir: str,
    topic: str,
    date: Optional[str] = None
) -> Path:
    """
    Create output path.

    Args:
        base_dir: Base directory (e.g., "./경제 블로그")
        topic: Topic name
        date: Date (uses today's date if not provided)

    Returns:
        Output path (Path object)

    Example:
        >>> create_output_path("./경제 블로그", "육아휴직 가이드")
        Path('./경제 블로그/2026-01-27/육아휴직-가이드')
    """
    if date is None:
        date = get_today_date()

    normalized_topic = normalize_filename(topic)
    return Path(base_dir) / date / normalized_topic


def clean_text(text: str) -> str:
    """
    Clean text (remove unnecessary whitespace, normalize line breaks).

    Args:
        text: Text to clean

    Returns:
        Cleaned text
    """
    # Normalize multiple line breaks to two
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove trailing whitespace from lines
    lines = [line.rstrip() for line in text.split('\n')]
    text = '\n'.join(lines)

    return text.strip()


def extract_extension_from_url(url: str) -> str:
    """
    Extract file extension from URL.

    Args:
        url: Image URL

    Returns:
        Extension (default: 'jpg')
    """
    # Remove query parameters from URL
    clean_url = url.split('?')[0]

    # Extract extension
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
    lower_url = clean_url.lower()

    for ext in extensions:
        if lower_url.endswith(ext):
            return ext[1:]  # Remove dot

    return 'jpg'  # Default


def format_image_filename(
    index: int,
    source: str,
    description: str,
    extension: str
) -> str:
    """
    Format image filename.

    Args:
        index: Sequence number (starting from 1)
        source: Source (뉴스/블로그/검색)
        description: Description (Korean)
        extension: Extension

    Returns:
        Formatted filename

    Example:
        >>> format_image_filename(1, "뉴스", "금리 비교표", "jpg")
        '01_뉴스_금리비교표.jpg'
    """
    # Remove spaces from description
    clean_desc = description.replace(' ', '')
    clean_desc = normalize_filename(clean_desc, max_length=20)

    return f"{index:02d}_{source}_{clean_desc}.{extension}"


def count_chars_excluding_html(html_content: str) -> int:
    """
    Count characters excluding HTML tags.

    Args:
        html_content: HTML content

    Returns:
        Character count (including spaces)
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_content)

    # Remove image placeholders
    text = re.sub(r'\[이미지\s*\d+\s*삽입[^\]]*\]', '', text)

    # Normalize consecutive spaces to single space
    text = re.sub(r'\s+', ' ', text)

    return len(text.strip())


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to specified length.

    Args:
        text: Original text
        max_length: Maximum length
        suffix: Ellipsis indicator (default: "...")

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def parse_time_ago(time_str: str) -> Optional[int]:
    """
    Convert '~시간 전', '~일 전' format strings to minutes.

    Args:
        time_str: Time string (e.g., "3시간 전", "1일 전")

    Returns:
        Time in minutes (None if parsing fails)
    """
    patterns = [
        (r'(\d+)\s*분\s*전', 1),
        (r'(\d+)\s*시간\s*전', 60),
        (r'(\d+)\s*일\s*전', 60 * 24),
    ]

    for pattern, multiplier in patterns:
        match = re.search(pattern, time_str)
        if match:
            return int(match.group(1)) * multiplier

    return None


def sanitize_for_markdown(text: str) -> str:
    """
    Escape markdown special characters.

    Args:
        text: Original text

    Returns:
        Escaped text
    """
    special_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!', '|']

    for char in special_chars:
        text = text.replace(char, '\\' + char)

    return text
