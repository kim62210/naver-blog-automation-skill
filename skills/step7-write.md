# STEP 7: Content Writing and Saving

Write the body content according to selected options and save to files.

## Progress Status

```
[STEP 7/9] Content writing █████████████████████░░░░░░░░ 77%
```

---

## 7-1a. 2-Step Writing Workflow (🚨 CRITICAL - READ FIRST!)

### Why This Matters

When you write HTML directly, you tend to count the total string length (including HTML tags) as the character count. This causes the **actual text content to be only 800-1000 characters** when the target is 1850-1950.

**Solution**: Write pure text first → Verify character count → Convert to HTML

### Step 1: Write Plain Text First (순수 텍스트 먼저 작성)

1. Write the entire blog post as **pure text** (no HTML tags, no formatting)
2. Include `[이미지 N 삽입]` placeholders where images go
3. Target: **1850-1950 characters** (including spaces)
4. Count characters after each section to track progress

### Step 2: Verify Character Count (글자수 확인)

Before converting to HTML, verify your plain text meets the target:

```python
plain_text = """(your plain text content here)"""
from scripts.validator import count_content_chars

char_count = count_content_chars(plain_text)
print(f"Plain text (counted text only): {char_count} chars")  # Should be 1850-1950
```

If under 1850: Add more content to core sections
If over 1950: Trim redundant phrases

### Step 3: Convert to HTML (HTML 변환)

Only after reaching 1850-1950 characters:
1. Add HTML structure and tags
2. Apply font sizes (28px title, 24px headings, 19px subheadings, 16px body)
3. Add line breaks (`<br>`) per readability rules
4. The character count should remain the same (only text counts)

### ✅ Plain Text 작성 예시

```
[도입부 - 120자]
육아휴직이 2026년부터 크게 달라집니다. 급여 인상, 기간 연장까지.
워킹맘, 워킹대디라면 반드시 알아야 할 핵심 변경사항을 정리했습니다.

[이미지 1 삽입]

[문제 제기 - 180자]
기존 육아휴직 제도의 가장 큰 문제는 급여였습니다. 통상임금의
80%만 지급되던 급여로는 생활이 어려워 많은 부모들이 휴직을
포기해야 했죠. 하지만 2026년부터 상황이 완전히 달라집니다.

[핵심 정보 1 - 400자]
첫 번째 변화는 급여 인상입니다. 기존 통상임금 80%에서 100%로
상향됩니다. 상한액도 월 150만원에서 250만원으로 크게 올랐어요.
이제 육아휴직 중에도 경제적 부담 없이 아이와 시간을 보낼 수
있게 되었습니다.

특히 첫 3개월은 통상임금의 100%를 그대로 받을 수 있어요.
4개월째부터는 80%가 적용되지만, 상한액 인상으로 대부분의
근로자가 혜택을 체감할 수 있습니다.

맞벌이 부부의 경우 부부 동시 사용도 가능해져 한층 유연해졌어요.
아빠 육아휴직 인센티브도 강화되어 남성 육아휴직 사용률도
높아질 전망입니다.

[이미지 2 삽입]

[핵심 정보 2 - 400자]
(두 번째 핵심 내용을 400자 내외로 작성...)

[핵심 정보 3 - 400자]
(세 번째 핵심 내용을 400자 내외로 작성...)

[이미지 3 삽입]

[실용 팁 - 300자]
(실용적인 조언을 300자 내외로 작성...)

[마무리 - 130자]
(마무리 및 CTA를 130자 내외로 작성...)
```

### Workflow Summary

