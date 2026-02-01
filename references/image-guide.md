# Image Guide Creation

Guide images for blog posts using one of **3 methods**.
The image guide is written in a separate **이미지 가이드.md** file, not included in 본문.html.

---

## 📐 Naver Blog Image Size Standards

### Required Sizes

| Purpose | Size (px) | Ratio | Description |
|---------|-----------|-------|-------------|
| **Thumbnail (OG Image)** | 1300×885 | 1.47:1 | Displayed in search results, SNS shares |
| **Content Basic Width** | 693×(free) | - | Editor default width |
| **Content Extended Width** | 886×(free) | - | Extended layout width |
| **Square** | 700×700 | 1:1 | Instagram style |
| **Wide Title** | 1920×(free) | - | Full width title |

### Recommended Heights

- **Thumbnail**: 885px (1300×885, approx. 1.47:1 ratio)
- **Content images**: 400~600px
- **Infographics**: 600~1200px (tall vertical format allowed)

---

## 🔤 Naver Blog Font Guide

### Recommended Settings

- **Default font**: Nanum Gothic, Pretendard, sans-serif
- **Base size**: 16px (line-height 180%)
- **Size range**: 12~38px

### Size by Purpose

| Purpose | Size | Style | Use Case |
|---------|------|-------|----------|
| Main title | 28~38px | Bold/Extra Bold | Thumbnail text, main heading |
| Subheading | 22~26px | Bold | Section divider |
| Body | 15~17px | Regular | General content |
| Emphasis | 18~20px | Bold | Key phrases |
| Caption/Source | 12~14px | Light | Image descriptions, sources |

### Font Combination Examples

```
Thumbnail:
- Main: 48px Bold (key keywords)
- Sub: 24px Regular (additional description)

Infographic:
- Title: 28px Bold
- Items: 16px Regular
- Numbers: 32px Bold (emphasis)
```

---

## Core Principles

1. **Provide one of 2 methods for every image position**
   - 🖼️ Mode A: Insert collected reference image directly
   - 🎨 Mode B: Provide AI generation prompt (auto-generated via Gemini API)

2. **AI generation is automatic**
   - Mode B images are automatically generated via Gemini API
   - Just write the prompts and images will be saved to `./images/` folder

3. **Style consistency**
   - Maintain unified color palette within same article
   - Specify color palette at top of 이미지 가이드.md

---

## 🖼️ Mode A: Direct Reference Image Insertion

### Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {image role}

📷 Reference Image:
{image URL}

📍 Source: {source URL}
💡 Usage: {usage method}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Usage Method Options

| Usage Method | Description |
|--------------|-------------|
| Direct use | Insert image directly into blog (cite source) |
| Layout reference | Reference composition/arrangement to create similar |
| Color reference | Reference color palette for different content |
| Style reference | Reference overall design style only |

---

## 🎨 Mode B: AI Image Generation (Gemini API Auto)

> **Automation**: Mode B images are automatically generated via Gemini API.
> Just write the prompt and images will be saved to `./images/` folder without manual generation.
>
> **IMPORTANT (Automation format)**: In the actual `이미지 가이드.md`, put the AI prompt inside a fenced code block (``` ... ```).
> The pipeline extracts the first fenced code block per image section. See `templates/image-guide.md` for a working format.

### Mode B-1: Basic Format (AI generates everything including text)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {image role}

🎨 AI Generation (Gemini Auto)

[Korean Description]
{Describe specifically what to include}

[AI Generation Prompt]
{English prompt - automatically processed by Gemini API}

[Style Guide]
- Color: {color}
- Mood: {mood}
- Format: {format}
- Ratio: {ratio}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Mode B-3: AI Text Rendering + Watermark Only (Recommended for thumbnails)

> **New Workflow**: AI renders text directly in the image. PIL only adds watermark at bottom-center.
> This approach leverages improved AI text rendering capabilities.
>
> **Font Style Guidance for AI Prompts:**
> - Always specify "bold modern sans-serif Korean font" in prompts
> - Request clean, high-contrast text for readability
> - AI handles: main_text (title), sub_text (subtitle)
> - PIL handles: watermark only

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {image role}

🎨 AI Generation (With Text)

[Korean Description]
{이미지 전체 설명 - 텍스트 포함}

[AI Generation Prompt]
{AI가 텍스트까지 렌더링하는 프롬프트}

