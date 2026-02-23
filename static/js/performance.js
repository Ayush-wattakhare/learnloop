/* ══════════════════════════════════════════════════════════════════════
   Performance Optimizations for LearnLoop
   ══════════════════════════════════════════════════════════════════════ */

// ── Lazy Loading Images ──
document.addEventListener('DOMContentLoaded', function() {
  // Lazy load images
  const images = document.querySelectorAll('img[data-src]');
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        imageObserver.unobserve(img);
      }
    });
  });

  images.forEach(img => imageObserver.observe(img));
});

// ── Debounce Function for Search/Filter ──
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ── Throttle Function for Scroll Events ──
function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// ── Optimize Scroll Performance ──
let ticking = false;
function optimizedScroll(callback) {
  if (!ticking) {
    window.requestAnimationFrame(function() {
      callback();
      ticking = false;
    });
    ticking = true;
  }
}

// ── Preload Critical Resources ──
function preloadResource(url, type) {
  const link = document.createElement('link');
  link.rel = 'preload';
  link.href = url;
  link.as = type;
  document.head.appendChild(link);
}

// ── Cache API Responses ──
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
      cache.set(cacheKey, {
        data: data,
        timestamp: Date.now()
      });
      return data;
    });
}

// ── Optimize Form Submissions ──
function optimizeForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;
  
  form.addEventListener('submit', function(e) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner"></span> Loading...';
    }
  });
}

// ── Mobile Menu Toggle ──
function initMobileMenu() {
  const menuToggle = document.createElement('button');
  menuToggle.className = 'mobile-menu-toggle hide-desktop';
  menuToggle.innerHTML = '☰';
  menuToggle.setAttribute('aria-label', 'Toggle menu');
  
  const navbar = document.querySelector('.navbar');
  const navLinks = document.querySelector('.navbar-links');
  
  if (navbar && navLinks && window.innerWidth <= 768) {
    navbar.insertBefore(menuToggle, navLinks);
    navLinks.classList.add('mobile-hidden');
    
    menuToggle.addEventListener('click', function() {
      navLinks.classList.toggle('mobile-hidden');
      navLinks.classList.toggle('mobile-visible');
      menuToggle.innerHTML = navLinks.classList.contains('mobile-visible') ? '✕' : '☰';
    });
  }
}

// ── Detect Slow Connection ──
function detectSlowConnection() {
  if ('connection' in navigator) {
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (connection) {
      if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
        document.body.classList.add('slow-connection');
        console.log('⚠️ Slow connection detected - optimizing...');
        
        // Disable animations on slow connections
        const style = document.createElement('style');
        style.innerHTML = '* { animation: none !important; transition: none !important; }';
        document.head.appendChild(style);
      }
    }
  }
}

// ── Reduce Data Usage on Slow Connections ──
function optimizeForSlowConnection() {
  if (document.body.classList.contains('slow-connection')) {
    // Reduce image quality
    const images = document.querySelectorAll('img');
    images.forEach(img => {
      if (img.src && !img.dataset.optimized) {
        img.dataset.optimized = 'true';
        // Add compression parameter if using image CDN
      }
    });
  }
}

// ── Virtual Scrolling for Long Lists ──
function initVirtualScroll(containerId, itemHeight, items) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  const visibleItems = Math.ceil(container.clientHeight / itemHeight) + 2;
  let scrollTop = 0;
  
  function render() {
    const startIndex = Math.floor(scrollTop / itemHeight);
    const endIndex = Math.min(startIndex + visibleItems, items.length);
    
    container.innerHTML = '';
    for (let i = startIndex; i < endIndex; i++) {
      const item = document.createElement('div');
      item.style.height = itemHeight + 'px';
      item.innerHTML = items[i];
      container.appendChild(item);
    }
  }
  
  container.addEventListener('scroll', throttle(function() {
    scrollTop = container.scrollTop;
    render();
  }, 100));
  
  render();
}

// ── Prefetch Links on Hover ──
function initLinkPrefetch() {
  const links = document.querySelectorAll('a[href^="/"]');
  links.forEach(link => {
    link.addEventListener('mouseenter', function() {
      const url = this.getAttribute('href');
      if (url && !document.querySelector(`link[href="${url}"]`)) {
        const prefetch = document.createElement('link');
        prefetch.rel = 'prefetch';
        prefetch.href = url;
        document.head.appendChild(prefetch);
      }
    }, { once: true });
  });
}

// ── Optimize WebSocket Reconnection ──
function createOptimizedSocket(url) {
  let socket;
  let reconnectAttempts = 0;
  const maxReconnectDelay = 30000; // 30 seconds
  
  function connect() {
    socket = io(url);
    
    socket.on('disconnect', () => {
      const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), maxReconnectDelay);
      console.log(`Reconnecting in ${delay}ms...`);
      setTimeout(() => {
        reconnectAttempts++;
        connect();
      }, delay);
    });
    
    socket.on('connect', () => {
      reconnectAttempts = 0;
      console.log('✅ Connected');
    });
  }
  
  connect();
  return socket;
}

// ── Batch DOM Updates ──
function batchDOMUpdates(updates) {
  requestAnimationFrame(() => {
    updates.forEach(update => update());
  });
}

// ── Initialize Performance Optimizations ──
document.addEventListener('DOMContentLoaded', function() {
  // Detect slow connection
  detectSlowConnection();
  optimizeForSlowConnection();
  
  // Initialize mobile menu
  if (window.innerWidth <= 768) {
    initMobileMenu();
  }
  
  // Prefetch links on hover (desktop only)
  if (window.innerWidth > 768) {
    initLinkPrefetch();
  }
  
  // Optimize all forms
  document.querySelectorAll('form').forEach(form => {
    if (form.id) optimizeForm(form.id);
  });
  
  // Add loading states to buttons
  document.querySelectorAll('button[type="submit"]').forEach(btn => {
    btn.addEventListener('click', function() {
      if (!this.disabled) {
        this.classList.add('loading');
      }
    });
  });
});

// ── Handle Orientation Change ──
window.addEventListener('orientationchange', function() {
  // Reload certain components on orientation change
  setTimeout(() => {
    window.dispatchEvent(new Event('resize'));
  }, 100);
});

// ── Monitor Performance ──
if ('PerformanceObserver' in window) {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.duration > 100) {
        console.warn(`⚠️ Slow operation: ${entry.name} took ${entry.duration}ms`);
      }
    }
  });
  
  observer.observe({ entryTypes: ['measure', 'navigation'] });
}

// ── Export functions for use in other scripts ──
window.LearnLoopPerf = {
  debounce,
  throttle,
  cachedFetch,
  optimizedScroll,
  batchDOMUpdates,
  preloadResource
};
