# STEP 7: Content Writing and Saving

Write the body content according to selected options and save to files.

## Progress Status

```
[STEP 7/8] Content writing ████████████████████████████░ 87%
```

---

## 7-1. Character Count Rules (Important!)

### Target
- **Strictly follow 본문.html: Around 1850 characters**
- **Allowed range: 1800~1900 characters (±50)**
- Including spaces

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

## 7-2. HTML Format Guide

본문.html is written as a **complete HTML file**.
Open in browser, select all (Cmd+A) → copy (Cmd+C) → paste into Naver Blog (Cmd+V) to preserve formatting.

### HTML Tag Mapping

| Element | HTML Tag |
|---------|----------|
| Main heading | `<h2 style="font-size:24px;font-weight:bold;">` |
| Subheading | `<h3 style="font-size:18px;font-weight:bold;">` |
| Minor heading | `<h4 style="font-size:15px;font-weight:bold;">` |
| Blockquote | `<blockquote style="border-left:4px solid #ccc;padding-left:16px;color:#666;">` |
| Highlighted quote | `<blockquote style="background:#f0f7ff;padding:16px;border-radius:8px;">` |
| Extra large text | `<p style="font-size:24px;font-weight:bold;text-align:center;">` |
| Small text | `<p style="font-size:12px;color:#888;">` |
| Divider | `<hr style="border:none;border-top:1px solid #ddd;margin:24px 0;">` |
| Image position | `<p style="color:#999;text-align:center;">[이미지 N 삽입]</p>` |

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

### Manual Writing Reference

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: 'Noto Sans KR', sans-serif; line-height: 1.8; max-width: 700px; margin: 0 auto; padding: 20px; }
    /* ... styles omitted ... */
  </style>
</head>
<body>

<h1>{title}</h1>

<div class="image-placeholder">[이미지 1 삽입 - 썸네일]</div>

<hr>

<h2>{subheading}</h2>

<blockquote>
"{quote text}"
</blockquote>

<p>{body content}</p>

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
```md
## [Image N] {image role description}

### 📷 Reference Image
- File: ./images/{filename}
- Source: {URL}
- Usage: direct use / layout reference / color reference
```

#### 🎨 Mode B: AI Image Generation (Auto-generated via Gemini API)
````md
## [Image N] {image role description}

### 🎨 AI Generation Prompt

**Korean Description:**
{detailed description of image content in Korean}

**AI Generation Prompt:**
```text
{English prompt}
```

**Style:**
- Colors: {main colors}
- Mood: {mood keywords}
- Format: {infographic/illustration/photo style/flat design}
- Ratio: {16:9 / 1:1 / 4:3}
````

**Gemini API Auto-Generation**:
Mode B images are automatically generated via Gemini API.
After writing the prompt, images are saved to `./images/` folder without manual work.

#### 🎨 Mode B-2: Background Only + Text Overlay (Recommended for thumbnails)

**제목 단어화 규칙**: 긴 제목을 2~3개 핵심 단어로 압축하여 가독성을 높입니다.
- "2026년 0세 적금 금리 비교 완벽 가이드" → "0세 적금 필수!"
- "육아휴직 급여 신청 방법 총정리" → "육아휴직 급여"

**썸네일 레이아웃 (1300×885)**:
- main_text: Y 35% (상단 1/3), 64px Bold
- sub_text: Y 50% (중앙), 32px Regular
- watermark: 하단에서 60px 위, 18px Light

````md
## [Image N] {image role description}

### 🎨 AI Generation (Background Only)

**Korean Description:**
{배경 설명 - 텍스트 제외}

**AI Generation Prompt (Background Only):**
```text
{배경 전용 프롬프트 - NO TEXT 포함}
```

**[Text Overlay Config]**
# 메인 텍스트 (상단 1/3, 중앙)
- main_text: "{핵심 키워드 2~3개}"
- main_text_y: "35%"
- font_size: 64
- font_weight: "bold"
- font_color: "#FFFFFF"
- shadow: true
- shadow_offset: 2
- shadow_color: "rgba(0,0,0,0.5)"

# 부제목 (중앙)
- sub_text: "{부제목}"
- sub_text_y: "50%"
- sub_font_size: 32
- sub_font_color: "rgba(255,255,255,0.9)"

# 배경 박스 (선택)
- background_box: true
- background_box_color: "rgba(0,0,0,0.3)"
- background_box_padding: 20

# 워터마크 (필수)
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 60
- watermark_font_size: 18
- watermark_font_color: "rgba(255,255,255,0.6)"
````

**본문 이미지용 Text Overlay Config:**
````md
**[Text Overlay Config]**
# 타이틀 (상단)
- main_text: "{이미지 제목}"
- main_text_y: "10%"
- font_size: 32
- font_weight: "bold"
- font_color: "#333333"

# 워터마크 (필수)
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 30
- watermark_font_size: 14
- watermark_font_color: "rgba(0,0,0,0.4)"
````

