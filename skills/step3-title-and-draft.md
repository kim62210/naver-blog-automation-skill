# STEP 3: Title Selection + Draft Writing

Generate 3 title candidates and write the draft simultaneously. Present both title options and a preview draft for user selection.

**Refer to [Naver Blog Writing Style Guide](../naver_blog_style_guide.md) for tone/sentence structure/intro-closing patterns.**

## Progress Status

```
[STEP 3/6] Title + Draft ████████████████░░░░░░░░░░░ 55%
```

---

## 3-1. Outputs

### Output (Required)
`{project_path}/draft.txt`

> This step does NOT create `body.html`, `image guide.md`, or `references.md`. (Created in STEP 4)

---

## 3-2. Title + Draft Generation Strategy

**Generate simultaneously:**
1. Create 3 title candidates
2. Write draft using the recommended title (candidate 1) immediately
3. Present both title options and draft preview to user

If user selects a different title -> replace only the title line (no full rewrite needed).

---

## 3-3. Title Writing Principles

### Required Elements
1. **Include key keyword**: Search optimization
2. **Use numbers/year**: Improve click-through rate
3. **Evoke curiosity or state benefit**: Draw reader interest
4. **Recommend under 30 characters**: Mobile optimization

### Title Patterns

| Pattern | Example |
|---------|---------|
| Number-based | "2026년 육아휴직 급여, 이렇게 달라집니다 3가지" |
| Question-based | "0세 적금 금리 7%? 진짜 가능한 상품 정리" |
| Benefit-based | "연말정산 환급액 늘리는 5가지 소득공제 꿀팁" |
| Comparison-based | "적금 vs 예금, 2026년에는 뭐가 더 유리할까?" |
| Timely | "2026년 1월 시행! 달라지는 금융 정책 총정리" |

### Title Style by Tone & Manner

| Tone | Title Style |
|------|-------------|
| Professional | "2026년 육아휴직 급여 인상, 주요 변경사항 총정리" |
| Friendly | "육아휴직 급여 이렇게 올랐어요! 꼭 알아야 할 3가지" |
| Neutral | "2026년 육아휴직 급여 변경: 금액, 기간, 신청방법" |

---

## 3-4. Title Selection (User Interaction)

```
Here are the title candidates (draft already written with #1):

1. {title 1} (Recommended)
2. {title 2}
3. {title 3}

Please select. Or say "regenerate" for new candidates.
```

- If user selects title 2 or 3 -> replace title line in draft only
- If user requests "regenerate" -> present 3 new candidates using different patterns
- If user directly inputs a title -> use as-is

---

## 3-5. Writing Style Guide (MANDATORY)

> Full guide: [Naver Blog Writing Style Guide](../naver_blog_style_guide.md)

### (1) Tone & Endings

| Ending | Ratio | Example |
|--------|-------|---------|
| ~합니다/습니다 | **70%** | "매우 인기가 많습니다", "불가능합니다" |
| ~이다/~다 (descriptive) | **20%** | "자산 기준이다", "아직 멀었다" |
| ~죠/~요 (conversational) | **10%** | "뻔하죠", "~거든요" |

- **Use first person actively**: "저도", "저는", "제가 해봐서 잘 압니다"
- **Address readers**: "여러분", "~하시는 분들", "~하시겠죠?"
- **Mix emotion with data**: add emotional comment after data presentation

### (2) Sentence/Paragraph Structure

- **Sentence length**: 20~40 chars (max 50)
- **Rhythm**: short > long > short pattern
- **Paragraph**: 1~3 sentences, frequent line breaks
- **Q&A structure**: "뭐가 다르냐? 바로 수수료입니다."

### (3) Intro Patterns

| Type | Ratio | Template |
|------|-------|----------|
| Empathy | **40%** | "{현재 트렌드}하면서 {독자 상황}하신 분들이 많을 것입니다." |
| Conclusion-first | **25%** | "결론부터 말하면 {핵심 결론}하는 게 유리하다." |
| Question-driven | **20%** | "도대체 왜 {상황}하는 걸까요?" |
| Stats/Fact | **15%** | "{핵심 수치/데이터}. 이 숫자가 의미하는 바는..." |

