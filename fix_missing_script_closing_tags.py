
import os
import re

def fix_missing_script_tags():
    """romance-test 폴더의 모든 HTML 파일에서 </body> 앞에 누락된 </script> 태그 추가"""
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
                    
                    # </body> 태그 바로 앞에 JavaScript 코드가 있는지 확인
                    # </body> 앞에 </script> 태그가 없고 JavaScript 코드가 있는 경우 수정
                    pattern = r'(\s*)(</body>)'
                    
                    # </body> 태그 위치 찾기
                    body_match = re.search(pattern, content)
                    if body_match:
                        body_start = body_match.start()
                        
                        # </body> 앞의 내용에서 열린 <script> 태그가 있는지 확인
                        content_before_body = content[:body_start]
                        
                        # 마지막 </script> 태그 이후에 <script> 태그가 있는지 확인
                        last_script_close = content_before_body.rfind('</script>')
                        last_script_open = content_before_body.rfind('<script>')
                        
                        # <script> 태그가 열려있고 닫히지 않은 경우
                        if last_script_open > last_script_close:
                            # </body> 앞에 </script> 추가
                            content = re.sub(r'(</body>)', r'  </script>\n</body>', content)
                            print(f"  ✅ {filename}: </script> 태그 추가됨")
                            total_files_fixed += 1
                    
                    # 파일 내용이 변경된 경우 저장
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                
                except Exception as e:
                    print(f"  ❌ {filename}: 오류 - {e}")
    
    print(f"\n✅ 총 {total_files_fixed}개 파일이 수정되었습니다.")

if __name__ == "__main__":
    fix_missing_script_tags()
