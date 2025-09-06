
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
from typing import List
from utils import FileManager, ContentProcessor, SecurityUtils, logger
from config import Config
import re

def get_coupang_ad_html(container_width: int = 800) -> str:
    """쿠팡 파트너스 광고 HTML 반환 (적응형)"""
    config = Config.get_adaptive_coupang_config(container_width)
    return f'''
<!-- Coupang Partners Ad Section (Adaptive: {config['width']}x{config['height']}) -->
<div style="background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 20px; margin: 30px auto; max-width: {container_width}px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
  <h3 style="color: #2d3748; margin-bottom: 15px; font-size: 1.2rem;">🛍️ 추천 상품</h3>
  <p style="color: #4a5568; font-size: 0.9rem; margin-bottom: 15px;">연애 테스트를 즐기며 쇼핑도 함께! 쿠팡에서 다양한 상품을 만나보세요.</p>

  <!-- 쿠팡 파트너스 광고 (적응형 크기) -->
  <div style="margin: 15px 0; width: 100%; max-width: {config['width']}px; margin-left: auto; margin-right: auto;">
    <script src="https://ads-partners.coupang.com/g.js"></script>
    <script>
      new PartnersCoupang.G({{"id":{config['id']},"template":"carousel","trackingCode":"{config['tracking_code']}","width":"{config['width']}","height":"{config['height']}","tsource":""}});
    </script>
  </div>

  <p style="color: #4a5568; font-size: 0.8rem; margin-top: 15px;">
    "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
  </p>
</div>'''

def get_main_page_coupang_ad_html(container_width: int = 800) -> str:
    """메인 페이지용 쿠팡 파트너스 광고 HTML 반환 (적응형)"""
    config = Config.get_adaptive_coupang_config(container_width)
    return f'''
  <!-- Coupang Partners Ad Section (Adaptive: {config['width']}x{config['height']}) -->
  <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 20px; margin: 40px auto; max-width: {container_width}px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.2);">
    <h3 style="color: #ffffff; margin-bottom: 15px; font-size: 1.2rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">🛍️ 추천 상품</h3>
    <p style="color: #ffffff; font-size: 0.9rem; margin-bottom: 15px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">심리테스트를 즐기며 쇼핑도 함께! 쿠팡에서 다양한 상품을 만나보세요.</p>
    
    <!-- 쿠팡 파트너스 광고 (적응형 크기) -->
    <div style="margin: 15px 0; width: 100%; max-width: {config['width']}px; margin-left: auto; margin-right: auto;">
      <script src="https://ads-partners.coupang.com/g.js"></script>
      <script>
        new PartnersCoupang.G({{"id":{config['id']},"template":"carousel","trackingCode":"{config['tracking_code']}","width":"{config['width']}","height":"{config['height']}","tsource":""}});
      </script>
    </div>
    
    <p style="color: #ffffff; font-size: 0.8rem; margin-top: 15px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
      "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
    </p>
  </div>'''

def find_korean_html_files() -> List[str]:
    """한국어 HTML 파일들을 찾아서 반환 (레거시 호환성)"""
    return FileManager.find_html_files_by_language('ko')

def has_coupang_ad(content: str) -> bool:
    """이미 쿠팡 광고가 있는지 확인"""
    return ContentProcessor.has_content_marker(content, 'Coupang Partners') or \
           ContentProcessor.has_content_marker(content, 'PartnersCoupang.G')

