// Simple Quiz Engine (vanilla JS)
// Expects window.quizConfig = {
//   id, title, subtitle, questions: [{id, text, options: [{text, weights:{[category]:score}}]}],
//   categories: { [categoryId]: { name, description } },
//   share: { title, hashtags }
// }

(function(){
  const locale = (function(){
    const lang = (document.documentElement.getAttribute('lang') || '').toLowerCase();
    if (lang.startsWith('ja')) return 'ja';
    if (lang.startsWith('en')) return 'en';
    return 'ko';
  })();

  const I18N = {
    ko: {
      prev: '◀ 이전',
      next: '다음 ▶',
      submit: '결과 보기',
      selectOne: '하나를 선택해주세요.',
      resultBadge: 'RESULT',
      shareX: 'X (Twitter)',
      copy: '링크 복사',
      copied: '링크를 복사했어요!\n친구에게 바로 공유해보세요.',
      copyFailed: '복사 실패. 주소창에서 직접 복사해주세요.',
      tryAgain: '다시 하기',
      shareFacebook: 'Facebook',
      shareLine: 'LINE',
      shareThreads: 'Threads',
      shareNative: '공유',
      goHome: '메인으로',
      allTests: '모든 테스트'
    },
    ja: {
      prev: '◀ 前へ',
      next: '次へ ▶',
      submit: '結果を見る',
      selectOne: '1つ選んでください。',
      resultBadge: '結果',
      shareX: 'X (Twitter)',
      copy: 'リンクをコピー',
      copied: 'リンクをコピーしました！\n友だちにシェアしましょう。',
      copyFailed: 'コピーに失敗しました。アドレスバーからコピーしてください。',
      tryAgain: 'もう一度',
      shareFacebook: 'Facebook',
      shareLine: 'LINE',
      shareThreads: 'Threads',
      shareNative: '共有',
      goHome: 'ホームへ',
      allTests: 'すべてのテスト'
    },
    en: {
      prev: '◀ Prev',
      next: 'Next ▶',
      submit: 'See Result',
      selectOne: 'Please select one.',
      resultBadge: 'RESULT',
      shareX: 'X (Twitter)',
      copy: 'Copy link',
      copied: 'Link copied!\nShare it with your friends.',
      copyFailed: 'Copy failed. Please copy from the address bar.',
      tryAgain: 'Try Again',
      shareFacebook: 'Facebook',
      shareLine: 'LINE',
      shareThreads: 'Threads',
      shareNative: 'Share',
      goHome: 'Go Home',
      allTests: 'All Tests'
    }
  }[locale];
  function $(sel, root=document){ return root.querySelector(sel); }
  function $all(sel, root=document){ return Array.from(root.querySelectorAll(sel)); }

  function renderQuiz(root, config){
    root.innerHTML = '';

    const header = document.createElement('div');
    header.className = 'q-header';
    header.innerHTML = `
      <h1>${escapeHtml(config.title)}</h1>
      ${config.subtitle ? `<p class="muted">${escapeHtml(config.subtitle)}</p>` : ''}
    `;
    root.appendChild(header);

    const progress = document.createElement('div');
    progress.className = 'q-progress';
    progress.innerHTML = `<div class="bar" style="width:0%"></div>`;
    root.appendChild(progress);

    const qwrap = document.createElement('div');
    qwrap.className = 'q-wrap';
    qwrap.setAttribute('role', 'region');
    qwrap.setAttribute('aria-live', 'polite');
    root.appendChild(qwrap);

    const actions = document.createElement('div');
    actions.className = 'q-actions';
    actions.innerHTML = `
      <button class="prev" disabled>${I18N.prev}</button>
      <button class="next">${I18N.next}</button>
      <button class="submit" style="display:none">${I18N.submit}</button>
    `;
    root.appendChild(actions);

    const prevBtn = $('.prev', actions);
    const nextBtn = $('.next', actions);
    const submitBtn = $('.submit', actions);

    let idx = 0;
    const answers = new Map();
    const storeKey = `quiz:${config.id}`;

    // restore state if present
    try {
      const saved = JSON.parse(sessionStorage.getItem(storeKey) || 'null');
      if (saved && Array.isArray(saved.answers)){
        idx = Math.max(0, Math.min(saved.idx || 0, (config.questions.length - 1)));
        saved.answers.forEach(a => answers.set(a.questionId, a));
      }
    } catch(e) {}
    const total = config.questions.length;

    function updateProgress(){
      const pct = Math.round(((idx) / total) * 100);
      const bar = $('.bar', progress);
      bar.style.transition = 'width 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
      bar.style.width = pct + '%';
      
      // Add visual feedback for progress
      if (pct > 0) {
        bar.style.background = `linear-gradient(90deg, #4ade80 0%, #22c55e ${Math.max(20, pct)}%, #16a34a 100%)`;
      }
    }

    function renderQuestion(){
      const q = config.questions[idx];
      qwrap.innerHTML = '';
      const card = document.createElement('div');
      card.className = 'q-card';
      const qTitleId = `q_title_${idx+1}`;
      card.innerHTML = `<div class="q-num">Q${idx+1}/${total}</div><h2 id="${qTitleId}">${escapeHtml(q.text)}</h2>`;

      const list = document.createElement('div');
      list.className = 'q-options';
      list.setAttribute('role', 'radiogroup');
      list.setAttribute('aria-labelledby', qTitleId);
      q.options.forEach((opt, i) => {
        const id = `${q.id}_${i}`;
        const item = document.createElement('label');
        item.className = 'q-option';
        item.innerHTML = `
          <input type="radio" name="${q.id}" id="${id}">
          <span>${escapeHtml(opt.text)}</span>
        `;
        list.appendChild(item);
        
        // Add enhanced interaction feedback
        const input = item.querySelector('input');
        input.addEventListener('change', () => {
          // Visual feedback for selection
          const allOptions = list.querySelectorAll('.q-option');
          allOptions.forEach(opt => opt.classList.remove('selected'));
          if (input.checked) {
            item.classList.add('selected');
            item.style.transform = 'scale(1.02)';
            setTimeout(() => {
              item.style.transform = '';
            }, 200);
          }
        });
      });
      card.appendChild(list);
      qwrap.appendChild(card);
      
      // Add smooth slide-in animation
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      card.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
      setTimeout(() => {
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, 50);

      // restore selection with visual feedback
      if (answers.has(q.id)){
        const savedIdx = answers.get(q.id).index;
        const input = $(`input#${q.id}_${savedIdx}`, qwrap);
        if (input) {
          input.checked = true;
          input.closest('.q-option').classList.add('selected');
        }
      }

      prevBtn.disabled = idx === 0;
      nextBtn.style.display = idx < total - 1 ? '' : 'none';
      submitBtn.style.display = idx === total - 1 ? '' : 'none';
      updateProgress();

      // keyboard navigation: up/down to move selection
      list.addEventListener('keydown', (ev) => {
        if (!['ArrowDown','ArrowUp'].includes(ev.key)) return;
        const radios = Array.from(list.querySelectorAll(`input[name="${q.id}"]`));
        const current = radios.findIndex(r => r.checked);
        let nextIndex = current;
        if (ev.key === 'ArrowDown') nextIndex = Math.min(radios.length-1, current < 0 ? 0 : current+1);
        if (ev.key === 'ArrowUp') nextIndex = Math.max(0, current < 0 ? 0 : current-1);
        radios[nextIndex]?.focus();
        radios[nextIndex].checked = true;
        ev.preventDefault();
      });
    }

    function currentSelection(){
      const q = config.questions[idx];
      const checked = $(`input[name="${q.id}"]:checked`, qwrap);
      if (!checked) return null;
      const parts = checked.id.split('_');
      const optIdx = parseInt(parts[parts.length-1],10);
      return { questionId: q.id, index: optIdx };
    }

    nextBtn.addEventListener('click', () => {
      const sel = currentSelection();
      if (!sel){ alert(I18N.selectOne); return; }
      answers.set(sel.questionId, sel);
      // persist state
      try { sessionStorage.setItem(storeKey, JSON.stringify({ idx, answers: Array.from(answers.values()) })); } catch(e) {}
      if (window.track){
        document.dispatchEvent(new CustomEvent('question_answered', { detail: { questionNumber: idx+1, answerValue: sel.index, responseTime: 0 }}));
      }
      idx = Math.min(idx+1, total-1);
      renderQuestion();
    });

    prevBtn.addEventListener('click', () => {
      idx = Math.max(idx-1, 0);
      renderQuestion();
    });

    submitBtn.addEventListener('click', () => {
      const sel = currentSelection();
      if (!sel){ alert(I18N.selectOne); return; }
      answers.set(sel.questionId, sel);
      
      // Show loading state
      submitBtn.innerHTML = '<div style="display: inline-flex; align-items: center; gap: 8px;"><div class="loading-spinner"></div>결과 분석 중...</div>';
      submitBtn.disabled = true;
      
      // Add loading animation styles if not exists
      if (!document.querySelector('#loading-spinner-styles')) {
        const style = document.createElement('style');
        style.id = 'loading-spinner-styles';
        style.textContent = `
          .loading-spinner {
            width: 16px; height: 16px;
            border: 2px solid #f3f3f3;
            border-top: 2px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
          }
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `;
        document.head.appendChild(style);
      }
      
      // Simulate processing time for better UX
      setTimeout(() => {
        const result = computeResult(config, answers);
        renderResult(root, config, result);
        
        // update URL with result for share/deeplink
        try{
          const url = new URL(window.location.href);
          url.searchParams.set('r', result.categoryId);
          history.replaceState(null, '', url.toString());
        }catch(e){}
        // clear saved state on finish
        try { sessionStorage.removeItem(storeKey); } catch(e) {}
      }, 1200); // 1.2초 로딩 시뮬레이션
    });

    // start
    if (window.track){
      document.dispatchEvent(new CustomEvent('test_started', { detail: { testType: config.id }}));
    }
    renderQuestion();
  }

  function computeResult(config, answers){
    const scores = {};
    Object.keys(config.categories).forEach(k => scores[k]=0);
    config.questions.forEach(q => {
      const a = answers.get(q.id);
      if (!a) return;
      const opt = q.options[a.index];
      if (!opt || !opt.weights) return;
      Object.entries(opt.weights).forEach(([k,v]) => { scores[k] = (scores[k]||0) + v; });
    });
    const best = Object.entries(scores).sort((a,b)=>b[1]-a[1])[0];
    const categoryId = best ? best[0] : Object.keys(config.categories)[0];
    return { categoryId, scores };
  }

function getCategoryTheme(config, categoryId){
  const fallback = { emoji: '✨', gradient: 'linear-gradient(135deg,#667eea,#764ba2)' };
  const catCfg = (config.categories && config.categories[categoryId]) || {};
  if (catCfg.emoji || catCfg.gradient){
    return { emoji: catCfg.emoji || fallback.emoji, gradient: catCfg.gradient || fallback.gradient };
  }
  const map = {
    stability: { emoji: '🛋️', gradient: 'linear-gradient(135deg,#34d399,#10b981)' },
    passion:   { emoji: '🔥', gradient: 'linear-gradient(135deg,#f472b6,#ef4444)' },
    caretaking:{ emoji: '💞', gradient: 'linear-gradient(135deg,#f59e0b,#fcd34d)' },
    free:      { emoji: '🌈', gradient: 'linear-gradient(135deg,#60a5fa,#a78bfa)' },
    egen:      { emoji: '🎨', gradient: 'linear-gradient(135deg,#22d3ee,#818cf8)' },
    teto:      { emoji: '🧠', gradient: 'linear-gradient(135deg,#f43f5e,#f59e0b)' },
    mix:       { emoji: '⚡', gradient: 'linear-gradient(135deg,#14b8a6,#6366f1)' },
    teen:      { emoji: '⚡', gradient: 'linear-gradient(135deg,#67e8f9,#a78bfa)' },
    twenties:  { emoji: '🔥', gradient: 'linear-gradient(135deg,#8b5cf6,#f472b6)' },
    thirties:  { emoji: '⚖️', gradient: 'linear-gradient(135deg,#22c55e,#86efac)' },
    forties:   { emoji: '🍶', gradient: 'linear-gradient(135deg,#f59e0b,#fde68a)' }
  };
  return map[categoryId] || fallback;
}

function renderResult(root, config, result){
  const cat = config.categories[result.categoryId];
  const theme = getCategoryTheme(config, result.categoryId);
    const container = document.createElement('div');
    container.className = 'q-result';
    const baseUrl = (document.documentElement.lang||'ko').startsWith('ja') ? '/ja/' : (document.documentElement.lang||'ko').startsWith('en') ? '/en/' : '/';
    // Build insights (score bars + secondary trait) and tips
    const insightsHtml = (function(){
      const entries = Object.entries(result.scores||{});
      if (!entries.length) return '';
      const sorted = entries.sort((a,b)=>b[1]-a[1]);
      const top = sorted[0];
      const second = sorted[1];
      const bars = sorted.map(([k,v])=>{
        const max = top ? top[1] : 1;
        const pct = Math.max(6, Math.round((v / (max||1)) * 100));
        const name = (config.categories[k] && config.categories[k].name) || k;
        return `<div class="scorebar"><div class="label">${escapeHtml(name)}</div><div class="bar"><span style="width:${pct}%"></span></div></div>`;
      }).join('');
      const lang2 = (document.documentElement.lang||'ko').slice(0,2);
      const secMsg = lang2==='en' ? 'also shows up in your vibe.' : lang2==='ja' ? 'の傾向も見られます。' : '기질이 함께 보여요.';
      const secLine = second && config.categories[second[0]] ? `<div class="secondary">${escapeHtml(config.categories[second[0]].name)} ${secMsg}</div>` : '';
      return `<div class="q-insights">${secLine}<div class="score-list">${bars}</div></div>`;
    })();
    const tipsHtml = (function(){
      const lang = (document.documentElement.lang||'ko').slice(0,2);
      const T = {
        ko: {
          stability: '루틴과 신뢰를 살린 데이트를 계획해보세요. 조용한 맛집, 산책이 잘 맞아요.',
          passion: '새롭고 강렬한 경험을 탐색해보세요. 테마공원/콘서트/핫플 탐방 추천!',
          caretaking: '따뜻한 관심과 배려가 큰 힘이 돼요. 직접 만든 작은 선물도 좋습니다.',
          free: '자유롭고 편안한 분위기를 만들어보세요. 피크닉/드라이브 찰떡!',
          perfect: '메뉴 고민이 즐거운 케미! 음식 사진 챌린지를 함께 해보세요.',
          good: '합의점을 정하고 가끔 새로운 맛도 시도해보세요.',
          spicy: '취향 차이를 놀이로! “매운맛 챌린지” 같은 미션으로 재미를.',
          tricky: '“주 1회 번갈아 선택” 같은 룰을 정하면 편해요.',
          leader: '명확한 플랜 공유 + 경청을 함께. 일정은 간결하게.',
          vocal: '감정을 자주 표현하고 공감 대화를 연습하세요.',
          rap: '쿨한 솔직함에 배려 한 스푼을 더하면 완벽!',
          center: '무드/비주얼 연출이 강점. 사진 스폿/드레스코드로 설렘↑',
          all: '상황 적응형 장점! 파트너 스타일에 맞춰 모드 전환.',
          egen: '새 장르/콜라보 탐험! 실험정신이 매력 포인트.',
          teto: '완성도 높은 디테일로 설득력↑ 정성 플랜 잘 어울림.',
          mix: 'EGEN×TETO 밸런스! 순간에 맞게 톤 조절로 시너지.'
        },
        en: {
          stability: 'Plan calm, trust‑building dates—cozy spots and walks work well.',
          passion: 'Try bold, novel experiences—theme parks, concerts, hot places.',
          caretaking: 'Warm care matters—a small handmade gift can be lovely.',
          free: 'Keep it light and free—picnic or scenic drives shine.',
          perfect: 'Make menu‑picking fun—start a food photo challenge together.',
          good: 'Find middle ground and try new tastes occasionally.',
          spicy: 'Turn differences into play—try a “spice challenge.”',
          tricky: 'Set simple rules like “take turns choosing weekly.”',
          leader: 'Share clear plans yet listen well; keep the itinerary concise.',
          vocal: 'Express feelings often and practice empathetic talks.',
          rap: 'Be direct yet kind—cool honesty plus care wins.',
          center: 'Lean into mood/visuals—photo spots and dress codes spark fun.',
          all: 'Adapt strengths to partner’s style; switch modes as needed.',
          egen: 'Explore genres/collabs—the experimental vibe attracts.',
          teto: 'Show refined details—a well‑crafted plan fits you.',
          mix: 'Balance EGEN×TETO; tune your tone to the moment.'
        },
        ja: {
          stability: '落ち着いた信頼づくりデートを。居心地のよい店と散歩が相性◎',
          passion: '新しく刺激的な体験を。テーマパーク/ライブ/話題スポットへ',
          caretaking: 'やさしい気遣いが鍵。手作りの小さなギフトも素敵',
          free: '軽やかで自由な空気を。ピクニックやドライブが映えます',
          perfect: 'メニュー選び自体を楽しもう。写真企画を一緒に！',
          good: '歩み寄りルールを作り、時々新しい味にも挑戦',
          spicy: '違いを遊びに。辛さチャレンジなどミッション制も楽しい',
          tricky: '「週1交代で選ぶ」など簡単なルール設定が有効',
          leader: '方向性を示しつつ傾聴を。プラン共有は簡潔に',
          vocal: '気持ちを言葉に。共感の会話を習慣化しよう',
          rap: '率直さに思いやりを添えて最強に',
          center: 'ムード/ビジュアル演出が得意。撮影スポットやドレスコードも',
          all: '状況適応の強み。相手の性格に合わせてモード切替を',
          egen: '新ジャンル/コラボの探索を。実験精神が魅力',
          teto: '完成度の高いディテールを。丁寧なプランが似合う',
          mix: 'EGEN×TETOのバランス。瞬間に合わせてトーン調整'
        }
      };
      return (T[lang] && T[lang][result.categoryId]) || '';
    })();
  container.innerHTML = `
    <div class="q-hero" style="--hero-gradient:${theme.gradient}">
      <div class="q-emoji-container" aria-hidden="true">
        <div class="q-emoji">${escapeHtml(theme.emoji || '✨')}</div>
        <div class="q-emoji-shadow"></div>
      </div>
      <div class="q-hero-text">
        <div class="badge animate-badge">${I18N.resultBadge}</div>
        <h2 class="animate-title">${escapeHtml(cat.name)}</h2>
        <p class="muted animate-desc">${escapeHtml(cat.description)}</p>
      </div>
    </div>
    ${generateDetailedInsights(result, config, lang)}
    ${insightsHtml}
    ${tipsHtml ? `<div class=\"q-tips\">${tipsHtml}</div>` : ''}
    <div class="share enhanced-share">
      <div class="share-header">${I18N.shareNative}</div>
      <div class="share-grid">
        <button class="share-x share-btn twitter-btn">
          <div class="btn-icon">𝕏</div>
          <div class="btn-text">Twitter</div>
        </button>
        <button class="copy share-btn copy-btn">
          <div class="btn-icon">🔗</div>
          <div class="btn-text">${I18N.copy}</div>
        </button>
        <button class="fb share-btn facebook-btn">
          <div class="btn-icon">f</div>
          <div class="btn-text">Facebook</div>
        </button>
        <button class="line share-btn line-btn">
          <div class="btn-icon">📱</div>
          <div class="btn-text">LINE</div>
        </button>
        <button class="threads share-btn threads-btn">
          <div class="btn-icon">@</div>
          <div class="btn-text">Threads</div>
        </button>
        <button class="native share-btn native-btn">
          <div class="btn-icon">📤</div>
          <div class="btn-text">${I18N.shareNative}</div>
        </button>
      </div>
    </div>
      <div class="again"><a href="?">${I18N.tryAgain}</a></div>
      <div class="q-nav">
        <a class="q-nav-btn" href="${baseUrl}">${I18N.goHome}</a>
        <a class="q-nav-btn" href="${baseUrl}#all-tests">${I18N.allTests}</a>
      </div>
    `;
    root.innerHTML = '';
    root.appendChild(container);
    
    // Add enhanced result animations
    if (!document.querySelector('#result-animations')) {
      const style = document.createElement('style');
      style.id = 'result-animations';
      style.textContent = `
        .q-emoji-container {
          position: relative;
          display: inline-block;
        }
        .q-emoji {
          display: inline-block;
          animation: emojiPop 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
          transform: scale(0) rotate(-180deg);
        }
        .q-emoji-shadow {
          position: absolute;
          top: 100%;
          left: 50%;
          transform: translateX(-50%);
          width: 60%;
          height: 20%;
          background: rgba(0,0,0,0.1);
          border-radius: 50%;
          animation: shadowGrow 0.8s ease-out 0.3s forwards;
          opacity: 0;
        }
        .animate-badge {
          animation: slideUp 0.6s ease-out 0.4s backwards;
        }
        .animate-title {
          animation: slideUp 0.6s ease-out 0.6s backwards;
        }
        .animate-desc {
          animation: slideUp 0.6s ease-out 0.8s backwards;
        }
        .q-insights {
          animation: slideUp 0.6s ease-out 1.0s backwards;
        }
        .q-tips {
          animation: slideUp 0.6s ease-out 1.2s backwards;
        }
        .share {
          animation: slideUp 0.6s ease-out 1.4s backwards;
        }
        @keyframes emojiPop {
          0% { transform: scale(0) rotate(-180deg); }
          50% { transform: scale(1.2) rotate(-90deg); }
          100% { transform: scale(1) rotate(0deg); }
        }
        @keyframes shadowGrow {
          to { opacity: 1; }
        }
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(30px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .enhanced-share {
          padding: 20px;
          background: rgba(255,255,255,0.95);
          border-radius: 16px;
          box-shadow: 0 8px 32px rgba(0,0,0,0.1);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255,255,255,0.2);
        }
        .share-header {
          text-align: center;
          font-weight: bold;
          color: #333;
          margin-bottom: 16px;
          font-size: 1.1em;
        }
        .share-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
          gap: 12px;
        }
        .share-btn {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 16px 8px;
          border: none;
          border-radius: 12px;
          background: #f8f9fa;
          cursor: pointer;
          transition: all 0.3s ease;
          font-family: inherit;
          position: relative;
          overflow: hidden;
        }
        .share-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }
        .share-btn:active {
          transform: translateY(0);
        }
        .btn-icon {
          font-size: 24px;
          font-weight: bold;
          margin-bottom: 8px;
        }
        .btn-text {
          font-size: 12px;
          font-weight: 500;
          color: #666;
        }
        .twitter-btn:hover { background: #1da1f2; color: white; }
        .facebook-btn:hover { background: #4267b2; color: white; }
        .line-btn:hover { background: #00b900; color: white; }
        .threads-btn:hover { background: #000; color: white; }
        .copy-btn:hover { background: #6c757d; color: white; }
        .native-btn:hover { background: #28a745; color: white; }
        .twitter-btn:hover .btn-text,
        .facebook-btn:hover .btn-text,
        .line-btn:hover .btn-text,
        .threads-btn:hover .btn-text,
        .copy-btn:hover .btn-text,
        .native-btn:hover .btn-text {
          color: white;
        }
      `;
      document.head.appendChild(style);
    }

    if (window.track){
      document.dispatchEvent(new CustomEvent('test_completed', { detail: { testType: config.id, completionTime: 0, resultType: cat.name }}));
    }

    $('.share-x', container).addEventListener('click', () => {
      const title = config.share?.title || config.title;
      const url = window.location.href;
      const text = `${title} - ${cat.name}`;
      const tags = config.share?.hashtags ? '&hashtags=' + encodeURIComponent(config.share.hashtags) : '';
      window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}${tags}`, '_blank', 'noopener');
    });
    $('.copy', container).addEventListener('click', async () => {
      try{
        await navigator.clipboard.writeText(window.location.href);
        alert(I18N.copied);
      }catch(e){ alert(I18N.copyFailed); }
    });
    $('.fb', container).addEventListener('click', () => {
      const u = encodeURIComponent(window.location.href);
      window.open(`https://www.facebook.com/sharer/sharer.php?u=${u}`, '_blank', 'noopener');
    });
    $('.line', container).addEventListener('click', () => {
      const title = config.share?.title || config.title;
      const url = window.location.href;
      const text = `${title} - ${cat.name}`;
      window.open(`https://social-plugins.line.me/lineit/share?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`, '_blank', 'noopener');
    });
    $('.threads', container).addEventListener('click', () => {
      const title = config.share?.title || config.title;
      const url = window.location.href;
      const text = `${title} - ${cat.name}`;
      window.open(`https://www.threads.net/intent/post?text=${encodeURIComponent(text + ' ' + url)}`, '_blank', 'noopener');
    });
    $('.native', container).addEventListener('click', async () => {
      try{
        if (navigator.share){
          await navigator.share({ title: document.title, url: window.location.href, text: (config.share?.title || config.title) + ' - ' + cat.name });
        } else {
          await navigator.clipboard.writeText(window.location.href);
          alert(I18N.copied);
        }
      }catch(e){}
    });
  }

  function generateDetailedInsights(result, config, lang) {
    const testId = config.id;
    const categoryId = result.categoryId;
    
    const insights = {
      'kfood-romance': {
        ko: {
          stability: {
            personality: "안정감을 중시하는 당신은 깊이 있는 관계를 추구합니다.",
            compatibility: "차분하고 믿을 수 있는 파트너와 잘 맞아요.",
            advice: "급하지 않게, 천천히 서로를 알아가는 시간을 가지세요."
          },
          passion: {
            personality: "열정적이고 모험을 좋아하는 활발한 타입이에요.",
            compatibility: "에너지가 넘치고 새로운 도전을 함께할 수 있는 사람과 좋아요.",
            advice: "함께 새로운 경험을 만들어가며 관계에 활력을 불어넣으세요."
          },
          caretaking: {
            personality: "따뜻한 마음으로 상대를 챙기는 것을 좋아해요.",
            compatibility: "감정 표현이 풍부하고 소통을 중요하게 생각하는 사람과 잘 맞아요.",
            advice: "작은 관심과 배려로 상대의 마음을 따뜻하게 해주세요."
          },
          free: {
            personality: "자유롭고 유연한 사고를 가진 개방적인 성격이에요.",
            compatibility: "속박하지 않고 서로의 개성을 존중하는 파트너가 좋아요.",
            advice: "서로의 자유를 인정하면서도 함께하는 시간을 소중히 하세요."
          }
        },
        ja: {
          stability: {
            personality: "安定感を重視するあなたは、深みのある関係を求めます。",
            compatibility: "落ち着いていて信頼できるパートナーと相性が良いです。",
            advice: "急がず、ゆっくりとお互いを知る時間を持ってください。"
          },
          passion: {
            personality: "情熱的で冒険好きな活発なタイプです。",
            compatibility: "エネルギッシュで新しい挑戦を一緒にできる人と良いですね。",
            advice: "一緒に新しい経験を作りながら関係に活力を吹き込みましょう。"
          },
          caretaking: {
            personality: "温かい心で相手を気遣うのが好きです。",
            compatibility: "感情表現が豊かでコミュニケーションを大切にする人と合います。",
            advice: "小さな気遣いと思いやりで相手の心を温かくしてあげてください。"
          },
          free: {
            personality: "自由で柔軟な思考を持つ開放的な性格です。",
            compatibility: "束縛せずお互いの個性を尊重するパートナーが良いです。",
            advice: "お互いの自由を認めながらも一緒にいる時間を大切にしましょう。"
          }
        },
        en: {
          stability: {
            personality: "You value stability and seek deep, meaningful relationships.",
            compatibility: "You match well with calm and trustworthy partners.",
            advice: "Take time to slowly get to know each other without rushing."
          },
          passion: {
            personality: "You're passionate and adventurous, full of energy.",
            compatibility: "You work well with energetic people who enjoy new challenges.",
            advice: "Create new experiences together to bring vitality to your relationship."
          },
          caretaking: {
            personality: "You have a warm heart and love caring for your partner.",
            compatibility: "You match with emotionally expressive and communicative people.",
            advice: "Warm your partner's heart with small gestures of care and attention."
          },
          free: {
            personality: "You're free-spirited with flexible thinking and an open personality.",
            compatibility: "You need partners who respect individuality without being possessive.",
            advice: "Respect each other's freedom while cherishing your time together."
          }
        }
      },
      'food-compat': {
        ko: {
          perfect: {
            personality: "음식 취향까지 완벽하게 맞는 당신들은 진정한 소울메이트예요.",
            compatibility: "서로의 모든 면에서 깊은 이해와 공감대를 형성해요.",
            advice: "이 특별한 케미를 계속 유지하며 더 많은 추억을 만들어가세요."
          },
          good: {
            personality: "적당히 비슷하면서도 새로운 것을 받아들이는 유연한 타입이에요.",
            compatibility: "서로 다른 점을 존중하면서도 공통점을 찾는 능력이 있어요.",
            advice: "가끔은 상대의 취향에 맞춰보며 새로운 맛을 발견해보세요."
          },
          spicy: {
            personality: "자극적이고 도전적인 것을 좋아하는 모험가 타입이에요.",
            compatibility: "열정적이고 에너지 넘치는 관계를 만들어갈 수 있어요.",
            advice: "서로의 다른 취향을 재미있는 도전으로 받아들여보세요."
          },
          tricky: {
            personality: "개성이 강하고 자신만의 확고한 기준을 가진 타입이에요.",
            compatibility: "서로의 차이를 인정하고 조율하는 과정이 필요해요.",
            advice: "타협점을 찾아가며 서로를 이해하는 시간을 충분히 가지세요."
          }
        }
      },
      'kpop-idol-romance': {
        ko: {
          leader: {
            personality: "리더십이 강하고 계획적인 연애를 추구하는 타입이에요.",
            compatibility: "든든하고 주도적인 관계에서 빛을 발해요.",
            advice: "상대방의 의견도 충분히 들어주며 함께 방향을 정해가세요."
          },
          vocal: {
            personality: "감정 표현이 풍부하고 소통을 중시하는 타입이에요.",
            compatibility: "마음을 활짝 열고 진솔한 대화를 나누는 관계가 좋아요.",
            advice: "당신의 따뜻한 마음을 더 많이 표현해보세요."
          },
          rap: {
            personality: "직설적이고 솔직한 소통을 선호하는 쿨한 타입이에요.",
            compatibility: "서로 솔직하고 터놓고 지내는 관계에서 편안함을 느껴요.",
            advice: "가끔은 부드러운 표현으로 마음을 전해보세요."
          },
          center: {
            personality: "매력적이고 분위기를 이끄는 것을 좋아하는 타입이에요.",
            compatibility: "시각적이고 감각적인 즐거움을 함께할 수 있는 관계가 좋아요.",
            advice: "외적인 매력뿐만 아니라 내면의 깊이도 보여주세요."
          },
          all: {
            personality: "다재다능하고 상황에 맞게 유연하게 대응하는 타입이에요.",
            compatibility: "어떤 상대와도 조화를 이룰 수 있는 포용력이 있어요.",
            advice: "때로는 자신만의 색깔을 명확히 드러내는 것도 중요해요."
          }
        }
      },
      'kpop-egen-teto': {
        ko: {
          egen: {
            personality: "실험적이고 창의적인 것을 추구하는 자유로운 영혼이에요.",
            compatibility: "새로운 시도를 함께 즐기고 변화를 두려워하지 않는 파트너와 좋아요.",
            advice: "당신의 창의성과 실험정신을 관계에도 적용해보세요."
          },
          teto: {
            personality: "완성도와 안정감을 중시하는 체계적인 타입이에요.",
            compatibility: "신뢰할 수 있고 일관성 있는 관계를 만들어가는 파트너와 잘 맞아요.",
            advice: "때로는 예상치 못한 변화도 받아들여보는 유연함을 기르세요."
          },
          mix: {
            personality: "상황에 따라 유연하게 대응하는 균형잡힌 타입이에요.",
            compatibility: "다양한 매력을 가진 파트너와 조화롭게 어울릴 수 있어요.",
            advice: "당신의 밸런스 감각을 활용해 관계의 조화를 만들어가세요."
          }
        }
      }
    };

    const testInsights = insights[testId];
    if (!testInsights || !testInsights[lang] || !testInsights[lang][categoryId]) {
      return '';
    }

    const insight = testInsights[lang][categoryId];
    
    const titles = {
      ko: "💡 상세 분석",
      ja: "💡 詳細分析", 
      en: "💡 Detailed Analysis"
    };

    const labels = {
      ko: { personality: "🎯 성격 특징", compatibility: "💕 궁합 타입", advice: "✨ 연애 조언" },
      ja: { personality: "🎯 性格特徴", compatibility: "💕 相性タイプ", advice: "✨ 恋愛アドバイス" },
      en: { personality: "🎯 Personality", compatibility: "💕 Compatibility", advice: "✨ Dating Advice" }
    };

    return `
      <div class="q-detailed-insights">
        <h3 style="color:var(--accent-color,#667eea); margin-bottom:16px; text-align:center;">${titles[lang] || titles.ko}</h3>
        <div style="display:grid; gap:12px; margin-bottom:16px;">
          <div style="background:rgba(102,126,234,0.05); border-radius:12px; padding:16px; border-left:4px solid var(--accent-color,#667eea);">
            <div style="font-weight:700; color:var(--accent-color,#667eea); margin-bottom:8px;">${labels[lang]?.personality || labels.ko.personality}</div>
            <div style="color:var(--text-secondary,#666); line-height:1.5;">${insight.personality}</div>
          </div>
          <div style="background:rgba(245,158,11,0.05); border-radius:12px; padding:16px; border-left:4px solid #f59e0b;">
            <div style="font-weight:700; color:#f59e0b; margin-bottom:8px;">${labels[lang]?.compatibility || labels.ko.compatibility}</div>
            <div style="color:var(--text-secondary,#666); line-height:1.5;">${insight.compatibility}</div>
          </div>
          <div style="background:rgba(34,197,94,0.05); border-radius:12px; padding:16px; border-left:4px solid #22c55e;">
            <div style="font-weight:700; color:#22c55e; margin-bottom:8px;">${labels[lang]?.advice || labels.ko.advice}</div>
            <div style="color:var(--text-secondary,#666); line-height:1.5;">${insight.advice}</div>
          </div>
        </div>
      </div>
    `;
  }

  function escapeHtml(s){
    return String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  }

  function injectStyles(){
    const css = `
    .q-header{ text-align:center; margin:10px 0 8px; }
    .q-header h1{ font-size: clamp(20px, 3.2vw, 28px); margin:0 0 4px; }
    .q-header .muted{ color: var(--text-secondary, #666); }
    .q-progress{ width:100%; height:8px; background:rgba(0,0,0,.06); border-radius:6px; overflow:hidden; margin:8px auto 12px; max-width:820px; }
    .q-progress .bar{ height:100%; background:linear-gradient(90deg,#667eea,#764ba2); transition: width .25s ease; }
    .q-wrap{ max-width:820px; margin:0 auto; }
    .q-card{ background:var(--card-bg, #fff); border:1px solid var(--border-color,#e5e7eb); border-radius:12px; padding:16px; box-shadow: var(--shadow, 0 6px 18px rgba(0,0,0,.08)); }
    .q-num{ font-size:12px; color: var(--text-secondary,#666); margin-bottom:6px; }
    .q-options{ display:grid; gap:8px; margin-top:12px; }
    .q-option{ display:flex; gap:10px; align-items:center; padding:12px; border:1px solid var(--border-color,#e5e7eb); border-radius:10px; cursor:pointer; background:rgba(255,255,255,.9); }
    .q-option:hover{ border-color: var(--accent-color,#667eea); }
    .q-actions{ display:flex; gap:8px; justify-content:center; margin:12px 0; z-index:5; }
    .q-actions button{ padding:10px 16px; min-width:110px; border-radius:999px; border:1px solid var(--border-color,#e5e7eb); background:var(--card-bg,#fff); cursor:pointer; color: var(--text-primary,#111); }
    .q-actions .prev[disabled]{ opacity:.5; }
    .q-actions .prev:not([disabled]){ background: linear-gradient(90deg,#667eea,#764ba2); color:#fff; border:none; }
    .q-actions .next, .q-actions .submit{ background: linear-gradient(90deg,#667eea,#764ba2); color:#fff; border:none; }
    .q-result{ max-width:820px; margin:0 auto; background:var(--card-bg,#fff); border:1px solid var(--border-color,#e5e7eb); border-radius:12px; padding:18px; text-align:center; box-shadow: var(--shadow, 0 6px 18px rgba(0,0,0,.08)); }
    .q-hero{ position:relative; display:flex; gap:12px; align-items:center; border-radius:12px; padding:14px; margin-bottom:10px; background: var(--hero-gradient, linear-gradient(135deg,#667eea,#764ba2)); color:#0b0f14; overflow:hidden; }
    .q-hero::after{ content:''; position:absolute; inset:0; background: radial-gradient(600px 240px at 90% -10%, rgba(255,255,255,.25), transparent); pointer-events:none; }
    .q-emoji{ width:54px; height:54px; border-radius:12px; background: rgba(255,255,255,.85); display:flex; align-items:center; justify-content:center; font-size:28px; box-shadow: 0 6px 18px rgba(0,0,0,.12); }
    .q-hero .badge{ display:inline-block; padding:4px 10px; border-radius:999px; background: rgba(255,255,255,.7); color:#111; font-weight:700; font-size:.75rem; }
    .q-hero h2{ margin:6px 0 2px; color:#0b0f14; }
    .q-hero p{ margin:0; color:#0b0f14; opacity:.85; }
    .q-result .badge{ display:inline-block; padding:4px 10px; border-radius:999px; background:#f1f5f9; color:#64748b; font-size:12px; margin-bottom:8px; }
    .q-result h2{ margin:6px 0 8px; }
    .q-result .muted{ color: var(--text-secondary,#666); }
    .q-insights{ margin-top:10px; text-align:left; max-width:820px; margin-left:auto; margin-right:auto; }
    .q-insights .secondary{ font-size:.95rem; color: var(--text-secondary,#666); margin:4px 0 8px; }
    .score-list{ display:grid; gap:6px; }
    .scorebar{ display:flex; align-items:center; gap:8px; }
    .scorebar .label{ width:120px; font-size:.9rem; color:#374151; }
    .scorebar .bar{ flex:1; height:8px; background:#eef2f7; border-radius:999px; overflow:hidden; }
    .scorebar .bar > span{ display:block; height:100%; background:linear-gradient(90deg,#667eea,#764ba2); box-shadow: 0 2px 8px rgba(102,126,234,.35); border-radius:999px; }
    .q-tips{ background:#f8fafc; border:1px solid #e5e7eb; border-radius:12px; padding:10px; margin:12px 0; font-size:.95rem; color:#374151; }
    .q-result .share{ display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin-top:12px; 
      background: var(--share-bg, #f8fafc); border:1px solid var(--border-color,#e5e7eb); border-radius:12px; padding:12px; backdrop-filter: blur(6px); }
    .q-result .share button{ padding:10px 16px; border-radius:8px; border:none; color:#fff; cursor:pointer; box-shadow: 0 2px 10px rgba(0,0,0,.1); font-weight:600; font-size:13px; transition: all 0.2s ease; }
    .q-result .share .share-x{ background:linear-gradient(135deg,#1da1f2,#0d8bd9); }
    .q-result .share .copy{ background:linear-gradient(135deg,#6c757d,#495057); }
    .q-result .share .fb{ background:linear-gradient(135deg,#1877f2,#166fe5); }
    .q-result .share .line{ background:linear-gradient(135deg,#00c300,#00b300); }
    .q-result .share .threads{ background:linear-gradient(135deg,#000,#333); }
    .q-result .share .native{ background:linear-gradient(135deg,var(--accent-color,#667eea),var(--accent-color,#667eea)); }
    .q-result .share button:hover{ transform:translateY(-1px); box-shadow: 0 4px 15px rgba(0,0,0,.15); }
    .q-result .again{ margin-top:10px; }
    .q-nav{ display:flex; gap:10px; justify-content:center; margin-top:12px; }
    .q-nav-btn{ display:inline-block; padding:10px 14px; border-radius:999px; background:linear-gradient(90deg,#667eea,#764ba2); color:#fff; text-decoration:none; }
    @media (max-width:600px){ .q-option{ padding:10px; } }
    @media (max-width: 720px){
      .q-actions{ position: sticky; bottom: 8px; background: rgba(255,255,255,.92); backdrop-filter: blur(6px); padding: 8px; border:1px solid var(--border-color,#e5e7eb); border-radius: 12px; box-shadow: var(--shadow, 0 6px 18px rgba(0,0,0,.08)); max-width: 820px; margin-left:auto; margin-right:auto; }
    }
    `;
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
  }

  function renderRecommendations(root, config, locale){
    const map = {
      'age-vibe': [
        { id: 'romance-test', path: 'romance-test' },
        { id: 'anime-personality', path: 'anime-personality' },
        { id: 'food-compat', path: 'food-compat' },
        { id: 'kfood-romance', path: 'kfood-romance' }
      ],
      'kfood-romance': [
        { id: 'food-compat', path: 'food-compat' },
        { id: 'romance-test', path: 'romance-test' },
        { id: 'anime-personality', path: 'anime-personality' },
        { id: 'egen-teto', path: 'egen-teto' }
      ],
      'food-compat': [
        { id: 'kfood-romance', path: 'kfood-romance' },
        { id: 'romance-test', path: 'romance-test' },
        { id: 'anime-personality', path: 'anime-personality' },
        { id: 'egen-teto', path: 'egen-teto' }
      ],
      'kpop-idol-romance': [
        { id: 'kpop-egen-teto', path: 'kpop-egen-teto' },
        { id: 'egen-teto', path: 'egen-teto' },
        { id: 'romance-test', path: 'romance-test' },
        { id: 'anime-personality', path: 'anime-personality' }
      ],
      'kpop-egen-teto': [
        { id: 'kpop-idol-romance', path: 'kpop-idol-romance' },
        { id: 'egen-teto', path: 'egen-teto' },
        { id: 'romance-test', path: 'romance-test' },
        { id: 'anime-personality', path: 'anime-personality' }
      ]
    };
    const items = map[config.id] || [];
    if (!items.length) return;
    const base = locale; // 'ko' | 'ja' | 'en'
    const titles = {
      ko: {
        'food-compat': '🍽️ 음식 궁합 테스트',
        'kfood-romance': '🍲 K-FOOD 연애 취향',
        'romance-test': '💕 연애 스타일 테스트',
        'kpop-idol-romance': '🎤 K-POP 아이돌 연애 취향',
        'kpop-egen-teto': '🎵 K-POP EGEN/TETO 성향',
        'egen-teto': '💖 에겐 vs 테토 성향 테스트',
        'anime-personality': '🎭 애니메 성격 진단',
        'age-vibe': '🕒 감성연령 테스트',
        'compat-pick': '🔥 이름 케미 테스트'
      },
      ja: {
        'food-compat': '🍽️ フード相性テスト',
        'kfood-romance': '🍲 K-FOOD 恋愛タイプ',
        'romance-test': '💕 恋愛スタイルテスト',
        'kpop-idol-romance': '🎤 K-POP アイドル恋愛',
        'kpop-egen-teto': '🎵 K-POP EGEN/TETO 性向',
        'egen-teto': '💖 エゲン vs テト 性向テスト',
        'anime-personality': '🎭 アニメ性格診断',
        'age-vibe': '🕒 感性年齢テスト',
        'compat-pick': '🔥 名前相性テスト'
      },
      en: {
        'food-compat': '🍽️ Food Compatibility Test',
        'kfood-romance': '🍲 K-FOOD Romance',
        'romance-test': '💕 Love Style Test',
        'kpop-idol-romance': '🎤 K-POP Idol Romance',
        'kpop-egen-teto': '🎵 K-POP EGEN/TETO Preference',
        'egen-teto': '💖 Estrogen vs Testosterone Personality Test',
        'anime-personality': '🎭 Anime Personality Test',
        'age-vibe': '🕒 Emotional Age Test',
        'compat-pick': '🔥 Name Chemistry Test'
      }
    }[base] || {};
    const section = document.createElement('div');
    section.className = 'q-recs';
    const title = locale==='ja' ? 'おすすめのテスト' : locale==='en' ? 'Recommended Tests' : '추천 테스트';
    section.innerHTML = `<h3 style="margin:14px 0 8px;">${title}</h3>`;
    const list = document.createElement('div');
    list.style.display = 'grid'; list.style.gap = '8px'; list.style.gridTemplateColumns = '1fr';
    items.forEach(it => {
      const a = document.createElement('a');
      a.className = 'q-option';
      a.style.textDecoration='none';
      a.href = `/${it.path}/${base}/`;
      const label = titles[it.id] || `/${it.path}/${base}/`;
      a.innerHTML = `<span>${escapeHtml(label)}</span>`;
      list.appendChild(a);
    });
    section.appendChild(list);
    root.appendChild(section);
  }

  function tryDeeplinkResult(root, config){
    try{
      const url = new URL(window.location.href);
      const r = url.searchParams.get('r');
      if (r && config.categories && config.categories[r]){
        renderResult(root, config, { categoryId: r, scores: {} });
        return true;
      }
    }catch(e){}
    return false;
  }

  document.addEventListener('DOMContentLoaded', () => {
    injectStyles();
    const root = document.getElementById('quiz');
    if (!root) return;
    if (!window.quizConfig){
      root.textContent = '퀴즈 구성이 없습니다.';
      return;
    }
    // if deep link to result exists, render result directly
    if (!tryDeeplinkResult(root, window.quizConfig)) {
      renderQuiz(root, window.quizConfig);
    }
    // render recommendations (under result container if present)
    const recRoot = root.querySelector('.q-result') || root;
    renderRecommendations(recRoot, window.quizConfig, (document.documentElement.lang||'ko').slice(0,2));
  });
})();
