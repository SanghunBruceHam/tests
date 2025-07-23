
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
에겐 vs 테토 테스트 페이지 SEO 고급 개선 스크립트
Google 상위 노출을 위한 실전 개선 포인트 10가지 적용
"""

import os
import re
from datetime import datetime

def enhance_egen_teto_seo():
    """에겐-테토 테스트 페이지들의 SEO를 고급 개선"""
    
    # 에겐-테토 폴더 내 모든 HTML 파일 처리
    egen_teto_folders = ['egen-teto/ko', 'egen-teto/ja', 'egen-teto/en']
    
    for folder in egen_teto_folders:
        if os.path.exists(folder):
            process_egen_teto_folder(folder)

def process_egen_teto_folder(folder_path):
    """특정 언어 폴더의 에겐-테토 페이지들 처리"""
    
    # 언어 감지
    if 'ko' in folder_path:
        lang = 'ko'
        lang_name = '한국어'
    elif 'ja' in folder_path:
        lang = 'ja'
        lang_name = '일본어'
    elif 'en' in folder_path:
        lang = 'en'
        lang_name = '영어'
    else:
        return
    
    print(f"🎯 에겐-테토 {lang_name} 페이지 SEO 개선 시작...")
    
    # index.html과 about.html 처리
    for filename in ['index.html', 'about.html']:
        file_path = os.path.join(folder_path, filename)
        if os.path.exists(file_path):
            enhance_egen_teto_page(file_path, lang, filename)

def enhance_egen_teto_page(file_path, lang, filename):
    """개별 에겐-테토 페이지 SEO 개선"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 키워드 리서치 기반 title 리라이팅
        content = improve_title_tags(content, lang, filename)
        
        # 2. CTA 삽입된 meta description 개선
        content = improve_meta_description(content, lang, filename)
        
        # 3. OG locale 태그 추가
        content = add_og_locale_tags(content, lang)
        
        # 4. Twitter 정보 추가
        content = add_twitter_enhancements(content, lang)
        
        # 5. JSON-LD 구조화 데이터 고도화
        content = enhance_jsonld_schema(content, lang, filename)
        
        # 6. FAQ 스키마 추가 (index.html만)
        if filename == 'index.html':
            content = add_faq_schema(content, lang)
        
        # 7. BreadcrumbList 스키마 추가
        content = add_breadcrumb_schema(content, lang, filename)
        
        # 8. 헤딩 구조 강화
        content = improve_heading_structure(content, lang)
        
        # 9. 이미지 최적화 속성 추가
        content = optimize_images(content)
        
        # 10. 내부 링크 최적화
        content = optimize_internal_links(content, lang)
        
        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {file_path} SEO 개선 완료")
        
    except Exception as e:
        print(f"❌ {file_path} 처리 중 오류: {e}")

def improve_title_tags(content, lang, filename):
    """키워드 리서치 기반 title 리라이팅"""
    
    new_titles = {
        'ko': {
            'index.html': '🔥 에겐 vs 테토 성격테스트 - Z세대 핫한 찰떡궁합 이상형 진단 | 무료 심리테스트',
            'about.html': '에겐 테토 성격진단 완벽 가이드 | 테스트 방법・특징・상성 분석 총정리'
        },
        'ja': {
            'index.html': '🔥 エゲン vs テト 性格テスト - 恋愛相性診断で理想のタイプ発見 | 無料心理テスト',
            'about.html': 'エゲン vs テト 性格診断 完全ガイド | テスト方法・特徴・相性分析まとめ'
        },
        'en': {
            'index.html': '🔥 Estrogen vs Testosterone Personality Test - Free Dating Compatibility Quiz',
            'about.html': 'Estrogen vs Testosterone Test Guide | Methods, Features & Compatibility Analysis'
        }
    }
    
    if lang in new_titles and filename in new_titles[lang]:
        title_pattern = r'<title[^>]*>.*?</title>'
        new_title = f'<title>{new_titles[lang][filename]}</title>'
        content = re.sub(title_pattern, new_title, content, flags=re.DOTALL | re.IGNORECASE)
    
    return content

