# STEP 3: Parallel Research

Run a small number of agents in parallel to collect only the minimum materials needed for a 1800~2000자 글.

## Progress Status

```
[STEP 3/8] Research ████████████░░░░░░░░░░░░░░░░ 37%
```

---

## 3-1. Execution Method

Launch 3 librarian agents **in parallel** using the Task tool:

```
Agent 1: Naver News search (WebSearch - site:news.naver.com)
Agent 2: Official/Institutional sources (WebSearch - gov/agency/bank/company)
Agent 3: Practical guide / explanation (Naver Blog or general web)
```

> ✅ Stop early rule: When you have **6~10 sources** and can extract **5~8 key points + 2~4 numbers/data**, proceed to STEP 4 (do not keep searching).

---

## 3-2. Collection Goals

| Item | Target |
|------|--------|
| Text materials | 2~3 per source, **6~10 total** |
| Reference images | **0~3 (optional)** — only when Mode A is needed |

---

## 3-3. Agent Prompt Templates

### Agent 1 - Naver News (3 results)

```
Search for the latest 3 Naver news articles about "{topic}" (site:news.naver.com).
For each result, extract:
- title
- URL
- publish date/time
- 2~3 bullet key facts (numbers/changes/quotes if present)
```

### Agent 2 - Official / Institutional (3 results)

```
Search for 3 reliable official sources about "{topic}".
Prioritize:
- Government/agency (go.kr, or.kr, etc.)
- Public institutions
- Bank/company official pages (when topic is product/policy)

For each result, extract:
- title
- URL
- 2~3 bullet key facts (definition/requirements/process/criteria)
```

### Agent 3 - Practical Guide (2 results)

```
Search for 2 practical explanation sources about "{topic}" (Naver Blog or reliable web).
Extract:
- title
- URL
- 3~5 bullet tips or FAQ-style answers (what readers actually ask)
```

### Optional - Minimal Reference Images (0~3)

```
Only if you need Mode A (reference image insertion):
- Find up to 3 infographics/tables that directly match the article’s key sections.
- Record: image URL, source page URL, 1-line description, type (infographic/table/photo).
```

---

## 3-4. Image Collection Criteria

| Priority | Image Type | Usage |
|----------|-----------|-------|
| 1 | Infographic | Reference for key information sections |
| 2 | Comparison table/chart | Reference for comparisons / numbers |
| 3 | Procedure guide | Reference for steps / checklist |
| 4 | Product/service image | Visual material for body |
| 5 | Emotional image | Mood for intro/closing |

---

## 3-5. Image Download and Save

### Using Python Script

```python
from scripts.collector import collect_images, print_collection_report

images = [
    {
        "url": "{image URL}",
        "source_url": "{source URL}",
        "source_name": "News",
        "description": "Interest rate comparison table",
        "type": "Infographic"
    },
    # ... more images
]

result = collect_images(images, project_path)
print_collection_report(result)
```

### Manual Download (curl)

```bash
# Create directory
mkdir -p "./경제 블로그/YYYY-MM-DD/topic-name/images"

# Download images
# Filename format: {number}_{source}_{description}.{extension}
curl -L -o "./images/01_뉴스_금리비교표.jpg" "{image URL}"
curl -L -o "./images/02_블로그_신청절차.png" "{image URL}"
```

### Filename Rules
- Number: 01, 02, 03... (collection order)
- Source: 뉴스/블로그/검색 (News/Blog/Search)
- Description summary: Korean summary of image content (no spaces)
- Extension: Extract from original URL (jpg, png, gif, webp)

### Download Notes
- Use `-L` option to follow redirects
- Add User-Agent header if needed: `-H "User-Agent: Mozilla/5.0"`
- Record URL only in 참조.md if download fails

---

## Next Step

Research complete → **[STEP 4: Review Collection Results](step4-review.md)**
