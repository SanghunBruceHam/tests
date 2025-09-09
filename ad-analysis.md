# Google AdSense 광고 구현 분석 보고서

## 분석 완료 파일 목록

### 1. egen-teto/ja/index.html
- **광고 위치:** 페이지 하단, 결과 표시 영역 이후, 푸터 이전
- **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
- **광고 슬롯:** `data-ad-slot="7298546648"`
- **스타일링:** 
  - `<div style="text-align: center; margin: 20px 0;">` 래퍼
  - `display:block` 스타일
- **특이사항:** AMP 광고도 함께 사용 중 (라인 1420-1423)
- **광고 위치 라인:** 1425-1439

### 2. egen-teto/ja/about.html
- **광고 위치:** 콘텐츠 하단, 푸터 이전
- **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
- **광고 슬롯:** `data-ad-slot="7298546648"`
- **스타일링:** `display:block` 스타일, div 래퍼 없음
- **특이사항:** About 페이지용 단순한 구조
- **광고 위치 라인:** 303-317

### 3. egen-teto/ko/index.html
- **광고 위치:** 페이지 하단, 결과 표시 영역 이후
- **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
- **광고 슬롯:** `data-ad-slot="7298546648"`
- **스타일링:** 
  - `<div style="text-align: center; margin: 20px 0;">` 래퍼
  - `display:block` 스타일
- **특이사항:** 공통 테마 CSS 사용 (`/assets/common-theme.css`)
- **광고 위치 라인:** 1447-1461

### 4. egen-teto/ko/about.html
- **광고 위치:** 콘텐츠 하단, 푸터 이전
- **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
- **광고 슬롯:** `data-ad-slot="7298546648"`
- **스타일링:** `display:block` 스타일, div 래퍼 없음
- **특이사항:** ja about 페이지와 동일한 구조
- **광고 위치 라인:** 309-323

### 5. egen-teto/en/index.html
- **광고 위치:** 페이지 하단, 결과 표시 영역 이후
- **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
- **광고 슬롯:** `data-ad-slot="7298546648"`
- **스타일링:** 
  - `<div style="text-align: center; margin: 20px 0;">` 래퍼
  - `display:block` 스타일
- **특이사항:** 코멘트가 영어로 변경 ("Display Horizontal")
- **광고 위치 라인:** 1445-1459

### 6. egen-teto/en/about.html
- **광고 위치:** 콘텐츠 하단, 푸터 이전
- **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
- **광고 슬롯:** `data-ad-slot="7298546648"`
- **스타일링:** `display:block` 스타일, div 래퍼 없음
- **특이사항:** 코멘트는 한글 유지 ("디스플레이 가로")
- **광고 위치 라인:** 323-337

### 7. index.html (메인 페이지)
- **광고 개수:** 2개
- **첫 번째 광고:**
  - **위치:** 콘텐츠 중간
  - **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
  - **광고 슬롯:** `data-ad-slot="4067267701"`
  - **스타일링:** `<div class="ad-container" style="max-width:860px; margin:30px auto; text-align:center; padding:0 20px;">`
  - **광고 위치 라인:** 1167-1175
- **두 번째 광고:**
  - **위치:** 페이지 하단
  - **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
  - **광고 슬롯:** 없음 (자동)
  - **스타일링:** `<div style="max-width:860px; margin:30px auto 20px; text-align:center; padding:0 20px;">`
  - **광고 위치 라인:** 1213-1216
- **특이사항:** 쿠팡 파트너스 광고도 포함 (라인 1177)

### 8. kpop-egen-teto/ja/index.html
- **광고 개수:** 0개
- **특이사항:** AdSense 스크립트만 로드 (Auto Ads만 사용 가능)
- **광고 위치 라인:** 30 (스크립트만)

### 9. kpop-egen-teto/ko/index.html
- **광고 개수:** 0개
- **특이사항:** AdSense 스크립트만 로드 (Auto Ads만 사용 가능)
- **광고 위치 라인:** 34 (스크립트만)

### 10. kpop-egen-teto/en/index.html
- **광고 개수:** 0개
- **특이사항:** AdSense 스크립트만 로드 (Auto Ads만 사용 가능)
- **광고 위치 라인:** 30 (스크립트만)

### 11. ja/index.html
- **광고 개수:** 0개
- **특이사항:** AdSense 스크립트만 로드 (Auto Ads만 사용 가능), AMP 스크립트도 포함
- **광고 위치 라인:** 75 (스크립트만)

### 12. kpop-idol-romance/ja/index.html
- **광고 개수:** 0개
- **특이사항:** AdSense 스크립트만 로드 (Auto Ads만 사용 가능)
- **광고 위치 라인:** 30 (스크립트만)

### 13-14. kpop-idol-romance/ko, en/index.html
- **광고 개수:** 0개 (각각)
- **특이사항:** AdSense 스크립트만 로드