```
┌─────────────────────────────────────────────────────────┐
│                  2-Step Writing Workflow                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Step 1: 순수 텍스트 작성                                │
│  ├── HTML 태그 없이 본문만 작성                          │
│  ├── [이미지 N 삽입] 플레이스홀더 포함                   │
│  └── 목표: 1850-1950자                                  │
│                                                         │
│          ↓                                              │
│                                                         │
│  Step 2: 글자수 검증                                    │
│  ├── len(plain_text) 확인                               │
│  ├── 1850 미만 → 핵심 정보 섹션 보강                    │
│  └── 1950 초과 → 불필요한 수식어 삭제                   │
│                                                         │
│          ↓                                              │
│                                                         │
│  Step 3: HTML 변환                                      │
│  ├── 폰트 크기 규칙 적용 (28/24/19/16/11px)             │
│  ├── 줄바꿈 규칙 적용 (<br>)                            │
│  └── 최종 본문.html 생성                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 7-1. Character Count Rules (🚨 CRITICAL!)

### 🚨 MANDATORY: Total 1900 Characters (±50)
- **Minimum**: 1850 characters
- **Maximum**: 1950 characters
- **Target**: 1900 characters
- Including spaces

### Section-by-Section Character Allocation (7-Step Structure)

| Section | Min Chars | Max Chars | Target | Description |
|---------|-----------|-----------|--------|-------------|
| 도입 (Introduction) | 120 | 160 | 140 | Hook + topic intro |
| 문제 제기 (Problem) | 170 | 230 | 200 | Why this matters |
| 핵심 정보 1 | 340 | 400 | 370 | First key point (detailed!) |
| 핵심 정보 2 | 340 | 400 | 370 | Second key point (detailed!) |
| 핵심 정보 3 | 340 | 400 | 370 | Third key point (detailed!) |
| 실용 팁 (Tips) | 270 | 330 | 300 | Practical advice |
| 마무리 (Closing) | 130 | 170 | 150 | CTA + summary |

⚠️ **IMPORTANT**: If you’re under the minimum, expand 핵심 정보 1~3 first. If you’re over the maximum, trim redundancy there first.

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

### 🚨 Image Prompt Length Requirement (1000자+ per image)

**Each image section MUST be at least 1000 characters total.** This ensures enough detail for high-quality AI image generation.

#### Required Components per Image Section

| Component | Target Length | Purpose |
|-----------|---------------|---------|
| **Korean Description** | 100-150자 | What the image represents, key visual elements |
| **AI Generation Prompt** | 400-500자 | Detailed prompt with text, colors, layout |
| **Style Guide** | 100-150자 | Colors (HEX), mood, format, ratio |
| **Watermark Config** | 150-200자 | 6 required fields for watermark |
| **TOTAL** | **850-1000자+** | Minimum per image section |

#### Example: Complete 1000+ Character Image Section

```markdown
## [Image 1] 썸네일

🎨 AI Generation (With Text)

[Korean Description]
ETF 개념을 표현하는 블로그 썸네일. 다양한 자산(주식, 채권, 금)이 하나의 ETF 상자로 모이는 모습.
투자 초보자도 쉽게 이해할 수 있는 시각적 메타포를 사용하여 분산투자의 핵심을 전달한다.

[AI Generation Prompt]
```
Blog thumbnail image, ETF investment concept,
diverse investment icons (stocks charts showing upward trends, golden bonds certificates,
shiny gold coins and bars) flowing into one central ETF container box with modern design,
bold modern sans-serif Korean font text "주식보다 쉬운 ETF" in upper third,
subtitle "소액으로 분산투자" in clean modern font below,
navy blue (#1a365d) to sky blue (#63b3ed) gradient background,
floating investment symbols around the ETF box,
eye-catching modern design with subtle shadows and depth,
high contrast readable text with slight glow effect,
professional Korean financial blog style,
clean minimalist layout with focus on central message,
16:9 ratio, 1300x885 pixels
```

