#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_thumbnail(text_main, text_sub, text_bottom, filename):
    # 썸네일 크기
    width, height = 800, 600
    
    # 그라디언트 배경 생성
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # 그라디언트 효과를 위한 단순한 접근
    for y in range(height):
        # 색상 interpolation
        ratio = y / height
        if ratio < 0.25:
            r = int(255 * (1 - ratio*4) + 255 * ratio*4)
            g = int(179 * (1 - ratio*4) + 204 * ratio*4) 
            b = int(230 * (1 - ratio*4) + 249 * ratio*4)
        elif ratio < 0.5:
            ratio_local = (ratio - 0.25) * 4
            r = int(255 * (1 - ratio_local) + 230 * ratio_local)
            g = int(204 * (1 - ratio_local) + 204 * ratio_local)
            b = int(249 * (1 - ratio_local) + 255 * ratio_local)
        elif ratio < 0.75:
            ratio_local = (ratio - 0.5) * 4
            r = int(230 * (1 - ratio_local) + 204 * ratio_local)
            g = int(204 * (1 - ratio_local) + 242 * ratio_local)
            b = int(255 * (1 - ratio_local) + 255 * ratio_local)
        else:
            ratio_local = (ratio - 0.75) * 4
            r = int(204 * (1 - ratio_local) + 255 * ratio_local)
            g = int(242 * (1 - ratio_local) + 255 * ratio_local)
            b = int(255 * (1 - ratio_local) + 204 * ratio_local)
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    try:
        # 폰트 로드 시도
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 28) 
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        # 기본 폰트 사용
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 메인 텍스트
    bbox = draw.textbbox((0, 0), text_main, font=font_large)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, 150), text_main, fill=(90, 79, 207), font=font_large)
    
    # 서브 텍스트
    bbox = draw.textbbox((0, 0), text_sub, font=font_medium)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, 220), text_sub, fill=(123, 104, 238), font=font_medium)
    
    # 하단 텍스트
    bbox = draw.textbbox((0, 0), text_bottom, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, 520), text_bottom, fill=(75, 0, 130), font=font_small)
    
    # 장식 요소들 (간단한 원과 사각형으로 캐릭터 표현)
    # 왼쪽 캐릭터
    draw.ellipse([210, 310, 290, 390], fill=(147, 112, 219))
    draw.rectangle([230, 380, 270, 460], fill=(147, 112, 219))
    
    # 오른쪽 캐릭터  
    draw.ellipse([510, 310, 590, 390], fill=(138, 43, 226))
    draw.rectangle([530, 380, 570, 460], fill=(138, 43, 226))
    
    # 중앙 원형 장식
    draw.ellipse([320, 270, 480, 430], outline=(255, 105, 180), width=3)
    
    img.save(filename)
    print(f"Created {filename}")

def create_favicon(filename):
    # 파비콘 크기
    size = 64
    img = Image.new('RGB', (size, size))
    draw = ImageDraw.Draw(img)
    
    # 그라디언트 배경
    for y in range(size):
        ratio = y / size
        r = int(255 * (1 - ratio) + 230 * ratio)
        g = int(179 * (1 - ratio) + 204 * ratio)
        b = int(230 * (1 - ratio) + 255 * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b))
    
    # 하트 모양 (간단한 원 두개로)
    draw.ellipse([12, 15, 28, 31], fill=(255, 105, 180))
    draw.ellipse([27, 15, 43, 31], fill=(255, 105, 180))
    
    # 하트 하단부
    points = [(12, 23), (32, 50), (52, 23)]
    draw.polygon(points, fill=(255, 105, 180))
    
    img.save(filename)
    print(f"Created {filename}")

# 이미지 생성
if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    # 한국어 썸네일
    create_thumbnail(
        "애니메 성격 테스트",
        "나는 어떤 애니메 캐릭터 타입일까?",
        "6가지 성격 유형으로 알아보는 나의 애니메 캐릭터!",
        str(base_dir / "ko/thumbnail.png")
    )
    
    # 일본어 썸네일
    create_thumbnail(
        "アニメ性格診断",
        "あなたはどのアニメキャラタイプ？",
        "6つの性格タイプであなたのアニメキャラを診断！",
        str(base_dir / "ja/thumbnail.png")
    )
    
    # 파비콘
    create_favicon(str(base_dir / "ko/favicon.png"))
    create_favicon(str(base_dir / "ja/favicon.png"))
