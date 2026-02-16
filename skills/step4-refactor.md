# STEP 4: Writing Refactoring (원본.txt -> HTML/MD)

STEP 3에서 저장한 `원본.txt`(일반 텍스트 + [괄호] 가이드)를 기반으로, 실제 블로그 업로드용 파일들을 생성합니다.

> 문체 가이드 참조: [네이버 블로그 문체 가이드](../네이버_블로그_문체_가이드.md)

## Progress Status

```
[STEP 4/6] Refactoring ████████████████████░░░░░░░ 70%
```

---

## 4-1. Inputs -> Outputs

### Input (Required)
- `{project_path}/원본.txt`

### Output (Generate in this step)
```
~/workspace/경제 블로그/YYYY-MM-DD/{topic-slug}/
├── 원본.txt               # [STEP 3] 순수 텍스트 원고 (STEP 4 이후 수정 금지)
├── 본문.html              # [STEP 4] 블로그 HTML (네이버 블로그 붙여넣기용)
├── 이미지 가이드.md       # [STEP 4] 이미지 생성 프롬프트 명세
├── 참조.md               # [STEP 4] 출처 및 참고자료
└── images/                # [STEP 5] 생성된 이미지
```

---

## 4-2. 원본.txt 정리 원칙 (Draft Cleanup)

- STEP 3에서 작성한 **본문 텍스트의 의미/분량은 유지**
- **스타일 결정(볼드/언더라인/이탤릭/폰트 크기 등)은 이 단계에서 확정**
- 최종 `본문.html`의 **순수 텍스트 글자수는 1850~1950자** 유지

---

## 4-3. Writing Refactoring (스타일/레이아웃 결정)

### (1) 강조 체계
- **Bold**: 결론/핵심 수치/행동 CTA 중심으로 제한적으로 사용
- **Underline**: "실행해야 하는 문장(신청 조건/방법/주의)"에만 사용
- **Italic**: 용어 정의/보조 설명에만 사용 (남용 금지)

### (2) 폰트 크기 체계 (Naver Blog 기준)
- 제목: 28px / 중제목: 24px / 소제목: 19px / 본문: 16px / 각주: 11px

> 기준값은 `config.yaml`의 `typography.blog_sizes`와 동일.

### (3) 가독성/리듬
- 문장 길이: **20~40자** (최대 50자)
- 문단: 1~3문장, 줄바꿈 적극 활용
- 문단 사이: `<br><br>` 또는 `<p>` 분리
- 리듬: short(15~25자) > long(35~45자) > short(15~25자)

---

## 4-4. 본문.html 생성 규칙

### HTML Structure

> 정확한 HTML 구조와 CSS는 `templates/blog-post.html` 템플릿 파일을 참조하세요.

### 태그 -> HTML 변환 규칙

| 원본.txt 태그 | HTML 변환 | 비고 |
|------|----------|------|
| `[중제목]` | `<h2>` 또는 24px bold 스타일 | |
| `[소제목]` | `<h3>` 또는 19px bold 스타일 | |
| `[인용]` | `<blockquote>` (배경/패딩 적용) | |
| 일반 문단 | `<p>` 단위 분리 + 문장 단위 `<br>` | |
| `[이미지 N 삽입 ...]` | `<div class="image-placeholder">` | 텍스트 그대로 유지 |

### 이미지 플레이스홀더 형식

```html
<!-- 썸네일 (항상 이미지 1) -->
<div class="image-placeholder">[이미지 1 삽입 - 썸네일]</div>

<!-- 본문 이미지 (이미지 2부터) -->
<div class="image-placeholder">[이미지 N 삽입]</div>
```

### 줄바꿈 규칙
1. 문장 끝: `<br>` 1개
2. 문단 사이: `<br><br>` 또는 `<p>` 분리

### 금지 패턴
- `<script>` 태그, 인라인 JavaScript, 외부 리소스 로딩 금지

### 글자수 검증

| 항목 | 값 | config.yaml 경로 |
|------|-----|-------------------|
| 타겟 글자수 | 1900자 | `writing.char_count` |
| 허용 오차 | +-50자 | `writing.char_tolerance` |

