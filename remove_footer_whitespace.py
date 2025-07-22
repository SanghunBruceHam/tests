#!/usr/bin/env python3
import os
import re
from pathlib import Path

def clean_footer_whitespace(content):
    """푸터 위의 화이트스페이스를 강력하게 제거"""
    lines = content.split('\n')
    cleaned_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # 푸터 태그를 찾았을 때
        if '<footer>' in line.lower():
            # 현재까지 추가된 라인들에서 끝의 모든 빈 줄과 공백만 있는 줄들을 제거
            while cleaned_lines and (cleaned_lines[-1].strip() == '' or cleaned_lines[-1].isspace()):
                cleaned_lines.pop()

            # </div> 태그 다음에 오는 빈 줄들도 추가로 확인해서 제거
            # 마지막 라인이 </div>로 끝나는 경우, 그 다음 빈 줄까지 제거
            if cleaned_lines and '</div>' in cleaned_lines[-1]:
                # 푸터 바로 앞에 빈 줄 없이 추가
                cleaned_lines.append(line)
            else:
                # 다른 경우에도 빈 줄 없이 추가
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

        i += 1

    # 전체 파일 끝의 불필요한 공백도 정리
    while cleaned_lines and cleaned_lines[-1].strip() == '':
        cleaned_lines.pop()

    return '\n'.join(cleaned_lines)

def remove_footer_whitespace(file_path):
    """HTML 파일에서 풋터 위의 불필요한 화이트스페이스 강력하게 제거"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        content = clean_footer_whitespace(content)

        # 파일 저장 (변경사항이 있을 때만)
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """romance-test 폴더의 모든 HTML 파일에서 풋터 위 화이트스페이스 제거"""
    base_path = Path('romance-test')
    languages = ['ko', 'ja', 'en']

    print("🧹 풋터 위 화이트스페이스 강력 제거 중...\n")

    total_processed = 0

    for lang in languages:
        lang_path = base_path / lang
        if not lang_path.exists():
            continue

        print(f"📁 {lang.upper()} 폴더 처리 중...")

        # index.html과 모든 test 파일들 처리
        files_to_process = ['index.html'] + [f'test{i}.html' for i in range(1, 31)]

        for filename in files_to_process:
            file_path = lang_path / filename

            if file_path.exists():
                if remove_footer_whitespace(file_path):
                    print(f"  ✅ {filename}: 화이트스페이스 제거됨")
                    total_processed += 1
                else:
                    print(f"  ℹ️  {filename}: 변경사항 없음")

    print(f"\n🎉 총 {total_processed}개 파일에서 화이트스페이스가 제거되었습니다!")

if __name__ == "__main__":
    main()