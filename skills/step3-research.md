# STEP 3: Parallel Research

Run 6 agents simultaneously to collect materials and images.

## Progress Status

```
[STEP 3/8] Research ████████████░░░░░░░░░░░░░░░░ 37%
```

---

## 3-1. Execution Method

Launch 6 librarian agents **in parallel** using the Task tool:

```
Agent 1: Naver News search (WebSearch - site:news.naver.com) + News image collection
Agent 2: Naver Blog search (mcp__naver-search__search_blog) + Blog image collection
Agent 3: General web search (WebSearch)
Agent 4: Extended keyword search 1 (AI generates related keywords then searches)
Agent 5: Extended keyword search 2 (AI generates related keywords then searches)
Agent 6: Image-only search (WebSearch - Naver/Google image search)
```

---

## 3-2. Collection Goals

| Item | Target |
|------|--------|
| Text materials | 5 per source, 15~25 total |
| Reference images | 10~15 (combined from news/blog/image search) |

---

## 3-3. Agent Prompt Templates

### Agent 1 - Naver News + Images

```
Search for the latest 5 Naver news articles about "{topic}".
Extract title, URL, and key content summary from each result.

**Image collection**: Also collect representative image URLs from news articles.
- Access article pages via WebFetch and extract og:image or main images from the body
- Also record image descriptions (alt text or captions)
```

### Agent 2 - Naver Blog + Images

```
Use mcp__naver-search__search_blog tool to search "{topic}" and collect 5 results.
Organize title, URL, and summary for each result.

**Image collection**: Collect image URLs embedded in blog posts.
- Prioritize infographics, tables, chart images
- Record brief description per image (e.g., "interest rate comparison table", "application process guide")
```

### Agent 3 - Web Search

```
Search for 5 reliable web sources about "{topic}".
Prioritize official agencies, financial companies, government sites.
```

### Agent 4, 5 - Extended Keywords

```
Search for additional information using related keyword "{expanded keyword}" for "{topic}".
```

### Agent 6 - Image-Only Search

```
Search for reference images about "{topic}".

**Search query examples:**
- "{topic} 인포그래픽"
- "{topic} 비교표"
- "{topic} 설명 이미지"

**Collection items:**
- Image URL
- Source page URL
- Image description (search result or alt text)
- Image type (photo/infographic/table/illustration)

**Priority collection targets:**
1. Infographics (data visualization)
2. Comparison tables/charts
3. Procedure/process guides
4. Related product/service images
```

---

## 3-4. Image Collection Criteria

| Priority | Image Type | Usage |
|----------|-----------|-------|
| 1 | Infographic | Reference for key information sections |
| 2 | Comparison table/chart | Use for data comparison sections |
| 3 | Procedure guide | Reference for guide/tips sections |
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
