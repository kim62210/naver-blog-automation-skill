---
name: search-blogging
description: |
  A skill for collecting trending topics from Naver Shortents (multi-category) and automating blog post writing.
  Supports 27 categories: Economy, Entertainment, Sports, Travel/Food, Fashion/Beauty, Lifestyle.
  In step 1, select category and collect today's top 10 trending topics for user selection.
  Then collect materials via parallel web search and write a blog post of around 1850 characters.

  When to use:
  (1) When blog post writing is needed
  (2) When writing about trending topics (any category)
  (3) When /search-blogging command is entered

  Trigger keywords: blog post writing, write a blog post, research and write, trending blog
---

# search-blogging Skill v2.1

Automates the entire workflow from trending topic collection on Naver Shortents to blog post writing.
**Now supports 27 categories** across Economy, Entertainment, Sports, Travel/Food, Fashion/Beauty, and Lifestyle.

## Quick Start

```bash
# Select from trending topics
/search-blogging

# Specify topic directly
/search-blogging 육아휴직 급여
```

---

## Output Files

| File | Description | Purpose |
|------|-------------|---------|
| 본문.html | HTML for Naver Blog | Open in browser, copy → paste to blog |
| 이미지 가이드.md | AI prompts + SVG guide | Image generation reference |
| 참조.md | Source list | Reference verification |
| images/ | Reference images + Generated SVGs | Blog image insertion |

### Save Path

```
./{카테고리별 폴더}/YYYY-MM-DD/topic-name/
├── 본문.html
├── 이미지 가이드.md
├── 참조.md
└── images/
```

**Category folder examples:**
- 경제 종합 → `./경제 블로그/`
- 증권 → `./증권 블로그/`
- 야구 → `./야구 블로그/`
- 맛집/카페 → `./맛집카페 블로그/`

---

## Workflow (8 Steps)

| Step | Description | Detailed Guide |
|------|-------------|----------------|
| **STEP 1** | Trending topic collection and selection | [skills/step1-collect.md](skills/step1-collect.md) |
| **STEP 2** | Topic confirmation and keyword expansion | [skills/step2-confirm.md](skills/step2-confirm.md) |
| **STEP 3** | Parallel research (3 agents) | [skills/step3-research.md](skills/step3-research.md) |
| **STEP 4** | Research summary and review | [skills/step4-review.md](skills/step4-review.md) |
| **STEP 5** | Writing options selection | [skills/step5-options.md](skills/step5-options.md) |
| **STEP 6** | Title selection | [skills/step6-title.md](skills/step6-title.md) |
| **STEP 7** | Content writing and saving | [skills/step7-write.md](skills/step7-write.md) |
| **STEP 8** | Revision loop | [skills/step8-revise.md](skills/step8-revise.md) |

### Progress Display

```
[STEP 1/8] Topic collection ████░░░░░░░░░░░░░░░░░░░░░░░░ 12%
[STEP 2/8] Topic confirmation ████████░░░░░░░░░░░░░░░░░░░░ 25%
[STEP 3/8] Research ████████████░░░░░░░░░░░░░░░░ 37%
[STEP 4/8] Review ████████████████░░░░░░░░░░░░ 50%
[STEP 5/8] Options ████████████████████░░░░░░░░ 62%
[STEP 6/8] Title ████████████████████████░░░░ 75%
[STEP 7/8] Writing ████████████████████████████░ 87%
[STEP 8/8] Review/Edit ████████████████████████████ 100%
```

---

## Writing Rules

### Character Count (Important!)
- **Target: Around 1850 characters**
- **Allowed range: 1800~1900 characters (±50)**
- Count pure body text only (excluding HTML tags, image placeholders)

### Character Count Validation (Python)

```python
from scripts.validator import validate_char_count

result = validate_char_count(html_content)
print(f"Character count: {result.char_count}")
print(result.message)  # ✅ Valid / ⚠️ Over / ⚠️ Under
```

---

## Options

### Tone & Manner

| Option | Description | Suitable Topics |
|--------|-------------|-----------------|
| Professional | Objective and trustworthy tone | Finance, Health, Legal |
| Friendly | Casual conversational tone | Parenting, Reviews, Daily life |
| Neutral | Balanced information-focused tone | Comparisons, Guides, News |

### Article Structure

| Option | Structure | Use Case |
|--------|-----------|----------|
| 7-step | Intro→Problem→Core1,2,3→Tips→Closing | Informational content |
| 5-step | Intro→Core→Details→Tips→Closing | Concise delivery |
| Flexible | AI adapts to topic | Storytelling, Q&A |

