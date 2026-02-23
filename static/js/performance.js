/* ══════════════════════════════════════════════════════════════════════
   Performance Optimizations for LearnLoop - OPTIMIZED
   ══════════════════════════════════════════════════════════════════════ */

// ── Debounce Function for Search/Filter ──
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

// ── Throttle Function for Scroll Events ──
function throttle(func, limit) {
  let inThrottle;
  return function() {
    if (!inThrottle) {
      func.apply(this, arguments);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// ── Cache API Responses (Lightweight) ──
const cache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

function cachedFetch(url, options = {}) {
  const cacheKey = url + JSON.stringify(options);
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return Promise.resolve(cached.data);
  }
  
  return fetch(url, options)
    .then(response => response.json())
    .then(data => {
      cache.set(cacheKey, { data, timestamp: Date.now() });
      return data;
    });
}

// ── Prefetch Links on Hover (Desktop Only) ──
if (window.innerWidth > 768) {
  document.addEventListener('mouseover', (e) => {
    const link = e.target.closest('a[href^="/"]');
    if (link && !link.dataset.prefetched) {
      const url = link.getAttribute('href');
      const prefetch = document.createElement('link');
      prefetch.rel = 'prefetch';
      prefetch.href = url;
      document.head.appendChild(prefetch);
      link.dataset.prefetched = 'true';
    }
  }, { passive: true, capture: true });
}

// ── Export functions ──
window.LearnLoopPerf = {
  debounce,
  throttle,
  cachedFetch
};
