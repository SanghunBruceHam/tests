#!/usr/bin/env python3
"""
SEO Issues Fixer - Fix critical SEO problems across the project
"""
import re
from pathlib import Path
import json

# Meta descriptions for romance test files
ROMANCE_META_DESCRIPTIONS = {
    'test1': '바닐라 아이스크림 토핑 선택으로 알아보는 당신의 숨겨진 연애 성향! 달콤한 선택이 말해주는 사랑의 비밀을 30초 만에 확인해보세요.',
    'test2': '급한 외출 시 꼭 챙기는 아이템으로 드러나는 당신의 연애 행동 패턴! 무의식 속 선택에 숨어있는 사랑의 우선순위를 발견하세요.',
    'test3': '혼자만의 주말 시간 활용법에서 보이는 당신이 연인에게 감추고 싶은 모습! 진짜 자신의 연애 스타일을 솔직하게 알아보세요.',
    'test4': '공원에서 시선을 끄는 첫 번째 풍경이 말해주는 당신만의 특별한 연애 스타일! 무의식적 선택이 드러내는 사랑의 패턴을 확인하세요.',
    'test5': '카페 음료 선택으로 알아보는 당신의 이상적인 데이트 스타일과 연애 가치관! 작은 취향이 보여주는 큰 사랑의 그림을 발견해보세요.',
    'test6': '영화관 데이트에서의 행동으로 드러나는 당신의 스킨십 성향과 애정 표현 방식! 연인과의 친밀감에 대한 진실을 솔직하게 알아보세요.',
    'test7': '연인과의 데이트에서 가장 중시하는 것으로 보이는 당신의 연애 우선순위! 사랑에서 진짜 중요하게 여기는 가치가 무엇인지 확인하세요.',
    'test8': '이상적인 데이트 코스 선택이 말해주는 당신의 연애 우선순위와 사랑 철학! 로맨틱한 상상 속에 숨어있는 진짜 마음을 찾아보세요.',
    'test9': '힘든 순간 대처 방식으로 알아보는 당신의 애교와 의존성 지수! 연인에게 얼마나 잘 의지하고 사랑받는 타입인지 확인해보세요.',
    'test10': '연인의 늦은 약속에 대한 반응으로 보이는 당신의 연애 일관성과 감정 관리 능력! 사랑 속에서의 진짜 성격을 정확히 분석해보세요.',
    'test11': '예상치 못한 상황에서의 선택으로 드러나는 당신의 연애 스타일! 갑작스러운 순간에 보이는 진짜 마음과 사랑의 본능을 발견하세요.',
    'test12': '소중한 물건 분실 상황에서의 반응으로 알아보는 당신의 연애 집착도! 사랑하는 사람과 추억에 대한 진짜 마음의 깊이를 측정해보세요.',
    'test13': '새로운 취미 선택으로 보이는 당신의 연애 호기심과 관계 발전 의욕! 사랑을 더욱 풍성하게 만드는 당신만의 특별한 방식을 알아보세요.',
    'test14': '친구와의 갈등 상황 대처법으로 드러나는 당신의 연애 갈등 해결 능력! 사랑하는 사람과의 문제를 얼마나 현명하게 풀어나가는지 확인하세요.',
    'test15': '스트레스 해소 방법으로 알아보는 당신의 연애 안정감 추구 성향! 연인과 함께 평화로운 관계를 만들어가는 당신만의 비법을 찾아보세요.',
    'test16': '색깔 선택으로 보이는 당신의 연애 감정 표현 방식과 사랑의 색깔! 마음 속 깊이 숨어있는 로맨틱한 감성과 애정의 스타일을 발견하세요.',
    'test17': '계절별 데이트 선호도로 알아보는 당신의 연애 무드와 로맨틱 감성! 사계절 사랑 이야기 속에서 당신만의 특별한 연애 스타일을 찾아보세요.',
    'test18': '음식 선택으로 드러나는 당신의 연애 만족도와 행복 추구 방식! 미각이 말해주는 사랑의 취향과 관계에서 원하는 달콤함을 알아보세요.',
    'test19': '여행지 선택으로 보이는 당신의 연애 모험심과 관계 확장 의지! 사랑하는 사람과 함께 만들고 싶은 추억의 스타일과 꿈을 확인해보세요.',
    'test20': '선물 선택으로 알아보는 당신의 연애 헌신도와 사랑 표현 방식! 마음을 전하는 특별한 방법과 연인에 대한 진정한 마음의 크기를 측정하세요.',
    'test21': '시간 활용 방식으로 드러나는 당신의 연애 균형감과 관계 우선순위! 바쁜 일상 속에서도 사랑을 소중히 지켜나가는 당신만의 방법을 찾아보세요.',
    'test22': '소통 방식 선택으로 보이는 당신의 연애 친밀감 형성 능력! 연인과의 깊은 교감을 만들어가는 특별한 대화법과 마음 나누기 스타일을 알아보세요.',
    'test23': '위기 상황 대처법으로 알아보는 당신의 연애 보호본능과 사랑의 책임감! 소중한 사람을 지키기 위한 당신의 진짜 마음과 행동력을 확인하세요.',
    'test24': '취향 변화에 대한 반응으로 드러나는 당신의 연애 포용력과 적응 능력! 서로 다른 면을 받아들이며 함께 성장하는 사랑의 지혜를 측정해보세요.',
    'test25': '추억 간직 방식으로 보이는 당신의 연애 소중함 인식도와 기억 보관법! 사랑하는 순간들을 얼마나 특별하게 간직하고 있는지 확인해보세요.',
    'test26': '갑작스러운 변화 상황에서의 반응으로 알아보는 당신의 연애 유연성! 예상치 못한 순간에도 사랑을 지켜나가는 마음의 강인함을 측정하세요.',
    'test27': '선택의 기준으로 드러나는 당신의 연애 가치관과 사랑의 우선순위! 인생의 중요한 결정 순간에 보이는 진정한 마음의 방향을 발견해보세요.',
    'test28': '감정 표현 방식으로 보이는 당신의 연애 솔직함과 마음 전달 능력! 사랑하는 마음을 얼마나 진실하고 아름답게 표현하는지 확인해보세요.',
    'test29': '중요한 결정 상황에서의 판단력으로 알아보는 당신의 연애 결단력! 사랑을 위한 선택의 순간에 보이는 마음의 확신과 용기를 측정해보세요.',
    'test30': '이상적인 연애 장면 선택으로 드러나는 당신의 꿈꾸는 사랑 스타일! 마음 속 깊이 간직한 로맨틱한 이상향과 진정 원하는 연애를 발견하세요.'
}

