"""
글자수 검증 모듈

HTML 태그를 제외한 순수 텍스트의 글자수를 검증하고,
초과/미달 시 조정을 제안합니다.
"""

import re
from dataclasses import dataclass
from typing import List, Tuple, Optional
from .config import get_config, get_config_value


@dataclass
class ValidationResult:
    """글자수 검증 결과"""
    char_count: int          # 실제 글자수
    target: int              # 목표 글자수
    min_chars: int           # 최소 글자수
    max_chars: int           # 최대 글자수
    is_valid: bool           # 유효 여부
    status: str              # 상태 ('ok', 'under', 'over')
    difference: int          # 차이 (양수: 초과, 음수: 미달)
    message: str             # 상태 메시지


def strip_html_tags(html_content: str) -> str:
    """
    HTML 태그를 모두 제거합니다.

    Args:
        html_content: HTML 콘텐츠

    Returns:
        태그가 제거된 텍스트
    """
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', html_content)
    return text


def remove_non_content(text: str) -> str:
    """
    글자수 카운트에서 제외할 요소를 제거합니다.

    제외 항목:
    - 이미지 placeholder
    - CSS 스타일 코드

    Args:
        text: 원본 텍스트

    Returns:
        정리된 텍스트
    """
    # 이미지 placeholder 제거
    text = re.sub(r'\[이미지\s*\d+\s*삽입[^\]]*\]', '', text)

    # CSS 스타일 블록 제거 (만약 남아있다면)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)

    return text


def normalize_whitespace(text: str) -> str:
    """
    공백을 정규화합니다.

    Args:
        text: 원본 텍스트

    Returns:
        정규화된 텍스트
    """
    # 연속된 공백을 단일 공백으로
    text = re.sub(r'[ \t]+', ' ', text)

    # 줄바꿈은 하나의 공백으로 취급
    text = re.sub(r'\n+', ' ', text)

    return text.strip()


def count_content_chars(html_content: str, include_spaces: bool = True) -> int:
    """
    HTML 콘텐츠에서 순수 글자수를 카운트합니다.

    Args:
        html_content: HTML 콘텐츠
        include_spaces: 공백 포함 여부 (기본값: True)

    Returns:
        글자수
    """
    # HTML 태그 제거
    text = strip_html_tags(html_content)

    # 비콘텐츠 요소 제거
    text = remove_non_content(text)

    # 공백 정규화
    text = normalize_whitespace(text)

    if not include_spaces:
        text = re.sub(r'\s+', '', text)

    return len(text)


def validate_char_count(html_content: str, config: Optional[dict] = None) -> ValidationResult:
    """
    글자수를 검증합니다.

    Args:
        html_content: HTML 콘텐츠
        config: 설정 딕셔너리 (없으면 기본 설정 사용)

    Returns:
        ValidationResult 객체
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
        message = f"⚠️ 글자수 미달: {char_count}자 (최소 {min_chars}자 필요, {min_chars - char_count}자 부족)"
    elif char_count > max_chars:
        status = "over"
        is_valid = False
        message = f"⚠️ 글자수 초과: {char_count}자 (최대 {max_chars}자, {char_count - max_chars}자 초과)"
    else:
        status = "ok"
        is_valid = True
        message = f"✅ 글자수 적합: {char_count}자 (목표: {target}자)"

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
    섹션별 글자수를 분석합니다.

    Args:
        html_content: HTML 콘텐츠

    Returns:
        (섹션명, 글자수) 튜플 리스트
    """
    sections = []

    # h2, h3 태그를 기준으로 섹션 분리
    pattern = r'<h[23][^>]*>(.*?)</h[23]>'
    matches = list(re.finditer(pattern, html_content, re.DOTALL))

    if not matches:
        # 섹션 구분이 없으면 전체를 하나의 섹션으로
        char_count = count_content_chars(html_content)
        return [("전체", char_count)]

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
    글자수 조정 제안을 생성합니다.

    Args:
        result: ValidationResult 객체

    Returns:
        조정 제안 메시지
    """
    if result.is_valid:
        return "글자수가 적합합니다. 조정이 필요하지 않습니다."

    suggestions = []

    if result.status == "under":
        needed = result.min_chars - result.char_count
        suggestions.append(f"📝 {needed}자 이상 추가가 필요합니다.")
        suggestions.append("추천 조정 방법:")
        suggestions.append("  - 핵심 정보 섹션에 구체적인 예시 추가")
        suggestions.append("  - 실용 팁 섹션 확장")
        suggestions.append("  - 관련 통계나 데이터 보충")

    elif result.status == "over":
        excess = result.char_count - result.max_chars
        suggestions.append(f"✂️ {excess}자 이상 삭제가 필요합니다.")
        suggestions.append("추천 조정 방법:")
        suggestions.append("  - 중복되는 내용 제거")
        suggestions.append("  - 부연 설명 간소화")
        suggestions.append("  - 불필요한 수식어 삭제")

    return "\n".join(suggestions)


def print_validation_report(html_content: str, config: Optional[dict] = None) -> ValidationResult:
    """
    글자수 검증 보고서를 출력합니다.

    Args:
        html_content: HTML 콘텐츠
        config: 설정 딕셔너리

    Returns:
        ValidationResult 객체
    """
    result = validate_char_count(html_content, config)

    print("=" * 50)
    print("📊 글자수 검증 결과")
    print("=" * 50)
    print(f"현재 글자수: {result.char_count}자")
    print(f"목표 글자수: {result.target}자")
    print(f"허용 범위: {result.min_chars}~{result.max_chars}자")
    print(f"차이: {result.difference:+d}자")
    print("-" * 50)
    print(result.message)

    if not result.is_valid:
        print("-" * 50)
        print(suggest_adjustment(result))

    # 섹션별 분석
    print("-" * 50)
    print("📑 섹션별 글자수:")
    sections = get_section_breakdown(html_content)
    for section_name, char_count in sections:
        print(f"  - {section_name}: {char_count}자")

    print("=" * 50)

    return result


if __name__ == "__main__":
    # 테스트용 샘플 HTML
    sample_html = """
    <h2>테스트 제목</h2>
    <p>이것은 테스트 본문입니다. 글자수를 측정하기 위한 샘플 텍스트입니다.</p>
    <div class="image-placeholder">[이미지 1 삽입]</div>
    <h3>소제목</h3>
    <p>추가 내용입니다.</p>
    """

    result = print_validation_report(sample_html)
    print(f"\n유효 여부: {result.is_valid}")
