
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def get_test_coupang_ad(test_num):
    """개별 테스트 페이지용 쿠팡 광고 HTML 반환"""
    return f'''
  <!-- Coupang Partners Ad Section -->
  <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 30px; margin: 40px auto; max-width: 800px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.2);">
    <h3 style="color: #ffffff; margin-bottom: 15px; font-size: 1.4rem; font-weight: 700; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">💕 연애 테스트 #{test_num} 관련 추천 상품</h3>
    <p style="color: #ffffff; font-size: 1rem; margin-bottom: 20px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">연애 심리 분석 결과와 함께 연인과의 시간을 더욱 특별하게 만들어줄 상품들을 확인해보세요!</p>
    
    <!-- 쿠팡 파트너스 광고 -->
    <div style="margin: 20px 0; width: 100%; max-width: 750px; overflow: hidden; margin-left: auto; margin-right: auto;">
      <div id="coupang-ad-container" style="width: 100%; max-width: 750px; overflow: hidden;">
        <script src="https://ads-partners.coupang.com/g.js"></script>
        <script>
          // 모바일 대응 광고 크기 조정
          const isMobile = window.innerWidth <= 768;
          const adWidth = isMobile ? Math.min(window.innerWidth - 40, 300) : 750;
          const adHeight = isMobile ? 120 : 150;
          
          new PartnersCoupang.G({{
            "id": 867629,
            "template": "carousel",
            "trackingCode": "AF6959276",
            "width": adWidth.toString(),
            "height": adHeight.toString(),
            "tsource": ""
          }});
        </script>
      </div>
    </div>
    
    <p style="color: #ffffff; font-size: 0.8rem; margin-top: 15px; font-style: italic; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
      "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
    </p>
  </div>
'''

def add_coupang_to_test_file(file_path):
    """테스트 파일에 쿠팡 광고 추가"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 쿠팡 광고가 있는지 확인
        if 'PartnersCoupang.G' in content:
            print(f"⚠️  {file_path}: 이미 쿠팡 광고가 있음")
            return False
        
        # 테스트 번호 추출
        test_num = re.search(r'test(\d+)\.html', str(file_path))
        test_number = test_num.group(1) if test_num else "1"
        
        # footer 전에 광고 삽입
        footer_pattern = r'(<footer>)'
        if re.search(footer_pattern, content):
            content = re.sub(
                footer_pattern,
                get_test_coupang_ad(test_number) + r'\1',
                content
            )
        else:
            # </body> 전에 삽입
            body_end_pattern = r'(</body>)'
            if re.search(body_end_pattern, content):
                content = re.sub(
                    body_end_pattern,
                    get_test_coupang_ad(test_number) + r'\1',
                    content
                )
            else:
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
    print("🔍 연애 테스트 파일들 검색 중...")
    
    # romance-test/ko 디렉토리의 모든 test 파일들 찾기
    test_files = []
    ko_dir = Path('romance-test/ko')
    
    if ko_dir.exists():
        for i in range(1, 31):  # test1.html ~ test30.html
            test_file = ko_dir / f'test{i}.html'
            if test_file.exists():
                test_files.append(str(test_file))
    
    print(f"📋 발견된 테스트 파일: {len(test_files)}개")
    
    if not test_files:
        print("❌ 연애 테스트 파일을 찾을 수 없습니다.")
        return
    
    success_count = 0
    
    for file_path in test_files:
        print(f"처리 중: {file_path}")
        if add_coupang_to_test_file(file_path):
            success_count += 1
            print(f"✅ {file_path}: 쿠팡 광고 추가 완료")
        else:
            print(f"❌ {file_path}: 쿠팡 광고 추가 실패")
    
    print(f"\n🎉 작업 완료: {success_count}/{len(test_files)}개 파일 처리됨")

if __name__ == "__main__":
    main()
