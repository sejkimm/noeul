/*!
 * noeul.js | MIT License
 * Marks the table-of-contents link of the section being read with aria-current.
 * Usage: load it with a script tag (src="noeul.js", defer) or inline it anywhere.
 */
const noeulToc = () => {
  const links = new Map();
  for (const a of document.querySelectorAll('nav a[href^="#"]')) {
    const target = document.getElementById(decodeURIComponent(a.hash.slice(1)));
    if (target) links.set(target, a);
  }
  if (links.size === 0) return;

  const headings = [...links.keys()];
  let current = null;
  const update = () => {
    let next = headings[0];
    for (const h of headings) if (h.getBoundingClientRect().top <= 96) next = h;
    if (next === current) return;
    links.get(current)?.removeAttribute('aria-current');
    links.get(next).setAttribute('aria-current', 'location');
    current = next;
  };
  addEventListener('scroll', update, { passive: true });
  addEventListener('resize', update);
  update();
};
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', noeulToc);
else noeulToc();
