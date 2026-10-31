/**
 * AutoFlow — Flow Anti-Hijack Interceptor
 *
 * Runs at document_start in world: "MAIN" on https://flow.google.com/*
 * Captures authentic grecaptcha.enterprise.execute before Google Flow's
 * bundle (AiSandboxAngularFrontend / gTa) overwrites it with the honeypot
 * wrapper that silently forces { action: "extension_hijack_detected" }.
 */
(function () {
  if (window.__af_interceptor_installed) return;
  window.__af_interceptor_installed = true;

  function saveIfClean(fn) {
    if (!fn || typeof fn !== 'function') return;
    if (window.__real_execute) return;
    try {
      var str = fn.toString();
      if (!str.includes('extension_hijack_detected')) {
        window.__real_execute = fn;
      }
    } catch (e) {}
  }

  var origDef = Object.defineProperty;
  Object.defineProperty = function (obj, prop, desc) {
    if (prop === 'execute') {
      if (obj && obj.execute) {
        saveIfClean(obj.execute);
      }
      if (desc && typeof desc.value === 'function') {
        saveIfClean(desc.value);
      }
    }
    return origDef.apply(this, arguments);
  };

  var timer = setInterval(function () {
    if (window.grecaptcha && window.grecaptcha.enterprise && window.grecaptcha.enterprise.execute) {
      saveIfClean(window.grecaptcha.enterprise.execute);
    }
  }, 5);
  setTimeout(function () {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }, 20000);
})();