# 환경 설정 가이드

## 자동 설정 (권장)

첫 실행 시 자동으로:
1. `.venv` 가상환경 생성
2. 필수 패키지 설치 (PyYAML, google-genai, pillow)
3. GOOGLE_API_KEY 입력 요청 → `.env`에 저장

```bash
python3 ~/.claude/skills/search-blogging/scripts/ensure_venv.py
```

## 수동 설정

```bash
cd ~/.claude/skills/search-blogging
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo 'GOOGLE_API_KEY="your-key"' > .env
```

## API 키 재설정

```bash
rm ~/.claude/skills/search-blogging/.env
python3 ~/.claude/skills/search-blogging/scripts/ensure_venv.py
```

## Dependencies

### For Image Generation (Gemini API)
```bash
pip install google-genai pillow
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
