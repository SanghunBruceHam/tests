
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def get_coupang_ad_html():
    """쿠팡 파트너스 광고 HTML 반환"""
    return '''
<!-- Coupang Partners Ad Section -->
<div style="background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 20px; margin: 30px auto; max-width: 800px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
  <h3 style="color: #2d3748; margin-bottom: 15px; font-size: 1.2rem;">🛍️ 추천 상품</h3>
  <p style="color: #4a5568; font-size: 0.9rem; margin-bottom: 15px;">연애 테스트를 즐기며 쇼핑도 함께! 쿠팡에서 다양한 상품을 만나보세요.</p>

  <!-- 쿠팡 파트너스 광고 -->
  <div style="margin: 15px 0; width: 100%; max-width: 750px;">
    <script src="https://ads-partners.coupang.com/g.js"></script>
    <script>
      new PartnersCoupang.G({"id":867629,"template":"carousel","trackingCode":"AF6959276","width":"750","height":"150","tsource":""});
    </script>
  </div>

  <p style="color: #4a5568; font-size: 0.8rem; margin-top: 15px;">
    "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
  </p>
</div>'''

def get_main_page_coupang_ad_html():
    """메인 페이지용 쿠팡 파트너스 광고 HTML 반환"""
    return '''
  <!-- Coupang Partners Ad Section -->
  <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 20px; margin: 40px auto; max-width: 800px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.2);">
    <h3 style="color: #ffffff; margin-bottom: 15px; font-size: 1.2rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">🛍️ 추천 상품</h3>
    <p style="color: #ffffff; font-size: 0.9rem; margin-bottom: 15px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">심리테스트를 즐기며 쇼핑도 함께! 쿠팡에서 다양한 상품을 만나보세요.</p>
    
    <!-- 쿠팡 파트너스 광고 -->
    <div style="margin: 15px 0;">
      <script src="https://ads-partners.coupang.com/g.js"></script>
      <script>
        new PartnersCoupang.G({"id":867629,"template":"carousel","trackingCode":"AF6959276","width":"680","height":"140","tsource":""});
      </script>
    </div>
    
    <p style="color: #ffffff; font-size: 0.8rem; margin-top: 15px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
      "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
    </p>
  </div>'''

def find_korean_html_files():
    """한국어 HTML 파일들을 찾아서 반환"""
    korean_files = []
    
    # 루트 index.html
    if os.path.exists('index.html'):
        korean_files.append('index.html')
    
    # ko/ 디렉토리의 파일들
    ko_dir = Path('ko')
    if ko_dir.exists():
        for file in ko_dir.glob('*.html'):
            korean_files.append(str(file))
    
    # 각 테스트 디렉토리의 ko/ 하위 파일들
    for test_dir in ['romance-test', 'egen-teto']:
        ko_test_dir = Path(test_dir) / 'ko'
        if ko_test_dir.exists():
            for file in ko_test_dir.glob('*.html'):
                korean_files.append(str(file))
    
    return korean_files

def has_coupang_ad(content):
    """이미 쿠팡 광고가 있는지 확인"""
    return 'Coupang Partners' in content or 'PartnersCoupang.G' in content

def add_coupang_ad_to_main_page(file_path):
    """메인 페이지에 쿠팡 광고 추가"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if has_coupang_ad(content):
            print(f"⚠️  {file_path}: 이미 쿠팡 광고가 있음")
            return False
        
        # AMP Ad 다음에 추가
        amp_ad_pattern = r'(.*?<amp-ad.*?</amp-ad>)'
        footer_pattern = r'(\s*</div>\s*<!-- Scroll to Top Button -->)'
        
        if re.search(amp_ad_pattern, content, re.DOTALL):
            # AMP Ad 다음에 추가
            content = re.sub(
                amp_ad_pattern,
                r'\1' + get_main_page_coupang_ad_html(),
                content,
                flags=re.DOTALL
            )
        elif re.search(footer_pattern, content):
            # Scroll to Top Button 전에 추가
            content = re.sub(
                footer_pattern,
                get_main_page_coupang_ad_html() + r'\1',
                content
            )
        else:
            # </div> 태그 전에 추가 (컨테이너 끝)
            container_end_pattern = r'(\s*</div>\s*<!-- Scroll to Top Button -->|\s*</div>\s*<div class="scroll-to-top")'
            if re.search(container_end_pattern, content):
                content = re.sub(
                    container_end_pattern,
                    get_main_page_coupang_ad_html() + r'\1',
                    content
                )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ {file_path} 처리 실패: {e}")
        return False

def add_coupang_ad_to_test_page(file_path):
    """테스트 페이지에 쿠팡 광고 추가"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if has_coupang_ad(content):
            print(f"⚠️  {file_path}: 이미 쿠팡 광고가 있음")
            return False
        
        # </div> 태그 찾기 (navigation 다음, footer 전)
        insertion_patterns = [
            r'(<div class="additional-nav">.*?</div>)',  # additional-nav 다음
            r'(<div class="navigation">.*?</div>)',      # navigation 다음  
            r'(</div>\s*<footer>)',                      # footer 전
            r'(</div>\s*</body>)'                        # body 끝 전
        ]
        
        inserted = False
        for pattern in insertion_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(
                    pattern,
                    r'\1' + get_coupang_ad_html(),
                    content,
                    flags=re.DOTALL
                )
                inserted = True
                break
        
        if not inserted:
            print(f"⚠️  {file_path}: 삽입 위치를 찾을 수 없음")
            return False
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ {file_path} 처리 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🔍 한국어 HTML 파일 검색 중...")
    korean_files = find_korean_html_files()
    
    if not korean_files:
        print("❌ 한국어 HTML 파일을 찾을 수 없습니다.")
        return
    
    print(f"📋 발견된 한국어 파일: {len(korean_files)}개")
    
    success_count = 0
    skip_count = 0
    
    for file_path in korean_files:
        print(f"\n처리 중: {file_path}")
        
        # 메인 페이지인지 테스트 페이지인지 구분
        if file_path in ['index.html'] or '/index.html' in file_path:
            if add_coupang_ad_to_main_page(file_path):
                success_count += 1
                print(f"✅ {file_path}: 메인 페이지 광고 추가 완료")
            else:
                skip_count += 1
        else:
            if add_coupang_ad_to_test_page(file_path):
                success_count += 1
                print(f"✅ {file_path}: 테스트 페이지 광고 추가 완료")
            else:
                skip_count += 1
    
    print(f"\n🎉 작업 완료!")
    print(f"✅ 성공: {success_count}개 파일")
    print(f"⚠️  건너뜀: {skip_count}개 파일")

if __name__ == "__main__":
    main()
