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

### 🎨 AI Generation (With Text)

> **Note**: AI renders text directly. PIL adds watermark only.

**Korean Description:**
${thumbnail_description_kr}

**AI Generation Prompt:**
```
Blog thumbnail image, ${topic} concept,
bold Korean text "${title}" in upper third,
subtitle "${subtitle}" in center,
${thumbnail_colors} gradient background,
eye-catching modern design, 16:9 ratio
```

**Style:**
- Colors: ${thumbnail_colors}
- Mood: ${thumbnail_mood}
- Format: ${thumbnail_format}
- Ratio: 16:9

**[Watermark Config]**
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 60
- watermark_font_size: 18
- watermark_font_color: "rgba(255,255,255,0.6)"

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

---

## [Image 4] ${image4_role}

### 🎨 AI Generation Prompt

**Korean Description:**
${image4_description_kr}

**AI Generation Prompt:**
```
${image4_prompt_en}
```

---

## [Image 5] ${image5_role}

### 🎨 AI Generation Prompt

**Korean Description:**
${image5_description_kr}

**AI Generation Prompt:**
```
${image5_prompt_en}
```

---

## Image Generation Guide

### AI Image Generation (Gemini API Auto)
Images are automatically generated via Gemini API.
Just write the prompts above and the pipeline will generate images.

### Image Optimization
- Recommended blog upload width: 800px
- File format: JPG (photos), PNG (transparent background)
- File size: 1MB or less recommended
