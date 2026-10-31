// Runs in the PAGE's MAIN world (injected via manifest content_scripts
// in world: 'MAIN' at document_start, or fallback <script> by mainworld.ts).
// Executes NAMED primitives and replies via postMessage.
//
// MUST be a plain .js file, NOT .ts: Chrome serves extension .ts files with the
// MIME type video/mp2t, so a <script src="....ts"> is rejected by the browser as
// a non-JavaScript MIME.
// NO eval / new Function (flow.google.com is script-src 'self' with no unsafe-eval).
;(function () {
  if (typeof window !== 'undefined' && window.__af_mainworld_bridge_installed) return
  if (typeof window !== 'undefined') window.__af_mainworld_bridge_installed = true

  const REQ = 'AF_MW_REQ'
  const RES = 'AF_MW_RES'
  const DEFAULT_SITE_KEY = '6LdsFiUsAAAAAIjVDZcuLhaHiDn5nnHVXVRQGeMV'

  // Best-effort reCAPTCHA site-key discovery from grecaptcha's internal config,
  // for pages that don't expose it via rc.
  function detectSiteKey() {
    try {
      const cfg = typeof ___grecaptcha_cfg !== 'undefined' ? ___grecaptcha_cfg : undefined
      const clients = cfg && cfg.clients
      if (clients) {
        for (const ck of Object.keys(clients)) {
          const client = clients[ck]
          for (const p of Object.keys(client)) {
            const v = client[p]
            if (v && typeof v === 'object') {
              for (const p2 of Object.keys(v)) {
                const v2 = v[p2]
                if (v2 && typeof v2 === 'object' && v2.sitekey) return v2.sitekey
              }
            }
          }
        }
      }
      const scripts = document.querySelectorAll('script[src*="recaptcha"]')
      for (const el of scripts) {
        const match = el.src && el.src.match(/[?&]render=([^&]+)/)
        if (match && match[1] && match[1] !== 'explicit') return match[1]
      }
    } catch (e) {
      /* ignore */
    }
    return ''
  }

  // grecaptcha.enterprise is native on a flow.google.com PROJECT page but NOT on the
  // public /about page. It CAN be injected there with the right recipe (proven in the
  // Auth Helper): a Trusted Types 'default' policy that allowlists ONLY google/gstatic
  // recaptcha URLs (require-trusted-types-for 'script' otherwise blocks reCAPTCHA's own
  // child-script loads -> execute never initialises), plus copying the page nonce (CSP
  // script-src is nonce-based, no strict-dynamic). No CSP removal, no extra permission.
  // Only used on the hidden /about mint tab; a /project page already has grecaptcha so
  // this is a no-op there.
  function injectGrecaptcha(siteKey) {
    try {
      if (typeof grecaptcha !== 'undefined' && grecaptcha.enterprise && (window.__real_execute || grecaptcha.enterprise.execute)) return
      const effectiveKey = siteKey || DEFAULT_SITE_KEY
      if (document.querySelector('script[data-af-recaptcha]')) return
      try {
        if (window.trustedTypes && window.trustedTypes.createPolicy) {
          window.trustedTypes.createPolicy('default', {
            createScriptURL: function (u) {
              if (/^https:\/\/(www\.google\.com\/recaptcha\/|www\.gstatic\.com\/recaptcha\/)/.test(u)) return u
              throw new Error('blocked')
            },
            createScript: function (s) { return s },
            createHTML: function (s) { return s },
          })
        }
      } catch (e) { /* default policy already exists -> reuse it */ }
      var s = document.createElement('script')
      var nEl = document.querySelector('script[nonce]')
      if (nEl && nEl.nonce) s.nonce = nEl.nonce
      s.src = 'https://www.google.com/recaptcha/enterprise.js?render=' + encodeURIComponent(effectiveKey)
      s.async = true
      s.setAttribute('data-af-recaptcha', '1')
      ;(document.head || document.documentElement).appendChild(s)
    } catch (e) { /* best-effort */ }
  }

  // Poll for grecaptcha to appear (it loads async) then mint.
  function waitGrecaptcha(ms) {
    return new Promise((resolve) => {
      var deadline = Date.now() + ms
      var check = function () {
        if (typeof grecaptcha !== 'undefined' && grecaptcha.enterprise && (window.__real_execute || grecaptcha.enterprise.execute)) return resolve(true)
        if (Date.now() > deadline) return resolve(false)
        setTimeout(check, 300)
      }
      check()
    })
  }

  async function mintCaptcha(payload) {
    const siteKey = (payload && payload.siteKey) || ''
    const action = (payload && payload.action) || ''
    // DEBUG: reCAPTCHA site keys are PUBLIC (embedded in the page), so logging them is
    // safe and lets us compare the key we mint with vs the key the page actually loaded
    // -> a mismatch means the token is for the wrong key -> Flow rejects (UNUSUAL_ACTIVITY).
    const detected = detectSiteKey()
    const effectiveKey = siteKey || detected || DEFAULT_SITE_KEY
    const dbg = {
      url: location.href,
      action,
      keyPassed: siteKey || '(none-auto-detect)',
      keyDetected: detected || '(none)',
      keyMatch: siteKey && detected ? siteKey === detected : null,
      keyUsed: effectiveKey,
    }
    // On the public /about page grecaptcha isn't native -> inject it (no-op on /project).
    if (!(typeof grecaptcha !== 'undefined' && grecaptcha.enterprise && (window.__real_execute || grecaptcha.enterprise.execute))) {
      injectGrecaptcha(effectiveKey)
    }
    if (!(await waitGrecaptcha(10000))) {
      dbg.ready = false
      return { token: null, error: 'grecaptcha.enterprise not available (open a flow.google.com project page)', dbg }
    }
    dbg.ready = true
    const key = effectiveKey
    if (!key) return { token: null, error: 'site key unresolved', dbg }
    try {
      await new Promise((resolve) => grecaptcha.enterprise.ready(resolve))
      const t0 = Date.now()
      const execFn = (typeof window !== 'undefined' && window.__real_execute) || grecaptcha.enterprise.execute
      const token = await Promise.race([
        execFn(key, { action }),
        new Promise((_, reject) => setTimeout(() => reject(new Error('execute timeout')), 15000)),
      ])
      dbg.mintMs = Date.now() - t0
      dbg.tokenLen = token ? String(token).length : 0
      return { token, error: null, dbg }
    } catch (e) {
      return { token: null, error: String((e && e.message) || e), dbg }
    }
  }

  // Scrape the flow.google.com session tokens from the page's MAIN-world globals.
  // window.WIZ_global_data is a page global (not visible from the content script's
  // isolated world), so it must be read here. at=SNlM0e (the only truly required
  // token), bl=cfb2h, sid=FdrFJe (docs/flow-google-com/00). Also best-effort the
  // signed-in email for per-account cache keying (mirrors flow_google_bridge
  // _email_from_html). Returns nulls when the page hasn't loaded a session yet.
  function scrapeEmail() {
    try {
      var html = document.documentElement ? document.documentElement.innerHTML : ''
      if (!html) return ''
      var pats = [
        /"([\w.+-]+@[\w-]+\.[\w.]+)"\s*,\s*(?:true|1)\s*\]/, // OGB account tuple
        /\\"email\\":\\"([\w.+-]+@[\w-]+\.[\w.]+)\\"/,
        /"email":"([\w.+-]+@[\w-]+\.[\w.]+)"/,
      ]
      for (var i = 0; i < pats.length; i++) {
        var m = html.match(pats[i])
        if (m) return m[1]
      }
      var g = html.match(/[\w.+-]+@(?:gmail\.com|googlemail\.com|[\w-]+\.[\w.]+)/)
      return g ? g[0] : ''
    } catch (e) {
      return ''
    }
  }

  function flowAuth() {
    try {
      var w = typeof WIZ_global_data !== 'undefined' ? WIZ_global_data : (window.WIZ_global_data || null)
      var at = w && w.SNlM0e ? String(w.SNlM0e) : ''
      var bl = w && w.cfb2h ? String(w.cfb2h) : ''
      var sid = w && w.FdrFJe != null ? String(w.FdrFJe) : ''
      return { at: at, bl: bl, sid: sid, email: scrapeEmail() }
    } catch (e) {
      return { at: '', bl: '', sid: '', email: '', error: String((e && e.message) || e) }
    }
  }

  async function handle(kind, payload) {
    if (kind === 'grecaptcha') return mintCaptcha(payload)
    if (kind === 'flowauth') return flowAuth()
    throw new Error('unknown mainworld kind: ' + kind)
  }

  window.addEventListener('message', (ev) => {
    // Same-window, same-origin requests only (the content script). Page scripts in
    // other frames can't drive grecaptcha through us or read the minted tokens.
    if (ev.source !== window || ev.origin !== location.origin) return
    const d = ev.data
    if (!d || d.__af !== REQ) return
    handle(d.kind, d.payload)
      .then((result) => window.postMessage({ __af: RES, id: d.id, result }, location.origin))
      .catch((e) => window.postMessage({ __af: RES, id: d.id, error: String((e && e.message) || e) }, location.origin))
  })
})();
