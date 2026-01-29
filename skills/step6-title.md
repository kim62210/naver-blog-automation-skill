# STEP 6: Title Selection

Present 3 title candidates and let user select.

## Progress Status

```
[STEP 6/8] Title selection ████████████████████████░░░░ 75%
```

---

## 6-1. Title Presentation Format

```
Here are the title candidates:

1️⃣ {title 1}
2️⃣ {title 2}
3️⃣ {title 3}

Please select. Or say "regenerate" for new candidates.
```

---

## 6-2. Title Writing Principles

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

## 6-3. Title Generation Logic

### Input Information
- Topic keywords
- Collected key information
- Selected tone & manner
- Current year/month

### Title Composition Elements

```yaml
title_elements:
  keyword: "{main keyword}"
  year: "2026년"
  benefit: "{key benefit/information}"
  number: "{number}" # optional
  question: "{question}" # optional
```

---

## 6-4. Regeneration

When user requests "regenerate":
- Present 3 new candidates
- **Unlimited repeats allowed**
- Use different patterns from previous candidates

```
Here are new title candidates:

1️⃣ {new title 1} - Question-based
2️⃣ {new title 2} - Benefit-based
3️⃣ {new title 3} - Comparison-based

Please select.
```

---

## 6-5. Direct Input

When user directly inputs a title:
- Use the input title as-is
- Only check character count/special character restrictions

---

## 6-6. Title Confirmation

```
✅ Confirmed title: "{selected title}"

Starting body content writing.
```

---

## Next Step

Title selection complete → **[STEP 7: Content Writing and Saving](step7-write.md)**
