# STEP 9: Image Generation (🚨 MANDATORY)

> **⚠️ 이 단계는 건너뛸 수 없습니다.**
> 블로그 글 작성 후 반드시 이미지 생성을 완료해야 합니다.

## Progress Status

```
[STEP 9/10] Image generation ██████████████████████████░░ 90%
```

---

## 9-1. Pre-flight Checklist

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

## 9-2. Image Generation Pipeline

Mode B (🎨 AI Generation) images are automatically generated via Gemini API.

### Pipeline Overview

```
┌──────────────────────────────────────────────────────┐
│              이미지 생성 파이프라인                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  이미지 가이드.md 파싱                                │
│         ↓                                            │
│  Gemini API (gemini-3-pro-image-preview)             │
│  ├── 배경 이미지 생성                                │
│  ├── main_text (메인 텍스트) AI 렌더링               │
│  └── sub_text (부제목) AI 렌더링                     │
│  └── 비율: 1:1 (1024x1024)                           │
│         ↓                                            │
│  PIL (Pillow)                                        │
│  └── watermark (워터마크)만 후처리                   │
│  └── config.yaml watermark.*                         │
│         ↓                                            │
│  ./images/{NN}_{역할}.png 저장                       │
│                                                      │
└──────────────────────────────────────────────────────┘
```

AI now renders text directly in the image. PIL only adds watermark:
1. AI generates image with text included in prompt
2. PIL adds watermark at bottom-center
3. Final PNG exported

### Image Specification

| 속성 | 값 | 설정 경로 |
|------|-----|-----------|
| Model | `gemini-3-pro-image-preview` | `config.yaml` → `gemini.models.primary` |
| Size | `1024x1024` (1:1) | `config.yaml` → `gemini.default_size` |
| Format | PNG | 고정 |
| Watermark | `@money-lab-brian` | `config.yaml` → `watermark.*` |

### Image Count

| 항목 | 값 | config.yaml 경로 |
|------|-----|-------------------|
| 기본 이미지 수 | 5장 | `images.default_count` |
| 최소 | 3장 | `images.min_count` |
| 최대 | 10장 | `images.max_count` |

환경변수 `BLOG_IMAGE_COUNT`로 오버라이드 가능.

### Pipeline Sequence

표준 진입점: `ImagePipeline.process_image_guide()`

1. `_parse_image_guide()` → `image_guide_parser.split_image_sections()` 호출
2. 각 섹션에서 모드 판별 (`_parse_image_section()`)
3. 프롬프트 추출 (`image_guide_parser.extract_first_prompt()`)
4. 워터마크 설정 추출 (`prompt_converter.extract_watermark_config()`)
5. Gemini API 배치 생성 (`generator.generate_batch_with_text_overlay()`)
6. 워터마크 적용 (PIL, `text_overlay.add_watermark_to_image()`)

### Filename Convention

- 형식: `{NN}_{역할}.png` (예: `01_썸네일.png`, `02_금리비교차트.png`)
- `{NN}`: 2자리 제로패딩 인덱스 (01, 02, ...)
- `{역할}`: 이미지 역할 설명, **20자 절삭**
- 특수문자 제거(`[^\w가-힣\s]`), 공백→`_`
- 확장자: `.png` 고정

---

## 9-2.5. 이미지 유형별 생성 가이드

### 썸네일 (Image 1)

- 이미지의 **70-80% 영역**에 텍스트 배치
- **메인 텍스트**: 블로그 제목 (굵은 한글 폰트, 고대비)
- **서브 텍스트**: 부제목 (선택 사항)
- **배경**: 그라데이션/테마 비주얼
- 프롬프트에 반드시 포함: `"render exact Korean text characters as specified"`
- 비율: **1:1 (1024x1024)**

### 본문 이미지 (Image 2+)

- 해당 문단 내용에 충실한 이미지
- 비율: **1:1 (1024x1024)**

**콘텐츠 유형별 가이드:**

| 콘텐츠 유형 | 권장 이미지 | 예시 |
|---|---|---|
| 데이터/통계 | 막대/원형 차트 | 금리 비교 |
| 비교 | VS 레이아웃 | 상품 A vs B |
| 절차/단계 | 플로우 다이어그램 | 신청 절차 |
| 체크리스트 | 체크박스 레이아웃 | 필요 서류 |
| 감성/마무리 | 사진 스타일 | 희망/응원 테마 |

