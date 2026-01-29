# STEP 4: Review Collection Results

Summarize collected materials and get user confirmation.

## Progress Status

```
[STEP 4/8] Review ████████████████░░░░░░░░░░░░ 50%
```

---

## 4-1. Summary Format

```
📊 Material Collection Complete

[Text Materials]
• Naver News: N items
• Official/Institutional: N items
• Practical guide: N items
• Total collected: N items (target: 6~10)

[Reference Images (Optional)]
• Downloaded: N items (target: 0~3)
• Save location: ./images/ (if any)

[Key Information Summary]
1. {key information 1}
2. {key information 2}
3. {key information 3}
...

[Material Sufficiency Assessment]
✅ Sufficient / ⚠️ Moderate / ❌ Insufficient

Proceed with writing?
1️⃣ Proceed
2️⃣ Additional search (specify keyword)
3️⃣ Change topic
```

---

## 4-2. Material Sufficiency Criteria

### ✅ Sufficient
- **6~10 text sources**
- **5~8 key information points extracted**
- At least **1 news** + **1 official** source included
- Reference images are optional (0~3 is fine)

### ⚠️ Moderate
- 4~5 text sources
- 3~4 key information points extracted
- Missing either news or official source

### ❌ Insufficient
- 3 or fewer text sources
- Less than 3 key information points extracted
- Source diversity is missing (single-source)

---

## 4-3. When Materials are Insufficient

Notify user when materials are deemed insufficient:

```
⚠️ Collected materials are insufficient.

[Missing parts]
- {specific content}

How would you like to proceed?
1️⃣ Proceed with current materials (content may be thin)
2️⃣ Search with additional keyword: "{suggested keyword}"
3️⃣ Change topic
```

---

## 4-4. Key Information Extraction

Extract key information needed for writing from collected materials:

### Extraction Items
1. **Key concepts**: Definition/overview of the topic
2. **Important figures/data**: Statistics, amounts, percentages, etc.
3. **Comparison information**: Pros and cons, before-after comparison
4. **Practical information**: Application methods, precautions
5. **Recent trends**: Changes, trends

### Information Structure

```yaml
topic: "{topic}"
key_concepts:
  - "{key concept 1}"
  - "{key concept 2}"
data_points:
  - "{figure/data 1}"
  - "{figure/data 2}"
comparisons:
  - "{comparison info}"
practical_tips:
  - "{practical tip 1}"
  - "{practical tip 2}"
recent_changes:
  - "{recent trend}"
```

---

## 4-5. Generate Reference File

Save collection results to 참조.md file:

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

## Next Step

When user selects "Proceed" → **[STEP 5: Select Writing Options](step5-options.md)**
