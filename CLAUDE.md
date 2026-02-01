# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**search-blogging** is a Claude Code skill that automates the workflow from collecting trending economy topics on Naver Shortents to writing Korean blog posts (~1850 characters) with AI-generated images.

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
from scripts.validator import validate_char_count
result = validate_char_count(html_content)
# Returns: ValidationResult(char_count, is_valid, message)
```

## Architecture

### 9-Step Modular Workflow
Each step is a separate markdown file in `skills/`:
1. **step1-collect** - Crawl Naver Economy Shortents via Chrome DevTools MCP
2. **step2-confirm** - User confirms topic, expand keywords
3. **step3-research** - 6 parallel WebSearch agents
4. **step4-review** - Consolidate research into outline
5. **step5-options** - Select tone, structure, image count
6. **step6-title** - Generate and select title
7. **step7-write** - Write HTML + image guide + references
8. **step8-image** - 🖼️ Image generation (MANDATORY)
9. **step9-revise** - Revision loop

### Python Modules (`scripts/`)

**Core Infrastructure:**
- `shared_types.py` - Dataclasses: `ImageResult`, `ValidationResult`, `WatermarkConfig`, `PipelineConfig`, etc.
- `config.py` - YAML loader with env overrides and validation
- `validator.py` - Character count validation (target: 1850 ±50)

**Image Generation Pipeline:**
- `gemini_image.py` - Gemini API with 3-tier model fallback (rate limit: 10 req/min)
- `image_pipeline.py` - Orchestrates generation, coordinates watermarking
- `text_overlay.py` - PIL-based watermark overlay
- `prompt_converter.py` - Parses image guide, converts Korean → English prompts
- `collector.py` - Downloads reference images

**Content Generation:**
- `writer.py` - Generates 본문.html, 이미지 가이드.md, 참조.md
- `setup.py` - Creates project directory structure

### Image Generation Modes
- **Mode A**: Download reference images from web
- **Mode B**: AI generation via Gemini API
- **Mode B-3**: AI generation + watermark overlay (PIL)

### 3-Tier Gemini API Fallback
Triggers on 429/QUOTA_EXCEEDED/SAFETY errors:
1. `gemini-2.0-flash-exp-image-generation` (primary)
2. `gemini-2.5-flash-image` (fallback)
3. `gemini-3-pro-image-preview` (fallback 2)

## Key Patterns

### Character Count Validation
- Target: **1850 characters** (±50 tolerance: 1800-1900)
- Counts pure text only (excludes HTML tags, `[이미지 N 삽입]` placeholders, CSS)
- Configured in `config.yaml`: `writing.char_count`, `writing.char_tolerance`

### Output Structure
```
./경제 블로그/YYYY-MM-DD/topic-name/
├── 본문.html          # Blog HTML (copy-paste to Naver Blog)
├── 이미지 가이드.md   # Image generation prompts
├── 참조.md            # Source references
└── images/            # Generated images
```

### Environment Variables
- `GOOGLE_API_KEY` or `GEMINI_API_KEY` - Required for Gemini image generation
- `BLOG_CHAR_COUNT` - Override target character count
- `BLOG_IMAGE_COUNT` - Override default image count
- `BLOG_OUTPUT_DIR` - Override output directory

### Watermark Configuration
- Text: "@money-lab-brian"
- Position: bottom-center
- Applied via PIL (`text_overlay.py`)

## Configuration

`config.yaml` contains all global settings:
- `writing.char_count/char_tolerance` - Character count validation
- `images.default_count` - Default image count per post
- `gemini.models` - 3-tier fallback model configuration
- `watermark.*` - Watermark text, position, styling
- `output.base_dir` - Output directory path
