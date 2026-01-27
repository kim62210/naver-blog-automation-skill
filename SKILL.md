---
name: search-blogging
description: |
  네이버 경제 숏텐츠에서 트렌딩 주제를 수집하고, 블로그 글 작성까지 자동화하는 스킬.
  1단계에서 오늘의 인기 경제 뉴스 10개를 Chrome DevTools로 수집하여 사용자가 선택하고,
  이후 병렬 웹 검색으로 자료를 수집하여 1850자 내외 블로그 글을 작성한다.

  사용 시점:
  (1) 블로그 글 작성이 필요할 때
  (2) 오늘의 트렌딩 경제 주제로 글 작성이 필요할 때
  (3) /search-blogging 명령어 입력 시

  트리거 키워드: 블로그 글 작성, 블로그 글 써줘, 자료 조사 후 글 작성, 경제 블로그
---

# search-blogging 스킬 v2.0

네이버 경제 숏텐츠에서 트렌딩 주제 수집부터 블로그 글 작성까지의 전체 워크플로우를 자동화합니다.

## 빠른 시작

```bash
# 트렌딩 주제에서 선택
/search-blogging

# 직접 주제 지정
/search-blogging 육아휴직 급여
```

---

## 출력물

| 파일 | 설명 | 용도 |
|------|------|------|
| 본문.html | 네이버 블로그용 HTML | 브라우저에서 열어 복사 → 블로그에 붙여넣기 |
| 이미지 가이드.md | AI 프롬프트 + SVG 가이딩 | 이미지 생성 참고 |
| 참조.md | 출처 목록 | 자료 확인용 |
| images/ | 참고 이미지 + 생성된 SVG | 블로그 이미지 삽입 |

### 저장 경로

```
./경제 블로그/YYYY-MM-DD/주제명/
├── 본문.html
├── 이미지 가이드.md
├── 참조.md
└── images/
```

---

## 워크플로우 (8단계)

| 단계 | 설명 | 상세 가이드 |
|------|------|------------|
| **STEP 1** | 트렌딩 주제 수집 및 선택 | [skills/step1-collect.md](skills/step1-collect.md) |
| **STEP 2** | 주제 확정 및 키워드 확장 | [skills/step2-confirm.md](skills/step2-confirm.md) |
| **STEP 3** | 병렬 자료 수집 (6개 에이전트) | [skills/step3-research.md](skills/step3-research.md) |
| **STEP 4** | 수집 결과 요약 및 확인 | [skills/step4-review.md](skills/step4-review.md) |
| **STEP 5** | 글 작성 옵션 선택 | [skills/step5-options.md](skills/step5-options.md) |
| **STEP 6** | 제목 선택 | [skills/step6-title.md](skills/step6-title.md) |
| **STEP 7** | 본문 작성 및 저장 | [skills/step7-write.md](skills/step7-write.md) |
| **STEP 8** | 수정 루프 | [skills/step8-revise.md](skills/step8-revise.md) |

### 진행 상태 표시

```
[STEP 1/8] 주제 수집 ████░░░░░░░░░░░░░░░░░░░░░░░░ 12%
[STEP 2/8] 주제 확정 ████████░░░░░░░░░░░░░░░░░░░░ 25%
[STEP 3/8] 자료 수집 ████████████░░░░░░░░░░░░░░░░ 37%
[STEP 4/8] 결과 확인 ████████████████░░░░░░░░░░░░ 50%
[STEP 5/8] 옵션 선택 ████████████████████░░░░░░░░ 62%
[STEP 6/8] 제목 선택 ████████████████████████░░░░ 75%
[STEP 7/8] 본문 작성 ████████████████████████████░ 87%
[STEP 8/8] 검토/수정 ████████████████████████████ 100%
```

---

## 글 작성 규칙

### 글자수 (중요!)
- **목표: 1850자 내외**
- **허용 범위: 1800~1900자 (±50자)**
- 순수 본문 텍스트만 카운트 (HTML 태그, 이미지 placeholder 제외)

### 글자수 검증 (Python)

```python
from scripts.validator import validate_char_count

result = validate_char_count(html_content)
print(f"글자수: {result.char_count}자")
print(result.message)  # ✅ 적합 / ⚠️ 초과 / ⚠️ 미달
```

---

## 옵션

### 톤앤매너

| 옵션 | 설명 | 적합 주제 |
|------|------|----------|
| 전문적 | 객관적이고 신뢰감 있는 어조 | 금융, 건강, 법률 |
| 친근한 | 대화하듯 편안한 어조 | 육아, 리뷰, 일상 |
| 중립적 | 정보 전달 중심 균형 잡힌 어조 | 비교, 가이드, 뉴스 |

