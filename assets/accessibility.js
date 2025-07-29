// 접근성 및 사용자 경험 향상 라이브러리
class AccessibilityEnhancer {
  constructor() {
    this.preferences = this.loadUserPreferences();
    this.init();
  }

  init() {
    this.setupFocusManagement();
    this.setupKeyboardNavigation();
    this.setupScreenReaderSupport();
    this.setupColorContrastToggle();
    this.setupFontSizeControls();
    this.setupMotionPreferences();
    this.setupLanguageDetection();
  }

  // 포커스 관리
  setupFocusManagement() {
    // 포커스 표시기 강화
    const style = document.createElement('style');
    style.textContent = `
      *:focus {
        outline: 2px solid #4A90E2 !important;
        outline-offset: 2px !important;
        box-shadow: 0 0 0 4px rgba(74, 144, 226, 0.3) !important;
      }
      
      .skip-link {
        position: absolute;
        top: -40px;
        left: 6px;
        background: #000;
        color: #fff;
        padding: 8px;
        text-decoration: none;
        z-index: 100;
        border-radius: 4px;
      }
      
      .skip-link:focus {
        top: 6px;
      }
    `;
    document.head.appendChild(style);

    // Skip link 추가
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.className = 'skip-link';
    skipLink.textContent = '메인 콘텐츠로 건너뛰기';
    document.body.insertBefore(skipLink, document.body.firstChild);
  }

  // 키보드 네비게이션 강화
  setupKeyboardNavigation() {
    // Tab 순서 관리
    this.manageFocusOrder();
    
    // 키보드 단축키
    document.addEventListener('keydown', (e) => {
      // Alt + H: 홈으로
      if (e.altKey && e.key === 'h') {
        e.preventDefault();
        window.location.href = '/';
      }
      
      // Alt + M: 메인 메뉴
      if (e.altKey && e.key === 'm') {
        e.preventDefault();
        const menu = document.querySelector('nav, .navigation');
        if (menu) menu.focus();
      }
      
      // Alt + S: 검색/테스트 선택
      if (e.altKey && e.key === 's') {
        e.preventDefault();
        const searchElement = document.querySelector('.test-grid, .search-input');
        if (searchElement) searchElement.focus();
      }
    });
  }

  manageFocusOrder() {
    // 동적으로 생성된 요소들의 tab index 관리
    const focusableElements = [
      'button',
      'input',
      'select',
      'textarea',
      'a[href]',
      '[tabindex]:not([tabindex="-1"])'
    ];

    const elements = document.querySelectorAll(focusableElements.join(','));
    elements.forEach((el, index) => {
      if (!el.hasAttribute('tabindex')) {
        el.setAttribute('tabindex', '0');
      }
    });
  }

  // 스크린 리더 지원
  setupScreenReaderSupport() {
    // ARIA 라벨 자동 추가
    this.addAriaLabels();
    
    // 동적 콘텐츠 알림
    this.setupLiveRegions();
    
    // 진행률 표시기 ARIA 속성
    this.enhanceProgressIndicators();
  }

  addAriaLabels() {
    // 버튼에 ARIA 라벨 추가
    document.querySelectorAll('button:not([aria-label])').forEach(button => {
      const text = button.textContent.trim();
      if (text) {
        button.setAttribute('aria-label', text);
      }
    });

    // 링크에 설명 추가
    document.querySelectorAll('a:not([aria-label])').forEach(link => {
      const text = link.textContent.trim();
      if (text) {
        link.setAttribute('aria-label', `${text} 페이지로 이동`);
      }
    });

    // 테스트 결과에 역할 정의
    document.querySelectorAll('.result, .test-result').forEach(result => {
      result.setAttribute('role', 'region');
      result.setAttribute('aria-label', '테스트 결과');
    });
  }

  setupLiveRegions() {
    // 실시간 업데이트 영역 생성
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    liveRegion.id = 'live-region';
    liveRegion.style.cssText = `
      position: absolute;
      left: -10000px;
      width: 1px;
      height: 1px;
      overflow: hidden;
    `;
    document.body.appendChild(liveRegion);

    // 전역 알림 함수
    window.announceToScreenReader = (message) => {
      liveRegion.textContent = message;
      setTimeout(() => {
        liveRegion.textContent = '';
      }, 1000);
    };
  }

