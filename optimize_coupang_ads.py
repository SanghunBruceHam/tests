#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from utils import FileManager, ContentProcessor, SecurityUtils, logger
from config import Config

def detect_container_width(content: str) -> int:
    """HTML 콘텐츠에서 container의 max-width를 감지"""
    
    # 패턴별 우선순위로 검색
    patterns = [
        r'<main[^>]*style="[^"]*max-width:\s*(\d+)px',  # main 태그 inline style
        r'\.container[^}]*max-width:\s*(\d+)px',        # CSS .container 클래스
        r'\.hero[^}]*max-width:\s*(\d+)px',             # CSS .hero 클래스  
        r'max-width:\s*min\([^,]*,\s*(\d+)px\)',        # min() 함수 사용
        r'max-width:\s*(\d+)px'                         # 일반적인 max-width
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            # 가장 큰 값을 컨테이너 크기로 사용
            width = max(int(match) for match in matches)
            logger.info(f"Detected container width: {width}px using pattern: {pattern}")
            return width
    
    # 기본값: 800px
    logger.warning("No container width detected, using default: 800px")
    return 800

def get_adaptive_coupang_ad_html(container_width: int, is_main_page: bool = False) -> str:
    """컨테이너 크기에 맞는 적응형 쿠팡 광고 HTML 생성"""
    config = Config.get_adaptive_coupang_config(container_width)
    
    # 메인 페이지와 테스트 페이지 스타일 구분
    if is_main_page:
        bg_style = "background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);"
        text_color = "#ffffff"
        text_shadow = "text-shadow: 1px 1px 2px rgba(0,0,0,0.5);"
    else:
        bg_style = "background: rgba(255, 255, 255, 0.95); border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"
        text_color = "#2d3748"
        text_shadow = ""
    
    return f'''
<!-- Coupang Partners Ad Section (Adaptive: {config['width']}x{config['height']}) -->
<div id="coupang-partners-ad" style="{bg_style} border-radius: 15px; padding: 20px; margin: 30px auto; max-width: {container_width}px; text-align: center;">
  <h3 style="color: {text_color}; margin-bottom: 15px; font-size: 1.2rem; {text_shadow}">🛍️ 추천 상품</h3>
  <p style="color: {text_color}; font-size: 0.9rem; margin-bottom: 15px; {text_shadow}">{"심리테스트를 즐기며" if is_main_page else "연애 테스트를 즐기며"} 쇼핑도 함께! 쿠팡에서 다양한 상품을 만나보세요.</p>

  <!-- 쿠팡 파트너스 광고 (적응형 크기) -->
  <div style="margin: 15px 0; width: 100%; max-width: {config['width']}px; margin-left: auto; margin-right: auto;">
    <script src="https://ads-partners.coupang.com/g.js"></script>
    <script>
      new PartnersCoupang.G({{"id":{config['id']},"template":"carousel","trackingCode":"{config['tracking_code']}","width":"{config['width']}","height":"{config['height']}","tsource":""}});
    </script>
  </div>

  <p style="color: {text_color}; font-size: 0.8rem; margin-top: 15px; {text_shadow}">
    "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
  </p>
</div>'''

def has_coupang_ad(content: str) -> bool:
    """이미 쿠팡 광고가 있는지 확인"""
    return (
        ContentProcessor.has_content_marker(content, 'Coupang Partners') or
        ContentProcessor.has_content_marker(content, 'PartnersCoupang.G') or
        ContentProcessor.has_content_marker(content, 'id="coupang-partners-ad"')
    )

def remove_existing_coupang_ad(content: str) -> str:
    """기존 쿠팡 광고(및 중복 공지)를 안전하게 제거"""
    original = None
    # 반복적으로 제거하여 중복 흔적까지 정리
    while original != content:
        original = content
        # 1) id가 있는 최신 광고 블록 제거
        content = re.sub(
            r'<div[^>]*id=["\']coupang-partners-ad["\'][^>]*>.*?</div>',
            '',
            content,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # 2) 코멘트로 시작하는 이전 광고 블록을 공지 단락까지 포함하여 제거
        content = re.sub(
            r'<!--\s*Coupang\s+Partners\s+Ad\s+Section.*?<p[^>]*>\s*"이\s*포스팅은\s*쿠팡\s*파트너스\s*활동의\s*일환으로,\s*이에\s*따른\s*일정액의\s*수수료를\s*제공받습니다\."\s*</p>\s*</div>',
            '',
            content,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # 3) 쿠팡 스크립트 포함 블록(광고 컨테이너) 제거 시도
        content = re.sub(
            r'<script\s+src=\"https://ads-partners\.coupang\.com/g\.js\"></script>.*?</script>\s*</div>',
            '',
            content,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # 4) 남아있는 중복 공지 단락과 그 직후의 닫는 div까지 제거 (잔여물 정리)
        content = re.sub(
            r'\s*<p[^>]*>\s*"이\s*포스팅은\s*쿠팡\s*파트너스\s*활동의\s*일환으로,\s*이에\s*따른\s*일정액의\s*수수료를\s*제공받습니다\."\s*</p>\s*</div>\s*',
            '',
            content,
            flags=re.DOTALL | re.IGNORECASE,
        )

    return content

def optimize_coupang_ad_in_file(file_path: str) -> bool:
    """단일 파일의 쿠팡 광고를 최적화"""
    if not SecurityUtils.validate_file_path(file_path, ['.html']):
        logger.error(f"Invalid file path: {file_path}")
        return False
    
    content = FileManager.read_file_safely(file_path)
    if not content:
        return False
    
    try:
        # 컨테이너 크기 감지
        container_width = detect_container_width(content)
        
        # 메인 페이지 여부 확인
        is_main_page = file_path in ['index.html'] or '/index.html' in file_path
        
        # 기존 쿠팡 광고 제거
        content = remove_existing_coupang_ad(content)
        
        # 새로운 적응형 광고 삽입
        adaptive_ad_html = get_adaptive_coupang_ad_html(container_width, is_main_page)
        
        if is_main_page:
            # 메인 페이지: AMP Ad 다음에 추가
            insertion_patterns = [
                r'(.*?<amp-ad.*?</amp-ad>)',
                r'(\s*</div>\s*<!-- Scroll to Top Button -->)',
                r'(\s*</div>\s*<div class="scroll-to-top")'
            ]
        else:
            # 테스트 페이지: 네비게이션 다음에 추가
            insertion_patterns = [
                r'(<div class="additional-nav">.*?</div>)',
                r'(<div class="navigation">.*?</div>)',
                r'(</div>\s*<footer>)',
                r'(</div>\s*</body>)',
                r'(<footer[^>]*>)',  # footer 태그 시작 전
                r'(</main>)',  # main 태그 끝
                r'(</div>\s*</div>\s*</body>)',  # 중첩된 div 끝
                r'(</section>\s*</div>)',  # section + div 끝
                r'(</section>)',  # section 태그 끝
                r'(<!-- Back to top functionality -->)',  # 스크립트 전
                r'(<script>\s*// Back to top)',  # Back to top 스크립트 전
                r'(<script defer)',  # defer script 전
                r'(</script>\s*</body>)',  # 스크립트 후 body 끝 전
                r'(</div>\s*<script)',  # div 끝과 script 사이
                r'(<div class="faq-section">)',  # FAQ 섹션 전
                r'(<script src="/assets/quiz-engine.js">)',  # quiz-engine 스크립트 전
                r'(<script defer src="/assets/seo-optimizer.js">)',  # seo-optimizer 스크립트 전
                r'(</body>)',  # 최후의 수단: body 태그 직전
                r'(<script defer src)',  # defer 스크립트 전
                r'(<div id="coupang-ad-container")',  # 쿠팡 애드 컨테이너 전
                r'(</div>\s*<footer)',  # footer 직전 div
            ]
        
        inserted = False
        for i, pattern in enumerate(insertion_patterns):
            if re.search(pattern, content, re.DOTALL):
                try:
                    content = re.sub(
                        pattern,
                        r'\1' + adaptive_ad_html,
                        content,
                        flags=re.DOTALL
                    )
                    inserted = True
                    logger.info(f"광고 삽입 성공 - 패턴 {i+1}: {pattern[:30]}...")
                    break
                except Exception as e:
                    logger.warning(f"패턴 {i+1} 실패: {e}")
                    continue
        
        if not inserted:
            logger.warning(f"{file_path}: 삽입 위치를 찾을 수 없음")
            return False
        
        # 파일 저장
        success = FileManager.write_file_safely(file_path, content)
        if success:
            logger.info(f"✅ {file_path}: 적응형 광고 최적화 완료 (컨테이너: {container_width}px)")
        
        return success
        
    except Exception as e:
        logger.error(f"Unexpected error processing {file_path}: {e}")
        return False

def find_candidate_files() -> List[str]:
    """최적화 대상 파일 찾기: 한국어 HTML 전체"""
    return FileManager.find_html_files_by_language('ko')

def main():
    """메인 실행 함수"""
    logger.info("쿠팡 광고 크기 최적화 시작")
    
    # 한국어 HTML 전체를 최적화 대상으로 사용 (있다면 제거 후 1회 삽입)
    files_to_optimize = find_candidate_files()
    
    if not files_to_optimize:
        logger.error("쿠팡 광고가 있는 파일을 찾을 수 없습니다.")
        return
    
    logger.info(f"최적화할 파일: {len(files_to_optimize)}개")
    
    success_count = 0
    fail_count = 0
    
    for file_path in files_to_optimize:
        logger.info(f"최적화 중: {file_path}")
        
        if optimize_coupang_ad_in_file(file_path):
            success_count += 1
        else:
            fail_count += 1
    
    logger.info(f"쿠팡 광고 최적화 완료! 성공: {success_count}개, 실패: {fail_count}개")

if __name__ == "__main__":
    main()
