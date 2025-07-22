
#!/usr/bin/env python3
import os
import re

def fix_css_scripts():
    """romance-test 폴더의 모든 HTML 파일에서 CSS 링크 위에 </script> 태그 추가"""
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
                    
                    # CSS 링크 패턴 찾기 (./style.css 또는 style.css)
                    css_pattern = r'(\s*)<link rel="stylesheet" href="(?:\./)?style\.css"'
                    
                    if re.search(css_pattern, content):
                        # CSS 링크 위에 </script> 태그가 없는 경우에만 추가
                        if not re.search(r'</script>\s*<link rel="stylesheet" href="(?:\./)?style\.css"', content):
                            # CSS 링크 앞에 </script> 추가
                            content = re.sub(
                                css_pattern,
                                r'\1</script>\n\1<link rel="stylesheet" href="./style.css"',
                                content
                            )
                            
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            
                            print(f"  ✅ {filename}: </script> 태그 추가됨")
                            total_files_fixed += 1
                        else:
                            print(f"  📝 {filename}: 이미 </script> 태그가 있음")
                    else:
                        print(f"  📝 {filename}: CSS 링크 없음")
                        
                except Exception as e:
                    print(f"  ❌ {filename}: 오류 발생 - {e}")
    
    print(f"\n✅ 총 {total_files_fixed}개 파일이 수정되었습니다!")

if __name__ == "__main__":
    fix_css_scripts()
