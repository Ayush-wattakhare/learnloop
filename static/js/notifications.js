/* ══════════════════════════════════════════════════════════════════════
   Real-time Notification System
   ══════════════════════════════════════════════════════════════════════ */

// Notification popup queue
let notificationQueue = [];
let isShowingNotification = false;

// Check for new notifications every 30 seconds
setInterval(checkForNewNotifications, 30000);

// Check on page load
document.addEventListener('DOMContentLoaded', function() {
    checkForNewNotifications();
});

// Check for new notifications
function checkForNewNotifications() {
    fetch('/notifications/count')
        .then(response => response.json())
        .then(data => {
            updateNotificationBadge(data.count);
            
            // If there are new notifications, fetch them
            if (data.count > 0) {
                fetchLatestNotifications();
            }
        })
        .catch(error => console.error('Error checking notifications:', error));
}

// Fetch latest notifications
function fetchLatestNotifications() {
    fetch('/api/latest-notifications')
        .then(response => response.json())
        .then(data => {
            if (data.notifications && data.notifications.length > 0) {
                data.notifications.forEach(notif => {
                    // Only show if not already shown
                    if (!isNotificationShown(notif.id)) {
                        showNotificationPopup(notif);
                        markNotificationAsShown(notif.id);
                    }
                });
            }
        })
        .catch(error => console.error('Error fetching notifications:', error));
}

// Show notification popup
function showNotificationPopup(notification) {
    // Add to queue
    notificationQueue.push(notification);
    
    // Process queue if not already showing
    if (!isShowingNotification) {
        processNotificationQueue();
    }
}

// Process notification queue
function processNotificationQueue() {
    if (notificationQueue.length === 0) {
        isShowingNotification = false;
        return;
    }
    
    isShowingNotification = true;
    const notification = notificationQueue.shift();
    
    // Create popup element
    const popup = document.createElement('div');
    popup.className = 'notification-popup';
    popup.innerHTML = `
        <div class="notification-popup-icon">
            ${getNotificationIcon(notification.type)}
        </div>
        <div class="notification-popup-content">
            <div class="notification-popup-title">${notification.title}</div>
            <div class="notification-popup-message">${notification.message}</div>
        </div>
        <button class="notification-popup-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    // Add click handler
    if (notification.link) {
        popup.style.cursor = 'pointer';
        popup.addEventListener('click', function(e) {
            if (!e.target.classList.contains('notification-popup-close')) {
                window.location.href = notification.link;
            }
        });
    }
    
    // Add to page
    document.body.appendChild(popup);
    
    // Animate in
    setTimeout(() => popup.classList.add('show'), 10);
    
    // Remove after 5 seconds
    setTimeout(() => {
        popup.classList.remove('show');
        setTimeout(() => {
            popup.remove();
            processNotificationQueue(); // Process next in queue
        }, 300);
    }, 5000);
}

// Get notification icon
function getNotificationIcon(type) {
    const icons = {
        'friend_request': '👥',
        'group_created': '📚',
        'message': '💬',
        'group_invite': '📨',
        'default': '🔔'
    };
    return icons[type] || icons.default;
}

// Update notification badge
function updateNotificationBadge(count) {
    const badge = document.getElementById('notificationBadge');
    if (badge) {
        if (count > 0) {
            badge.textContent = count > 99 ? '99+' : count;
            badge.style.display = 'block';
        } else {
            badge.style.display = 'none';
        }
    }
}

// Track shown notifications (using localStorage)
function isNotificationShown(notifId) {
    const shown = JSON.parse(localStorage.getItem('shownNotifications') || '[]');
    return shown.includes(notifId);
}

function markNotificationAsShown(notifId) {
    let shown = JSON.parse(localStorage.getItem('shownNotifications') || '[]');
    shown.push(notifId);
    
    // Keep only last 100 notifications
    if (shown.length > 100) {
        shown = shown.slice(-100);
    }
    
    localStorage.setItem('shownNotifications', JSON.stringify(shown));
}

// Clear old shown notifications (older than 7 days)
function clearOldShownNotifications() {
    // This would require storing timestamps, simplified for now
    const shown = JSON.parse(localStorage.getItem('shownNotifications') || '[]');
    if (shown.length > 200) {
        localStorage.setItem('shownNotifications', JSON.stringify(shown.slice(-100)));
    }
}

// Run cleanup on page load
clearOldShownNotifications();

// CSS for notification popup
const style = document.createElement('style');
style.textContent = `
.notification-popup {
    position: fixed;
    top: 80px;
    right: 20px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    padding: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    max-width: 400px;
    z-index: 9999;
    transform: translateX(450px);
    transition: transform 0.3s ease;
    border-left: 4px solid #2563EB;
}

.notification-popup.show {
    transform: translateX(0);
}

.notification-popup-icon {
    font-size: 2rem;
    flex-shrink: 0;
}

.notification-popup-content {
    flex: 1;
    min-width: 0;
}

.notification-popup-title {
    font-weight: 700;
    font-size: 0.95rem;
    color: #111827;
    margin-bottom: 4px;
}

.notification-popup-message {
    font-size: 0.85rem;
    color: #6B7280;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

.notification-popup-close {
    background: #F3F4F6;
    color: #6B7280;
    border: none;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.2s;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
}

.notification-popup-close:hover {
    background: #EF4444;
    color: white;
}

@media (max-width: 768px) {
    .notification-popup {
        top: auto;
        bottom: calc(90px + env(safe-area-inset-bottom));
        left: 16px;
        right: 16px;
        max-width: none;
        transform: translateY(200px);
    }
    
    .notification-popup.show {
        transform: translateY(0);
    }
}
`;
document.head.appendChild(style);