### 글 구성

| 옵션 | 구조 | 용도 |
|------|------|------|
| 7단계 | 도입→문제→핵심1,2,3→팁→마무리 | 정보성 글 |
| 5단계 | 도입→핵심→상세→팁→마무리 | 간결한 전달 |
| 자유 | AI 유연 구성 | 스토리텔링, Q&A |

### 이미지

| 옵션 | 수량 | 구성 |
|------|------|------|
| 최소 | 3개 | 썸네일 + 핵심 2개 |
| 권장 | 5개 | 썸네일 + 섹션별 1개 |
| 풍부 | 7개+ | 모든 섹션에 이미지 |

---

## 설정 파일

글로벌 설정은 `config.yaml`에서 관리합니다:

```yaml
# config.yaml
writing:
  char_count: 1850
  char_tolerance: 50

images:
  default_count: 5

tags:
  count: 8

output:
  base_dir: "./경제 블로그"
```

---

## Python 스크립트

| 스크립트 | 기능 |
|----------|------|
| `scripts/config.py` | 설정 파일 로드 |
| `scripts/utils.py` | 공통 유틸리티 |
| `scripts/validator.py` | 글자수 검증 |
| `scripts/setup.py` | 프로젝트 디렉토리 초기화 |
| `scripts/collector.py` | 이미지 수집 |
| `scripts/writer.py` | HTML/MD 생성 |

### 사용 예시

```python
# 프로젝트 초기화
from scripts.setup import create_project_structure
project_path = create_project_structure("육아휴직 가이드")

# 이미지 수집
from scripts.collector import collect_images
result = collect_images(images, project_path)

# 파일 저장
from scripts.writer import save_blog_files
files = save_blog_files(project_path, html, image_guide, references)
```

---

## 참조 파일

스킬 실행 중 필요 시 아래 파일을 참조합니다:

| 파일 | 용도 | 참조 시점 |
|------|------|----------|
| `references/tone-guide.md` | 톤앤매너 상세 가이드 | STEP 5-1 |
| `references/structure-templates.md` | 글 구성 템플릿 | STEP 5-2 |
| `references/image-guide.md` | 이미지 가이드 작성법 | STEP 5-3, STEP 7 |

---

## 템플릿 파일

| 파일 | 용도 |
|------|------|
| `templates/blog-post.html` | HTML 본문 템플릿 |
| `templates/image-guide.md` | 이미지 가이드 템플릿 |
| `templates/references.md` | 참조 문서 템플릿 |

---

## 디렉토리 구조

```
naver-blog-automation/
├── SKILL.md                    # 이 파일 (진입점)
├── config.yaml                 # 전역 설정
├── skills/                     # 모듈화된 스킬 (8개)
│   ├── step1-collect.md       # 트렌딩 주제 수집
│   ├── step2-confirm.md       # 주제 확정
│   ├── step3-research.md      # 자료 수집 (병렬)
│   ├── step4-review.md        # 결과 확인
│   ├── step5-options.md       # 옵션 선택
│   ├── step6-title.md         # 제목 선택
│   ├── step7-write.md         # 본문 작성
│   └── step8-revise.md        # 수정 루프
├── references/                 # 참조 자료
│   ├── tone-guide.md
│   ├── structure-templates.md
│   └── image-guide.md
├── templates/                  # 출력 템플릿
│   ├── blog-post.html
│   ├── image-guide.md
│   └── references.md
└── scripts/                    # Python 자동화
    ├── __init__.py
    ├── config.py
    ├── utils.py
    ├── validator.py
    ├── setup.py
    ├── collector.py
    └── writer.py
```

---

## 본문.html 사용법

1. **본문.html 파일을 브라우저에서 열기** (더블클릭)
2. **Cmd+A** (전체 선택)
3. **Cmd+C** (복사)
4. **네이버 블로그 에디터에서 Cmd+V** (붙여넣기)
5. 이미지 placeholder 위치에 실제 이미지 삽입

> 표, 글자 크기, 볼드, 인용구 등 모든 서식이 그대로 유지됩니다.

---

## 버전 정보

- **v2.0.0** (2026-01-27)
  - 스킬 모듈화 (8개 step 파일로 분리)
  - Python 자동화 스크립트 추가
  - YAML 설정 파일 도입
  - 템플릿 시스템 구축