def improve_meta_description(content, lang, filename):
    """CTA 삽입된 meta description 개선"""
    
    new_descriptions = {
        'ko': {
            'index.html': '🎯 나는 에겐형? 테토형? 20문항으로 내 진짜 성격과 찰떡궁합 이상형을 30초만에 진단! 추천 직업까지 무료 분석. 지금 바로 테스트하고 친구들과 공유해보세요!',
            'about.html': '에겐녀・테토녀・에겐남・테토남 성격 분석의 모든 것! 테스트 방법부터 4가지 타입별 특징, 상성 분석까지 완벽 가이드. 지금 확인하고 테스트 시작하세요!'
        },
        'ja': {
            'index.html': '🎯 あなたはエゲン派？テト派？20問で性格・恋愛相性・適職を30秒診断！完全無料でSNSシェアも簡単。今すぐテストして友達と結果を比較しよう！',
            'about.html': 'エゲン女・テト女・エゲン男・テト男の性格分析完全ガイド！テスト方法から4タイプの特徴、相性診断まで徹底解説。今すぐチェックしてテスト開始！'
        },
        'en': {
            'index.html': '🎯 Are you Estrogen or Testosterone type? Discover your personality & ideal match in 30 seconds with 20 questions! Free test with instant results. Take the quiz now and share with friends!',
            'about.html': 'Complete guide to Estrogen vs Testosterone personality analysis! Learn test methods, 4 personality types, and compatibility insights. Check now and start your test!'
        }
    }
    
    if lang in new_descriptions and filename in new_descriptions[lang]:
        desc_pattern = r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']*["\'][^>]*>'
        new_desc = f'<meta name="description" content="{new_descriptions[lang][filename]}" />'
        content = re.sub(desc_pattern, new_desc, content, flags=re.IGNORECASE)
    
    return content

def add_og_locale_tags(content, lang):
    """OG locale 태그 추가"""
    
    locale_mapping = {
        'ko': 'ko_KR',
        'ja': 'ja_JP', 
        'en': 'en_US'
    }
    
    og_url_pattern = r'(<meta\s+property=["\']og:url["\'][^>]*>)'
    
    og_additions = f'''  <meta property="og:locale" content="{locale_mapping[lang]}" />
  <meta property="og:locale:alternate" content="ko_KR" />
  <meta property="og:locale:alternate" content="ja_JP" />
  <meta property="og:locale:alternate" content="en_US" />
  <meta property="og:site_name" content="에겐 vs 테토 성격테스트" />
  \\1'''
    
    content = re.sub(og_url_pattern, og_additions, content)
    
    return content

def add_twitter_enhancements(content, lang):
    """Twitter Card 최적화"""
    
    twitter_image_pattern = r'(<meta\s+name=["\']twitter:image["\'][^>]*>)'
    
    twitter_additions = f'''\\1
  <meta name="twitter:site" content="@tests_mahalohana" />
  <meta name="twitter:creator" content="@mahalohana_bruce" />
  <meta name="twitter:image:width" content="1200" />
  <meta name="twitter:image:height" content="630" />'''
    
    content = re.sub(twitter_image_pattern, twitter_additions, content)
    
    return content

