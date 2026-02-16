---
name: search-blogging
description: |
  A skill for collecting trending topics from Naver Economy Shortents and automating blog post writing.
  In step 1, collect today's top 10 economy news using web-first tools in this priority: Playwriter, Playwright, Google Chrome DevTools, then web search fallback.
  Then collect materials via parallel web search and write a blog post of around 1900 characters (configurable).

  When to use:
  (1) When blog post writing is needed
  (2) When writing about today's trending economy topics
  (3) When /search-blogging command is entered

  Trigger keywords: blog post writing, write a blog post, research and write, economy blog
---

# search-blogging Skill v3.0

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
| 본문.html | HTML for Naver Blog | Open in browser, copy -> paste to blog |
| 원본.txt | Plain text draft | Source of truth for writing/refactoring |
| 이미지 가이드.md | AI prompts | Image generation reference |
| 참조.md | Source list | Reference verification |
| images/ | Generated images | Blog image insertion |

### Save Path

```
~/workspace/경제 블로그/YYYY-MM-DD/{topic-slug}/
├── 원본.txt          # Plain text draft (STEP 3, immutable after STEP 4)
├── 본문.html          # Blog HTML (copy-paste to Naver Blog)
├── 이미지 가이드.md   # Image generation prompts (## [Image N] format)
├── 참조.md            # Source references (4-column tables)
└── images/            # Generated images ({NN}_{역할}.png)
```

---

## Workflow (6 Steps)

| Step | Description | User Interaction | Detailed Guide |
|------|-------------|------------------|----------------|
| **STEP 1** | Topic selection + tone/structure/image options | 1 AskUserQuestion (4 questions) | [step1-topic-and-options.md](skills/step1-topic-and-options.md) |
| **STEP 2** | Parallel research (3 agents) | Auto (ask only if < 10 sources) | [step2-research.md](skills/step2-research.md) |
| **STEP 3** | Title selection + draft writing (원본.txt) | 1 AskUserQuestion (title) | [step3-title-and-draft.md](skills/step3-title-and-draft.md) |
| **STEP 4** | Writing refactoring (txt -> HTML/MD) | Auto | [step4-refactor.md](skills/step4-refactor.md) |
| **STEP 5** | **Image generation (MANDATORY)** | Auto (API-driven) | [step5-image.md](skills/step5-image.md) |
| **STEP 6** | Revision loop | User-driven | [step6-revise.md](skills/step6-revise.md) |

### Progress Display

```
[STEP 1/6] Topic + Options   ████░░░░░░░░░░░░░░░░░░░░░░░ 15%
[STEP 2/6] Research           ████████░░░░░░░░░░░░░░░░░░░ 30%
[STEP 3/6] Title + Draft      ████████████████░░░░░░░░░░░ 55%
[STEP 4/6] Refactoring        ████████████████████░░░░░░░ 70%
[STEP 5/6] Image generation   ██████████████████████████░░ 90%
[STEP 6/6] Revision loop      ████████████████████████████ 100%
```

---

## Writing Rules

### Character Count (Important!)
- **Target: Around 1900 characters**
- **Allowed range: 1850~1950 characters (+-50)**
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
print(result.message)
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
| 7-step | Intro > Problem > Core1,2,3 > Tips > Closing | Informational content |
| 5-step | Intro > Core > Details > Tips > Closing | Concise delivery |
| Flexible | AI adapts to topic | Storytelling, Q&A |

### Images

| Option | Count | Composition |
|--------|-------|-------------|
| Minimum | 3 | Thumbnail + 2 core images |
| Recommended | 5 | Thumbnail + 1 per section |
| Rich | 7+ | Images for all sections |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes* | Google API key for Gemini image generation |
| `GEMINI_API_KEY` | Yes* | Alternative name for Google API key |

*Either `GOOGLE_API_KEY` or `GEMINI_API_KEY` must be set for image generation.

---

## Configuration File

Global settings in `config.yaml`:

```yaml
writing:
  char_count: 1900
  char_tolerance: 50

images:
  default_count: 5

tags:
  count: 8

output:
  base_dir: "~/workspace/경제 블로그"

gemini:
  models:
    primary: "gemini-3-pro-image-preview"
```

