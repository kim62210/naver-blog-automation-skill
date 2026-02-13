# STEP 2: Research (3 Parallel Agents)

Run 3 agents simultaneously to collect materials. Auto-assess sufficiency and proceed.

## Progress Status

```
[STEP 2/6] Research ████████░░░░░░░░░░░░░░░░░░░ 30%
```

---

## 2-1. Execution Method

Launch 3 librarian agents **in parallel** using the Task tool:

```
Agent 1: Naver News search (WebSearch - site:news.naver.com) + News image collection
Agent 2: Naver Blog search (mcp__naver-search__search_blog) + Blog image collection
Agent 3: General web + Extended keyword search (WebSearch with primary + expanded keywords)
```

> Agent 6 (image-only search) removed: images are generated via Gemini AI, reference image collection is unnecessary.
> Agents 4+5 (extended keyword searches) merged into Agent 3.

---

## 2-2. Collection Goals

| Item | Target |
|------|--------|
| Text materials | 5 per source, 15~25 total |
| Reference images | Optional (AI-generated images are primary) |

---

## 2-3. Agent Prompt Templates

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
- Record brief description per image
```

### Agent 3 - Web Search + Extended Keywords

```
Search for reliable web sources about "{topic}".
Prioritize official agencies, financial companies, government sites.

Also search with related keywords:
- "{expanded keyword 1}"
- "{expanded keyword 2}"
- "{expanded keyword 3}"

Collect 5-10 results total across all keyword searches.
```

---

## 2-4. Sufficiency Auto-Assessment

After all agents complete, automatically evaluate material sufficiency:

### Auto-proceed (no user interaction needed)
- **15+ text materials** collected
- **5+ key information points** extracted
- **Diverse sources** (news + blog + official sites)

### Ask user (only when materials are insufficient)
- **Less than 10 text materials** -> Ask whether to proceed or search more

```
Material collection: {N} items collected.

Collected materials may be insufficient.

[Missing parts]
- {specific content}

How would you like to proceed?
1. Proceed with current materials
2. Search with additional keyword: "{suggested keyword}"
3. Change topic
```

---

## 2-5. Key Information Extraction

Extract key information from collected materials:

1. **Key concepts**: Definition/overview of the topic
2. **Important figures/data**: Statistics, amounts, percentages
3. **Comparison information**: Pros and cons, before-after comparison
4. **Practical information**: Application methods, precautions
5. **Recent trends**: Changes, trends

---

## 2-6. Generate Reference File

Save collection results to reference file:

```python
from scripts.writer import generate_references, save_blog_files

references_md = generate_references(
    topic="{topic}",
    text_sources={
        "Naver News": news_results,
        "Naver Blog": blog_results,
        "Web Search": web_results
    },
    images=collected_images
)
```

---

## 2-7. Summary (Auto-displayed)

```
Material Collection Complete

[Text Materials]
- Naver News: N items
- Naver Blog: N items
- Web search: N items
- Total collected: N items

[Key Information Summary]
1. {key information 1}
2. {key information 2}
3. {key information 3}

Proceeding to title generation and draft writing...
```

---

## Next Step

Research complete -> **[STEP 3: Title + Draft](step3-title-and-draft.md)**
