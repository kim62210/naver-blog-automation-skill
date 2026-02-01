# STEP 8: Writing Refactoring (원본.txt → HTML/MD 생성)

STEP 7에서 저장한 `원본.txt`(일반 텍스트 + [괄호] 가이드)를 기반으로, 실제 블로그 업로드용 파일들을 생성합니다.

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
./경제 블로그/YYYY-MM-DD/topic-name/
├── 원본.txt
├── 본문.html
├── 이미지 가이드.md
└── 참조.md
```

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
- 문장 길이: 50~60자 이내
- 문단 길이: 200자 내외
- 문단 사이: 빈 줄(또는 `<br><br>`)로 호흡 확보

---

## 8-4. 본문.html 생성 규칙 (원본.txt → HTML)

### 폰트 크기 / 태그 매핑 (고정)

| 용도 | 권장 태그 | 크기 |
|------|----------|------|
| 제목 | `<h1>` | 28px |
| 중제목 | `<h2>` | 24px |
| 소제목 | `<h3>` | 19px |
| 본문 | `<p>` | 16px |
| 각주/출처 | `<span class="small">` | 11px |

### 최소 변환 규칙
- `[중제목]` → `<h2>` 또는 24px bold 스타일
- `[소제목]` → `<h3>` 또는 19px bold 스타일
- `[인용]` → `<blockquote>` (배경/패딩 적용)
- 일반 문단 → `<p>` 단위로 분리 + 문장 단위 `<br>` 적용
- `[이미지 N 삽입 ...]` → 그대로 HTML에 “이미지 플레이스홀더”로 유지

### 줄바꿈 규칙 (가독성)
1. 문장 끝: `<br>` 1개
2. 문단 사이: `<br><br>` 또는 `<p>` 분리로 빈 줄 1개 확보

> 최종 HTML에서 글자수는 “태그를 제외한 순수 텍스트”만 카운트됩니다.

### 글자수 검증 (HTML 기준)
```python
from scripts.validator import validate_char_count

result = validate_char_count(html_content)
print(result.message)
```

---

## 8-5. 이미지 가이드.md 생성 규칙

- `본문.html`의 **섹션 흐름/핵심 메시지**에 맞춰 이미지 역할을 정의합니다.
- 이미지별 섹션은 “충분히 구체적인 프롬프트”를 위해 **최소 1000자**를 권장합니다.
- 썸네일(이미지 1)은 **정확한 한글 텍스트 렌더링 지시**를 반드시 포함합니다.
- 워터마크 6개 필드는 누락하지 않습니다.
- 팔레트/비율 참고:
  - `references/palettes.yaml`
  - `references/image-sizes.yaml`

### 워터마크 6개 필드 (누락 금지)
- watermark_text
- watermark_position
- watermark_margin_bottom
- watermark_font_size
- watermark_font_color
- watermark_font_family

### 이미지 섹션 예시 (요약)

> 아래는 “구조” 예시입니다. 실제 `이미지 가이드.md`에서는 `[AI Generation Prompt]` 구간을 코드블록( ``` )으로 감싸세요.

## [Image 1] 썸네일

[Korean Description]
...

[AI Generation Prompt]
Blog thumbnail, bold Korean text "..." ...
IMPORTANT: Render the exact Korean text characters as specified above.

[Watermark Config]
- watermark_text: "@money-lab-brian"
- watermark_position: "bottom-center"
- watermark_margin_bottom: 60
- watermark_font_size: 18
- watermark_font_color: "rgba(255,255,255,0.6)"
- watermark_font_family: "Pretendard, Nanum Gothic, sans-serif"

---

## 8-6. 태그 생성

- 8~10개 추천
- 핵심 키워드 + 연관 키워드
- 최종 `본문.html` 맨 아래에 `#` 형태로 배치

---

## 8-7. 참조.md 생성 규칙

- STEP 3~4에서 사용한 출처를 “텍스트 근거”로 정리합니다.
- 항목별로 `제목 / URL / 한 줄 요약`을 포함합니다.
- 숫자/제도/기간처럼 사실 검증이 필요한 문장은 출처를 반드시 붙입니다.

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

- [ ] `원본.txt` 대비 본문 의미/분량이 유지되었는가
- [ ] `본문.html` 순수 글자수 1850~1950자 충족
- [ ] `이미지 가이드.md`에 이미지 N개가 존재하고, 썸네일 텍스트 렌더링 지시가 포함되었는가
- [ ] `참조.md`에 핵심 근거가 빠짐없이 정리되었는가

---

## Next Step

파일 생성 완료 → **[STEP 9: 🖼️ Image Generation (MANDATORY)](step9-image.md)**
