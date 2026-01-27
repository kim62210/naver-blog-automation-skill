"""
공통 유틸리티 함수

파일명 정규화, 날짜 처리, 텍스트 정리 등의 공통 기능을 제공합니다.
"""

import re
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Optional


def normalize_filename(text: str, max_length: int = 50) -> str:
    """
    텍스트를 파일명으로 사용 가능한 형태로 정규화합니다.

    Args:
        text: 정규화할 텍스트
        max_length: 최대 길이 (기본값: 50)

    Returns:
        정규화된 파일명

    Example:
        >>> normalize_filename("2026년 육아휴직 변경 사항!")
        '2026년-육아휴직-변경-사항'
    """
    # 유니코드 정규화 (NFC)
    text = unicodedata.normalize("NFC", text)

    # 파일명에 사용할 수 없는 특수문자 제거
    # 허용: 한글, 영문, 숫자, 하이픈, 언더스코어
    text = re.sub(r'[^\w가-힣\s-]', '', text)

    # 연속된 공백을 하이픈으로 변환
    text = re.sub(r'\s+', '-', text.strip())

    # 연속된 하이픈 제거
    text = re.sub(r'-+', '-', text)

    # 앞뒤 하이픈 제거
    text = text.strip('-')

    # 최대 길이 제한
    if len(text) > max_length:
        text = text[:max_length].rstrip('-')

    return text


def get_today_date(format_str: str = "%Y-%m-%d") -> str:
    """
    오늘 날짜를 지정된 형식으로 반환합니다.

    Args:
        format_str: 날짜 형식 (기본값: "%Y-%m-%d")

    Returns:
        형식화된 날짜 문자열
    """
    return datetime.now().strftime(format_str)


def create_output_path(
    base_dir: str,
    topic: str,
    date: Optional[str] = None
) -> Path:
    """
    출력 경로를 생성합니다.

    Args:
        base_dir: 기본 디렉토리 (예: "./경제 블로그")
        topic: 주제명
        date: 날짜 (없으면 오늘 날짜 사용)

    Returns:
        출력 경로 (Path 객체)

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
    텍스트를 정리합니다 (불필요한 공백, 줄바꿈 정리).

    Args:
        text: 정리할 텍스트

    Returns:
        정리된 텍스트
    """
    # 여러 줄바꿈을 두 줄바꿈으로 통일
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 줄 끝 공백 제거
    lines = [line.rstrip() for line in text.split('\n')]
    text = '\n'.join(lines)

    return text.strip()


def extract_extension_from_url(url: str) -> str:
    """
    URL에서 파일 확장자를 추출합니다.

    Args:
        url: 이미지 URL

    Returns:
        확장자 (기본값: 'jpg')
    """
    # URL에서 쿼리 파라미터 제거
    clean_url = url.split('?')[0]

    # 확장자 추출
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
    lower_url = clean_url.lower()

    for ext in extensions:
        if lower_url.endswith(ext):
            return ext[1:]  # 점 제거

    return 'jpg'  # 기본값


def format_image_filename(
    index: int,
    source: str,
    description: str,
    extension: str
) -> str:
    """
    이미지 파일명을 형식화합니다.

    Args:
        index: 순번 (1부터 시작)
        source: 출처 (뉴스/블로그/검색)
        description: 설명 (한글)
        extension: 확장자

    Returns:
        형식화된 파일명

    Example:
        >>> format_image_filename(1, "뉴스", "금리 비교표", "jpg")
        '01_뉴스_금리비교표.jpg'
    """
    # 설명에서 공백 제거
    clean_desc = description.replace(' ', '')
    clean_desc = normalize_filename(clean_desc, max_length=20)

    return f"{index:02d}_{source}_{clean_desc}.{extension}"


def count_chars_excluding_html(html_content: str) -> int:
    """
    HTML 태그를 제외한 순수 텍스트의 글자수를 카운트합니다.

    Args:
        html_content: HTML 콘텐츠

    Returns:
        글자수 (공백 포함)
    """
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', html_content)

    # 이미지 placeholder 제거
    text = re.sub(r'\[이미지\s*\d+\s*삽입[^\]]*\]', '', text)

    # 연속된 공백을 단일 공백으로
    text = re.sub(r'\s+', ' ', text)

    return len(text.strip())


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    텍스트를 지정된 길이로 자릅니다.

    Args:
        text: 원본 텍스트
        max_length: 최대 길이
        suffix: 말줄임 표시 (기본값: "...")

    Returns:
        잘린 텍스트
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def parse_time_ago(time_str: str) -> Optional[int]:
    """
    '~시간 전', '~일 전' 형식의 문자열을 분 단위로 변환합니다.

    Args:
        time_str: 시간 문자열 (예: "3시간 전", "1일 전")

    Returns:
        분 단위 시간 (파싱 실패 시 None)
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
    마크다운 특수문자를 이스케이프합니다.

    Args:
        text: 원본 텍스트

    Returns:
        이스케이프된 텍스트
    """
    special_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!', '|']

    for char in special_chars:
        text = text.replace(char, '\\' + char)

    return text
