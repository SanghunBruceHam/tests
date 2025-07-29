#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import quote
from utils import FileManager, logger
from config import Config

class SitemapGenerator:
    """SEO 최적화된 사이트맵 생성기"""
    
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.sitemap_file = Config.SITEMAP_FILE
        self.excluded_patterns = ['.git', 'node_modules', '__pycache__', '.DS_Store']
        
    def find_html_files(self, directory: str = ".") -> List[Dict[str, str]]:
        """HTML 파일들을 찾아서 메타데이터와 함께 반환"""
        html_files = []
        
        try:
            for root, dirs, files in os.walk(directory):
                # 제외할 디렉토리 필터링
                dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.excluded_patterns)]
                
                for file in files:
                    if file.endswith(".html"):
                        full_path = os.path.join(root, file).replace("\\", "/")
                        
                        # 제외 패턴 확인
                        if any(pattern in full_path for pattern in self.excluded_patterns):
                            continue
                        
                        # URL 생성 (안전한 인코딩)
                        relative_path = full_path.lstrip("./")
                        encoded_path = quote(relative_path, safe='/')
                        url = f"{self.base_url}/{encoded_path}"
                        
                        # 파일 메타데이터 수집
                        file_info = self._get_file_metadata(full_path)
                        file_info['url'] = url
                        html_files.append(file_info)
            
            logger.info(f"발견된 HTML 파일: {len(html_files)}개")
            return html_files
            
        except OSError as e:
            logger.error(f"디렉토리 탐색 오류: {e}")
            return []
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}")
            return []
    
    def _get_file_metadata(self, file_path: str) -> Dict[str, str]:
        """파일 메타데이터 추출"""
        try:
            # 파일 수정 시간
            mtime = os.path.getmtime(file_path)
            lastmod = datetime.fromtimestamp(mtime).strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # 우선순위 결정
            priority = self._calculate_priority(file_path)
            
            # 변경 빈도 결정
            changefreq = self._determine_changefreq(file_path)
            
            return {
                'lastmod': lastmod,
                'priority': priority,
                'changefreq': changefreq,
                'path': file_path
            }
            
        except OSError as e:
            logger.warning(f"파일 메타데이터 추출 실패 {file_path}: {e}")
            return {
                'lastmod': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                'priority': '0.5',
                'changefreq': 'weekly',
                'path': file_path
            }
    
    def _calculate_priority(self, file_path: str) -> str:
        """파일 경로 기반 우선순위 계산"""
        if file_path == 'index.html':
            return '1.0'  # 메인 페이지
        elif '/index.html' in file_path:
            return '0.9'  # 섹션 메인 페이지
        elif any(lang in file_path for lang in Config.SUPPORTED_LANGUAGES):
            return '0.8'  # 언어별 페이지
        elif 'test' in file_path.lower():
            return '0.7'  # 테스트 페이지
        else:
            return '0.5'  # 기타 페이지
    
    def _determine_changefreq(self, file_path: str) -> str:
        """파일 유형별 변경 빈도 결정"""
        if file_path == 'index.html':
            return 'daily'
        elif '/index.html' in file_path:
            return 'weekly'
        elif 'test' in file_path.lower():
            return 'monthly'
        else:
            return 'yearly'
    
    def generate_sitemap(self) -> bool:
        """사이트맵 XML 생성"""
        try:
            html_files = self.find_html_files()
            
            if not html_files:
                logger.warning("생성할 URL이 없습니다.")
                return False
            
            # XML 생성
            sitemap_content = self._build_sitemap_xml(html_files)
            
            # 파일 저장
            if FileManager.write_file_safely(self.sitemap_file, sitemap_content):
                logger.info(f"사이트맵 생성 완료: {len(html_files)}개 URL")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"사이트맵 생성 실패: {e}")
            return False
    
    def _build_sitemap_xml(self, html_files: List[Dict[str, str]]) -> str:
        """XML 사이트맵 구조 생성"""
        sitemap_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
            '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
            '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9',
            '        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'
        ]
        
        # URL 정렬 (우선순위 높은 순)
        sorted_files = sorted(html_files, key=lambda x: float(x['priority']), reverse=True)
        
        for file_info in sorted_files:
            sitemap_lines.extend([
                "  <url>",
                f"    <loc>{file_info['url']}</loc>",
                f"    <lastmod>{file_info['lastmod']}</lastmod>",
                f"    <changefreq>{file_info['changefreq']}</changefreq>",
                f"    <priority>{file_info['priority']}</priority>",
                "  </url>"
            ])
        
        sitemap_lines.append("</urlset>")
        return "\n".join(sitemap_lines)
    
    def validate_sitemap(self) -> bool:
        """생성된 사이트맵 유효성 검사"""
        try:
            content = FileManager.read_file_safely(self.sitemap_file)
            if not content:
                return False
            
            # 기본 XML 구조 확인
            required_elements = ['<?xml', '<urlset', '</urlset>', '<url>', '<loc>']
            if all(element in content for element in required_elements):
                logger.info("사이트맵 유효성 검사 통과")
                return True
            else:
                logger.error("사이트맵 유효성 검사 실패")
                return False
                
        except Exception as e:
            logger.error(f"사이트맵 유효성 검사 오류: {e}")
            return False

def main():
    """메인 실행 함수"""
    generator = SitemapGenerator()
    
    if generator.generate_sitemap():
        generator.validate_sitemap()
        logger.info("사이트맵 생성 프로세스 완료")
    else:
        logger.error("사이트맵 생성 실패")

if __name__ == "__main__":
    main()
