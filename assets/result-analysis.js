
// Advanced Result Analysis System
class ResultAnalysis {
  constructor() {
    this.personalityTypes = {
      'egen-female': {
        name: '에겐녀',
        description: '감정적이고 직관적인 여성형',
        strengths: ['공감능력', '창의성', '소통능력', '협력적'],
        weaknesses: ['감정기복', '우유부단', '스트레스 민감'],
        careers: ['상담사', '디자이너', '마케터', '교사', '작가'],
        compatibility: ['teto-male', 'egen-male']
      },
      'teto-female': {
        name: '테토녀',
        description: '논리적이고 독립적인 여성형',
        strengths: ['분석력', '결단력', '독립성', '목표지향'],
        weaknesses: ['감정표현 어려움', '완벽주의', '고집'],
        careers: ['개발자', '연구원', '의사', '변호사', '경영자'],
        compatibility: ['egen-male', 'teto-male']
      },
      'egen-male': {
        name: '에겐남',
        description: '감수성이 풍부한 남성형',
        strengths: ['섬세함', '예술적 감각', '배려심', '소통능력'],
        weaknesses: ['우유부단', '자신감 부족', '스트레스 취약'],
        careers: ['예술가', '상담사', '요리사', '간호사', '교육자'],
        compatibility: ['egen-female', 'teto-female']
      },
      'teto-male': {
        name: '테토남',
        description: '전형적인 남성적 특성의 남성형',
        strengths: ['리더십', '논리적 사고', '추진력', '경쟁력'],
        weaknesses: ['감정 억제', '융통성 부족', '스트레스 높음'],
        careers: ['CEO', '군인', '운동선수', '엔지니어', '영업'],
        compatibility: ['egen-female', 'teto-female']
      }
    };
  }

  generateComprehensiveReport(userType, scores, traits, responseData) {
    const typeInfo = this.personalityTypes[userType];
    
    return {
      basic: typeInfo,
      detailedScores: {
        egenScore: scores.egen,
        tetoScore: scores.teto,
        balance: this.calculateBalance(scores.egen, scores.teto),
        dominance: scores.egen > scores.teto ? 'egen' : 'teto'
      },
      traitAnalysis: {
        creativity: traits.creativity,
        logic: traits.logic,
        empathy: traits.empathy,
        leadership: traits.leadership,
        radar: this.generateRadarData(traits)
      },
      recommendations: {
        careers: this.getDetailedCareerInfo(typeInfo.careers),
        relationships: this.getRelationshipAdvice(userType),
        development: this.getDevelopmentPlan(userType, traits)
      },
      insights: {
        avgResponseTime: responseData.avgTime,
        consistency: this.calculateConsistency(responseData.answers),
        confidence: this.calculateConfidence(responseData.times)
      }
    };
  }

  generateRadarData(traits) {
    return {
      labels: ['창의성', '논리성', '공감능력', '리더십', '직관성', '분석력'],
      values: [
        traits.creativity,
        traits.logic,
        traits.empathy,
        traits.leadership,
        (traits.creativity + traits.empathy) / 2, // 직관성
        (traits.logic + traits.leadership) / 2   // 분석력
      ]
    };
  }

  getDetailedCareerInfo(careers) {
    const careerDetails = {
      '상담사': { salary: '3000-5000만원', growth: '높음', satisfaction: '85%' },
      '디자이너': { salary: '3500-7000만원', growth: '보통', satisfaction: '78%' },
      '개발자': { salary: '4000-10000만원', growth: '매우높음', satisfaction: '82%' },
      '의사': { salary: '8000-15000만원', growth: '안정', satisfaction: '76%' },
      // ... 더 많은 직업 정보
    };
    
    return careers.map(career => ({
      name: career,
      details: careerDetails[career] || { salary: '정보없음', growth: '보통', satisfaction: '70%' }
    }));
  }

  calculateBalance(egenScore, tetoScore) {
    const total = egenScore + tetoScore;
    const difference = Math.abs(egenScore - tetoScore);
    return Math.round((1 - difference / total) * 100);
  }

  calculateConsistency(answers) {
    // 응답 패턴의 일관성 측정
    let consistency = 0;
    for (let i = 0; i < answers.length - 1; i++) {
      const diff = Math.abs(answers[i] - answers[i + 1]);
      consistency += diff;
    }
    return Math.max(0, 100 - (consistency / answers.length * 10));
  }

  calculateConfidence(responseTimes) {
    // 응답 시간 기반 확신도 측정
    const avgTime = responseTimes.reduce((sum, time) => sum + time, 0) / responseTimes.length;
    const variance = responseTimes.reduce((sum, time) => sum + Math.pow(time - avgTime, 2), 0) / responseTimes.length;
    
    // 빠르고 일정한 응답 = 높은 확신도
    const speedScore = Math.max(0, 100 - avgTime / 100);
    const consistencyScore = Math.max(0, 100 - Math.sqrt(variance) / 10);
    
    return Math.round((speedScore + consistencyScore) / 2);
  }
}

window.ResultAnalysis = ResultAnalysis;
