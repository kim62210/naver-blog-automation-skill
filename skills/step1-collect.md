# STEP 1: Trending Topic Collection

Use Chrome DevTools MCP to collect today's topics from Naver Economy Shortents. See `_flow.md` for progress.

---

## 1-1. Access Page

```
mcp__chrome-devtools__navigate_page:
  type: "url"
  url: "https://search.naver.com/search.naver?category=%EA%B2%BD%EC%A0%9C+%EC%A2%85%ED%95%A9&query=%EA%B2%BD%EC%A0%9C+%EC%A2%85%ED%95%A9+%EC%88%8F%ED%85%90%EC%B8%A0&sm=mtb_pcv&ssc=tab.shortents.all"

mcp__chrome-devtools__take_snapshot
```

---

## 1-2. Extract Topics

Parse shortents links from snapshot:
- Title (main text)
- Subtitle/description
- Post time (N hours/days ago)

---

## 1-3. Present Top 10

```
📊 Today's Top 10 Economy Topics

| # | Topic | Key Content | Time | Reason |
|---|-------|-------------|------|--------|
| 1 | {title} | {description} | {time} | {analysis} |
| ... | ... | ... | ... | ... |
```

**Selection criteria**: Timeliness (24h) > Trending rank > Blog suitability > Reader interest

---

## 1-4. User Selection

Use AskUserQuestion:
- Options 1-4, then 5-8
- Include "Other" for custom input

**Direct input**: If user provides `/search-blogging topic`, skip to STEP 2.

---

## Next Step

→ **[STEP 2: Topic Confirmation](step2-confirm.md)**