[Style Guide]
- Color: {color}
- Mood: {mood}
- Format: {format}
- Ratio: {ratio}

[Watermark Config]
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 60
- watermark_font_size: 18
- watermark_font_color: "rgba(255,255,255,0.6)"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Benefits of Mode B-3:**
1. AI handles all text rendering directly
2. Simpler workflow - no complex text overlay configuration
3. Watermark added consistently at bottom-center
4. Faster generation (simpler workflow)

### Gemini API Usage

```python
from scripts.gemini_image import GeminiImageGenerator
from scripts.prompt_converter import generate_image_prompts_for_batch

# Extract prompts from image guide and auto-generate
prompts = generate_image_prompts_for_batch(image_guide_content)
generator = GeminiImageGenerator()
result = await generator.generate_batch(prompts, "./images/")
```

### Limits & Fallback (Config-driven)

- Rate limiting/delay is configured in `config.yaml` (`gemini.rate_limit.*`) and enforced by the generator.
- Model fallback order is configured in `config.yaml` (`gemini.models.primary` → `fallback` → `fallback_2`).
- Exact quotas/availability vary by account and can change.

---

## Image Type Prompt Templates

### 1. Thumbnail Image

#### Recommended: AI Text Rendering + Watermark
```
[AI Generation Prompt]
Blog thumbnail image, {topic keywords} concept,
{core object} as main element,
bold modern sans-serif Korean font text "{제목 텍스트}" in upper third,
subtitle "{부제목}" in modern clean font in center,
{color} gradient background,
eye-catching modern design, high contrast text, 16:9 ratio

[Style Guide]
- Color: {main color} + {accent color} gradient
- Mood: Eye-catching and click-inducing
- Format: Modern thumbnail design
- Ratio: 16:9

[Watermark Config]
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 60
- watermark_font_size: 18
- watermark_font_color: "rgba(255,255,255,0.6)"
```

**Example (AI Text Rendering + Watermark):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Thumbnail] 0세 적금 고금리 안내

🎨 AI Generation (With Text)

[Korean Description]
아기 손과 돼지저금통이 있는 따뜻한 썸네일 이미지, "0세 적금 필수!" 텍스트 포함

[AI Generation Prompt]
Blog thumbnail image, baby savings account concept,
cute piggy bank and baby hands as main elements,
bold modern sans-serif Korean font text "0세 적금 필수!" in upper third,
subtitle "연 12% 고금리" in clean modern font in center,
warm yellow to soft orange gradient background,
eye-catching modern design, high contrast readable text, 16:9 ratio

[Style Guide]
- Color: Warm yellow + Soft orange gradient
- Mood: Warm, friendly, trustworthy
- Format: Modern thumbnail design
- Ratio: 16:9

[Watermark Config]
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 60
- watermark_font_size: 18
- watermark_font_color: "rgba(255,255,255,0.6)"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2. Infographic (Comparison/Data)

```
[AI Generation Prompt]
Clean infographic, {data type} comparison chart,
{comparison items} side by side,
{numbers/text to emphasize} highlighted,
{color} color scheme, minimal flat design,
white background, {ratio} ratio

[Style Guide]
- Color: {two contrasting colors}
- Mood: Clean with clear information delivery
- Format: Flat design infographic
- Ratio: 16:9 or 4:3
```

**Example:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image 2] 일반 적금 vs 0세 적금 금리 비교

🎨 Generation Required

[Korean Description]
막대그래프로 일반 적금(3~4%)과 0세 적금(7~12%)의 금리 차이를 시각화.
0세 적금 막대가 2~3배 더 높게 표현되어 차이가 확연히 보임.

[AI Generation Prompt]
Clean infographic, interest rate comparison bar chart,
"일반 적금 3-4%" vs "0세 적금 7-12%" side by side,
dramatic height difference emphasized,
gray and gold color scheme, minimal flat design,
white background, 16:9 ratio

[Style Guide]
- Color: Gray (regular) vs Gold (0세) contrast
- Mood: Clean with clear differences
- Format: Flat design bar chart
- Ratio: 16:9
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3. Process/Procedure Diagram

