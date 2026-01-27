"""
프로젝트 초기화 모듈

출력 디렉토리 자동 생성, 메타데이터 초기화 등을 담당합니다.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any

from .config import get_config, get_config_value
from .utils import normalize_filename, get_today_date


def create_project_structure(
    topic: str,
    base_dir: Optional[str] = None,
    date: Optional[str] = None,
    config: Optional[Dict] = None
) -> Path:
    """
    블로그 글 작성을 위한 프로젝트 디렉토리 구조를 생성합니다.

    구조:
    ./경제 블로그/YYYY-MM-DD/주제명/
    ├── images/
    └── .metadata.json

    Args:
        topic: 주제명
        base_dir: 기본 디렉토리 (없으면 설정에서 로드)
        date: 날짜 (없으면 오늘 날짜)
        config: 설정 딕셔너리

    Returns:
        생성된 프로젝트 디렉토리 경로
    """
    if config is None:
        config = get_config()

    if base_dir is None:
        base_dir = get_config_value(config, "output", "base_dir", default="./경제 블로그")

    if date is None:
        date_format = get_config_value(config, "output", "date_format", default="%Y-%m-%d")
        date = get_today_date(date_format)

    # 주제명 정규화
    normalized_topic = normalize_filename(topic)

    # 프로젝트 경로 생성
    project_path = Path(base_dir) / date / normalized_topic

    # 디렉토리 생성
    project_path.mkdir(parents=True, exist_ok=True)

    # 하위 디렉토리 생성
    subdirs = get_config_value(config, "output", "subdirs", default=["images"])
    for subdir in subdirs:
        (project_path / subdir).mkdir(exist_ok=True)

    # 메타데이터 파일 생성
    create_metadata_file(project_path, topic, config)

    return project_path


def create_metadata_file(
    project_path: Path,
    topic: str,
    config: Optional[Dict] = None
) -> Path:
    """
    프로젝트 메타데이터 파일을 생성합니다.

    Args:
        project_path: 프로젝트 디렉토리 경로
        topic: 주제명
        config: 설정 딕셔너리

    Returns:
        메타데이터 파일 경로
    """
    if config is None:
        config = get_config()

    metadata = {
        "topic": topic,
        "created_at": datetime.now().isoformat(),
        "status": "initialized",
        "config": {
            "char_count": get_config_value(config, "writing", "char_count"),
            "image_count": get_config_value(config, "images", "default_count"),
            "tag_count": get_config_value(config, "tags", "count"),
        },
        "files": {
            "html": None,
            "image_guide": None,
            "references": None,
        },
        "images": [],
        "sources": [],
    }

    metadata_path = project_path / ".metadata.json"

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return metadata_path


def update_metadata(
    project_path: Path,
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    메타데이터 파일을 업데이트합니다.

    Args:
        project_path: 프로젝트 디렉토리 경로
        updates: 업데이트할 내용

    Returns:
        업데이트된 메타데이터
    """
    metadata_path = project_path / ".metadata.json"

    if metadata_path.exists():
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    else:
        metadata = {}

    # 깊은 업데이트
    def deep_update(base: dict, updates: dict):
        for key, value in updates.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                deep_update(base[key], value)
            else:
                base[key] = value

    deep_update(metadata, updates)
    metadata["updated_at"] = datetime.now().isoformat()

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return metadata


def load_metadata(project_path: Path) -> Optional[Dict[str, Any]]:
    """
    메타데이터 파일을 로드합니다.

    Args:
        project_path: 프로젝트 디렉토리 경로

    Returns:
        메타데이터 딕셔너리 (없으면 None)
    """
    metadata_path = project_path / ".metadata.json"

    if not metadata_path.exists():
        return None

    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_existing_project(
    topic: str,
    base_dir: Optional[str] = None,
    date: Optional[str] = None,
    config: Optional[Dict] = None
) -> Optional[Path]:
    """
    기존 프로젝트 디렉토리를 찾습니다.

    Args:
        topic: 주제명
        base_dir: 기본 디렉토리
        date: 날짜
        config: 설정 딕셔너리

    Returns:
        프로젝트 경로 (없으면 None)
    """
    if config is None:
        config = get_config()

    if base_dir is None:
        base_dir = get_config_value(config, "output", "base_dir", default="./경제 블로그")

    if date is None:
        date = get_today_date()

    normalized_topic = normalize_filename(topic)
    project_path = Path(base_dir) / date / normalized_topic

    if project_path.exists():
        return project_path

    return None


def list_projects(
    base_dir: Optional[str] = None,
    date: Optional[str] = None,
    config: Optional[Dict] = None
) -> list:
    """
    프로젝트 목록을 반환합니다.

    Args:
        base_dir: 기본 디렉토리
        date: 특정 날짜 (없으면 모든 날짜)
        config: 설정 딕셔너리

    Returns:
        프로젝트 정보 리스트
    """
    if config is None:
        config = get_config()

    if base_dir is None:
        base_dir = get_config_value(config, "output", "base_dir", default="./경제 블로그")

    base_path = Path(base_dir)

    if not base_path.exists():
        return []

    projects = []

    if date:
        date_dirs = [base_path / date] if (base_path / date).exists() else []
    else:
        date_dirs = [d for d in base_path.iterdir() if d.is_dir()]

    for date_dir in sorted(date_dirs, reverse=True):
        for project_dir in date_dir.iterdir():
            if project_dir.is_dir():
                metadata = load_metadata(project_dir)
                projects.append({
                    "path": project_dir,
                    "date": date_dir.name,
                    "topic": project_dir.name,
                    "metadata": metadata,
                })

    return projects


def print_project_info(project_path: Path) -> None:
    """
    프로젝트 정보를 출력합니다.

    Args:
        project_path: 프로젝트 디렉토리 경로
    """
    metadata = load_metadata(project_path)

    print("=" * 50)
    print(f"📁 프로젝트: {project_path}")
    print("=" * 50)

    if metadata:
        print(f"주제: {metadata.get('topic', 'N/A')}")
        print(f"생성일: {metadata.get('created_at', 'N/A')}")
        print(f"상태: {metadata.get('status', 'N/A')}")

        if metadata.get("files"):
            print("\n📄 파일:")
            for file_type, file_path in metadata["files"].items():
                status = "✅" if file_path else "⬜"
                print(f"  {status} {file_type}: {file_path or '미생성'}")

        if metadata.get("images"):
            print(f"\n🖼️ 이미지: {len(metadata['images'])}개")
    else:
        print("메타데이터 없음")

    print("=" * 50)


if __name__ == "__main__":
    # 테스트
    test_topic = "2026년 육아휴직 변경사항"

    print("프로젝트 구조 생성 테스트")
    project_path = create_project_structure(test_topic)
    print(f"생성된 경로: {project_path}")

    print_project_info(project_path)
