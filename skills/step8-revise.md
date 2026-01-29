# STEP 8: Revision Loop

Present the completed work and receive user feedback.

## Progress Status

```
[STEP 8/8] Review/Edit ████████████████████████████ 100%
```

---

## 8-1. Completion Notice

```
✅ Blog post writing complete!

📁 Save Location
./경제 블로그/YYYY-MM-DD/topic-name/
├── 본문.html (HTML file)
├── 이미지 가이드.md (Image generation guide)
├── 참조.md (Source list)
└── images/  (Reference images + Generated SVGs)

📋 How to Paste into Naver Blog
1. Open 본문.html file in browser (double-click)
2. Cmd+A (select all) → Cmd+C (copy)
3. Cmd+V (paste) in Naver Blog editor
4. Upload actual images at [이미지 N 삽입] positions

📊 Writing Info
- Body character count: XXXX chars (pure body text)
- Image guides: N
  - 🔷 SVG generation: N
  - 🎨 AI generation: N
  - 📷 Reference images: N
- Tags: N

Let me know if you need any revisions.
- "Change the title"
- "Make the tone more friendly"
- "Expand the 2nd section"
- "Add more image guides"
- "Generate SVG directly"

Say "done" when you're finished.
```

---

## 8-2. Handling Revision Requests

### Supported Revision Types

| Revision Request | Action |
|-----------------|--------|
| "Change the title" | Suggest 3 new titles |
| "Make tone more friendly/professional" | Rewrite entire content with new tone |
| "Expand section N" | Modify only that section |
| "Increase/decrease character count" | Adjust to specified count |
| "Change tags" | Suggest new tags |
| "Add image guide" | Generate additional image guide |
| "Generate SVG directly" | Create SVG file via svg-canvas-mcp |
| "Add a table" | Insert related data table |

### Revision Process

```
1. Receive user revision request
2. Modify only relevant parts (minimize full rewrites)
3. Present modified content preview
4. Update files
5. Present completed work again
```

---

## 8-3. Immediate SVG Image Generation

When user requests "Generate SVG directly":

```
Which image should be generated as SVG?

Image list from 이미지 가이드.md:
1. Thumbnail (1200x630px)
2. Interest rate comparison chart (800x450px)
3. Application process infographic (800x600px)

Select a number or say "all".
```

### SVG Generation Execution

```python
# Using svg-canvas-mcp tools
# Example: Creating bar chart

mcp__svg-canvas__svg_create(width=800, height=450, background="#ffffff")
mcp__svg-canvas__draw_rect(x=200, y=260, width=120, height=90, fill="#B0B0B0")
mcp__svg-canvas__draw_rect(x=480, y=140, width=120, height=210, fill="#FFD700")
mcp__svg-canvas__draw_text(x=260, y=380, text="일반 적금 3%", fontSize=14)
mcp__svg-canvas__draw_text(x=540, y=380, text="특판 적금 7%", fontSize=14)
mcp__svg-canvas__svg_save(filePath="./images/02_금리비교차트.svg")
```

---

## 8-4. File Update After Revision

```python
from scripts.writer import save_blog_files

# Save files again with modified content
files = save_blog_files(
    project_path=project_path,
    html_content=updated_html_content,
    image_guide=updated_image_guide,
    references=references_md,
    validate=True
)
```

---

## 8-5. Unlimited Revision Loop

- Modify only relevant parts per user request
- Present completed work again after modification
- **Unlimited repeats allowed**

```
Revision complete!

📝 Changes Made
- {summary of changes}

📊 Current Info
- Body character count: XXXX chars
- Image guides: N

Let me know if you need more revisions.
Say "done" when you're finished.
```

---

## 8-6. Exit Conditions

Workflow ends when one of these occurs:
- User indicates completion with "done", "finished", "OK", "confirm", etc.
- Or conversation ends without additional revision requests

### Exit Message

```
✨ Blog post writing is complete!

📁 Final save location: ./경제 블로그/YYYY-MM-DD/topic-name/

Usage summary:
1. 본문.html → Open in browser, copy → paste into blog
2. 이미지 가이드.md → Generate images with AI or SVG
3. Upload images at [이미지 N 삽입] positions

Run /search-blogging again to write your next post.
```

---

## Error Handling

### When Search Fails
```
⚠️ An error occurred while searching {source name}.
Would you like to proceed with materials from other sources?

1️⃣ Proceed with currently collected materials
2️⃣ Retry search
3️⃣ Cancel operation
```

### Auto Character Count Adjustment
Before completion, self-validate and adjust to 1800~1900 character range (target: 1850 chars)
