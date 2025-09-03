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
      $('.bar', progress).style.width = pct + '%';
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
      });
      card.appendChild(list);
      qwrap.appendChild(card);

      // restore selection
      if (answers.has(q.id)){
        const savedIdx = answers.get(q.id).index;
        const input = $(`input#${q.id}_${savedIdx}`, qwrap);
        if (input) input.checked = true;
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

  function renderResult(root, config, result){
    const cat = config.categories[result.categoryId];
    const container = document.createElement('div');
    container.className = 'q-result';
    const baseUrl = (document.documentElement.lang||'ko').startsWith('ja') ? '/ja/' : (document.documentElement.lang||'ko').startsWith('en') ? '/en/' : '/';
    container.innerHTML = `
      <div class="badge">${I18N.resultBadge}</div>
      <h2>${escapeHtml(cat.name)}</h2>
      <p class="muted">${escapeHtml(cat.description)}</p>
      <div class="share">
        <button class="share-x">${I18N.shareX}</button>
        <button class="copy">${I18N.copy}</button>
        <button class="fb">${I18N.shareFacebook}</button>
        <button class="line">${I18N.shareLine}</button>
        <button class="threads">${I18N.shareThreads}</button>
        <button class="native">${I18N.shareNative}</button>
      </div>
      <div class="again"><a href="?">${I18N.tryAgain}</a></div>
      <div class="q-nav">
        <a class="q-nav-btn" href="${baseUrl}">${I18N.goHome}</a>
        <a class="q-nav-btn" href="${baseUrl}#all-tests">${I18N.allTests}</a>
      </div>
    `;
    root.innerHTML = '';
    root.appendChild(container);

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
    .q-result .badge{ display:inline-block; padding:4px 10px; border-radius:999px; background:#f1f5f9; color:#64748b; font-size:12px; margin-bottom:8px; }
    .q-result h2{ margin:6px 0 8px; }
    .q-result .muted{ color: var(--text-secondary,#666); }
    .q-result .share{ display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-top:12px; 
      background: var(--share-bg, #f8fafc); border:1px solid var(--border-color,#e5e7eb); border-radius:12px; padding:8px; }
    .q-result .share button{ padding:8px 12px; border-radius:999px; border:1px solid var(--border-color,#e5e7eb); background:#ffffff; color:#111; cursor:pointer; box-shadow: 0 2px 6px rgba(0,0,0,.06); }
    .q-result .share button:hover{ border-color: var(--accent-color,#667eea); }
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
      'kfood-romance': [
        { id: 'food-compat', path: 'food-compat' },
        { id: 'romance-test', path: 'romance-test' }
      ],
      'food-compat': [
        { id: 'kfood-romance', path: 'kfood-romance' },
        { id: 'romance-test', path: 'romance-test' }
      ],
      'kpop-idol-romance': [
        { id: 'kpop-egen-teto', path: 'kpop-egen-teto' },
        { id: 'egen-teto', path: 'egen-teto' }
      ],
      'kpop-egen-teto': [
        { id: 'kpop-idol-romance', path: 'kpop-idol-romance' },
        { id: 'egen-teto', path: 'egen-teto' }
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
        'egen-teto': '💖 에겐 vs 테토 성향 테스트'
      },
      ja: {
        'food-compat': '🍽️ フード相性テスト',
        'kfood-romance': '🍲 K-FOOD 恋愛タイプ',
        'romance-test': '💕 恋愛スタイルテスト',
        'kpop-idol-romance': '🎤 K-POP アイドル恋愛',
        'kpop-egen-teto': '🎵 K-POP EGEN/TETO 性向',
        'egen-teto': '💖 エゲン vs テト 性向テスト'
      },
      en: {
        'food-compat': '🍽️ Food Compatibility Test',
        'kfood-romance': '🍲 K-FOOD Romance',
        'romance-test': '💕 Love Style Test',
        'kpop-idol-romance': '🎤 K-POP Idol Romance',
        'kpop-egen-teto': '🎵 K-POP EGEN/TETO Preference',
        'egen-teto': '💖 Estrogen vs Testosterone Personality Test'
      }
    }[base] || {};
    const section = document.createElement('div');
    section.className = 'q-recs';
    const title = locale==='ja' ? 'おすすめのテスト' : locale==='en' ? 'Recommended Tests' : '추천 테스트';
    section.innerHTML = `<h3 style="margin:14px 0 8px;">${title}</h3>`;
    const list = document.createElement('div');
    list.style.display = 'grid'; list.style.gap = '8px';
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
