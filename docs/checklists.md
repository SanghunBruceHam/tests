# 체크리스트

## 릴리즈 체크리스트

- [ ] `python update_index.py` 실행, 테스트 카드/카운트 갱신 확인
- [ ] `python sitemap_generator.py` 실행, URL 수/우선순위 확인
- [ ] `python seo_audit_fixed.py` 실행, 주요 경고(Description/OG/Twitter/JSON-LD/Canonical) 해소
- [ ] 크리티컬 페이지 수동 QA(메인, 언어 인덱스, 상위 테스트)
- [ ] (선택) `python performance_monitor.py`로 LCP/CLS/FID 점검
- [ ] `python submit_sitemap.py` 제출

## 접근성 QA

- [ ] 키보드 탭 순서 확인 및 포커스 표시
- [ ] 이미지 `alt` 적절성/빈값 확인
- [ ] 대비(텍스트/배경) 문제 없음
- [ ] H1 단일성, 제목 레벨 다운그레이드 없음

## SEO 기본

- [ ] Title 30–60자, Description 120–160자
- [ ] OG/Twitter 필수 5개 태그 보유
- [ ] JSON-LD Website/Organization + 필요 시 Quiz/FAQ/Breadcrumb
- [ ] Canonical, hreflang(ko/ja/en/x-default)

## 성능

- [ ] 이미지 lazy, width/height 설정
- [ ] 모듈 지연 로딩, 불필요 스크립트 제거
- [ ] preconnect/dns-prefetch 적용

