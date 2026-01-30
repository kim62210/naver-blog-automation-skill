# STEP 2: Topic Confirmation

Confirm topic and expand keywords. See `_flow.md` for progress.

---

## 2-1. Confirmation

```
✅ Selected topic: "{topic}"
Starting material collection...
```

---

## 2-2. Keyword Expansion

| Method | Example |
|--------|---------|
| Synonyms | 0세 적금 → 신생아 적금, 아기 적금 |
| Subtopics | 금리, 비교, 추천 2026 |
| Questions | 금리 몇%?, 어떻게 가입? |
| Timeliness | 2026, 최신, 변경사항 |

---

## 2-3. Search Keyword Set

```yaml
primary_keyword: "{main topic}"
secondary_keywords: ["{expanded 1}", "{expanded 2}"]
image_keywords: ["{topic} 인포그래픽", "{topic} 비교표"]
```

---

## 2-4. Create Project Directory

```python
from scripts.setup import create_project_structure
project_path = create_project_structure(topic="{topic}", base_dir="./경제 블로그")
```

**Result**: `./경제 블로그/YYYY-MM-DD/topic/` with `images/` and `.metadata.json`

---

## Next Step

→ **[STEP 3: Parallel Research](step3-research.md)**
