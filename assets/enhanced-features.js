
// Enhanced Features for Egen-Teto Test
class EgenTetoEnhanced {
  constructor() {
    this.particles = [];
    this.currentQuestion = 0;
    this.answers = [];
    this.startTime = Date.now();
    this.questionTimes = [];
    
    // DOM 요소 캐싱
    this.cachedElements = new Map();
    
    // 성능 최적화를 위한 디바운스 함수
    this.debounce = this.createDebounce();
    
    this.init();
  }

  init() {
    // DOM이 준비되면 초기화
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.initializeFeatures());
    } else {
      this.initializeFeatures();
    }
  }

  initializeFeatures() {
    this.cacheCommonElements();
    this.createParticles();
    this.setupProgressTracking();
    this.setupKeyboardNavigation();
    this.setupAnalytics();
    this.setupAutoSave();
  }

  // DOM 요소 캐싱
  cacheCommonElements() {
    const selectors = [
      '.progress-bar',
      '.progress-text',
      '.question-container',
      '.answer-option',
      '.next-btn',
      '.result-btn'
    ];
    
    selectors.forEach(selector => {
      this.cachedElements.set(selector, document.querySelector(selector));
    });
  }

  // 캐시된 요소 가져오기
  getElement(selector) {
    if (this.cachedElements.has(selector)) {
      return this.cachedElements.get(selector);
    }
    
    const element = document.querySelector(selector);
    this.cachedElements.set(selector, element);
    return element;
  }

  // 디바운스 함수 생성
  createDebounce() {
    let timeouts = new Map();
    
    return function(func, delay, key = 'default') {
      clearTimeout(timeouts.get(key));
      timeouts.set(key, setTimeout(func, delay));
    };
  }

  createParticles() {
    // Intersection Observer로 뷰포트에 있을 때만 파티클 생성
    if (!('IntersectionObserver' in window)) return;
    
    const particleContainer = document.createElement('div');
    particleContainer.className = 'floating-particles';
    
    // Fragment 사용으로 DOM 조작 최적화
    const fragment = document.createDocumentFragment();
    
    for (let i = 0; i < 20; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.cssText = `
        left: ${Math.random() * 100}%;
        animation-delay: ${Math.random() * 6}s;
        animation-duration: ${Math.random() * 3 + 3}s;
      `;
      fragment.appendChild(particle);
    }
    
    particleContainer.appendChild(fragment);
    document.body.appendChild(particleContainer);
  }

  setupProgressTracking() {
    const progressContainer = document.createElement('div');
    progressContainer.className = 'progress-container';
    progressContainer.innerHTML = `
      <div class="progress-bar" style="--progress-width: 0%"></div>
      <div class="progress-text">질문 0/20</div>
    `;
    
    const firstQuestion = this.getElement('.question-container');
    if (firstQuestion && firstQuestion.parentNode) {
      firstQuestion.parentNode.insertBefore(progressContainer, firstQuestion);
      
      // 캐시 업데이트
      this.cachedElements.set('.progress-bar', progressContainer.querySelector('.progress-bar'));
      this.cachedElements.set('.progress-text', progressContainer.querySelector('.progress-text'));
    }
  }

  updateProgress(current, total) {
    const progressBar = this.getElement('.progress-bar');
    const progressText = this.getElement('.progress-text');
    
    if (progressBar && progressText) {
      const percentage = (current / total) * 100;
      
      // requestAnimationFrame으로 애니메이션 최적화
      requestAnimationFrame(() => {
        progressBar.style.setProperty('--progress-width', percentage + '%');
        progressText.textContent = `질문 ${current}/${total}`;
      });
    }
  }

  setupKeyboardNavigation() {
    // 이벤트 위임 사용으로 성능 최적화
    document.addEventListener('keydown', this.debounce((e) => {
      this.handleKeyboardInput(e);
    }, 100, 'keyboard'));
  }

  handleKeyboardInput(e) {
    if (e.key >= '1' && e.key <= '4') {
      const options = document.querySelectorAll('.answer-option');
      const index = parseInt(e.key) - 1;
      if (options[index]) {
        options[index].click();
      }
    }
    
    if (e.key === 'Enter') {
      const nextBtn = this.getElement('.next-btn') || this.getElement('.result-btn');
      if (nextBtn) nextBtn.click();
    }
  }

  setupAnalytics() {
    this.questionStartTime = Date.now();
    
    // 성능 메트릭 수집
    this.performanceMetrics = {
      renderTime: 0,
      interactionTime: 0,
      memoryUsage: this.getMemoryUsage()
    };
  }

  getMemoryUsage() {
    if ('memory' in performance) {
      return {
        used: performance.memory.usedJSHeapSize,
        total: performance.memory.totalJSHeapSize
      };
    }
    return null;
  }

  recordAnswer(questionId, answer) {
    const responseTime = Date.now() - this.questionStartTime;
    this.questionTimes.push({
      question: questionId,
      answer: answer,
      responseTime: responseTime,
      timestamp: Date.now()
    });
    
    // 배치 처리로 Analytics 이벤트 전송
    this.debounce(() => {
      if (typeof gtag !== 'undefined') {
        gtag('event', 'question_answered', {
          'question_id': questionId,
          'answer': answer,
          'response_time': responseTime,
          'memory_usage': this.getMemoryUsage()
        });
      }
    }, 500, 'analytics');
    
    this.questionStartTime = Date.now();
  }

  setupAutoSave() {
    // Idle callback 사용으로 성능 최적화
    const saveData = () => {
      const testData = {
        answers: this.answers,
        currentQuestion: this.currentQuestion,
        startTime: this.startTime,
        lastSaved: Date.now(),
        performanceMetrics: this.performanceMetrics
      };
      
      try {
        localStorage.setItem('egenTetoProgress', JSON.stringify(testData));
      } catch (e) {
        console.warn('LocalStorage quota exceeded:', e);
        // 오래된 데이터 정리
        this.cleanupOldData();
      }
    };

    // 10초마다 자동저장 (requestIdleCallback 사용)
    setInterval(() => {
      if ('requestIdleCallback' in window) {
        requestIdleCallback(saveData);
      } else {
        saveData();
      }
    }, 10000);
  }

  cleanupOldData() {
    const keys = Object.keys(localStorage);
    const testDataKeys = keys.filter(key => key.includes('Progress'));
    
    // 24시간 이상 된 데이터 삭제
    testDataKeys.forEach(key => {
      try {
        const data = JSON.parse(localStorage.getItem(key));
        if (Date.now() - data.lastSaved > 24 * 60 * 60 * 1000) {
          localStorage.removeItem(key);
        }
      } catch (e) {
        localStorage.removeItem(key);
      }
    });
  }

  loadProgress() {
    const saved = localStorage.getItem('egenTetoProgress');
    if (saved) {
      const data = JSON.parse(saved);
      // 24시간 이내 데이터만 복원
      if (Date.now() - data.lastSaved < 24 * 60 * 60 * 1000) {
        return data;
      }
    }
    return null;
  }

  generateDetailedResult(answers) {
    const egenScore = this.calculateEgenScore(answers);
    const tetoScore = this.calculateTetoScore(answers);
    
    // 세부 분석 추가
    const analysis = {
      primary: egenScore > tetoScore ? 'egen' : 'teto',
      balance: Math.abs(egenScore - tetoScore),
      dominant: Math.max(egenScore, tetoScore),
      traits: this.analyzeTraits(answers),
      compatibility: this.calculateCompatibility(answers),
      careerSuggestions: this.getCareerSuggestions(answers),
      avgResponseTime: this.questionTimes.reduce((sum, q) => sum + q.responseTime, 0) / this.questionTimes.length
    };
    
    return analysis;
  }

  analyzeTraits(answers) {
    return {
      creativity: this.calculateTraitScore(answers, [1, 5, 9, 13, 17]),
      logic: this.calculateTraitScore(answers, [2, 6, 10, 14, 18]),
      empathy: this.calculateTraitScore(answers, [3, 7, 11, 15, 19]),
      leadership: this.calculateTraitScore(answers, [4, 8, 12, 16, 20])
    };
  }

  calculateTraitScore(answers, questionIndices) {
    let score = 0;
    questionIndices.forEach(index => {
      if (answers[index - 1]) {
        score += answers[index - 1];
      }
    });
    return Math.round((score / (questionIndices.length * 4)) * 100);
  }
}

// 페이지 로드시 초기화
document.addEventListener('DOMContentLoaded', () => {
  window.egenTetoEnhanced = new EgenTetoEnhanced();
});
