// SEO 최적화 라이브러리
class SEOOptimizer {
  constructor() {
    this.config = {
      siteName: '심리테스트 모음',
      defaultDescription: '무료 심리테스트로 나를 알아보세요! 성격, 연애, 직업 적성 등 다양한 테스트',
      defaultKeywords: '심리테스트, 성격테스트, 연애테스트, 직업적성검사, 무료테스트',
      twitterSite: '@tests_mahalohana',
      baseUrl: 'https://tests.mahalohana-bruce.com'
    };
    
    this.init();
  }

  init() {
    this.enhanceMetaTags();
    this.addStructuredData();
    this.optimizeImages();
    this.setupBreadcrumbs();
    this.addAlternateLanguages();
    this.optimizeHeadings();
    this.addSocialMetaTags();
  }

  // 메타 태그 최적화
  enhanceMetaTags() {
    // 뷰포트 최적화
    this.updateMetaTag('viewport', 'width=device-width, initial-scale=1.0, viewport-fit=cover');
    
    // 캐시 제어
    this.addMetaTag('http-equiv', 'Cache-Control', 'public, max-age=3600');
    
    // 보안 헤더
    this.addMetaTag('http-equiv', 'X-Content-Type-Options', 'nosniff');
    this.addMetaTag('http-equiv', 'X-Frame-Options', 'SAMEORIGIN');
    
    // 모바일 최적화
    this.addMetaTag('name', 'mobile-web-app-capable', 'yes');
    this.addMetaTag('name', 'apple-mobile-web-app-capable', 'yes');
    this.addMetaTag('name', 'apple-mobile-web-app-status-bar-style', 'default');
    
    // 검색엔진 최적화
    this.addMetaTag('name', 'robots', 'index, follow, max-image-preview:large');
    this.addMetaTag('name', 'googlebot', 'index, follow');
    
    // 페이지 분류
    this.addMetaTag('name', 'category', 'Education, Psychology, Entertainment');
    this.addMetaTag('name', 'coverage', 'Worldwide');
    this.addMetaTag('name', 'distribution', 'Global');
    this.addMetaTag('name', 'rating', 'General');
  }

  updateMetaTag(attribute, name, content) {
    let meta = document.querySelector(`meta[${attribute}="${name}"]`);
    if (!meta) {
      meta = document.createElement('meta');
      meta.setAttribute(attribute, name);
      document.head.appendChild(meta);
    }
    meta.setAttribute('content', content);
  }

  addMetaTag(attribute, name, content) {
    if (!document.querySelector(`meta[${attribute}="${name}"]`)) {
      const meta = document.createElement('meta');
      meta.setAttribute(attribute, name);
      meta.setAttribute('content', content);
      document.head.appendChild(meta);
    }
  }

  // 구조화된 데이터 추가
  addStructuredData() {
    const structuredData = {
      '@context': 'https://schema.org',
      '@type': 'WebApplication',
      name: this.config.siteName,
      description: this.config.defaultDescription,
      url: this.config.baseUrl,
      applicationCategory: 'EntertainmentApplication',
      operatingSystem: 'Any',
      offers: {
        '@type': 'Offer',
        price: '0',
        priceCurrency: 'KRW'
      },
      publisher: {
        '@type': 'Organization',
        name: this.config.siteName,
        url: this.config.baseUrl
      },
      mainEntity: {
        '@type': 'WebSite',
        url: this.config.baseUrl,
        potentialAction: {
          '@type': 'SearchAction',
          target: `${this.config.baseUrl}/search?q={search_term_string}`,
          'query-input': 'required name=search_term_string'
        }
      }
    };

    // 테스트 페이지인 경우 추가 구조화 데이터
    if (this.isTestPage()) {
      structuredData['@type'] = 'Quiz';
      structuredData.educationalLevel = 'beginner';
      structuredData.assesses = 'personality, psychology';
    }

    this.addJsonLd(structuredData);
    
    // FAQ 구조화 데이터 (해당하는 경우)
    this.addFAQStructuredData();
    
    // 빵부스러기 구조화 데이터
    this.addBreadcrumbStructuredData();
  }

  addJsonLd(data) {
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(data, null, 2);
    document.head.appendChild(script);
  }

