"""
Gemini 이미지 생성 API 연동 모듈

Google Gemini API를 사용하여 블로그 이미지를 자동 생성합니다.
Gemini 2.5 Flash를 기본으로 사용하며, 한도 초과 시 Imagen 4로 폴백합니다.
"""

import asyncio
import base64
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .config import get_config, get_config_value


# API 설정 상수
DEFAULT_MODEL = "gemini-2.0-flash-exp"
FALLBACK_MODEL = "imagen-3.0-generate-002"
DEFAULT_SIZE = "1024x1024"
DEFAULT_TIMEOUT = 60
DEFAULT_RETRY_COUNT = 3
RATE_LIMIT_DELAY = 4.0  # 분당 15회 제한 고려


@dataclass
class ImageResult:
    """이미지 생성 결과를 담는 데이터 클래스"""

    success: bool
    file_path: Optional[str] = None
    prompt: str = ""
    model_used: str = ""
    error_message: Optional[str] = None
    generation_time: float = 0.0

    def __str__(self) -> str:
        if self.success:
            return f"✅ 생성 완료: {self.file_path} ({self.model_used})"
        return f"❌ 생성 실패: {self.error_message}"


@dataclass
class BatchResult:
    """배치 이미지 생성 결과"""

    total: int = 0
    success_count: int = 0
    failed_count: int = 0
    results: List[ImageResult] = field(default_factory=list)
    total_time: float = 0.0

    @property
    def success_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return (self.success_count / self.total) * 100

    def summary(self) -> str:
        return (
            f"📊 배치 생성 결과: {self.success_count}/{self.total} 성공 "
            f"({self.success_rate:.1f}%), 소요시간: {self.total_time:.1f}초"
        )


