// 향상된 분석 및 모니터링 시스템
class AnalyticsEnhanced {
  constructor() {
    this.config = {
      batchSize: 10,
      flushInterval: 30000, // 30초
      maxRetries: 3,
      debugMode: false
    };
    
    this.eventQueue = [];
    this.sessionData = {
      sessionId: this.generateSessionId(),
      startTime: Date.now(),
      pageViews: 0,
      interactions: 0,
      errors: 0
    };
    
    this.performanceMetrics = {
      pageLoadTime: 0,
      firstContentfulPaint: 0,
      largestContentfulPaint: 0,
      firstInputDelay: 0,
      cumulativeLayoutShift: 0
    };
    
    this.init();
  }

  init() {
    this.setupErrorTracking();
    this.setupPerformanceMonitoring();
    this.setupUserBehaviorTracking();
    this.setupCustomEvents();
    this.startBatchProcessing();
    this.trackPageView();
  }

  generateSessionId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  }

  // 오류 추적
  setupErrorTracking() {
    // JavaScript 오류 추적
    window.addEventListener('error', (event) => {
      this.trackError({
        type: 'javascript_error',
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        stack: event.error?.stack,
        timestamp: Date.now()
      });
    });

    // Promise rejection 추적
    window.addEventListener('unhandledrejection', (event) => {
      this.trackError({
        type: 'promise_rejection',
        message: event.reason?.message || 'Promise rejected',
        stack: event.reason?.stack,
        timestamp: Date.now()
      });
    });

    // 리소스 로딩 오류 추적
    window.addEventListener('error', (event) => {
      if (event.target !== window) {
        this.trackError({
          type: 'resource_error',
          element: event.target.tagName,
          source: event.target.src || event.target.href,
          timestamp: Date.now()
        });
      }
    }, true);
  }

  trackError(errorData) {
    this.sessionData.errors++;
    
    this.queueEvent({
      event_name: 'error_occurred',
      event_category: 'error',
      error_type: errorData.type,
      error_message: errorData.message?.substring(0, 100), // 메시지 길이 제한
      error_source: errorData.filename || errorData.source,
      session_id: this.sessionData.sessionId,
      timestamp: errorData.timestamp
    });

    // 심각한 오류는 즉시 전송
    if (errorData.type === 'javascript_error') {
      this.flushEvents();
    }
  }

  // 성능 모니터링
  setupPerformanceMonitoring() {
    // Core Web Vitals 측정
    this.measureWebVitals();
    
    // 네트워크 상태 모니터링
    this.monitorNetworkStatus();
    
    // 메모리 사용량 추적
    this.trackMemoryUsage();
    
    // 페이지 로드 성능
    window.addEventListener('load', () => {
      setTimeout(() => {
        this.measurePagePerformance();
      }, 0);
    });
  }

  measureWebVitals() {
    // Largest Contentful Paint (LCP)
    const lcpObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      const lastEntry = entries[entries.length - 1];
      this.performanceMetrics.largestContentfulPaint = lastEntry.startTime;
      
      this.queueEvent({
        event_name: 'web_vital_lcp',
        event_category: 'performance',
        value: Math.round(lastEntry.startTime),
        session_id: this.sessionData.sessionId
      });
    });
    
    if ('PerformanceObserver' in window) {
      try {
        lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
      } catch (e) {
        console.warn('LCP measurement not supported');
      }
    }

    // First Input Delay (FID)
    const fidObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach(entry => {
        this.performanceMetrics.firstInputDelay = entry.processingStart - entry.startTime;
        
        this.queueEvent({
          event_name: 'web_vital_fid',
          event_category: 'performance',
          value: Math.round(this.performanceMetrics.firstInputDelay),
          session_id: this.sessionData.sessionId
        });
      });
    });

    if ('PerformanceObserver' in window) {
      try {
        fidObserver.observe({ entryTypes: ['first-input'] });
      } catch (e) {
        console.warn('FID measurement not supported');
      }
    }

    // Cumulative Layout Shift (CLS)
    let clsValue = 0;
    const clsObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach(entry => {
        if (!entry.hadRecentInput) {
          clsValue += entry.value;
        }
      });
      
      this.performanceMetrics.cumulativeLayoutShift = clsValue;
    });

    if ('PerformanceObserver' in window) {
      try {
        clsObserver.observe({ entryTypes: ['layout-shift'] });
      } catch (e) {
        console.warn('CLS measurement not supported');
      }
    }

    // 페이지 언로드 시 CLS 전송
    window.addEventListener('beforeunload', () => {
      if (clsValue > 0) {
        this.queueEvent({
          event_name: 'web_vital_cls',
          event_category: 'performance',
          value: Math.round(clsValue * 1000) / 1000,
          session_id: this.sessionData.sessionId
        });
        this.flushEvents();
      }
    });
  }

  measurePagePerformance() {
    if ('performance' in window && 'getEntriesByType' in performance) {
      const navigation = performance.getEntriesByType('navigation')[0];
      
      if (navigation) {
        const metrics = {
          dns_lookup: navigation.domainLookupEnd - navigation.domainLookupStart,
          tcp_connection: navigation.connectEnd - navigation.connectStart,
          server_response: navigation.responseStart - navigation.requestStart,
          dom_parsing: navigation.domContentLoadedEventEnd - navigation.responseEnd,
          resource_loading: navigation.loadEventStart - navigation.domContentLoadedEventEnd,
          total_load_time: navigation.loadEventEnd - navigation.navigationStart
        };

        Object.entries(metrics).forEach(([metric, value]) => {
          this.queueEvent({
            event_name: 'page_timing',
            event_category: 'performance',
            timing_metric: metric,
            value: Math.round(value),
            session_id: this.sessionData.sessionId
          });
        });
      }
    }
  }

  monitorNetworkStatus() {
    if ('connection' in navigator) {
      const connection = navigator.connection;
      
      this.queueEvent({
        event_name: 'network_info',
        event_category: 'technical',
        connection_type: connection.effectiveType,
        download_speed: Math.round(connection.downlink),
        session_id: this.sessionData.sessionId
      });

      // 연결 상태 변화 감지
      connection.addEventListener('change', () => {
        this.queueEvent({
          event_name: 'network_change',
          event_category: 'technical',
          new_connection_type: connection.effectiveType,
          new_download_speed: Math.round(connection.downlink),
          session_id: this.sessionData.sessionId
        });
      });
    }
  }

  trackMemoryUsage() {
    if ('memory' in performance) {
      const measureMemory = () => {
        const memory = performance.memory;
        
        this.queueEvent({
          event_name: 'memory_usage',
          event_category: 'technical',
          used_memory: Math.round(memory.usedJSHeapSize / 1024 / 1024), // MB
          total_memory: Math.round(memory.totalJSHeapSize / 1024 / 1024), // MB
          memory_limit: Math.round(memory.jsHeapSizeLimit / 1024 / 1024), // MB
          session_id: this.sessionData.sessionId
        });
      };

      // 초기 측정
      measureMemory();
      
      // 주기적 측정 (5분마다)
      setInterval(measureMemory, 300000);
    }
  }

  // 사용자 행동 추적
  setupUserBehaviorTracking() {
    // 클릭 추적
    document.addEventListener('click', (event) => {
      this.trackInteraction('click', event.target);
    });

    // 스크롤 추적
    let scrollTimeout;
    let maxScroll = 0;
    
    window.addEventListener('scroll', () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        const scrollPercent = Math.round(
          (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100
        );
        
        if (scrollPercent > maxScroll) {
          maxScroll = scrollPercent;
          
          // 25%, 50%, 75%, 100% 지점에서 이벤트 발생
          const milestones = [25, 50, 75, 100];
          const milestone = milestones.find(m => scrollPercent >= m && maxScroll < m);
          
          if (milestone) {
            this.queueEvent({
              event_name: 'scroll_milestone',
              event_category: 'engagement',
              scroll_percentage: milestone,
              session_id: this.sessionData.sessionId
            });
          }
        }
      }, 100);
    });

    // 폼 상호작용 추적
    document.addEventListener('focus', (event) => {
      if (event.target.matches('input, textarea, select')) {
        this.trackInteraction('form_focus', event.target);
      }
    }, true);

    // 페이지 가시성 변화 추적
    document.addEventListener('visibilitychange', () => {
      this.queueEvent({
        event_name: 'visibility_change',
        event_category: 'engagement',
        is_visible: !document.hidden,
        session_id: this.sessionData.sessionId
      });
    });

    // 페이지 이탈 시간 추적
    let pageStartTime = Date.now();
    
    window.addEventListener('beforeunload', () => {
      const timeOnPage = Date.now() - pageStartTime;
      
      this.queueEvent({
        event_name: 'time_on_page',
        event_category: 'engagement',
        duration: Math.round(timeOnPage / 1000), // 초
        session_id: this.sessionData.sessionId
      });
      
      this.flushEvents();
    });
  }

  trackInteraction(type, element) {
    this.sessionData.interactions++;
    
    const elementInfo = this.getElementInfo(element);
    
    this.queueEvent({
      event_name: 'user_interaction',
      event_category: 'interaction',
      interaction_type: type,
      element_tag: elementInfo.tag,
      element_class: elementInfo.className,
      element_id: elementInfo.id,
      element_text: elementInfo.text,
      session_id: this.sessionData.sessionId
    });
  }

  getElementInfo(element) {
    return {
      tag: element.tagName?.toLowerCase() || '',
      className: element.className || '',
      id: element.id || '',
      text: (element.textContent || element.value || '').substring(0, 50)
    };
  }

  // 커스텀 이벤트 설정
  setupCustomEvents() {
    // 테스트 관련 이벤트
    this.trackTestEvents();
    
    // A/B 테스트 추적
    this.trackABTests();
    
    // 사용자 선호도 추적
    this.trackUserPreferences();
  }

  trackTestEvents() {
    // 테스트 시작
    document.addEventListener('test_started', (event) => {
      this.queueEvent({
        event_name: 'test_started',
        event_category: 'test',
        test_type: event.detail?.testType || 'unknown',
        session_id: this.sessionData.sessionId
      });
    });

    // 테스트 완료
    document.addEventListener('test_completed', (event) => {
      this.queueEvent({
        event_name: 'test_completed',
        event_category: 'test',
        test_type: event.detail?.testType || 'unknown',
        completion_time: event.detail?.completionTime || 0,
        result_type: event.detail?.resultType || 'unknown',
        session_id: this.sessionData.sessionId
      });
    });

    // 질문 응답
    document.addEventListener('question_answered', (event) => {
      this.queueEvent({
        event_name: 'question_answered',
        event_category: 'test',
        question_number: event.detail?.questionNumber || 0,
        answer_value: event.detail?.answerValue || '',
        response_time: event.detail?.responseTime || 0,
        session_id: this.sessionData.sessionId
      });
    });
  }

  trackABTests() {
    // A/B 테스트 변형 할당
    const abTestVariant = this.getABTestVariant();
    
    if (abTestVariant) {
      this.queueEvent({
        event_name: 'ab_test_assigned',
        event_category: 'experiment',
        test_name: abTestVariant.testName,
        variant: abTestVariant.variant,
        session_id: this.sessionData.sessionId
      });
    }
  }

  getABTestVariant() {
    // 간단한 A/B 테스트 로직 (세션 기반)
    const hash = this.hashCode(this.sessionData.sessionId);
    const variant = hash % 2 === 0 ? 'A' : 'B';
    
    return {
      testName: 'main_layout',
      variant: variant
    };
  }

  hashCode(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash);
  }

  trackUserPreferences() {
    // 테마 선택
    if (localStorage.getItem('theme')) {
      this.queueEvent({
        event_name: 'user_preference',
        event_category: 'preference',
        preference_type: 'theme',
        preference_value: localStorage.getItem('theme'),
        session_id: this.sessionData.sessionId
      });
    }

    // 언어 선택
    if (localStorage.getItem('preferred_language')) {
      this.queueEvent({
        event_name: 'user_preference',
        event_category: 'preference',
        preference_type: 'language',
        preference_value: localStorage.getItem('preferred_language'),
        session_id: this.sessionData.sessionId
      });
    }
  }

  // 페이지뷰 추적
  trackPageView() {
    this.sessionData.pageViews++;
    
    this.queueEvent({
      event_name: 'page_view',
      event_category: 'navigation',
      page_title: document.title,
      page_url: window.location.href,
      page_path: window.location.pathname,
      referrer: document.referrer,
      user_agent: navigator.userAgent,
      screen_resolution: `${screen.width}x${screen.height}`,
      viewport_size: `${window.innerWidth}x${window.innerHeight}`,
      session_id: this.sessionData.sessionId,
      page_view_number: this.sessionData.pageViews
    });
  }

  // 이벤트 큐 관리
  queueEvent(eventData) {
    // 기본 메타데이터 추가
    const enrichedEvent = {
      ...eventData,
      timestamp: eventData.timestamp || Date.now(),
      user_id: this.getUserId(),
      session_duration: Date.now() - this.sessionData.startTime
    };

    this.eventQueue.push(enrichedEvent);

    if (this.config.debugMode) {
      console.log('Event queued:', enrichedEvent);
    }

    // 큐가 가득 찬 경우 즉시 전송
    if (this.eventQueue.length >= this.config.batchSize) {
      this.flushEvents();
    }
  }

  getUserId() {
    // 익명 사용자 ID 생성/유지
    let userId = localStorage.getItem('analytics_user_id');
    if (!userId) {
      userId = 'user_' + Date.now().toString(36) + Math.random().toString(36).substr(2);
      localStorage.setItem('analytics_user_id', userId);
    }
    return userId;
  }

  // 배치 처리
  startBatchProcessing() {
    setInterval(() => {
      if (this.eventQueue.length > 0) {
        this.flushEvents();
      }
    }, this.config.flushInterval);
  }

  async flushEvents() {
    if (this.eventQueue.length === 0) return;

    const eventsToSend = [...this.eventQueue];
    this.eventQueue = [];

    try {
      // Google Analytics로 전송
      await this.sendToGoogleAnalytics(eventsToSend);
      
      // 커스텀 분석 서버로 전송 (있는 경우)
      await this.sendToCustomAnalytics(eventsToSend);
      
      if (this.config.debugMode) {
        console.log(`${eventsToSend.length} events sent successfully`);
      }
    } catch (error) {
      console.error('Failed to send analytics events:', error);
      
      // 실패한 이벤트를 큐에 다시 추가 (재시도 제한)
      eventsToSend.forEach(event => {
        event.retryCount = (event.retryCount || 0) + 1;
        if (event.retryCount <= this.config.maxRetries) {
          this.eventQueue.unshift(event);
        }
      });
    }
  }

  async sendToGoogleAnalytics(events) {
    if (typeof gtag === 'undefined') return;

    events.forEach(event => {
      const { event_name, event_category, ...parameters } = event;
      
      gtag('event', event_name, {
        event_category: event_category,
        ...parameters
      });
    });
  }

  async sendToCustomAnalytics(events) {
    // 커스텀 분석 서버가 있는 경우 구현
    // 예: fetch('/api/analytics', { method: 'POST', body: JSON.stringify(events) });
  }

  // 세션 요약 생성
  generateSessionSummary() {
    return {
      session_id: this.sessionData.sessionId,
      total_page_views: this.sessionData.pageViews,
      total_interactions: this.sessionData.interactions,
      total_errors: this.sessionData.errors,
      session_duration: Date.now() - this.sessionData.startTime,
      performance_metrics: this.performanceMetrics
    };
  }

  // 공개 API
  track(eventName, properties = {}) {
    this.queueEvent({
      event_name: eventName,
      event_category: 'custom',
      ...properties,
      session_id: this.sessionData.sessionId
    });
  }

  setUserProperty(property, value) {
    if (typeof gtag !== 'undefined') {
      gtag('config', 'GA_MEASUREMENT_ID', {
        custom_map: { [property]: value }
      });
    }
  }
}

// 전역 초기화
document.addEventListener('DOMContentLoaded', () => {
  window.analyticsEnhanced = new AnalyticsEnhanced();
});

// 전역 추적 함수
window.track = (eventName, properties) => {
  if (window.analyticsEnhanced) {
    window.analyticsEnhanced.track(eventName, properties);
  }
};