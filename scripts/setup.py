"""
Project initialization module

Handles automatic output directory creation, metadata initialization, etc.
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
    Create project directory structure for blog post writing.

    Structure:
    ./경제 블로그/YYYY-MM-DD/topic-name/
    ├── images/
    └── .metadata.json

    Args:
        topic: Topic name
        base_dir: Base directory (loads from config if not provided)
        date: Date (uses today's date if not provided)
        config: Configuration dictionary

    Returns:
        Created project directory path
    """
    if config is None:
        config = get_config()

    if base_dir is None:
        base_dir = get_config_value(config, "output", "base_dir", default="./경제 블로그")

    if date is None:
        date_format = get_config_value(config, "output", "date_format", default="%Y-%m-%d")
        date = get_today_date(date_format)

    # Normalize topic name
    normalized_topic = normalize_filename(topic)

    # Create project path
    project_path = Path(base_dir) / date / normalized_topic

    # Create directory
    project_path.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    subdirs = get_config_value(config, "output", "subdirs", default=["images"])
    for subdir in subdirs:
        (project_path / subdir).mkdir(exist_ok=True)

    # Create metadata file
    create_metadata_file(project_path, topic, config)

    return project_path


def create_metadata_file(
    project_path: Path,
    topic: str,
    config: Optional[Dict] = None
) -> Path:
    """
    Create project metadata file.

    Args:
        project_path: Project directory path
        topic: Topic name
        config: Configuration dictionary

    Returns:
        Metadata file path
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
    Update metadata file.

    Args:
        project_path: Project directory path
        updates: Content to update

    Returns:
        Updated metadata
    """
    metadata_path = project_path / ".metadata.json"

    if metadata_path.exists():
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    else:
        metadata = {}

    # Deep update
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
    Load metadata file.

    Args:
        project_path: Project directory path

    Returns:
        Metadata dictionary (None if not found)
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
    Find existing project directory.

    Args:
        topic: Topic name
        base_dir: Base directory
        date: Date
        config: Configuration dictionary

    Returns:
        Project path (None if not found)
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
    Return list of projects.

    Args:
        base_dir: Base directory
        date: Specific date (all dates if not provided)
        config: Configuration dictionary

    Returns:
        Project info list
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
    Print project information.

    Args:
        project_path: Project directory path
    """
    metadata = load_metadata(project_path)

    print("=" * 50)
    print(f"📁 Project: {project_path}")
    print("=" * 50)

    if metadata:
        print(f"Topic: {metadata.get('topic', 'N/A')}")
        print(f"Created: {metadata.get('created_at', 'N/A')}")
        print(f"Status: {metadata.get('status', 'N/A')}")

        if metadata.get("files"):
            print("\n📄 Files:")
            for file_type, file_path in metadata["files"].items():
                status = "✅" if file_path else "⬜"
                print(f"  {status} {file_type}: {file_path or 'Not created'}")

        if metadata.get("images"):
            print(f"\n🖼️ Images: {len(metadata['images'])}")
    else:
        print("No metadata")

    print("=" * 50)


if __name__ == "__main__":
    # Test
    test_topic = "2026년 육아휴직 변경사항"

    print("Project structure creation test")
    project_path = create_project_structure(test_topic)
    print(f"Created path: {project_path}")

    print_project_info(project_path)
