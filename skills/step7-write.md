# STEP 7: Content Writing and Saving

Write the body content according to selected options and save to files.

## Progress Status

```
[STEP 7/8] Content writing ████████████████████████████░ 87%
```

---

## 7-1. Character Count Rules (🚨 CRITICAL!)

### 🚨 MANDATORY: Total 1850 Characters (±100)
- **Minimum**: 1750 characters
- **Maximum**: 1950 characters
- **Target**: 1850 characters
- Including spaces

### Section-by-Section Character Allocation (7-Step Structure)

| Section | Min Chars | Max Chars | Target | Description |
|---------|-----------|-----------|--------|-------------|
| 도입 (Introduction) | 80 | 120 | 100 | Hook + topic intro |
| 문제 제기 (Problem) | 120 | 180 | 150 | Why this matters |
| 핵심 정보 1 | 280 | 380 | 330 | First key point |
| 핵심 정보 2 | 280 | 380 | 330 | Second key point |
| 핵심 정보 3 | 280 | 380 | 330 | Third key point |
| 실용 팁 (Tips) | 200 | 300 | 250 | Practical advice |
| 마무리 (Closing) | 100 | 160 | 130 | CTA + summary |
| **TOTAL** | **1340** | **1900** | **1620+** | **Must reach 1750+ total** |

⚠️ **IMPORTANT**: Each core section (핵심 정보 1,2,3) MUST be 280+ characters. Short sections will fail validation. If you write less than 1750 characters total, ADD more content to the core information sections.

### Excluded from Count
- All HTML tags (`<h2>`, `<p>`, `<table>`, `<blockquote>`, etc.)
- Image placeholders (`[이미지 N 삽입]`)
- CSS style code
- Hashtag list

### Included in Count
- Body text (intro, core content, closing)
- Text content inside tables
- CTA text
- All actual content text

### Python Character Validation

```python
from scripts.validator import validate_char_count, print_validation_report

result = validate_char_count(html_content)
# result.is_valid: True/False
# result.char_count: Actual character count
# result.message: Status message
```

---

## 7-1b. Readability Rules (가독성 규칙)

### Line Break Rules (줄바꿈 규칙)
1. **문장 단위 (1 newline)**: 한 문장 최대 50~60자, 문장 끝에 `<br>` 1개
2. **문단 단위 (2 newlines)**: 문단은 200자 내외, 문단 사이 빈 줄 1개 (`<br><br>` 또는 `</p>\n\n<p>`)

### Font Size Guide (폰트 크기 가이드)
| 용도 | HTML | 크기 |
|------|------|------|
| 제목 | `<h1>` 또는 `<p style="font-size:28px;font-weight:bold;">` | 28px |
| 중제목 | `<h2>` 또는 `<p style="font-size:24px;font-weight:bold;">` | 24px |
| 소제목 | `<h3>` 또는 `<p style="font-size:19px;font-weight:bold;">` | 19px |
| 본문 | `<p>` | 16px |
| 각주/출처 | `<span style="font-size:11px;color:#888;">` | 11px |

### ❌ BAD Example (줄바꿈 없음, 긴 문장)
```html
<p>육아휴직은 근로자가 자녀를 양육하기 위해 사용하는 휴직 제도입니다. 2026년부터 급여가 인상되며 최대 월 250만원까지 지급됩니다. 신청 조건은 고용보험 가입 180일 이상이며 신청 방법은 고용센터 방문 또는 온라인으로 가능합니다.</p>
```
**문제점**: 줄바꿈 없음, 60자 초과 문장, 폰트 크기 1종류

### ✅ GOOD Example (적절한 줄바꿈, 다양한 폰트)
```html
<p style="font-size:24px;font-weight:bold;">육아휴직이란?</p>

<p>근로자가 자녀를 양육하기 위해 사용하는 휴직 제도입니다.<br>
만 8세 이하 자녀가 있는 근로자라면 누구나 신청할 수 있어요.</p>

<p style="font-size:19px;font-weight:bold;">2026년 핵심 변경사항</p>

<p>급여가 인상되어 최대 월 250만원까지 지급됩니다.<br>
육아휴직 기간도 최대 1년 6개월로 연장되었습니다.<br>
부부 동시 사용도 가능해져 더욱 유연해졌어요.</p>

<p><span style="font-size:11px;color:#888;">출처: 고용노동부 2025년 발표</span></p>
```
**장점**: 문장당 50자 이내 + `<br>`, 문단 200자 내외 + 빈 줄, 5가지 폰트 크기

