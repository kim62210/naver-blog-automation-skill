# STEP 5: Image Generation (MANDATORY)

> **This step cannot be skipped.** Images must be generated after blog writing is complete.

## Progress Status

```
[STEP 5/6] Image generation ██████████████████████████░░ 90%
```

---

## 5-1. Pre-flight Checklist

- [ ] `이미지 가이드.md` exists in `{project_path}/`
- [ ] Gemini API key set (`GOOGLE_API_KEY` or `GEMINI_API_KEY`)
- [ ] Output directory `{project_path}/images/` exists

```python
import os

project_path = "./경제 블로그/YYYY-MM-DD/topic-name"
image_guide_path = f"{project_path}/이미지 가이드.md"
assert os.path.exists(image_guide_path), f"Image guide not found: {image_guide_path}"

api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
assert api_key, "API key not set."

os.makedirs(f"{project_path}/images", exist_ok=True)
```

---

## 5-2. Image Generation Pipeline

Standard entry point: `ImagePipeline.process_image_guide()`

### Pipeline Sequence

1. Parse `이미지 가이드.md` -> split into image sections
2. Each section: detect mode (B-3 recommended)
3. Extract prompt from fenced code block
4. Extract watermark config from `[Watermark Config]` section
5. Gemini API batch generation (`generate_batch_with_text_overlay()`)
6. PIL watermark overlay (`text_overlay.add_watermark_to_image()`)

### Image Specification

| Property | Value | Config Path |
|----------|-------|-------------|
| Model | `gemini-3-pro-image-preview` | `gemini.models.primary` |
| Size | `1024x1024` (1:1) | `gemini.default_size` |
| Format | PNG | Fixed |
| Watermark | `@money-lab-brian` | `watermark.*` |

### Rate Limiting
- **10 requests/minute** (`gemini.rate_limit.requests_per_minute`)
- **6s interval** (`gemini.rate_limit.delay_between_requests`)

### Filename Convention
- Format: `{NN}_{역할}.png` (e.g., `01_썸네일.png`, `02_금리비교차트.png`)
- `{NN}`: 2-digit zero-padded index
- `{역할}`: Image role description, **20 char truncation**
- Extension: `.png` fixed

---

## 5-3. Execution

### Option A: Process Entire Image Guide (Recommended)

```python
from scripts.image_pipeline import ImagePipeline

pipeline = ImagePipeline()

with open(f"{project_path}/이미지 가이드.md", "r", encoding="utf-8") as f:
    image_guide_content = f.read()

result = await pipeline.process_image_guide(
    image_guide_content=image_guide_content,
    output_dir=f"{project_path}/images/"
)

print(result.summary())
```

### Option B: Generate Single Image

```python
from scripts.image_pipeline import ImagePipeline
from scripts.prompt_converter import WatermarkConfig

pipeline = ImagePipeline()

result = await pipeline.generate_with_watermark(
    prompt="Blog thumbnail, bold Korean sans-serif font...",
    output_path=f"{project_path}/images/01_썸네일.png",
    watermark_config=WatermarkConfig(
        watermark_text="@money-lab-brian",
        watermark_position="bottom-center",
        watermark_margin_bottom=60,
        watermark_font_size=18,
        watermark_font_color="rgba(255,255,255,0.6)"
    )
)
```

---

## 5-4. Mode Detection

`image_pipeline.py` -> `_parse_image_section()` auto-detects mode:

| Priority | Condition | Mode | Status |
|----------|-----------|------|--------|
| 1 | `[Watermark Config]` exists | Mode B-3 | **Recommended** |
| 2 | `🎨 AI Generation` exists | Mode B | Standard |

> Mode A (reference images) support removed. All images are AI-generated.

---

## 5-5. Watermark Specification

| Field | Value |
|-------|-------|
| Text | `@money-lab-brian` |
| Position | bottom-center |
| Margin bottom | 60px |
| Font size | 18px |
| Font color | `rgba(255,255,255,0.6)` |
| Font family | `Pretendard, Nanum Gothic, sans-serif` |

---

## 5-6. Error Handling

| Error Type | Solution |
|------------|----------|
| API key error | Check `.env` or re-run `ensure_venv.py` |
| Quota exceeded | Wait and retry |
| Partial failure | Retry only failed images |
| Safety filter | Modify prompt and retry |

---

## 5-7. Verification Checklist

- [ ] `images/` directory exists
- [ ] All images generated (N/N success)
- [ ] Image count >= 3 and <= 10
- [ ] All filenames in `{NN}_{역할}.png` format
- [ ] `01_썸네일.png` exists
- [ ] All images have `@money-lab-brian` watermark
- [ ] Each image <= 1MB
- [ ] Image quality: text rendering OK, 1:1 ratio

```python
from pathlib import Path

images_dir = Path(f"{project_path}/images")
images = list(images_dir.glob("*.png"))

print(f"Image result: {len(images)} files")
for img in sorted(images):
    size_kb = img.stat().st_size / 1024
    status = "OK" if size_kb < 1024 else "WARNING (>1MB)"
    print(f"  {status} {img.name}: {size_kb:.1f} KB")
```

---

## Next Step

Image generation complete -> **[STEP 6: Revision Loop](step6-revise.md)**
