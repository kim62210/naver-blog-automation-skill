"""
Configuration file loader

Loads and validates config.yaml files, merging with default values.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


# Default configuration values
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
    Find config.yaml file.

    Args:
        start_path: Starting path for search (defaults to current directory)

    Returns:
        Path to config.yaml file (None if not found)
    """
    if start_path is None:
        start_path = Path.cwd()

    # Search upward from current directory
    current = Path(start_path).resolve()

    for _ in range(5):  # Search up to 5 levels
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
    Deep merge two dictionaries.

    Args:
        base: Base dictionary
        override: Dictionary to override with

    Returns:
        Merged dictionary
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
    Load configuration file.

    Args:
        config_path: Configuration file path (auto-search if not provided)

    Returns:
        Configuration dictionary

    Raises:
        FileNotFoundError: When configuration file cannot be found
        yaml.YAMLError: When YAML parsing fails
    """
    if config_path is None:
        config_path = find_config_file()

    if config_path is None or not config_path.exists():
        print(f"⚠️ config.yaml not found. Using default values.")
        return DEFAULT_CONFIG.copy()

    with open(config_path, "r", encoding="utf-8") as f:
        user_config = yaml.safe_load(f) or {}

    # Merge default and user configuration
    config = deep_merge(DEFAULT_CONFIG, user_config)

    # Apply environment variable overrides
    config = apply_env_overrides(config)

    return config


def apply_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Override configuration with environment variables.

    Supported environment variables:
    - BLOG_CHAR_COUNT: Target character count
    - BLOG_IMAGE_COUNT: Default image count
    - BLOG_OUTPUT_DIR: Output directory

    Args:
        config: Configuration dictionary

    Returns:
        Configuration with environment variables applied
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
    Safely retrieve nested configuration values.

    Args:
        config: Configuration dictionary
        *keys: Key path
        default: Default value

    Returns:
        Configuration value or default

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
    Validate configuration file.

    Args:
        config: Configuration dictionary

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Validate character count range
    min_chars = get_config_value(config, "writing", "min_chars", default=1800)
    max_chars = get_config_value(config, "writing", "max_chars", default=1900)
    char_count = get_config_value(config, "writing", "char_count", default=1850)

    if not (min_chars <= char_count <= max_chars):
        errors.append(f"char_count({char_count}) is outside range ({min_chars}~{max_chars}).")

    # Validate image count range
    min_images = get_config_value(config, "images", "min_count", default=3)
    max_images = get_config_value(config, "images", "max_count", default=10)
    default_images = get_config_value(config, "images", "default_count", default=5)

    if not (min_images <= default_images <= max_images):
        errors.append(f"default_count({default_images}) is outside range ({min_images}~{max_images}).")

    return errors


# Singleton instance for convenience
_config_instance: Optional[Dict[str, Any]] = None


def get_config() -> Dict[str, Any]:
    """
    Return configuration singleton instance.

    Returns:
        Configuration dictionary
    """
    global _config_instance

    if _config_instance is None:
        _config_instance = load_config()

    return _config_instance


def reload_config() -> Dict[str, Any]:
    """
    Reload configuration.

    Returns:
        Newly loaded configuration dictionary
    """
    global _config_instance
    _config_instance = load_config()
    return _config_instance
