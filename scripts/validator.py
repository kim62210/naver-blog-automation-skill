"""
Character count validation module

Validates character count of pure text excluding HTML tags,
and suggests adjustments when over/under the limit.
"""

import re
from dataclasses import dataclass
from typing import List, Tuple, Optional
from .config import get_config, get_config_value


@dataclass
class ValidationResult:
    """Character count validation result"""
    char_count: int          # Actual character count
    target: int              # Target character count
    min_chars: int           # Minimum character count
    max_chars: int           # Maximum character count
    is_valid: bool           # Validity status
    status: str              # Status ('ok', 'under', 'over')
    difference: int          # Difference (positive: over, negative: under)
    message: str             # Status message


def strip_html_tags(html_content: str) -> str:
    """
    Remove all HTML tags.

    Args:
        html_content: HTML content

    Returns:
        Text with tags removed
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_content)
    return text


def remove_non_content(text: str) -> str:
    """
    Remove elements excluded from character count.

    Excluded items:
    - Image placeholders
    - CSS style code

    Args:
        text: Original text

    Returns:
        Cleaned text
    """
    # Remove image placeholders
    text = re.sub(r'\[이미지\s*\d+\s*삽입[^\]]*\]', '', text)

    # Remove CSS style blocks (if any remain)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)

    return text


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace.

    Args:
        text: Original text

    Returns:
        Normalized text
    """
    # Convert consecutive spaces to single space
    text = re.sub(r'[ \t]+', ' ', text)

    # Treat line breaks as single space
    text = re.sub(r'\n+', ' ', text)

    return text.strip()


def count_content_chars(html_content: str, include_spaces: bool = True) -> int:
    """
    Count characters in HTML content.

    Args:
        html_content: HTML content
        include_spaces: Include spaces (default: True)

    Returns:
        Character count
    """
    # Remove HTML tags
    text = strip_html_tags(html_content)

    # Remove non-content elements
    text = remove_non_content(text)

    # Normalize whitespace
    text = normalize_whitespace(text)

    if not include_spaces:
        text = re.sub(r'\s+', '', text)

    return len(text)


def validate_char_count(html_content: str, config: Optional[dict] = None) -> ValidationResult:
    """
    Validate character count.

    Args:
        html_content: HTML content
        config: Configuration dictionary (uses default if not provided)

    Returns:
        ValidationResult object
    """
    if config is None:
        config = get_config()

    target = get_config_value(config, "writing", "char_count", default=1850)
    min_chars = get_config_value(config, "writing", "min_chars", default=1800)
    max_chars = get_config_value(config, "writing", "max_chars", default=1900)

    char_count = count_content_chars(html_content)
    difference = char_count - target

    if char_count < min_chars:
        status = "under"
        is_valid = False
        message = f"⚠️ Character count under limit: {char_count} chars (minimum {min_chars} required, {min_chars - char_count} short)"
    elif char_count > max_chars:
        status = "over"
        is_valid = False
        message = f"⚠️ Character count over limit: {char_count} chars (maximum {max_chars}, {char_count - max_chars} over)"
    else:
        status = "ok"
        is_valid = True
        message = f"✅ Character count valid: {char_count} chars (target: {target})"

    return ValidationResult(
        char_count=char_count,
        target=target,
        min_chars=min_chars,
        max_chars=max_chars,
        is_valid=is_valid,
        status=status,
        difference=difference,
        message=message
    )


def get_section_breakdown(html_content: str) -> List[Tuple[str, int]]:
    """
    Analyze character count by section.

    Args:
        html_content: HTML content

    Returns:
        List of (section_name, char_count) tuples
    """
    sections = []

    # Split sections by h2, h3 tags
    pattern = r'<h[23][^>]*>(.*?)</h[23]>'
    matches = list(re.finditer(pattern, html_content, re.DOTALL))

    if not matches:
        # If no section divisions, treat entire content as one section
        char_count = count_content_chars(html_content)
        return [("Total", char_count)]

    for i, match in enumerate(matches):
        section_title = strip_html_tags(match.group(1)).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(html_content)

        section_content = html_content[start:end]
        char_count = count_content_chars(section_content)
        sections.append((section_title, char_count))

    return sections


def suggest_adjustment(result: ValidationResult) -> str:
    """
    Generate character count adjustment suggestions.

    Args:
        result: ValidationResult object

    Returns:
        Adjustment suggestion message
    """
    if result.is_valid:
        return "Character count is valid. No adjustment needed."

    suggestions = []

    if result.status == "under":
        needed = result.min_chars - result.char_count
        suggestions.append(f"📝 Need to add {needed}+ characters.")
        suggestions.append("Recommended adjustments:")
        suggestions.append("  - Add specific examples to key information sections")
        suggestions.append("  - Expand practical tips section")
        suggestions.append("  - Add relevant statistics or data")

    elif result.status == "over":
        excess = result.char_count - result.max_chars
        suggestions.append(f"✂️ Need to remove {excess}+ characters.")
        suggestions.append("Recommended adjustments:")
        suggestions.append("  - Remove redundant content")
        suggestions.append("  - Simplify elaborations")
        suggestions.append("  - Delete unnecessary modifiers")

    return "\n".join(suggestions)


def print_validation_report(html_content: str, config: Optional[dict] = None) -> ValidationResult:
    """
    Print character count validation report.

    Args:
        html_content: HTML content
        config: Configuration dictionary

    Returns:
        ValidationResult object
    """
    result = validate_char_count(html_content, config)

    print("=" * 50)
    print("📊 Character Count Validation Result")
    print("=" * 50)
    print(f"Current count: {result.char_count} chars")
    print(f"Target count: {result.target} chars")
    print(f"Allowed range: {result.min_chars}~{result.max_chars} chars")
    print(f"Difference: {result.difference:+d} chars")
    print("-" * 50)
    print(result.message)

    if not result.is_valid:
        print("-" * 50)
        print(suggest_adjustment(result))

    # Section analysis
    print("-" * 50)
    print("📑 Character count by section:")
    sections = get_section_breakdown(html_content)
    for section_name, char_count in sections:
        print(f"  - {section_name}: {char_count} chars")

    print("=" * 50)

    return result


if __name__ == "__main__":
    # Test sample HTML
    sample_html = """
    <h2>테스트 제목</h2>
    <p>이것은 테스트 본문입니다. 글자수를 측정하기 위한 샘플 텍스트입니다.</p>
    <div class="image-placeholder">[이미지 1 삽입]</div>
    <h3>소제목</h3>
    <p>추가 내용입니다.</p>
    """

    result = print_validation_report(sample_html)
    print(f"\nValidity: {result.is_valid}")
