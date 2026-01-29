# Image Guide

## Basic Information
- Topic: ${topic}
- Date: ${date}
- Total Images: ${image_count}

## Color Palette (70-25-5 Rule)
- Main (70%): ${color_main} (${color_main_name}) - Background, primary areas
- Sub (25%): ${color_accent} (${color_accent_name}) - Accents, secondary elements
- Point (5%): ${color_point} - CTA, highlights
- Background: ${color_background}
- Text: ${color_text}

---

## [Image 1] Thumbnail

### 🎨 AI Generation (Background Only)

> **Note**: AI generates background image only. Text is added via SVG overlay.

**Korean Description:**
${thumbnail_description_kr}

**AI Generation Prompt (Background Only):**
```
${thumbnail_prompt_en_background}
```

**Style:**
- Colors: ${thumbnail_colors}
- Mood: ${thumbnail_mood}
- Format: ${thumbnail_format}
- Ratio: 16:9

**[Text Overlay Config]**
- main_text: "${title}"
- sub_text: "${subtitle}"
- position: "center"
- font_size: 48
- font_color: "#FFFFFF"
- shadow: true
- background_box: false

### 🔷 SVG Generation Guide

**Canvas:** 1300x885px (Naver OG image standard)
**Background:** ${color_main} or gradient
**Font:**
- Main: 32~48px Bold (key keywords)
- Sub: 18~24px Regular (supplementary text)

**Elements:**
1. Main text: "${title}" - center aligned, white, 48px bold
2. Sub text: "${subtitle}" - below main, light color, 24px
3. Icon/graphic: topic-related symbol - left or right placement
4. Brand element: logo or watermark - bottom corner

**Save Path:** ./images/01_썸네일.svg

---

## [Image 2] ${image2_role}

### 📷 Reference Image (if downloaded)

**File:** ${image2_filename}
**Source:** ${image2_source_url}
**Usage:** ${image2_usage}

### 🎨 AI Generation Prompt

**Korean Description:**
${image2_description_kr}

**AI Generation Prompt:**
```
${image2_prompt_en}
```

**Style:**
- Colors: ${image2_colors}
- Mood: ${image2_mood}
- Format: ${image2_format}

### 🔷 SVG Generation Guide

**Canvas:** 693x450px (Naver content basic width)
**Background:** #ffffff

**Elements:**
${image2_svg_elements}

**Save Path:** ./images/02_${image2_filename_base}.svg

---

## [Image 3] ${image3_role}

### 🎨 AI Generation Prompt

**Korean Description:**
${image3_description_kr}

**AI Generation Prompt:**
```
${image3_prompt_en}
```

**Style:**
- Colors: ${image3_colors}
- Mood: ${image3_mood}
- Format: ${image3_format}

### 🔷 SVG Generation Guide

**Canvas:** 693x450px (Naver content basic width)
**Background:** ${color_background}

**Elements:**
${image3_svg_elements}

**Save Path:** ./images/03_${image3_filename_base}.svg

---

## [Image 4] ${image4_role}

### 🎨 AI Generation Prompt

**Korean Description:**
${image4_description_kr}

**AI Generation Prompt:**
```
${image4_prompt_en}
```

### 🔷 SVG Generation Guide

**Canvas:** 693x450px (Naver content basic width)
**Background:** ${color_background}

**Elements:**
${image4_svg_elements}

**Save Path:** ./images/04_${image4_filename_base}.svg

---

## [Image 5] ${image5_role}

### 🎨 AI Generation Prompt

**Korean Description:**
${image5_description_kr}

**AI Generation Prompt:**
```
${image5_prompt_en}
```

**Save Path:** ./images/05_${image5_filename_base}.svg

---

## Image Generation Guide

### AI Image Generation Services
- **Midjourney**: High-quality artwork, use `/imagine` command
- **DALL-E 3**: Available in OpenAI ChatGPT
- **Canva AI**: Text to Image feature
- **Leonardo AI**: Free plan available

### SVG Generation (Claude + svg-canvas-mcp)
1. Create canvas with svg_create
2. Add elements with draw_* tools
3. Add text with draw_text
4. Save with svg_save

### Image Optimization
- Recommended blog upload width: 800px
- File format: JPG (photos), PNG (transparent background), SVG (vector)
- File size: 1MB or less recommended
