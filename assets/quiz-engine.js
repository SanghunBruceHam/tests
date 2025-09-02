// Simple Quiz Engine (vanilla JS)
// Expects window.quizConfig = {
//   id, title, subtitle, questions: [{id, text, options: [{text, weights:{[category]:score}}]}],
//   categories: { [categoryId]: { name, description } },
//   share: { title, hashtags }
// }

(function(){
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
    root.appendChild(qwrap);

    const actions = document.createElement('div');
    actions.className = 'q-actions';
    actions.innerHTML = `
      <button class="prev" disabled>◀ 이전</button>
      <button class="next">다음 ▶</button>
      <button class="submit" style="display:none">결과 보기</button>
    `;
    root.appendChild(actions);

    const prevBtn = $('.prev', actions);
    const nextBtn = $('.next', actions);
    const submitBtn = $('.submit', actions);

    let idx = 0;
    const answers = new Map();
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
      card.innerHTML = `<div class="q-num">Q${idx+1}/${total}</div><h2>${escapeHtml(q.text)}</h2>`;

      const list = document.createElement('div');
      list.className = 'q-options';
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
      if (!sel){ alert('하나를 선택해주세요.'); return; }
      answers.set(sel.questionId, sel);
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
      if (!sel){ alert('하나를 선택해주세요.'); return; }
      answers.set(sel.questionId, sel);
      const result = computeResult(config, answers);
      renderResult(root, config, result);
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
    container.innerHTML = `
      <div class="badge">RESULT</div>
      <h2>${escapeHtml(cat.name)}</h2>
      <p class="muted">${escapeHtml(cat.description)}</p>
      <div class="share">
        <button class="share-x">X (Twitter)</button>
        <button class="copy">링크 복사</button>
      </div>
      <div class="again"><a href="?">다시 하기</a></div>
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
        alert('링크를 복사했어요!');
      }catch(e){ alert('복사 실패. 주소창에서 직접 복사해주세요.'); }
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
    .q-actions{ display:flex; gap:8px; justify-content:center; margin:12px 0; }
    .q-actions button{ padding:10px 16px; border-radius:999px; border:1px solid var(--border-color,#e5e7eb); background:var(--card-bg,#fff); cursor:pointer; }
    .q-actions .next, .q-actions .submit{ background: linear-gradient(90deg,#667eea,#764ba2); color:#fff; border:none; }
    .q-result{ max-width:820px; margin:0 auto; background:var(--card-bg,#fff); border:1px solid var(--border-color,#e5e7eb); border-radius:12px; padding:18px; text-align:center; box-shadow: var(--shadow, 0 6px 18px rgba(0,0,0,.08)); }
    .q-result .badge{ display:inline-block; padding:4px 10px; border-radius:999px; background:#f1f5f9; color:#64748b; font-size:12px; margin-bottom:8px; }
    .q-result h2{ margin:6px 0 8px; }
    .q-result .muted{ color: var(--text-secondary,#666); }
    .q-result .share{ display:flex; gap:10px; justify-content:center; margin-top:12px; }
    .q-result .again{ margin-top:10px; }
    @media (max-width:600px){ .q-option{ padding:10px; } }
    `;
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
  }

  document.addEventListener('DOMContentLoaded', () => {
    injectStyles();
    const root = document.getElementById('quiz');
    if (!root) return;
    if (!window.quizConfig){
      root.textContent = '퀴즈 구성이 없습니다.';
      return;
    }
    renderQuiz(root, window.quizConfig);
  });
})();

