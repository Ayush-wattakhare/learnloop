// LearnLoop Service Worker - Optimized for Speed
const CACHE_NAME = 'learnloop-v1.2.0';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/css/mobile-optimizations.css',
  '/static/css/mobile-app-enhancements.css',
  '/static/js/main.js',
  '/static/js/performance.js',
  '/static/js/mobile-app.js',
  '/static/js/page-loader.js',
  '/static/manifest.json'
];

// Install service worker and cache resources
self.addEventListener('install', event => {
  console.log('[Service Worker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Caching app shell');
        return cache.addAll(urlsToCache);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate service worker and clean old caches
self.addEventListener('activate', event => {
  console.log('[Service Worker] Activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Optimized fetch strategy
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;
  
  // Skip chrome extensions
  if (!event.request.url.startsWith('http')) return;
  
  // Cache-first strategy for static assets
  if (event.request.url.includes('/static/')) {
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          if (response) {
            return response;
          }
          return fetch(event.request).then(response => {
            if (response && response.status === 200) {
              const responseToCache = response.clone();
              caches.open(CACHE_NAME).then(cache => {
                cache.put(event.request, responseToCache);
              });
            }
            return response;
          });
        })
    );
    return;
  }
  
  // Network-first strategy for dynamic content
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Clone and cache successful responses
        if (response && response.status === 200) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(() => {
        // Fallback to cache if network fails
        return caches.match(event.request)
          .then(response => {
            if (response) {
              return response;
            }
            // Return offline page
            return caches.match('/');
          });
      })
  );
});

// Handle messages from clients
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Background sync for offline actions
self.addEventListener('sync', event => {
  if (event.tag === 'sync-data') {
    event.waitUntil(syncOfflineData());
  }
});

function syncOfflineData() {
  return Promise.resolve();
}

console.log('[Service Worker] Loaded and optimized');
