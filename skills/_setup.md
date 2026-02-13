# Environment Setup Guide

## Auto Setup (Recommended)

First run automatically:
1. Creates `.venv` virtual environment
2. Installs required packages (PyYAML, google-genai, pillow)
3. Prompts for GOOGLE_API_KEY and saves to `.env`

```bash
python3 ~/.claude/skills/search-blogging/scripts/ensure_venv.py
```

## Manual Setup

```bash
cd ~/.claude/skills/search-blogging
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo 'GOOGLE_API_KEY="your-key"' > .env
```

## API Key Reset

```bash
rm ~/.claude/skills/search-blogging/.env
python3 ~/.claude/skills/search-blogging/scripts/ensure_venv.py
```

## Dependencies

### For Image Generation (Gemini API)
```bash
pip install google-genai pillow
```

## Limits & Model Order (Config-driven)

- Rate limiting/delay is configured in `config.yaml` (`gemini.rate_limit.*`) and enforced by the generator.
- Model: `gemini-3-pro-image-preview` only (`gemini.models.primary`).
- Exact quotas/availability/cost vary by account and can change.

## Quick Start

```python
from scripts.image_pipeline import ImagePipeline

pipeline = ImagePipeline()
result = await pipeline.process_image_guide(
    image_guide_content=open("./이미지 가이드.md").read(),
    output_dir="./images/"
)
print(result.summary())
```
