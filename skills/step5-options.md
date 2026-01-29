# STEP 5: Select Writing Options

Ask the user 3 questions in sequence.

## Progress Status

```
[STEP 5/8] Options ████████████████████░░░░░░░░ 62%
```

---

## 5-1. Tone & Manner

```
Please select the tone & manner for your article:

1️⃣ **Professional** - Objective and trustworthy tone (suitable for finance/health/legal information)
2️⃣ **Friendly** - Casual conversational tone (suitable for parenting/reviews/daily tips)
3️⃣ **Neutral** - Balanced information-focused tone (suitable for comparisons/guides)
```

### Tone & Manner Details

| Tone | Style | Suitable Topics | Example Sentence |
|------|-------|-----------------|------------------|
| Professional | 합니다/습니다 (formal) | Finance, Health, Legal | "이 상품의 금리는 연 7%로, 시중 평균 대비 높은 편입니다." |
| Friendly | Informal speech | Parenting, Reviews, Daily life | "이거 진짜 대박이에요! 저도 써보고 깜짝 놀랐어요~" |
| Neutral | Mixed | Comparison, Guide, News | "A 상품과 B 상품을 비교해 보면 다음과 같은 차이가 있습니다." |

> Detailed guide: See `references/tone-guide.md`

---

## 5-2. Article Structure

```
Please select the article structure:

1️⃣ **7-Step Structure** - Intro→Problem→Core1,2,3→Tips→Closing (optimal for informational articles)
2️⃣ **5-Step Structure** - Intro→Core→Details→Tips→Closing (suitable for concise delivery)
3️⃣ **Flexible Structure** - AI adapts structure to topic (storytelling/Q&A etc.)
```

### Character Distribution by Structure (Target: 1850 chars)

#### 7-Step Structure
| Section | Characters |
|---------|------------|
| Introduction | 50~100 chars |
| Problem statement | 100~150 chars |
| Core information 1 | 300~400 chars |
| Core information 2 | 300~400 chars |
| Core information 3 | 300~400 chars |
| Practical tips | 200~300 chars |
| Closing | 100~150 chars |

#### 5-Step Structure
| Section | Characters |
|---------|------------|
| Intro + Problem | 150~200 chars |
| Core information | 600~800 chars |
| Detailed explanation | 400~500 chars |
| Practical tips | 200~300 chars |
| Closing | 100~150 chars |

> Detailed guide: See `references/structure-templates.md`

---

## 5-3. Number of Images

AI analyzes the topic and suggests recommended number of images first:

```
How many image guides should be included?

Based on topic analysis, **N images** are recommended:
- 1 thumbnail
- N body images
- N infographics

1️⃣ **As recommended** (N images)
2️⃣ **Minimum** (3 images - thumbnail + 2 core images)
3️⃣ **Rich** (N+2 images - images for all sections)
```

### Image Count Guidelines

| Article Length | Recommended Images | Composition |
|----------------|-------------------|-------------|
| Under 1500 chars | 3 | Thumbnail + 2 core images |
| 1500~2000 chars | 4 | Thumbnail + 2 core images + 1 infographic |
| Over 2000 chars | 7+ | Images for all sections |

> Detailed guide: See `references/image-guide.md`

---

## 5-4. Options Summary

Summarize and confirm selected options:

```
📝 Writing Options Confirmed

• Tone & Manner: {selected tone}
• Article Structure: {selected structure}
• Number of Images: {selected count}

Proceed with generating title candidates?
```

---

## config.yaml Integration

Selected options integrate with config.yaml presets:

```yaml
# Load from config.yaml
tones:
  professional:
    name: "전문적"
    style: "합니다/습니다"

structures:
  standard:
    name: "7단계"
    sections: 7
```

---

## Next Step

Options selection complete → **[STEP 6: Title Selection](step6-title.md)**
