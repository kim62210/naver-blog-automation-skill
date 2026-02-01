# 네이버 블로그 이미지 템플릿 가이드

> 네이버 블로그 인플루언서/피드메이커 스타일 기반 **10가지 실용 템플릿**
> 각 템플릿은 AI 이미지 생성 + 텍스트 오버레이 설정을 포함합니다.

---

## 목차

1. [프리미엄 금융](#template-1-프리미엄-금융) - 투자/재테크 고급 콘텐츠
2. [클린 미니멀](#template-2-클린-미니멀) - 정보 전달형 콘텐츠
3. [임팩트 그라데이션](#template-3-임팩트-그라데이션) - 시선 집중 필요시
4. [숫자 강조 빅넘버](#template-4-숫자-강조-빅넘버) - 수익/금액 강조
5. [인포그래픽 비교](#template-5-인포그래픽-비교) - 상품/서비스 비교
6. [단계별 가이드](#template-6-단계별-가이드) - How-to 콘텐츠
7. [경고/주의 알림](#template-7-경고주의-알림) - 리스크/주의사항
8. [트렌디 카드뉴스](#template-8-트렌디-카드뉴스) - SNS 공유용
9. [체크리스트](#template-9-체크리스트) - 팁/가이드 정리
10. [속보 헤드라인](#template-10-속보-헤드라인) - 뉴스/이슈 속보

---

## 공통 사항

### 권장 이미지 사이즈
- **썸네일**: 1300 x 885 px (네이버 블로그 대표이미지)
- **본문 이미지**: 886 x 500 px (모바일 최적화)
- **카드뉴스**: 1080 x 1080 px (정사각형)

### 권장 폰트
- **고딕 (가독성)**: Pretendard, 소스 한 산스, Noto Sans KR
- **감성/손글씨**: 나눔 손글씨 펜, 꽃길체
- **명조 (고급스러움)**: 디딤명조, 나눔명조

### 텍스트 규칙
- 제목: 12~14자 이내
- 핵심 단어 2색 이상으로 강조
- 질문형 헤드라인 효과적 ("~할까?", "~일까?")

---

## Template 1: 프리미엄 금융

### 개요
- **용도**: 투자, 재테크, 자산관리, 금융 상품 분석
- **분위기**: 신뢰감, 전문성, 고급스러움
- **권장 사이즈**: 1300 x 885 (썸네일) / 886 x 500 (본문)

### 색상 팔레트
| 역할 | HEX 코드 | 설명 |
|------|----------|------|
| **메인 (70%)** | `#1A2744` | 딥 네이비 - 신뢰와 안정감 |
| **서브 (25%)** | `#2C3E5A` | 미드 네이비 - 깊이감 |
| **포인트 (5%)** | `#D4AF37` | 골드 - 프리미엄 강조 |

### 🎨 AI Generation

**Korean Description:**
어두운 네이비 블루 배경에 고급스러운 금융 이미지. 주식 차트 그래프가 우상향하는 모습, 금색 조명이 은은하게 비치는 분위기. 미니멀하고 깔끔한 구성으로 텍스트 공간 확보. 블러 처리된 도시 야경이 배경에 희미하게 보임.

**AI Generation Prompt:**
```text
Dark navy blue financial background, elegant and premium atmosphere, subtle upward trending stock chart graph with golden glow, minimalist composition with ample text space, blurred city skyline at night in the far background, professional investment theme, soft golden ambient lighting, clean and sophisticated, 4K quality
```

**Negative Prompt:**
```text
logos, watermarks, people, faces, cluttered, busy, low quality
```

### [Text Overlay Config]

```json
{
  "main_text": "2025년 주식투자\n핵심 전략 3가지",
  "main_text_position": "center-left",
  "main_text_x": "8%",
  "main_text_y": "35%",
  "font_size": 58,
  "font_weight": "bold",
  "font_color": "#FFFFFF",
  "font_family": "Pretendard",
  "line_height": 1.3,
  "text_shadow": "2px 2px 8px rgba(0,0,0,0.7)",

  "sub_text": "월급쟁이도 할 수 있는 안전한 투자법",
  "sub_text_x": "8%",
  "sub_text_y": "58%",
  "sub_font_size": 24,
  "sub_font_color": "#B8C4D4",

  "accent_text": "PREMIUM",
  "accent_x": "8%",
  "accent_y": "25%",
  "accent_font_size": 14,
  "accent_font_color": "#D4AF37",
  "accent_letter_spacing": "3px",

  "watermark": "@채널명",
  "watermark_x": "92%",
  "watermark_y": "95%",
  "watermark_font_size": 12,
  "watermark_color": "rgba(255,255,255,0.5)"
}
```

### 사용 예시

| 콘텐츠 유형 | 메인 텍스트 예시 |
|-------------|------------------|
| 투자 전략 | "2025년 주식투자 핵심 전략 3가지" |
| 재테크 가이드 | "1억 모으기 현실적인 방법" |
| 금융 상품 분석 | "ISA vs 연금저축 뭐가 유리할까?" |
| 부동산 정보 | "전세 vs 월세 2025년 선택 기준" |

---

## Template 2: 클린 미니멀

### 개요
- **용도**: 정보 전달, 가이드, 설명형 콘텐츠, 일상 정보
- **분위기**: 깔끔함, 신선함, 접근성
- **권장 사이즈**: 1300 x 885 (썸네일) / 886 x 500 (본문)

### 색상 팔레트
| 역할 | HEX 코드 | 설명 |
|------|----------|------|
| **메인 (70%)** | `#FFFFFF` | 퓨어 화이트 - 깨끗함 |
| **서브 (25%)** | `#F5F7FA` | 라이트 그레이 - 구분감 |
| **포인트 (5%)** | `#2563EB` | 블루 - 신뢰 강조 |

### 🎨 AI Generation

**Korean Description:**
밝고 깔끔한 흰색 배경, 부드러운 그림자가 있는 미니멀한 오브젝트들, 파스텔 블루 악센트, 충분한 여백, 심플한 기하학적 형태가 은은하게 배치됨. 자연광이 비치는 듯한 밝고 청량한 느낌.

**AI Generation Prompt:**
```text
Clean white minimalist background, soft natural lighting, subtle geometric shapes in pastel blue, gentle shadows, ample negative space for text, light and airy atmosphere, simple abstract elements, professional and fresh aesthetic, high key lighting, 4K quality
```

**Negative Prompt:**
```text
logos, watermarks, dark, cluttered, busy, people, faces
```

### [Text Overlay Config]

```json
{
  "main_text": "초보자를 위한\n블로그 시작 가이드",
  "main_text_position": "center",
  "main_text_x": "50%",
  "main_text_y": "40%",
  "text_align": "center",
  "font_size": 52,
  "font_weight": "bold",
  "font_color": "#1F2937",
  "font_family": "Pretendard",
  "line_height": 1.4,

  "sub_text": "5분이면 충분해요",
  "sub_text_x": "50%",
  "sub_text_y": "60%",
  "sub_text_align": "center",
  "sub_font_size": 22,
  "sub_font_color": "#6B7280",

  "badge_text": "GUIDE",
  "badge_x": "50%",
  "badge_y": "25%",
  "badge_bg_color": "#2563EB",
  "badge_text_color": "#FFFFFF",
  "badge_padding": "8px 16px",
  "badge_border_radius": "20px",
  "badge_font_size": 12,

  "watermark": "@채널명",
  "watermark_x": "50%",
  "watermark_y": "92%",
  "watermark_font_size": 11,
  "watermark_color": "#9CA3AF"
}
```

### 사용 예시

| 콘텐츠 유형 | 메인 텍스트 예시 |
|-------------|------------------|
| 가이드 | "초보자를 위한 블로그 시작 가이드" |
| 설명 | "애드센스 승인받는 핵심 조건" |
| 일상 정보 | "직장인 점심시간 활용법 5가지" |
| 리뷰 | "맥북 에어 M3 한달 사용 후기" |

---

## Template 3: 임팩트 그라데이션

### 개요
- **용도**: 시선 집중이 필요한 콘텐츠, 중요 공지, 핫한 주제
- **분위기**: 강렬함, 트렌디함, 역동적
- **권장 사이즈**: 1300 x 885 (썸네일) / 886 x 500 (본문)

### 색상 팔레트
| 역할 | HEX 코드 | 설명 |
|------|----------|------|
| **그라데이션 시작** | `#1A1A2E` | 딥 퍼플 블랙 |
| **그라데이션 중간** | `#16213E` | 다크 블루 |
| **그라데이션 끝** | `#0F3460` | 미드나잇 블루 |
| **포인트** | `#E94560` | 핫 핑크/레드 |

### 🎨 AI Generation

**Korean Description:**
어두운 보라-파랑 그라데이션 배경, 우주적이고 신비로운 분위기, 미세한 빛 입자들이 흩어져 있음, 네온 핑크/마젠타 색상의 은은한 광선 효과, 깊이감 있는 레이어 구성, 중앙에 텍스트 공간 확보.

**AI Generation Prompt:**
```text
Dark purple to blue gradient background, cosmic mysterious atmosphere, scattered light particles, subtle neon pink magenta light rays, deep layered composition, abstract flowing shapes, cinematic lighting, futuristic aesthetic, ample center space for text, dramatic mood, 4K quality
```

**Negative Prompt:**
```text
logos, watermarks, people, faces, bright, overexposed
```

### [Text Overlay Config]

```json
{
  "main_text": "지금 당장 확인해야 할\n2025 트렌드 리포트",
  "main_text_position": "center",
  "main_text_x": "50%",
  "main_text_y": "45%",
  "text_align": "center",
  "font_size": 56,
  "font_weight": "800",
  "font_color": "#FFFFFF",
  "font_family": "Pretendard",
  "line_height": 1.3,
  "text_shadow": "0 0 30px rgba(233,69,96,0.5)",

  "highlight_word": "2025 트렌드",
  "highlight_color": "#E94560",

  "sub_text": "놓치면 후회할 핵심 인사이트",
  "sub_text_x": "50%",
  "sub_text_y": "65%",
  "sub_text_align": "center",
  "sub_font_size": 20,
  "sub_font_color": "rgba(255,255,255,0.8)",

  "watermark": "@채널명",
  "watermark_x": "50%",
  "watermark_y": "93%",
  "watermark_font_size": 11,
  "watermark_color": "rgba(255,255,255,0.4)"
}
```

### 사용 예시

| 콘텐츠 유형 | 메인 텍스트 예시 |
|-------------|------------------|
| 트렌드 | "지금 당장 확인해야 할 2025 트렌드" |
| 핫이슈 | "이 정책 모르면 손해봅니다" |
| 강조 | "반드시 알아야 할 세금 상식" |
| 공지 | "구독자 10만 기념 이벤트 오픈" |

---

## Template 4: 숫자 강조 빅넘버

### 개요
- **용도**: 수익, 금액, 통계, 성과 강조
- **분위기**: 임팩트, 성공, 결과 중심
- **권장 사이즈**: 1300 x 885 (썸네일) / 886 x 500 (본문)

### 색상 팔레트
| 역할 | HEX 코드 | 설명 |
|------|----------|------|
| **메인 (70%)** | `#0D0D0D` | 블랙 - 고급스러움 |
| **서브 (25%)** | `#1A1A1A` | 다크 그레이 |
| **포인트 A** | `#FF3B30` | 레드 - 숫자 강조 |
| **포인트 B** | `#FFD700` | 골드 - 금액 강조 |

### 🎨 AI Generation

**Korean Description:**
검은색 배경에 금색과 빨간색의 추상적인 빛 효과, 성공과 부를 상징하는 고급스러운 분위기, 미니멀한 구성으로 중앙에 큰 숫자를 배치할 공간 확보, 살짝 빛나는 입자들이 떠다니는 효과.

**AI Generation Prompt:**
```text
Pure black background with abstract golden and red light effects, luxury wealth success atmosphere, subtle floating particles with golden glow, minimalist composition with large center space for big numbers, premium elegant aesthetic, ambient light rays, cinematic contrast, 4K quality
```

**Negative Prompt:**
```text
logos, watermarks, people, faces, busy, cluttered
```

### [Text Overlay Config]

```json
{
  "big_number": "1억",
  "big_number_x": "50%",
  "big_number_y": "40%",
  "big_number_font_size": 120,
  "big_number_font_weight": "900",
  "big_number_color": "#FFD700",
  "big_number_font_family": "Pretendard",
  "big_number_shadow": "0 0 40px rgba(255,215,0,0.6)",

  "main_text": "월급쟁이가\n3년만에 모은 비결",
  "main_text_x": "50%",
  "main_text_y": "65%",
  "text_align": "center",
  "font_size": 36,
  "font_weight": "bold",
  "font_color": "#FFFFFF",
  "line_height": 1.4,

  "sub_text": "현실적인 재테크 로드맵 공개",
  "sub_text_x": "50%",
  "sub_text_y": "82%",
  "sub_font_size": 18,
  "sub_font_color": "rgba(255,255,255,0.6)",

  "watermark": "@채널명",
  "watermark_x": "92%",
  "watermark_y": "95%",
  "watermark_font_size": 11,
  "watermark_color": "rgba(255,255,255,0.3)"
}
```

### 사용 예시

| 콘텐츠 유형 | 빅넘버 | 메인 텍스트 예시 |
|-------------|--------|------------------|
| 수익 | "1억" | "월급쟁이가 3년만에 모은 비결" |
| 수익률 | "127%" | "올해 내 계좌 수익률 공개" |
| 통계 | "5000만" | "구독자가 선택한 최고의 앱" |
| 비교 | "3배" | "작년 대비 수익이 3배가 된 이유" |

---

## Template 5: 인포그래픽 비교

### 개요
- **용도**: 상품 비교, 서비스 분석, 장단점 정리, VS 콘텐츠
- **분위기**: 객관성, 정보 중심, 분석적
- **권장 사이즈**: 1300 x 885 (썸네일) / 886 x 500 (본문)

### 색상 팔레트
| 역할 | HEX 코드 | 설명 |
|------|----------|------|
| **메인 (70%)** | `#F8FAFC` | 오프 화이트 |
| **서브 (25%)** | `#E2E8F0` | 라이트 그레이 |
| **옵션 A** | `#3B82F6` | 블루 - 왼쪽 옵션 |
| **옵션 B** | `#10B981` | 그린 - 오른쪽 옵션 |
| **구분선** | `#CBD5E1` | 미디움 그레이 |

### 🎨 AI Generation

**Korean Description:**
밝은 회색-흰색 배경, 좌우로 나뉜 듯한 레이아웃 암시, 파란색과 초록색의 추상적 도형이 양쪽에 배치, 깔끔하고 정돈된 인포그래픽 스타일, 중앙에 VS 배치 공간 확보.

**AI Generation Prompt:**
```text
Clean light gray white background, split layout design, abstract geometric shapes in blue on left side and green on right side, infographic style, organized symmetrical composition, subtle grid pattern, professional comparison theme, center space for VS element, modern corporate aesthetic, 4K quality
```

**Negative Prompt:**
```text
logos, watermarks, people, faces, dark, cluttered
```

### [Text Overlay Config]

```json
{
  "left_option": "적금",
  "left_option_x": "25%",
  "left_option_y": "45%",
  "left_font_size": 48,
  "left_font_weight": "bold",
  "left_font_color": "#3B82F6",

  "vs_text": "VS",
  "vs_x": "50%",
  "vs_y": "45%",
  "vs_font_size": 36,
  "vs_font_weight": "900",
  "vs_font_color": "#64748B",
  "vs_bg_color": "#FFFFFF",
  "vs_border_radius": "50%",
  "vs_padding": "15px",
  "vs_shadow": "0 4px 12px rgba(0,0,0,0.1)",

  "right_option": "ETF",
  "right_option_x": "75%",
  "right_option_y": "45%",
  "right_font_size": 48,
  "right_font_weight": "bold",
  "right_font_color": "#10B981",

  "main_text": "2025년 재테크 뭐가 유리할까?",
  "main_text_x": "50%",
  "main_text_y": "75%",
  "text_align": "center",
  "font_size": 28,
  "font_weight": "600",
  "font_color": "#1E293B",

  "watermark": "@채널명",
  "watermark_x": "50%",
  "watermark_y": "92%",
  "watermark_font_size": 11,
  "watermark_color": "#94A3B8"
}
```

### 사용 예시

| 콘텐츠 유형 | 왼쪽 vs 오른쪽 | 메인 텍스트 예시 |
|-------------|----------------|------------------|
| 금융 비교 | "적금 vs ETF" | "2025년 재테크 뭐가 유리할까?" |
| 기기 비교 | "아이폰 vs 갤럭시" | "실사용자가 말하는 진짜 차이" |
| 서비스 비교 | "네이버 vs 카카오" | "블로그 플랫폼 장단점 분석" |
| 방법 비교 | "국내주식 vs 해외주식" | "초보자에게 더 맞는 선택은?" |

---

## Template 6: 단계별 가이드

### 개요
- **용도**: How-to 콘텐츠, 튜토리얼, 프로세스 설명
- **분위기**: 체계적, 교육적, 따라하기 쉬운
- **권장 사이즈**: 1300 x 885 (썸네일) / 886 x 500 (본문)

### 색상 팔레트
| 역할 | HEX 코드 | 설명 |
|------|----------|------|
| **메인 (70%)** | `#EFF6FF` | 라이트 블루 |
| **서브 (25%)** | `#DBEAFE` | 소프트 블루 |
| **포인트** | `#2563EB` | 블루 - 단계 표시 |
| **강조** | `#1D4ED8` | 딥 블루 |

### 🎨 AI Generation

**Korean Description:**
밝은 파란색 계열 배경, 단계를 암시하는 계단 또는 화살표 형태의 추상적 도형, 위에서 아래로 또는 왼쪽에서 오른쪽으로 흐르는 듯한 구성, 교육적이고 친근한 분위기, 숫자를 배치할 수 있는 공간 확보.

**AI Generation Prompt:**
```text
Light blue gradient background, abstract step-by-step visual elements, flowing arrows or staircase shapes suggesting progression, educational friendly atmosphere, clean organized layout, circular numbered step indicators in deep blue, left to right or top to bottom flow, ample space for step numbers, modern tutorial aesthetic, 4K quality
```

**Negative Prompt:**
```text
logos, watermarks, people, faces, dark, cluttered, complex
```

### [Text Overlay Config]

```json
{
  "step_indicator": "STEP BY STEP",
  "step_indicator_x": "50%",
  "step_indicator_y": "18%",
  "step_indicator_font_size": 14,
  "step_indicator_color": "#2563EB",
  "step_indicator_letter_spacing": "4px",

  "main_text": "블로그 수익화\n완벽 가이드",
  "main_text_x": "50%",
  "main_text_y": "42%",
  "text_align": "center",
  "font_size": 52,
  "font_weight": "bold",
  "font_color": "#1E3A8A",
  "font_family": "Pretendard",
  "line_height": 1.3,

  "step_count": "5단계",
  "step_count_x": "50%",
  "step_count_y": "62%",
  "step_count_font_size": 24,
  "step_count_color": "#FFFFFF",
  "step_count_bg": "#2563EB",
  "step_count_padding": "10px 24px",
  "step_count_border_radius": "25px",

  "sub_text": "처음부터 끝까지 따라만 하세요",
  "sub_text_x": "50%",
  "sub_text_y": "78%",
  "sub_font_size": 18,
  "sub_font_color": "#64748B",

  "watermark": "@채널명",
  "watermark_x": "50%",
  "watermark_y": "92%",
  "watermark_font_size": 11,
  "watermark_color": "#94A3B8"
}
```

### 사용 예시

| 콘텐츠 유형 | 단계 수 | 메인 텍스트 예시 |
|-------------|---------|------------------|
| 수익화 | "5단계" | "블로그 수익화 완벽 가이드" |
| 시작 가이드 | "3단계" | "주식 계좌 개설 초간단 방법" |
| 튜토리얼 | "7단계" | "ChatGPT 활용법 A to Z" |
| 프로세스 | "4단계" | "세금 환급 신청 절차" |

---

## Template 7: 경고/주의 알림

### 개요
- **용도**: 리스크 경고, 주의사항, 피해야 할 것들, 실수 방지
- **분위기**: 긴급함, 경각심, 중요성 강조
- **권장 사이즈**: 1300 x 885 (썸네일) / 886 x 500 (본문)

### 색상 팔레트
| 역할 | HEX 코드 | 설명 |
|------|----------|------|
| **메인 (70%)** | `#1C1917` | 다크 브라운 블랙 |
| **서브 (25%)** | `#292524` | 차콜 |
| **경고** | `#EF4444` | 레드 - 위험 강조 |
| **주의** | `#F59E0B` | 앰버 - 주의 표시 |

### 🎨 AI Generation

**Korean Description:**
어두운 배경에 경고를 암시하는 빨간색과 노란색 추상적 요소, 경고 삼각형이나 느낌표를 암시하는 형태, 긴장감 있는 분위기, 텍스트를 위한 중앙 공간 확보, 그라데이션 테두리 효과.

**AI Generation Prompt:**
```text
Dark dramatic background with red and amber warning elements, abstract caution shapes suggesting alert triangles or exclamation marks, tense urgent atmosphere, subtle danger gradient from dark to red edges, spotlight effect on center for text space, dramatic lighting, cinematic warning mood, 4K quality
```

**Negative Prompt:**
```text
logos, watermarks, people, faces, bright, cheerful, happy
```

### [Text Overlay Config]

```json
{
  "warning_badge": "⚠️ 주의",
  "warning_badge_x": "50%",
  "warning_badge_y": "20%",
  "warning_badge_font_size": 16,
  "warning_badge_color": "#FBBF24",
  "warning_badge_bg": "rgba(245,158,11,0.2)",
  "warning_badge_padding": "8px 20px",
  "warning_badge_border": "1px solid #F59E0B",
  "warning_badge_border_radius": "5px",

  "main_text": "이것만은 절대\n하지 마세요",
  "main_text_x": "50%",
  "main_text_y": "45%",
  "text_align": "center",
  "font_size": 54,
  "font_weight": "800",
  "font_color": "#FFFFFF",
  "font_family": "Pretendard",
  "line_height": 1.3,

  "highlight_word": "절대",
  "highlight_color": "#EF4444",

  "sub_text": "초보 투자자가 흔히 저지르는 치명적 실수",
  "sub_text_x": "50%",
  "sub_text_y": "68%",
  "sub_font_size": 20,
  "sub_font_color": "rgba(255,255,255,0.7)",

  "watermark": "@채널명",
  "watermark_x": "50%",
  "watermark_y": "93%",
  "watermark_font_size": 11,
  "watermark_color": "rgba(255,255,255,0.3)"
}
```

### 사용 예시

| 콘텐츠 유형 | 메인 텍스트 예시 |
|-------------|------------------|
| 실수 방지 | "이것만은 절대 하지 마세요" |
| 리스크 경고 | "투자 전 반드시 확인할 3가지" |
| 사기 주의 | "이런 문자 오면 100% 스미싱" |
| 함정 경고 | "청약 신청 전 꼭 알아야 할 것" |

---

## Template 8: 트렌디 카드뉴스

### 개요
- **용도**: SNS 공유용, 바이럴 콘텐츠, 젊은 층 타겟
- **분위기**: 트렌디, 감각적, 에너지틱
- **권장 사이즈**: 1080 x 1080 (정사각형) / 1300 x 885 (썸네일)

### 색상 팔레트
| 역할 | HEX 코드 | 설명 |
|------|----------|------|
| **메인 (60%)** | `#FDF4FF` | 소프트 핑크 화이트 |
| **서브 (30%)** | `#FAE8FF` | 라이트 퍼플 핑크 |
| **그라데이션 A** | `#C084FC` | 퍼플 |
| **그라데이션 B** | `#F472B6` | 핑크 |
| **그라데이션 C** | `#60A5FA` | 스카이 블루 |

### 🎨 AI Generation

**Korean Description:**
부드러운 파스텔 톤의 퍼플-핑크-블루 그라데이션 배경, 글래스모피즘 효과(유리 느낌), 둥근 모서리의 추상적 도형들이 떠다니는 듯한 구성, 밝고 경쾌한 분위기, 네온 글로우 효과.

**AI Generation Prompt:**
```text
Soft pastel gradient background blending purple pink and sky blue, glassmorphism effect with frosted glass elements, floating rounded abstract shapes, bright cheerful trendy atmosphere, subtle neon glow accents, Gen Z aesthetic, holographic iridescent hints, bubbly playful composition, Instagram card news style, 4K quality
```

**Negative Prompt:**
```text
logos, watermarks, people, faces, dark, serious, corporate
```

### [Text Overlay Config]

```json
{
  "category_badge": "TREND",
  "category_badge_x": "50%",
  "category_badge_y": "18%",
  "category_badge_font_size": 12,
  "category_badge_color": "#A855F7",
  "category_badge_bg": "rgba(168,85,247,0.15)",
  "category_badge_padding": "6px 16px",
  "category_badge_border_radius": "15px",

  "main_text": "MZ세대가\n열광하는 앱 TOP5",
  "main_text_x": "50%",
  "main_text_y": "45%",
  "text_align": "center",
  "font_size": 46,
  "font_weight": "800",
  "font_color": "#581C87",
  "font_family": "Pretendard",
  "line_height": 1.35,

  "highlight_gradient": "linear-gradient(90deg, #C084FC, #F472B6)",
  "highlight_word": "TOP5",

  "sub_text": "다운로드 1위 앱은 바로...",
  "sub_text_x": "50%",
  "sub_text_y": "68%",
  "sub_font_size": 18,
  "sub_font_color": "#7C3AED",

  "emoji_decoration": "✨",
  "emoji_positions": ["15%, 25%", "85%, 75%"],

  "watermark": "@채널명",
  "watermark_x": "50%",
  "watermark_y": "92%",
  "watermark_font_size": 11,
  "watermark_color": "#A78BFA"
}
```

### 사용 예시

| 콘텐츠 유형 | 메인 텍스트 예시 |
|-------------|------------------|
| 트렌드 | "MZ세대가 열광하는 앱 TOP5" |
| 추천 | "요즘 핫한 넷플릭스 신작 3선" |
| 라이프 | "자취생 필수 가성비 아이템" |
| 리뷰 | "SNS에서 난리난 신상 카페" |

---

## Template 9: 체크리스트

### 개요
- **용도**: 팁 모음, 체크할 항목, 정리된 정보 제공
- **분위기**: 정돈됨, 실용적, 도움이 되는
- **권장 사이즈**: 1300 x 885 (썸네일) / 886 x 500 (본문)

### 색상 팔레트
| 역할 | HEX 코드 | 설명 |
|------|----------|------|
| **메인 (70%)** | `#F0FDF4` | 민트 화이트 |
| **서브 (25%)** | `#DCFCE7` | 라이트 그린 |
| **포인트** | `#22C55E` | 그린 - 체크 표시 |
| **강조** | `#16A34A` | 딥 그린 |

### 🎨 AI Generation

**Korean Description:**
밝은 민트-그린 계열 배경, 체크 표시나 목록을 암시하는 추상적 도형들, 깔끔하게 정렬된 수평선 요소, 자연스럽고 신선한 느낌, 잎사귀나 성장을 암시하는 미니멀한 요소.

**AI Generation Prompt:**
```text
Light mint green background, abstract checkmark and list elements, clean horizontal aligned shapes, fresh natural atmosphere, subtle leaf or growth motifs, organized grid pattern hints, minimal botanical elements, productivity wellness aesthetic, ample space for checklist overlay, clean organized design, 4K quality
```

**Negative Prompt:**
```text
logos, watermarks, people, faces, dark, cluttered, complex
```

### [Text Overlay Config]

```json
{
  "list_badge": "✓ CHECKLIST",
  "list_badge_x": "50%",
  "list_badge_y": "18%",
  "list_badge_font_size": 13,
  "list_badge_color": "#16A34A",
  "list_badge_letter_spacing": "3px",

  "main_text": "출근 전 10분\n모닝루틴 체크리스트",
  "main_text_x": "50%",
  "main_text_y": "42%",
  "text_align": "center",
  "font_size": 48,
  "font_weight": "bold",
  "font_color": "#166534",
  "font_family": "Pretendard",
  "line_height": 1.35,

  "item_count": "7가지",
  "item_count_x": "50%",
  "item_count_y": "62%",
  "item_count_font_size": 22,
  "item_count_color": "#FFFFFF",
  "item_count_bg": "#22C55E",
  "item_count_padding": "8px 20px",
  "item_count_border_radius": "20px",

  "sub_text": "이것만 지키면 하루가 달라져요",
  "sub_text_x": "50%",
  "sub_text_y": "78%",
  "sub_font_size": 17,
  "sub_font_color": "#4B5563",

  "watermark": "@채널명",
  "watermark_x": "50%",
  "watermark_y": "92%",
  "watermark_font_size": 11,
  "watermark_color": "#86EFAC"
}
```

### 사용 예시

| 콘텐츠 유형 | 항목 수 | 메인 텍스트 예시 |
|-------------|---------|------------------|
| 루틴 | "7가지" | "출근 전 10분 모닝루틴 체크리스트" |
| 필수 확인 | "5가지" | "해외여행 전 필수 체크리스트" |
| 정리 | "10가지" | "세금 신고 전 준비물 총정리" |
| 팁 | "8가지" | "면접 전날 꼭 확인할 것들" |

---

## Template 10: 속보 헤드라인

### 개요
- **용도**: 뉴스, 이슈 속보, 긴급 정보, 시사 콘텐츠
- **분위기**: 긴급함, 뉴스 느낌, 신속한 정보 전달
- **권장 사이즈**: 1300 x 885 (썸네일) / 886 x 500 (본문)

### 색상 팔레트
| 역할 | HEX 코드 | 설명 |
|------|----------|------|
| **메인 (70%)** | `#0F0F0F` | 블랙 |
| **서브 (25%)** | `#1A1A1A` | 다크 그레이 |
| **속보** | `#DC2626` | 레드 - 속보 표시 |
| **강조** | `#FFFFFF` | 화이트 - 가독성 |

### 🎨 AI Generation

**Korean Description:**
검은색 배경에 뉴스 스튜디오를 연상시키는 분위기, 빨간색 악센트 라인, 디지털 그래픽 요소, 긴급 뉴스 느낌의 동적인 조명, 하단에 뉴스 티커 공간을 암시하는 레이아웃.

**AI Generation Prompt:**
```text
Dark black news broadcast style background, red accent lines and geometric shapes, digital news graphics aesthetic, dynamic urgent lighting, news studio atmosphere, subtle screen glare effects, breaking news layout with ticker space at bottom, professional broadcast quality, cinematic news mood, 4K quality
```

**Negative Prompt:**
```text
logos, watermarks, people, faces, bright, cheerful, casual
```

### [Text Overlay Config]

```json
{
  "breaking_badge": "속보",
  "breaking_badge_x": "8%",
  "breaking_badge_y": "20%",
  "breaking_badge_font_size": 14,
  "breaking_badge_color": "#FFFFFF",
  "breaking_badge_bg": "#DC2626",
  "breaking_badge_padding": "6px 16px",
  "breaking_badge_font_weight": "bold",
  "breaking_badge_animation": "pulse",

  "main_text": "기준금리 또 인하\n부동산 시장 영향은?",
  "main_text_x": "8%",
  "main_text_y": "40%",
  "text_align": "left",
  "font_size": 52,
  "font_weight": "800",
  "font_color": "#FFFFFF",
  "font_family": "Pretendard",
  "line_height": 1.3,

  "highlight_word": "기준금리",
  "highlight_color": "#FCA5A5",

  "ticker_bar": true,
  "ticker_y": "90%",
  "ticker_bg": "#DC2626",
  "ticker_height": "40px",
  "ticker_text": "2025.01.31 | 경제 뉴스 | @채널명",
  "ticker_text_color": "#FFFFFF",
  "ticker_font_size": 14,

  "date_stamp": "2025.01.31",
  "date_stamp_x": "92%",
  "date_stamp_y": "20%",
  "date_stamp_font_size": 12,
  "date_stamp_color": "rgba(255,255,255,0.6)"
}
```

### 사용 예시

| 콘텐츠 유형 | 메인 텍스트 예시 |
|-------------|------------------|
| 경제 속보 | "기준금리 또 인하, 부동산 시장 영향은?" |
| 정책 뉴스 | "2025 연말정산 달라지는 점 총정리" |
| 시장 이슈 | "삼성전자 급등, 무슨 일이?" |
| 긴급 정보 | "오늘부터 시행! 새로운 청약 제도" |

---

## 부록: 템플릿 선택 가이드

### 콘텐츠 목적별 추천

| 목적 | 1순위 템플릿 | 2순위 템플릿 |
|------|--------------|--------------|
| 전문성 강조 | 프리미엄 금융 | 클린 미니멀 |
| 시선 끌기 | 임팩트 그라데이션 | 숫자 강조 빅넘버 |
| 정보 정리 | 체크리스트 | 단계별 가이드 |
| 비교 분석 | 인포그래픽 비교 | 클린 미니멀 |
| 경고/주의 | 경고 주의 알림 | 속보 헤드라인 |
| SNS 공유 | 트렌디 카드뉴스 | 임팩트 그라데이션 |
| 뉴스/속보 | 속보 헤드라인 | 경고 주의 알림 |

### 타겟 연령별 추천

| 연령대 | 추천 템플릿 |
|--------|-------------|
| 20대 | 트렌디 카드뉴스, 임팩트 그라데이션 |
| 30대 | 클린 미니멀, 단계별 가이드, 체크리스트 |
| 40대+ | 프리미엄 금융, 숫자 강조 빅넘버, 속보 헤드라인 |

---

## 도구 활용 팁

### AI 이미지 생성 도구
- **Midjourney**: 고품질, 예술적 표현에 강함
- **DALL-E 3**: 프롬프트 이해도 높음, 텍스트 친화적
- **Stable Diffusion**: 무료, 커스터마이징 가능

### 텍스트 오버레이 도구
- **Canva**: 템플릿 기반, 초보자 친화적
- **미리캔버스**: 한국어 특화, 무료 폰트 다양
- **Figma**: 정교한 디자인, 협업 용이
- **Photoshop**: 전문가용, 세밀한 조정 가능

### 폰트 다운로드
- [눈누 (noonnu.cc)](https://noonnu.cc) - 무료 한글 폰트 모음
- [Google Fonts](https://fonts.google.com) - Noto Sans KR 등
- [Pretendard](https://cactus.tistory.com/306) - 무료 상업용 고딕

---

*이 가이드는 네이버 블로그 인플루언서/피드메이커 스타일을 분석하여 작성되었습니다.*
*최종 업데이트: 2025.01.31*