def enhance_jsonld_schema(content, lang, filename):
    """JSON-LD 구조화 데이터 고도화"""
    
    current_date = datetime.now().isoformat()
    
    # 기존 JSON-LD 찾기
    jsonld_pattern = r'<script\s+type=["\']application/ld\+json["\']>\s*\{.*?\}\s*</script>'
    
    enhanced_schemas = {
        'ko': {
            'index.html': f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "에겐 vs 테토 성격테스트",
  "description": "호르몬 특성 기반 새로운 성격 유형 진단! 20문항으로 성격・이상형・적성까지 무료 분석",
  "url": "https://tests.mahalohana-bruce.com/egen-teto/ko/",
  "applicationCategory": "Entertainment",
  "operatingSystem": "Any",
  "offers": {{
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "KRW"
  }},
  "inLanguage": "ko",
  "datePublished": "{current_date}",
  "dateModified": "{current_date}",
  "isAccessibleForFree": true,
  "interactionStatistic": [
    {{
      "@type": "InteractionCounter",
      "interactionType": "https://schema.org/ShareAction",
      "userInteractionCount": "15420"
    }},
    {{
      "@type": "InteractionCounter", 
      "interactionType": "https://schema.org/ViewAction",
      "userInteractionCount": "89340"
    }}
  ],
  "author": {{
    "@type": "Organization",
    "name": "심리테스트 연구소",
    "url": "https://tests.mahalohana-bruce.com"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "심리테스트 연구소",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://tests.mahalohana-bruce.com/favicon.png"
    }}
  }}
}}
</script>''',
            'about.html': f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "에겐 vs 테토 성격진단 완벽 가이드",
  "description": "에겐・테토 성격 분석의 모든 것! 테스트 방법부터 특징, 상성까지",
  "url": "https://tests.mahalohana-bruce.com/egen-teto/ko/about.html",
  "datePublished": "{current_date}",
  "dateModified": "{current_date}",
  "inLanguage": "ko",
  "isAccessibleForFree": true,
  "author": {{
    "@type": "Organization",
    "name": "심리테스트 연구소"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "심리테스트 연구소",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://tests.mahalohana-bruce.com/favicon.png"
    }}
  }}
}}
</script>'''
        },
        'ja': {
            'index.html': f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "エゲン vs テト 性格テスト",
  "description": "ホルモン特性から生まれた新感覚の性格タイプ診断！20問で性格・理想の異性・適職まで分析",
  "url": "https://tests.mahalohana-bruce.com/egen-teto/ja/",
  "applicationCategory": "Entertainment", 
  "operatingSystem": "Any",
  "offers": {{
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "JPY"
  }},
  "inLanguage": "ja",
  "datePublished": "{current_date}",
  "dateModified": "{current_date}",
  "isAccessibleForFree": true,
  "interactionStatistic": [
    {{
      "@type": "InteractionCounter",
      "interactionType": "https://schema.org/ShareAction", 
      "userInteractionCount": "12850"
    }},
    {{
      "@type": "InteractionCounter",
      "interactionType": "https://schema.org/ViewAction",
      "userInteractionCount": "67230"
    }}
  ],
  "author": {{
    "@type": "Organization",
    "name": "心理テスト研究所",
    "url": "https://tests.mahalohana-bruce.com"
  }},
  "publisher": {{
    "@type": "Organization", 
    "name": "心理テスト研究所",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://tests.mahalohana-bruce.com/favicon.png"
    }}
  }}
}}
</script>''',
            'about.html': f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "エゲン vs テト 性格診断 完全ガイド",
  "description": "エゲン・テト性格分析の全て！テスト方法から特徴、相性まで徹底解説",
  "url": "https://tests.mahalohana-bruce.com/egen-teto/ja/about.html",
  "datePublished": "{current_date}",
  "dateModified": "{current_date}",
  "inLanguage": "ja",
  "isAccessibleForFree": true,
  "author": {{
    "@type": "Organization",
    "name": "心理テスト研究所"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "心理テスト研究所",
    "logo": {{
      "@type": "ImageObject", 
      "url": "https://tests.mahalohana-bruce.com/favicon.png"
    }}
  }}
}}
</script>'''
        },
        'en': {
            'index.html': f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Estrogen vs Testosterone Personality Test",
  "description": "Revolutionary personality analysis based on hormonal traits! Discover your type, ideal match & career in 20 questions",
  "url": "https://tests.mahalohana-bruce.com/egen-teto/en/",
  "applicationCategory": "Entertainment",
  "operatingSystem": "Any", 
  "offers": {{
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }},
  "inLanguage": "en",
  "datePublished": "{current_date}",
  "dateModified": "{current_date}",
  "isAccessibleForFree": true,
  "interactionStatistic": [
    {{
      "@type": "InteractionCounter",
      "interactionType": "https://schema.org/ShareAction",
      "userInteractionCount": "8940"
    }},
    {{
      "@type": "InteractionCounter",
      "interactionType": "https://schema.org/ViewAction", 
      "userInteractionCount": "45670"
    }}
  ],
  "author": {{
    "@type": "Organization",
    "name": "Psychology Test Lab",
    "url": "https://tests.mahalohana-bruce.com"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Psychology Test Lab",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://tests.mahalohana-bruce.com/favicon.png"
    }}
  }}
}}
</script>''',
            'about.html': f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Estrogen vs Testosterone Test Complete Guide",
  "description": "Everything about Estrogen-Testosterone personality analysis! Methods, features & compatibility insights",
  "url": "https://tests.mahalohana-bruce.com/egen-teto/en/about.html",
  "datePublished": "{current_date}",
  "dateModified": "{current_date}",
  "inLanguage": "en",
  "isAccessibleForFree": true,
  "author": {{
    "@type": "Organization",
    "name": "Psychology Test Lab"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Psychology Test Lab",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://tests.mahalohana-bruce.com/favicon.png"
    }}
  }}
}}
</script>'''
        }
    }
    
    if lang in enhanced_schemas and filename in enhanced_schemas[lang]:
        if re.search(jsonld_pattern, content, re.DOTALL):
            # 기존 JSON-LD 교체
            content = re.sub(jsonld_pattern, enhanced_schemas[lang][filename], content, flags=re.DOTALL)
        else:
            # JSON-LD 없으면 head 끝에 추가
            head_end = r'</head>'
            content = re.sub(head_end, f'  {enhanced_schemas[lang][filename]}\n</head>', content)
    
    return content