  enhanceProgressIndicators() {
    document.querySelectorAll('.progress-bar, .progress').forEach(progress => {
      progress.setAttribute('role', 'progressbar');
      progress.setAttribute('aria-valuemin', '0');
      progress.setAttribute('aria-valuemax', '100');
      
      // 현재 값 업데이트 감지
      const observer = new MutationObserver(() => {
        const value = this.getProgressValue(progress);
        progress.setAttribute('aria-valuenow', value);
        progress.setAttribute('aria-label', `진행률: ${value}%`);
      });
      
      observer.observe(progress, { attributes: true, childList: true });
    });
  }

  getProgressValue(element) {
    // 다양한 방식으로 진행률 값 추출
    const style = element.style.getPropertyValue('--progress-width');
    if (style) return parseInt(style) || 0;
    
    const width = element.style.width;
    if (width && width.includes('%')) return parseInt(width) || 0;
    
    return 0;
  }

  // 색상 대비 토글
  setupColorContrastToggle() {
    const contrastToggle = document.createElement('button');
    contrastToggle.textContent = '고대비 모드';
    contrastToggle.className = 'contrast-toggle';
    contrastToggle.setAttribute('aria-label', '고대비 모드 토글');
    
    contrastToggle.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      z-index: 1000;
      padding: 8px 12px;
      background: #333;
      color: #fff;
      border: none;
      border-radius: 4px;
      font-size: 12px;
      cursor: pointer;
    `;

    contrastToggle.addEventListener('click', () => {
      document.body.classList.toggle('high-contrast');
      const isActive = document.body.classList.contains('high-contrast');
      contrastToggle.textContent = isActive ? '일반 모드' : '고대비 모드';
      this.saveUserPreference('highContrast', isActive);
    });

    document.body.appendChild(contrastToggle);

    // 고대비 CSS 추가
    const contrastStyle = document.createElement('style');
    contrastStyle.textContent = `
      .high-contrast {
        filter: contrast(150%) brightness(110%);
      }
      
      .high-contrast * {
        text-shadow: none !important;
        box-shadow: none !important;
      }
      
      .high-contrast a {
        text-decoration: underline !important;
      }
    `;
    document.head.appendChild(contrastStyle);

    // 저장된 설정 적용
    if (this.preferences.highContrast) {
      contrastToggle.click();
    }
  }

  // 폰트 크기 조절
  setupFontSizeControls() {
    const fontControls = document.createElement('div');
    fontControls.className = 'font-size-controls';
    fontControls.style.cssText = `
      position: fixed;
      top: 50px;
      right: 10px;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      gap: 4px;
    `;

    const sizes = [
      { label: 'A-', value: 0.8, desc: '작은 글씨' },
      { label: 'A', value: 1.0, desc: '보통 글씨' },
      { label: 'A+', value: 1.2, desc: '큰 글씨' }
    ];

    sizes.forEach(size => {
      const button = document.createElement('button');
      button.textContent = size.label;
      button.setAttribute('aria-label', size.desc);
      button.style.cssText = `
        padding: 4px 8px;
        background: #666;
        color: #fff;
        border: none;
        border-radius: 3px;
        font-size: 12px;
        cursor: pointer;
      `;

      button.addEventListener('click', () => {
        document.documentElement.style.fontSize = `${size.value}rem`;
        this.saveUserPreference('fontSize', size.value);
        
        // 시각적 피드백
        fontControls.querySelectorAll('button').forEach(b => {
          b.style.background = '#666';
        });
        button.style.background = '#4A90E2';
      });

      fontControls.appendChild(button);
    });

    document.body.appendChild(fontControls);

    // 저장된 폰트 크기 적용
    if (this.preferences.fontSize) {
      document.documentElement.style.fontSize = `${this.preferences.fontSize}rem`;
    }
  }

  // 모션 선호도 설정
  setupMotionPreferences() {
    // prefers-reduced-motion 감지
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    
    if (prefersReducedMotion.matches || this.preferences.reducedMotion) {
      this.disableAnimations();
    }

    // 모션 토글 버튼
    const motionToggle = document.createElement('button');
    motionToggle.textContent = '애니메이션 끄기';
    motionToggle.style.cssText = `
      position: fixed;
      top: 120px;
      right: 10px;
      z-index: 1000;
      padding: 6px 10px;
      background: #666;
      color: #fff;
      border: none;
      border-radius: 3px;
      font-size: 11px;
      cursor: pointer;
    `;

    motionToggle.addEventListener('click', () => {
      const isDisabled = document.body.classList.contains('no-animations');
      if (isDisabled) {
        this.enableAnimations();
        motionToggle.textContent = '애니메이션 끄기';
      } else {
        this.disableAnimations();
        motionToggle.textContent = '애니메이션 켜기';
      }
      this.saveUserPreference('reducedMotion', !isDisabled);
    });

    document.body.appendChild(motionToggle);
  }

  disableAnimations() {
    document.body.classList.add('no-animations');
    const style = document.createElement('style');
    style.id = 'no-animations-style';
    style.textContent = `
      .no-animations *,
      .no-animations *::before,
      .no-animations *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
    `;
    document.head.appendChild(style);
  }

  enableAnimations() {
    document.body.classList.remove('no-animations');
    const style = document.getElementById('no-animations-style');
    if (style) style.remove();
  }

  // 언어 자동 감지
  setupLanguageDetection() {
    const userLang = navigator.language || navigator.userLanguage;
    const supportedLangs = ['ko', 'ja', 'en'];
    const detectedLang = userLang.substring(0, 2);
    
    if (supportedLangs.includes(detectedLang) && 
        !window.location.pathname.includes(`/${detectedLang}/`) &&
        !this.preferences.languageSet) {
      
      this.showLanguageSuggestion(detectedLang);
    }
  }

  showLanguageSuggestion(lang) {
    const langNames = { ko: '한국어', ja: '日本語', en: 'English' };
    
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: #4A90E2;
      color: white;
      padding: 12px 20px;
      border-radius: 6px;
      z-index: 10000;
      font-size: 14px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    `;
    
    notification.innerHTML = `
      ${langNames[lang]}로 보시겠습니까?
      <button onclick="window.location.href='/${lang}/'" 
              style="margin-left: 10px; padding: 4px 8px; background: white; color: #4A90E2; border: none; border-radius: 3px; cursor: pointer;">
        예
      </button>
      <button onclick="this.parentElement.remove(); localStorage.setItem('languageSet', 'true')" 
              style="margin-left: 5px; padding: 4px 8px; background: transparent; color: white; border: 1px solid white; border-radius: 3px; cursor: pointer;">
        아니오
      </button>
    `;
    
    document.body.appendChild(notification);
    
    // 10초 후 자동 제거
    setTimeout(() => {
      if (notification.parentElement) {
        notification.remove();
      }
    }, 10000);
  }

  // 사용자 설정 저장/로드
  loadUserPreferences() {
    try {
      const saved = localStorage.getItem('accessibility-preferences');
      return saved ? JSON.parse(saved) : {};
    } catch (e) {
      return {};
    }
  }

  saveUserPreference(key, value) {
    try {
      this.preferences[key] = value;
      localStorage.setItem('accessibility-preferences', JSON.stringify(this.preferences));
    } catch (e) {
      console.warn('사용자 설정 저장 실패:', e);
    }
  }
}

// 페이지 로드시 초기화
document.addEventListener('DOMContentLoaded', () => {
  window.accessibilityEnhancer = new AccessibilityEnhancer();
});

// 전역 유틸리티 함수들
window.a11y = {
  announce: (message) => {
    if (window.announceToScreenReader) {
      window.announceToScreenReader(message);
    }
  },
  
  focus: (selector) => {
    const element = document.querySelector(selector);
    if (element) {
      element.focus();
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }
};