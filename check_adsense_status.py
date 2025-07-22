
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def check_adsense_in_file(file_path):
    """파일의 AdSense 구현 상태 확인"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # 1. Head 섹션에 필요한 스크립트들 확인
        has_adsense_script = 'pagead2.googlesyndication.com/pagead/js/adsbygoogle.js' in content
        has_amp_script = 'cdn.ampproject.org/v0/amp-ad-0.1.js' in content
        
        if not has_adsense_script:
            issues.append("❌ AdSense 스크립트가 헤드에 없음")
        if not has_amp_script:
            issues.append("❌ AMP 스크립트가 헤드에 없음")
        
        # 2. AMP 광고 확인
        amp_ad_pattern = r'<amp-ad width="100vw" height="320"[^>]*data-ad-client="ca-pub-5508768187151867"[^>]*>'
        has_amp_ad = re.search(amp_ad_pattern, content)
        
        if not has_amp_ad:
            issues.append("❌ AMP 광고가 없음")
        
        # 3. 일반 AdSense 광고 확인
        adsense_ins_pattern = r'<ins class="adsbygoogle"[^>]*data-ad-client="ca-pub-5508768187151867"[^>]*data-ad-slot="7298546648"[^>]*>'
        has_adsense_ins = re.search(adsense_ins_pattern, content)
        
        if not has_adsense_ins:
            issues.append("❌ AdSense ins 태그가 없음")
        
        # 4. AdSense 초기화 스크립트 확인
        adsense_init_pattern = r'\(adsbygoogle = window\.adsbygoogle \|\| \[\]\)\.push\(\{\}\);'
        has_adsense_init = re.search(adsense_init_pattern, content)
        
        if not has_adsense_init:
            issues.append("❌ AdSense 초기화 스크립트가 없음")
        
        # 5. 중복된 스크립트 확인
        adsense_script_count = len(re.findall(r'pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js', content))
        if adsense_script_count > 2:
            issues.append(f"⚠️ AdSense 스크립트 중복 ({adsense_script_count}개)")
        
        # 6. 잘못된 광고 코드 패턴 확인
        old_patterns = [
            r'data-ad-format="autorelaxed"',
            r'data-ad-slot="9345718962"',
        ]
        
        for pattern in old_patterns:
            if re.search(pattern, content):
                issues.append(f"❌ 구버전 광고 코드 발견: {pattern}")
        
        return issues
        
    except Exception as e:
        return [f"❌ 파일 읽기 오류: {e}"]

def main():
    """romance-test 폴더의 모든 HTML 파일 검사"""
    base_path = Path('romance-test')
    languages = ['ko', 'ja', 'en']
    
    print("🔍 Romance-test AdSense 구현 상태 전수 조사\n")
    
    total_issues = 0
    files_with_issues = []
    
    for lang in languages:
        lang_path = base_path / lang
        if not lang_path.exists():
            continue
            
        print(f"📁 {lang.upper()} 언어 폴더 검사...")
        
        # index.html과 모든 test 파일들 검사
        files_to_check = ['index.html'] + [f'test{i}.html' for i in range(1, 31)]
        
        for filename in files_to_check:
            file_path = lang_path / filename
            
            if file_path.exists():
                issues = check_adsense_in_file(file_path)
                
                if issues:
                    print(f"  📄 {filename}:")
                    for issue in issues:
                        print(f"    {issue}")
                    files_with_issues.append(f"{lang}/{filename}")
                    total_issues += len(issues)
                else:
                    print(f"  ✅ {filename}: 정상")
            else:
                print(f"  ❌ {filename}: 파일 없음")
        
        print()
    
    # 요약 보고서
    print("=" * 50)
    print("📊 검사 결과 요약")
    print("=" * 50)
    
    if total_issues == 0:
        print("🎉 모든 파일이 올바르게 구현되어 있습니다!")
    else:
        print(f"❌ 총 {total_issues}개의 이슈가 발견되었습니다.")
        print(f"🔧 수정이 필요한 파일: {len(files_with_issues)}개")
        print("\n문제가 있는 파일 목록:")
        for file in files_with_issues:
            print(f"  - {file}")

if __name__ == "__main__":
    main()
