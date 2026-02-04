# STEP 8: Writing Refactoring (원본.txt → HTML/MD 생성)

STEP 7에서 저장한 `원본.txt`(일반 텍스트 + [괄호] 가이드)를 기반으로, 실제 블로그 업로드용 파일들을 생성합니다.

> 📖 **문체 가이드 참조**: [네이버 블로그 문체 가이드](../네이버_블로그_문체_가이드.md)의 톤/문장 구조가 원본.txt에 적용되었는지 확인하면서 리팩토링합니다.

## Progress Status

```
[STEP 8/10] Writing refactoring ███████████████████████░░░░ 80%
```

---

## 8-1. Inputs → Outputs

### Input (Required)
- `{project_path}/원본.txt`

### Output (Generate in this step)
```
./경제 블로그/YYYY-MM-DD/{topic-slug}/
├── 원본.txt               # [STEP 7] 순수 텍스트 원고 (STEP 8 이후 수정 금지)
├── 본문.html              # [STEP 8] 블로그 HTML (네이버 블로그 붙여넣기용)
├── 이미지 가이드.md       # [STEP 8] 이미지 생성 프롬프트 명세
├── 참조.md               # [STEP 8] 출처 및 참고자료
└── images/                # [STEP 9] 생성된 이미지
    ├── 01_썸네일.png
    ├── 02_{역할}.png
    └── ...
```

**경로 규칙:**
- `base_dir`: `config.yaml` → `output.base_dir` (기본값: `./경제 블로그`)
- `date`: `YYYY-MM-DD` 형식 (`config.yaml` → `output.date_format`)
- `topic-slug`: 주제명 (한글 허용, 특수문자 제거)
- 인코딩: UTF-8 (`config.yaml` → `output.encoding`)

> STEP 9에서 `이미지 가이드.md`를 읽어 이미지를 생성합니다.

---

## 8-2. 원본.txt 정리 원칙 (Draft Cleanup)

### 목표
- STEP 7에서 작성한 **본문 텍스트의 의미/분량은 유지**
- **스타일 결정(볼드/언더라인/이탤릭/폰트 크기 등)은 이 단계에서 확정**
- 최종 `본문.html`의 **순수 텍스트 글자수는 1850~1950자** 유지

### 권장 원본.txt 표기 규칙 (가이드/렌더 분리)

- **렌더 대상(블로그에 실제로 보이는 텍스트)**: 한 줄의 시작에 “스타일 태그”를 붙이고, 뒤에 실제 문구를 둡니다.
  - 예: `[중제목] 육아휴직 급여, 2026년에 뭐가 바뀌나`
  - 예: `[인용] "급여 인상은 체감 효과가 가장 큰 변화다"`
- **렌더 제외(내부 메모/판단 힌트)**: `[[...]]` 한 줄 메모로 작성합니다.
  - 예: `[[여기 표를 넣을지 판단]]`
- **이미지 위치**: `[이미지 1 삽입 - 썸네일]`, `[이미지 2 삽입]` 형식 유지
  - 글자수 카운트에서 제외됩니다.

> 위 규칙을 따르면 “태그/메모를 제거한 순수 텍스트”와 “최종 HTML의 순수 텍스트”가 거의 동일하게 유지됩니다.

---

## 8-3. Writing Refactoring (스타일·레이아웃 최종 결정)

아래 항목을 **구간별로 분석해서 최종 결정을 내립니다**.

### (1) 강조 체계
- **Bold**: 결론/핵심 수치/행동 CTA 중심으로 제한적으로 사용
- **Underline**: “실행해야 하는 문장(신청 조건/방법/주의)”에만 사용
- **Italic**: 용어 정의/보조 설명에만 사용 (남용 금지)

### (2) 폰트 크기 체계 (Naver Blog 기준)
- 제목: 28px
- 중제목: 24px
- 소제목: 19px
- 본문: 16px
- 각주/출처: 11px