```python
from scripts.validator import validate_char_count, validate_draft_char_count

result = validate_char_count(html_content)
print(result.message)
```

---

## 4-5. 이미지 가이드.md 생성 규칙

### 공통 규칙

- `본문.html`의 **섹션 흐름/핵심 메시지**에 맞춰 이미지 역할을 정의
- 모든 이미지 비율: **1:1 (500x500)** 고정
- 모든 이미지에 `[Watermark Config]` 6필드 필수
- 이미지별 섹션 **최소 1000자** 권장
- 헤더 형식: `## [Image N] {역할}` (h2 마크다운)
- 모든 AI 프롬프트는 펜스드 코드블록으로 감싸기

### 이미지 가이드 문서 구조

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
```

### 썸네일 (Image 1) 규칙

- **메인 텍스트**: 블로그 제목 (굵은 한글 폰트, 고대비)
- **서브 텍스트**: 부제목 또는 핵심 키워드 (선택)
- **배경**: 주제에 맞는 그라데이션 또는 테마 비주얼
- 프롬프트에 반드시 포함: `"render exact Korean text characters as specified"`
- 비율: **1:1 (500x500)**

> 상세 썸네일 레이아웃: `thumbnail_layout.svg`, `references/thumbnail-templates.md` 참조

### 본문 이미지 (Image 2+) 규칙

| 콘텐츠 유형 | 권장 이미지 | 예시 |
|---|---|---|
| 데이터/통계 | 막대/원형 차트 | 금리 비교 |
| 비교 | VS 레이아웃 | 상품 A vs B |
| 절차/단계 | 플로우 다이어그램 | 신청 절차 |
| 체크리스트 | 체크박스 레이아웃 | 필요 서류 |
| 감성/마무리 | 사진 스타일 | 희망/응원 테마 |

### 이미지 섹션 정규 구조

```markdown
## [Image N] {역할}

🎨 AI Generation (With Text)

[Korean Description]
{이미지 설명 한국어 100-150자}

[AI Generation Prompt]
\```
{영어 프롬프트 400-500자}
\```

[Style Guide]
- Color: {HEX 색상 코드}
- Mood: {분위기 키워드}
- Format: {형식}
- Ratio: 1:1 (500x500)

[Watermark Config]
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 60
- watermark_font_size: 18
- watermark_font_color: "rgba(255,255,255,0.6)"
- watermark_font_family: "Pretendard, Nanum Gothic, sans-serif"
```

---

## 4-6. 태그 생성

```html
<p class="tags">#태그1 #태그2 #태그3 #태그4 #태그5 #태그6 #태그7 #태그8</p>
```

- 기본 태그 수: **8개** (`config.yaml` -> `tags.count`)
- 최대: **10개** (`config.yaml` -> `tags.max_count`)
- 핵심 키워드 + 연관 키워드 조합

---

## 4-7. 참조.md 생성

> `writer.py` -> `generate_references()`의 실제 출력을 정규 형식으로 채택.
> 상세 형식은 `templates/references.md` 템플릿 참조.

---

## 4-8. 파일 저장 (Python)

```python
from scripts.writer import save_blog_files

files = save_blog_files(
    project_path=project_path,
    html_content=html_content,
    image_guide=image_guide_md,
    references=references_md,
    validate=True
)
```

---

## 4-9. 최종 체크리스트

- [ ] `본문.html` 파일 존재
- [ ] `본문.html` 순수 글자수 1850~1950자 충족
- [ ] `본문.html`에 `[이미지 1 삽입 - 썸네일]` 포함
- [ ] `이미지 가이드.md` 파일 존재, `## [Image N]` 형식 헤더 사용
- [ ] 모든 AI 프롬프트가 코드블록으로 감싸져 있음
- [ ] 각 섹션에 `[Watermark Config]` 6필드 포함
- [ ] 모든 이미지 비율 1:1 (500x500)
- [ ] `참조.md` 파일 존재
- [ ] `원본.txt` 대비 본문 의미/분량 유지
- [ ] 문체 가이드 적용 확인

---

## Next Step

파일 생성 완료 -> **[STEP 5: Image Generation (MANDATORY)](step5-image.md)**
