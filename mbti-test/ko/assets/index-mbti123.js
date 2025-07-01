import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';

// MBTI 질문 데이터
const questions = [
  {
    text: "새로운 사람들과 만나는 것을 좋아한다.",
    dimension: "EI", // E(외향) vs I(내향)
    direction: "E"
  },
  {
    text: "계획을 세우고 그에 따라 행동하는 것을 선호한다.",
    dimension: "JP", // J(판단) vs P(인식)
    direction: "J"
  },
  {
    text: "논리적 분석보다는 감정을 중시해서 결정한다.",
    dimension: "TF", // T(사고) vs F(감정)
    direction: "F"
  },
  {
    text: "구체적인 사실보다는 가능성과 의미를 중시한다.",
    dimension: "SN", // S(감각) vs N(직관)
    direction: "N"
  },
  {
    text: "혼자 있는 시간이 에너지를 충전해준다.",
    dimension: "EI",
    direction: "I"
  },
  {
    text: "즉흥적이고 유연한 접근을 선호한다.",
    dimension: "JP",
    direction: "P"
  },
  {
    text: "객관적인 기준으로 판단하는 것을 중요하게 생각한다.",
    dimension: "TF",
    direction: "T"
  },
  {
    text: "현실적이고 실용적인 해결책을 선호한다.",
    dimension: "SN",
    direction: "S"
  },
  {
    text: "파티나 모임에서 활기를 얻는다.",
    dimension: "EI",
    direction: "E"
  },
  {
    text: "마감일을 정해두고 체계적으로 일하는 것을 좋아한다.",
    dimension: "JP",
    direction: "J"
  },
  {
    text: "다른 사람의 감정을 배려해서 의사결정한다.",
    dimension: "TF",
    direction: "F"
  },
  {
    text: "새로운 아이디어와 가능성에 관심이 많다.",
    dimension: "SN",
    direction: "N"
  },
  {
    text: "조용한 환경에서 깊이 생각하는 것을 선호한다.",
    dimension: "EI",
    direction: "I"
  },
  {
    text: "상황에 따라 융통성 있게 대응하는 것을 좋아한다.",
    dimension: "JP",
    direction: "P"
  },
  {
    text: "원칙과 일관성을 중시한다.",
    dimension: "TF",
    direction: "T"
  },
  {
    text: "세부사항과 구체적인 정보에 주의를 기울인다.",
    dimension: "SN",
    direction: "S"
  },
  {
    text: "사람들과 대화하며 아이디어를 발전시킨다.",
    dimension: "EI",
    direction: "E"
  },
  {
    text: "미리 계획하고 준비하는 것을 선호한다.",
    dimension: "JP",
    direction: "J"
  },
  {
    text: "조화와 협력을 중시한다.",
    dimension: "TF",
    direction: "F"
  },
  {
    text: "전체적인 그림과 패턴을 보는 것을 좋아한다.",
    dimension: "SN",
    direction: "N"
  }
];

