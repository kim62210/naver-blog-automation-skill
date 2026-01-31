# STEP 1: Category Selection & Trending Topic Collection

Use Chrome DevTools MCP to collect today's topics from Naver Shortents. See `_flow.md` for progress.

---

## 1-0. Category Selection (NEW)

First, ask the user to select a category using AskUserQuestion:

```
📂 블로그 카테고리를 선택해주세요

어떤 주제의 트렌딩 토픽을 수집할까요?
```

**Option groups (present in order):**

| Group | Categories |
|-------|------------|
| 경제/금융 | 경제 종합, 생활경제, 증권, 부동산 |
| 엔터테인먼트 | 엔터 종합, 영화, 드라마, 뮤직 |
| 스포츠 | 스포츠 종합, 야구, 해외야구, 축구, 해외축구, 농구, 배구, 동계올림픽 |
| 여행/맛집 | 여행맛집 종합, 국내여행, 세계여행, 맛집/카페, 푸드 |
| 패션/뷰티 | 패션뷰티 종합, 패션트렌드, 뷰티 |
| 라이프스타일 | 리빙푸드 종합, 카테크 종합, 자동차, 지식 종합 |

**Implementation:**
1. Use AskUserQuestion with 4 options at a time (tool limit)
2. First ask for category group, then specific category
3. Store selected category for URL construction and output directory

**URL Construction:**
```
Base: https://search.naver.com/search.naver
Params:
  - category={URL encoded category param}
  - query={category name} 숏텐츠
  - sm=tab_sht.ctg
  - ssc=tab.shortents.all

Example (증권):
https://search.naver.com/search.naver?category=%EC%A6%9D%EA%B6%8C&query=%EC%A6%9D%EA%B6%8C+%EC%88%8F%ED%85%90%EC%B8%A0&sm=tab_sht.ctg&ssc=tab.shortents.all
```

---

## 1-1. Access Page

After category selection, navigate to the constructed URL:

```
mcp__chrome-devtools__navigate_page:
  type: "url"
  url: "{constructed_url_from_category}"

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
📊 Today's Top 10 {category_name} Topics

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

**Direct input**: If user provides `/search-blogging topic`, skip category selection and go to STEP 2.

---

## Output Directory

Based on selected category, use the corresponding `output_dir` from config:

```
./{category_output_dir}/YYYY-MM-DD/topic-name/
```

Examples:
- 경제 종합 → `./경제 블로그/2026-01-31/...`
- 증권 → `./증권 블로그/2026-01-31/...`
- 야구 → `./야구 블로그/2026-01-31/...`

---

## Next Step

→ **[STEP 2: Topic Confirmation](step2-confirm.md)**
