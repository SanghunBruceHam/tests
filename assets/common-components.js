
// 공통 테마 및 다국어 처리 모듈
class CommonComponents {
  constructor() {
    this.initTheme();
    this.initLanguageSelector();
  }

  // 다크모드 테마 처리
  initTheme() {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    this.updateTheme(isDarkMode);
    
    // 테마 토글 버튼 이벤트
    document.addEventListener('DOMContentLoaded', () => {
      const themeToggle = document.querySelector('.theme-toggle, #themeToggle');
      if (themeToggle) {
        themeToggle.addEventListener('click', () => {
          const currentMode = localStorage.getItem('darkMode') === 'true';
          this.updateTheme(!currentMode);
        });
      }
    });
  }

  updateTheme(isDarkMode) {
    const body = document.body;
    const icon = document.querySelector('.theme-toggle i, #themeToggle i');
    
    if (isDarkMode) {
      body.setAttribute('data-theme', 'dark');
      if (icon) icon.className = 'fas fa-sun';
    } else {
      body.removeAttribute('data-theme');
      if (icon) icon.className = 'fas fa-moon';
    }
    
    localStorage.setItem('darkMode', isDarkMode);
  }

  // 언어 선택기 초기화
  initLanguageSelector() {
    document.addEventListener('DOMContentLoaded', () => {
      const langButtons = document.querySelectorAll('.lang-btn');
      const currentLang = this.getCurrentLanguage();
      
      langButtons.forEach(btn => {
        const btnLang = this.getLangFromUrl(btn.href);
        if (btnLang === currentLang) {
          btn.classList.add('active');
        }
      });
    });
  }

  getCurrentLanguage() {
    const path = window.location.pathname;
    if (path.includes('/ko/')) return 'ko';
    if (path.includes('/ja/')) return 'ja';
    if (path.includes('/en/')) return 'en';
    return 'ko'; // 기본값
  }

  getLangFromUrl(url) {
    if (url.includes('/ko/')) return 'ko';
    if (url.includes('/ja/')) return 'ja';
    if (url.includes('/en/')) return 'en';
    return 'ko';
  }

  // 공통 SNS 공유 기능
  shareToSNS(platform, text, url = window.location.href) {
    const encodedText = encodeURIComponent(text);
    const encodedUrl = encodeURIComponent(url);
    
    const shareUrls = {
      twitter: `https://twitter.com/intent/tweet?text=${encodedText}&url=${encodedUrl}`,
      facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`,
      threads: `https://www.threads.net/intent/post?text=${encodedText}%20${encodedUrl}`
    };
    
    if (shareUrls[platform]) {
      window.open(shareUrls[platform], '_blank', 'noopener,noreferrer');
    }
  }

  // 결과 복사 기능
  async copyToClipboard(text) {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
        this.showNotification('복사되었습니다!');
      } else {
        this.fallbackCopy(text);
      }
    } catch (err) {
      this.fallbackCopy(text);
    }
  }

  fallbackCopy(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.opacity = '0';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
      document.execCommand('copy');
      this.showNotification('복사되었습니다!');
    } catch (err) {
      this.showNotification('복사 기능을 지원하지 않는 브라우저입니다.');
    }
    
    document.body.removeChild(textArea);
  }

  // 알림 표시
  showNotification(message) {
    // 기존 알림 제거
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
      existingNotification.remove();
    }

    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: var(--accent-color);
      color: white;
      padding: 12px 20px;
      border-radius: 8px;
      z-index: 10000;
      font-weight: 600;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, 2000);
  }

  // Google Analytics 이벤트 추적
  trackEvent(action, category = 'engagement', label = '') {
    if (typeof gtag !== 'undefined') {
      gtag('event', action, {
        event_category: category,
        event_label: label || this.getCurrentLanguage()
      });
    }
  }
}

// 애니메이션 CSS 추가
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
  }
`;
document.head.appendChild(style);

// 전역 인스턴스 생성
window.CommonComponents = new CommonComponents();
