/* ══════════════════════════════════════════════════════════════════════
   Mobile App-Like Interactions for LearnLoop
   ══════════════════════════════════════════════════════════════════════ */

// ── Initialize Mobile App Features ──
document.addEventListener('DOMContentLoaded', function() {
  if (window.innerWidth <= 768) {
    initBottomNavigation();
    initPullToRefresh();
    initHapticFeedback();
    initSwipeGestures();
    initPageTransitions();
    hideAddressBar();
  }
});

// ── Bottom Navigation Bar ──
function initBottomNavigation() {
  // Check if user is logged in
  const isLoggedIn = document.querySelector('.navbar-links a[href="/dashboard"]');
  if (!isLoggedIn) return;
  
  // Create bottom navigation
  const bottomNav = document.createElement('div');
  bottomNav.className = 'mobile-bottom-nav';
  bottomNav.innerHTML = `
    <a href="/dashboard" class="mobile-bottom-nav-item ${window.location.pathname === '/dashboard' ? 'active' : ''}">
      <span class="icon">🏠</span>
      <span>Home</span>
    </a>
    <a href="/groups" class="mobile-bottom-nav-item ${window.location.pathname === '/groups' ? 'active' : ''}">
      <span class="icon">👥</span>
      <span>Groups</span>
    </a>
    <a href="/messages" class="mobile-bottom-nav-item ${window.location.pathname === '/messages' ? 'active' : ''}">
      <span class="icon">💬</span>
      <span>Messages</span>
    </a>
    <a href="/voice-rooms" class="mobile-bottom-nav-item ${window.location.pathname.includes('/voice-room') ? 'active' : ''}">
      <span class="icon">🎙️</span>
      <span>Rooms</span>
    </a>
    <a href="/profile" class="mobile-bottom-nav-item ${window.location.pathname === '/profile' ? 'active' : ''}">
      <span class="icon">👤</span>
      <span>Profile</span>
    </a>
  `;
  
  document.body.appendChild(bottomNav);
  
  // Add active state on click
  bottomNav.querySelectorAll('.mobile-bottom-nav-item').forEach(item => {
    item.addEventListener('click', function() {
      bottomNav.querySelectorAll('.mobile-bottom-nav-item').forEach(i => i.classList.remove('active'));
      this.classList.add('active');
    });
  });
}

// ── Pull to Refresh ──
function initPullToRefresh() {
  let startY = 0;
  let currentY = 0;
  let pulling = false;
  
  const indicator = document.createElement('div');
  indicator.className = 'pull-to-refresh';
  indicator.innerHTML = '↓ Pull to refresh';
  document.body.appendChild(indicator);
  
  document.addEventListener('touchstart', function(e) {
    if (window.scrollY === 0) {
      startY = e.touches[0].pageY;
      pulling = true;
    }
  }, { passive: true });
  
  document.addEventListener('touchmove', function(e) {
    if (!pulling) return;
    
    currentY = e.touches[0].pageY;
    const diff = currentY - startY;
    
    if (diff > 0 && diff < 100) {
      indicator.style.transform = `translateX(-50%) translateY(${diff - 100}px)`;
      indicator.innerHTML = '↓ Pull to refresh';
    } else if (diff >= 100) {
      indicator.classList.add('visible');
      indicator.innerHTML = '↻ Release to refresh';
    }
  }, { passive: true });
  
  document.addEventListener('touchend', function() {
    if (!pulling) return;
    
    const diff = currentY - startY;
    if (diff >= 100) {
      indicator.innerHTML = '⟳ Refreshing...';
      setTimeout(() => {
        window.location.reload();
      }, 500);
    } else {
      indicator.classList.remove('visible');
      indicator.style.transform = 'translateX(-50%) translateY(-100px)';
    }
    
    pulling = false;
    startY = 0;
    currentY = 0;
  });
}

// ── Haptic Feedback ──
function initHapticFeedback() {
  // Vibration API for haptic feedback
  const haptic = (duration = 10) => {
    if ('vibrate' in navigator) {
      navigator.vibrate(duration);
    }
  };
  
  // Add haptic feedback to buttons
  document.querySelectorAll('.btn, .nav-link, .group-card, .mobile-bottom-nav-item').forEach(element => {
    element.addEventListener('touchstart', () => haptic(10), { passive: true });
  });
  
  // Add haptic feedback to form submissions
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => haptic(20));
  });
}

// ── Swipe Gestures ──
function initSwipeGestures() {
  let touchStartX = 0;
  let touchEndX = 0;
  
  document.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });
  
  document.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  }, { passive: true });
  
  function handleSwipe() {
    const swipeThreshold = 100;
    const diff = touchEndX - touchStartX;
    
    if (Math.abs(diff) > swipeThreshold) {
      if (diff > 0) {
        // Swipe right - go back
        if (window.history.length > 1) {
          window.history.back();
        }
      }
      // Swipe left could be used for forward navigation
    }
  }
}

