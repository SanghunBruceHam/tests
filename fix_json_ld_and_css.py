
#!/usr/bin/env python3
import os
import re

def fix_json_ld_and_css():
    """romance-test 폴더의 모든 HTML 파일에서 JSON-LD와 CSS 링크 문제 수정"""
    base_dir = "romance-test"
    
    if not os.path.exists(base_dir):
        print(f"❌ {base_dir} 폴더를 찾을 수 없습니다.")
        return
    
    languages = ["ko", "ja", "en"]
    total_files_fixed = 0
    
    for lang in languages:
        lang_dir = os.path.join(base_dir, lang)
        if not os.path.exists(lang_dir):
            print(f"⚠️ {lang_dir} 폴더를 찾을 수 없습니다.")
            continue
        
        print(f"\n📁 {lang.upper()} 폴더 처리 중...")
        
        for filename in os.listdir(lang_dir):
            if filename.endswith('.html'):
                file_path = os.path.join(lang_dir, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # 1. JSON-LD 스크립트의 잘못된 닫는 태그 수정
                    # }로 끝나고 바로 </script>가 없는 경우 수정
                    content = re.sub(
                        r'(\s*}\s*)\n\s*</script>\s*\n\s*\n\s*<link rel="stylesheet"',
                        r'\1\n  </script>\n\n  <link rel="stylesheet"',
                        content,
                        flags=re.MULTILINE
                    )
                    
                    # 2. CSS 링크 앞의 잘못된 </script> 태그 제거
                    content = re.sub(
                        r'</script>\s*\n\s*<link rel="stylesheet" href="\.?/?style\.css">',
                        r'<link rel="stylesheet" href="./style.css">',
                        content,
                        flags=re.MULTILINE
                    )
                    
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"  ✅ {filename}: JSON-LD 및 CSS 링크 수정됨")
                        total_files_fixed += 1
                    else:
                        print(f"  📝 {filename}: 수정 사항 없음")
                        
                except Exception as e:
                    print(f"  ❌ {filename}: 오류 발생 - {e}")
    
    print(f"\n✅ 총 {total_files_fixed}개 파일이 수정되었습니다!")

if __name__ == "__main__":
    fix_json_ld_and_css()