// MBTI 결과 데이터
const mbtiResults = {
  "INTJ": {
    name: "건축가",
    emoji: "🏗️",
    description: "혼자서도 척척! 머릿속에 이미 완벽한 계획이 다 있는 전략가 타입. '나만의 방식'이 확실한 독립적인 마스터마인드입니다.",
    traits: ["천재적 전략가", "혼자가 편한", "완벽주의", "미래 설계사"],
    famous: ["일론 머스크", "마크 저커버그"]
  },
  "INTP": {
    name: "논리술사",
    emoji: "🔬",
    description: "호기심 대장! '왜지?' '어떻게?' 질문이 끝이 없는 진짜 지식 덕후. 새로운 아이디어가 샘솟는 창의적 천재입니다.",
    traits: ["궁금한 게 많은", "창의적 천재", "논리 마스터", "자유로운 영혼"],
    famous: ["알베르트 아인슈타인", "빌 게이츠"]
  },
  "ENTJ": {
    name: "통솔자",
    emoji: "👑",
    description: "타고난 리더! 목표가 생기면 무조건 달성하는 추진력甲. 주변 사람들을 이끌어가는 카리스마 넘치는 보스입니다.",
    traits: ["천상 리더", "목표 달성기계", "카리스마 만점", "효율성 킹"],
    famous: ["스티브 잡스", "고든 램지"]
  },
  "ENTP": {
    name: "변론가",
    emoji: "💡",
    description: "말하는 게 너무 재밌어! 토론하고 새로운 아이디어 내는 걸 좋아하는 에너지 넘치는 아이디어 뱅크입니다.",
    traits: ["아이디어 뱅크", "말빨 좋은", "도전 정신", "창의력 폭발"],
    famous: ["로버트 다우니 주니어", "라이언 레이놀즈"]
  },
  "INFJ": {
    name: "옹호자",
    emoji: "🌟",
    description: "따뜻한 마음의 소유자! 다른 사람의 마음을 잘 알아주고, 세상을 더 좋게 만들고 싶어하는 이상주의적 힐러입니다.",
    traits: ["공감 능력甲", "이상주의자", "따뜻한 조언자", "깊은 통찰력"],
    famous: ["넬슨 만델라", "마틴 루터 킹"]
  },
  "INFP": {
    name: "중재자",
    emoji: "🦋",
    description: "감수성 풍부한 낭만주의자! 자신만의 가치관이 확고하고, 예술적이고 창의적인 일을 좋아하는 순수한 영혼입니다.",
    traits: ["감성적인", "개성 강한", "예술적 감각", "순수한 마음"],
    famous: ["윌리엄 셰익스피어", "조니 뎁"]
  },
  "ENFJ": {
    name: "주인공",
    emoji: "🌈",
    description: "분위기 메이커! 다른 사람을 도와주는 걸 좋아하고, 긍정 에너지로 주변을 밝게 만드는 천생 인싸입니다.",
    traits: ["분위기 메이커", "도움 주는 게 좋은", "긍정 에너지", "인기쟁이"],
    famous: ["오프라 윈프리", "버락 오바마"]
  },
  "ENFP": {
    name: "활동가",
    emoji: "🎉",
    description: "에너지 폭발! 새로운 사람, 새로운 경험을 좋아하는 자유로운 영혼. 열정적이고 낙천적인 라이프의 주인공입니다.",
    traits: ["에너지 폭발", "새로운 거 좋아", "자유로운 영혼", "긍정 마인드"],
    famous: ["로빈 윌리엄스", "엘렌 드제너러스"]
  },
  "ISTJ": {
    name: "물류담당자",
    emoji: "📋",
    description: "믿고 맡기는 그 사람! 계획적이고 책임감 강해서 주변에서 든든한 존재. 전통과 질서를 중시하는 성실한 일꾼입니다.",
    traits: ["믿고 맡기는", "계획적인", "책임감 强", "성실함의 대명사"],
    famous: ["워런 버핏", "조지 워싱턴"]
  },
  "ISFJ": {
    name: "수호자",
    emoji: "🛡️",
    description: "따뜻한 케어러! 다른 사람을 챙겨주는 걸 좋아하고, 조용히 뒤에서 든든하게 지켜주는 마음씨 좋은 수호천사입니다.",
    traits: ["남 챙기는 게 취미", "온화한 성격", "든든한 지원군", "배려심 만점"],
    famous: ["마더 테레사", "케이트 미들턴"]
  },
  "ESTJ": {
    name: "경영자",
    emoji: "💼",
    description: "조직의 핵심! 체계적이고 현실적이어서 일 처리가 깔끔한 타입. 팀을 이끌어 목표를 달성하는 프로 매니저입니다.",
    traits: ["조직의 기둥", "일 처리 깔끔", "현실적 사고", "프로 매니저"],
    famous: ["힐러리 클린턴", "판사 주디"]
  },
  "ESFJ": {
    name: "집정관",
    emoji: "🤝",
    description: "사교계의 달인! 사람들과 어울리는 걸 좋아하고, 분위기를 화목하게 만드는 천성의 사교가입니다.",
    traits: ["사교계 달인", "화목한 분위기", "인기 많은", "협력의 왕"],
    famous: ["테일러 스위프트", "휴 잭맨"]
  },
  "ISTP": {
    name: "만능재주꾼",
    emoji: "🔧",
    description: "손재주 좋은 쿨가이! 혼자서도 뭐든 뚝딱 만들어내고, 위기상황에서도 침착한 실용적 문제해결사입니다.",
    traits: ["손재주 좋은", "쿨한 성격", "실용적 사고", "위기대응 능력자"],
    famous: ["클린트 이스트우드", "브루스 리"]
  },
  "ISFP": {
    name: "모험가",
    emoji: "🎨",
    description: "예술가 기질! 자신만의 스타일이 확실하고, 아름다운 것을 추구하는 감성적이고 매력적인 아티스트입니다.",
    traits: ["예술가 기질", "독특한 매력", "감성적인", "아름다움 추구"],
    famous: ["마이클 잭슨", "오드리 헵번"]
  },
  "ESTP": {
    name: "사업가",
    emoji: "🏃",
    description: "액션파! 지금 이 순간을 즐기는 걸 좋아하고, 새로운 도전을 두려워하지 않는 에너지 넘치는 행동대장입니다.",
    traits: ["지금이 좋은", "도전 정신", "에너지 넘치는", "행동대장"],
    famous: ["도널드 트럼프", "마돈나"]
  },
  "ESFP": {
    name: "연예인",
    emoji: "🌟",
    description: "분위기 UP! 어디서든 재미있게 만드는 엔터테이너. 사람들과 함께 있을 때 가장 빛나는 천생 스타입니다.",
    traits: ["분위기 메이커", "재미있는", "사람 좋아하는", "천생 스타"],
    famous: ["윌 스미스", "마릴린 먼로"]
  }
};

