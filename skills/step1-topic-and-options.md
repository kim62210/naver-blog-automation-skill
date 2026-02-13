# STEP 1: Topic Selection + Options

Use Chrome DevTools MCP to collect today's popular topics from Naver Economy Shortents, let the user select one, and configure writing options in a single interaction.

## Progress Status

```
[STEP 1/6] Topic + Options ████░░░░░░░░░░░░░░░░░░░░░░░ 15%
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
Today's Top 10 Recommended Economy Blog Topics

| # | Topic | Key Content | Time | Recommendation Reason |
|---|-------|-------------|------|----------------------|
| 1 | {title} | {subtitle/description} | {time} | {timeliness/interest analysis} |
| ... | ... | ... | ... | ... |
| 10 | {title} | {subtitle/description} | {time} | {timeliness/interest analysis} |
```

### Topic Selection Criteria
1. **Timeliness**: Prioritize news within 24 hours
2. **Search volume**: Prioritize higher trending rankings
3. **Blog suitability**: Suitable for informational content
4. **Reader interest**: Relevance to daily life

---

## 1-4. User Selection + Options (Single Interaction)

Use **one AskUserQuestion call** with up to 4 questions to collect everything at once:

**Question 1: Topic Selection**
- Options: Top 4 topics from the list
- "Other" for custom input or topics 5-10

**Question 2: Tone & Manner**
- Professional (Recommended) - Objective and trustworthy tone
- Friendly - Casual conversational tone
- Neutral - Balanced information-focused tone

**Question 3: Article Structure**
- 7-step (Recommended) - Intro > Problem > Core1,2,3 > Tips > Closing
- 5-step - Intro > Core > Details > Tips > Closing
- Flexible - AI adapts structure to topic

**Question 4: Number of Images**
- Recommended (5 images) - Thumbnail + 1 per section
- Minimum (3 images) - Thumbnail + 2 core images
- Rich (7+ images) - Images for all sections

> Detailed guides: `references/tone-guide.md`, `references/structure-templates.md`, `references/image-guide.md`

---

## 1-5. Direct Topic Input (Optional)

If user directly inputs a topic in `/search-blogging topic` format:
- Skip topic collection (1-1 ~ 1-3) and show only options questions (1-4 Q2~Q4)
- Use the input topic keyword

---

## 1-6. Keyword Expansion (Automatic)

After selection, automatically expand related search keywords:

### Expansion Methods
1. **Synonyms/Similar terms**: Alternative expressions for the topic
2. **Subtopics**: Sub-categories
3. **Related questions**: What readers would be curious about
4. **Timeliness keywords**: Year, latest, changes, etc.

### Generate Search Keyword Set

```yaml
primary_keyword: "{main topic}"
secondary_keywords:
  - "{expanded keyword 1}"
  - "{expanded keyword 2}"
  - "{expanded keyword 3}"
image_keywords:
  - "{topic} infographic"
  - "{topic} comparison table"
```

---

## 1-7. Create Project Directory

```python
from scripts.setup import create_project_structure

project_path = create_project_structure(
    topic="{topic}",
    base_dir="./economy blog"
)
```

---

## 1-8. Options Summary

```
Selected topic: "{topic}"
Writing options:
- Tone & Manner: {selected tone}
- Article Structure: {selected structure}
- Number of Images: {selected count}

Starting material collection...
```

---

## Next Step

Topic + options complete -> **[STEP 2: Research](step2-research.md)**