> 기준값은 `config.yaml`의 `typography.blog_sizes`와 동일해야 합니다.

### (3) 가독성/리듬
- 문장 길이: **20~40자** (문체 가이드 기준, 최대 50자)
- 문단 길이: 1~3문장 (줄바꿈 적극 활용)
- 문단 사이: 빈 줄(또는 `<br><br>`)로 호흡 확보
- 리듬: short(15~25자) → long(35~45자) → short(15~25자) 반복

---

## 8-4. 본문.html 생성 규칙 (원본.txt → HTML)

### 8-4-1. HTML 필수 구조

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    /* CSS 스타일 (8-4-2 참조) */
  </style>
</head>
<body>

<h1>{제목}</h1>

<div class="image-placeholder">[이미지 1 삽입 - 썸네일]</div>

<hr>

<!-- 섹션 반복 -->
<h2>{섹션 제목}</h2>
<p>{본문 내용}</p>
<div class="image-placeholder">[이미지 N 삽입]</div>
<hr>

<!-- 태그 -->
<p class="tags">#태그1 #태그2 #태그3 ...</p>

</body>
</html>
```

### 8-4-2. CSS Style Specification

아래 값은 `config.yaml` → `typography.blog_sizes`에서 가져오며, 기본값은 다음과 같다:

| Selector | Property | Value | config.yaml 경로 |
|----------|----------|-------|-------------------|
| `body` | `font-family` | `Nanum Gothic, Pretendard, sans-serif` | `typography.font_family` |
| `body` | `line-height` | `1.8` | `typography.line_height` |
| `body` | `max-width` | `700px` | (하드코딩) |
| `h1` | `font-size` | `28px` | `typography.blog_sizes.title` |
| `h2` | `font-size` | `24px` | `typography.blog_sizes.title_medium` |
| `h3` | `font-size` | `19px` | `typography.blog_sizes.title_small` |
| `p` | `font-size` | `16px` | `typography.blog_sizes.body` |
| `.small` | `font-size` | `11px` | `typography.blog_sizes.footnote` |
| `blockquote` | `border-left` | `4px solid #4A90D9` | (하드코딩) |
| `.highlight-quote` | `background` | `#f0f7ff` | (하드코딩) |
| `.cta` | `font-size` | `24px` | (하드코딩) |
| `.image-placeholder` | `background` | `#f9f9f9` | (하드코딩) |
| `.tags` | `color` | `#4A90D9` | (하드코딩) |

### 8-4-3. 태그 → HTML 변환 규칙

| 원본.txt 태그 | HTML 변환 | 비고 |
|------|----------|------|
| `[중제목]` | `<h2>` 또는 24px bold 스타일 | |
| `[소제목]` | `<h3>` 또는 19px bold 스타일 | |
| `[인용]` | `<blockquote>` (배경/패딩 적용) | |
| 일반 문단 | `<p>` 단위 분리 + 문장 단위 `<br>` | |
| `[이미지 N 삽입 ...]` | `<div class="image-placeholder">` | 텍스트 그대로 유지 |

### 8-4-4. 이미지 플레이스홀더 형식

```html
<!-- 썸네일 (항상 이미지 1) -->
<div class="image-placeholder">[이미지 1 삽입 - 썸네일]</div>

<!-- 본문 이미지 (이미지 2부터) -->
<div class="image-placeholder">[이미지 N 삽입]</div>
```

- 형식: `[이미지 {N} 삽입]` 또는 `[이미지 {N} 삽입 - {설명}]`
- 이미지 1은 항상 썸네일
- 이미지 인덱스는 2부터 순차 증가
- `validator.py`에서 글자수 카운트 시 제외됨 (정규식: `\[이미지\s*\d+\s*삽입[^\]]*\]`)

### 8-4-5. 줄바꿈 규칙 (가독성)

1. 문장 끝: `<br>` 1개
2. 문단 사이: `<br><br>` 또는 `<p>` 분리로 빈 줄 1개 확보

