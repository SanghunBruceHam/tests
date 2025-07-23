
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def get_improved_coupang_ad_html():
    """개선된 쿠팡 파트너스 광고 HTML 반환"""
    return '''
<!-- Coupang Partners Ad Section -->
<div style="background: var(--card_bg); backdrop-filter: blur(20px); border-radius: 16px; padding: 20px; margin: 40px auto; max-width: 840px; text-align: center; border: 1px solid var(--border_color); box-shadow: var(--shadow);">
  <h3 style="color: var(--text_primary); margin-bottom: 15px; font-size: 1.3rem; font-weight: 700;">💕 연애 관련 추천 상품</h3>
  <p style="color: var(--text_secondary); font-size: 1rem; margin-bottom: 20px;">연애 테스트를 즐기며 쇼핑도 함께! 쿠팡에서 다양한 상품을 만나보세요.</p>
  
  <!-- 쿠팡 파트너스 광고 -->
  <div id="coupang-ad-container" style="width: 100%; max-width: 840px; margin: 20px auto; display: flex; justify-content: center; align-items: center; overflow: hidden;">
    <script src="https://ads-partners.coupang.com/g.js"></script>
    <script>
      // 화면 크기에 따른 광고 크기 조정
      const isMobile = window.innerWidth <= 768;
      const isSmallMobile = window.innerWidth <= 480;
      
      let adWidth, adHeight;
      
      if (isSmallMobile) {
        adWidth = Math.min(window.innerWidth - 40, 320);
        adHeight = 160;
      } else if (isMobile) {
        adWidth = Math.min(window.innerWidth - 40, 500);
        adHeight = 180;
      } else {
        adWidth = 840;
        adHeight = 200;
      }
      
      new PartnersCoupang.G({
        "id": 867629,
        "template": "carousel",
        "trackingCode": "AF6959276",
        "width": adWidth.toString(),
        "height": adHeight.toString(),
        "tsource": ""
      });
    </script>
  </div>
  
  <p style="color: var(--text_secondary); font-size: 0.85rem; margin-top: 20px; font-style: italic;">
    "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
  </p>
</div>'''

def get_coupang_css_styles():
    """쿠팡 광고용 CSS 스타일 반환"""
    return '''
    /* 쿠팡 광고 반응형 스타일 */
    #coupang-ad-container iframe,
    #coupang-ad-container > div {
      max-width: 100% !important;
      width: 100% !important;
    }

    @media (max-width: 768px) {
      #coupang-ad-container {
        max-width: 100% !important;
      }
      
      #coupang-ad-container iframe,
      #coupang-ad-container > div {
        max-width: 500px !important;
        width: 100% !important;
      }
    }

    @media (max-width: 480px) {
      #coupang-ad-container iframe,
      #coupang-ad-container > div {
        max-width: 320px !important;
        width: 100% !important;
      }
    }'''

def update_coupang_ad_in_test_file(file_path):
    """테스트 파일의 쿠팡 광고를 업데이트"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 쿠팡 광고가 있는지 확인
        if 'PartnersCoupang.G' not in content:
            return False, "쿠팡 광고 없음"
        
        # 이미 업데이트된 광고인지 확인
        if 'max-width: 840px' in content and 'isSmallMobile' in content:
            return False, "이미 업데이트됨"
        
        # 기존 쿠팡 광고 섹션을 찾아서 교체
        patterns = [
            r'<!-- Coupang Partners Ad Section -->.*?</div>\s*</div>',
            r'<div style="background: .*?쿠팡 파트너스.*?</div>\s*</div>',
            r'<div[^>]*>.*?PartnersCoupang\.G.*?</div>\s*</div>'
        ]
        
        updated = False
        for pattern in patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, get_improved_coupang_ad_html().strip(), content, flags=re.DOTALL)
                updated = True
                break
        
        if not updated:
            return False, "쿠팡 광고 패턴을 찾을 수 없음"
        
        # CSS 스타일 추가/업데이트
        if '#coupang-ad-container' not in content:
            # </style> 태그 바로 앞에 CSS 추가
            css_pattern = r'(\s*</style>)'
            if re.search(css_pattern, content):
                content = re.sub(css_pattern, get_coupang_css_styles() + r'\1', content)
            else:
                # head 태그 끝에 스타일 추가
                head_pattern = r'(</head>)'
                style_block = f'\n  <style>{get_coupang_css_styles()}\n  </style>\n'
                content = re.sub(head_pattern, style_block + r'\1', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, "성공"
        
    except Exception as e:
        return False, f"오류: {e}"

def main():
    """메인 실행 함수"""
    print("🔍 romance-test 한국어 테스트 파일 검색 중...")
    
    # romance-test/ko 디렉토리의 test 파일들 찾기
    test_files = []
    ko_dir = Path('romance-test/ko')
    
    if ko_dir.exists():
        for file in ko_dir.glob('test*.html'):
            test_files.append(str(file))
    
    if not test_files:
        print("❌ romance-test 한국어 테스트 파일을 찾을 수 없습니다.")
        return
    
    print(f"📋 발견된 테스트 파일: {len(test_files)}개")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for file_path in sorted(test_files):
        success, message = update_coupang_ad_in_test_file(file_path)
        
        if success:
            print(f"✅ {file_path}: {message}")
            success_count += 1
        elif "이미 업데이트됨" in message:
            print(f"⚠️  {file_path}: {message}")
            skip_count += 1
        else:
            print(f"❌ {file_path}: {message}")
            error_count += 1
    
    print(f"\n📊 작업 완료!")
    print(f"✅ 성공: {success_count}개")
    print(f"⚠️  건너뜀: {skip_count}개")
    print(f"❌ 실패: {error_count}개")
    print(f"📁 총 파일: {len(test_files)}개")

if __name__ == "__main__":
    main()