### Visual Rhythm Checklist
- [ ] 모든 문장 50~60자 이내?
- [ ] 문장 끝마다 `<br>` 처리?
- [ ] 문단 사이 빈 줄(2 newlines) 있음?
- [ ] 제목(28px), 중제목(24px), 소제목(19px), 본문(16px), 각주(11px) 골고루 사용?

---

## 7-2. HTML Format Guide

본문.html is written as a **complete HTML file**.
Open in browser, select all (Cmd+A) → copy (Cmd+C) → paste into Naver Blog (Cmd+V) to preserve formatting.

### HTML Tag Mapping (폰트 크기 필수 준수!)

| 용도 | HTML Tag | 크기 |
|------|----------|------|
| 제목 | `<p style="font-size:28px;font-weight:bold;">` | 28px |
| 중제목 | `<p style="font-size:24px;font-weight:bold;">` | 24px |
| 소제목 | `<p style="font-size:19px;font-weight:bold;">` | 19px |
| 본문 | `<p>` (기본 16px) | 16px |
| 각주/출처 | `<span style="font-size:11px;color:#888;">` | 11px |
| 인용문 | `<blockquote style="border-left:4px solid #ccc;padding-left:16px;color:#666;">` | - |
| 강조 인용 | `<blockquote style="background:#f0f7ff;padding:16px;border-radius:8px;">` | - |
| 구분선 | `<hr style="border:none;border-top:1px solid #ddd;margin:24px 0;">` | - |
| 이미지 위치 | `<p style="color:#999;text-align:center;">[이미지 N 삽입]</p>` | - |

### Line Break Rules (줄바꿈 규칙)

| 단위 | 규칙 | 처리 방법 |
|------|------|-----------|
| 문장 | 50~60자 최대 | 문장 끝에 `<br>` 1개 |
| 문단 | 200자 내외 | 문단 사이 빈 줄 (`</p>\n\n<p>` 또는 `<br><br>`) |

---

## 7-3. Body Writing

### Using Templates

```python
from scripts.writer import generate_html_content

sections = [
    {"title": "Introduction", "content": "...", "has_image": False},
    {"title": "Core Information 1", "content": "...", "has_image": True},
    {"title": "Core Information 2", "content": "...", "has_image": True},
    # ...
]

html_content = generate_html_content(
    title="{title}",
    sections=sections,
    tags=["tag1", "tag2", ...]
)
```

### Manual Writing Reference (폰트 크기 및 줄바꿈 규칙 적용)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: 'Nanum Gothic', 'Pretendard', sans-serif; line-height: 1.8; max-width: 700px; margin: 0 auto; padding: 20px; font-size: 16px; }
  </style>
</head>
<body>

<!-- 제목: 28px -->
<p style="font-size:28px;font-weight:bold;">{제목}</p>

<p style="color:#999;text-align:center;">[이미지 1 삽입 - 썸네일]</p>

<hr style="border:none;border-top:1px solid #ddd;margin:24px 0;">

<!-- 중제목: 24px -->
<p style="font-size:24px;font-weight:bold;">{중제목}</p>

<!-- 본문: 16px, 문장마다 <br>, 문단 사이 빈 줄 -->
<p>첫 번째 문장은 50자 이내로 작성합니다.<br>
두 번째 문장도 간결하게 작성합니다.<br>
세 번째 문장으로 문단을 마무리합니다.</p>

<p>새로운 문단은 빈 줄 후 시작합니다.<br>
이렇게 가독성을 높일 수 있습니다.</p>

<!-- 소제목: 19px -->
<p style="font-size:19px;font-weight:bold;">{소제목}</p>

<blockquote style="background:#f0f7ff;padding:16px;border-radius:8px;">
"{인용문 내용}"
</blockquote>

<p>{본문 내용}</p>

<!-- 각주: 11px -->
<p><span style="font-size:11px;color:#888;">출처: {출처명}</span></p>