### 8-4-6. 금지 패턴

- `<script>` 태그 사용 금지
- 인라인 JavaScript 금지
- 외부 리소스 로딩 (`<link>`, `<img src="http...">`) 금지
- 네이버 블로그 에디터에서 지원하지 않는 CSS 속성 사용 자제

### 8-4-7. 글자수 검증

#### 타겟

| 항목 | 값 | config.yaml 경로 |
|------|-----|-------------------|
| 타겟 글자수 | 1900자 | `writing.char_count` |
| 허용 오차 | ±50자 | `writing.char_tolerance` |
| 최소 | 1850자 | `writing.min_chars` |
| 최대 | 1950자 | `writing.max_chars` |

환경변수 `BLOG_CHAR_COUNT`로 타겟 오버라이드 가능.

#### 카운트 제외 대상

순수 텍스트만 카운트한다. 아래 항목은 **제외**:

| 제외 대상 | 제거 방법 (validator.py) |
|-----------|--------------------------|
| CSS `<style>...</style>` 블록 | `re.sub(r'<style[^>]*>.*?</style>', ...)` |
| HTML 주석 `<!-- ... -->` | `re.sub(r'<!--.*?-->', ...)` |
| HTML 태그 `<tag>` | `re.sub(r'<[^>]+>', ...)` |
| 이미지 플레이스홀더 `[이미지 N 삽입...]` | `re.sub(r'\[이미지\s*\d+\s*삽입[^\]]*\]', ...)` |
| 해시태그 `#태그` | `re.sub(r'(?:^|\s)#\S+', ...)` |

공백은 카운트에 **포함**된다 (`include_spaces=True` 기본값).

#### Draft vs HTML 검증

| 대상 | 함수 | 추가 제외 항목 |
|------|------|---------------|
| `원본.txt` | `validate_draft_char_count()` | 메모 블록 `[[...]]`, 렌더 태그 `[제목]`, `[중제목]` 등, 인라인 마커 `[B]`, `[/B]` 등 |
| `본문.html` | `validate_char_count()` | (위 기본 규칙만 적용) |

```python
from scripts.validator import validate_char_count, validate_draft_char_count

# HTML 검증
result = validate_char_count(html_content)
print(result.message)

# Draft 검증
draft_result = validate_draft_char_count(draft_text)
print(draft_result.message)
```

