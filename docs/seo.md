# SEO 가이드

## 정적 + 동적 보강 전략

- 정적 메타 태그: 각 HTML에 Title/Description/OG/Twitter/Canonical 명시
- 동적 보강: `assets/seo-optimizer.js`로 다음을 자동화
  - viewport/robots/caching/security 등 공통 메타 보강
  - Open Graph/Twitter Card 누락값 보완(이미지 후보 자동 탐색 포함)
  - JSON-LD(WebApplication/Quiz/FAQ/Breadcrumb) 추가
  - hreflang 대체 링크 생성(ko/ja/en/x-default)
  - 브레드크럼 렌더링 및 구조화 데이터 삽입
  - 제목 구조(H1 1개 원칙 등) 정리 및 빈 제목 경고

## 페이지 구조 예시

- 메인: `index.html`
  - 다국어 hreflang, JSON-LD(Website/Breadcrumb/FAQ/Organization), GA/AdSense, AMP Ad, 폰트/프리커넥트
  - 테스트 목록은 `update_index.py`로 자동 유지

## 점검/개선 워크플로우

1) 점검
```
python seo_audit_simple.py
python seo_audit_fixed.py
python seo_audit_advanced.py
```
2) 누락 항목 확인
```
python find_missing_tags.py
python find_title_issues.py
```
3) 자동 보정(선택)
```
python seo_fixer.py
```
4) 사이트맵 재생성 및 제출
```
python sitemap_generator.py
python submit_sitemap.py
```

## 권장 기준(요약)

- Title: 30–60자
- Meta description: 120–160자
- OG/Twitter: 핵심 5개 태그 모두 채우기(제목/설명/이미지/URL/타입)
- JSON-LD: Website/Organization + 필요시 Quiz/FAQ/Breadcrumb
- 이미지: 의미있는 alt, lazy 로딩, width/height 지정

