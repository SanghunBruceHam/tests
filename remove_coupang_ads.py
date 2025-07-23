
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def remove_coupang_ads_from_file(file_path):
    """파일에서 쿠팡 광고를 제거"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 쿠팡 광고가 있는지 확인
        if 'PartnersCoupang.G' not in content and 'Coupang Partners' not in content:
            return False, "쿠팡 광고 없음"
        
        original_content = content
        
        # 다양한 쿠팡 광고 패턴들을 모두 제거
        patterns = [
            # Coupang Partners Ad Section 전체
            r'<!-- Coupang Partners Ad Section -->.*?</div>\s*</div>',
            r'<div[^>]*>.*?Coupang Partners.*?</div>\s*</div>',
            
            # 광고 섹션만
            r'<div[^>]*ad-section[^>]*>.*?</div>',
            r'<div[^>]*>.*?🛍️.*?추천 상품.*?</div>\s*</div>',
            r'<div[^>]*>.*?💕 연애 관련 추천 상품.*?</div>\s*</div>',
            r'<div[^>]*>.*?🧠 심리테스트 관련 추천 상품.*?</div>\s*</div>',
            
            # 쿠팡 스크립트 블록
            r'<script src="https://ads-partners\.coupang\.com/g\.js"></script>.*?</script>',
            r'<div[^>]*coupang-ad-container[^>]*>.*?</div>',
            
            # 쿠팡 파트너스 문구
            r'<p[^>]*>.*?"이 포스팅은 쿠팡 파트너스.*?</p>',
            
            # 전체 광고 div
            r'<div[^>]*background:.*?rgba\(255, 255, 255.*?</div>\s*</div>',
            r'<div[^>]*backdrop-filter: blur.*?</div>\s*</div>',
        ]
        
        # 각 패턴으로 제거 시도
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 빈 줄 정리
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "성공"
        else:
            return False, "변경사항 없음"
        
    except Exception as e:
        return False, f"오류: {e}"

def main():
    """메인 실행 함수"""
    print("🔍 romance-test 한국어 테스트 파일에서 쿠팡 광고 제거 중...")
    
    # romance-test/ko 디렉토리의 모든 HTML 파일들 찾기
    files_to_process = []
    ko_dir = Path('romance-test/ko')
    
    if ko_dir.exists():
        for file in ko_dir.glob('*.html'):
            files_to_process.append(str(file))
    
    if not files_to_process:
        print("❌ romance-test 한국어 파일을 찾을 수 없습니다.")
        return
    
    print(f"📋 발견된 파일: {len(files_to_process)}개")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for file_path in files_to_process:
        success, message = remove_coupang_ads_from_file(file_path)
        
        if success:
            print(f"✅ {file_path}: {message}")
            success_count += 1
        elif "쿠팡 광고 없음" in message or "변경사항 없음" in message:
            print(f"⚠️  {file_path}: {message}")
            skip_count += 1
        else:
            print(f"❌ {file_path}: {message}")
            error_count += 1
    
    print(f"\n📊 작업 완료!")
    print(f"✅ 성공: {success_count}개")
    print(f"⚠️  건너뜀: {skip_count}개")
    print(f"❌ 실패: {error_count}개")
    print(f"📁 총 파일: {len(files_to_process)}개")

if __name__ == "__main__":
    main()
