
import os
import re
from pathlib import Path

def get_mobile_responsive_coupang_ad():
    """모바일 반응형 쿠팡 광고 HTML 반환"""
    return '''
    <!-- 쿠팡 파트너스 광고 -->
    <div style="margin: 15px 0; width: 100%; max-width: 680px; overflow: hidden;">
      <div id="coupang-ad-container" style="width: 100%; max-width: 680px; overflow: hidden;">
        <script src="https://ads-partners.coupang.com/g.js"></script>
        <script>
          // 모바일 대응 광고 크기 조정
          const isMobile = window.innerWidth <= 768;
          const adWidth = isMobile ? Math.min(window.innerWidth - 40, 300) : 680;
          const adHeight = isMobile ? 120 : 140;
          
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
    </div>'''

def get_mobile_css_styles():
    """모바일 반응형 CSS 스타일 반환"""
    return '''
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
    
    # 각 테스트 디렉토리의 ko/ 폴더
    for item in os.listdir('.'):
        if os.path.isdir(item) and not item.startswith('.'):
            ko_path = Path(item) / 'ko'
            if ko_path.exists():
                for file in ko_path.glob('*.html'):
                    korean_files.append(str(file))
    
    return sorted(korean_files)

def update_coupang_ad_in_file(file_path):
    """파일의 쿠팡 광고를 모바일 반응형으로 업데이트"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 모바일 반응형 광고가 있는지 확인
        if 'const isMobile = window.innerWidth <= 768;' in content:
            return False, "이미 모바일 반응형 적용됨"
        
        # 기존 쿠팡 광고 패턴들 찾기
        old_patterns = [
            # 기본 쿠팡 광고 패턴
            r'<script src="https://ads-partners\.coupang\.com/g\.js"></script>\s*<script>\s*new PartnersCoupang\.G\([^}]+\);\s*</script>',
            # div로 감싼 쿠팡 광고 패턴
            r'<div[^>]*>\s*<script src="https://ads-partners\.coupang\.com/g\.js"></script>\s*<script>\s*new PartnersCoupang\.G\([^}]+\);\s*</script>\s*</div>',
            # width가 명시된 패턴들
            r'<script>\s*new PartnersCoupang\.G\(\{"id":867629,"template":"carousel","trackingCode":"AF6959276","width":"[^"]+","height":"[^"]+","tsource":""\}\);\s*</script>'
        ]
        
        # 기존 광고를 새로운 모바일 반응형 광고로 교체
        updated = False
        for pattern in old_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, get_mobile_responsive_coupang_ad().strip(), content, flags=re.DOTALL)
                updated = True
                break
        
        if not updated:
            return False, "쿠팡 광고를 찾을 수 없음"
        
        # CSS 스타일 추가 확인 및 추가
        if '#coupang-ad-container' not in content:
            # </style> 태그 바로 앞에 CSS 추가
            css_pattern = r'(\s*</style>)'
            if re.search(css_pattern, content):
                content = re.sub(css_pattern, get_mobile_css_styles() + r'\1', content)
            else:
                # head 태그 끝에 스타일 추가
                head_pattern = r'(</head>)'
                style_block = f'\n  <style>{get_mobile_css_styles()}\n  </style>\n'
                content = re.sub(head_pattern, style_block + r'\1', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, "성공"
        
    except Exception as e:
        return False, f"오류: {e}"

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
    error_count = 0
    
    for file_path in korean_files:
        success, message = update_coupang_ad_in_file(file_path)
        
        if success:
            print(f"✅ {file_path}: {message}")
            success_count += 1
        elif "이미 모바일 반응형 적용됨" in message:
            print(f"⚠️  {file_path}: {message}")
            skip_count += 1
        else:
            print(f"❌ {file_path}: {message}")
            error_count += 1
    
    print(f"\n📊 작업 완료!")
    print(f"✅ 성공: {success_count}개")
    print(f"⚠️  건너뜀: {skip_count}개")
    print(f"❌ 실패: {error_count}개")
    print(f"📁 총 파일: {len(korean_files)}개")

if __name__ == "__main__":
    main()
