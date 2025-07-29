#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import Dict, Any

class Config:
    """애플리케이션 설정 관리 클래스"""
    
    # 기본 설정
    BASE_URL = "https://tests.mahalohana-bruce.com"
    SITEMAP_FILE = "sitemap.xml"
    
    # Google Analytics & AdSense (환경변수에서 읽기)
    GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID', 'G-45VSGEM7EZ')
    ADSENSE_CLIENT_ID = os.getenv('ADSENSE_CLIENT_ID', 'ca-pub-5508768187151867')
    
    # 쿠팡 파트너스 설정
    COUPANG_PARTNER_ID = os.getenv('COUPANG_PARTNER_ID', '867629')
    COUPANG_TRACKING_CODE = os.getenv('COUPANG_TRACKING_CODE', 'AF6959276')
    
    # 지원 언어
    SUPPORTED_LANGUAGES = ['ko', 'ja', 'en']
    
    # 파일 경로 설정
    DIRECTORIES = {
        'tests': ['romance-test', 'egen-teto'],
        'assets': 'assets',
        'attached_assets': 'attached_assets'
    }
    
    # SEO 설정
    SEO_CONFIG = {
        'site_name': '심리테스트 모음',
        'twitter_site': '@tests_mahalohana',
        'twitter_creator': '@mahalohana_bruce',
        'default_description': '무료 심리테스트 모음! 성격 테스트, 연애 궁합, 직업 적성 검사 등',
        'keywords': 'P심리테스트, 성격테스트, 연애테스트, 직업적성검사, 무료테스트, 성향분석'
    }
    
    # 로깅 설정
    LOGGING_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'app.log'
    }

    @classmethod
    def get_coupang_ad_config(cls) -> Dict[str, Any]:
        """쿠팡 광고 설정 반환"""
        return {
            'id': cls.COUPANG_PARTNER_ID,
            'tracking_code': cls.COUPANG_TRACKING_CODE,
            'templates': {
                'main_width': '680',
                'main_height': '140',
                'test_width': '750',
                'test_height': '150'
            }
        }
    
    @classmethod
    def get_analytics_config(cls) -> Dict[str, str]:
        """분석 도구 설정 반환"""
        return {
            'google_analytics_id': cls.GOOGLE_ANALYTICS_ID,
            'adsense_client_id': cls.ADSENSE_CLIENT_ID
        }