function MBTITest() {
  const [currentStep, setCurrentStep] = useState('start'); // 'start', 'test', 'result'
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  const startTest = () => {
    setCurrentStep('test');
    setCurrentQuestion(0);
    setAnswers({});
  };

  const answerQuestion = (score) => {
    const question = questions[currentQuestion];
    const newAnswers = {
      ...answers,
      [question.dimension]: (answers[question.dimension] || 0) + 
        (question.direction === 'E' || question.direction === 'S' || 
         question.direction === 'T' || question.direction === 'J' ? score : -score)
    };

    setAnswers(newAnswers);

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      calculateResult(newAnswers);
    }
  };

  const calculateResult = (finalAnswers) => {
    const mbtiType = 
      (finalAnswers.EI > 0 ? 'E' : 'I') +
      (finalAnswers.SN > 0 ? 'S' : 'N') +
      (finalAnswers.TF > 0 ? 'T' : 'F') +
      (finalAnswers.JP > 0 ? 'J' : 'P');

    setResult(mbtiResults[mbtiType]);
    setCurrentStep('result');
  };

  const resetTest = () => {
    setCurrentStep('start');
    setCurrentQuestion(0);
    setAnswers({});
    setResult(null);
  };

  const shareResult = (platform) => {
    const text = `나의 MBTI 결과: ${result.emoji} ${result.name} - ${result.description}`;
    const url = window.location.href;

    if (platform === 'twitter') {
      window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`);
    } else if (platform === 'facebook') {
      window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`);
    } else if (platform === 'copy') {
      navigator.clipboard.writeText(`${text}\n\n테스트 링크: ${url}`);
      alert('결과가 클립보드에 복사되었습니다!');
    }
  };

  const goHome = () => {
    window.location.href = '/ko/';
  };

  const progressPercentage = ((currentQuestion + 1) / questions.length) * 100;

  if (currentStep === 'start') {
    return (
      <div className="container">
        <div className="test-card">
          <div className="logo">🧠</div>
          <h1>MBTI 성격 유형 테스트</h1>
          <p className="subtitle">
            20문항으로 알아보는 나의 성격 유형<br/>
            16가지 MBTI 중 당신은 어떤 타입일까요?
          </p>
          <button className="start-btn" onClick={startTest}>
            테스트 시작하기
          </button>
        </div>
      </div>
    );
  }

  if (currentStep === 'test') {
    const question = questions[currentQuestion];
    return (
      <div className="container">
        <div className="test-card">
          <div className="progress-bar">
            <div className="progress-fill" style={{width: `${progressPercentage}%`}}></div>
          </div>
          <div className="question-number">
            {currentQuestion + 1} / {questions.length}
          </div>
          <div className="question-text">
            {question.text}
          </div>
          <div className="answers-grid">
            <button className="answer-btn" onClick={() => answerQuestion(2)}>
              매우 그렇다
            </button>
            <button className="answer-btn" onClick={() => answerQuestion(1)}>
              그렇다
            </button>
            <button className="answer-btn" onClick={() => answerQuestion(-1)}>
              그렇지 않다
            </button>
            <button className="answer-btn" onClick={() => answerQuestion(-2)}>
              전혀 그렇지 않다
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (currentStep === 'result') {
    return (
      <div className="container">
        <div className="test-card result-card">
          <div className="result-type">{result.emoji}</div>
          <div className="result-title">{result.name}</div>
          <div className="result-description">{result.description}</div>

          <div className="traits-grid">
            {result.traits.map((trait, index) => (
              <div key={index} className="trait-badge">{trait}</div>
            ))}
          </div>

          <div className="share-section">
            <div className="share-title">결과 공유하기</div>
            <div className="share-buttons">
              <button className="share-btn" onClick={() => shareResult('twitter')}>
                트위터
              </button>
              <button className="share-btn" onClick={() => shareResult('facebook')}>
                페이스북
              </button>
              <button className="share-btn" onClick={() => shareResult('copy')}>
                복사하기
              </button>
              <button className="share-btn" onClick={goHome}>
                다른 테스트
              </button>
            </div>
          </div>

          <button className="retry-btn" onClick={resetTest}>
            다시 테스트하기
          </button>
        </div>
      </div>
    );
  }

  return null;
}

// React 앱 마운트
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<MBTITest />);