def detect_container_width(content: str) -> int:
    """컨테이너 크기 감지"""
    patterns = [
        r'<main[^>]*style="[^"]*max-width:\s*(\d+)px',
        r'\.container[^}]*max-width:\s*(\d+)px',
        r'\.hero[^}]*max-width:\s*(\d+)px',
        r'max-width:\s*min\([^,]*,\s*(\d+)px\)',
        r'max-width:\s*(\d+)px'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            return max(int(match) for match in matches)
    
    return 800  # 기본값

def add_coupang_ad_to_main_page(file_path: str) -> bool:
    """메인 페이지에 쿠팡 광고 추가"""
    if not SecurityUtils.validate_file_path(file_path, ['.html']):
        logger.error(f"Invalid file path: {file_path}")
        return False
    
    content = FileManager.read_file_safely(file_path)
    if not content:
        return False
    
    if has_coupang_ad(content):
        logger.warning(f"{file_path}: 이미 쿠팡 광고가 있음")
        return False
    
    try:
        # 컨테이너 크기 감지
        container_width = detect_container_width(content)
        
        # AMP Ad 다음에 추가
        amp_ad_pattern = r'(.*?<amp-ad.*?</amp-ad>)'
        footer_pattern = r'(\s*</div>\s*<!-- Scroll to Top Button -->)'
        
        if re.search(amp_ad_pattern, content, re.DOTALL):
            content = re.sub(
                amp_ad_pattern,
                r'\1' + get_main_page_coupang_ad_html(container_width),
                content,
                flags=re.DOTALL
            )
        elif re.search(footer_pattern, content):
            content = re.sub(
                footer_pattern,
                get_main_page_coupang_ad_html(container_width) + r'\1',
                content
            )
        else:
            container_end_pattern = r'(\s*</div>\s*<!-- Scroll to Top Button -->|\s*</div>\s*<div class="scroll-to-top")'
            if re.search(container_end_pattern, content):
                content = re.sub(
                    container_end_pattern,
                    get_main_page_coupang_ad_html(container_width) + r'\1',
                    content
                )
        
        return FileManager.write_file_safely(file_path, content)
        
    except re.error as e:
        logger.error(f"Regex error in {file_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error processing {file_path}: {e}")
        return False

def add_coupang_ad_to_test_page(file_path: str) -> bool:
    """테스트 페이지에 쿠팡 광고 추가"""
    if not SecurityUtils.validate_file_path(file_path, ['.html']):
        logger.error(f"Invalid file path: {file_path}")
        return False
    
    content = FileManager.read_file_safely(file_path)
    if not content:
        return False
    
    if has_coupang_ad(content):
        logger.warning(f"{file_path}: 이미 쿠팡 광고가 있음")
        return False
    
    try:
        # 컨테이너 크기 감지
        container_width = detect_container_width(content)
        
        insertion_patterns = [
            r'(<div class="additional-nav">.*?</div>)',
            r'(<div class="navigation">.*?</div>)',
            r'(</div>\s*<footer>)',
            r'(</div>\s*</body>)'
        ]
        
        for pattern in insertion_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(
                    pattern,
                    r'\1' + get_coupang_ad_html(container_width),
                    content,
                    flags=re.DOTALL
                )
                return FileManager.write_file_safely(file_path, content)
        
        logger.warning(f"{file_path}: 삽입 위치를 찾을 수 없음")
        return False
        
    except re.error as e:
        logger.error(f"Regex error in {file_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error processing {file_path}: {e}")
        return False

def main():
    """메인 실행 함수"""
    logger.info("한국어 HTML 파일 검색 시작")
    korean_files = find_korean_html_files()
    
    if not korean_files:
        logger.error("한국어 HTML 파일을 찾을 수 없습니다.")
        return
    
    logger.info(f"발견된 한국어 파일: {len(korean_files)}개")
    
    success_count = 0
    skip_count = 0
    
    for file_path in korean_files:
        logger.info(f"처리 중: {file_path}")
        
        is_main_page = file_path in ['index.html'] or '/index.html' in file_path
        
        if is_main_page:
            success = add_coupang_ad_to_main_page(file_path)
            page_type = "메인 페이지"
        else:
            success = add_coupang_ad_to_test_page(file_path)
            page_type = "테스트 페이지"
        
        if success:
            success_count += 1
            logger.info(f"✅ {file_path}: {page_type} 광고 추가 완료")
        else:
            skip_count += 1
    
    logger.info(f"작업 완료! 성공: {success_count}개, 건너뜀: {skip_count}개")

if __name__ == "__main__":
    main()
