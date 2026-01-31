# Image Guide Creation

Guide images for blog posts using one of **3 methods**.
The image guide is written in a separate **이미지가이드.md** file, not included in 본문.md.

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

### Recommended SVG Generation Sizes

| Purpose | Size | Description |
|---------|------|-------------|
| Thumbnail | 1300×885 | OG image standard |
| Content (basic) | 693×450 | Basic width fit |
| Content (extended) | 886×500 | Extended width fit |
| Infographic | 886×800 | Tall vertical format |
| Chart | 800×500 | Recommended for charts |

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

### SVG Text Guide

```
Main title: 32~48px, font-weight: 700~900
Subtitle: 18~24px, font-weight: 500~600
Body: 14~16px, font-weight: 400
Caption: 11~13px, font-weight: 300~400
```

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

1. **Provide one of 3 methods for every image position**
   - 🖼️ Mode A: Insert collected reference image directly
   - 🎨 Mode B: Provide AI generation prompt (Midjourney, DALL-E, etc.)
   - 🔷 Mode C: SVG image generation guide (using svg-canvas-mcp)

2. **Recommend SVG for infographics/charts**
   - Infographics, comparison tables, charts, diagrams → Mode C (SVG) recommended
   - Photographic, emotional images → Mode B (AI generation) recommended
   - When collected image is suitable → Mode A

3. **Style consistency**
   - Maintain unified color palette within same article
   - Specify color palette at top of 이미지가이드.md

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
> **Important (for auto-generation scripts)**: Use the heading-based format `## [Image N] ...` (see `templates/image-guide.md`).

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

### Mode B-2: Background Only + Text Overlay (Recommended for thumbnails)

> **New**: AI generates background only, then text is added locally (Pillow) for better Korean text quality.

#### 제목 단어화 규칙 (Thumbnail Text)

긴 제목을 **2~3개 핵심 단어로 압축**하여 가독성 높은 썸네일을 생성합니다:

| 원본 제목 | 압축된 텍스트 |
|----------|--------------|
| 2026년 0세 적금 금리 비교 완벽 가이드 | 0세 적금 필수! |
| 육아휴직 급여 신청 방법 총정리 | 육아휴직 급여 |
| 전세대출 금리 비교 및 조건 안내 | 전세대출 총정리 |

#### 썸네일 레이아웃 (1300×885 기준)

```
┌────────────────────────────────────────────┐
│                                            │
│         ┌──────────────────────┐           │
│         │   [main_text: 64px]  │           │  ← Y: 35% (310px)
│         │   Bold, 중앙 정렬     │           │
│         └──────────────────────┘           │
│                                            │
│         ┌──────────────────────┐           │
│         │   [sub_text: 32px]   │           │  ← Y: 50% (443px)
│         │   Regular, 중앙 정렬  │           │
│         └──────────────────────┘           │
│                                            │
│         ───@money-lab-brian───             │  ← Y: 하단에서 60px 위
└────────────────────────────────────────────┘
```

#### 텍스트 위치 상세

| 요소 | X 좌표 | Y 좌표 | 정렬 | 크기 | 비고 |
|------|--------|--------|------|------|------|
| main_text | 650 (중앙) | 35% (310px) | center | 64px Bold | 이미지 상단 1/3 |
| sub_text | 650 (중앙) | 50% (443px) | center | 32px Regular | main 아래 |
| watermark | 650 (중앙) | 하단-60px | center | 18px Light | 반투명 |

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {image role}

🎨 AI Generation (Background Only)

[Korean Description]
{배경 이미지 설명 - 텍스트 제외}

[AI Generation Prompt]
{배경 전용 프롬프트 - NO TEXT, NO TYPOGRAPHY 포함}

[Style Guide]
- Color: {color}
- Mood: {mood}
- Format: {format}
- Ratio: {ratio}

[Text Overlay Config]
# 메인 텍스트 (이미지 상단 1/3 중앙)
- main_text: "{핵심 키워드 2~3개}"
- main_text_y: "35%"
- font_size: 64
- font_weight: "bold"
- font_color: "#FFFFFF"
- shadow: true
- shadow_offset: 2
- shadow_color: "rgba(0,0,0,0.5)"

# 부제목 (메인 텍스트 아래, 중앙)
- sub_text: "{부제목}"
- sub_text_y: "50%"
- sub_font_size: 32
- sub_font_color: "rgba(255,255,255,0.9)"

# 배경 박스 (선택)
- background_box: true
- background_box_color: "rgba(0,0,0,0.3)"
- background_box_padding: 20

# 워터마크 (필수) - 하단 중앙에서 살짝 위로
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 60
- watermark_font_size: 18
- watermark_font_color: "rgba(255,255,255,0.6)"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 본문 이미지 텍스트 배치

| 이미지 타입 | 텍스트 위치 | 크기 | 특징 |
|------------|------------|------|------|
| 인포그래픽 | 상단 타이틀 (Y: 10%) | 32px | Bold, 중앙정렬 |
| 비교표 | 상단 헤더 (Y: 8%) | 28px | Bold, 좌측정렬 |
| 프로세스 | 각 단계 라벨 | 18px | Regular, 중앙정렬 |
| 무드 이미지 | 하단 캡션 (Y: 90%) | 16px | Light, 중앙정렬 |

