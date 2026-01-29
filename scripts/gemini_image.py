"""
Gemini Image Generation API Integration Module

Automatically generates blog images using Google Gemini API.
Uses Gemini 2.0 Flash Nano Banana by default, falls back to Imagen 3 when quota exceeded.

Updated to use the new google-genai SDK.
Supports text overlay pipeline for better Korean text quality.
"""

import asyncio
import base64
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

from .config import get_config, get_config_value

if TYPE_CHECKING:
    from .prompt_converter import TextOverlayConfig as PromptTextOverlayConfig


# API configuration constants - 3-tier fallback system
# 📚 Rate Limit 상세 정보: docs/GEMINI_IMAGE_API_LIMITS.md 참조
DEFAULT_MODEL = "gemini-2.0-flash-exp-image-generation"  # Nano Banana - 무료 티어 가능
FALLBACK_MODEL = "gemini-2.5-flash-image"  # Gemini 2.5 Flash Image - 무료 제한적
FALLBACK_MODEL_2 = "gemini-3-pro-image-preview"  # Gemini 3 Pro Image - 결제 필수
DEFAULT_SIZE = "1024x1024"
DEFAULT_TIMEOUT = 60
DEFAULT_RETRY_COUNT = 3
RATE_LIMIT_DELAY = 6.0  # 안전 간격: 60초/10요청 = 6초


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
    Image generator using Gemini API (new google-genai SDK)

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
        fallback_model_2: Optional[str] = None,
    ):
        """
        Initialize GeminiImageGenerator

        Args:
            api_key: Google API key (loads from environment variable if not provided)
            primary_model: Primary model (default: gemini-2.0-flash-exp-image-generation)
            fallback_model: First fallback model (default: imagen-3.0-fast-generate-001)
            fallback_model_2: Second fallback model (default: imagen-3.0-generate-002)
        """
        self.api_key = api_key or self._load_api_key()
        self.primary_model = primary_model or self._get_config_model("primary") or DEFAULT_MODEL
        self.fallback_model = fallback_model or self._get_config_model("fallback") or FALLBACK_MODEL
        self.fallback_model_2 = fallback_model_2 or self._get_config_model("fallback_2") or FALLBACK_MODEL_2
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
        """Initialize Google GenAI client (new SDK)"""
        if self._client is not None:
            return

        try:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            self._genai_types = None
            # Import types for configuration
            try:
                from google.genai import types
                self._genai_types = types
            except ImportError:
                pass
        except ImportError:
            raise ImportError(
                "google-genai package not installed. "
                "Install with: pip install google-genai"
            )

    async def generate_image(
        self,
        prompt: str,
        save_path: Optional[str] = None,
        size: str = DEFAULT_SIZE,
        use_fallback: bool = True,
    ) -> ImageResult:
        """
        Generate a single image with 3-tier fallback.

        Args:
            prompt: Image generation prompt (English recommended)
            save_path: Save path (generates temp file if not provided)
            size: Image size (default: 1024x1024)
            use_fallback: Whether to use fallback models on failure

        Returns:
            ImageResult: Generation result
        """
        start_time = datetime.now()

        # Tier 1: Primary model (Nano Banana)
        result = await self._generate_with_model(
            prompt=prompt,
            save_path=save_path,
            size=size,
            model=self.primary_model,
        )

        # Tier 2: First fallback (Imagen 3 Fast)
        if not result.success and use_fallback and self._should_fallback(result.error_message):
            print(f"⚠️ {self.primary_model} failed, retrying with {self.fallback_model}...")
            await asyncio.sleep(RATE_LIMIT_DELAY)

            result = await self._generate_with_model(
                prompt=prompt,
                save_path=save_path,
                size=size,
                model=self.fallback_model,
            )

        # Tier 3: Second fallback (Imagen 3 Standard)
        if not result.success and use_fallback and self._should_fallback(result.error_message):
            print(f"⚠️ {self.fallback_model} failed, retrying with {self.fallback_model_2}...")
            await asyncio.sleep(RATE_LIMIT_DELAY)

            result = await self._generate_with_model(
                prompt=prompt,
                save_path=save_path,
                size=size,
                model=self.fallback_model_2,
            )

        result.generation_time = (datetime.now() - start_time).total_seconds()
        return result

    def _should_fallback(self, error_message: Optional[str]) -> bool:
        """Determine whether to attempt fallback"""
        if not error_message:
            return True

        # Fallback trigger conditions
        fallback_triggers = [
            "429", "QUOTA_EXCEEDED", "RATE_LIMIT", "ResourceExhausted",
            "SAFETY", "blocked", "filtered", "RECITATION",
            "INVALID_ARGUMENT", "does not support", "not support"
        ]
        return any(trigger.lower() in error_message.lower() for trigger in fallback_triggers)

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
                # Generate image with Gemini model (Nano Banana)
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
        """Generate image with Gemini model (Nano Banana) using new SDK"""
        try:
            # Build configuration for image generation
            config = None
            if self._genai_types:
                config = self._genai_types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                )

            # Image generation request using new SDK
            if config:
                response = await asyncio.to_thread(
                    self._client.models.generate_content,
                    model=model,
                    contents=prompt,
                    config=config,
                )
            else:
                # Fallback without types
                response = await asyncio.to_thread(
                    self._client.models.generate_content,
                    model=model,
                    contents=prompt,
                )

            # Extract image from response (new SDK format)
            image_data = None

            # Handle new SDK response format
            if hasattr(response, 'parts'):
                for part in response.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        mime_type = getattr(part.inline_data, 'mime_type', '')
                        if mime_type.startswith("image/"):
                            image_data = part.inline_data.data
                            break
                    # Try as_image() method
                    if hasattr(part, 'as_image'):
                        try:
                            img = part.as_image()
                            # Get bytes from PIL Image
                            from io import BytesIO
                            buffer = BytesIO()
                            img.save(buffer, format='PNG')
                            image_data = buffer.getvalue()
                            break
                        except Exception:
                            pass

            # Fallback: check candidates structure
            if not image_data and hasattr(response, 'candidates'):
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                mime_type = getattr(part.inline_data, 'mime_type', '')
                                if mime_type.startswith("image/"):
                                    image_data = part.inline_data.data
                                    break
                            if hasattr(part, 'as_image'):
                                try:
                                    img = part.as_image()
                                    from io import BytesIO
                                    buffer = BytesIO()
                                    img.save(buffer, format='PNG')
                                    image_data = buffer.getvalue()
                                    break
                                except Exception:
                                    pass

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
        """Generate image with Imagen model using new SDK"""
        try:
            # Parse size and get aspect ratio
            width, height = self._parse_size(size)
            aspect_ratio = self._get_aspect_ratio(width, height)

            # Build configuration
            config = None
            if self._genai_types:
                config = self._genai_types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio=aspect_ratio,
                    output_mime_type='image/png',
                    include_rai_reason=True,
                )

            # Generate image using new SDK
            if config:
                response = await asyncio.to_thread(
                    self._client.models.generate_images,
                    model=model,
                    prompt=prompt,
                    config=config,
                )
            else:
                response = await asyncio.to_thread(
                    self._client.models.generate_images,
                    model=model,
                    prompt=prompt,
                )

            if not response.generated_images:
                # Check for RAI reason (content blocked)
                rai_reason = None
                if hasattr(response, 'generated_images') and response.generated_images:
                    first_img = response.generated_images[0]
                    if hasattr(first_img, 'rai_reason'):
                        rai_reason = first_img.rai_reason

                error_msg = "No image generation result"
                if rai_reason:
                    error_msg = f"Content blocked: {rai_reason}"

                return ImageResult(
                    success=False,
                    prompt=prompt,
                    model_used=model,
                    error_message=error_msg,
                )

            # Extract and save image data using new SDK
            generated_image = response.generated_images[0]

            # Try to save directly using the image object
            if hasattr(generated_image, 'image'):
                img = generated_image.image
                if hasattr(img, 'save'):
                    # Direct save method
                    final_path = self._get_save_path(save_path, "png")
                    final_path.parent.mkdir(parents=True, exist_ok=True)
                    await asyncio.to_thread(img.save, str(final_path))

                    return ImageResult(
                        success=True,
                        file_path=str(final_path),
                        prompt=prompt,
                        model_used=model,
                    )
                elif hasattr(img, '_image_bytes'):
                    # Legacy bytes access
                    image_data = img._image_bytes
                    final_path = self._save_image(image_data, save_path, "png")

                    return ImageResult(
                        success=True,
                        file_path=str(final_path),
                        prompt=prompt,
                        model_used=model,
                    )

            # Fallback: Try to get bytes from data attribute
            if hasattr(generated_image, 'data'):
                image_data = generated_image.data
                if isinstance(image_data, str):
                    image_data = base64.b64decode(image_data)
                final_path = self._save_image(image_data, save_path, "png")

                return ImageResult(
                    success=True,
                    file_path=str(final_path),
                    prompt=prompt,
                    model_used=model,
                )

            return ImageResult(
                success=False,
                prompt=prompt,
                model_used=model,
                error_message="Could not extract image data from response",
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

    def _get_save_path(self, save_path: Optional[str], ext: str = "png") -> Path:
        """Get the save path"""
        if save_path:
            return Path(save_path)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return Path(f"generated_image_{timestamp}.{ext}")

    def _save_image(
        self,
        image_data: bytes,
        save_path: Optional[str],
        ext: str = "png",
    ) -> Path:
        """Save image to file"""
        path = self._get_save_path(save_path, ext)

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

    async def generate_with_text_overlay(
        self,
        prompt: str,
        output_path: str,
        text_config: "PromptTextOverlayConfig",
        size: str = DEFAULT_SIZE,
        use_fallback: bool = True,
        background_only: bool = True,
    ) -> ImageResult:
        """
        Generate image with text overlay pipeline.

        Workflow:
        1. Strip text instructions from prompt (if background_only=True)
        2. Generate background image via Gemini
        3. Apply text overlay locally (Pillow)
        4. Export final PNG

        Args:
            prompt: Image generation prompt
            output_path: Final output path for PNG
            text_config: TextOverlayConfig from prompt_converter module
            size: Image size (default: 1024x1024)
            use_fallback: Whether to use fallback models on failure
            background_only: Whether to strip text instructions from prompt

        Returns:
            ImageResult: Generation result with final PNG path

        Example:
            from scripts.prompt_converter import TextOverlayConfig

            text_config = TextOverlayConfig(
                main_text="0세 적금 필수!",
                sub_text="연 12% 고금리",
                position="center",
                font_size=48,
                font_color="#FFFFFF",
                shadow=True
            )

            result = await generator.generate_with_text_overlay(
                prompt="Blog thumbnail, finance concept, warm gradient...",
                output_path="./images/01_썸네일.png",
                text_config=text_config
            )
        """
        import tempfile
        from pathlib import Path as PathLib

        start_time = datetime.now()

        # Step 1: Strip text instructions if background_only
        processed_prompt = prompt
        if background_only:
            from .prompt_converter import strip_text_instructions
            processed_prompt = strip_text_instructions(prompt)
            # Add explicit "NO TEXT" instruction
            if "no text" not in processed_prompt.lower():
                processed_prompt += " NO TEXT, NO LETTERS, NO WORDS."

        # Step 2: Generate background image to temp file
        temp_dir = tempfile.mkdtemp()
        temp_bg_path = PathLib(temp_dir) / "background.png"

        bg_result = await self.generate_image(
            prompt=processed_prompt,
            save_path=str(temp_bg_path),
            size=size,
            use_fallback=use_fallback,
        )

        if not bg_result.success:
            return ImageResult(
                success=False,
                prompt=prompt,
                model_used=bg_result.model_used,
                error_message=f"Background generation failed: {bg_result.error_message}",
                generation_time=(datetime.now() - start_time).total_seconds(),
            )

        # Step 3: Apply text overlay
        try:
            from .text_overlay import add_text_to_existing_image

            overlay_result = add_text_to_existing_image(
                image_path=str(temp_bg_path),
                text_config=text_config,
                output_path=output_path,
            )

            if not overlay_result.get("success"):
                return ImageResult(
                    success=False,
                    prompt=prompt,
                    model_used=bg_result.model_used,
                    error_message=f"Text overlay failed: {overlay_result.get('error')}",
                    generation_time=(datetime.now() - start_time).total_seconds(),
                )

            return ImageResult(
                success=True,
                file_path=output_path,
                prompt=prompt,
                model_used=bg_result.model_used,
                generation_time=(datetime.now() - start_time).total_seconds(),
            )

        except ImportError as e:
            return ImageResult(
                success=False,
                prompt=prompt,
                model_used=bg_result.model_used,
                error_message=f"Text overlay module not available: {e}",
                generation_time=(datetime.now() - start_time).total_seconds(),
            )
        finally:
            # Cleanup temp files
            try:
                if temp_bg_path.exists():
                    temp_bg_path.unlink()
                PathLib(temp_dir).rmdir()
            except Exception:
                pass

    async def generate_batch_with_text_overlay(
        self,
        items: List[Dict[str, Any]],
        output_dir: str,
        concurrent_limit: int = 2,
    ) -> BatchResult:
        """
        Generate multiple images with text overlay in batch.

        Args:
            items: List of generation configs, each containing:
                - prompt: Image generation prompt
                - filename: Output filename
                - text_config: TextOverlayConfig (optional, if None uses regular generation)
            output_dir: Output directory
            concurrent_limit: Concurrent execution limit

        Returns:
            BatchResult: Batch generation result

        Example:
            from scripts.prompt_converter import TextOverlayConfig

            items = [
                {
                    "prompt": "Blog thumbnail background...",
                    "filename": "01_썸네일.png",
                    "text_config": TextOverlayConfig(
                        main_text="제목",
                        sub_text="부제목"
                    )
                },
                {
                    "prompt": "Info graphic...",
                    "filename": "02_인포그래픽.png",
                    "text_config": None  # No text overlay
                }
            ]

            result = await generator.generate_batch_with_text_overlay(
                items=items,
                output_dir="./images/"
            )
        """
        start_time = datetime.now()
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results: List[ImageResult] = []
        semaphore = asyncio.Semaphore(concurrent_limit)

        async def generate_with_limit(item: Dict[str, Any]) -> ImageResult:
            async with semaphore:
                prompt = item.get("prompt", "")
                filename = item.get("filename", f"image_{len(results):02d}.png")
                text_config = item.get("text_config")
                save_path = str(output_path / filename)

                if text_config:
                    # Use text overlay pipeline
                    result = await self.generate_with_text_overlay(
                        prompt=prompt,
                        output_path=save_path,
                        text_config=text_config,
                    )
                else:
                    # Regular generation
                    result = await self.generate_image(
                        prompt=prompt,
                        save_path=save_path,
                    )

                # Delay to prevent rate limiting
                await asyncio.sleep(RATE_LIMIT_DELAY)

                return result

        # Parallel execution (with limited concurrency)
        tasks = [generate_with_limit(item) for item in items]
        results = await asyncio.gather(*tasks)

        # Aggregate results
        success_count = sum(1 for r in results if r.success)
        total_time = (datetime.now() - start_time).total_seconds()

        return BatchResult(
            total=len(items),
            success_count=success_count,
            failed_count=len(items) - success_count,
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
