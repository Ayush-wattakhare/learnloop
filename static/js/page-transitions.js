/* ══════════════════════════════════════════════════════════════════════
   Smooth Page Transitions & Loading Optimization
   ══════════════════════════════════════════════════════════════════════ */

// Preload pages on hover
document.addEventListener('DOMContentLoaded', function() {
    // Preload links on hover (desktop only)
    if (window.innerWidth > 768) {
        document.querySelectorAll('a[href^="/"]').forEach(link => {
            link.addEventListener('mouseenter', function() {
                const url = this.getAttribute('href');
                if (url && !url.includes('#')) {
                    preloadPage(url);
                }
            }, { once: true });
        });
    }
    
    // Instant page transitions
    initInstantPageTransitions();
    
    // Show loading indicator
    initLoadingIndicator();
});

// Preload page
function preloadPage(url) {
    const link = document.createElement('link');
    link.rel = 'prefetch';
    link.href = url;
    document.head.appendChild(link);
}

// Instant page transitions
function initInstantPageTransitions() {
    // Intercept navigation clicks
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a[href^="/"]');
        
        if (link && !link.hasAttribute('target') && !link.hasAttribute('download')) {
            const url = link.getAttribute('href');
            
            // Skip if it's a hash link or special link
            if (url.includes('#') || url.includes('logout') || url.includes('exit-demo')) {
                return;
            }
            
            e.preventDefault();
            navigateToPage(url);
        }
    });
    
    // Handle back/forward buttons
    window.addEventListener('popstate', function(e) {
        if (e.state && e.state.url) {
            loadPageContent(e.state.url, false);
        }
    });
}

// Navigate to page with transition
function navigateToPage(url) {
    // Show loading indicator
    showLoadingIndicator();
    
    // Add to history
    history.pushState({ url: url }, '', url);
    
    // Load page content
    loadPageContent(url, true);
}

// Load page content via AJAX
function loadPageContent(url, addToHistory) {
    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        // Parse HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        // Get new content
        const newContent = doc.querySelector('.page-container, .container, main, [role="main"]');
        const currentContent = document.querySelector('.page-container, .container, main, [role="main"]');
        
        if (newContent && currentContent) {
            // Fade out
            currentContent.style.opacity = '0';
            currentContent.style.transform = 'translateY(10px)';
            
            setTimeout(() => {
                // Replace content
                currentContent.innerHTML = newContent.innerHTML;
                
                // Update title
                const newTitle = doc.querySelector('title');
                if (newTitle) {
                    document.title = newTitle.textContent;
                }
                
                // Scroll to top
                window.scrollTo(0, 0);
                
                // Fade in
                currentContent.style.opacity = '1';
                currentContent.style.transform = 'translateY(0)';
                
                // Hide loading indicator
                hideLoadingIndicator();
                
                // Re-initialize scripts
                reinitializeScripts();
            }, 200);
        } else {
            // Fallback to normal navigation
            window.location.href = url;
        }
    })
    .catch(error => {
        console.error('Navigation error:', error);
        // Fallback to normal navigation
        window.location.href = url;
    });
}

// Loading indicator
let loadingIndicator;

function initLoadingIndicator() {
    loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'page-loading-indicator';
    loadingIndicator.innerHTML = '<div class="loading-bar"></div>';
    document.body.appendChild(loadingIndicator);
}

function showLoadingIndicator() {
    if (loadingIndicator) {
        loadingIndicator.classList.add('active');
    }
}

function hideLoadingIndicator() {
    if (loadingIndicator) {
        loadingIndicator.classList.remove('active');
    }
}

// Re-initialize scripts after content load
function reinitializeScripts() {
    // Re-run any initialization scripts
    if (window.initMobileMenu) window.initMobileMenu();
    if (window.optimizeImages) window.optimizeImages();
    
    // Trigger custom event for other scripts
    window.dispatchEvent(new Event('contentLoaded'));
}

// Add CSS for loading indicator
const style = document.createElement('style');
style.textContent = `
.page-loading-indicator {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    z-index: 99999;
    opacity: 0;
    transition: opacity 0.2s;
}

.page-loading-indicator.active {
    opacity: 1;
}

.loading-bar {
    height: 100%;
    background: linear-gradient(90deg, #2563EB, #4338CA, #2563EB);
    background-size: 200% 100%;
    animation: loadingAnimation 1s ease-in-out infinite;
}

@keyframes loadingAnimation {
    0% {
        background-position: 200% 0;
    }
    100% {
        background-position: -200% 0;
    }
}

/* Smooth content transitions */
.page-container,
.container,
main,
[role="main"] {
    transition: opacity 0.2s ease, transform 0.2s ease;
}
`;
document.head.appendChild(style);

// Optimize images on content load
window.addEventListener('contentLoaded', function() {
    const images = document.querySelectorAll('img:not([loading])');
    images.forEach(img => {
        img.setAttribute('loading', 'lazy');
    });
});