### Images

| Option | Count | Composition |
|--------|-------|-------------|
| Minimum | 3 | Thumbnail + 2 core images |
| Recommended | 4 | Thumbnail + 2 core images + 1 infographic |
| Rich | 7+ | Images for all sections |

---

## Supported Categories

| Group | Categories |
|-------|------------|
| **경제/금융** | 경제 종합, 생활경제, 증권, 부동산 |
| **엔터테인먼트** | 엔터 종합, 영화, 드라마, 뮤직 |
| **스포츠** | 스포츠 종합, 야구, 해외야구, 축구, 해외축구, 농구, 배구, 동계올림픽 |
| **여행/맛집** | 여행맛집 종합, 국내여행, 세계여행, 맛집/카페, 푸드 |
| **패션/뷰티** | 패션뷰티 종합, 패션트렌드, 뷰티 |
| **라이프스타일** | 리빙푸드 종합, 카테크 종합, 자동차, 지식 종합 |

---

## Configuration File

Global settings are managed in `config.yaml`:

```yaml
# config.yaml
writing:
  char_count: 1850
  char_tolerance: 50

images:
  default_count: 4

tags:
  count: 8

# Category-specific output directories
categories:
  economy:
    - id: "economy_general"
      name: "경제 종합"
      output_dir: "경제 블로그"
  # ... (27 categories total)
```

---

## Python Scripts

| Script | Function |
|--------|----------|
| `scripts/config.py` | Configuration file loader |
| `scripts/utils.py` | Common utilities |
| `scripts/validator.py` | Character count validation |
| `scripts/setup.py` | Project directory initialization |
| `scripts/collector.py` | Image collection |
| `scripts/writer.py` | HTML/MD generation |

### Usage Examples

```python
# Project initialization
from scripts.setup import create_project_structure
project_path = create_project_structure("육아휴직 가이드")

# Image collection
from scripts.collector import collect_images
result = collect_images(images, project_path)

# File saving
from scripts.writer import save_blog_files
files = save_blog_files(project_path, html, image_guide, references)
```

---

## Reference Files

Reference these files as needed during skill execution:

| File | Purpose | When to Reference |
|------|---------|-------------------|
| `references/tone-guide.md` | Detailed tone & manner guide | STEP 5-1 |
| `references/structure-templates.md` | Article structure templates | STEP 5-2 |
| `references/image-guide.md` | Image guide creation | STEP 5-3, STEP 7 |

---

## Template Files

| File | Purpose |
|------|---------|
| `templates/blog-post.html` | HTML content template |
| `templates/image-guide.md` | Image guide template |
| `templates/references.md` | References document template |

---

## Directory Structure

```
naver-blog-automation/
├── SKILL.md                    # This file (entry point)
├── config.yaml                 # Global configuration
├── skills/                     # Modularized skills (8 files)
│   ├── step1-collect.md       # Trending topic collection
│   ├── step2-confirm.md       # Topic confirmation
│   ├── step3-research.md      # Research (parallel)
│   ├── step4-review.md        # Review
│   ├── step5-options.md       # Options selection
│   ├── step6-title.md         # Title selection
│   ├── step7-write.md         # Content writing
│   └── step8-revise.md        # Revision loop
├── references/                 # Reference materials
│   ├── tone-guide.md
│   ├── structure-templates.md
│   └── image-guide.md
├── templates/                  # Output templates
│   ├── blog-post.html
│   ├── image-guide.md
│   └── references.md
└── scripts/                    # Python automation
    ├── __init__.py
    ├── config.py
    ├── utils.py
    ├── validator.py
    ├── setup.py
    ├── collector.py
    └── writer.py
```

---

## How to Use 본문.html

1. **Open 본문.html file in browser** (double-click)
2. **Cmd+A** (select all)
3. **Cmd+C** (copy)
4. **Cmd+V in Naver Blog editor** (paste)
5. Insert actual images at image placeholder positions

> Tables, font sizes, bold, blockquotes and all formatting will be preserved.

---

## Version Information

- **v2.1.0** (2026-01-31)
  - **Multi-category support**: 27 categories across 6 groups
  - Category selection step added (STEP 1-0)
  - Dynamic output directory based on selected category
  - Updated URL construction for category-specific trending pages

- **v2.0.0** (2026-01-27)
  - Skill modularization (separated into 8 step files)
  - Python automation scripts added
  - YAML configuration file introduced
  - Template system implemented