  addFAQStructuredData() {
    const faqElements = document.querySelectorAll('.faq-item, .question-answer');
    if (faqElements.length > 0) {
      const faqData = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        mainEntity: []
      };

      faqElements.forEach(item => {
        const question = item.querySelector('.question, h3, .faq-question');
        const answer = item.querySelector('.answer, .faq-answer, p');
        
        if (question && answer) {
          faqData.mainEntity.push({
            '@type': 'Question',
            name: question.textContent.trim(),
            acceptedAnswer: {
              '@type': 'Answer',
              text: answer.textContent.trim()
            }
          });
        }
      });

      if (faqData.mainEntity.length > 0) {
        this.addJsonLd(faqData);
      }
    }
  }

  addBreadcrumbStructuredData() {
    const breadcrumbs = this.generateBreadcrumbs();
    if (breadcrumbs.length > 1) {
      const breadcrumbData = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        itemListElement: breadcrumbs.map((crumb, index) => ({
          '@type': 'ListItem',
          position: index + 1,
          name: crumb.name,
          item: crumb.url
        }))
      };

      this.addJsonLd(breadcrumbData);
    }
  }

  // 이미지 최적화
  optimizeImages() {
    document.querySelectorAll('img').forEach(img => {
      // Alt 태그 확인
      if (!img.alt) {
        img.alt = this.generateImageAltText(img);
      }

      // 로딩 최적화
      if (!img.loading) {
        img.loading = 'lazy';
      }

      // 크기 속성 추가
      if (!img.width && !img.height) {
        img.addEventListener('load', () => {
          img.width = img.naturalWidth;
          img.height = img.naturalHeight;
        });
      }
    });
  }

  generateImageAltText(img) {
    const src = img.src;
    const title = document.title;
    
    if (src.includes('favicon')) return '사이트 아이콘';
    if (src.includes('logo')) return '로고';
    if (src.includes('thumbnail')) return '테스트 썸네일';
    
    return `${title} 관련 이미지`;
  }

  // 빵부스러기 내비게이션
  setupBreadcrumbs() {
    const breadcrumbs = this.generateBreadcrumbs();
    if (breadcrumbs.length > 1) {
      this.renderBreadcrumbs(breadcrumbs);
    }
  }

  generateBreadcrumbs() {
    const path = window.location.pathname;
    const segments = path.split('/').filter(segment => segment);
    const breadcrumbs = [{ name: '홈', url: '/' }];

    let currentPath = '';
    segments.forEach(segment => {
      currentPath += '/' + segment;
      
      let name = this.segmentToName(segment);
      breadcrumbs.push({
        name: name,
        url: this.config.baseUrl + currentPath
      });
    });

    return breadcrumbs;
  }

  segmentToName(segment) {
    const nameMap = {
      'ko': '한국어',
      'ja': '日本語', 
      'en': 'English',
      'romance-test': '연애 테스트',
      'egen-teto': '에겐테토 테스트',
      'about': '소개'
    };

    return nameMap[segment] || segment.replace(/-/g, ' ');
  }

  renderBreadcrumbs(breadcrumbs) {
    const nav = document.createElement('nav');
    nav.setAttribute('aria-label', '페이지 경로');
    nav.className = 'breadcrumbs';
    
    const ol = document.createElement('ol');
    ol.style.cssText = `
      display: flex;
      list-style: none;
      padding: 0;
      margin: 10px 0;
      font-size: 14px;
      color: #666;
    `;

    breadcrumbs.forEach((crumb, index) => {
      const li = document.createElement('li');
      li.style.cssText = `
        display: flex;
        align-items: center;
      `;

      if (index === breadcrumbs.length - 1) {
        // 현재 페이지
        li.textContent = crumb.name;
        li.style.color = '#333';
        li.setAttribute('aria-current', 'page');
      } else {
        // 링크
        const a = document.createElement('a');
        a.href = crumb.url;
        a.textContent = crumb.name;
        a.style.cssText = `
          color: #007bff;
          text-decoration: none;
        `;
        li.appendChild(a);

        // 구분자
        const separator = document.createElement('span');
        separator.textContent = ' › ';
        separator.style.margin = '0 8px';
        li.appendChild(separator);
      }

      ol.appendChild(li);
    });

    nav.appendChild(ol);
    
    // 메인 콘텐츠 앞에 삽입
    const main = document.querySelector('main, .main-content, .container');
    if (main) {
      main.insertBefore(nav, main.firstChild);
    }
  }

  // 다국어 대체 링크
  addAlternateLanguages() {
    const currentPath = window.location.pathname;
    const languages = ['ko', 'ja', 'en'];
    
    languages.forEach(lang => {
      const hrefLang = lang === 'ko' ? 'ko-KR' : lang === 'ja' ? 'ja-JP' : 'en-US';
      let href;
      
      if (lang === 'ko') {
        href = currentPath.replace(/\/(ja|en)\//, '/');
        if (href.startsWith('/ja/') || href.startsWith('/en/')) {
          href = href.substring(3);
        }
      } else {
        href = currentPath.replace(/\/(ko|ja|en)\//, `/${lang}/`);
        if (!href.startsWith(`/${lang}/`)) {
          href = `/${lang}${href}`;
        }
      }

      const link = document.createElement('link');
      link.rel = 'alternate';
      link.hreflang = hrefLang;
      link.href = this.config.baseUrl + href;
      document.head.appendChild(link);
    });

    // x-default 추가
    const defaultLink = document.createElement('link');
    defaultLink.rel = 'alternate';
    defaultLink.hreflang = 'x-default';
    defaultLink.href = this.config.baseUrl + '/';
    document.head.appendChild(defaultLink);
  }

  // 제목 구조 최적화
  optimizeHeadings() {
    const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
    let h1Count = 0;

    headings.forEach(heading => {
      if (heading.tagName === 'H1') {
        h1Count++;
        if (h1Count > 1) {
          // H1이 여러 개인 경우 H2로 변경
          const newHeading = document.createElement('h2');
          newHeading.innerHTML = heading.innerHTML;
          newHeading.className = heading.className;
          heading.parentNode.replaceChild(newHeading, heading);
        }
      }

      // 빈 제목 확인
      if (!heading.textContent.trim()) {
        console.warn('Empty heading detected:', heading);
      }
    });
  }

  // 소셜 미디어 메타 태그
  addSocialMetaTags() {
    const title = document.title;
    const description = this.getMetaContent('description') || this.config.defaultDescription;
    const url = window.location.href;
    const image = this.findBestImage();

    // Open Graph
    this.updateMetaTag('property', 'og:type', 'website');
    this.updateMetaTag('property', 'og:title', title);
    this.updateMetaTag('property', 'og:description', description);
    this.updateMetaTag('property', 'og:url', url);
    this.updateMetaTag('property', 'og:site_name', this.config.siteName);
    
    if (image) {
      this.updateMetaTag('property', 'og:image', image);
      this.updateMetaTag('property', 'og:image:width', '1200');
      this.updateMetaTag('property', 'og:image:height', '630');
    }

    // Twitter Card
    this.updateMetaTag('name', 'twitter:card', 'summary_large_image');
    this.updateMetaTag('name', 'twitter:site', this.config.twitterSite);
    this.updateMetaTag('name', 'twitter:title', title);
    this.updateMetaTag('name', 'twitter:description', description);
    
    if (image) {
      this.updateMetaTag('name', 'twitter:image', image);
    }
  }

  getMetaContent(name) {
    const meta = document.querySelector(`meta[name="${name}"]`);
    return meta ? meta.getAttribute('content') : null;
  }

  findBestImage() {
    // 우선순위에 따라 이미지 검색
    const selectors = [
      'meta[property="og:image"]',
      '.main-image img',
      '.thumbnail img',
      'img[src*="thumbnail"]',
      'img[src*="logo"]'
    ];

    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element) {
        const src = element.tagName === 'IMG' ? element.src : element.getAttribute('content');
        if (src && !src.includes('favicon')) {
          return new URL(src, this.config.baseUrl).href;
        }
      }
    }

    return `${this.config.baseUrl}/favicon.png`;
  }

  // 유틸리티 메서드
  isTestPage() {
    return window.location.pathname.includes('test') || 
           document.querySelector('.test-container, .quiz-container');
  }

  // 성능 모니터링
  trackPagePerformance() {
    if ('performance' in window) {
      window.addEventListener('load', () => {
        setTimeout(() => {
          const perfData = performance.getEntriesByType('navigation')[0];
          const metrics = {
            'page_load_time': perfData.loadEventEnd - perfData.loadEventStart,
            'dom_content_loaded': perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
            'first_paint': performance.getEntriesByType('paint')[0]?.startTime || 0
          };

          // Google Analytics로 전송
          if (typeof gtag !== 'undefined') {
            Object.entries(metrics).forEach(([metric, value]) => {
              gtag('event', 'timing_complete', {
                'name': metric,
                'value': Math.round(value)
              });
            });
          }
        }, 0);
      });
    }
  }
}

// 페이지 로드시 초기화
document.addEventListener('DOMContentLoaded', () => {
  window.seoOptimizer = new SEOOptimizer();
});

// 전역 SEO 유틸리티
window.seo = {
  updateTitle: (title) => {
    document.title = title;
    window.seoOptimizer?.updateMetaTag('property', 'og:title', title);
    window.seoOptimizer?.updateMetaTag('name', 'twitter:title', title);
  },
  
  updateDescription: (description) => {
    window.seoOptimizer?.updateMetaTag('name', 'description', description);
    window.seoOptimizer?.updateMetaTag('property', 'og:description', description);
    window.seoOptimizer?.updateMetaTag('name', 'twitter:description', description);
  }
};