// 모듈 지연 로딩 및 관리 시스템
class ModuleLoader {
  constructor() {
    this.loadedModules = new Set();
    this.loadingPromises = new Map();
  }

  // 모듈 동적 로딩
  async loadModule(moduleName, condition = true) {
    if (!condition) return null;
    
    if (this.loadedModules.has(moduleName)) {
      return true;
    }
    
    if (this.loadingPromises.has(moduleName)) {
      return this.loadingPromises.get(moduleName);
    }
    
    const promise = this._loadScript(moduleName);
    this.loadingPromises.set(moduleName, promise);
    
    try {
      await promise;
      this.loadedModules.add(moduleName);
      this.loadingPromises.delete(moduleName);
      return true;
    } catch (error) {
      this.loadingPromises.delete(moduleName);
      console.error(`Failed to load module ${moduleName}:`, error);
      return false;
    }
  }

  // 스크립트 동적 로딩
  _loadScript(moduleName) {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = `/assets/${moduleName}.js`;
      script.async = true;
      
      script.onload = () => resolve();
      script.onerror = () => reject(new Error(`Script load failed: ${moduleName}`));
      
      document.head.appendChild(script);
    });
  }

  // 페이지 타입별 필수 모듈 로딩
  async loadPageModules() {
    const pageType = this._detectPageType();
    const modules = this._getModulesForPage(pageType);
    
    // 병렬 로딩
    const loadPromises = modules.map(module => this.loadModule(module.name, module.condition));
    await Promise.allSettled(loadPromises);
  }

  // 페이지 타입 감지
  _detectPageType() {
    const path = window.location.pathname;
    
    if (path.includes('/test') && path.includes('.html')) return 'test';
    if (path.includes('/index.html') || path === '/') return 'index';
    if (path.includes('/about')) return 'about';
    
    return 'default';
  }

  // 페이지별 모듈 매핑
  _getModulesForPage(pageType) {
    const moduleConfig = {
      test: [
        { name: 'enhanced-features', condition: true },
        { name: 'result-analysis', condition: true },
        { name: 'chart-visualization', condition: document.querySelector('.chart-container') },
        { name: 'analytics-enhanced', condition: true }
      ],
      index: [
        { name: 'common-components', condition: true },
        { name: 'seo-optimizer', condition: true },
        { name: 'analytics-enhanced', condition: true }
      ],
      default: [
        { name: 'accessibility', condition: true },
        { name: 'common-components', condition: true }
      ]
    };

    return moduleConfig[pageType] || moduleConfig.default;
  }

  // 사용자 상호작용 기반 지연 로딩
  async loadOnInteraction(moduleName, triggerSelector, eventType = 'click') {
    const trigger = document.querySelector(triggerSelector);
    if (!trigger) return;

    const loadHandler = async () => {
      await this.loadModule(moduleName);
      trigger.removeEventListener(eventType, loadHandler);
    };

    trigger.addEventListener(eventType, loadHandler, { once: true });
  }

  // Intersection Observer 기반 지연 로딩
  loadOnVisible(moduleName, targetSelector) {
    const target = document.querySelector(targetSelector);
    if (!target) return;

    const observer = new IntersectionObserver(async (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          await this.loadModule(moduleName);
          observer.disconnect();
          break;
        }
      }
    }, { rootMargin: '50px' });

    observer.observe(target);
  }
}

// 전역 인스턴스
window.moduleLoader = new ModuleLoader();

// DOM 로드 완료 후 페이지별 모듈 로딩
document.addEventListener('DOMContentLoaded', async () => {
  await window.moduleLoader.loadPageModules();
  
  // 필요시 추가 지연 로딩 설정
  window.moduleLoader.loadOnVisible('chart-visualization', '.result-section');
  window.moduleLoader.loadOnInteraction('result-analysis', '.share-button', 'click');
});