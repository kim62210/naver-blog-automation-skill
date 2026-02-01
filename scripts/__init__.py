"""
네이버 블로그 자동화 스크립트 패키지

이 패키지는 네이버 블로그 글 작성을 자동화하기 위한 유틸리티를 제공합니다:
- shared_types: 공유 타입 정의 (모든 데이터클래스)
- config: 설정 파일 로드
- utils: 공통 유틸리티
- validator: 글자수 검증
- setup: 프로젝트 디렉토리 초기화
- collector: 이미지 수집
- writer: HTML/MD 생성
- gemini_image: Gemini API 이미지 생성
- prompt_converter: 프롬프트 변환
- text_overlay: SVG 텍스트 오버레이
- image_pipeline: 통합 이미지 생성 파이프라인
"""

__version__ = "2.1.0"
__all__ = [
    # Types (import from shared_types)
    "shared_types",
    # Modules
    "config",
    "utils",
    "validator",
    "setup",
    "collector",
    "writer",
    "gemini_image",
    "prompt_converter",
    "text_overlay",
    "image_pipeline",
]

# Convenience exports for commonly used types
from .shared_types import (
    ImageResult,
    BatchResult,
    ValidationResult,
    WatermarkConfig,
    TextStyleConfig,
    TextElement,
    CollectionResult,
    ImageInfo,
    PipelineResult,
)
