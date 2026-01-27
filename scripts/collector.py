"""
이미지 수집 모듈

URL에서 이미지를 다운로드하고, 파일명을 생성하며, 메타데이터를 추출합니다.
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


@dataclass
class ImageInfo:
    """이미지 정보"""
    url: str                         # 원본 URL
    source_url: str                  # 출처 페이지 URL
    source_name: str                 # 출처명 (뉴스/블로그/검색)
    description: str                 # 설명
    image_type: str                  # 유형 (인포그래픽/표/일러스트/사진)
    filename: Optional[str] = None   # 저장된 파일명
    local_path: Optional[Path] = None  # 로컬 저장 경로
    downloaded: bool = False         # 다운로드 성공 여부
    error: Optional[str] = None      # 오류 메시지


@dataclass
class CollectionResult:
    """수집 결과"""
    total: int                       # 총 수집 시도 수
    success: int                     # 성공 수
    failed: int                      # 실패 수
    images: List[ImageInfo] = field(default_factory=list)  # 이미지 목록


def download_image(
    url: str,
    save_path: Path,
    timeout: int = 30,
    user_agent: Optional[str] = None
) -> bool:
    """
    이미지를 다운로드합니다.

    Args:
        url: 이미지 URL
        save_path: 저장 경로
        timeout: 타임아웃 (초)
        user_agent: User-Agent 헤더

    Returns:
        성공 여부
    """
    config = get_config()

    if user_agent is None:
        user_agent = get_config_value(
            config, "images", "user_agent",
            default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )

    try:
        request = urllib.request.Request(url)
        request.add_header("User-Agent", user_agent)
        request.add_header("Accept", "image/*")

        with urllib.request.urlopen(request, timeout=timeout) as response:
            content = response.read()

            # 최소 크기 확인 (100 bytes 이상)
            if len(content) < 100:
                return False

            save_path.parent.mkdir(parents=True, exist_ok=True)

            with open(save_path, "wb") as f:
                f.write(content)

            return True

    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        return False
    except Exception as e:
        return False


def collect_images(
    images: List[Dict[str, str]],
    output_dir: Path,
    config: Optional[Dict] = None
) -> CollectionResult:
    """
    여러 이미지를 수집합니다.

    Args:
        images: 이미지 정보 리스트 [{"url", "source_url", "source_name", "description", "type"}]
        output_dir: 출력 디렉토리
        config: 설정 딕셔너리

    Returns:
        CollectionResult 객체
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

        # 파일 확장자 추출
        extension = extract_extension_from_url(url)

        # 파일명 생성
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

        # 다운로드 시도
        success = download_image(url, save_path, timeout=timeout)

        if success:
            image_info.downloaded = True
            image_info.local_path = save_path
            result.success += 1
        else:
            image_info.downloaded = False
            image_info.error = "다운로드 실패"
            result.failed += 1

        result.images.append(image_info)

    return result


def validate_image_url(url: str) -> bool:
    """
    이미지 URL의 유효성을 검사합니다.

    Args:
        url: 이미지 URL

    Returns:
        유효 여부
    """
    if not url:
        return False

    try:
        parsed = urlparse(url)

        # 스킴 확인
        if parsed.scheme not in ("http", "https"):
            return False

        # 호스트 확인
        if not parsed.netloc:
            return False

        # 이미지 확장자 확인 (선택적)
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp')
        path_lower = parsed.path.lower()

        # 확장자가 있으면 이미지 확장자인지 확인
        if '.' in parsed.path:
            return any(path_lower.endswith(ext) for ext in image_extensions)

        # 확장자가 없으면 일단 허용 (CDN 등)
        return True

    except Exception:
        return False


def generate_image_metadata(images: List[ImageInfo]) -> List[Dict[str, Any]]:
    """
    이미지 목록에서 메타데이터를 생성합니다.

    Args:
        images: ImageInfo 리스트

    Returns:
        메타데이터 딕셔너리 리스트
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
    수집 결과를 메타데이터 파일에 저장합니다.

    Args:
        result: CollectionResult 객체
        project_path: 프로젝트 디렉토리 경로
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
    수집 결과 보고서를 출력합니다.

    Args:
        result: CollectionResult 객체
    """
    print("=" * 50)
    print("📷 이미지 수집 결과")
    print("=" * 50)
    print(f"총 시도: {result.total}건")
    print(f"성공: {result.success}건")
    print(f"실패: {result.failed}건")
    print("-" * 50)

    if result.success > 0:
        print("\n✅ 다운로드 완료:")
        for img in result.images:
            if img.downloaded:
                print(f"  - {img.filename}")
                print(f"    └ {img.description} ({img.image_type})")

    if result.failed > 0:
        print("\n❌ 다운로드 실패 (URL만 기록):")
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
    검색 결과에서 이미지 리스트를 생성합니다.

    Args:
        search_results: 검색 결과 리스트
        source_name: 출처명

    Returns:
        이미지 정보 리스트
    """
    images = []

    for result in search_results:
        # 이미지 URL 추출 (다양한 필드명 지원)
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
    # 테스트
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