class GeminiImageGenerator:
    """
    Gemini API를 사용한 이미지 생성기

    사용 예시:
        generator = GeminiImageGenerator()
        result = await generator.generate_image(
            prompt="Blog thumbnail, modern design...",
            save_path="./images/01_thumbnail.png"
        )
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        primary_model: Optional[str] = None,
        fallback_model: Optional[str] = None,
    ):
        """
        GeminiImageGenerator 초기화

        Args:
            api_key: Google API 키 (없으면 환경변수에서 로드)
            primary_model: 기본 모델 (기본값: gemini-2.0-flash-exp)
            fallback_model: 폴백 모델 (기본값: imagen-3.0-generate-002)
        """
        self.api_key = api_key or self._load_api_key()
        self.primary_model = primary_model or self._get_config_model("primary") or DEFAULT_MODEL
        self.fallback_model = fallback_model or self._get_config_model("fallback") or FALLBACK_MODEL
        self.timeout = self._get_config_timeout() or DEFAULT_TIMEOUT
        self.retry_count = self._get_config_retry_count() or DEFAULT_RETRY_COUNT

        # 클라이언트 초기화 (lazy loading)
        self._client = None

    def _load_api_key(self) -> str:
        """환경변수에서 API 키를 로드합니다"""
        api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "Google API 키가 설정되지 않았습니다. "
                "환경변수 GOOGLE_API_KEY 또는 GEMINI_API_KEY를 설정하세요."
            )

        return api_key

    def _get_config_model(self, model_type: str) -> Optional[str]:
        """config.yaml에서 모델 설정을 가져옵니다"""
        config = get_config()
        return get_config_value(config, "gemini", "models", model_type)

    def _get_config_timeout(self) -> Optional[int]:
        """config.yaml에서 타임아웃 설정을 가져옵니다"""
        config = get_config()
        return get_config_value(config, "gemini", "timeout")

    def _get_config_retry_count(self) -> Optional[int]:
        """config.yaml에서 재시도 횟수 설정을 가져옵니다"""
        config = get_config()
        return get_config_value(config, "gemini", "retry_count")

    def _init_client(self):
        """Google Generative AI 클라이언트를 초기화합니다"""
        if self._client is not None:
            return

        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._client = genai
        except ImportError:
            raise ImportError(
                "google-generativeai 패키지가 설치되지 않았습니다. "
                "pip install google-generativeai 로 설치하세요."
            )

    async def generate_image(
        self,
        prompt: str,
        save_path: Optional[str] = None,
        size: str = DEFAULT_SIZE,
        use_fallback: bool = True,
    ) -> ImageResult:
        """
        단일 이미지를 생성합니다

        Args:
            prompt: 이미지 생성 프롬프트 (영문 권장)
            save_path: 저장 경로 (없으면 임시 파일 생성)
            size: 이미지 크기 (기본값: 1024x1024)
            use_fallback: 실패 시 폴백 모델 사용 여부

        Returns:
            ImageResult: 생성 결과
        """
        start_time = datetime.now()

        # 기본 모델로 시도
        result = await self._generate_with_model(
            prompt=prompt,
            save_path=save_path,
            size=size,
            model=self.primary_model,
        )

        # 실패 시 폴백 모델 시도
        if not result.success and use_fallback and self._should_fallback(result.error_message):
            print(f"⚠️ {self.primary_model} 실패, {self.fallback_model}로 재시도...")
            await asyncio.sleep(RATE_LIMIT_DELAY)

            result = await self._generate_with_model(
                prompt=prompt,
                save_path=save_path,
                size=size,
                model=self.fallback_model,
            )

        result.generation_time = (datetime.now() - start_time).total_seconds()
        return result

    def _should_fallback(self, error_message: Optional[str]) -> bool:
        """폴백 시도 여부를 결정합니다"""
        if not error_message:
            return True

        # 폴백 트리거 조건
        fallback_triggers = ["429", "QUOTA_EXCEEDED", "RATE_LIMIT", "ResourceExhausted"]
        return any(trigger in error_message for trigger in fallback_triggers)

    async def _generate_with_model(
        self,
        prompt: str,
        save_path: Optional[str],
        size: str,
        model: str,
    ) -> ImageResult:
        """특정 모델로 이미지를 생성합니다"""
        self._init_client()

        for attempt in range(self.retry_count):
            try:
                # Gemini 모델로 이미지 생성
                if model.startswith("gemini"):
                    return await self._generate_with_gemini(prompt, save_path, model)
                else:
                    return await self._generate_with_imagen(prompt, save_path, size, model)

            except Exception as e:
                error_msg = str(e)

                # Rate limit 에러 시 대기 후 재시도
                if "429" in error_msg or "ResourceExhausted" in error_msg:
                    if attempt < self.retry_count - 1:
                        wait_time = RATE_LIMIT_DELAY * (attempt + 1)
                        print(f"⏳ Rate limit, {wait_time:.1f}초 대기 후 재시도...")
                        await asyncio.sleep(wait_time)
                        continue

                # 마지막 시도가 아니면 재시도
                if attempt < self.retry_count - 1:
                    await asyncio.sleep(1)
                    continue

                return ImageResult(
                    success=False,
                    prompt=prompt,
                    model_used=model,
                    error_message=error_msg,
                )

        return ImageResult(
            success=False,
            prompt=prompt,
            model_used=model,
            error_message="최대 재시도 횟수 초과",
        )

    async def _generate_with_gemini(
        self,
        prompt: str,
        save_path: Optional[str],
        model: str,
    ) -> ImageResult:
        """Gemini 모델로 이미지를 생성합니다"""
        try:
            # Gemini 2.0 Flash 모델 설정 (이미지 생성 지원)
            generation_config = {
                "response_modalities": ["image", "text"],
            }

            gemini_model = self._client.GenerativeModel(
                model_name=model,
                generation_config=generation_config,
            )

            # 이미지 생성 요청
            response = await asyncio.to_thread(
                gemini_model.generate_content,
                prompt,
            )

            # 응답에서 이미지 추출
            image_data = None
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data.mime_type.startswith("image/"):
                    image_data = part.inline_data.data
                    break

            if not image_data:
                return ImageResult(
                    success=False,
                    prompt=prompt,
                    model_used=model,
                    error_message="응답에서 이미지를 찾을 수 없습니다",
                )

            # 파일 저장
            final_path = self._save_image(image_data, save_path, "png")

            return ImageResult(
                success=True,
                file_path=str(final_path),
                prompt=prompt,
                model_used=model,
            )

        except Exception as e:
            raise e

    async def _generate_with_imagen(
        self,
        prompt: str,
        save_path: Optional[str],
        size: str,
        model: str,
    ) -> ImageResult:
        """Imagen 모델로 이미지를 생성합니다"""
        try:
            imagen_model = self._client.ImageGenerationModel(model_name=model)

            # 크기 파싱
            width, height = self._parse_size(size)

            # 이미지 생성
            response = await asyncio.to_thread(
                imagen_model.generate_images,
                prompt=prompt,
                number_of_images=1,
                aspect_ratio=self._get_aspect_ratio(width, height),
            )

            if not response.images:
                return ImageResult(
                    success=False,
                    prompt=prompt,
                    model_used=model,
                    error_message="이미지 생성 결과가 없습니다",
                )

            # 이미지 데이터 추출 및 저장
            image_data = response.images[0]._image_bytes
            final_path = self._save_image(image_data, save_path, "png")

            return ImageResult(
                success=True,
                file_path=str(final_path),
                prompt=prompt,
                model_used=model,
            )

        except Exception as e:
            raise e

    def _parse_size(self, size: str) -> Tuple[int, int]:
        """크기 문자열을 파싱합니다"""
        match = re.match(r"(\d+)x(\d+)", size)
        if match:
            return int(match.group(1)), int(match.group(2))
        return 1024, 1024

    def _get_aspect_ratio(self, width: int, height: int) -> str:
        """가로세로 비율을 반환합니다"""
        ratio = width / height

        if abs(ratio - 1.0) < 0.1:
            return "1:1"
        elif abs(ratio - 16/9) < 0.1:
            return "16:9"
        elif abs(ratio - 9/16) < 0.1:
            return "9:16"
        elif abs(ratio - 4/3) < 0.1:
            return "4:3"
        elif abs(ratio - 3/4) < 0.1:
            return "3:4"
        else:
            return "1:1"

    def _save_image(
        self,
        image_data: bytes,
        save_path: Optional[str],
        ext: str = "png",
    ) -> Path:
        """이미지를 파일로 저장합니다"""
        if save_path:
            path = Path(save_path)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = Path(f"generated_image_{timestamp}.{ext}")

        # 디렉토리 생성
        path.parent.mkdir(parents=True, exist_ok=True)

        # 파일 저장
        with open(path, "wb") as f:
            if isinstance(image_data, str):
                f.write(base64.b64decode(image_data))
            else:
                f.write(image_data)

        return path

    async def generate_batch(
        self,
        prompts: List[Dict[str, str]],
        output_dir: str,
        concurrent_limit: int = 2,
    ) -> BatchResult:
        """
        여러 이미지를 일괄 생성합니다

        Args:
            prompts: 프롬프트 목록 [{"prompt": "...", "filename": "..."}, ...]
            output_dir: 출력 디렉토리
            concurrent_limit: 동시 실행 제한 (분당 15회 제한 고려)

        Returns:
            BatchResult: 배치 생성 결과
        """
        start_time = datetime.now()
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results: List[ImageResult] = []
        semaphore = asyncio.Semaphore(concurrent_limit)

        async def generate_with_limit(item: Dict[str, str]) -> ImageResult:
            async with semaphore:
                prompt = item.get("prompt", "")
                filename = item.get("filename", f"image_{len(results):02d}.png")
                save_path = str(output_path / filename)

                result = await self.generate_image(prompt=prompt, save_path=save_path)

                # Rate limit 방지를 위한 딜레이
                await asyncio.sleep(RATE_LIMIT_DELAY)

                return result

        # 병렬 실행 (제한된 동시성)
        tasks = [generate_with_limit(item) for item in prompts]
        results = await asyncio.gather(*tasks)

        # 결과 집계
        success_count = sum(1 for r in results if r.success)
        total_time = (datetime.now() - start_time).total_seconds()

        return BatchResult(
            total=len(prompts),
            success_count=success_count,
            failed_count=len(prompts) - success_count,
            results=list(results),
            total_time=total_time,
        )


def create_generator(api_key: Optional[str] = None) -> GeminiImageGenerator:
    """
    GeminiImageGenerator 인스턴스를 생성하는 팩토리 함수

    Args:
        api_key: Google API 키 (선택)

    Returns:
        GeminiImageGenerator 인스턴스
    """
    return GeminiImageGenerator(api_key=api_key)


# 편의를 위한 동기 래퍼 함수들
def generate_image_sync(
    prompt: str,
    save_path: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ImageResult:
    """
    동기 방식으로 이미지를 생성합니다

    Args:
        prompt: 이미지 생성 프롬프트
        save_path: 저장 경로
        api_key: API 키 (선택)

    Returns:
        ImageResult: 생성 결과
    """
    generator = create_generator(api_key)
    return asyncio.run(generator.generate_image(prompt=prompt, save_path=save_path))


def generate_batch_sync(
    prompts: List[Dict[str, str]],
    output_dir: str,
    api_key: Optional[str] = None,
) -> BatchResult:
    """
    동기 방식으로 여러 이미지를 생성합니다

    Args:
        prompts: 프롬프트 목록
        output_dir: 출력 디렉토리
        api_key: API 키 (선택)

    Returns:
        BatchResult: 배치 생성 결과
    """
    generator = create_generator(api_key)
    return asyncio.run(generator.generate_batch(prompts=prompts, output_dir=output_dir))
