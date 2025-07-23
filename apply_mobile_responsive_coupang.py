
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def update_coupang_ad_mobile_responsive():
    """연애 테스트 페이지들의 쿠팡 광고를 모바일 반응형으로 업데이트"""
    
    # romance-test/ko 디렉토리의 모든 test 파일들 찾기
    test_files = []
    ko_dir = Path('romance-test/ko')
    
    if ko_dir.exists():
        for file in ko_dir.glob('test*.html'):
            test_files.append(str(file))
    
    print(f"🔍 발견된 테스트 파일: {len(test_files)}개")
    
    updated_count = 0
    
    for file_path in test_files:
        try:
            print(f"처리 중: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 쿠팡 광고가 있는지 확인
            if 'PartnersCoupang.G' not in content:
                print(f"⚠️  {file_path}: 쿠팡 광고 없음")
                continue
            
            # 이미 모바일 반응형이 적용되어 있는지 확인
            if 'coupang-ad-container' in content and 'max-width: 100%' in content:
                print(f"✅ {file_path}: 이미 모바일 반응형 적용됨")
                continue
            
            # 기존 쿠팡 광고 섹션을 모바일 반응형으로 교체
            old_pattern = r'<!-- Coupang Partners Ad Section -->.*?</div>\s*</div>'
            
            new_ad_section = '''<!-- Coupang Partners Ad Section -->
<div style="background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 20px; margin: 30px auto; max-width: 800px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
  <h3 style="color: #2d3748; margin-bottom: 15px; font-size: 1.2rem;">🛍️ 추천 상품</h3>
  <p style="color: #4a5568; font-size: 0.9rem; margin-bottom: 15px;">연애 테스트를 즐기며 쇼핑도 함께! 쿠팡에서 다양한 상품을 만나보세요.</p>

  <!-- 쿠팡 파트너스 광고 -->
  <div style="margin: 15px 0; width: 100%; max-width: 750px; overflow: hidden;">
    <div id="coupang-ad-container" style="width: 100%; max-width: 750px; overflow: hidden;">
      <script src="https://ads-partners.coupang.com/g.js"></script>
      <script>
        // 모바일 대응 광고 크기 조정
        const isMobile = window.innerWidth <= 768;
        const adWidth = isMobile ? Math.min(window.innerWidth - 40, 300) : 750;
        const adHeight = isMobile ? 120 : 150;
        
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
  </div>

  <p style="color: #4a5568; font-size: 0.8rem; margin-top: 15px;">
    "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
  </p>
</div>'''

            # CSS 스타일도 추가
            css_styles = '''
    /* 쿠팡 광고 반응형 스타일 */
    #coupang-ad-container {
      display: flex;
      justify-content: center;
      align-items: center;
    }

    #coupang-ad-container iframe,
    #coupang-ad-container div {
      max-width: 100% !important;
      width: 100% !important;
      height: auto !important;
    }

    @media (max-width: 768px) {
      #coupang-ad-container {
        width: 100% !important;
        max-width: 100% !important;
      }
      
      #coupang-ad-container iframe,
      #coupang-ad-container div {
        width: 100% !important;
        max-width: 300px !important;
        height: 120px !important;
      }
    }'''

            # 1. 기존 쿠팡 광고 섹션 교체
            if re.search(old_pattern, content, re.DOTALL):
                content = re.sub(old_pattern, new_ad_section, content, flags=re.DOTALL)
                updated_count += 1
                print(f"✅ {file_path}: 광고 섹션 업데이트 완료")
            else:
                print(f"⚠️  {file_path}: 광고 섹션 패턴을 찾을 수 없음")
                continue
            
            # 2. CSS 스타일 추가 (head 태그 끝 전에)
            if css_styles not in content:
                head_end_pattern = r'(</style>\s*</head>)'
                if re.search(head_end_pattern, content):
                    content = re.sub(
                        head_end_pattern,
                        css_styles + r'\1',
                        content
                    )
                else:
                    # </head> 전에 직접 추가
                    content = re.sub(
                        r'(</head>)',
                        f'  <style>{css_styles}\n  </style>\n\\1',
                        content
                    )
            
            # 파일 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            print(f"❌ {file_path} 처리 실패: {e}")
    
    print(f"\n🎉 완료! {updated_count}개 파일이 업데이트되었습니다.")

if __name__ == "__main__":
    update_coupang_ad_mobile_responsive()