#### 🔷 Mode C: SVG Image Generation Guide
```md
## [Image N] {image role description}

### 🔷 SVG Generation Guide

**Canvas:** {width}x{height}
**Background:** {hex color code}

**Elements:**
1. {element1}: {position}, {size}, {color}
2. {element2}: {position}, {size}, {color}

**Save Path:** ./images/{filename}.svg
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

## 7-6. 이미지 자동 생성 (필수 단계)

⚠️ **필수**: 본문 작성 후 모든 이미지는 이 단계에서 자동 생성됩니다.
이미지 가이드.md 작성이 완료되면, 반드시 이미지 파이프라인을 실행하여 이미지를 생성해야 합니다.

### 생성 파이프라인

```
이미지 가이드.md 파싱
       ↓
Gemini API (배경 생성, NO TEXT)
       ↓
PIL 텍스트 오버레이
       ↓
./images/*.png 저장
```

### 이미지 타입별 생성 방식

| 이미지 타입 | 생성 방식 | 비고 |
|------------|----------|------|
| **썸네일** | Mode B-2 (배경 + 텍스트 오버레이) | **필수** - 항상 텍스트 오버레이 적용 |
| **본문 이미지** | Mode B (AI 생성) 또는 Mode B-2 | 텍스트 필요시 B-2 사용 |
| **인포그래픽** | Mode C (SVG) | svg-canvas-mcp로 자동 생성 |
| **참조 이미지** | Mode A (수집) | 웹에서 수집한 이미지 사용 |

### 자동 실행 (필수)

본문과 이미지 가이드 작성 후 반드시 아래 코드를 실행합니다:

```python
from scripts.image_pipeline import ImagePipeline

# 이미지 가이드 파일 읽기
with open(f"{project_path}/이미지 가이드.md", "r", encoding="utf-8") as f:
    image_guide_content = f.read()

# 파이프라인 실행 (필수)
pipeline = ImagePipeline()
result = await pipeline.process_image_guide(
    image_guide_content=image_guide_content,
    output_dir=f"{project_path}/images/",
    use_text_overlay=True  # 항상 True
)

# 결과 확인
print(result.summary())
# 📊 Pipeline result: 5/5 success, 3 with text overlay

# 실패한 이미지 처리
if result.failed_count > 0:
    print(f"⚠️ {result.failed_count}개 이미지 생성 실패")
    for failed in result.failed_items:
        print(f"  - {failed.filename}: {failed.error}")
    # 재시도 또는 사용자에게 알림
```

### 단일 이미지 생성 (텍스트 오버레이)

개별 이미지 생성이 필요한 경우:

```python
from scripts.image_pipeline import ImagePipeline
from scripts.prompt_converter import TextOverlayConfig

pipeline = ImagePipeline()

# 썸네일 생성 예시 (새로운 확장 형식)
result = await pipeline.generate_with_text_overlay(
    prompt="Blog thumbnail background, finance concept, warm gradient, NO TEXT",
    output_path="./images/01_썸네일.png",
    text_config=TextOverlayConfig(
        # 메인 텍스트 (상단 1/3)
        main_text="0세 적금 필수!",
        main_text_y="35%",
        font_size=64,
        font_weight="bold",
        font_color="#FFFFFF",
        shadow=True,
        shadow_offset=2,

        # 부제목 (중앙)
        sub_text="연 12% 고금리",
        sub_text_y="50%",
        sub_font_size=32,
        sub_font_color="rgba(255,255,255,0.9)",

        # 배경 박스
        background_box=True,
        background_box_color="rgba(0,0,0,0.3)",

        # 워터마크 (필수)
        watermark_text="@money-lab-brian",
        watermark_margin_bottom=60,
        watermark_font_size=18,
        watermark_font_color="rgba(255,255,255,0.6)",
    )
)
```

### 환경 변수 설정 (필수)

```bash
export GOOGLE_API_KEY="your-api-key"
# 또는
export GEMINI_API_KEY="your-api-key"
```

### 생성 제한

- **15 requests per minute** limit (자동 딜레이 적용)
- **500 images/day** 무료 할당량 (gemini-2.0-flash-exp)
- 할당량 초과시 imagen-3.0으로 자동 전환

### 텍스트 오버레이 의존성

```bash
python3 -m pip install -r requirements.txt
# 또는 최소 설치
python3 -m pip install pillow
```

> 한글 텍스트가 깨지면 폰트 경로 설정:
> `export BLOG_FONT_PATH="/path/to/NanumGothic.ttf"`

### 완료 확인

이미지 생성이 완료되면 다음을 확인합니다:
- [ ] `./images/` 폴더에 PNG 파일 생성됨
- [ ] 썸네일에 한글 텍스트가 깔끔하게 렌더링됨
- [ ] 모든 이미지가 이미지 가이드와 일치함

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
