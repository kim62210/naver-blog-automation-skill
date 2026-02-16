"""
Image collection module

Downloads images from URLs, generates filenames, and extracts metadata.
"""

import hashlib
import mimetypes
import re
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse

from .config import get_config, get_config_value
from .utils import format_image_filename, extract_extension_from_url
from .setup import update_metadata


_DEFAULT_BROWSER_HEADERS = {
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Connection": "keep-alive",
}


def build_crawl_headers(
    url: str,
    source_url: str = "",
    user_agent: Optional[str] = None,
) -> Dict[str, str]:
    """Create browser-like headers for URL fetching."""
    config = get_config()

    headers = dict(_DEFAULT_BROWSER_HEADERS)
    if user_agent is None:
        user_agent = get_config_value(
            config, "images", "user_agent",
            default=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
        )

    headers["User-Agent"] = user_agent

    if source_url:
        headers["Referer"] = source_url
        try:
            parsed_source = urlparse(source_url)
            if parsed_source.scheme and parsed_source.netloc:
                headers["Origin"] = f"{parsed_source.scheme}://{parsed_source.netloc}"
        except Exception:
            headers["Origin"] = "https://www.google.com"
    else:
        headers["Referer"] = "https://www.google.com/"
        headers["Origin"] = "https://www.google.com"

    parsed = urlparse(url)
    if parsed.hostname:
        headers["Host"] = parsed.hostname

    return headers


@dataclass
class ImageInfo:
    """Image information"""
    url: str                         # Original URL
    source_url: str                  # Source page URL
    source_name: str                 # Source name (뉴스/블로그/검색)
    description: str                 # Description
    image_type: str                  # Type (인포그래픽/표/일러스트/사진)
    filename: Optional[str] = None   # Saved filename
    local_path: Optional[Path] = None  # Local storage path
    downloaded: bool = False         # Download success status
    error: Optional[str] = None      # Error message


@dataclass
class CollectionResult:
    """Collection result"""
    total: int                       # Total collection attempts
    success: int                     # Success count
    failed: int                      # Failure count
    images: List[ImageInfo] = field(default_factory=list)  # Image list


def download_image(
    url: str,
    save_path: Path,
    timeout: int = 30,
    source_url: str = "",
    user_agent: Optional[str] = None
) -> bool:
    """
    Download an image.

    Args:
        url: Image URL
        save_path: Save path
        timeout: Timeout (seconds)
        user_agent: User-Agent header

    Returns:
        Success status
    """
    config = get_config()

    if user_agent is None:
        user_agent = get_config_value(
            config, "images", "user_agent",
            default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )

    try:
        request = urllib.request.Request(url, headers=build_crawl_headers(url, source_url, user_agent))

        with urllib.request.urlopen(request, timeout=timeout) as response:
            content = response.read()

            # Check minimum size (100 bytes or more)
            if len(content) < 100:
                return False

            save_path.parent.mkdir(parents=True, exist_ok=True)

            with open(save_path, "wb") as f:
                f.write(content)

            return True

    except urllib.error.HTTPError as e:
        print(f"⚠️ HTTP error downloading {url[:50]}...: {e.code} {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"⚠️ URL error downloading {url[:50]}...: {e.reason}")
        return False
    except TimeoutError:
        print(f"⚠️ Timeout downloading {url[:50]}...")
        return False
    except Exception as e:
        print(f"⚠️ Error downloading {url[:50]}...: {type(e).__name__}: {e}")
        return False


def collect_images(
    images: List[Dict[str, str]],
    output_dir: Path,
    config: Optional[Dict] = None
) -> CollectionResult:
    """
    Collect multiple images.

    Args:
        images: Image info list [{"url", "source_url", "source_name", "description", "type"}]
        output_dir: Output directory
        config: Configuration dictionary

    Returns:
        CollectionResult object
    """
    if config is None:
        config = get_config()

    timeout = get_config_value(config, "images", "download_timeout", default=30)
    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True)

    result = CollectionResult(total=len(images), success=0, failed=0)

    for idx, img_data in enumerate(images, 1):
        url = img_data.get("url", "")
        source_url = img_data.get("source_url", "")
        source_name = img_data.get("source_name", "검색")
        description = img_data.get("description", f"이미지{idx}")
        image_type = img_data.get("type", "기타")

        # Extract file extension
        extension = extract_extension_from_url(url)

        # Generate filename
        filename = format_image_filename(idx, source_name, description, extension)
        save_path = images_dir / filename

        image_info = ImageInfo(
            url=url,
            source_url=source_url,
            source_name=source_name,
            description=description,
            image_type=image_type,
            filename=filename,
        )

        # Attempt download with detailed error capture
        try:
            success = download_image(
                url,
                save_path,
                timeout=timeout,
                source_url=source_url,
                user_agent=None,
            )

            if success:
                image_info.downloaded = True
                image_info.local_path = save_path
                result.success += 1
            else:
                image_info.downloaded = False
                image_info.error = f"Download failed (file too small or network error)"
                result.failed += 1
        except Exception as e:
            image_info.downloaded = False
            image_info.error = f"{type(e).__name__}: {str(e)}"
            result.failed += 1

        result.images.append(image_info)

    return result


