# Environment Setup Guide

## Required Environment Variables

```bash
export GOOGLE_API_KEY="your-api-key"
```

## Dependencies

### For Image Generation (Gemini API)
```bash
pip install google-generativeai pillow
```

### For SVG to PNG Conversion (Text Overlay)
```bash
# Option 1: Recommended
pip install cairosvg

# Option 2: System package
sudo apt install librsvg2-bin

# Option 3: Fallback
pip install svglib reportlab
```

## API Limits

| Model | RPM | Daily Quota | Cost |
|-------|-----|-------------|------|
| gemini-2.0-flash-exp | 10 | 100-500 | Free |
| gemini-2.5-flash-image | 15 | 500 | Free/Paid |
| gemini-3-pro-image | - | - | $0.134/img |

## Quick Start

```python
from scripts.gemini_image import GeminiImageGenerator
from scripts.image_pipeline import ImagePipeline

# Single image
gen = GeminiImageGenerator()
result = await gen.generate_image("prompt", "output.png")

# Batch from image guide
pipeline = ImagePipeline()
result = await pipeline.process_image_guide(content, "./images/")
```
