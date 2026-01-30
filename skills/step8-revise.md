# STEP 8: Revision Loop

Present completed work and handle feedback. See `_flow.md` for progress.

---

## 8-1. Completion Notice

```
✅ Blog post complete!

📁 ./경제 블로그/YYYY-MM-DD/topic/
├── 본문.html
├── 이미지 가이드.md
├── 참조.md
└── images/

📋 Paste to Naver Blog:
1. Open 본문.html in browser
2. Cmd+A → Cmd+C
3. Cmd+V in editor
4. Upload images at [이미지 N 삽입]

📊 Stats: XXXX chars, N images, N tags

Revisions? Say "done" when finished.
```

---

## 8-2. Revision Types

| Request | Action |
|---------|--------|
| Change title | Suggest 3 alternatives |
| Change tone | Rewrite with new style |
| Expand section | Modify specific section |
| Adjust length | Add/remove content |
| Add images | Generate more guides |
| Generate SVG | Create via svg-canvas-mcp |

---

## 8-3. SVG Generation

```python
mcp__svg-canvas__svg_create(width=800, height=450, background="#ffffff")
mcp__svg-canvas__draw_rect(x=200, y=260, width=120, height=90, fill="#B0B0B0")
mcp__svg-canvas__draw_text(x=260, y=380, text="일반 적금 3%", fontSize=14)
mcp__svg-canvas__svg_save(filePath="./images/chart.svg")
```

---

## 8-4. Save After Revision

```python
from scripts.writer import save_blog_files
files = save_blog_files(project_path, html_content, image_guide, references, validate=True)
```

---

## 8-5. Exit

Workflow ends when user says "done", "finished", "OK", etc.

```
✨ Complete!
📁 Final: ./경제 블로그/YYYY-MM-DD/topic/
Run /search-blogging for next post.
```