### (4) Closing Patterns

| Type | Ratio | Template |
|------|-------|----------|
| CTA | **45%** | "~해 보시기 바랍니다" |
| Question | **25%** | "여러분의 ~은 무엇인가요?" |
| Summary | **20%** | "정리하면 {핵심 3줄 요약}" |
| Personal | **10%** | "제 꿈은 ~입니다" |

### (5) Emphasis/Lists

- **Bold**: 5~10% of text only (key conclusions/warnings)
- **Lists**: Prefer numbered lists ("1. ...", "2. ...", "3. ...")
- **Emoji**: Minimize in body, use only for CTA (engagement prompts)

### (6) Number Formatting

| Type | Format | Example |
|------|--------|---------|
| Large amounts | Korean+Arabic mix | "3억 4천만원", "600만 원" |
| Small amounts | Arabic numerals | "1,875원", "49만 5천원" |
| Percentages | Arabic + % | "23.9%", "0.2%", "50% 이상" |
| Rankings/Counts | Arabic numerals | "TOP 5", "3가지", "10명 중 7명" |

---

## 3-6. draft.txt Writing Rules

### (1) Pure text only
- No HTML tags (`<h2>`, `<p>`, `<br>` etc.)
- No markdown formatting (`**bold**`, `__underline__` etc.)
- Separate paragraphs with **blank lines**

### (2) [Brackets] as guides only

#### Render tags (text remains, tag removed)
- `[제목] Title text`
- `[중제목] Section heading text`
- `[소제목] Sub-section heading text`
- `[인용] "Quote text"`
- `[강조:Bold] Emphasized sentence`

#### Render-excluded memos (not included in final output)
- `[[insert table here?]]`
- `[[expand this paragraph by 30~50 chars]]`

#### Image placeholders (excluded from char count)
- `[이미지 1 삽입 - 썸네일]`
- `[이미지 2 삽입]`

---

## 3-7. Character Count Rules (MANDATORY)

- Target: 1900 chars
- Allowed range: **1850~1950 chars**

### Include/Exclude Criteria (draft.txt)
- **Include**: Actual text of titles/headings/quotes/body
- **Exclude**: `[이미지 N 삽입...]` placeholders, `[[...]]` memos, `[tag]` strings themselves

### Python Validation (draft.txt)
```python
from pathlib import Path
from scripts.validator import validate_draft_char_count

draft_text = Path(project_path / "원본.txt").read_text(encoding="utf-8")
result = validate_draft_char_count(draft_text)
print(result.message)  # Valid / Over / Under
```

---

## 3-8. Section Length Guide (7-step structure)

| Section | Min | Max | Target | Style Guide Recommendation |
|---------|-----|-----|--------|---------------------------|
| Intro | 120 | 160 | 140 | Empathy(40%) or conclusion-first(25%) |
| Problem | 170 | 230 | 200 | Q&A structure, short-long-short rhythm |
| Core Info 1 | 340 | 400 | 370 | 1st person experience + data, numbered list |
| Core Info 2 | 340 | 400 | 370 | Comparison data, bold key points only |
| Core Info 3 | 340 | 400 | 370 | Reader-addressing, emotional comments |
| Practical Tips | 270 | 330 | 300 | Numbered list, checkmarks |
| Closing | 130 | 170 | 150 | CTA + question combo |

---

## 3-9. Save Location

```
~/workspace/경제 블로그/YYYY-MM-DD/topic-name/원본.txt
```

```python
from scripts.writer import save_draft_file

draft_path = save_draft_file(project_path=project_path, draft_text=draft_text, validate=True)
```

---

## Next Step

Draft writing/validation complete -> **[STEP 4: Writing Refactoring](step4-refactor.md)**
