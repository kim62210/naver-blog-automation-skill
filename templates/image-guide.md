# 이미지 가이드

## 기본 정보
- 주제: ${topic}
- 작성일: ${date}
- 총 이미지 수: ${image_count}개

## 색상 팔레트
- 메인: ${color_main} (${color_main_name})
- 포인트: ${color_accent} (${color_accent_name})
- 배경: ${color_background}
- 텍스트: ${color_text}

---

## [이미지 1] 썸네일

### 🎨 AI 생성 프롬프트

**한글 설명:**
${thumbnail_description_kr}

**AI 생성 프롬프트:**
```
${thumbnail_prompt_en}
```

**스타일:**
- 색상: ${thumbnail_colors}
- 분위기: ${thumbnail_mood}
- 형식: ${thumbnail_format}
- 비율: 16:9

### 🔷 SVG 생성 가이드

**캔버스:** 1200x630px (OG 이미지 최적 크기)
**배경:** ${color_main} 또는 그라데이션

**요소:**
1. 메인 텍스트: "${title}" - 중앙 배치, 흰색, 48px bold
2. 서브 텍스트: "${subtitle}" - 메인 아래, 연한 색상, 24px
3. 아이콘/그래픽: 주제 관련 심볼 - 좌측 또는 우측 배치
4. 브랜드 요소: 로고 또는 워터마크 - 하단 코너

**저장 경로:** ./images/01_썸네일.svg

---

## [이미지 2] ${image2_role}

### 📷 참고 이미지 (다운로드된 경우)

**파일:** ${image2_filename}
**출처:** ${image2_source_url}
**활용:** ${image2_usage}

### 🎨 AI 생성 프롬프트

**한글 설명:**
${image2_description_kr}

**AI 생성 프롬프트:**
```
${image2_prompt_en}
```

**스타일:**
- 색상: ${image2_colors}
- 분위기: ${image2_mood}
- 형식: ${image2_format}

### 🔷 SVG 생성 가이드

**캔버스:** 800x450px
**배경:** #ffffff

**요소:**
${image2_svg_elements}

**저장 경로:** ./images/02_${image2_filename_base}.svg

---

## [이미지 3] ${image3_role}

### 🎨 AI 생성 프롬프트

**한글 설명:**
${image3_description_kr}

**AI 생성 프롬프트:**
```
${image3_prompt_en}
```

**스타일:**
- 색상: ${image3_colors}
- 분위기: ${image3_mood}
- 형식: ${image3_format}

### 🔷 SVG 생성 가이드

**캔버스:** 800x450px
**배경:** ${color_background}

**요소:**
${image3_svg_elements}

**저장 경로:** ./images/03_${image3_filename_base}.svg

---

## [이미지 4] ${image4_role}

### 🎨 AI 생성 프롬프트

**한글 설명:**
${image4_description_kr}

**AI 생성 프롬프트:**
```
${image4_prompt_en}
```

### 🔷 SVG 생성 가이드

**캔버스:** 800x450px
**배경:** ${color_background}

**요소:**
${image4_svg_elements}

**저장 경로:** ./images/04_${image4_filename_base}.svg

---

## [이미지 5] ${image5_role}

### 🎨 AI 생성 프롬프트

**한글 설명:**
${image5_description_kr}

**AI 생성 프롬프트:**
```
${image5_prompt_en}
```

**저장 경로:** ./images/05_${image5_filename_base}.svg

---

## 이미지 생성 가이드

### AI 이미지 생성 서비스
- **Midjourney**: 고품질 아트워크, `/imagine` 명령어 사용
- **DALL-E 3**: OpenAI ChatGPT에서 사용 가능
- **Canva AI**: Text to Image 기능
- **Leonardo AI**: 무료 플랜 제공

### SVG 생성 (Claude + svg-canvas-mcp)
1. svg_create로 캔버스 생성
2. draw_* 도구로 요소 추가
3. draw_text로 텍스트 추가
4. svg_save로 저장

### 이미지 최적화
- 블로그 업로드 권장 크기: 800px 너비
- 파일 형식: JPG (사진), PNG (투명 배경), SVG (벡터)
- 파일 크기: 1MB 이하 권장
