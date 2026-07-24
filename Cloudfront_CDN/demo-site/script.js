// Everything below runs client-side, in the visitor's browser.
// The HTML/CSS/JS themselves are static files cached by CloudFront —
// this script is what proves per-visitor personalization is still possible
// on top of a globally cached, static shell.

document.getElementById('year').textContent = new Date().getFullYear();

function tick() {
  const el = document.getElementById('clock');
  if (el) el.textContent = new Date().toLocaleTimeString();
}
setInterval(tick, 1000);
tick();

const tzEl = document.getElementById('tz');
if (tzEl) {
  tzEl.textContent = `your browser reports: ${Intl.DateTimeFormat().resolvedOptions().timeZone}`;
}
