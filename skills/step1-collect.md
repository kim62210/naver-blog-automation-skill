# STEP 1: Trending Topic Collection and Selection

Use Chrome DevTools MCP to collect today's popular topics from Naver Economy Shortents, and let the user select one.

## Progress Status

```
[STEP 1/8] Topic collection ████░░░░░░░░░░░░░░░░░░░░░░░░ 12%
```

---

## 1-1. Access Naver Economy Shortents Page

Use Chrome DevTools MCP tools to access the page:

```
1. Call mcp__chrome-devtools__navigate_page:
   - type: "url"
   - url: "https://search.naver.com/search.naver?category=%EA%B2%BD%EC%A0%9C+%EC%A2%85%ED%95%A9&query=%EA%B2%BD%EC%A0%9C+%EC%A2%85%ED%95%A9+%EC%88%8F%ED%85%90%EC%B8%A0&sm=mtb_pcv&ssc=tab.shortents.all"
   - timeout: 30000

2. Call mcp__chrome-devtools__take_snapshot:
   - Capture page content snapshot
```

---

## 1-2. Topic Extraction

Parse economy-related shortents links from the snapshot:

**Extraction targets:**
- `link` elements for shortents content (identify by uid pattern)
- Extract title (StaticText) and time information from each link

**Extracted data:**
- Title (main title)
- Subtitle/description
- Post time (N hours ago, N days ago)

---

## 1-3. Select and Present 10 Topics

Select 10 topics from collected items based on timeliness and blog suitability, then present in a table:

```
📊 Today's Top 10 Recommended Economy Blog Topics

| # | Topic | Key Content | Time | Recommendation Reason |
|---|-------|-------------|------|----------------------|
| 1 | {title} | {subtitle/description} | {time} | {timeliness/interest analysis} |
| 2 | {title} | {subtitle/description} | {time} | {timeliness/interest analysis} |
| ... | ... | ... | ... | ... |
| 10 | {title} | {subtitle/description} | {time} | {timeliness/interest analysis} |
```

### Topic Selection Criteria
1. **Timeliness**: Prioritize news within 24 hours
2. **Search volume**: Prioritize higher trending rankings
3. **Blog suitability**: Suitable for informational content
4. **Reader interest**: Relevance to daily life

---

## 1-4. User Selection

Use AskUserQuestion tool to let user select a topic:

**Question structure:**
- First question: Topic choices 1-4
- Second question: Topic choices 5-8 (if not in above)
- "Other" option for custom input

**After selection:**
- Proceed to STEP 2 based on selected topic
- Use the keyword if user directly inputs

---

## 1-5. Direct Topic Input (Optional)

If user directly inputs a topic in `/search-blogging topic` format:
- Skip STEP 1 and proceed directly to STEP 2
- Use the input topic keyword

---

## Next Step

When topic is selected → **[STEP 2: Topic Confirmation and Keyword Expansion](step2-confirm.md)**
