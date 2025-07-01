
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
    description: "상상력이 풍부하면서도 결단력이 있으며, 야심차고 독립적인 성격입니다.",
    traits: ["전략적 사고", "독립적", "결단력", "창의적"],
    famous: ["일론 머스크", "마크 저커버그"]
  },
  "INTP": {
    name: "논리술사",
    emoji: "🔬",
    description: "혁신적인 발명가로, 지식에 대한 갈증을 멈출 수 없는 성격입니다.",
    traits: ["논리적", "독창적", "객관적", "유연한"],
    famous: ["알베르트 아인슈타인", "빌 게이츠"]
  },
  "ENTJ": {
    name: "통솔자",
    emoji: "👑",
    description: "대담하고 상상력이 풍부한 지도자로, 길을 찾거나 만들어내는 성격입니다.",
    traits: ["리더십", "결단력", "효율성", "전략적"],
    famous: ["스티브 잡스", "고든 램지"]
  },
  "ENTP": {
    name: "변론가",
    emoji: "💡",
    description: "똑똑하고 호기심이 많은 사색가로, 지적 도전을 거부할 수 없는 성격입니다.",
    traits: ["혁신적", "열정적", "창의적", "논쟁적"],
    famous: ["로버트 다우니 주니어", "라이언 레이놀즈"]
  },
  "INFJ": {
    name: "옹호자",
    emoji: "🌟",
    description: "선의의 옹호자로, 독창성과 원동력, 그리고 높은 이상을 품고 있습니다.",
    traits: ["통찰력", "창의적", "이상주의", "결단력"],
    famous: ["넬슨 만델라", "마틴 루터 킹"]
  },
  "INFP": {
    name: "중재자",
    emoji: "🦋",
    description: "항상 선을 행할 준비가 되어 있는 시적이고 친절한 성격입니다.",
    traits: ["이상주의", "충성심", "적응력", "창의적"],
    famous: ["윌리엄 셰익스피어", "조니 뎁"]
  },
  "ENFJ": {
    name: "주인공",
    emoji: "🌈",
    description: "카리스마가 넘치고 영감을 주는 지도자로, 듣는 이들을 매혹시킵니다.",
    traits: ["카리스마", "이타적", "신뢰할 수 있는", "영감을 주는"],
    famous: ["오프라 윈프리", "버락 오바마"]
  },
  "ENFP": {
    name: "활동가",
    emoji: "🎉",
    description: "열정적이고 창의적인 성격으로, 긍정적으로 삶을 바라보는 사람입니다.",
    traits: ["열정적", "창의적", "사교적", "자유로운"],
    famous: ["로빈 윌리엄스", "엘렌 드제너러스"]
  },
  "ISTJ": {
    name: "물류담당자",
    emoji: "📋",
    description: "현실적이고 사실에 기반해서 행동하며, 신뢰할 수 있는 성격입니다.",
    traits: ["책임감", "체계적", "전통적", "실용적"],
    famous: ["워런 버핏", "조지 워싱턴"]
  },
  "ISFJ": {
    name: "수호자",
    emoji: "🛡️",
    description: "따뜻하고 착한 마음씨를 가진 헌신적인 수호자입니다.",
    traits: ["지지적", "신뢰할 수 있는", "인내심", "관찰력"],
    famous: ["마더 테레사", "케이트 미들턴"]
  },
  "ESTJ": {
    name: "경영자",
    emoji: "💼",
    description: "뛰어난 관리자로서 사람과 일을 관리하는 데 타고난 재능이 있습니다.",
    traits: ["조직적", "실용적", "논리적", "결단력"],
    famous: ["힐러리 클린턴", "판사 주디"]
  },
  "ESFJ": {
    name: "집정관",
    emoji: "🤝",
    description: "인기가 많고 사교적인 성격으로, 언제나 도움을 주고자 합니다.",
    traits: ["사교적", "지지적", "신뢰할 수 있는", "협조적"],
    famous: ["테일러 스위프트", "휴 잭맨"]
  },
  "ISTP": {
    name: "만능재주꾼",
    emoji: "🔧",
    description: "만능재주꾼이자 탐험가로, 손으로 만지고 눈으로 보며 체험하는 것을 좋아합니다.",
    traits: ["실용적", "유연한", "관찰력", "현실적"],
    famous: ["클린트 이스트우드", "브루스 리"]
  },
  "ISFP": {
    name: "모험가",
    emoji: "🎨",
    description: "유연하고 매력적인 예술가로, 늘 새로운 가능성을 탐험할 준비가 되어 있습니다.",
    traits: ["예술적", "민감한", "유연한", "매력적"],
    famous: ["마이클 잭슨", "오드리 헵번"]
  },
  "ESTP": {
    name: "사업가",
    emoji: "🏃",
    description: "에너지 넘치고 관찰력이 뛰어나며, 진정으로 모든 순간을 만끽하는 성격입니다.",
    traits: ["활동적", "현실적", "사교적", "대담한"],
    famous: ["도널드 트럼프", "마돈나"]
  },
  "ESFP": {
    name: "연예인",
    emoji: "🌟",
    description: "자발적이고 열정적이며 사교적인 성격으로, 어디서든 삶을 즐깁니다.",
    traits: ["열정적", "사교적", "낙관적", "유연한"],
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
