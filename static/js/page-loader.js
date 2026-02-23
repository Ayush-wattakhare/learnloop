/* ══════════════════════════════════════════════════════════════════════
   Fast Page Loading Indicator for LearnLoop
   ══════════════════════════════════════════════════════════════════════ */

// Show loading indicator on page navigation
(function() {
    // Create loading indicator
    const loader = document.createElement('div');
    loader.id = 'page-loader';
    loader.innerHTML = '<div class="loader-spinner"></div>';
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #2563EB, #4338CA, #2563EB);
        background-size: 200% 100%;
        animation: loading 1s ease-in-out infinite;
        z-index: 99999;
        display: none;
    `;
    
    // Add to page
    document.addEventListener('DOMContentLoaded', function() {
        document.body.appendChild(loader);
    });
    
    // Show loader on link clicks
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a[href^="/"]');
        if (link && !link.hasAttribute('target') && !link.hasAttribute('download')) {
            loader.style.display = 'block';
        }
    });
    
    // Show loader on form submissions
    document.addEventListener('submit', function(e) {
        loader.style.display = 'block';
    });
    
    // Hide loader when page loads
    window.addEventListener('load', function() {
        loader.style.display = 'none';
    });
    
    // Hide loader on page show (back/forward navigation)
    window.addEventListener('pageshow', function() {
        loader.style.display = 'none';
    });
    
    // Add animation keyframes
    const style = document.createElement('style');
    style.textContent = `
        @keyframes loading {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    `;
    document.head.appendChild(style);
})();