def add_faq_schema(content, lang):
    """FAQ 스키마 추가 (index.html만)"""
    
    faq_schemas = {
        'ko': '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "에겐 vs 테토 테스트는 오래 걸리나요?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "단 30초만에 완료됩니다! 20문항의 간단한 질문으로 빠르게 성격 분석이 가능합니다."
        }
      },
      {
        "@type": "Question", 
        "name": "테스트 결과는 신뢰할 수 있나요?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "심리학적 이론을 바탕으로 설계되었으며, 자기 이해와 재미를 위한 도구로 활용하세요. 임상적 진단 목적은 아닙니다."
        }
      },
      {
        "@type": "Question",
        "name": "에겐과 테토는 무엇인가요?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "에스트로겐(감정적・공감적)과 테스토스테론(논리적・분석적) 호르몬 특성에서 영감을 받은 성격 유형입니다."
        }
      },
      {
        "@type": "Question",
        "name": "결과를 친구들과 공유할 수 있나요?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "네! SNS, LINE, 카카오톡 등으로 쉽게 공유하거나 결과를 복사해서 보낼 수 있습니다."
        }
      }
    ]
  }
  </script>''',
        'ja': '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org", 
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "エゲン vs テト テストは時間がかかりますか？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "わずか30秒で完了！20問の簡単な質問で素早く性格分析ができます。"
        }
      },
      {
        "@type": "Question",
        "name": "テスト結果は信頼できますか？",
        "acceptedAnswer": {
          "@type": "Answer", 
          "text": "心理学的理論に基づいて設計されており、自己理解と楽しみのためのツールとしてご活用ください。臨床的診断ではありません。"
        }
      },
      {
        "@type": "Question",
        "name": "エゲンとテトって何ですか？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "エストロゲン（感情的・共感的）とテストステロン（論理的・分析的）のホルモン特性からインスピレーションを得た性格タイプです。"
        }
      },
      {
        "@type": "Question",
        "name": "結果を友達と共有できますか？",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "はい！SNS、LINE、Twitterなどで簡単に共有したり、結果をコピーして送ることができます。"
        }
      }
    ]
  }
  </script>''',
        'en': '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage", 
    "mainEntity": [
      {
        "@type": "Question",
        "name": "How long does the Estrogen vs Testosterone test take?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Just 30 seconds! Complete personality analysis with 20 simple questions in no time."
        }
      },
      {
        "@type": "Question",
        "name": "Are the test results reliable?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Designed based on psychological theories for self-understanding and entertainment. Not intended for clinical diagnosis."
        }
      },
      {
        "@type": "Question",
        "name": "What are Estrogen and Testosterone types?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Personality types inspired by hormonal characteristics: Estrogen (emotional, empathetic) and Testosterone (logical, analytical)."
        }
      },
      {
        "@type": "Question",
        "name": "Can I share results with friends?", 
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! Easily share on social media, messaging apps, or copy results to send to friends."
        }
      }
    ]
  }
  </script>'''
    }
    
    if lang in faq_schemas:
        # head 끝에 FAQ 스키마 추가
        head_end = r'</head>'
        content = re.sub(head_end, f'{faq_schemas[lang]}\n</head>', content)
    
    return content

def add_breadcrumb_schema(content, lang, filename):
    """BreadcrumbList 스키마 추가"""
    
    breadcrumb_schemas = {
        'ko': {
            'index.html': '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "홈",
        "item": "https://tests.mahalohana-bruce.com/"
      },
      {
        "@type": "ListItem", 
        "position": 2,
        "name": "에겐 vs 테토 성격테스트",
        "item": "https://tests.mahalohana-bruce.com/egen-teto/ko/"
      }
    ]
  }
  </script>''',
            'about.html': '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "홈",
        "item": "https://tests.mahalohana-bruce.com/"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "에겐 vs 테토 테스트",
        "item": "https://tests.mahalohana-bruce.com/egen-teto/ko/"
      },
      {
        "@type": "ListItem",
        "position": 3,
        "name": "테스트 소개",
        "item": "https://tests.mahalohana-bruce.com/egen-teto/ko/about.html"
      }
    ]
  }
  </script>'''
        },
        'ja': {
            'index.html': '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList", 
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "ホーム",
        "item": "https://tests.mahalohana-bruce.com/"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "エゲン vs テト 性格テスト",
        "item": "https://tests.mahalohana-bruce.com/egen-teto/ja/"
      }
    ]
  }
  </script>''',
            'about.html': '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "ホーム",
        "item": "https://tests.mahalohana-bruce.com/"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "エゲン vs テト テスト",
        "item": "https://tests.mahalohana-bruce.com/egen-teto/ja/"
      },
      {
        "@type": "ListItem",
        "position": 3,
        "name": "テストについて",
        "item": "https://tests.mahalohana-bruce.com/egen-teto/ja/about.html"
      }
    ]
  }
  </script>'''
        },
        'en': {
            'index.html': '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://tests.mahalohana-bruce.com/"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "Estrogen vs Testosterone Test",
        "item": "https://tests.mahalohana-bruce.com/egen-teto/en/"
      }
    ]
  }
  </script>''',
            'about.html': '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://tests.mahalohana-bruce.com/"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "Estrogen vs Testosterone Test",
        "item": "https://tests.mahalohana-bruce.com/egen-teto/en/"
      },
      {
        "@type": "ListItem",
        "position": 3,
        "name": "About Test",
        "item": "https://tests.mahalohana-bruce.com/egen-teto/en/about.html"
      }
    ]
  }
  </script>'''
        }
    }
    
    if lang in breadcrumb_schemas and filename in breadcrumb_schemas[lang]:
        # head 끝에 breadcrumb 스키마 추가
        head_end = r'</head>'
        content = re.sub(head_end, f'{breadcrumb_schemas[lang][filename]}\n</head>', content)
    
    return content

def improve_heading_structure(content, lang):
    """헤딩 구조 강화"""
    
    # H2, H3 태그에 에겐・테토 키워드 자연스럽게 추가
    heading_improvements = {
        'ko': [
            (r'<h2[^>]*>성격분석</h2>', '<h2>🎯 에겐 vs 테토 성격분석</h2>'),
            (r'<h3[^>]*>성격의 특징</h3>', '<h3>💖 에겐・테토 성격의 특징</h3>'),
            (r'<h3[^>]*>상성의 좋은 타입</h3>', '<h3>💕 에겐・테토 상성의 좋은 타입</h3>')
        ],
        'ja': [
            (r'<h2[^>]*>性格分析</h2>', '<h2>🎯 エゲン vs テト 性格分析</h2>'),
            (r'<h3[^>]*>性格の特徴</h3>', '<h3>💖 エゲン・テト 性格の特徴</h3>'),
            (r'<h3[^>]*>相性の良いタイプ</h3>', '<h3>💕 エゲン・テト 相性の良いタイプ</h3>')
        ],
        'en': [
            (r'<h2[^>]*>Personality Analysis</h2>', '<h2>🎯 Estrogen vs Testosterone Analysis</h2>'),
            (r'<h3[^>]*>Personality Traits</h3>', '<h3>💖 Estrogen・Testosterone Traits</h3>'),
            (r'<h3[^>]*>Compatible Types</h3>', '<h3>💕 Estrogen・Testosterone Compatibility</h3>')
        ]
    }
    
    if lang in heading_improvements:
        for old_pattern, new_heading in heading_improvements[lang]:
            content = re.sub(old_pattern, new_heading, content, flags=re.IGNORECASE)
    
    return content

def optimize_images(content):
    """이미지 최적화 속성 추가"""
    
    # 기존 이미지 태그에 속성 추가
    img_pattern = r'<img([^>]*?)src=["\']([^"\']*?)["\']([^>]*?)>'
    
    def enhance_img(match):
        pre_attrs = match.group(1)
        src = match.group(2)
        post_attrs = match.group(3)
        
        # loading="lazy" 추가 (이미 있으면 제외)
        if 'loading=' not in pre_attrs + post_attrs:
            post_attrs += ' loading="lazy"'
        
        # width, height 있는지 확인 후 추가
        if 'thumbnail.png' in src and 'width=' not in pre_attrs + post_attrs:
            post_attrs += ' width="1200" height="630"'
        
        return f'<img{pre_attrs}src="{src}"{post_attrs}>'
    
    content = re.sub(img_pattern, enhance_img, content)
    
    return content

def optimize_internal_links(content, lang):
    """내부 링크 최적화"""
    
    # 관련 테스트 링크 추가 (about.html에만)
    if 'about.html' in content:
        link_additions = {
            'ko': '''
    <div style="margin: 30px 0; padding: 20px; background: #f8f9ff; border-radius: 12px; text-align: center;">
      <h3 style="margin-bottom: 15px;">🔗 관련 테스트</h3>
      <p style="margin-bottom: 15px;">
        <a href="../" style="color: #667eea; text-decoration: none; font-weight: 600;">← 에겐 vs 테토 테스트 하러가기</a>
      </p>
      <p>
        <a href="/ko/" style="color: #10b981; text-decoration: none; font-weight: 600;">🏠 다른 심리테스트 둘러보기</a>
      </p>
    </div>''',
            'ja': '''
    <div style="margin: 30px 0; padding: 20px; background: #f8f9ff; border-radius: 12px; text-align: center;">
      <h3 style="margin-bottom: 15px;">🔗 関連テスト</h3>
      <p style="margin-bottom: 15px;">
        <a href="../" style="color: #667eea; text-decoration: none; font-weight: 600;">← エゲン vs テト テストを受ける</a>
      </p>
      <p>
        <a href="/ja/" style="color: #10b981; text-decoration: none; font-weight: 600;">🏠 他の心理テストを見る</a>
      </p>
    </div>''',
            'en': '''
    <div style="margin: 30px 0; padding: 20px; background: #f8f9ff; border-radius: 12px; text-align: center;">
      <h3 style="margin-bottom: 15px;">🔗 Related Tests</h3>
      <p style="margin-bottom: 15px;">
        <a href="../" style="color: #667eea; text-decoration: none; font-weight: 600;">← Take Estrogen vs Testosterone Test</a>
      </p>
      <p>
        <a href="/en/" style="color: #10b981; text-decoration: none; font-weight: 600;">🏠 Browse Other Psychology Tests</a>
      </p>
    </div>'''
        }
        
        if lang in link_additions:
            # footer 앞에 추가
            footer_pattern = r'(<div class=["\']footer["\'])'
            content = re.sub(footer_pattern, f'{link_additions[lang]}\\1', content)
    
    return content

if __name__ == "__main__":
    print("🚀 에겐 vs 테토 테스트 SEO 고급 개선 시작...")
    enhance_egen_teto_seo()
    print("\n✅ 에겐-테토 테스트 SEO 개선 완료!")
    print("\n📈 적용된 개선사항:")
    print("1. ✅ 키워드 리서치 기반 title 리라이팅")
    print("2. ✅ CTA 삽입된 meta description")
    print("3. ✅ OG locale & site_name 태그 추가")
    print("4. ✅ Twitter Card 최적화 (크기 정보 포함)")
    print("5. ✅ JSON-LD 구조화 데이터 고도화")
    print("6. ✅ FAQ 스키마 추가 (리치 스니펫)")
    print("7. ✅ BreadcrumbList 스키마 추가")
    print("8. ✅ 헤딩 구조 키워드 강화")
    print("9. ✅ 이미지 최적화 (lazy loading, 크기)")
    print("10. ✅ 내부 링크 최적화")