[Style Guide]
- Color: Navy blue (#1a365d) + Sky blue (#63b3ed) gradient
- Mood: Professional, trustworthy, modern, approachable
- Format: Modern thumbnail design with central focus
- Ratio: 16:9

[Watermark Config]
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 60
- watermark_font_size: 18
- watermark_font_color: "rgba(255,255,255,0.6)"
- watermark_font_family: "Pretendard, Nanum Gothic, sans-serif"
```

#### Checklist for Each Image Section

- [ ] Korean Description: 100자 이상, 이미지가 무엇을 표현하는지 명확히
- [ ] AI Prompt: 400자 이상, 모든 시각 요소 상세 설명
- [ ] Exact Korean text in quotes (예: "주식보다 쉬운 ETF")
- [ ] Position specified for all text elements
- [ ] Color codes in HEX format (예: #1a365d)
- [ ] Style keywords (3-4개 mood 키워드)
- [ ] All 6 watermark config fields included
- [ ] Total section length: 1000자+

---

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
Render the exact Korean text characters as specified.
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

**⚠️ WARNING: Without these elements, Gemini will generate images WITHOUT text!**

| Required Element | Example | Why It Matters |
|-----------------|---------|----------------|
| **Exact Korean text** | `"육아휴직 완벽 가이드"` | AI needs literal characters to render |
| **Position** | `upper-center (y: 25%)` | Prevents text overlap issues |
| **Font size** | `48-52px equivalent` | Ensures readability |
| **Color** | `#FFFFFF with drop shadow` | Contrast against background |
| **Explicit instruction** | `"Render exact Korean text as specified"` | Ensures text accuracy |

**Checklist:**
- [ ] Main title text specified with **exact Korean characters** (e.g., "육아휴직 완벽 가이드")
- [ ] Position specified (upper/center/lower + percentage from top)
- [ ] Font style specified (bold/medium/light, sans-serif)
- [ ] Color specified (hex code + opacity if needed)
- [ ] Explicit instruction to render exact Korean text included
- [ ] Subtitle (if any) with same level of detail

### ❌ Common Mistakes vs ✅ Correct Approach

**❌ WRONG (텍스트 누락됨):**
```
Blog thumbnail, baby savings concept, warm gradient background, 16:9
```
→ Result: Background image only, NO text rendered

**✅ CORRECT (텍스트 포함됨):**
```
Create a professional Korean blog thumbnail.
Background: warm gradient from coral pink to soft orange.

**TEXT RENDERING (CRITICAL)**:
- Main title: "0세 적금 필수 가이드"
  - Position: upper-center (y: 25% from top)
  - Font: Extra bold Korean sans-serif, 52px
  - Color: White (#FFFFFF) with black outline
- Subtitle: "2026년 고금리 상품 TOP 5"
  - Position: center (y: 50% from top)
  - Font: Bold sans-serif, 32px
  - Color: White

IMPORTANT: Render the exact Korean text characters as specified.
```
→ Result: Complete thumbnail with Korean title rendered

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
IMPORTANT: Render the exact Korean text characters as specified above.
```

**Key Points:**
- `main_text`, `sub_text` → Included in AI prompt (Gemini renders directly)
- `watermark_*` → Processed by PIL only

**Gemini API Auto-Generation**:
Mode B images are automatically generated via Gemini API.
After writing the prompt, images are saved to `./images/` folder without manual work.

---

## 7-5. Tag Generation

- Auto-generate 8~10 tags
- Core keywords + related keywords
- Start with # symbol

```
#육아휴직 #육아휴직급여 #2026육아휴직 #육아휴직신청 #출산휴가 #부모급여 #워킹맘 #워킹대디
```

---

## 7-6. File Saving

### Save Path
```
./경제 블로그/YYYY-MM-DD/topic-name/
├── 본문.html
├── 이미지 가이드.md
├── 참조.md
└── images/           ← Created in STEP 8
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

## 7-7. Character Count Validation and Adjustment

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

File saving complete → **[STEP 8: 🖼️ Image Generation (MANDATORY)](step8-image.md)**

> ⚠️ **중요**: 이미지 생성 단계는 건너뛸 수 없습니다. STEP 8에서 반드시 이미지를 생성해야 합니다.