**본문 이미지용 Text Overlay Config:**
```
[Text Overlay Config]
# 타이틀 (이미지 상단)
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
```

**Benefits of Mode B-2:**
1. Better Korean text rendering (AI struggles with Korean characters)
2. Easy text editing without regenerating images
3. Consistent font styling across all thumbnails
4. Professional typography control (shadows, positioning, etc.)
5. **Watermark support** for brand recognition

### Gemini API Usage

```python
from scripts.gemini_image import GeminiImageGenerator
from scripts.prompt_converter import generate_image_prompts_for_batch

# Extract prompts from image guide and auto-generate
prompts = generate_image_prompts_for_batch(image_guide_content)
generator = GeminiImageGenerator()
result = await generator.generate_batch(prompts, "./images/")
```

### API Limitations

| Item | Limit |
|------|-------|
| Requests per minute | 15 (auto delay applied) |
| Daily limit | 500 images (free tier) |
| Fallback | gemini-2.0-flash-exp → imagen-3.0 |

---

## Image Type Prompt Templates

### 1. Thumbnail Image

#### Option A: AI generates text (legacy)
```
[AI Generation Prompt]
Blog thumbnail image, {topic keywords} concept,
{core object} as main element,
bold "{thumbnail text}" text overlay,
{color} gradient background,
eye-catching modern design, 16:9 ratio

[Style Guide]
- Color: {main color} + {accent color} gradient
- Mood: Eye-catching and click-inducing
- Format: Modern thumbnail design
- Ratio: 16:9
```

#### Option B: Background + Text Overlay (Recommended)
```
[AI Generation Prompt]
Blog thumbnail background image, {topic keywords} concept,
{core object} as main element,
{color} gradient background,
NO TEXT, NO LETTERS, NO TYPOGRAPHY,
clean background suitable for text overlay,
eye-catching modern design, 16:9 ratio

[Style Guide]
- Color: {main color} + {accent color} gradient
- Mood: Eye-catching and click-inducing
- Format: Modern thumbnail background
- Ratio: 16:9

[Text Overlay Config]
- main_text: "{제목 텍스트}"
- sub_text: "{부제목}"
- position: "center"
- font_size: 48
- font_color: "#FFFFFF"
- shadow: true
```

**Example (Recommended - Background + Text Overlay):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Thumbnail] 0세 적금 고금리 안내

🎨 AI Generation (Background Only)

[Korean Description]
아기 손과 돼지저금통이 있는 따뜻한 배경 이미지 (텍스트 없음)

[AI Generation Prompt]
Blog thumbnail background image, baby savings account concept,
cute piggy bank and baby hands as main elements,
warm yellow to soft orange gradient background,
NO TEXT, NO LETTERS, NO TYPOGRAPHY, NO WORDS,
clean background suitable for text overlay,
eye-catching modern design, 16:9 ratio

[Style Guide]
- Color: Warm yellow + Soft orange gradient
- Mood: Warm, friendly, trustworthy
- Format: Modern thumbnail background
- Ratio: 16:9

[Text Overlay Config]
# 메인 텍스트 (상단 1/3, 중앙)
- main_text: "0세 적금 필수!"
- main_text_y: "35%"
- font_size: 64
- font_weight: "bold"
- font_color: "#FFFFFF"
- shadow: true
- shadow_offset: 2
- shadow_color: "rgba(0,0,0,0.5)"

# 부제목 (중앙)
- sub_text: "연 12% 고금리"
- sub_text_y: "50%"
- sub_font_size: 32
- sub_font_color: "rgba(255,255,255,0.9)"

# 배경 박스
- background_box: true
- background_box_color: "rgba(0,0,0,0.3)"
- background_box_padding: 20

# 워터마크 (하단 중앙)
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

**SVG Application**:
```
Use style_gradient tool:
- type: "linear"
- stops: [{offset: 0, color: "#667eea"}, {offset: 1, color: "#764ba2"}]
```

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

---

## 🔷 Mode C: SVG Image Generation Guide

Use svg-canvas-mcp tools to generate SVG images directly.

### Suitable Image Types

| Type | Suitability | Recommended Tools |
|------|-------------|-------------------|
| Infographic | ⭐⭐⭐ | chart_bar, chart_pie, draw_text |
| Comparison/Chart | ⭐⭐⭐ | chart_bar, chart_line |
| Process diagram | ⭐⭐⭐ | draw_rect, draw_text, draw_line |
| Checklist | ⭐⭐ | draw_rect, draw_text |
| Thumbnail | ⭐⭐ | draw_text, style_gradient |
| Photography style | ❌ | Use Mode B (AI generation) |

### SVG Guide Basic Template

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {image role description}

🔷 SVG Generation

[Image Description]
{Detailed description of image content}

[Canvas Settings]
- Size: {width}x{height}px
- Background: {hex color} or gradient

[Color Palette]
- Main: {hex} - {usage}
- Accent: {hex} - {usage}
- Text: {hex}
- Background: {hex}

