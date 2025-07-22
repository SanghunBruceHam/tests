
#!/usr/bin/env python3
import os
import re

def validate_and_fix_js_errors():
    """romance-test 폴더의 모든 HTML 파일에서 JavaScript 구문 오류 검증 및 수정"""
    base_dir = "romance-test"
    
    if not os.path.exists(base_dir):
        print(f"❌ {base_dir} 폴더를 찾을 수 없습니다.")
        return
    
    languages = ["ko", "ja", "en"]
    total_files_fixed = 0
    errors_found = 0
    
    for lang in languages:
        lang_dir = os.path.join(base_dir, lang)
        if not os.path.exists(lang_dir):
            print(f"⚠️ {lang_dir} 폴더를 찾을 수 없습니다.")
            continue
        
        print(f"\n📁 {lang.upper()} 폴더 검증 중...")
        
        for filename in os.listdir(lang_dir):
            if filename.endswith('.html'):
                file_path = os.path.join(lang_dir, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    file_has_errors = False
                    
                    # 1. </body> 태그가 JavaScript 코드 중간에 있는지 확인
                    if '</body>' in content:
                        # </body> 태그 위치 찾기
                        body_end_pos = content.find('</body>')
                        
                        # </body> 태그 이전에 열린 <script> 태그가 있는지 확인
                        before_body = content[:body_end_pos]
                        
                        # 마지막 <script> 태그와 그 이후의 </script> 태그 확인
                        last_script_start = before_body.rfind('<script>')
                        if last_script_start != -1:
                            script_section = before_body[last_script_start:]
                            if '</script>' not in script_section:
                                file_has_errors = True
                                print(f"  ❌ {filename}: </script> 태그 누락 발견")
                                errors_found += 1
                    
                    # 2. JSON-LD 스크립트 블록 검증
                    json_ld_pattern = r'<script type="application/ld\+json">[^<]*\{[^}]*\}[^<]*(?!</script>)'
                    if re.search(json_ld_pattern, content, re.DOTALL):
                        file_has_errors = True
                        print(f"  ❌ {filename}: JSON-LD 스크립트 닫는 태그 누락")
                        errors_found += 1
                    
                    # 3. 수정 작업 수행
                    if file_has_errors:
                        # JSON-LD 스크립트 블록 수정
                        content = re.sub(
                            r'(\{[^}]*"@context"[^}]*\})\s*\n\s*(<link rel="stylesheet")',
                            r'\1\n  </script>\n\n  \2',
                            content,
                            flags=re.DOTALL
                        )
                        
                        # 일반 스크립트 블록에서 닫는 태그 누락 수정
                        content = re.sub(
                            r'(<script[^>]*>.*?function [^}]*\})\s*\n\s*(</body>)',
                            r'\1\n  </script>\n\n\2',
                            content,
                            flags=re.DOTALL
                        )
                        
                        # 중복된 </script> 태그 정리
                        content = re.sub(
                            r'</script>\s*\n\s*</script>',
                            r'</script>',
                            content,
                            flags=re.MULTILINE
                        )
                        
                        if content != original_content:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            
                            print(f"  ✅ {filename}: JavaScript 구문 오류 수정됨")
                            total_files_fixed += 1
                    else:
                        print(f"  ✅ {filename}: 구문 오류 없음")
                        
                except Exception as e:
                    print(f"  ❌ {filename}: 처리 중 오류 발생 - {e}")
    
    print(f"\n📊 검증 결과:")
    print(f"   🔍 총 {errors_found}개의 구문 오류 발견")
    print(f"   ✅ 총 {total_files_fixed}개 파일 수정")
    
    if errors_found == 0:
        print("🎉 모든 파일이 정상입니다!")
    else:
        print("⚠️ 추가 검토가 필요할 수 있습니다.")

if __name__ == "__main__":
    validate_and_fix_js_errors()
