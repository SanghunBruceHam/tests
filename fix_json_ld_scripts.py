
import os
import glob
import re

def fix_json_ld_script_tags():
    """romance-test의 모든 HTML 파일에서 JSON-LD 스크립트 태그 수정"""
    base_path = 'romance-test'
    languages = ['ko', 'ja', 'en']
    
    total_fixed = 0
    
    for lang in languages:
        lang_path = os.path.join(base_path, lang)
        if not os.path.exists(lang_path):
            continue
            
        print(f"\n📁 {lang.upper()} 폴더 처리 중...")
        
        # 모든 HTML 파일 찾기
        html_files = glob.glob(os.path.join(lang_path, '*.html'))
        
        for file_path in html_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # JSON-LD 스크립트 블록에서 닫는 태그가 없는 경우 찾기
                # 패턴: JSON 객체가 끝나고 } 다음에 바로 개행이나 공백만 있고 </script>가 없는 경우
                pattern = r'(\{\s*"@context"[^}]*\})\s*(\n\s*)((?!</script>))'
                
                if re.search(pattern, content, re.DOTALL):
                    # JSON-LD 스크립트 블록을 찾아서 닫는 태그 추가
                    def replace_json_ld(match):
                        json_content = match.group(1)
                        whitespace = match.group(2)
                        return json_content + whitespace + '  </script>'
                    
                    new_content = re.sub(pattern, replace_json_ld, content, flags=re.DOTALL)
                    
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"  ✅ {os.path.basename(file_path)}: JSON-LD 스크립트 태그 수정됨")
                        total_fixed += 1
                    else:
                        print(f"  📝 {os.path.basename(file_path)}: 이미 올바름")
                else:
                    print(f"  📝 {os.path.basename(file_path)}: JSON-LD 스크립트 없음 또는 이미 올바름")
                    
            except Exception as e:
                print(f"  ❌ {os.path.basename(file_path)}: 오류 - {e}")
    
    print(f"\n✅ 총 {total_fixed}개 파일의 JSON-LD 스크립트 태그가 수정되었습니다!")

if __name__ == "__main__":
    fix_json_ld_script_tags()
