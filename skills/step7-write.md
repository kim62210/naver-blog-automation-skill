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
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {image role description}

📷 Downloaded image: ./images/{filename}
📍 Original source: {URL}
💡 Usage: {direct use / reference layout / reference colors}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 🎨 Mode B: AI Image Generation (Auto-generated via Gemini API)
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {image role description}

🎨 AI Generation

[Korean Description]
{detailed description of image content in Korean}

[AI Generation Prompt]
{English prompt - auto-generated via Gemini API}

[Style Guide]
- Colors: {main colors}
- Mood: {mood keywords}
- Format: {infographic/illustration/photo style/flat design}
- Ratio: {16:9 / 1:1 / 4:3}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

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

### New: Background + Text Overlay Pipeline (Recommended)

For better Korean text quality, use the new pipeline:
1. Generate background image via Gemini (no text)
2. Add text overlay via SVG composition
3. Export final PNG

```python
from scripts.image_pipeline import ImagePipeline
from scripts.prompt_converter import TextOverlayConfig

# Initialize pipeline
pipeline = ImagePipeline()

# Example: Generate thumbnail with text overlay
result = await pipeline.generate_with_text_overlay(
    prompt="Blog thumbnail background, finance concept, warm gradient, NO TEXT",
    output_path="./images/01_썸네일.png",
    text_config=TextOverlayConfig(
        main_text="0세 적금 필수!",
        sub_text="연 12% 고금리",
        position="center",
        font_size=48,
        font_color="#FFFFFF",
        shadow=True
    )
)
# Result: Background generated → Text overlay applied → Final PNG saved
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

### Batch Generate with Text Overlay

```python
from scripts.image_pipeline import ImagePipeline

# Initialize pipeline
pipeline = ImagePipeline()

# Process entire image guide with text overlay support
with open("이미지 가이드.md", "r", encoding="utf-8") as f:
    image_guide_content = f.read()

result = await pipeline.process_image_guide(
    image_guide_content=image_guide_content,
    output_dir="./images/",
    use_text_overlay=True  # Enable SVG text overlay for Mode B-2 items
)

print(result.summary())
# 📊 Pipeline result: 5/5 success, 3 with text overlay
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
