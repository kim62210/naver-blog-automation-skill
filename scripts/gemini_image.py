"""
Gemini Image Generation API Integration Module

Generates blog images using Google Gemini API (gemini-3-pro-image-preview).
Uses the new google-genai SDK with text overlay and watermark support.
"""

import asyncio
import base64
import os
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .config import get_config, get_config_value

if TYPE_CHECKING:
    from .prompt_converter import WatermarkConfig

DEFAULT_MODEL = "gemini-3-pro-image-preview"
DEFAULT_SIZE = "1024x1024"
DEFAULT_TIMEOUT = 60
DEFAULT_RETRY_COUNT = 3
DEFAULT_RATE_LIMIT_DELAY = 6.0  # 60s / 10 requests


def _get_rate_limit_delay() -> float:
    """Get rate limit delay from config, falling back to default."""
    try:
        config = get_config()
        return float(get_config_value(config, "gemini", "rate_limit", "delay_between_requests") or DEFAULT_RATE_LIMIT_DELAY)
    except Exception:
        return DEFAULT_RATE_LIMIT_DELAY


@dataclass
class ImageResult:
    """Image generation result."""
    success: bool
    file_path: Optional[str] = None
    prompt: str = ""
    model_used: str = ""
    error_message: Optional[str] = None
    generation_time: float = 0.0

    def __str__(self) -> str:
        if self.success:
            return f"Generation complete: {self.file_path} ({self.model_used})"
        return f"Generation failed: {self.error_message}"


@dataclass
class BatchResult:
    """Batch image generation result."""
    total: int = 0
    success_count: int = 0
    failed_count: int = 0
    results: List[ImageResult] = field(default_factory=list)
    total_time: float = 0.0

    @property
    def success_rate(self) -> float:
        return (self.success_count / self.total * 100) if self.total else 0.0

    def summary(self) -> str:
        return (
            f"Batch result: {self.success_count}/{self.total} succeeded "
            f"({self.success_rate:.1f}%), {self.total_time:.1f}s"
        )