[Layer Composition]
1. Background layer
2. Shape layer
3. Text layer

[Shape Elements]
1. {shape}: position({x},{y}), size({w}x{h}), color({hex})
2. {shape}: ...

[Text Elements]
1. "{text}": position({x},{y}), size({size}px), color({hex}), align({align})
2. "{text}": ...

[Save]
./images/{NN}_{description}.svg
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### SVG Type-Specific Templates

#### 1. Bar Chart

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {title} Bar Chart

🔷 SVG Generation

[Image Description]
{data description}

[Canvas Settings]
- Size: 800x500px
- Background: #FFFFFF

[Chart Data]
| Item | Value | Color |
|------|-------|-------|
| {item1} | {value1} | {hex1} |
| {item2} | {value2} | {hex2} |
| ... | ... | ... |

[Chart Style]
- Bar width: 80px
- Bar spacing: 40px
- Label position: Below bars
- Y-axis max: {max_value}

[Text]
- Title: "{title}" / 24px bold / top center
- X-axis labels: Below each bar / 14px
- Y-axis values: Above bars / 16px bold

[Save]
./images/{NN}_bar_chart.svg
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 2. Pie/Donut Chart

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {title} Pie Chart

🔷 SVG Generation

[Image Description]
{data description}

[Canvas Settings]
- Size: 600x600px
- Background: #FFFFFF

[Chart Data]
| Item | Percentage | Color |
|------|------------|-------|
| {item1} | {%1} | {hex1} |
| {item2} | {%2} | {hex2} |
| ... | ... | ... |

[Chart Style]
- Type: pie / donut
- Radius: 200px
- Donut thickness: 60px (if donut)
- Legend position: Right

[Text]
- Title: "{title}" / 24px bold / top
- Legend: Item name + percentage / 14px

[Save]
./images/{NN}_pie_chart.svg
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 3. Process Diagram (Flowchart)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {title} {N}-Step Process

🔷 SVG Generation

[Image Description]
{process description}

[Canvas Settings]
- Size: 900x300px
- Background: #FFFFFF or {hex}

[Step Data]
| Order | Title | Icon/Description |
|-------|-------|------------------|
| 1 | {title1} | {desc1} |
| 2 | {title2} | {desc2} |
| ... | ... | ... |

[Layout]
- Direction: Horizontal / Vertical
- Step spacing: 200px
- Arrow style: → or ▶

[Step Box Style]
- Shape: Rounded rectangle (radius: 10px)
- Size: 150x100px
- Background: {hex}
- Border: 2px {hex}

[Text]
- Step number: Circle badge / 20px bold / {hex}
- Step title: 14px bold / box center
- Description: 12px / box bottom

[Save]
./images/{NN}_process.svg
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 4. Comparison Table

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image N] {Item A} vs {Item B} Comparison

🔷 SVG Generation

[Image Description]
{comparison description}

[Canvas Settings]
- Size: 800x500px
- Background: #FFFFFF

[Comparison Data]
| Criteria | {Item A} | {Item B} |
|----------|----------|----------|
| {criteria1} | {valueA1} | {valueB1} |
| {criteria2} | {valueA2} | {valueB2} |
| ... | ... | ... |

[Table Style]
- Header background: {hex}
- Odd row background: #F8F8F8
- Even row background: #FFFFFF
- Border: 1px #E0E0E0
- Cell padding: 15px

[Emphasis Style]
- Superior item: {hex} background or bold
- Icons: ✓ / ✗ or ⭐

[Save]
./images/{NN}_comparison.svg
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 5. Thumbnail

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Image 1] Thumbnail - {topic}

🔷 SVG Generation

[Image Description]
{thumbnail concept description}

[Canvas Settings]
- Size: 1300x885px (Naver OG image standard)
- Background: Gradient {hex1} → {hex2}

[Layer Composition]
1. Background gradient
2. Decorative elements (shapes, patterns)
3. Icons/Illustrations
4. Main text
5. Sub text

[Text Elements]
- Main: "{key phrase}" / 48px bold / upper center / {hex}
- Sub: "{additional description}" / 24px / lower center / {hex}

[Decorative Elements]
- {shape1}: position, size, color, opacity
- {shape2}: ...

[Save]
./images/01_thumbnail.svg
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### SVG Generation Notes

1. **Korean fonts**: SVG Korean display depends on system fonts
2. **Complex graphics**: If too complex, recommend Mode B (AI generation)
3. **File size**: More elements = larger file size
4. **Browser compatibility**: Recommend using only basic SVG elements

### svg-canvas-mcp Key Tools

| Tool | Purpose |
|------|---------|
| `svg_create` | Create new canvas |
| `chart_bar` | Bar chart |
| `chart_pie` / `chart_donut` | Pie chart |
| `chart_line` | Line graph |
| `draw_rect` | Rectangle |
| `draw_circle` | Circle |
| `draw_text` | Text |
| `draw_line` | Line |
| `style_gradient` | Gradient |
| `style_fill` | Fill color |
| `export_svg` | Save SVG file |