def add_meta_description(file_path, content, description):
    """Add meta description to HTML content"""
    # Check if meta description already exists
    if re.search(r'<meta[^>]*name=["\']description["\']', content, re.IGNORECASE):
        return content, False  # Already has meta description
    
    # Find the position to insert (after charset or viewport, before title)
    insert_patterns = [
        r'(<meta[^>]*name=["\']viewport["\'][^>]*>)',
        r'(<meta[^>]*charset[^>]*>)',
        r'(<title[^>]*>)'
    ]
    
    for pattern in insert_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            meta_tag = f'<meta content="{description}" name="description"/>'
            insertion_point = match.end()
            new_content = content[:insertion_point] + f'\n{meta_tag}' + content[insertion_point:]
            return new_content, True
    
    return content, False

def fix_romance_test_meta_descriptions():
    """Fix missing meta descriptions in romance test files"""
    base_dir = Path("/Users/sanghunbruceham/Documents/GitHub/tests/romance-test")
    fixed_count = 0
    
    for lang in ['en', 'ja', 'ko']:
        lang_dir = base_dir / lang
        if not lang_dir.exists():
            continue
            
        for test_num in range(1, 31):
            test_file = lang_dir / f"test{test_num}.html"
            if not test_file.exists():
                continue
                
            try:
                content = test_file.read_text(encoding='utf-8')
                
                # Skip if already has meta description
                if re.search(r'<meta[^>]*name=["\']description["\']', content, re.IGNORECASE):
                    continue
                
                # Get appropriate description
                test_key = f'test{test_num}'
                if test_key in ROMANCE_META_DESCRIPTIONS:
                    if lang == 'ja':
                        # For Japanese, use a generic but appropriate description
                        description = f"恋愛心理テスト{test_num}番：あなたの恋愛傾向を30秒で診断！心理学に基づいた分析で、隠れた恋愛スタイルと相性パターンを無料で発見できます。"
                    elif lang == 'en':
                        # For English, use a generic but appropriate description  
                        description = f"Romance Psychology Test {test_num}: Discover your hidden love style in 30 seconds! Free analysis based on psychology reveals your dating patterns and compatibility insights."
                    else:  # Korean
                        description = ROMANCE_META_DESCRIPTIONS[test_key]
                    
                    new_content, was_added = add_meta_description(test_file, content, description)
                    if was_added:
                        test_file.write_text(new_content, encoding='utf-8')
                        fixed_count += 1
                        print(f"✅ Added meta description to {test_file.name} ({lang})")
                        
            except Exception as e:
                print(f"❌ Error processing {test_file}: {e}")
    
    return fixed_count