---

## Python Scripts

| Script | Function |
|--------|----------|
| `scripts/config.py` | Configuration file loader (YAML parsing) |
| `scripts/utils.py` | Common utilities (date formatting, text cleaning) |
| `scripts/shared_types.py` | Shared type definitions (dataclasses) |
| `scripts/validator.py` | Character count validation (1900+-50 chars) |
| `scripts/setup.py` | Project directory initialization |
| `scripts/collector.py` | Reference image collection/download |
| `scripts/writer.py` | Draft + HTML/MD generation |
| `scripts/prompt_converter.py` | AI prompt conversion and watermark config |
| `scripts/gemini_image.py` | Gemini API integration (single model) |
| `scripts/image_guide_parser.py` | Image guide parsing and prompt extraction |
| `scripts/text_overlay.py` | PIL-based watermark overlay (@money-lab-brian) |
| `scripts/image_pipeline.py` | Integrated image generation pipeline |

---

## Reference Files

| File | Purpose | When to Reference |
|------|---------|-------------------|
| `references/tone-guide.md` | Detailed tone & manner guide | STEP 1 |
| `references/structure-templates.md` | Article structure templates | STEP 1 |
| `references/image-guide.md` | Image guide creation | STEP 1, STEP 4 |
| `references/thumbnail-templates.md` | Thumbnail templates (palettes, AI prompts) | STEP 4 |
| `네이버_블로그_문체_가이드.md` | Writing style analysis (tone, sentence structure, patterns) | STEP 3 (mandatory), STEP 4 |

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
├── CLAUDE.md                   # Architecture guide for Claude
├── config.yaml                 # Global configuration
├── requirements.txt            # Python dependencies
├── skills/                     # Modularized skills (6 files)
│   ├── step1-topic-and-options.md  # Topic + options selection
│   ├── step2-research.md          # Research (3 parallel agents)
│   ├── step3-title-and-draft.md   # Title + draft writing
│   ├── step4-refactor.md          # Writing refactoring (txt -> HTML/MD)
│   ├── step5-image.md             # Image generation (MANDATORY)
│   └── step6-revise.md            # Revision loop
├── references/                 # Reference materials
├── templates/                  # Output templates
└── scripts/                    # Python automation (12 modules)
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

- **v3.0.3** (2026-02-16)
  - Default output path changed to `~/workspace/경제 블로그`
  - Path resolver now expands `~` and environment variables during project path construction
  - Step/documentation examples updated to the new default save location

- **v3.0.2** (2026-02-16)
  - Image generation output is now forced to 500x500 by default (`gemini.default_size`)
  - Added deterministic post-save resize so generated PNG files are always normalized to 500x500
  - Updated image guide ratio notation from 1024x1024 to 500x500 for consistency

- **v3.0.1** (2026-02-16)
  - Section subtitles in generated `본문.html` now use Naver editor-compatible markup (`se-text-paragraph` + `se-ff-system se-fs30 __se-node`)
  - Subtitle IDs now use unique `SE-<uuid>` values per block to avoid duplicate node identifiers
  - Section subtitle rendering now inherits configured `line_height`, matching paragraph spacing in the template
  - Subtitle text is HTML-escaped before rendering to prevent malformed markup in pasted content

- **v3.0.0** (2026-02-14)
  - Workflow optimization: 10 steps -> 6 steps (~40% time reduction)
  - User interactions reduced: 5+ -> 2 (topic+options, title selection)
  - Research agents reduced: 6 -> 3 (image-only search removed)
  - Config cleanup: removed unused palettes, image sizes, fallback config
  - Python cleanup: removed fallback system, deprecated methods, sync wrappers
  - Step file spec trimming: template references instead of inline examples

- **v2.3.0** (2026-02-03)
  - Gemini API single model enforcement (force_primary_only)
  - STEP 8/9 documentation enhancement

- **v2.2.0** (2026-02-01)
  - Inserted STEP 8: Writing refactoring
  - Image generation moved to STEP 9

- **v2.0.0** (2026-01-27)
  - Skill modularization (8 step files)
  - Python automation scripts added
