
// Enhanced Features for Egen-Teto Test
class EgenTetoEnhanced {
  constructor() {
    this.particles = [];
    this.currentQuestion = 0;
    this.answers = [];
    this.startTime = Date.now();
    this.questionTimes = [];
    
    this.init();
  }

  init() {
    this.createParticles();
    this.setupProgressTracking();
    this.setupKeyboardNavigation();
    this.setupAnalytics();
    this.setupAutoSave();
  }

  createParticles() {
    const particleContainer = document.createElement('div');
    particleContainer.className = 'floating-particles';
    document.body.appendChild(particleContainer);

    for (let i = 0; i < 20; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = Math.random() * 100 + '%';
      particle.style.animationDelay = Math.random() * 6 + 's';
      particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
      particleContainer.appendChild(particle);
    }
  }

  setupProgressTracking() {
    const progressContainer = document.createElement('div');
    progressContainer.className = 'progress-container';
    progressContainer.innerHTML = `
      <div class="progress-bar" style="--progress-width: 0%"></div>
      <div class="progress-text">질문 0/20</div>
    `;
    
    const firstQuestion = document.querySelector('.question-container');
    if (firstQuestion) {
      firstQuestion.parentNode.insertBefore(progressContainer, firstQuestion);
    }
  }

  updateProgress(current, total) {
    const progressBar = document.querySelector('.progress-bar');
    const progressText = document.querySelector('.progress-text');
    
    if (progressBar && progressText) {
      const percentage = (current / total) * 100;
      progressBar.style.setProperty('--progress-width', percentage + '%');
      progressText.textContent = `질문 ${current}/${total}`;
    }
  }

  setupKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
      const options = document.querySelectorAll('.answer-option');
      
      if (e.key >= '1' && e.key <= '4') {
        const index = parseInt(e.key) - 1;
        if (options[index]) {
          options[index].click();
        }
      }
      
      if (e.key === 'Enter') {
        const nextBtn = document.querySelector('.next-btn, .result-btn');
        if (nextBtn) nextBtn.click();
      }
    });
  }

  setupAnalytics() {
    // 질문별 응답 시간 측정
    this.questionStartTime = Date.now();
  }

  recordAnswer(questionId, answer) {
    const responseTime = Date.now() - this.questionStartTime;
    this.questionTimes.push({
      question: questionId,
      answer: answer,
      responseTime: responseTime
    });
    
    // Google Analytics 이벤트 전송
    if (typeof gtag !== 'undefined') {
      gtag('event', 'question_answered', {
        'question_id': questionId,
        'answer': answer,
        'response_time': responseTime
      });
    }
    
    this.questionStartTime = Date.now();
  }

  setupAutoSave() {
    // 로컬 스토리지에 진행상황 저장
    setInterval(() => {
      const testData = {
        answers: this.answers,
        currentQuestion: this.currentQuestion,
        startTime: this.startTime,
        lastSaved: Date.now()
      };
      localStorage.setItem('egenTetoProgress', JSON.stringify(testData));
    }, 10000); // 10초마다 자동저장
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