### 8-4-8. 본문.html 완전 예시

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Nanum Gothic, Pretendard, sans-serif; line-height: 1.8; max-width: 700px; margin: 0 auto; padding: 20px; }
    h1 { font-size: 28px; font-weight: bold; margin-bottom: 20px; }
    h2 { font-size: 24px; font-weight: bold; margin: 32px 0 16px; }
    h3 { font-size: 19px; font-weight: bold; margin: 24px 0 12px; }
    p { font-size: 16px; margin: 12px 0; }
    blockquote { border-left: 4px solid #4A90D9; padding-left: 16px; color: #555; margin: 16px 0; }
    .highlight-quote { background: #f0f7ff; padding: 16px; border-radius: 8px; border-left: none; }
    hr { border: none; border-top: 1px solid #ddd; margin: 24px 0; }
    .thick-hr { border-top: 3px solid #333; }
    table { border-collapse: collapse; width: 100%; margin: 16px 0; }
    th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
    th { background: #f5f5f5; font-weight: bold; }
    .cta { font-size: 24px; font-weight: bold; text-align: center; margin: 32px 0; color: #4A90D9; }
    .small { font-size: 11px; color: #888; }
    .image-placeholder { color: #999; text-align: center; padding: 40px; background: #f9f9f9; margin: 16px 0; }
    .tags { color: #4A90D9; margin-top: 32px; }
  </style>
</head>
<body>

<h1>2026년 적금 금리 비교 총정리</h1>

<div class="image-placeholder">[이미지 1 삽입 - 썸네일]</div>

<hr>

<h2>왜 지금 적금에 주목해야 할까?</h2>

<blockquote>
"금리 인하기에 오히려 적금이 답이 될 수 있습니다."
</blockquote>

<p>2026년 들어 기준금리가 연속 인하되면서...</p>

<div class="image-placeholder">[이미지 2 삽입]</div>

<hr>

<h2>주요 은행별 적금 금리 비교</h2>

<table>
<tr><th>은행</th><th>상품명</th><th>금리</th></tr>
<tr><td>국민은행</td><td>KB스타적금</td><td>3.5%</td></tr>
</table>

<p>위 표에서 볼 수 있듯이...</p>

<div class="image-placeholder">[이미지 3 삽입]</div>

<hr>

<p class="cta">지금 바로 금리 비교하고 최적의 적금 찾아보세요!</p>

<hr>

<p class="tags">#적금 #금리비교 #2026적금 #고금리적금 #재테크 #저축 #은행금리 #적금추천</p>

</body>
</html>
```

---

## 8-5. 이미지 가이드.md 생성 규칙

### 8-5-1. 공통 규칙

- `본문.html`의 **섹션 흐름/핵심 메시지**에 맞춰 이미지 역할을 정의합니다.
- 모든 이미지 비율: **1:1 (1024x1024)** 고정 (`config.yaml` → `gemini.default_size`)
- 모든 이미지에 `[Watermark Config]` 6필드 필수 (아래 8-5-5 참조)
- 이미지별 섹션은 "충분히 구체적인 프롬프트"를 위해 **최소 1000자** 권장
- 헤더 형식: `## [Image N] {역할}` (h2 마크다운, `━━━` 구분선 사용 금지)
- 모든 AI 프롬프트는 펜스드 코드블록(` ``` `)으로 감싸기
- Mode B-3 (`[Watermark Config]` 포함) 권장
- 팔레트/비율 참고: `references/palettes.yaml`, `references/image-sizes.yaml`

### 8-5-2. 이미지 가이드 문서 구조

```markdown
# Image Guide

## Basic Information
- Topic: {topic}
- Created: {YYYY-MM-DD}
- Total images: {N}

## Color Palette
- Main: {hex}
- Accent: {hex}
- Background: {hex}
- Text: {hex}

---

## [Image 1] 썸네일
{Image 1 섹션 내용}

---

## [Image 2] {역할}
{Image 2 섹션 내용}

---

...
```

### 8-5-3. 썸네일 (Image 1) 생성 규칙

- **메인 텍스트**: 블로그 제목 (굵은 한글 폰트, 고대비)
- **서브 텍스트**: 부제목 또는 핵심 키워드 (선택 사항)
- **배경**: 주제에 맞는 그라데이션 또는 테마 비주얼
- 프롬프트에 반드시 포함: `"render exact Korean text characters as specified"`
- 비율: **1:1 (1024x1024)**

#### 썸네일 레이아웃 사양 (`thumbnail_layout.svg` 기준)

| 영역 | 치수 | 비율 (전체 대비) | 설명 |
|------|------|-----------------|------|
| 전체 캔버스 | 966×542 px | 100% | 1.78:1 (≈16:9) |
| 외곽 프레임 | 45px | 4.7% | 사방 여백 (파스텔 컬러 또는 테마 컬러) |
| 좌/우 이미지 확장 영역 | 167px 폭 | 17.3% | 배경 이미지가 확장되는 영역 |
| 중앙 콘텐츠 영역 | 542×452 px | 56.1%×83.4% | 핵심 시각 요소 배치 영역 |
| 텍스트 영역 | 502×210 px | 52%×38.7% | 하단 50%에 위치 |
| Main Text 행 | 502×120 px | - | 블로그 제목 (큰 폰트) |
| Sub Text 행 | 502×90 px | - | 부제목/키워드 (작은 폰트) |
| 워터마크 | 190×22 px | - | 하단 외곽 프레임 중앙 |

> 참고: `thumbnail_layout.svg` 파일에서 정확한 비례를 확인할 수 있습니다.

#### 썸네일 권장 폰트

| 우선순위 | 폰트명 | 용도 | 특징 |
|---------|--------|------|------|
| 1순위 | **G마켓 산스 Bold** | Main Text (제목) | 임팩트 있는 두꺼운 고딕, 무료 상업용 |
| 2순위 | **Pretendard Bold** | Main/Sub Text | 깔끔한 산세리프, 범용성 높음 |
| 3순위 | **어그로체 Bold (SB어그로)** | Main Text (강조형) | 강렬하고 힘 있는 서체, 시선 집중 |

- AI 프롬프트에 폰트 스타일 지시: `"bold Korean sans-serif font similar to Gmarket Sans Bold or SB Aggro Bold style"`
- font_family 지정: `"Gmarket Sans Bold, Pretendard Bold, SB Aggro Bold, sans-serif"`

### 8-5-4. 본문 이미지 (Image 2+) 생성 규칙

- 해당 문단의 내용에 충실한 텍스트/데이터를 이미지에 포함
- 비율: **1:1 (1024x1024)**

**콘텐츠 유형별 이미지 가이드:**

| 콘텐츠 유형 | 권장 이미지 | 예시 |
|---|---|---|
| 데이터/통계 | 막대/원형 차트 | 금리 비교 |
| 비교 | VS 레이아웃 | 상품 A vs B |
| 절차/단계 | 플로우 다이어그램 | 신청 절차 |
| 체크리스트 | 체크박스 레이아웃 | 필요 서류 |
| 감성/마무리 | 사진 스타일 | 희망/응원 테마 |

### 8-5-5. 이미지 섹션 정규 구조

각 이미지 섹션은 아래 구조를 따릅니다 (정규 형식):

```markdown
## [Image N] {역할}

🎨 AI Generation (With Text)

[Korean Description]
{이미지 설명 한국어 100-150자}

[AI Generation Prompt]
```
{영어 프롬프트 400-500자}
```

[Style Guide]
- Color: {HEX 색상 코드}
- Mood: {분위기 키워드}
- Format: {형식}
- Ratio: 1:1 (1024x1024)

[Watermark Config]
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 60
- watermark_font_size: 18
- watermark_font_color: "rgba(255,255,255,0.6)"
- watermark_font_family: "Pretendard, Nanum Gothic, sans-serif"
```

### 8-5-6. 썸네일 완전 예시

```markdown
## [Image 1] 썸네일

🎨 AI Generation (With Text)

[Korean Description]
블로그 글의 첫인상을 결정하는 썸네일 이미지.
주제를 시각적으로 표현하며, 메인 제목과 부제목을 포함한다.
독자의 관심을 끌 수 있는 전문적이고 현대적인 디자인.
이미지의 70-80% 영역에 텍스트가 배치되어 가독성을 극대화한다.

[AI Generation Prompt]
```
Blog thumbnail image, financial concept,
bold Korean sans-serif font (Gmarket Sans Bold / SB Aggro Bold style) text "{블로그 제목}",
text area positioned in bottom 50% of image occupying 52% width and 39% height,
main title in upper text row (22% of image height) with large impactful font,
subtitle "{부제목}" in lower text row (17% of image height) with clean readable font (Pretendard Bold style),
45px border frame around entire image in theme color,
left and right 17% areas for background image extension,
central 56% area as main content zone,
gradient background matching the topic theme,
eye-catching modern design with subtle depth and shadows,
high contrast readable text with slight glow or outline effect,
professional Korean financial blog style,
watermark "@money-lab-brian" at bottom center of frame,
1:1 ratio, 1024x1024 pixels,
render exact Korean text characters as specified
```

[Style Guide]
- Color: {Main HEX} + {Accent HEX} gradient
- Mood: Professional, trustworthy, modern, eye-catching
- Format: Modern thumbnail design (thumbnail_layout.svg 비례 기준)
- Ratio: 1:1 (1024x1024)
- Font: Gmarket Sans Bold, Pretendard Bold, SB Aggro Bold, sans-serif

[Watermark Config]
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 60
- watermark_font_size: 18
- watermark_font_color: "rgba(255,255,255,0.6)"
- watermark_font_family: "Pretendard, Nanum Gothic, sans-serif"
```

---

## 8-6. 태그 생성

```html
<p class="tags">#태그1 #태그2 #태그3 #태그4 #태그5 #태그6 #태그7 #태그8</p>
```

- 기본 태그 수: **8개** (`config.yaml` → `tags.count`)
- 최대: **10개** (`config.yaml` → `tags.max_count`)
- 해시태그 형식: `#` 접두사, 공백으로 구분
- 핵심 키워드 + 연관 키워드 조합
- 최종 `본문.html` 맨 아래에 배치
- `validator.py`에서 글자수 카운트 시 제외됨

---

## 8-7. 참조.md 생성 규칙

- STEP 3~4에서 사용한 출처를 "텍스트 근거"로 정리합니다.
- 항목별로 `제목 / URL / 한 줄 요약`을 포함합니다.
- 숫자/제도/기간처럼 사실 검증이 필요한 문장은 출처를 반드시 붙입니다.

> `writer.py` → `generate_references()`의 실제 출력을 정규 형식으로 채택한다.

### 참조.md 정규 구조

```markdown
# References

## Date
{YYYY-MM-DD}

## Topic
{topic}

---

## Text Sources

### {소스 카테고리명}
1. [{제목}]({URL})
   - Summary: {요약}

### {소스 카테고리명}
...

---

## Downloaded Images

Location: `./images/`

| # | Filename | Description | Source |
|---|--------|------|------|
| 1 | {filename} | {description} | [{source_name}]({source_url}) |

### Download Failed (URL only)

| # | Description | Image URL | Failure Reason |
|---|------|-----------|----------|
| 1 | {description} | {url}... | {error} |

---

## Notes
- Collection date: {YYYY-MM-DD}
- Text sources: {N}
- Downloaded images: {N}
- Failed downloads: {N}
```

**테이블 열 수:**
- Downloaded Images: **4열** (`#`, `Filename`, `Description`, `Source`)
- Download Failed: **4열** (`#`, `Description`, `Image URL`, `Failure Reason`)

---

## 8-8. 파일 저장 (Python)

```python
from scripts.writer import save_blog_files

files = save_blog_files(
    project_path=project_path,
    html_content=html_content,
    image_guide=image_guide_md,
    references=references_md,
    validate=True  # HTML 글자수 자동 검증
)
```

---

## 8-9. 최종 체크리스트

- [ ] `본문.html` 파일 존재
- [ ] `본문.html` 순수 글자수 1850~1950자 충족
- [ ] `본문.html`에 `[이미지 1 삽입 - 썸네일]` 포함
- [ ] `이미지 가이드.md` 파일 존재
- [ ] `이미지 가이드.md`에 `## [Image N]` 형식 헤더 사용
- [ ] 모든 AI 프롬프트가 코드블록(` ``` `)으로 감싸져 있음
- [ ] Image 1이 썸네일 역할 (70-80% 텍스트 영역)
- [ ] 각 섹션에 `[Watermark Config]` 6필드 포함
- [ ] 모든 이미지 비율이 1:1 (1024x1024)
- [ ] `참조.md` 파일 존재
- [ ] `참조.md`의 Downloaded Images 테이블이 4열 형식
- [ ] `원본.txt` 대비 본문 의미/분량 유지
- [ ] 문체 가이드 적용 확인 (종결어미 비율, 문장 길이, 도입/마무리 패턴)

---

## Next Step

파일 생성 완료 → **[STEP 9: 🖼️ Image Generation (MANDATORY)](step9-image.md)**