class GeminiImageGenerator:
    """Image generator using Gemini API (google-genai SDK)."""

    def __init__(self, api_key: Optional[str] = None, primary_model: Optional[str] = None):
        self.api_key = api_key or self._load_api_key()
        self.primary_model = primary_model or self._get_config_value("gemini", "models", "primary") or DEFAULT_MODEL
        self.timeout = self._get_config_value("gemini", "timeout") or DEFAULT_TIMEOUT
        self.retry_count = self._get_config_value("gemini", "retry_count") or DEFAULT_RETRY_COUNT
        self._client = None

    def _load_api_key(self) -> str:
        api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable.")
        return api_key

    @staticmethod
    def _get_config_value(*keys) -> Any:
        config = get_config()
        return get_config_value(config, *keys)

    def _init_client(self):
        if self._client is not None:
            return
        try:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            self._genai_types = None
            try:
                from google.genai import types
                self._genai_types = types
            except ImportError:
                pass
        except ImportError:
            raise ImportError("google-genai not installed. Run: pip install google-genai")

    async def generate_image(self, prompt: str, save_path: Optional[str] = None,
                             size: str = DEFAULT_SIZE, **kwargs) -> ImageResult:
        """Generate a single image using the primary model."""
        start_time = datetime.now()
        result = await self._generate_with_retry(prompt, save_path, self.primary_model)
        result.generation_time = (datetime.now() - start_time).total_seconds()
        return result

    async def _generate_with_retry(self, prompt: str, save_path: Optional[str],
                                   model: str) -> ImageResult:
        """Generate image with retry logic for rate limits and transient errors."""
        self._init_client()
        errors: List[str] = []

        for attempt in range(self.retry_count):
            try:
                return await self._call_gemini_api(prompt, save_path, model)
            except Exception as e:
                error_msg = f"Attempt {attempt + 1}: {type(e).__name__}: {e}"
                errors.append(error_msg)
                print(f"Warning: {model} failed - {error_msg}")

                if attempt >= self.retry_count - 1:
                    break

                if "429" in str(e) or "ResourceExhausted" in str(e):
                    wait_time = _get_rate_limit_delay() * (attempt + 1)
                    print(f"Rate limit, waiting {wait_time:.1f}s...")
                    await asyncio.sleep(wait_time)
                else:
                    await asyncio.sleep(1)

        return ImageResult(success=False, prompt=prompt, model_used=model,
                           error_message=" | ".join(errors))

    async def _call_gemini_api(self, prompt: str, save_path: Optional[str],
                               model: str) -> ImageResult:
        """Call Gemini generate_content API and extract image."""
        config = None
        if self._genai_types:
            config = self._genai_types.GenerateContentConfig(response_modalities=["IMAGE"])

        kwargs = dict(model=model, contents=prompt)
        if config:
            kwargs["config"] = config

        response = await asyncio.to_thread(self._client.models.generate_content, **kwargs)

        image_data = self._extract_image(response)
        if not image_data:
            return ImageResult(success=False, prompt=prompt, model_used=model,
                               error_message="No image found in response")

        final_path = self._save_image(image_data, save_path)
        return ImageResult(success=True, file_path=str(final_path), prompt=prompt,
                           model_used=model)

    def _extract_image(self, response) -> Optional[bytes]:
        """Extract image bytes from Gemini API response."""
        # Try response.parts directly
        if hasattr(response, 'parts'):
            data = self._extract_from_parts(response.parts)
            if data:
                return data

        # Try candidates structure
        if hasattr(response, 'candidates'):
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    data = self._extract_from_parts(candidate.content.parts)
                    if data:
                        return data
        return None

    @staticmethod
    def _extract_from_parts(parts) -> Optional[bytes]:
        """Extract image bytes from response parts."""
        for part in parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                if getattr(part.inline_data, 'mime_type', '').startswith("image/"):
                    return part.inline_data.data
            if hasattr(part, 'as_image'):
                try:
                    from io import BytesIO
                    buf = BytesIO()
                    part.as_image().save(buf, format='PNG')
                    return buf.getvalue()
                except Exception:
                    pass
        return None

    def _get_save_path(self, save_path: Optional[str]) -> Path:
        if save_path:
            return Path(save_path)
        return Path(f"generated_image_{datetime.now():%Y%m%d_%H%M%S}.png")

    def _save_image(self, image_data: bytes, save_path: Optional[str]) -> Path:
        """Save image bytes to file."""
        path = self._get_save_path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            f.write(base64.b64decode(image_data) if isinstance(image_data, str) else image_data)
        return path

    def _cleanup_temp(self, temp_path: Path, temp_dir: str):
        """Remove temp file and directory."""
        try:
            if temp_path.exists():
                temp_path.unlink()
            Path(temp_dir).rmdir()
        except Exception:
            pass

    async def generate_batch(self, prompts: List[Dict[str, str]], output_dir: str,
                             concurrent_limit: int = 2) -> BatchResult:
        """Generate multiple images in batch with rate limiting."""
        start_time = datetime.now()
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        semaphore = asyncio.Semaphore(concurrent_limit)

        async def _gen(item: Dict[str, str]) -> ImageResult:
            async with semaphore:
                result = await self.generate_image(
                    prompt=item.get("prompt", ""),
                    save_path=str(output_path / item.get("filename", "image.png")),
                )
                await asyncio.sleep(_get_rate_limit_delay())
                return result

        results = await asyncio.gather(*[_gen(item) for item in prompts])
        success_count = sum(1 for r in results if r.success)
        return BatchResult(
            total=len(prompts), success_count=success_count,
            failed_count=len(prompts) - success_count,
            results=list(results),
            total_time=(datetime.now() - start_time).total_seconds(),
        )

    async def generate_with_watermark(self, prompt: str, output_path: str,
                                      watermark_config: "WatermarkConfig",
                                      size: str = DEFAULT_SIZE, **kwargs) -> ImageResult:
        """Generate image with AI-rendered text, then add PIL watermark."""
        start_time = datetime.now()
        tmp_dir = tempfile.mkdtemp()
        tmp_img = Path(tmp_dir) / "generated.png"

        try:
            gen = await self.generate_image(prompt=prompt, save_path=str(tmp_img), size=size)
            elapsed = lambda: (datetime.now() - start_time).total_seconds()

            if not gen.success:
                return ImageResult(success=False, prompt=prompt, model_used=gen.model_used,
                                   error_message=f"Image generation failed: {gen.error_message}",
                                   generation_time=elapsed())
            try:
                from .text_overlay import add_watermark_to_image

                if not watermark_config.watermark_enabled:
                    import shutil
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(tmp_img), output_path)
                    return ImageResult(success=True, file_path=output_path, prompt=prompt,
                                       model_used=gen.model_used, generation_time=elapsed())

                result = add_watermark_to_image(
                    image_path=str(tmp_img), watermark_config=watermark_config,
                    output_path=output_path)

                if not result.get("success"):
                    return ImageResult(success=False, prompt=prompt, model_used=gen.model_used,
                                       error_message=f"Watermark failed: {result.get('error')}",
                                       generation_time=elapsed())

                return ImageResult(success=True, file_path=output_path, prompt=prompt,
                                   model_used=gen.model_used, generation_time=elapsed())
            except ImportError as e:
                return ImageResult(success=False, prompt=prompt, model_used=gen.model_used,
                                   error_message=f"Watermark module not available: {e}",
                                   generation_time=elapsed())
        finally:
            self._cleanup_temp(tmp_img, tmp_dir)

    async def generate_batch_with_text_overlay(self, items: List[Dict[str, Any]],
                                               output_dir: str,
                                               concurrent_limit: int = 2) -> BatchResult:
        """Generate multiple images with watermark in batch."""
        from .prompt_converter import WatermarkConfig as WMConfig

        start_time = datetime.now()
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        semaphore = asyncio.Semaphore(concurrent_limit)

        default_wm = WMConfig(watermark_text="@money-lab-brian",
                              watermark_position="bottom-center", watermark_enabled=True)

        async def _gen(item: Dict[str, Any]) -> ImageResult:
            async with semaphore:
                wm = item.get("watermark_config") or default_wm
                result = await self.generate_with_watermark(
                    prompt=item.get("prompt", ""),
                    output_path=str(output_path / item.get("filename", "image.png")),
                    watermark_config=wm,
                )
                await asyncio.sleep(_get_rate_limit_delay())
                return result

        results = await asyncio.gather(*[_gen(item) for item in items])
        success_count = sum(1 for r in results if r.success)
        return BatchResult(
            total=len(items), success_count=success_count,
            failed_count=len(items) - success_count,
            results=list(results),
            total_time=(datetime.now() - start_time).total_seconds(),
        )


def create_generator(api_key: Optional[str] = None) -> GeminiImageGenerator:
    """Factory function to create GeminiImageGenerator instance."""
    return GeminiImageGenerator(api_key=api_key)