---

## 9-3. Execution (🚨 MANDATORY)

### Mode Detection

`image_pipeline.py` → `_parse_image_section()`에서 모드를 자동 판별합니다:

| 우선순위 | 조건 | 모드 | 상태 |
|---------|------|------|------|
| 1 | `[Watermark Config]` 존재 | Mode B-3 | **권장** |
| 2 | `🎨 AI Generation` 존재 | Mode B | 표준 |
| 3 | `📷` 또는 `Reference Image` 존재 | Mode A | 허용 |

### Image Mode Normalization

| 모드 | 설명 | 상태 | 비고 |
|------|------|------|------|
| **Mode A** | 참조 이미지 직접 사용 | 허용 | 생성 파이프라인 스킵 (다운로드된 이미지 사용) |
| **Mode B** | AI 생성 (프롬프트에 텍스트 포함) | 표준 | `[Watermark Config]` 없으면 기본 워터마크 적용 |
| **Mode B-2** | AI 배경 생성 + PIL 텍스트 오버레이 | **폐기** | 하위호환 유지되나 신규 사용 금지 |
| **Mode B-3** | AI 텍스트 렌더링 + PIL 워터마크만 | **권장** | `[Watermark Config]` 섹션 포함 시 자동 판별 |

> **실질적 차이:** Mode B와 B-3의 차이는 `[Watermark Config]` 섹션 유무뿐이다. 두 모드 모두 AI가 텍스트를 직접 렌더링한다.

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
    output_dir=f"{project_path}/images/"
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
    prompt="Blog thumbnail, bold Korean text '0세 적금 필수!' occupying 70-80% of image area, subtitle '연 12% 고금리' below main title, warm gradient background, 1:1 ratio, 1024x1024, render exact Korean text characters as specified",
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

## 9-4. Environment Variable Setup

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

## 9-5. Model & Rate Limit Configuration

### Model Configuration

- **Primary model**: `gemini-3-pro-image-preview`
- **Fallback**: 비활성화 (`force_primary_only: true`)
- 3개 모델 슬롯 모두 동일 모델 설정 (`config.yaml` → `gemini.models`)

### Rate Limiting

- **10 requests/minute** (`config.yaml` → `gemini.rate_limit.requests_per_minute`)
- **6초 간격 요청** (`config.yaml` → `gemini.rate_limit.delay_between_requests`)
- Exact quotas/availability vary by account and can change. If you hit limits, lower concurrency in `config.yaml`.

---

## 9-6. Error Handling

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

## 9-6.5. Watermark Specification

| 필드 | 값 |
|------|-----|
| Text | `@money-lab-brian` |
| Position | bottom-center |
| Margin bottom | 60px |
| Font size | 18px (작은 폰트) |
| Font color | `rgba(255,255,255,0.6)` |
| Font family | `Pretendard, Nanum Gothic, sans-serif` |

- PIL `text_overlay.add_watermark_to_image()`로 적용
- `[Watermark Config]`가 이미지 가이드에 명시되면 해당 값이 기본값 오버라이드
- 기본 설정: `config.yaml` → `watermark.*`

---

## 9-7. Verification Checklist

**⚠️ 다음 단계로 진행하기 전에 모든 항목을 확인하세요:**

- [ ] `images/` 디렉토리 존재
- [ ] 모든 이미지 생성 완료 (N/N success)
- [ ] 이미지 수 >= 3 (`config.yaml` → `images.min_count`)
- [ ] 이미지 수 <= 10 (`config.yaml` → `images.max_count`)
- [ ] 모든 파일명 `{NN}_{역할}.png` 형식
- [ ] `01_썸네일.png` 존재
- [ ] 모든 이미지에 워터마크 `@money-lab-brian` 적용
- [ ] 각 이미지 파일 크기 <= 1MB
- [ ] 이미지 품질 확인 (텍스트 렌더링 정상, 1:1 비율)
- [ ] 썸네일(Image 1)에 블로그 제목 텍스트 정확 렌더링

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

이미지 생성 완료 → **[STEP 10: Revision Loop](step10-revise.md)**
