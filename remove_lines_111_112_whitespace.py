
#!/usr/bin/env python3
import os
from pathlib import Path

def remove_whitespace_from_specific_lines():
    """Remove whitespace from lines 111 and 112 in all test HTML files"""
    base_dir = "romance-test"
    languages = ["ko", "ja", "en"]
    
    print("🎯 Targeting lines 111 and 112 for whitespace removal...\n")
    
    total_fixes = 0
    
    for lang in languages:
        lang_dir = os.path.join(base_dir, lang)
        if not os.path.exists(lang_dir):
            continue
            
        print(f"📁 Processing {lang.upper()} files...")
        
        # Process all test files
        for i in range(1, 31):
            test_file = f"test{i}.html"
            file_path = os.path.join(lang_dir, test_file)
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    original_lines = lines[:]
                    modified = False
                    
                    # Check and fix line 111 (index 110)
                    if len(lines) > 110:
                        if lines[110].strip() == '' and lines[110] != '\n':
                            lines[110] = '\n'
                            modified = True
                            print(f"  ✅ {test_file}: Fixed line 111")
                    
                    # Check and fix line 112 (index 111) 
                    if len(lines) > 111:
                        if lines[111].strip() == '' and lines[111] != '\n':
                            lines[111] = '\n'
                            modified = True
                            print(f"  ✅ {test_file}: Fixed line 112")
                    
                    # Remove completely empty lines 111 and 112 if they exist
                    if len(lines) > 110 and lines[110].strip() == '':
                        if len(lines) > 111 and lines[111].strip() == '':
                            # Remove both lines if they're both empty
                            lines = lines[:110] + lines[112:]
                            modified = True
                            print(f"  🗑️ {test_file}: Removed empty lines 111-112")
                        else:
                            # Remove just line 111
                            lines = lines[:110] + lines[111:]
                            modified = True
                            print(f"  🗑️ {test_file}: Removed empty line 111")
                    elif len(lines) > 111 and lines[111].strip() == '':
                        # Remove just line 112
                        lines = lines[:111] + lines[112:]
                        modified = True
                        print(f"  🗑️ {test_file}: Removed empty line 112")
                    
                    if modified:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(lines)
                        total_fixes += 1
                    else:
                        print(f"  ℹ️ {test_file}: No whitespace issues on lines 111-112")
                        
                except Exception as e:
                    print(f"  ❌ Error processing {test_file}: {e}")
    
    print(f"\n🎉 Fixed {total_fixes} files total!")

if __name__ == "__main__":
    remove_whitespace_from_specific_lines()