// ── Page Transitions ──
function initPageTransitions() {
  // Add transition class to main content
  const pageContainer = document.querySelector('.page-container');
  if (pageContainer) {
    pageContainer.classList.add('page-transition');
  }
  
  // Smooth transitions between pages
  document.querySelectorAll('a:not([target="_blank"])').forEach(link => {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href && href.startsWith('/') && !href.includes('#')) {
        e.preventDefault();
        
        // Fade out
        if (pageContainer) {
          pageContainer.style.opacity = '0';
          pageContainer.style.transform = 'translateY(10px)';
        }
        
        // Navigate after animation
        setTimeout(() => {
          window.location.href = href;
        }, 200);
      }
    });
  });
}

// ── Hide Address Bar ──
function hideAddressBar() {
  // Scroll to hide address bar on mobile browsers
  window.addEventListener('load', () => {
    setTimeout(() => {
      window.scrollTo(0, 1);
    }, 0);
  });
}

// ── Toast Notifications ──
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="icon">${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span>
    <span>${message}</span>
  `;
  
  document.body.appendChild(toast);
  
  // Haptic feedback
  if ('vibrate' in navigator) {
    navigator.vibrate(type === 'error' ? [50, 50, 50] : 20);
  }
  
  // Remove after 3 seconds
  setTimeout(() => {
    toast.style.animation = 'slideOutDown 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// ── Loading Skeleton ──
function showLoadingSkeleton(container) {
  const skeleton = `
    <div class="skeleton-card">
      <div style="display: flex; gap: 12px; margin-bottom: 12px;">
        <div class="skeleton-circle"></div>
        <div style="flex: 1;">
          <div class="skeleton-line"></div>
          <div class="skeleton-line short"></div>
        </div>
      </div>
      <div class="skeleton-line"></div>
      <div class="skeleton-line"></div>
    </div>
  `;
  
  if (container) {
    container.innerHTML = skeleton.repeat(3);
  }
}

// ── Floating Action Button ──
function addFAB(icon, onClick) {
  const fab = document.createElement('button');
  fab.className = 'fab';
  fab.innerHTML = icon;
  fab.addEventListener('click', onClick);
  document.body.appendChild(fab);
  return fab;
}

// ── Optimize Images for Mobile ──
function optimizeImages() {
  const images = document.querySelectorAll('img');
  images.forEach(img => {
    // Add loading="lazy" if not present
    if (!img.hasAttribute('loading')) {
      img.setAttribute('loading', 'lazy');
    }
    
    // Add error handler
    img.addEventListener('error', function() {
      this.src = '/static/icons/icon-192x192.png'; // Fallback image
    });
  });
}

// ── Network Status Indicator ──
function initNetworkStatus() {
  window.addEventListener('online', () => {
    showToast('Back online!', 'success');
  });
  
  window.addEventListener('offline', () => {
    showToast('No internet connection', 'error');
  });
}

// ── Prevent Zoom on Double Tap ──
let lastTouchEnd = 0;
document.addEventListener('touchend', function(event) {
  const now = Date.now();
  if (now - lastTouchEnd <= 300) {
    event.preventDefault();
  }
  lastTouchEnd = now;
}, { passive: false });

// ── Smooth Scroll to Top ──
function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

// Add scroll to top button
window.addEventListener('scroll', function() {
  if (window.innerWidth <= 768) {
    const scrollBtn = document.getElementById('scrollTopBtn');
    if (window.scrollY > 300) {
      if (!scrollBtn) {
        const btn = document.createElement('button');
        btn.id = 'scrollTopBtn';
        btn.className = 'fab';
        btn.style.bottom = 'calc(150px + env(safe-area-inset-bottom))';
        btn.innerHTML = '↑';
        btn.addEventListener('click', scrollToTop);
        document.body.appendChild(btn);
      }
    } else if (scrollBtn) {
      scrollBtn.remove();
    }
  }
});

// ── Initialize All Features ──
if (window.innerWidth <= 768) {
  optimizeImages();
  initNetworkStatus();
}

// ── Export Functions ──
window.MobileApp = {
  showToast,
  showLoadingSkeleton,
  addFAB,
  scrollToTop
};

// ── Handle Flash Messages as Toasts ──
document.addEventListener('DOMContentLoaded', function() {
  if (window.innerWidth <= 768) {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
      const type = alert.classList.contains('alert-success') ? 'success' :
                   alert.classList.contains('alert-danger') || alert.classList.contains('alert-error') ? 'error' : 'info';
      showToast(alert.textContent.trim(), type);
      alert.style.display = 'none';
    });
  }
});
