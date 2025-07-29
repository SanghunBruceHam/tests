# 🧠 심리테스트 플랫폼

다국어 지원 심리테스트 웹 플랫폼으로, 성격 분석, 연애 궁합, 직업 적성 등 다양한 테스트를 제공합니다.

## ✨ 주요 기능

- 🌐 **다국어 지원**: 한국어, 일본어, 영어
- 📱 **반응형 디자인**: 모바일, 태블릿, 데스크톱 최적화
- 🎯 **접근성**: WCAG 2.1 AA 준수
- 🚀 **성능 최적화**: Core Web Vitals 최적화
- 📊 **분석**: 향상된 사용자 분석 및 성능 모니터링
- 🔒 **보안**: XSS 방지, 입력 검증, 안전한 데이터 처리

## 🏗️ 기술 스택

### Frontend
- **HTML5**: 시맨틱 마크업, 접근성 최적화
- **CSS3**: 반응형 디자인, 애니메이션
- **JavaScript ES6+**: 모듈화, 성능 최적화
- **Web APIs**: Intersection Observer, Performance API, Web Storage

### Backend & Automation
- **Python 3.12+**: 자동화 스크립트, 콘텐츠 관리
- **BeautifulSoup4**: HTML 파싱
- **Google APIs**: Analytics, Search Console 연동

### SEO & Analytics
- **Google Analytics 4**: 사용자 분석
- **Google Search Console**: 검색 최적화
- **Structured Data**: JSON-LD 스키마
- **Open Graph**: 소셜 미디어 최적화

## 📂 프로젝트 구조

```
tests/
├── assets/                     # JavaScript 라이브러리
│   ├── accessibility.js        # 접근성 향상
│   ├── analytics-enhanced.js   # 고급 분석
│   ├── chart-visualization.js  # 차트 시각화
│   ├── common-components.js    # 공통 컴포넌트
│   ├── enhanced-features.js    # 향상된 기능
│   ├── result-analysis.js      # 결과 분석
│   └── seo-optimizer.js        # SEO 최적화
├── romance-test/               # 연애 테스트
│   ├── ko/, ja/, en/           # 다국어 버전
├── egen-teto/                  # 에겐테토 테스트
│   ├── ko/, ja/, en/           # 다국어 버전
├── config.py                   # 설정 관리
├── utils.py                    # 공통 유틸리티
├── apply_coupang_ads.py        # 광고 자동화
├── update_index.py             # 인덱스 업데이트
├── sitemap_generator.py        # 사이트맵 생성
└── index.html                  # 메인 페이지
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# Python 환경 설정
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집
GOOGLE_ANALYTICS_ID=your_ga_id
ADSENSE_CLIENT_ID=your_adsense_id
COUPANG_PARTNER_ID=your_coupang_id
COUPANG_TRACKING_CODE=your_tracking_code
```

### 3. 사이트 빌드 및 배포

```bash
# 사이트맵 생성
python sitemap_generator.py

# 테스트 인덱스 업데이트
python update_index.py

# 광고 적용 (선택사항)
python apply_coupang_ads.py
```

## 🔧 개발 가이드

### 새로운 테스트 추가

1. **디렉토리 구조 생성**:
   ```
   new-test/
   ├── ko/index.html
   ├── ja/index.html
   └── en/index.html
   ```

2. **HTML 템플릿 구조**:
   ```html
   <!DOCTYPE html>
   <html lang="ko">
   <head>
     <!-- 메타 태그, SEO 설정 -->
   </head>
   <body>
     <main id="main-content">
       <!-- 테스트 콘텐츠 -->
     </main>
     
     <!-- JavaScript 라이브러리 -->
     <script src="/assets/accessibility.js"></script>
     <script src="/assets/analytics-enhanced.js"></script>
     <script src="/assets/seo-optimizer.js"></script>
   </body>
   </html>
   ```

3. **자동 업데이트**:
   ```bash
   python update_index.py  # 인덱스에 자동 추가
   python sitemap_generator.py  # 사이트맵 업데이트
   ```

### 접근성 가이드라인

- **키보드 네비게이션**: 모든 상호작용 요소가 키보드로 접근 가능
- **ARIA 라벨**: 스크린 리더를 위한 적절한 라벨 제공
- **색상 대비**: WCAG AA 기준 준수 (4.5:1 이상)
- **포커스 관리**: 명확한 포커스 표시
- **다국어 지원**: `lang` 속성 적절히 사용

### 성능 최적화

- **이미지**: WebP 형식 사용, lazy loading 적용
- **JavaScript**: 모듈 분할, 비동기 로딩
- **CSS**: Critical CSS 인라인, 비중요 CSS 지연 로딩
- **캐싱**: 적절한 HTTP 캐시 헤더 설정

## 📊 모니터링 및 분석

### Core Web Vitals 추적
- **LCP** (Largest Contentful Paint): 2.5초 이하 목표
- **FID** (First Input Delay): 100ms 이하 목표
- **CLS** (Cumulative Layout Shift): 0.1 이하 목표

### 커스텀 이벤트 추적
```javascript
// 테스트 완료 추적
window.track('test_completed', {
  test_type: 'romance',
  completion_time: 120000,
  result_type: 'compatible'
});

// 사용자 상호작용 추적
window.track('feature_used', {
  feature_name: 'social_share',
  platform: 'twitter'
});
```

## 🔒 보안 가이드

### 입력 검증
- HTML 콘텐츠 새니타이징
- XSS 방지
- 파일 경로 검증

### 데이터 보호
- 사용자 식별 정보 최소화
- localStorage 적절한 사용
- 쿠키 보안 설정

## 🌐 SEO 최적화

### 구조화된 데이터
```json
{
  "@context": "https://schema.org",
  "@type": "Quiz",
  "name": "연애 심리 테스트",
  "description": "당신의 연애 성향을 알아보는 심리테스트",
  "educationalLevel": "beginner"
}
```

### 다국어 SEO
- `hreflang` 태그 적절한 사용
- 언어별 sitemap 생성
- 지역화된 메타 태그

## 📈 성능 벤치마크

| 메트릭 | 목표 | 현재 |
|--------|------|------|
| Lighthouse Score | 90+ | 95+ |
| Page Load Time | <3s | <2s |
| First Contentful Paint | <1.5s | <1.2s |
| Time to Interactive | <3s | <2.5s |

## 🤝 기여 가이드

1. **이슈 생성**: 기능 요청이나 버그 리포트
2. **포크 및 브랜치**: `feature/feature-name` 형식
3. **코드 작성**: 가이드라인 준수
4. **테스트**: 접근성 및 성능 테스트
5. **풀 리퀘스트**: 상세한 설명과 함께

## 📝 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일 참조

## 📞 지원

- 🐛 **버그 리포트**: [GitHub Issues](https://github.com/username/tests/issues)
- 💡 **기능 요청**: [GitHub Discussions](https://github.com/username/tests/discussions)
- 📧 **연락처**: support@example.com

---

<div align="center">
  <strong>🧠 더 나은 자기 이해를 위한 심리테스트 플랫폼</strong>
</div>