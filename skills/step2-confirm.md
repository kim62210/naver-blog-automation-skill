# STEP 2: Topic Confirmation and Keyword Expansion

Confirm the selected topic and expand related keywords.

## Progress Status

```
[STEP 2/8] Topic confirmation ████████░░░░░░░░░░░░░░░░░░░░ 25%
```

---

## 2-1. Topic Confirmation Message

```
✅ Selected topic: "{topic}"

A blog post will be written on this topic.
Starting material collection...
```

---

## 2-2. Keyword Expansion

Expand related search keywords from the selected topic:

### Expansion Methods
1. **Synonyms/Similar terms**: Alternative expressions for the topic
2. **Subtopics**: Sub-categories
3. **Related questions**: What readers would be curious about
4. **Timeliness keywords**: Year, latest, changes, etc.

### Keyword Expansion Examples

| Input Keyword | Expanded Keywords |
|---------------|-------------------|
| 0세 적금 | 신생아 적금 금리, 아기 적금 추천 2026, 영유아 적금 비교 |
| 육아휴직 | 육아휴직 급여 계산, 육아휴직 연장 방법, 2026 육아휴직 변경 |
| 주담대 금리 | 주택담보대출 금리비교, 변동금리 고정금리, 은행별 주담대 |
| 연말정산 | 연말정산 방법, 소득공제 항목, 세액공제 계산 |

---

## 2-3. Generate Search Keyword Set

Prepare keyword sets for parallel searching:

```yaml
primary_keyword: "{main topic}"
secondary_keywords:
  - "{expanded keyword 1}"
  - "{expanded keyword 2}"
  - "{expanded keyword 3}"
image_keywords:
  - "{topic} 인포그래픽"
  - "{topic} 비교표"
  - "{topic} 설명 이미지"
```

---

## 2-4. Create Project Directory

Use Python script to auto-generate output directory:

```python
from scripts.setup import create_project_structure

project_path = create_project_structure(
    topic="{topic}",
    base_dir="./경제 블로그"
)
# Result: ./경제 블로그/2026-01-27/topic-name/
#         ├── images/
#         └── .metadata.json
```

### Generated Structure
```
./경제 블로그/YYYY-MM-DD/topic-name/
├── images/           # Image storage directory
└── .metadata.json    # Metadata file
```

---

## Next Step

Keyword expansion complete → **[STEP 3: Parallel Research](step3-research.md)**
