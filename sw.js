// Généré par Atlas/tools/pwa.py, ne pas modifier à la main.
const CACHE = 'tgm-plate-trainer-v1';
const SHELL = ["./", "data/countries.js", "data/frontmap.js", "data/frontplates.js", "data/pairs.js", "data/plates.js", "data/regions/ca-map.js", "data/regions/ca.js", "data/regions/mx-map.js", "data/regions/mx.js", "data/regions/us-map.js", "data/regions/us.js", "icons/icon-192.png", "index.html", "manifest.webmanifest", "tgm-core.js"];
const THUMBS = false;   // Atlas : miniatures listées dans data.js, gardées dès la première visite
const MEDIA = /\.(png|jpe?g|webp|gif|svg|mp3)$/i;

self.addEventListener('install', e => e.waitUntil((async () => {
  const c = await caches.open(CACHE);
  await c.addAll(SHELL);
  if (THUMBS) {
    try {
      const t = await (await fetch('data.js', { cache: 'no-cache' })).text();
      await c.addAll([...new Set(t.match(/thumbs\/[0-9a-f]+\.webp/g) || [])]);
    } catch (err) {}
  }
  await self.skipWaiting();
})()));
self.addEventListener('activate', e => e.waitUntil((async () => {
  for (const k of await caches.keys()) if (k.startsWith('tgm-plate-trainer-') && k !== CACHE) await caches.delete(k);
  await self.clients.claim();
})()));
const keep = (req, res) => { if (res && res.ok && res.type === 'basic') { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); } return res; };
const timeout = (p, ms) => Promise.race([p, new Promise((_, no) => setTimeout(() => no(new Error('timeout')), ms))]);
self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin || !req.url.startsWith(self.registration.scope)) return;
  if (MEDIA.test(url.pathname)) {
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => keep(req, res))));
    return;
  }
  e.respondWith(timeout(fetch(req), 4000).then(res => keep(req, res))
    .catch(() => caches.match(req, { ignoreSearch: true }).then(hit => hit || Response.error())));
});
