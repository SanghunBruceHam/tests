
#!/usr/bin/env python3
import os
import re

def fix_missing_script_tags():
    """romance-test 폴더의 모든 HTML 파일에서 누락된 </script> 태그 수정"""
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
                    
                    # JSON-LD 스크립트 블록에서 닫는 태그가 누락된 경우 찾기
                    # 패턴: JSON 객체가 끝나고 } 다음에 바로 CSS 링크가 오는 경우
                    pattern = r'(\{\s*"@context".*?\}\s*)\n\s*(<link rel="stylesheet")'
                    
                    if re.search(pattern, content, re.DOTALL):
                        # JSON-LD 스크립트 블록과 CSS 링크 사이에 </script> 태그 추가
                        content = re.sub(
                            pattern,
                            r'\1\n  </script>\n\n  \2',
                            content,
                            flags=re.DOTALL
                        )
                        
                        # 이미 </script>가 있는데 잘못된 형태로 있는 경우도 수정
                        content = re.sub(
                            r'(\}\s*)\n\s*</script>\s*\n\s*</script>\s*\n\s*(<link rel="stylesheet")',
                            r'\1\n  </script>\n\n  \2',
                            content,
                            flags=re.MULTILINE
                        )
                        
                        if content != original_content:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            
                            print(f"  ✅ {filename}: </script> 태그 수정됨")
                            total_files_fixed += 1
                        else:
                            print(f"  📝 {filename}: 수정 사항 없음")
                    else:
                        print(f"  📝 {filename}: JSON-LD 패턴 없음")
                        
                except Exception as e:
                    print(f"  ❌ {filename}: 오류 발생 - {e}")
    
    print(f"\n✅ 총 {total_files_fixed}개 파일이 수정되었습니다!")

if __name__ == "__main__":
    fix_missing_script_tags()