<!-- images, tables, additional sections... -->

<p class="tags">#태그1 #태그2 #태그3 ...</p>

</body>
</html>
```

---

## 7-4. Image Guide Writing (Separate File)

**Important**: Do not include image guides in 본문.html.
All image guides are written separately in the **이미지 가이드.md** file.

### Image Guide Modes

#### 📷 Mode A: Use Reference Image
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {image role description}

📷 Downloaded image: ./images/{filename}
📍 Original source: {URL}
💡 Usage: {direct use / reference layout / reference colors}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 🎨 Mode B: AI Image Generation (Auto-generated via Gemini API)

**Mode B-3 (Recommended)**: AI renders text directly + PIL adds watermark only

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {image role description}

🎨 AI Generation (With Text)

[Korean Description]
{detailed description including text content}

[AI Generation Prompt]
```
Create a professional Korean blog thumbnail.
Background: warm gradient from coral pink (#ff7675) to soft orange (#fdcb6e).
Layout: 16:9 aspect ratio, 1300x885 pixels.

**TEXT RENDERING (MUST INCLUDE)**:
- Main title: Bold white Korean text "육아휴직 완벽 가이드"
  - Position: upper-center (y: 30% from top)
  - Font: Bold sans-serif, 48px equivalent
  - Color: White (#FFFFFF) with subtle drop shadow
- Subtitle: "2026년 핵심 변경사항 총정리"
  - Position: center (y: 50% from top)
  - Font: Medium weight, 28px equivalent
  - Color: White with 90% opacity

Style: Modern, clean, professional Korean blog aesthetic.
NO placeholder text, render actual Korean characters.
```

[Style Guide]
- Colors: {main colors}
- Mood: {mood keywords}
- Format: {infographic/illustration/photo style/flat design}
- Ratio: {16:9 / 1:1 / 4:3}

[Watermark Config]
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 60
- watermark_font_size: 18
- watermark_font_color: "rgba(255,255,255,0.6)"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 🚨 Text Rendering Checklist (AI 프롬프트 필수 요소)
- [ ] Main title text specified with **exact Korean characters** (e.g., "육아휴직 완벽 가이드")
- [ ] Position specified (upper/center/lower + percentage from top)
- [ ] Font style specified (bold/medium/light, sans-serif)
- [ ] Color specified (hex code + opacity if needed)
- [ ] "NO placeholder text, render actual Korean characters" instruction included
- [ ] Subtitle (if any) with same level of detail

### Example: Complete Thumbnail Prompt
```
Create a professional Korean economy blog thumbnail.
Background: deep blue (#1a365d) to teal (#38b2ac) gradient.
Layout: 16:9 aspect ratio (1300x885 pixels).

**TEXT RENDERING (CRITICAL)**:
- Main title: "0세 적금 필수 가이드"
  - Position: upper third (y: 25% from top), centered horizontally
  - Font: Extra bold Korean sans-serif (Pretendard or similar), 52px
  - Color: Bright yellow (#ffd93d) with 2px black outline
  - Style: Slight 3D shadow effect for depth

- Subtitle: "2026년 고금리 상품 TOP 5"
  - Position: center (y: 50% from top), centered horizontally
  - Font: Bold sans-serif, 32px
  - Color: White (#ffffff)

- Accent: Baby icon or savings jar illustration on right side

Style: Modern fintech aesthetic, trustworthy, eye-catching.
IMPORTANT: Render actual Korean text characters, NOT placeholders or romanization.
```

**Key Points:**
- `main_text`, `sub_text` → Included in AI prompt (Gemini renders directly)
- `watermark_*` → Processed by PIL only

**Gemini API Auto-Generation**:
Mode B images are automatically generated via Gemini API.
After writing the prompt, images are saved to `./images/` folder without manual work.

#### 🔷 Mode C: SVG Image Generation Guide
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {image role description}

🔷 SVG Generation

[Image Description]
{detailed description of image content}

[SVG Guidance]
- Canvas size: {width}x{height}
- Background color: {hex color code}
- Key elements:
  1. {element1}: {position}, {size}, {color}
  2. {element2}: {position}, {size}, {color}

[Color Palette]
- Main: {hex}
- Point: {hex}
- Background: {hex}

[Save Path]
./images/{filename}.svg
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7-5. Tag Generation

- Auto-generate 8~10 tags
- Core keywords + related keywords
- Start with # symbol

```
#육아휴직 #육아휴직급여 #2026육아휴직 #육아휴직신청 #출산휴가 #부모급여 #워킹맘 #워킹대디
```

---

## 7-6. Auto-Generate Images via Gemini API

Mode B (🎨 AI Generation) images are automatically generated via Gemini API.

### New: AI Text Rendering + Watermark Pipeline (Recommended)

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

```python
from scripts.image_pipeline import ImagePipeline
from scripts.prompt_converter import WatermarkConfig

# Initialize pipeline
pipeline = ImagePipeline()

# Example: Generate thumbnail with AI-rendered text + watermark
result = await pipeline.generate_with_watermark(
    prompt="Blog thumbnail, bold Korean text '0세 적금 필수!' in upper third, subtitle '연 12% 고금리' in center, warm gradient background, 16:9",
    output_path="./images/01_썸네일.png",
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

### Legacy: Generate Images with Python

```python
from scripts.gemini_image import GeminiImageGenerator
from scripts.prompt_converter import generate_image_prompts_for_batch

# Extract prompts from image guide
with open("이미지 가이드.md", "r", encoding="utf-8") as f:
    image_guide_content = f.read()

prompts = generate_image_prompts_for_batch(image_guide_content)
# [{"prompt": "...", "filename": "01_썸네일.png"}, ...]

# Batch generate via Gemini API
generator = GeminiImageGenerator()
result = await generator.generate_batch(
    prompts=prompts,
    output_dir="./images/"
)

print(result.summary())
# 📊 Batch generation result: 5/5 success (100.0%), elapsed: 25.3s
```

### Batch Generate with Watermark

```python
from scripts.image_pipeline import ImagePipeline

# Initialize pipeline
pipeline = ImagePipeline()

# Process entire image guide - AI renders text, PIL adds watermark
with open("이미지 가이드.md", "r", encoding="utf-8") as f:
    image_guide_content = f.read()

result = await pipeline.process_image_guide(
    image_guide_content=image_guide_content,
    output_dir="./images/",
    use_text_overlay=True  # Enables watermark for Mode B-3 items
)

print(result.summary())
# 📊 Pipeline result: 5/5 success, 3 with watermark
```

### Environment Variable Setup (Required)

```bash
export GOOGLE_API_KEY="your-api-key"
```

### Generation Limits

- **15 requests per minute** limit (auto-delay applied)
- **500 images/day** free quota (gemini-2.0-flash-exp)
- Auto-fallback to imagen-3.0 when quota exceeded

### Text Overlay Dependencies

For SVG to PNG conversion, install one of:
```bash
pip install cairosvg  # Recommended
# or
sudo apt install librsvg2-bin  # rsvg-convert
# or
pip install svglib reportlab  # Fallback
```

---

## 7-7. File Saving

### Save Path
```
./경제 블로그/YYYY-MM-DD/topic-name/
├── 본문.html
├── 이미지 가이드.md
├── 참조.md
└── images/
    ├── 01_썸네일.png      ← Gemini auto-generated
    ├── 02_비교표.png       ← Gemini auto-generated
    └── ...
```

### Save with Python

```python
from scripts.writer import save_blog_files

files = save_blog_files(
    project_path=project_path,
    html_content=html_content,
    image_guide=image_guide_md,
    references=references_md,
    validate=True  # Auto character count validation
)
```

---

## 7-8. Character Count Validation and Adjustment

Validate character count after writing:

```python
from scripts.validator import print_validation_report

result = print_validation_report(html_content)

if not result.is_valid:
    # Adjustment needed when over/under
    print(suggest_adjustment(result))
```

### When Over Character Limit
- Remove redundant content
- Simplify supplementary explanations
- Delete unnecessary modifiers

### When Under Character Limit
- Add specific examples to core information sections
- Expand practical tips section
- Add related statistics or data

---

## Next Step

File saving complete → **[STEP 8: Revision Loop](step8-revise.md)**
