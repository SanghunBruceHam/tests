
const CACHE_NAME = 'egen-teto-test-v1.3.0';
const OFFLINE_URL = './offline.html';

// 캐시할 리소스들  
const STATIC_CACHE_URLS = [
  './',
  './index.html',
  './style.css',
  './manifest.json',
  './favicon.png',
  './thumbnail.png',
  OFFLINE_URL,
  // 폰트
  'https://fonts.googleapis.com/css2?family=Gmarket+Sans:wght@400;700&display=swap',
  // 중요한 아이콘
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css'
];

// 동적 캐시할 리소스 패턴
const DYNAMIC_CACHE_PATTERNS = [
  /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
  /\.(?:js|css)$/,
  /fonts\.googleapis\.com/,
  /fonts\.gstatic\.com/
];

// 설치 이벤트
self.addEventListener('install', (event) => {
  console.log('[SW] 설치 중...');
  
  event.waitUntil(
    (async () => {
      try {
        const cache = await caches.open(CACHE_NAME);
        
        // 오프라인 페이지를 먼저 캐시
        await cache.add(OFFLINE_URL);
        
        // 나머지 리소스들을 병렬로 캐시
        const cachePromises = STATIC_CACHE_URLS.map(async (url) => {
          try {
            await cache.add(url);
            console.log(`[SW] 캐시됨: ${url}`);
          } catch (error) {
            console.warn(`[SW] 캐시 실패: ${url}`, error);
          }
        });
        
        await Promise.allSettled(cachePromises);
        console.log('[SW] 정적 리소스 캐시 완료');
        
        // 즉시 활성화
        self.skipWaiting();
      } catch (error) {
        console.error('[SW] 설치 중 오류:', error);
      }
    })()
  );
});

// 활성화 이벤트
self.addEventListener('activate', (event) => {
  console.log('[SW] 활성화 중...');
  
  event.waitUntil(
    (async () => {
      try {
        // 이전 캐시 정리
        const cacheNames = await caches.keys();
        const deletePromises = cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => {
            console.log(`[SW] 이전 캐시 삭제: ${name}`);
            return caches.delete(name);
          });
        
        await Promise.all(deletePromises);
        
        // 모든 클라이언트 제어 시작
        await self.clients.claim();
        
        console.log('[SW] 활성화 완료');
      } catch (error) {
        console.error('[SW] 활성화 중 오류:', error);
      }
    })()
  );
});

// 네트워크 요청 처리
self.addEventListener('fetch', (event) => {
  // GET 요청만 처리
  if (event.request.method !== 'GET') {
    return;
  }

  // Chrome extension 요청 무시
  if (event.request.url.startsWith('chrome-extension://')) {
    return;
  }

  const { url } = event.request;

  event.respondWith(
    (async () => {
      try {
        // 1. 캐시에서 먼저 확인
        const cachedResponse = await caches.match(event.request);
        if (cachedResponse) {
          console.log(`[SW] 캐시에서 제공: ${url}`);
          
          // 백그라운드에서 업데이트 (stale-while-revalidate)
          updateCache(event.request);
          
          return cachedResponse;
        }

        // 2. 네트워크에서 가져오기
        const networkResponse = await fetch(event.request);
        
        // 3. 성공적인 응답이면 캐시에 저장
        if (networkResponse.ok) {
          await saveToCache(event.request, networkResponse.clone());
        }
        
        return networkResponse;
        
      } catch (error) {
        console.warn(`[SW] 네트워크 오류: ${url}`, error);
        
        // 4. 오프라인 대응
        return handleOffline(event.request);
      }
    })()
  );
});

// 캐시 업데이트 함수
async function updateCache(request) {
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      await saveToCache(request, networkResponse);
      console.log(`[SW] 백그라운드 업데이트: ${request.url}`);
    }
  } catch (error) {
    console.warn(`[SW] 백그라운드 업데이트 실패: ${request.url}`, error);
  }
}

// 캐시 저장 함수
async function saveToCache(request, response) {
  const { url } = request;
  
  // 캐시할 리소스인지 확인
  if (!shouldCache(url)) {
    return;
  }
  
  try {
    const cache = await caches.open(CACHE_NAME);
    await cache.put(request, response);
    console.log(`[SW] 캐시 저장: ${url}`);
  } catch (error) {
    console.warn(`[SW] 캐시 저장 실패: ${url}`, error);
  }
}

