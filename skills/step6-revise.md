# STEP 6: Revision Loop

Present the completed work and receive user feedback.

## Progress Status

```
[STEP 6/6] Review/Edit ████████████████████████████ 100%
```

---

## 6-1. Completion Notice

```
Blog post writing complete!

Save Location
./경제 블로그/YYYY-MM-DD/topic-name/
├── 원본.txt (Plain text draft)
├── 본문.html (HTML file)
├── 이미지 가이드.md (Image generation guide)
├── 참조.md (Source list)
└── images/  (Generated images)

How to Publish to Naver Blog
Option A (Auto): /naver-auto-post
  -> Automatically publishes with images, tags, and settings

Option B (Manual):
  1. Open 본문.html file in browser (double-click)
  2. Cmd+A (select all) -> Cmd+C (copy)
  3. Cmd+V (paste) in Naver Blog editor
  4. Upload actual images at [이미지 N 삽입] positions

Writing Info
- Body character count: XXXX chars (pure body text)
- Image guides: N
- Tags: N

Let me know if you need any revisions.
- "Change the title"
- "Make the tone more friendly"
- "Expand the 2nd section"
- "Add more image guides"

Say "done" when you're finished.
```

---

## 6-2. Handling Revision Requests

### Supported Revision Types

| Revision Request | Action |
|-----------------|--------|
| "Change the title" | Suggest 3 new titles |
| "Make tone more friendly/professional" | Rewrite entire content with new tone |
| "Expand section N" | Modify only that section |
| "Increase/decrease character count" | Adjust to specified count |
| "Change tags" | Suggest new tags |
| "Add image guide" | Generate additional image guide |
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

## 6-3. File Update After Revision

```python
from scripts.writer import save_blog_files

files = save_blog_files(
    project_path=project_path,
    html_content=updated_html_content,
    image_guide=updated_image_guide,
    references=references_md,
    validate=True
)
```

---

## 6-4. Unlimited Revision Loop

- Modify only relevant parts per user request
- Present completed work again after modification
- **Unlimited repeats allowed**

---

## 6-5. Exit Conditions

Workflow ends when:
- User indicates completion with "done", "finished", "OK", "confirm", etc.
- Or conversation ends without additional revision requests

### Exit Message

```
Blog post writing is complete!

Final save location: ./경제 블로그/YYYY-MM-DD/topic-name/

Usage summary:
1. /naver-auto-post -> Auto-publish to Naver Blog (recommended)
2. Or manually: 본문.html -> Open in browser, copy -> paste into blog
3. Upload images at [이미지 N 삽입] positions

Run /search-blogging again to write your next post.
```

---

## Error Handling

### When Search Fails
```
An error occurred while searching {source name}.
Would you like to proceed with materials from other sources?

1. Proceed with currently collected materials
2. Retry search
3. Cancel operation
```

### Auto Character Count Adjustment
Before completion, self-validate and adjust to 1850~1950 character range (target: 1900 chars)