```
[AI Generation Prompt]
Step-by-step process infographic, {N}-step flow chart,
{each step description} with icons,
connected by arrows, numbered steps,
{color} color scheme, clean minimal style,
white background, {ratio} ratio

[Style Guide]
- Color: {step gradient or unified color}
- Mood: Easy to follow, intuitive
- Format: Flow chart / Step diagram
- Ratio: 16:9 (horizontal) or 9:16 (vertical)
```

**Example:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image 4] 적금 가입 4단계 절차

🎨 Generation Required

[Korean Description]
1. 서류 준비 → 2. 은행 방문/앱 접속 → 3. 계좌 개설 → 4. 자동이체 설정
각 단계를 아이콘과 함께 화살표로 연결한 플로우차트

[AI Generation Prompt]
Step-by-step process infographic, 4-step flow chart,
Step 1: document preparation (paper icon),
Step 2: bank visit or app (building/phone icon),
Step 3: account opening (card icon),
Step 4: automatic transfer setup (sync icon),
connected by arrows, numbered circles,
soft blue and mint color scheme, clean minimal style,
white background, 16:9 ratio

[Style Guide]
- Color: Soft blue + Mint green
- Mood: Clean and easy to follow
- Format: Horizontal flow chart
- Ratio: 16:9
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. Checklist

```
[AI Generation Prompt]
Checklist infographic, {N} items to prepare,
checkbox style with {items},
{color} accent color, clean organized layout,
subtle {background elements} in background,
white background, {ratio} ratio

[Style Guide]
- Color: {check color} + clean background
- Mood: Organized, practical
- Format: Checkbox list
- Ratio: 1:1 or 4:3
```

**Example:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image 5] 준비 서류 체크리스트

🎨 Generation Required

[Korean Description]
적금 가입 시 필요한 서류 4가지를 체크박스 형태로 정리:
□ 아기 기본증명서, □ 가족관계증명서, □ 부모 신분증, □ 아기 도장

[AI Generation Prompt]
Checklist infographic, 4 required documents,
checkbox style with document icons,
"기본증명서, 가족관계증명서, 신분증, 도장" items,
green check accent color, clean organized layout,
subtle paper/document elements in background,
white background, 1:1 ratio

[Style Guide]
- Color: Green check accent + White background
- Mood: Clean and practical
- Format: Checkbox list
- Ratio: 1:1 (square)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5. Emotional/Mood Image

```
[AI Generation Prompt]
{mood} photography style image,
{subject description},
{lighting} lighting, {tones} tones,
{emotion keywords} mood, soft focus background,
{ratio} ratio

[Style Guide]
- Color: {tone description}
- Mood: {emotion keywords}
- Format: Photography style / Illustration
- Ratio: 16:9 or 4:3
```

**Example:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image 6] 마무리 - 가족 사랑 이미지

🎨 Generation Required

[Korean Description]
부모가 신생아의 작은 손을 잡고 있는 따뜻한 이미지.
미래를 위한 저축의 의미를 담은 희망적인 분위기.

[AI Generation Prompt]
Warm family photography style image,
parents holding newborn baby's tiny hand,
soft natural window lighting, warm golden tones,
love and hope mood, soft focus background,
16:9 ratio

[Style Guide]
- Color: Warm golden tones
- Mood: Loving and hopeful
- Format: Photography style
- Ratio: 16:9
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 6. Table Visualization

```
[AI Generation Prompt]
Clean data table visualization,
{rows} rows x {columns} columns comparison table,
headers: {column titles},
{emphasized row/column} highlighted,
{color} color scheme, modern minimal design,
white background, {ratio} ratio

[Style Guide]
- Color: {header color} + {emphasis color}
- Mood: Organized, easy to compare
- Format: Modern table
- Ratio: 16:9
```

---

## Color Palette Guide

### Color Balance Principle (70-25-5 Rule)

```
┌─────────────────────────────────────────┐
│  Main (70%)   │ Background, main areas  │
├─────────────────────────────────────────┤
│  Sub (25%)    │ Emphasis, secondary     │
├─────────────────────────────────────────┤
│  Accent (5%)  │ CTA buttons, highlights │
└─────────────────────────────────────────┘
```

⚠️ **Note**: Limit to 3~4 colors (too many colors looks cluttered)

### Color Application Example

```
Finance blog example:
- Main (70%): #1a365d (Navy) - Background, large areas
- Sub (25%): #d69e2e (Gold) - Headers, emphasis boxes
- Accent (5%): #38b2ac (Mint) - Buttons, links, number emphasis
```

