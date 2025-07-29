#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import logging
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
from config import Config

# 로깅 설정
logging.basicConfig(
    level=getattr(logging, Config.LOGGING_CONFIG['level']),
    format=Config.LOGGING_CONFIG['format'],
    handlers=[
        logging.FileHandler(Config.LOGGING_CONFIG['file'], encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class FileManager:
    """파일 관리 유틸리티 클래스"""
    
    @staticmethod
    def find_html_files_by_language(language: str = 'ko', 
                                   base_dir: str = '.') -> List[str]:
        """언어별 HTML 파일 찾기"""
        html_files = []
        
        try:
            # 루트 index.html (한국어의 경우)
            if language == 'ko' and os.path.exists('index.html'):
                html_files.append('index.html')
            
            # 언어별 디렉토리
            lang_dir = Path(base_dir) / language
            if lang_dir.exists():
                for file in lang_dir.glob('*.html'):
                    html_files.append(str(file))
            
            # 테스트 디렉토리의 언어별 파일들
            for test_dir in Config.DIRECTORIES['tests']:
                lang_test_dir = Path(base_dir) / test_dir / language
                if lang_test_dir.exists():
                    for file in lang_test_dir.glob('*.html'):
                        html_files.append(str(file))
                        
            logger.info(f"Found {len(html_files)} HTML files for language: {language}")
            return html_files
            
        except Exception as e:
            logger.error(f"Error finding HTML files for {language}: {e}")
            return []
    
    @staticmethod
    def read_file_safely(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
        """안전한 파일 읽기"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except UnicodeDecodeError:
            logger.error(f"Encoding error reading {file_path}")
        except PermissionError:
            logger.error(f"Permission denied: {file_path}")
        except Exception as e:
            logger.error(f"Unexpected error reading {file_path}: {e}")
        return None
    
    @staticmethod
    def write_file_safely(file_path: str, content: str, 
                         encoding: str = 'utf-8') -> bool:
        """안전한 파일 쓰기"""
        try:
            # 디렉토리 생성
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            logger.info(f"Successfully wrote file: {file_path}")
            return True
        except PermissionError:
            logger.error(f"Permission denied writing to: {file_path}")
        except OSError as e:
            logger.error(f"OS error writing {file_path}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error writing {file_path}: {e}")
        return False

class ContentProcessor:
    """콘텐츠 처리 유틸리티 클래스"""
    
    @staticmethod
    def has_content_marker(content: str, marker: str) -> bool:
        """특정 마커가 콘텐츠에 있는지 확인"""
        return marker in content
    
    @staticmethod
    def extract_test_info(html_file: str, language: str) -> Tuple[str, str]:
        """HTML 파일에서 테스트 제목과 설명 추출"""
        content = FileManager.read_file_safely(html_file)
        if not content:
            return "테스트", "심리테스트"
        
        try:
            # title 태그에서 제목 추출
            title_match = re.search(r'<title[^>]*>(.*?)</title>', 
                                  content, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1).strip() if title_match else "테스트"
            
            # description 메타 태그에서 설명 추출
            desc_pattern = (r'<meta[^>]*name=["\']description["\'][^>]*'
                          r'content=["\']([^"\']*)["\']')
            desc_match = re.search(desc_pattern, content, re.IGNORECASE)
            desc = desc_match.group(1).strip() if desc_match else "심리테스트"
            
            # 제목에서 불필요한 부분 제거
            title = re.sub(r'[|｜].*$', '', title).strip()
            
            logger.debug(f"Extracted info from {html_file}: {title}, {desc}")
            return title, desc
            
        except Exception as e:
            logger.error(f"Error extracting test info from {html_file}: {e}")
            return "테스트", "심리테스트"

class SecurityUtils:
    """보안 관련 유틸리티"""
    
    @staticmethod
    def sanitize_html_input(text: str) -> str:
        """HTML 입력 새니타이징"""
        if not text:
            return ""
        
        # 기본적인 XSS 방지
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>.*?</iframe>'
        ]
        
        sanitized = text
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        
        return sanitized
    
    @staticmethod
    def validate_file_path(file_path: str, allowed_extensions: List[str] = None) -> bool:
        """파일 경로 검증"""
        if not file_path:
            return False
        
        # 상위 디렉토리 접근 방지
        if '..' in file_path or file_path.startswith('/'):
            return False
        
        # 허용된 확장자 확인
        if allowed_extensions:
            ext = os.path.splitext(file_path)[1].lower()
            if ext not in allowed_extensions:
                return False
        
        return True

def setup_logging():
    """로깅 설정 초기화"""
    logger.info("Application logging initialized")
    return logger