# STEP 8: Image Generation (🚨 MANDATORY)

> **⚠️ 이 단계는 건너뛸 수 없습니다.**
> 블로그 글 작성 후 반드시 이미지 생성을 완료해야 합니다.

## Progress Status

```
[STEP 8/9] Image generation ████████████████████████░░░░ 88%
```

---

## 8-1. Pre-flight Checklist

Before generating images, verify the following:

- [ ] `이미지 가이드.md` 파일이 `{project_path}/` 에 존재하는지 확인
- [ ] Gemini API 키 설정 확인 (`GOOGLE_API_KEY` 또는 `GEMINI_API_KEY`)
- [ ] 출력 디렉토리 `{project_path}/images/` 존재 확인

```python
import os

# Check prerequisites
project_path = "./경제 블로그/YYYY-MM-DD/topic-name"  # Replace with actual path

# 1. Check image guide exists
image_guide_path = f"{project_path}/이미지 가이드.md"
assert os.path.exists(image_guide_path), f"❌ 이미지 가이드 파일이 없습니다: {image_guide_path}"

# 2. Check API key
api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
assert api_key, "❌ API 키가 설정되지 않았습니다. GOOGLE_API_KEY 또는 GEMINI_API_KEY를 설정하세요."

# 3. Ensure images directory exists
images_dir = f"{project_path}/images"
os.makedirs(images_dir, exist_ok=True)

print("✅ Pre-flight check passed!")
```

---

## 8-2. Image Generation Pipeline

Mode B (🎨 AI Generation) images are automatically generated via Gemini API.

### Pipeline Overview

```
┌─────────────────────────────────────────────────┐
│              이미지 생성 파이프라인               │
├─────────────────────────────────────────────────┤
│                                                 │
│  이미지 가이드.md 파싱                           │
│         ↓                                       │
│  Gemini API (gemini-3-pro-image-preview)        │
│  ├── 배경 이미지 생성                           │
│  ├── main_text (메인 텍스트) AI 렌더링          │
│  └── sub_text (부제목) AI 렌더링                │
│  └── 프롬프트에 폰트 스타일 포함                 │
│         ↓                                       │
│  PIL (Pillow)                                   │
│  └── watermark (워터마크)만 후처리              │
│  └── @money-lab-brian                           │
│         ↓                                       │
│  ./images/*.png 저장                            │
│                                                 │
└─────────────────────────────────────────────────┘
```

AI now renders text directly in the image. PIL only adds watermark:
1. AI generates image with text included in prompt
2. PIL adds watermark at bottom-center
3. Final PNG exported

---

## 8-3. Execution (🚨 MANDATORY)

### Option A: Process Entire Image Guide (Recommended)

```python
from scripts.image_pipeline import ImagePipeline

# Initialize pipeline
pipeline = ImagePipeline()

# Read image guide
with open(f"{project_path}/이미지 가이드.md", "r", encoding="utf-8") as f:
    image_guide_content = f.read()

# Generate all images with watermark
result = await pipeline.process_image_guide(
    image_guide_content=image_guide_content,
    output_dir=f"{project_path}/images/",
    use_text_overlay=True  # Enables watermark for Mode B-3 items
)

# Print summary
print(result.summary())
# 📊 Pipeline result: 5/5 success, 5 with watermark
```

### Option B: Generate Single Image with Watermark

```python
from scripts.image_pipeline import ImagePipeline
from scripts.prompt_converter import WatermarkConfig

# Initialize pipeline
pipeline = ImagePipeline()

# Generate single thumbnail with AI-rendered text + watermark
result = await pipeline.generate_with_watermark(
    prompt="Blog thumbnail, bold Korean text '0세 적금 필수!' in upper third, subtitle '연 12% 고금리' in center, warm gradient background, 16:9",
    output_path=f"{project_path}/images/01_썸네일.png",
    watermark_config=WatermarkConfig(
        watermark_text="@money-lab-brian",
        watermark_position="bottom-center",
        watermark_margin_bottom=60,
        watermark_font_size=18,
        watermark_font_color="rgba(255,255,255,0.6)"
    )
)
# Result: AI renders text → Watermark added → Final PNG saved
```

### Option C: Legacy Batch Generation

```python
from scripts.gemini_image import GeminiImageGenerator
from scripts.prompt_converter import generate_image_prompts_for_batch

# Extract prompts from image guide
with open(f"{project_path}/이미지 가이드.md", "r", encoding="utf-8") as f:
    image_guide_content = f.read()

prompts = generate_image_prompts_for_batch(image_guide_content)
# [{"prompt": "...", "filename": "01_썸네일.png"}, ...]

# Batch generate via Gemini API
generator = GeminiImageGenerator()
result = await generator.generate_batch(
    prompts=prompts,
    output_dir=f"{project_path}/images/"
)

print(result.summary())
# 📊 Batch generation result: 5/5 success (100.0%), elapsed: 25.3s
```

---

## 8-4. Environment Variable Setup

```bash
# Required: Set API key
export GOOGLE_API_KEY="your-api-key"

# Or use alternative name
export GEMINI_API_KEY="your-api-key"
```

### Get API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key
3. Enable Gemini API access

---

## 8-5. Generation Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Requests per minute | 15 | Auto-delay applied |
| Free daily quota | 500 images | gemini-2.0-flash-exp |
| Fallback model | imagen-3.0 | When quota exceeded |

### 3-Tier Model Fallback

Triggers on 429/QUOTA_EXCEEDED/SAFETY errors:
1. `gemini-2.0-flash-exp-image-generation` (primary)
2. `gemini-2.5-flash-image` (fallback)
3. `gemini-3-pro-image-preview` (fallback 2)

---

## 8-6. Error Handling

### 실패 시 처리

| Error Type | Solution |
|------------|----------|
| API 키 오류 | `.env` 파일 확인 또는 `ensure_venv.py` 재실행 |
| 쿼터 초과 | 자동 fallback 모델 사용 (3-tier system) |
| 부분 실패 | 실패한 이미지만 재생성 |
| 안전성 필터 | 프롬프트 수정 후 재시도 |

### Retry Failed Images Only

```python
# If some images failed, retry only those
failed_prompts = [p for p in prompts if p["status"] == "failed"]

if failed_prompts:
    print(f"⚠️ Retrying {len(failed_prompts)} failed images...")
    retry_result = await generator.generate_batch(
        prompts=failed_prompts,
        output_dir=f"{project_path}/images/"
    )
    print(retry_result.summary())
```

---

## 8-7. Verification Checklist

**⚠️ 다음 단계로 진행하기 전에 모든 항목을 확인하세요:**

- [ ] 모든 이미지 생성 완료 (N/N success)
- [ ] 워터마크 "@money-lab-brian" 적용 확인
- [ ] 파일 크기 적정 (각 이미지 < 1MB)
- [ ] 이미지 품질 확인 (텍스트 렌더링 정상)

### Quick Verification

```python
import os
from pathlib import Path

images_dir = Path(f"{project_path}/images")
images = list(images_dir.glob("*.png"))

print(f"📊 이미지 생성 결과: {len(images)} 개 파일")

for img in sorted(images):
    size_kb = img.stat().st_size / 1024
    status = "✅" if size_kb < 1024 else "⚠️ (>1MB)"
    print(f"  {status} {img.name}: {size_kb:.1f} KB")
```

---

## Next Step

이미지 생성 완료 → **[STEP 9: Revision Loop](step9-revise.md)**
