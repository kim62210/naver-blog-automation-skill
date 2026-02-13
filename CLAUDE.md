# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**search-blogging** is a Claude Code skill that automates the workflow from collecting trending economy topics on Naver Shortents to writing Korean blog posts (~1900 characters) with AI-generated images.

## Commands

### Environment Setup
```bash
# Auto setup: creates venv, installs packages, prompts for API key
python3 ~/.claude/skills/search-blogging/scripts/ensure_venv.py

# Reset API key
rm ~/.claude/skills/search-blogging/.env && python3 ~/.claude/skills/search-blogging/scripts/ensure_venv.py
```

### Running Python Scripts
```bash
# Always use venv Python
~/.claude/skills/search-blogging/.venv/bin/python -c "from scripts.config import load_config; print(load_config())"
```

### Validation
```python
from scripts.validator import validate_draft_char_count, validate_char_count

# Draft (원본.txt)
draft_result = validate_draft_char_count(draft_text)

# HTML (본문.html)
html_result = validate_char_count(html_content)
# Returns: ValidationResult(char_count, is_valid, message)
```

## Architecture

### 6-Step Modular Workflow
Each step is a separate markdown file in `skills/`:
1. **step1-topic-and-options** - Topic selection + tone/structure/image options (single AskUserQuestion)
2. **step2-research** - 3 parallel search agents, auto-sufficiency check
3. **step3-title-and-draft** - Title selection + draft writing (원본.txt) with style guide
4. **step4-refactor** - Writing refactoring (txt -> HTML/MD generation)
5. **step5-image** - Image generation (MANDATORY)
6. **step6-revise** - Revision loop

### Python Modules (`scripts/`)

**Core Infrastructure:**
- `shared_types.py` - Dataclasses: `ImageResult`, `ValidationResult`, `WatermarkConfig`, `PipelineConfig`, etc.
- `config.py` - YAML loader with env overrides and validation
- `validator.py` - Character count validation (draft + HTML, target: 1900 +-50)

**Image Generation Pipeline:**
- `image_pipeline.py` - Orchestrates generation, coordinates watermarking. Entry point: `ImagePipeline.process_image_guide()`
- `gemini_image.py` - Gemini API integration. Model: `gemini-3-pro-image-preview` (single model, no fallback)
- `image_guide_parser.py` - Parses `이미지 가이드.md` sections, extracts prompts via first fenced code block
- `prompt_converter.py` - Converts Korean -> English prompts, extracts `WatermarkConfig` from guide sections
- `text_overlay.py` - PIL-based watermark overlay (`@money-lab-brian`, bottom-center)
- `collector.py` - Downloads reference images (legacy)

**Content Generation:**
- `writer.py` - Generates 본문.html, 이미지 가이드.md, 참조.md using template system
- `setup.py` - Creates project directory structure

### Image Generation
- **Model**: `gemini-3-pro-image-preview` only
- **Size**: 1024x1024 (1:1)
- **Rate limit**: 10 req/min, 6s interval
- **Mode B-3**: AI renders text + PIL adds watermark (recommended)

## Key Patterns

### Character Count Validation
- Target: **1900 characters** (+-50 tolerance: 1850-1950)
- Counts pure text only (excludes HTML tags, `[이미지 N 삽입]` placeholders, CSS, hashtags)
- Configured in `config.yaml`: `writing.char_count`, `writing.char_tolerance`
- `validate_draft_char_count()` additionally strips `[[memo]]` blocks and render tags like `[중제목]`

### Output Structure
```
./경제 블로그/YYYY-MM-DD/{topic-slug}/
├── 원본.txt          # Plain text draft (STEP 3, immutable after STEP 4)
├── 본문.html          # Blog HTML (copy-paste to Naver Blog)
├── 이미지 가이드.md   # Image generation prompts (## [Image N] format)
├── 참조.md            # Source references (4-column tables)
└── images/            # Generated images ({NN}_{역할}.png, 20-char role truncation)
```

### Environment Variables
- `GOOGLE_API_KEY` or `GEMINI_API_KEY` - Required for Gemini image generation
- `BLOG_CHAR_COUNT` - Override target character count
- `BLOG_IMAGE_COUNT` - Override default image count
- `BLOG_OUTPUT_DIR` - Override output directory

### Watermark Configuration
- Text: `@money-lab-brian`
- Position: bottom-center, 60px margin, 18px font
- Applied via PIL (`text_overlay.add_watermark_to_image()`)
- Default values from `config.yaml` -> `watermark.*`, overridable per-image via `[Watermark Config]` in image guide

## Configuration

`config.yaml` contains all global settings:
- `writing.char_count/char_tolerance` - Character count validation
- `images.default_count` - Default image count per post (5), min 3, max 10
- `gemini.models.primary` - Gemini model (`gemini-3-pro-image-preview`)
- `gemini.default_size` - Image size (`1024x1024`)
- `watermark.*` - Watermark text, position, styling
- `output.base_dir` - Output directory path
- `tags.count/max_count` - Tag count (8 default, 10 max)
- `typography.blog_sizes.*` - Blog font sizes (h1:28, h2:24, h3:19, p:16, footnote:11)
