"""
Gemini Image Generation API Integration Module

Automatically generates blog images using Google Gemini API.
Uses Gemini 2.5 Flash by default, falls back to Imagen 4 when quota exceeded.
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


# API configuration constants
DEFAULT_MODEL = "gemini-2.0-flash-exp"
FALLBACK_MODEL = "imagen-3.0-generate-002"
DEFAULT_SIZE = "1024x1024"
DEFAULT_TIMEOUT = 60
DEFAULT_RETRY_COUNT = 3
RATE_LIMIT_DELAY = 4.0  # Considering 15 requests per minute limit


@dataclass
class ImageResult:
    """Data class for image generation result"""

    success: bool
    file_path: Optional[str] = None
    prompt: str = ""
    model_used: str = ""
    error_message: Optional[str] = None
    generation_time: float = 0.0

    def __str__(self) -> str:
        if self.success:
            return f"✅ Generation complete: {self.file_path} ({self.model_used})"
        return f"❌ Generation failed: {self.error_message}"


@dataclass
class BatchResult:
    """Batch image generation result"""

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
            f"📊 Batch generation result: {self.success_count}/{self.total} succeeded "
            f"({self.success_rate:.1f}%), time elapsed: {self.total_time:.1f}s"
        )


class GeminiImageGenerator:
    """
    Image generator using Gemini API

    Usage example:
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
        Initialize GeminiImageGenerator

        Args:
            api_key: Google API key (loads from environment variable if not provided)
            primary_model: Primary model (default: gemini-2.0-flash-exp)
            fallback_model: Fallback model (default: imagen-3.0-generate-002)
        """
        self.api_key = api_key or self._load_api_key()
        self.primary_model = primary_model or self._get_config_model("primary") or DEFAULT_MODEL
        self.fallback_model = fallback_model or self._get_config_model("fallback") or FALLBACK_MODEL
        self.timeout = self._get_config_timeout() or DEFAULT_TIMEOUT
        self.retry_count = self._get_config_retry_count() or DEFAULT_RETRY_COUNT

        # Client initialization (lazy loading)
        self._client = None

    def _load_api_key(self) -> str:
        """Load API key from environment variable"""
        api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "Google API key not set. "
                "Set environment variable GOOGLE_API_KEY or GEMINI_API_KEY."
            )

        return api_key

    def _get_config_model(self, model_type: str) -> Optional[str]:
        """Get model settings from config.yaml"""
        config = get_config()
        return get_config_value(config, "gemini", "models", model_type)

    def _get_config_timeout(self) -> Optional[int]:
        """Get timeout settings from config.yaml"""
        config = get_config()
        return get_config_value(config, "gemini", "timeout")

    def _get_config_retry_count(self) -> Optional[int]:
        """Get retry count settings from config.yaml"""
        config = get_config()
        return get_config_value(config, "gemini", "retry_count")

    def _init_client(self):
        """Initialize Google Generative AI client"""
        if self._client is not None:
            return

        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._client = genai
        except ImportError:
            raise ImportError(
                "google-generativeai package not installed. "
                "Install with: pip install google-generativeai"
            )

    async def generate_image(
        self,
        prompt: str,
        save_path: Optional[str] = None,
        size: str = DEFAULT_SIZE,
        use_fallback: bool = True,
    ) -> ImageResult:
        """
        Generate a single image.

        Args:
            prompt: Image generation prompt (English recommended)
            save_path: Save path (generates temp file if not provided)
            size: Image size (default: 1024x1024)
            use_fallback: Whether to use fallback model on failure

        Returns:
            ImageResult: Generation result
        """
        start_time = datetime.now()

        # Try with primary model
        result = await self._generate_with_model(
            prompt=prompt,
            save_path=save_path,
            size=size,
            model=self.primary_model,
        )

        # Try fallback model on failure
        if not result.success and use_fallback and self._should_fallback(result.error_message):
            print(f"⚠️ {self.primary_model} failed, retrying with {self.fallback_model}...")
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
        """Determine whether to attempt fallback"""
        if not error_message:
            return True

        # Fallback trigger conditions
        fallback_triggers = ["429", "QUOTA_EXCEEDED", "RATE_LIMIT", "ResourceExhausted"]
        return any(trigger in error_message for trigger in fallback_triggers)

    async def _generate_with_model(
        self,
        prompt: str,
        save_path: Optional[str],
        size: str,
        model: str,
    ) -> ImageResult:
        """Generate image with specific model"""
        self._init_client()

        for attempt in range(self.retry_count):
            try:
                # Generate image with Gemini model
                if model.startswith("gemini"):
                    return await self._generate_with_gemini(prompt, save_path, model)
                else:
                    return await self._generate_with_imagen(prompt, save_path, size, model)

            except Exception as e:
                error_msg = str(e)

                # Wait and retry on rate limit error
                if "429" in error_msg or "ResourceExhausted" in error_msg:
                    if attempt < self.retry_count - 1:
                        wait_time = RATE_LIMIT_DELAY * (attempt + 1)
                        print(f"⏳ Rate limit, waiting {wait_time:.1f}s before retry...")
                        await asyncio.sleep(wait_time)
                        continue

                # Retry if not last attempt
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
            error_message="Maximum retry count exceeded",
        )

    async def _generate_with_gemini(
        self,
        prompt: str,
        save_path: Optional[str],
        model: str,
    ) -> ImageResult:
        """Generate image with Gemini model"""
        try:
            # Gemini 2.0 Flash model configuration (supports image generation)
            generation_config = {
                "response_modalities": ["image", "text"],
            }

            gemini_model = self._client.GenerativeModel(
                model_name=model,
                generation_config=generation_config,
            )

            # Image generation request
            response = await asyncio.to_thread(
                gemini_model.generate_content,
                prompt,
            )

            # Extract image from response
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
                    error_message="No image found in response",
                )

            # Save file
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
        """Generate image with Imagen model"""
        try:
            imagen_model = self._client.ImageGenerationModel(model_name=model)

            # Parse size
            width, height = self._parse_size(size)

            # Generate image
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
                    error_message="No image generation result",
                )

            # Extract and save image data
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
        """Parse size string"""
        match = re.match(r"(\d+)x(\d+)", size)
        if match:
            return int(match.group(1)), int(match.group(2))
        return 1024, 1024

    def _get_aspect_ratio(self, width: int, height: int) -> str:
        """Return aspect ratio"""
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
        """Save image to file"""
        if save_path:
            path = Path(save_path)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = Path(f"generated_image_{timestamp}.{ext}")

        # Create directory
        path.parent.mkdir(parents=True, exist_ok=True)

        # Save file
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
        Generate multiple images in batch.

        Args:
            prompts: Prompt list [{"prompt": "...", "filename": "..."}, ...]
            output_dir: Output directory
            concurrent_limit: Concurrent execution limit (considering 15 requests/min limit)

        Returns:
            BatchResult: Batch generation result
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

                # Delay to prevent rate limiting
                await asyncio.sleep(RATE_LIMIT_DELAY)

                return result

        # Parallel execution (with limited concurrency)
        tasks = [generate_with_limit(item) for item in prompts]
        results = await asyncio.gather(*tasks)

        # Aggregate results
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
    Factory function to create GeminiImageGenerator instance.

    Args:
        api_key: Google API key (optional)

    Returns:
        GeminiImageGenerator instance
    """
    return GeminiImageGenerator(api_key=api_key)


# Synchronous wrapper functions for convenience
def generate_image_sync(
    prompt: str,
    save_path: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ImageResult:
    """
    Generate image synchronously.

    Args:
        prompt: Image generation prompt
        save_path: Save path
        api_key: API key (optional)

    Returns:
        ImageResult: Generation result
    """
    generator = create_generator(api_key)
    return asyncio.run(generator.generate_image(prompt=prompt, save_path=save_path))


def generate_batch_sync(
    prompts: List[Dict[str, str]],
    output_dir: str,
    api_key: Optional[str] = None,
) -> BatchResult:
    """
    Generate multiple images synchronously.

    Args:
        prompts: Prompt list
        output_dir: Output directory
        api_key: API key (optional)

    Returns:
        BatchResult: Batch generation result
    """
    generator = create_generator(api_key)
    return asyncio.run(generator.generate_batch(prompts=prompts, output_dir=output_dir))
