---
name: search-blogging
description: |
  A skill for collecting trending topics from Naver Economy Shortents and automating blog post writing.
  In step 1, collect today's top 10 economy news using Chrome DevTools for user selection.
  Then collect materials via parallel web search and write a blog post of around 1900 characters (configurable).

  When to use:
  (1) When blog post writing is needed
  (2) When writing about today's trending economy topics
  (3) When /search-blogging command is entered

  Trigger keywords: blog post writing, write a blog post, research and write, economy blog
---

# search-blogging Skill v2.3

Automates the entire workflow from trending topic collection on Naver Economy Shortents to blog post writing.

## Environment Setup

### First Run (Auto Setup)
```bash
python3 ~/.claude/skills/search-blogging/scripts/ensure_venv.py
```

This will:
1. Create `.venv` virtual environment
2. Install required packages (PyYAML, google-genai, pillow)
3. Prompt for GOOGLE_API_KEY and save to `.env`

### Running Python Scripts
```bash
~/.claude/skills/search-blogging/.venv/bin/python -c "..."
```

### Reset API Key
```bash
rm ~/.claude/skills/search-blogging/.env
python3 ~/.claude/skills/search-blogging/scripts/ensure_venv.py
```

---

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
| 원본.txt | Plain text draft | Source of truth for writing/refactoring |
| 이미지 가이드.md | AI prompts | Image generation reference |
| 참조.md | Source list | Reference verification |
| images/ | Generated images | Blog image insertion |

### Save Path

```
./경제 블로그/YYYY-MM-DD/{topic-slug}/
├── 원본.txt          # Plain text draft (STEP 7, immutable after STEP 8)
├── 본문.html          # Blog HTML (copy-paste to Naver Blog)
├── 이미지 가이드.md   # Image generation prompts (## [Image N] format)
├── 참조.md            # Source references (4-column tables)
└── images/            # Generated images ({NN}_{역할}.png)
```

---

## Workflow (10 Steps)

| Step | Description | Detailed Guide |
|------|-------------|----------------|
| **STEP 1** | Trending topic collection and selection | [skills/step1-collect.md](skills/step1-collect.md) |
| **STEP 2** | Topic confirmation and keyword expansion | [skills/step2-confirm.md](skills/step2-confirm.md) |
| **STEP 3** | Parallel research (6 agents) | [skills/step3-research.md](skills/step3-research.md) |
| **STEP 4** | Research summary and review | [skills/step4-review.md](skills/step4-review.md) |
| **STEP 5** | Writing options selection | [skills/step5-options.md](skills/step5-options.md) |
| **STEP 6** | Title selection | [skills/step6-title.md](skills/step6-title.md) |
| **STEP 7** | Draft writing & validation (`원본.txt`) + 문체 가이드 적용 | [skills/step7-write.md](skills/step7-write.md) |
| **STEP 8** | Writing refactoring (txt → HTML/MD) | [skills/step8-refactor.md](skills/step8-refactor.md) |
| **STEP 9** | **Image generation (MANDATORY)** | [skills/step9-image.md](skills/step9-image.md) |
| **STEP 10** | Revision loop | [skills/step10-revise.md](skills/step10-revise.md) |

### Progress Display

```
[STEP 1/10] Topic collection ██░░░░░░░░░░░░░░░░░░░░░░░░░ 10%
[STEP 2/10] Topic confirmation █████░░░░░░░░░░░░░░░░░░░░░░ 20%
[STEP 3/10] Research ████████░░░░░░░░░░░░░░░░░░░ 30%
[STEP 4/10] Review ██████████░░░░░░░░░░░░░░░░ 40%
[STEP 5/10] Options ████████████░░░░░░░░░░░░░░ 50%
[STEP 6/10] Title ███████████████░░░░░░░░░░░░ 60%
[STEP 7/10] Draft ████████████████████░░░░░░░░ 70%
[STEP 8/10] Refactor ███████████████████████░░░░ 80%
[STEP 9/10] Image ██████████████████████████░░ 90%
[STEP 10/10] Review/Edit ████████████████████████████ 100%
```

---

## Writing Rules

### Character Count (Important!)
- **Target: Around 1900 characters**
- **Allowed range: 1850~1950 characters (±50)**
- Count pure body text only (excluding HTML tags, image placeholders)

### Character Count Validation (Python)

```python
from pathlib import Path
from scripts.validator import validate_draft_char_count
from scripts.validator import validate_char_count

# Draft (원본.txt)
draft_text = Path(project_path / "원본.txt").read_text(encoding="utf-8")
draft_result = validate_draft_char_count(draft_text)
print(draft_result.message)

# HTML (본문.html)
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
| Recommended | 5 | Thumbnail + 1 per section |
| Rich | 7+ | Images for all sections |

---

## Environment Variables

Required environment variables for AI image generation:

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes* | Google API key for Gemini image generation |
| `GEMINI_API_KEY` | Yes* | Alternative name for Google API key |

*Either `GOOGLE_API_KEY` or `GEMINI_API_KEY` must be set for image generation.

### Setup

```bash
# Option 1: Export in terminal
export GOOGLE_API_KEY="your-api-key-here"

# Option 2: Add to shell profile (~/.zshrc or ~/.bashrc)
echo 'export GOOGLE_API_KEY="your-api-key-here"' >> ~/.zshrc

# Option 3: Create .env file (not committed to git)
echo 'GOOGLE_API_KEY=your-api-key-here' > .env
```

### Get API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key
3. Enable Gemini API access

---

## Configuration File

Global settings are managed in `config.yaml`:

```yaml
# config.yaml
writing:
  char_count: 1900
  char_tolerance: 50
  min_chars: 1850
  max_chars: 1950

