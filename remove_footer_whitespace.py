#!/usr/bin/env python3
import os
import re
from pathlib import Path

def remove_specific_empty_lines(file_path, target_lines):
    """특정 줄 번호들의 빈 줄을 제거"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        original_line_count = len(lines)
        removed_count = 0

        # 높은 줄 번호부터 제거 (인덱스 변화 방지)
        for line_num in sorted(target_lines, reverse=True):
            # 1-based에서 0-based로 변환
            index = line_num - 1
            if 0 <= index < len(lines):
                # 해당 줄이 빈 줄이거나 공백만 있는 경우에만 제거
                if lines[index].strip() == '':
                    lines.pop(index)
                    removed_count += 1

        if removed_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True

        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """특정 언어별 파일들에서 지정된 줄 번호의 빈 줄들을 제거"""
    base_path = Path('romance-test')

    # 각 언어별 처리할 줄 번호들
    targets = {
        'ko': [111],  # 111줄
        'ja': [112],  # 112줄  
        'en': [111],  # 111줄
    }

    print("🧹 특정 줄 번호의 빈 줄들을 제거 중...\n")

    total_processed = 0

    for lang, line_numbers in targets.items():
        lang_path = base_path / lang
        if not lang_path.exists():
            continue

        print(f"📁 {lang.upper()} 폴더 처리 중 (줄 번호: {line_numbers})...")

        # 해당 언어 폴더의 모든 HTML 파일 처리
        html_files = list(lang_path.glob('*.html'))

        for file_path in html_files:
            if remove_specific_empty_lines(file_path, line_numbers):
                print(f"  ✅ {file_path.name}: 빈 줄 제거됨")
                total_processed += 1
            else:
                print(f"  ℹ️  {file_path.name}: 변경사항 없음")

    print(f"\n🎉 총 {total_processed}개 파일에서 빈 줄이 제거되었습니다!")

if __name__ == "__main__":
    main()