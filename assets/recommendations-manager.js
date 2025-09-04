// Recommendations ordering and badge manager
(function(){
  function getLocale(){
    const path = location.pathname;
    if (/^\/ja\//.test(path)) return 'ja';
    if (/^\/en\//.test(path)) return 'en';
    if (/^\/ko\//.test(path) || path === '/' || path.startsWith('/index')) return 'ko';
    // Fallback to document lang
    const lang = (document.documentElement.getAttribute('lang')||'ko').toLowerCase();
    if (lang.startsWith('ja')) return 'ja';
    if (lang.startsWith('en')) return 'en';
    return 'ko';
  }

  const ORDER = [
    'age-vibe',
    'compat-pick',
    'kfood-romance',
    'food-compat',
    'kpop-idol-romance',
    'kpop-egen-teto',
    'anime-personality',
    'romance-test',
    'egen-teto'
  ];

  const BADGES = {
    rank: { 'anime-personality': 1, 'romance-test': 2, 'egen-teto': 3 },
    newly: new Set(['age-vibe','compat-pick']),
    hot: new Set(['kfood-romance','food-compat','kpop-idol-romance','kpop-egen-teto'])
  };

  function rankLabel(n, locale){
    if (locale === 'ja') return `${n}位`;
    if (locale === 'en') return n === 1 ? '1st' : n === 2 ? '2nd' : '3rd';
    return `${n}위`;
  }

  function ensureBadgeEl(card){
    let el = card.querySelector('.rank-badge');
    if (!el){
      el = document.createElement('span');
      el.className = 'rank-badge';
      el.style.cssText = 'position:absolute;top:12px;right:12px;background:linear-gradient(135deg,#ff6b9d,#c94b70);color:white;padding:6px 12px;border-radius:20px;font-size:.7rem;font-weight:600;z-index:1;box-shadow:0 2px 8px rgba(255,107,157,.3);letter-spacing:.5px;';
      card.appendChild(el);
    }
    return el;
  }

  function applyBadges(container, locale){
    const items = container.querySelectorAll('a.recommendation-item[data-id]');
    items.forEach(a => {
      const id = a.getAttribute('data-id');
      const rank = BADGES.rank[id];
      const badge = ensureBadgeEl(a);
      if (rank){
        badge.textContent = rankLabel(rank, locale);
        return;
      }
      if (BADGES.newly.has(id)){
        badge.textContent = 'NEW';
        return;
      }
      if (BADGES.hot.has(id)){
        badge.textContent = 'HOT';
        return;
      }
      // Default hide if no status
      badge.textContent = '';
      badge.style.display = 'none';
    });
  }

  function reorder(container){
    const children = Array.from(container.querySelectorAll('a.recommendation-item[data-id]'));
    if (!children.length) return;
    const map = new Map(children.map(ch => [ch.getAttribute('data-id'), ch]));
    const frag = document.createDocumentFragment();
    ORDER.forEach(id => { if (map.has(id)) frag.appendChild(map.get(id)); });
    // Append any leftovers (unexpected ids)
    children.forEach(ch => { if (!ORDER.includes(ch.getAttribute('data-id'))) frag.appendChild(ch); });
    container.innerHTML = '';
    container.appendChild(frag);
  }

  document.addEventListener('DOMContentLoaded', function(){
    const container = document.querySelector('.recommendation-cards');
    if (!container) return;
    reorder(container);
    applyBadges(container, getLocale());
  });
})();