images:
  default_count: 5

tags:
  count: 8

output:
  base_dir: "./경제 블로그"

# Gemini API settings - FORCE gemini-3-pro-image-preview
gemini:
  force_primary_only: true  # When true, disables fallback (ALWAYS use primary)
  models:
    primary: "gemini-3-pro-image-preview"   # ALWAYS USE THIS MODEL
    fallback: "gemini-3-pro-image-preview"  # Same as primary (fallback disabled)
    fallback_2: "gemini-3-pro-image-preview" # Same as primary (fallback disabled)
```

---

## Python Scripts

| Script | Function |
|--------|----------|
| `scripts/config.py` | Configuration file loader (YAML parsing) |
| `scripts/utils.py` | Common utilities (date formatting, text cleaning) |
| `scripts/shared_types.py` | Shared type definitions (dataclasses) |
| `scripts/validator.py` | Character count validation (1900±50 chars) |
| `scripts/setup.py` | Project directory initialization |
| `scripts/collector.py` | Reference image collection/download |
| `scripts/writer.py` | Draft + HTML/MD generation (원본.txt, 본문.html, 이미지 가이드.md, 참조.md) |
| `scripts/prompt_converter.py` | AI prompt conversion and text overlay config |
| `scripts/gemini_image.py` | Gemini API integration (single model, force_primary_only) |
| `scripts/image_guide_parser.py` | Image guide parsing and prompt extraction |
| `scripts/text_overlay.py` | PIL-based watermark overlay (@money-lab-brian) |
| `scripts/image_pipeline.py` | Integrated image generation pipeline |

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

# AI image generation with watermark
from scripts.image_pipeline import ImagePipeline
pipeline = ImagePipeline()
result = await pipeline.generate_with_watermark(
    prompt="Blog thumbnail, finance concept...",
    output_path="./images/01_thumbnail.png"
)
```

---

## Reference Files

Reference these files as needed during skill execution:

| File | Purpose | When to Reference |
|------|---------|-------------------|
| `references/tone-guide.md` | Detailed tone & manner guide | STEP 5-1 |
| `references/structure-templates.md` | Article structure templates | STEP 5-2 |
| `references/image-guide.md` | Image guide creation | STEP 5-3, STEP 8 |
| `references/thumbnail-templates.md` | 10가지 썸네일 템플릿 (색상팔레트, AI프롬프트, 텍스트오버레이) | STEP 5-3, STEP 8 (썸네일 생성시) |
| `네이버_블로그_문체_가이드.md` | 네이버 인기 경제 블로그 문체 분석 (톤, 문장 구조, 도입/마무리 패턴) | STEP 7 (필수), STEP 8 (확인) |

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
search-blogging/
├── SKILL.md                    # This file (entry point)
├── config.yaml                 # Global configuration
├── requirements.txt            # Python dependencies
├── skills/                     # Modularized skills (10 files)
│   ├── step1-collect.md       # Trending topic collection
│   ├── step2-confirm.md       # Topic confirmation
│   ├── step3-research.md      # Research (parallel)
│   ├── step4-review.md        # Review
│   ├── step5-options.md       # Options selection
│   ├── step6-title.md         # Title selection
│   ├── step7-write.md         # Draft writing (원본.txt)
│   ├── step8-refactor.md      # Writing refactoring (txt → HTML/MD)
│   ├── step9-image.md         # Image generation (MANDATORY)
│   └── step10-revise.md       # Revision loop
├── references/                 # Reference materials
│   ├── tone-guide.md
│   ├── structure-templates.md
│   └── image-guide.md
├── templates/                  # Output templates
│   ├── blog-post.html
│   ├── image-guide.md
│   └── references.md
└── scripts/                    # Python automation (11 modules)
    ├── __init__.py             # Package init
    ├── config.py               # YAML config loader
    ├── shared_types.py         # Shared dataclasses
    ├── utils.py                # Common utilities
    ├── validator.py            # Character count validation
    ├── setup.py                # Project structure setup
    ├── collector.py            # Reference image download
    ├── writer.py               # HTML/MD file generation
    ├── prompt_converter.py     # AI prompt processing
    ├── gemini_image.py         # Gemini API (gemini-3-pro-image-preview only)
    ├── image_guide_parser.py   # Image guide parsing
    ├── text_overlay.py         # PIL watermark overlay
    └── image_pipeline.py       # Integrated generation pipeline
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

- **v2.3.0** (2026-02-03)
  - Gemini API 단일 모델 강제 (force_primary_only, 3-tier fallback 폐기)
  - STEP 8 문서 명세 강화 (HTML 구조/CSS/태그변환/글자수검증 상세화)
  - STEP 9 문서 명세 강화 (이미지 유형별 가이드, 모드 자동 판별, 파일명 규칙)
  - image_guide_parser.py 모듈 문서화 반영

- **v2.2.0** (2026-02-01)
  - Inserted STEP 8: Writing refactoring (원본.txt → HTML/MD)
  - STEP 7 now saves `원본.txt` and validates draft character count
  - Image generation moved to STEP 9, revision loop moved to STEP 10

- **v2.1.0** (2026-02-01)
  - 9-step workflow
  - Image generation separated as STEP 8
  - Documentation sync (CLAUDE.md, PIPELINE-ANALYSIS.md)

- **v2.0.0** (2026-01-27)
  - Skill modularization (separated into 8 step files)
  - Python automation scripts added
  - YAML configuration file introduced
  - Template system implemented