def fix_title_lengths():
    """Fix titles that are too long (>60 chars)"""
    base_dir = Path("/Users/sanghunbruceham/Documents/GitHub/tests")
    
    # Title optimizations for specific files
    title_fixes = {
        'romance-test/ja/test3.html': '恋愛心理テスト 3: 숨겨진 모습 | 무료 연애 성향 진단',
        'romance-test/ja/test6.html': '恋愛心理테스ト 6: 스킨십 성향 | 무료 애정표현 진단', 
        'romance-test/en/test1.html': 'Romance Test 1: Ice Cream Topping Choice Analysis',
        'anime-personality/en/index.html': 'Anime Personality Test: Discover Your Anime Character Match',
        'egen-teto/en/index.html': 'EGEN TETO: Advanced AI Music Generation Platform'
    }
    
    fixed_count = 0
    for relative_path, new_title in title_fixes.items():
        file_path = base_dir / relative_path
        if not file_path.exists():
            continue
            
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Replace title
            title_pattern = r'<title[^>]*>(.*?)</title>'
            match = re.search(title_pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                old_title = match.group(1).strip()
                if len(old_title) > 60:  # Only fix if actually too long
                    new_content = re.sub(title_pattern, f'<title>{new_title}</title>', content, flags=re.IGNORECASE | re.DOTALL)
                    file_path.write_text(new_content, encoding='utf-8')
                    fixed_count += 1
                    print(f"✅ Fixed title length: {file_path.name}")
                    
        except Exception as e:
            print(f"❌ Error fixing title in {file_path}: {e}")
    
    return fixed_count

def add_twitter_cards():
    """Add missing Twitter Card tags to files that need them"""
    base_dir = Path("/Users/sanghunbruceham/Documents/GitHub/tests")
    
    # Files that need Twitter Card tags
    files_needing_twitter = [
        'anime-personality/en/index.html',
        'anime-personality/ko/index.html', 
        'anime-personality/ja/index.html',
        'egen-teto/ja/about.html',
        'egen-teto/ko/about.html',
        'egen-teto/ko/index.html',
        'egen-teto/en/index.html'
    ]
    
    fixed_count = 0
    for relative_path in files_needing_twitter:
        file_path = base_dir / relative_path
        if not file_path.exists():
            continue
            
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check if Twitter cards already exist
            if re.search(r'name=["\']twitter:card["\']', content, re.IGNORECASE):
                continue
                
            # Get existing title and description for Twitter cards
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
            og_image_match = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
            
            if title_match:
                title = title_match.group(1).strip()
                description = desc_match.group(1).strip() if desc_match else title
                image_url = og_image_match.group(1) if og_image_match else "https://tests.mahalohana-bruce.com/favicon.png"
                
                # Create Twitter Card tags
                twitter_tags = f'''<meta content="summary_large_image" name="twitter:card"/>
<meta content="{title}" name="twitter:title"/>
<meta content="{description}" name="twitter:description"/>
<meta content="{image_url}" name="twitter:image"/>
<meta content="@tests_mahalohana" name="twitter:site"/>
<meta content="@mahalohana_bruce" name="twitter:creator"/>'''
                
                # Insert after existing meta tags
                insertion_pattern = r'(<meta[^>]*name=["\']twitter:creator["\'][^>]*>|<link[^>]*rel=["\']canonical["\'][^>]*>)'
                if not re.search(insertion_pattern, content):
                    # Find a good insertion point
                    insertion_patterns = [
                        r'(<meta[^>]*property=["\']og:creator["\'][^>]*>)',
                        r'(<meta[^>]*property=["\']og:site_name["\'][^>]*>)',
                        r'(<link[^>]*rel=["\']canonical["\'][^>]*>)'
                    ]
                    
                    for pattern in insertion_patterns:
                        match = re.search(pattern, content, re.IGNORECASE)
                        if match:
                            insertion_point = match.end()
                            new_content = content[:insertion_point] + f'\n{twitter_tags}' + content[insertion_point:]
                            file_path.write_text(new_content, encoding='utf-8')
                            fixed_count += 1
                            print(f"✅ Added Twitter Card tags to {file_path.name}")
                            break
                            
        except Exception as e:
            print(f"❌ Error adding Twitter cards to {file_path}: {e}")
    
    return fixed_count

def fix_anime_personality_utility_files():
    """Fix basic HTML structure in anime personality utility files"""
    base_dir = Path("/Users/sanghunbruceham/Documents/GitHub/tests/anime-personality")
    
    utility_files = [
        'create_favicon.html',
        'generate_all_images.html',
        'ko/create_thumbnail.html', 
        'ja/create_thumbnail.html'
    ]
    
    fixed_count = 0
    for relative_path in utility_files:
        file_path = base_dir / relative_path
        if not file_path.exists():
            continue
            
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Add missing lang attribute
            if not re.search(r'<html[^>]*lang=', content, re.IGNORECASE):
                content = re.sub(r'<html([^>]*)>', r'<html\1 lang="en">', content, flags=re.IGNORECASE)
            
            # Add missing meta description if needed
            if not re.search(r'<meta[^>]*name=["\']description["\']', content, re.IGNORECASE):
                desc = "Utility tool for anime personality test content generation and image processing."
                meta_tag = f'<meta content="{desc}" name="description"/>'
                
                # Insert after title or head opening
                title_match = re.search(r'(<title[^>]*>.*?</title>)', content, re.IGNORECASE | re.DOTALL)
                if title_match:
                    insertion_point = title_match.end()
                    content = content[:insertion_point] + f'\n{meta_tag}' + content[insertion_point:]
            
            # Add viewport if missing
            if not re.search(r'<meta[^>]*name=["\']viewport["\']', content, re.IGNORECASE):
                viewport_tag = '<meta content="width=device-width, initial-scale=1.0" name="viewport"/>'
                title_match = re.search(r'(<title[^>]*>.*?</title>)', content, re.IGNORECASE | re.DOTALL)
                if title_match:
                    insertion_point = title_match.end()
                    content = content[:insertion_point] + f'\n{viewport_tag}' + content[insertion_point:]
            
            file_path.write_text(content, encoding='utf-8')
            fixed_count += 1
            print(f"✅ Fixed basic HTML structure in {file_path.name}")
            
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
    
    return fixed_count

def main():
    """Main SEO fixing function"""
    print("🔧 Starting SEO Issues Fix...")
    print("=" * 50)
    
    # 1. Fix romance test meta descriptions
    print("📝 Fixing romance test meta descriptions...")
    romance_fixed = fix_romance_test_meta_descriptions()
    print(f"Fixed {romance_fixed} romance test files\n")
    
    # 2. Fix title lengths
    print("✂️ Fixing title lengths...")
    titles_fixed = fix_title_lengths()
    print(f"Fixed {titles_fixed} title lengths\n")
    
    # 3. Add Twitter Card tags
    print("🐦 Adding Twitter Card tags...")
    twitter_fixed = add_twitter_cards()
    print(f"Added Twitter cards to {twitter_fixed} files\n")
    
    # 4. Fix anime personality utility files
    print("🔧 Fixing anime personality utility files...")
    anime_fixed = fix_anime_personality_utility_files()
    print(f"Fixed {anime_fixed} utility files\n")
    
    print("=" * 50)
    print(f"✅ SEO Fix Complete!")
    print(f"Total improvements: {romance_fixed + titles_fixed + twitter_fixed + anime_fixed}")
    print(f"- Meta descriptions: {romance_fixed}")
    print(f"- Title optimizations: {titles_fixed}")
    print(f"- Twitter cards: {twitter_fixed}")
    print(f"- HTML structure fixes: {anime_fixed}")

if __name__ == "__main__":
    main()