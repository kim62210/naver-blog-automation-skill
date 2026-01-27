# STEP 7: 본문 작성 및 저장

선택된 옵션에 따라 본문을 작성하고 파일로 저장합니다.

## 진행 상태

```
[STEP 7/8] 본문 작성 ████████████████████████████░ 87%
```

---

## 7-1. 글자수 규칙 (중요!)

### 목표
- **본문.html 엄격 준수: 1850자 내외**
- **허용 범위: 1800~1900자 (±50자)**
- 공백 포함

### 카운트 제외 항목
- 모든 HTML 태그 (`<h2>`, `<p>`, `<table>`, `<blockquote>` 등)
- 이미지 placeholder (`[이미지 N 삽입]`)
- CSS 스타일 코드
- 해시태그 목록

### 카운트 포함 항목
- 본문 텍스트 (도입, 핵심 내용, 마무리)
- 표 안의 텍스트 내용
- CTA 문구
- 모든 실제 콘텐츠 텍스트

### Python 글자수 검증

```python
from scripts.validator import validate_char_count, print_validation_report

result = validate_char_count(html_content)
# result.is_valid: True/False
# result.char_count: 실제 글자수
# result.message: 상태 메시지
```

---

## 7-2. HTML 형식 가이드

본문.html은 **완전한 HTML 파일**로 작성됩니다.
브라우저에서 열고 전체 선택(Cmd+A) → 복사(Cmd+C) → 네이버 블로그에 붙여넣기(Cmd+V)하면 서식이 그대로 유지됩니다.

### HTML 태그 매핑

| 요소 | HTML 태그 |
|------|-----------|
| 대제목 | `<h2 style="font-size:24px;font-weight:bold;">` |
| 중제목 | `<h3 style="font-size:18px;font-weight:bold;">` |
| 소제목 | `<h4 style="font-size:15px;font-weight:bold;">` |
| 인용구 | `<blockquote style="border-left:4px solid #ccc;padding-left:16px;color:#666;">` |
| 강조인용 | `<blockquote style="background:#f0f7ff;padding:16px;border-radius:8px;">` |
| 글자-특대 | `<p style="font-size:24px;font-weight:bold;text-align:center;">` |
| 글자-소 | `<p style="font-size:12px;color:#888;">` |
| 구분선 | `<hr style="border:none;border-top:1px solid #ddd;margin:24px 0;">` |
| 이미지 위치 | `<p style="color:#999;text-align:center;">[이미지 N 삽입]</p>` |

---

## 7-3. 본문 작성

### 템플릿 사용

```python
from scripts.writer import generate_html_content

sections = [
    {"title": "도입", "content": "...", "has_image": False},
    {"title": "핵심 정보 1", "content": "...", "has_image": True},
    {"title": "핵심 정보 2", "content": "...", "has_image": True},
    # ...
]

html_content = generate_html_content(
    title="{제목}",
    sections=sections,
    tags=["태그1", "태그2", ...]
)
```

### 직접 작성 시 참고

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: 'Noto Sans KR', sans-serif; line-height: 1.8; max-width: 700px; margin: 0 auto; padding: 20px; }
    /* ... 스타일 생략 ... */
  </style>
</head>
<body>

<h1>{제목}</h1>

<div class="image-placeholder">[이미지 1 삽입 - 썸네일]</div>

<hr>

<h2>{소제목}</h2>

<blockquote>
"{인용 문구}"
</blockquote>

<p>{본문 내용}</p>

<!-- 이미지, 표, 추가 섹션... -->

<p class="tags">#태그1 #태그2 #태그3 ...</p>

</body>
</html>
```

---

## 7-4. 이미지 가이드 작성 (별도 파일)

**중요**: 본문.html에는 이미지 가이드를 포함하지 않습니다.
모든 이미지 가이드는 **이미지 가이드.md** 파일에 별도로 작성합니다.

### 이미지 가이드 모드

#### 📷 모드 A: 참고 이미지 사용
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[이미지 N] {이미지 역할 설명}

📷 다운로드된 이미지: ./images/{파일명}
📍 원본 출처: {URL}
💡 활용: {직접 사용 / 레이아웃 참고 / 색감 참고}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 🎨 모드 B: AI 이미지 생성 프롬프트
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[이미지 N] {이미지 역할 설명}

🎨 AI 생성

[한글 설명]
{이미지에 담길 내용을 한글로 상세 설명}

[AI 생성 프롬프트]
{영문 프롬프트 - 복사해서 바로 사용 가능}

[스타일 가이드]
- 색상: {주요 색상}
- 분위기: {분위기 키워드}
- 형식: {인포그래픽/일러스트/사진풍/플랫디자인}
- 비율: {16:9 / 1:1 / 4:3}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 🔷 모드 C: SVG 이미지 생성 가이드
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[이미지 N] {이미지 역할 설명}

🔷 SVG 생성

[이미지 설명]
{이미지에 담길 내용을 상세 설명}

[SVG 가이딩]
- 캔버스 크기: {width}x{height}
- 배경색: {hex 색상코드}
- 주요 요소:
  1. {요소1}: {위치}, {크기}, {색상}
  2. {요소2}: {위치}, {크기}, {색상}

[색상 팔레트]
- 메인: {hex}
- 포인트: {hex}
- 배경: {hex}

[저장 경로]
./images/{파일명}.svg
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7-5. 태그 생성

- 8~10개 자동 생성
- 핵심 키워드 + 관련 키워드
- # 기호로 시작

```
#육아휴직 #육아휴직급여 #2026육아휴직 #육아휴직신청 #출산휴가 #부모급여 #워킹맘 #워킹대디
```

---

## 7-6. 파일 저장

### 저장 경로
```
./경제 블로그/YYYY-MM-DD/주제명/
├── 본문.html
├── 이미지 가이드.md
├── 참조.md
└── images/
```

### Python으로 저장

```python
from scripts.writer import save_blog_files

files = save_blog_files(
    project_path=project_path,
    html_content=html_content,
    image_guide=image_guide_md,
    references=references_md,
    validate=True  # 글자수 자동 검증
)
```

---

## 7-7. 글자수 검증 및 조정

작성 완료 후 글자수를 검증합니다:

```python
from scripts.validator import print_validation_report

result = print_validation_report(html_content)

if not result.is_valid:
    # 초과/미달 시 조정 필요
    print(suggest_adjustment(result))
```

### 글자수 초과 시
- 중복되는 내용 제거
- 부연 설명 간소화
- 불필요한 수식어 삭제

### 글자수 미달 시
- 핵심 정보 섹션에 구체적인 예시 추가
- 실용 팁 섹션 확장
- 관련 통계나 데이터 보충

---

## 다음 단계

파일 저장 완료 → **[STEP 8: 수정 루프](step8-revise.md)**