### Recommended Colors by Topic

| Topic | Main Color | Accent Color | Mood |
|-------|------------|--------------|------|
| Finance/Investment | Navy, Gold | Mint, White | Trust, Expertise |
| Parenting/Baby | Pastel Pink, Sky Blue | Light Yellow, Mint | Warm, Soft |
| Health/Medical | Green, White | Blue, Mint | Clean, Safe |
| Real Estate/Policy | Blue, Gray | Orange, Green | Stable, Trustworthy |
| Lifestyle | Beige, Terracotta | Olive, Cream | Natural |

### Color English Expressions for Prompts

| Korean | English Prompt |
|--------|----------------|
| 파스텔 블루 | soft pastel blue, baby blue |
| 민트 그린 | mint green, seafoam |
| 따뜻한 노랑 | warm yellow, golden yellow |
| 네이비 | navy blue, deep blue |
| 골드 | gold, champagne gold |
| 코랄 핑크 | coral pink, soft coral |

---

## Recommended Image Count

| Article Length | Recommended Count | Layout |
|----------------|-------------------|--------|
| Under 1500 chars | 2~3 | Thumbnail + 1~2 body images |
| 1500~2000 chars | 4~5 | Thumbnail + 3~4 body images |
| Over 2000 chars | 5~7 | Thumbnail + 4~6 body images |

### Layout Principles
1. **Introduction**: Visualize topic with thumbnail
2. **Core sections**: Convey information with infographics/comparison tables
3. **Closing**: Leave impression with emotional image

---

## User Prompt Template

```
How many images should be included in the guide?

📷 Collected reference images: N
  - Directly usable: N (🖼️ Mode A)
  - Generation needed: N (🎨 Mode B)

Based on topic analysis, **N images** recommended:
- 1 thumbnail
- N body images
- N infographics

1️⃣ **As recommended** (N images)
2️⃣ **Minimum** (3 - thumbnail + 2 core)
3️⃣ **Rich** (N+2 - images for all sections)
```

---

## Prompt Consistency Checklist

When generating multiple images in same article:

- [ ] Unified color palette (main color + accent color)
- [ ] Unified style (flat/photography/illustration)
- [ ] Unified ratio (16:9 recommended)
- [ ] Unified font style mention
- [ ] Unified background style

---

## 🎨 2025-2026 Blog Design Trends

### 1. Bold Gradients

Eye-catching with dramatic color transitions. Use two contrasting colors for depth.

**Recommended Combinations**:
| Name | Color Code | Characteristics |
|------|------------|-----------------|
| Purple Gradient | #667eea → #764ba2 | Mysterious, Premium |
| Orange-Pink | #f093fb → #f5576c | Warm, Energetic |
| Blue-Mint | #4facfe → #00f2fe | Cool, Refreshing |
| Sunset | #fa709a → #fee140 | Emotional, Trendy |
| Deep Ocean | #667eea → #00d2ff | Deep, Trustworthy |

### 2. Glassmorphism

Sophisticated feel with semi-transparent glass effect. Background blur + border highlight combination.

**CSS Style**:
```css
background: rgba(255, 255, 255, 0.25);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.18);
border-radius: 16px;
box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
```

**Applied elements**: Info cards, price tables, comparison boxes

### 3. Layered Design

Express depth through overlapping elements. Effective with shadows.

**Implementation**:
- Multiple layers + slight rotation (2~5 degrees)
- Shadow: `box-shadow: 0 8px 32px rgba(0,0,0,0.1)`
- Element offset: 10~20px

**Applied elements**: Thumbnails, feature cards, galleries

### 4. Bold Typography

Impact with Extra Bold (800~900) titles.

**Recommended use**:
- Thumbnail main text: font-weight 800~900
- Number emphasis: font-weight 700~800, large size (48px+)
- Key keywords: Background color + Bold combination

### 5. Analog Aesthetics

Collage, handwritten fonts, texture effects. Add warmth to digital images.

**Application methods**:
- Handwritten style fonts
- Paper texture backgrounds
- Sticker/tape effects
- Irregular borders

**Recommended colors**: Warm tones (cream, beige, coral, terracotta)

### 6. Asymmetric Layout

Guide eyes with dynamic composition. Break away from static grids.

**Application examples**:
- Text left + Image right offset
- Diagonal dividers
- Mixed size elements