// 캐시 여부 판단
function shouldCache(url) {
  // 애드센스 등 광고 관련 요청 제외
  if (url.includes('googlesyndication') || url.includes('googleads')) {
    return false;
  }
  
  // 분석 도구 제외
  if (url.includes('google-analytics') || url.includes('gtag')) {
    return false;
  }
  
  // 동적 캐시 패턴 확인
  return DYNAMIC_CACHE_PATTERNS.some(pattern => pattern.test(url)) ||
         url.includes('/egen-teto/ko/');
}

// 오프라인 처리
async function handleOffline(request) {
  const { destination } = request;
  
  try {
    // HTML 페이지 요청 시 오프라인 페이지 반환
    if (destination === 'document') {
      const offlineCache = await caches.match(OFFLINE_URL);
      if (offlineCache) {
        return offlineCache;
      }
    }
    
    // 이미지 요청 시 대체 이미지 반환
    if (destination === 'image') {
      return createFallbackResponse('🖼️', 'image/svg+xml');
    }
    
    // 폰트 요청 시 대체 응답
    if (request.url.includes('font')) {
      return createFallbackResponse('', 'font/woff2');
    }
    
    // 기본 오프라인 응답
    return createFallbackResponse('오프라인 상태입니다', 'text/plain');
    
  } catch (error) {
    console.error('[SW] 오프라인 처리 오류:', error);
    return new Response('서비스를 사용할 수 없습니다', {
      status: 503,
      statusText: 'Service Unavailable'
    });
  }
}

// 대체 응답 생성
function createFallbackResponse(content, contentType) {
  return new Response(content, {
    headers: {
      'Content-Type': contentType,
      'Cache-Control': 'no-cache'
    }
  });
}

// 메시지 처리 (클라이언트와 통신)
self.addEventListener('message', (event) => {
  const { action, data } = event.data;
  
  switch (action) {
    case 'SKIP_WAITING':
      self.skipWaiting();
      break;
      
    case 'GET_CACHE_SIZE':
      getCacheSize().then(size => {
        event.ports[0].postMessage({ cacheSize: size });
      });
      break;
      
    case 'CLEAR_CACHE':
      clearCache().then(success => {
        event.ports[0].postMessage({ success });
      });
      break;
      
    case 'UPDATE_CACHE':
      updateAllCache().then(success => {
        event.ports[0].postMessage({ success });
      });
      break;
  }
});

// 캐시 크기 조회
async function getCacheSize() {
  try {
    const cache = await caches.open(CACHE_NAME);
    const keys = await cache.keys();
    let totalSize = 0;
    
    for (const request of keys) {
      const response = await cache.match(request);
      if (response) {
        const blob = await response.blob();
        totalSize += blob.size;
      }
    }
    
    return {
      count: keys.length,
      size: totalSize,
      sizeFormatted: formatBytes(totalSize)
    };
  } catch (error) {
    console.error('[SW] 캐시 크기 조회 실패:', error);
    return { count: 0, size: 0, sizeFormatted: '0 B' };
  }
}

// 캐시 지우기
async function clearCache() {
  try {
    const deleted = await caches.delete(CACHE_NAME);
    console.log('[SW] 캐시 지우기:', deleted ? '성공' : '실패');
    return deleted;
  } catch (error) {
    console.error('[SW] 캐시 지우기 실패:', error);
    return false;
  }
}

// 모든 캐시 업데이트
async function updateAllCache() {
  try {
    const cache = await caches.open(CACHE_NAME);
    const updatePromises = STATIC_CACHE_URLS.map(async (url) => {
      try {
        const response = await fetch(url);
        if (response.ok) {
          await cache.put(url, response);
        }
      } catch (error) {
        console.warn(`[SW] 업데이트 실패: ${url}`, error);
      }
    });
    
    await Promise.allSettled(updatePromises);
    console.log('[SW] 캐시 업데이트 완료');
    return true;
  } catch (error) {
    console.error('[SW] 캐시 업데이트 실패:', error);
    return false;
  }
}

// 바이트 포맷팅
function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 B';
  
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// 백그라운드 동기화 (미래 기능)
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-analytics') {
    event.waitUntil(syncAnalytics());
  }
});

// 분석 데이터 동기화
async function syncAnalytics() {
  try {
    // 로컬에 저장된 오프라인 분석 데이터 전송
    console.log('[SW] 백그라운드 동기화 완료');
  } catch (error) {
    console.error('[SW] 백그라운드 동기화 실패:', error);
  }
}
