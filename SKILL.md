---
name: search-blogging
description: |
  A skill for collecting trending topics from Naver Economy Shortents and automating blog post writing.
  In step 1, collect today's top 10 economy news using Chrome DevTools for user selection.
  Then collect materials via parallel web search and write a blog post of around 1850 characters.

  When to use:
  (1) When blog post writing is needed
  (2) When writing about today's trending economy topics
  (3) When /search-blogging command is entered

  Trigger keywords: blog post writing, write a blog post, research and write, economy blog
---

# search-blogging Skill v2.1

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
| 이미지 가이드.md | AI prompts | Image generation reference |
| 참조.md | Source list | Reference verification |
| images/ | Generated images | Blog image insertion |

### Save Path

```
./경제 블로그/YYYY-MM-DD/topic-name/
├── 본문.html
├── 이미지 가이드.md
├── 참조.md
└── images/
```

---

## Workflow (9 Steps)

| Step | Description | Detailed Guide |
|------|-------------|----------------|
| **STEP 1** | Trending topic collection and selection | [skills/step1-collect.md](skills/step1-collect.md) |
| **STEP 2** | Topic confirmation and keyword expansion | [skills/step2-confirm.md](skills/step2-confirm.md) |
| **STEP 3** | Parallel research (6 agents) | [skills/step3-research.md](skills/step3-research.md) |
| **STEP 4** | Research summary and review | [skills/step4-review.md](skills/step4-review.md) |
| **STEP 5** | Writing options selection | [skills/step5-options.md](skills/step5-options.md) |
| **STEP 6** | Title selection | [skills/step6-title.md](skills/step6-title.md) |
| **STEP 7** | Content writing and saving | [skills/step7-write.md](skills/step7-write.md) |
| **STEP 8** | 🖼️ **Image generation (MANDATORY)** | [skills/step8-image.md](skills/step8-image.md) |
| **STEP 9** | Revision loop | [skills/step9-revise.md](skills/step9-revise.md) |

### Progress Display

```
[STEP 1/9] Topic collection ███░░░░░░░░░░░░░░░░░░░░░░░░░ 11%
[STEP 2/9] Topic confirmation ██████░░░░░░░░░░░░░░░░░░░░░░ 22%
[STEP 3/9] Research █████████░░░░░░░░░░░░░░░░░░░ 33%
[STEP 4/9] Review ████████████░░░░░░░░░░░░░░░░ 44%
[STEP 5/9] Options ███████████████░░░░░░░░░░░░░ 55%
[STEP 6/9] Title ██████████████████░░░░░░░░░░ 66%
[STEP 7/9] Writing █████████████████████░░░░░░░ 77%
[STEP 8/9] 🖼️ Image ████████████████████████░░░░ 88%
[STEP 9/9] Review/Edit ████████████████████████████ 100%
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
  char_count: 1850
  char_tolerance: 50

images:
  default_count: 5

tags:
  count: 8

output:
  base_dir: "./경제 블로그"

# Gemini API 3-tier fallback models
gemini:
  models:
    primary: "gemini-2.0-flash-exp-image-generation"
    fallback: "gemini-2.5-flash-image"
    fallback_2: "gemini-3-pro-image-preview"
```

---

## Python Scripts

| Script | Function |
|--------|----------|
| `scripts/config.py` | Configuration file loader (YAML parsing) |
| `scripts/utils.py` | Common utilities (date formatting, text cleaning) |
| `scripts/shared_types.py` | Shared type definitions (dataclasses) |
| `scripts/validator.py` | Character count validation (1850±50 chars) |
| `scripts/setup.py` | Project directory initialization |
| `scripts/collector.py` | Reference image collection/download |
| `scripts/writer.py` | HTML/MD generation (본문.html, 참조.md) |
| `scripts/prompt_converter.py` | AI prompt conversion and text overlay config |
| `scripts/gemini_image.py` | Gemini API integration (3-tier fallback) |
| `scripts/text_overlay.py` | PIL-based watermark and text overlay |
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
| `references/image-guide.md` | Image guide creation | STEP 5-3, STEP 7 |
| `references/thumbnail-templates.md` | 10가지 썸네일 템플릿 (색상팔레트, AI프롬프트, 텍스트오버레이) | STEP 5-3, STEP 7 (썸네일 생성시) |

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
├── requirements.txt            # Python dependencies
├── skills/                     # Modularized skills (9 files)
│   ├── step1-collect.md       # Trending topic collection
│   ├── step2-confirm.md       # Topic confirmation
│   ├── step3-research.md      # Research (parallel)
│   ├── step4-review.md        # Review
│   ├── step5-options.md       # Options selection
│   ├── step6-title.md         # Title selection
│   ├── step7-write.md         # Content writing
│   ├── step8-image.md         # 🖼️ Image generation (MANDATORY)
│   └── step9-revise.md        # Revision loop
├── references/                 # Reference materials
│   ├── tone-guide.md
│   ├── structure-templates.md
│   └── image-guide.md
├── templates/                  # Output templates
│   ├── blog-post.html
│   ├── image-guide.md
│   └── references.md
└── scripts/                    # Python automation (11 modules)
    ├── __init__.py             # Package init (v2.2.0)
    ├── config.py               # YAML config loader
    ├── shared_types.py         # Shared dataclasses
    ├── utils.py                # Common utilities
    ├── validator.py            # Character count validation
    ├── setup.py                # Project structure setup
    ├── collector.py            # Reference image download
    ├── writer.py               # HTML/MD file generation
    ├── prompt_converter.py     # AI prompt processing
    ├── gemini_image.py         # Gemini API integration
    ├── text_overlay.py         # PIL watermark/text overlay
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

- **v2.1.0** (2026-02-01)
  - 9-step workflow: Image generation separated as STEP 8
  - step8-image.md (MANDATORY) + step9-revise.md structure
  - Documentation sync (CLAUDE.md, PIPELINE-ANALYSIS.md)

- **v2.0.0** (2026-01-27)
  - Skill modularization (separated into 8 step files)
  - Python automation scripts added
  - YAML configuration file introduced
  - Template system implemented
