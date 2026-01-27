"""
설정 파일 로더

config.yaml 파일을 로드하고 검증하며, 기본값을 병합합니다.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


# 기본 설정값
DEFAULT_CONFIG = {
    "app": {
        "name": "search-blogging",
        "version": "2.0.0",
    },
    "writing": {
        "char_count": 1850,
        "char_tolerance": 50,
        "min_chars": 1800,
        "max_chars": 1900,
    },
    "images": {
        "default_count": 5,
        "min_count": 3,
        "max_count": 10,
        "download_timeout": 30,
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    },
    "tags": {
        "count": 8,
        "max_count": 10,
    },
    "output": {
        "base_dir": "./경제 블로그",
        "date_format": "%Y-%m-%d",
        "encoding": "utf-8",
    },
}


def find_config_file(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    config.yaml 파일을 찾습니다.

    Args:
        start_path: 검색 시작 경로 (없으면 현재 디렉토리)

    Returns:
        config.yaml 파일 경로 (없으면 None)
    """
    if start_path is None:
        start_path = Path.cwd()

    # 현재 디렉토리에서 시작하여 상위로 탐색
    current = Path(start_path).resolve()

    for _ in range(5):  # 최대 5레벨까지 탐색
        config_path = current / "config.yaml"
        if config_path.exists():
            return config_path

        parent = current.parent
        if parent == current:
            break
        current = parent

    return None


def deep_merge(base: Dict, override: Dict) -> Dict:
    """
    두 딕셔너리를 깊게 병합합니다.

    Args:
        base: 기본 딕셔너리
        override: 덮어쓸 딕셔너리

    Returns:
        병합된 딕셔너리
    """
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    설정 파일을 로드합니다.

    Args:
        config_path: 설정 파일 경로 (없으면 자동 탐색)

    Returns:
        설정 딕셔너리

    Raises:
        FileNotFoundError: 설정 파일을 찾을 수 없을 때
        yaml.YAMLError: YAML 파싱 오류 시
    """
    if config_path is None:
        config_path = find_config_file()

    if config_path is None or not config_path.exists():
        print(f"⚠️ config.yaml을 찾을 수 없습니다. 기본값을 사용합니다.")
        return DEFAULT_CONFIG.copy()

    with open(config_path, "r", encoding="utf-8") as f:
        user_config = yaml.safe_load(f) or {}

    # 기본값과 사용자 설정 병합
    config = deep_merge(DEFAULT_CONFIG, user_config)

    # 환경변수 오버라이드
    config = apply_env_overrides(config)

    return config


def apply_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    환경변수로 설정을 오버라이드합니다.

    지원하는 환경변수:
    - BLOG_CHAR_COUNT: 목표 글자수
    - BLOG_IMAGE_COUNT: 기본 이미지 수
    - BLOG_OUTPUT_DIR: 출력 디렉토리

    Args:
        config: 설정 딕셔너리

    Returns:
        환경변수가 적용된 설정
    """
    env_mappings = {
        "BLOG_CHAR_COUNT": ("writing", "char_count", int),
        "BLOG_IMAGE_COUNT": ("images", "default_count", int),
        "BLOG_OUTPUT_DIR": ("output", "base_dir", str),
        "BLOG_TAG_COUNT": ("tags", "count", int),
    }

    for env_var, (section, key, type_fn) in env_mappings.items():
        value = os.environ.get(env_var)
        if value is not None:
            try:
                config[section][key] = type_fn(value)
            except (ValueError, KeyError):
                pass

    return config


def get_config_value(config: Dict, *keys: str, default: Any = None) -> Any:
    """
    중첩된 설정값을 안전하게 가져옵니다.

    Args:
        config: 설정 딕셔너리
        *keys: 키 경로
        default: 기본값

    Returns:
        설정값 또는 기본값

    Example:
        >>> get_config_value(config, "writing", "char_count", default=1850)
        1850
    """
    current = config

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current


def validate_config(config: Dict[str, Any]) -> list:
    """
    설정 파일의 유효성을 검증합니다.

    Args:
        config: 설정 딕셔너리

    Returns:
        오류 메시지 목록 (비어있으면 유효)
    """
    errors = []

    # 글자수 범위 검증
    min_chars = get_config_value(config, "writing", "min_chars", default=1800)
    max_chars = get_config_value(config, "writing", "max_chars", default=1900)
    char_count = get_config_value(config, "writing", "char_count", default=1850)

    if not (min_chars <= char_count <= max_chars):
        errors.append(f"char_count({char_count})가 범위({min_chars}~{max_chars}) 밖입니다.")

    # 이미지 수 범위 검증
    min_images = get_config_value(config, "images", "min_count", default=3)
    max_images = get_config_value(config, "images", "max_count", default=10)
    default_images = get_config_value(config, "images", "default_count", default=5)

    if not (min_images <= default_images <= max_images):
        errors.append(f"default_count({default_images})가 범위({min_images}~{max_images}) 밖입니다.")

    return errors


# 편의를 위한 싱글톤 인스턴스
_config_instance: Optional[Dict[str, Any]] = None


def get_config() -> Dict[str, Any]:
    """
    설정 싱글톤 인스턴스를 반환합니다.

    Returns:
        설정 딕셔너리
    """
    global _config_instance

    if _config_instance is None:
        _config_instance = load_config()

    return _config_instance


def reload_config() -> Dict[str, Any]:
    """
    설정을 다시 로드합니다.

    Returns:
        새로 로드된 설정 딕셔너리
    """
    global _config_instance
    _config_instance = load_config()
    return _config_instance
