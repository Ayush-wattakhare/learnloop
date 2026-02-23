/* ══════════════════════════════════════════════════════════════════════
   Mobile App-Like Interactions for LearnLoop - OPTIMIZED
   ══════════════════════════════════════════════════════════════════════ */

// ── Initialize Mobile App Features (Optimized) ──
if (window.innerWidth <= 768) {
    // Use requestIdleCallback for non-critical features
    if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
            initBottomNavigation();
            initHapticFeedback();
        });
    } else {
        setTimeout(() => {
            initBottomNavigation();
            initHapticFeedback();
        }, 100);
    }
    
    // Critical features load immediately
    hideAddressBar();
    initPageTransitions();
}

// ── Bottom Navigation Bar (Fixed) ──
function initBottomNavigation() {
    const isLoggedIn = document.querySelector('.navbar-links a[href="/dashboard"]');
    if (!isLoggedIn) return;
    
    // Check if already exists
    if (document.querySelector('.mobile-bottom-nav')) return;
    
    const currentPath = window.location.pathname;
    const bottomNav = document.createElement('div');
    bottomNav.className = 'mobile-bottom-nav';
    bottomNav.innerHTML = `
        <a href="/dashboard" class="mobile-bottom-nav-item ${currentPath === '/dashboard' ? 'active' : ''}">
            <span class="icon">🏠</span>
            <span>Home</span>
        </a>
        <a href="/groups" class="mobile-bottom-nav-item ${currentPath === '/groups' || currentPath.includes('/group/') ? 'active' : ''}">
            <span class="icon">👥</span>
            <span>Groups</span>
        </a>
        <a href="/messages" class="mobile-bottom-nav-item ${currentPath === '/messages' || currentPath.includes('/chat/') ? 'active' : ''}">
            <span class="icon">💬</span>
            <span>Chat</span>
        </a>
        <a href="/voice-rooms" class="mobile-bottom-nav-item ${currentPath.includes('/voice-room') ? 'active' : ''}">
            <span class="icon">🎙️</span>
            <span>Rooms</span>
        </a>
        <a href="/profile" class="mobile-bottom-nav-item ${currentPath === '/profile' ? 'active' : ''}">
            <span class="icon">👤</span>
            <span>Me</span>
        </a>
    `;
    
    document.body.appendChild(bottomNav);
}

// ── Haptic Feedback (Lightweight) ──
function initHapticFeedback() {
    if (!('vibrate' in navigator)) return;
    
    const haptic = () => navigator.vibrate(10);
    
    // Use event delegation for better performance
    document.body.addEventListener('touchstart', (e) => {
        if (e.target.closest('.btn, .nav-link, .mobile-bottom-nav-item')) {
            haptic();
        }
    }, { passive: true });
}

// ── Fast Page Transitions ──
function initPageTransitions() {
    // Prefetch on hover (desktop) or touchstart (mobile)
    const prefetchLink = (href) => {
        if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;
        
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = href;
        document.head.appendChild(link);
    };
    
    // Prefetch on mobile touchstart
    document.body.addEventListener('touchstart', (e) => {
        const link = e.target.closest('a[href^="/"]');
        if (link) {
            prefetchLink(link.getAttribute('href'));
        }
    }, { passive: true });
}

// ── Hide Address Bar ──
function hideAddressBar() {
    window.addEventListener('load', () => {
        setTimeout(() => window.scrollTo(0, 1), 0);
    }, { once: true });
}

// ── Optimize Images (Lazy Loading) ──
if ('loading' in HTMLImageElement.prototype) {
    // Browser supports native lazy loading
    document.querySelectorAll('img').forEach(img => {
        if (!img.loading) img.loading = 'lazy';
    });
}

// ── Network Status (Lightweight) ──
if ('connection' in navigator) {
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (connection && connection.effectiveType === 'slow-2g') {
        document.body.classList.add('slow-connection');
    }
}

// ── Prevent Zoom on Double Tap (Optimized) ──
let lastTouchEnd = 0;
document.addEventListener('touchend', (e) => {
    const now = Date.now();
    if (now - lastTouchEnd <= 300) {
        e.preventDefault();
    }
    lastTouchEnd = now;
}, { passive: false });

// ── Export Functions ──
window.MobileApp = {
    showToast: (message, type = 'info') => {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = 'position:fixed;bottom:calc(90px + env(safe-area-inset-bottom));left:16px;right:16px;background:white;padding:16px;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.15);z-index:10000;animation:slideUp 0.3s ease';
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }
};