def validate_image_url(url: str) -> bool:
    """
    Validate image URL.

    Args:
        url: Image URL

    Returns:
        Validity status
    """
    if not url:
        return False

    try:
        parsed = urlparse(url)

        # Check scheme
        if parsed.scheme not in ("http", "https"):
            return False

        # Check host
        if not parsed.netloc:
            return False

        # Check image extension (optional)
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp')
        path_lower = parsed.path.lower()

        # If extension exists, verify it's an image extension
        if '.' in parsed.path:
            return any(path_lower.endswith(ext) for ext in image_extensions)

        # Allow if no extension (CDN, etc.)
        return True

    except Exception:
        return False


def generate_image_metadata(images: List[ImageInfo]) -> List[Dict[str, Any]]:
    """
    Generate metadata from image list.

    Args:
        images: ImageInfo list

    Returns:
        Metadata dictionary list
    """
    metadata = []

    for img in images:
        entry = {
            "filename": img.filename,
            "url": img.url,
            "source_url": img.source_url,
            "source_name": img.source_name,
            "description": img.description,
            "type": img.image_type,
            "downloaded": img.downloaded,
        }

        if img.local_path and img.downloaded:
            entry["local_path"] = str(img.local_path)
            entry["size"] = img.local_path.stat().st_size if img.local_path.exists() else 0

        if img.error:
            entry["error"] = img.error

        metadata.append(entry)

    return metadata


def save_collection_result(
    result: CollectionResult,
    project_path: Path
) -> None:
    """
    Save collection result to metadata file.

    Args:
        result: CollectionResult object
        project_path: Project directory path
    """
    metadata = generate_image_metadata(result.images)

    update_metadata(project_path, {
        "images": metadata,
        "collection_stats": {
            "total": result.total,
            "success": result.success,
            "failed": result.failed,
        }
    })


def print_collection_report(result: CollectionResult) -> None:
    """
    Print collection result report.

    Args:
        result: CollectionResult object
    """
    print("=" * 50)
    print("📷 Image Collection Result")
    print("=" * 50)
    print(f"Total attempts: {result.total}")
    print(f"Success: {result.success}")
    print(f"Failed: {result.failed}")
    print("-" * 50)

    if result.success > 0:
        print("\n✅ Downloads completed:")
        for img in result.images:
            if img.downloaded:
                print(f"  - {img.filename}")
                print(f"    └ {img.description} ({img.image_type})")

    if result.failed > 0:
        print("\n❌ Downloads failed (URL recorded):")
        for img in result.images:
            if not img.downloaded:
                print(f"  - {img.description}: {img.error}")
                print(f"    └ URL: {img.url[:50]}...")

    print("=" * 50)


def create_image_list_from_search_results(
    search_results: List[Dict[str, Any]],
    source_name: str
) -> List[Dict[str, str]]:
    """
    Create image list from search results.

    Args:
        search_results: Search result list
        source_name: Source name

    Returns:
        Image info list
    """
    images = []

    for result in search_results:
        # Extract image URL (support various field names)
        image_url = (
            result.get("image_url") or
            result.get("thumbnail") or
            result.get("og_image") or
            result.get("image")
        )

        if not image_url or not validate_image_url(image_url):
            continue

        images.append({
            "url": image_url,
            "source_url": result.get("url", ""),
            "source_name": source_name,
            "description": result.get("title", "")[:30],
            "type": result.get("image_type", "기타"),
        })

    return images


if __name__ == "__main__":
    # Test
    test_images = [
        {
            "url": "https://example.com/test.jpg",
            "source_url": "https://example.com",
            "source_name": "테스트",
            "description": "테스트 이미지",
            "type": "기타",
        }
    ]

    from pathlib import Path
    test_dir = Path("./test_output")

    result = collect_images(test_images, test_dir)
    print_collection_report(result)