### 15. anime-personality/ja/index.html
- **광고 개수:** 1개
- **광고 위치:** 페이지 하단, 결과 표시 영역 이후
- **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
- **광고 슬롯:** `data-ad-slot="7298546648"`
- **스타일링:** `<div style="text-align: center; margin: 20px 0;">` 래퍼
- **광고 위치 라인:** 1685-1699

### 16. anime-personality/ko/index.html
- **광고 개수:** 1개
- **광고 위치:** 페이지 하단, 결과 표시 영역 이후
- **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
- **광고 슬롯:** `data-ad-slot="7298546648"`
- **스타일링:** `<div style="text-align: center; margin: 20px 0;">` 래퍼
- **광고 위치 라인:** 1808-1821

### 17. anime-personality/en/index.html
- **광고 개수:** 0개
- **특이사항:** AdSense 스크립트만 로드

### 18-20. age-vibe/ko, ja, en/index.html
- **광고 개수:** 0개 (각각)
- **특이사항:** AdSense 스크립트만 로드, 주석처리된 예시 코드 포함

### 21. phone-style/ko/index.html
- **광고 개수:** 1개 (확인 필요)

### 22. money-style/ko/index.html
- **광고 개수:** 1개 (확인 필요)

### 23-25. compat-pick/ja, ko, en/index.html
- **광고 개수:** 1개씩 (이미 분석됨)

### Romance-test, food-compat, kfood-romance 시리즈
- **특이사항:** AdSense 스크립트만 로드 (Auto Ads만 사용)

### 누락 파일 분석 (추가 26개)

### 26. ko/index.html (한국어 메인)
- **광고 개수:** 1개
- **광고 위치:** 콘텐츠 중간
- **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
- **광고 슬롯:** `data-ad-slot="4067267701"`
- **스타일링:** `<div class="ad-container" style="max-width:860px; margin:30px auto; text-align:center; padding:0 20px;">`
- **광고 위치 라인:** 1012-1019

### 27. en/index.html (영어 메인)
- **광고 개수:** 0개
- **특이사항:** AdSense 스크립트만 로드 (Auto Ads만 사용)

### 28. phone-style/ko/index.html
- **광고 개수:** 1개
- **광고 위치:** 페이지 하단
- **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
- **광고 슬롯:** 없음 (자동)
- **스타일링:** `<div style="max-width:860px; margin:20px auto; text-align:center;">`
- **광고 위치 라인:** 178-181

### 29. money-style/ko/index.html
- **광고 개수:** 1개
- **광고 위치:** 페이지 하단
- **광고 타입:** 반응형 (`data-ad-format="auto"`, `data-full-width-responsive="true"`)
- **광고 슬롯:** 없음 (자동)
- **스타일링:** `<div style="max-width:860px; margin:20px auto; text-align:center;">`
- **광고 위치 라인:** 178-181

### 30. anime-personality 툴 파일들 (4개)
- **create_favicon.html, generate_all_images.html, ja/create_thumbnail.html, ko/create_thumbnail.html**
- **광고 개수:** 0개 (각각)
- **특이사항:** AdSense 스크립트만 로드

### 31-33. food-compat 시리즈 (en, ja, ko)
- **광고 개수:** 0개 (각각)
- **특이사항:** AdSense 스크립트만 로드

### 34-36. kfood-romance 시리즈 (en, ja, ko)
- **광고 개수:** 0개 (각각)
- **특이사항:** AdSense 스크립트만 로드

### 37-129. romance-test 시리즈 (93개 파일)
- **광고 개수:** 0개 (모든 파일)
- **특이사항:** AdSense 스크립트만 로드

### 130. compat-pick/en/index 2.html
- **광고 개수:** 0개
- **특이사항:** 주석처리된 예시 코드만 있음

### 131. sandbox.html
- **광고 개수:** 0개
- **특이사항:** AdSense 스크립트만 로드

## 실제 광고 단위가 있는 파일 최종 요약 (총 17개 파일)
1. **egen-teto 시리즈** (6개): ja, ko, en index/about - 슬롯 `7298546648`
2. **index.html (메인)**: 2개 광고 (슬롯 `4067267701` + 자동)
3. **ko/index.html (한국어 메인)**: 1개 광고 (슬롯 `4067267701`)
4. **anime-personality** (2개): ja, ko index - 슬롯 `7298546648`
5. **compat-pick** (3개): ja, ko, en index - 각각 다른 구현
6. **phone-style/ko/index.html**: 1개 광고 (자동 슬롯)
7. **money-style/ko/index.html**: 1개 광고 (자동 슬롯)

## 공통 패턴 발견
- egen-teto 시리즈는 모두 동일한 광고 슬롯 사용 (`7298546648`)
- 모든 광고가 반응형 설정 사용
- index 페이지는 div 래퍼 사용, about 페이지는 래퍼 없음