/* =========================================================
   BlueHarbor Advisory — shared site behaviour
   Adapted from the approved prototype's inline script so the
   exact same interactions and motion run on every page.
   Every lookup is guarded, since not every page has every
   component (e.g. only the home page has the hero chart).
   ========================================================= */
(() => {
  document.documentElement.classList.add('js');

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- Nav --- */
  const nav = $('#nav');
  if (nav) {
    const solid = nav.dataset.solid === 'true';
    const onScroll = () => nav.classList.toggle('scrolled', solid || scrollY > 24);
    onScroll();
    addEventListener('scroll', onScroll, { passive: true });

    const menuBtn = $('#menuBtn'), menu = $('#mobileMenu');
    if (menuBtn && menu) {
      menuBtn.addEventListener('click', () => {
        const open = menu.classList.toggle('open');
        document.body.classList.toggle('menu-open', open);
        menuBtn.setAttribute('aria-expanded', open);
        menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
        menuBtn.querySelector('path').setAttribute('d', open ? 'M6 6l12 12M18 6L6 18' : 'M4 7h16M4 12h16M4 17h10');
        nav.classList.add('scrolled');
      });
      $$('#mobileMenu a').forEach(a => a.addEventListener('click', () => { if (menu.classList.contains('open')) menuBtn.click(); }));
      matchMedia('(min-width: 981px)').addEventListener('change', e => { if (e.matches && menu.classList.contains('open')) menuBtn.click(); });
    }
  }

  /* active link: highlight by current in-view section (home) or current page (inner pages) */
  const links = $$('.nav-links a, .mobile-menu a');
  const sectionIds = ['about', 'services', 'approach', 'experience', 'team'];
  const sectionsPresent = sectionIds.filter(id => document.getElementById(id));
  if (sectionsPresent.length) {
    const spy = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
    }), { rootMargin: '-45% 0px -50% 0px' });
    sectionsPresent.forEach(id => spy.observe(document.getElementById(id)));
  }

  /* --- Split headlines into words (keeps the serif span + <br>) --- */
  const splitWords = (el) => {
    let i = 0;
    const walk = (node) => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(part => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
          const w = document.createElement('span'); w.className = 'w';
          const inner = document.createElement('span'); inner.textContent = part; inner.style.setProperty('--i', i++);
          w.appendChild(inner); frag.appendChild(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
    });
    el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
    walk(el); el.classList.add('split');
    [...el.querySelectorAll('.w')].forEach(w => w.setAttribute('aria-hidden', 'true'));
  };
  if (!reduce) $$('.hero h1, h2.h2, .page-hero h1').forEach(splitWords);

  /* stagger indexes for chips */
  $$('.chips, .deliv ul').forEach(list => [...list.children].forEach((c, i) => c.style.setProperty('--i', i)));

  /* --- Reveal --- */
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .12, rootMargin: '0px 0px -6% 0px' });
  $$('.reveal, .svc').forEach(el => io.observe(el));

  /* --- Hero contours (home only) --- */
  if (!reduce) $$('#contours path').forEach((p, i) => { p.classList.add('draw'); p.style.animationDelay = (i * 0.12) + 's'; });

  /* --- Audience tabs --- */
  const tabs = $$('.aud-tab');
  if (tabs.length) {
    const select = t => {
      tabs.forEach(x => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; document.getElementById(x.getAttribute('aria-controls')).hidden = !on; });
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(t));
      t.addEventListener('keydown', e => {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { const n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; select(n); n.focus(); }
      });
    });
  }

  /* --- Services accordion --- */
  $$('.svc-head').forEach(b => b.addEventListener('click', () => {
    const svc = b.closest('.svc'); const open = svc.dataset.open !== 'true';
    svc.dataset.open = open; b.setAttribute('aria-expanded', open);
  }));

  /* --- Mission / vision words --- */
  const mvWords = [];
  $$('.mv-item p:not(.label)').forEach(p => {
    const words = p.textContent.trim().split(/\s+/);
    p.setAttribute('aria-label', p.textContent.trim());
    p.innerHTML = words.map(w => `<span class="mw" aria-hidden="true">${w}</span>`).join(' ');
    mvWords.push({ el: p, words: [...p.querySelectorAll('.mw')] });
  });

  /* --- Scroll-linked effects (one rAF-throttled handler) --- */
  const steps = $('#steps'), stepItems = $$('.step', steps || document.createElement('div'));
  const hero = $('.hero'), root = document.documentElement, toTop = $('#toTop');
  const clamp = (v) => Math.min(1, Math.max(0, v));
  let ticking = false;
  const frame = () => {
    ticking = false;
    const vh = innerHeight, y = scrollY, max = root.scrollHeight - vh;
    root.style.setProperty('--sp', max > 0 ? (y / max).toFixed(4) : 0);
    if (toTop) toTop.classList.toggle('show', y > vh * 1.2);
    if (reduce) return;
    if (hero) hero.style.setProperty('--hp', clamp(y / hero.offsetHeight).toFixed(3));
    if (steps) {
      const r = steps.getBoundingClientRect();
      const p = clamp((vh * 0.82 - r.top) / (r.height + vh * 0.35));
      steps.style.setProperty('--p', (p * 100).toFixed(1) + '%');
      stepItems.forEach((s, i) => s.classList.toggle('lit', p >= i / stepItems.length + 0.02 || p > 0.97));
    }
    mvWords.forEach(({ el, words }) => {
      const b = el.getBoundingClientRect();
      const q = clamp((vh * 0.88 - b.top) / (b.height + vh * 0.3));
      const n = Math.round(q * words.length * 1.15);
      words.forEach((w, i) => w.classList.toggle('on', i < n));
    });
  };
  const onScrollFx = () => { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
  addEventListener('scroll', onScrollFx, { passive: true });
  addEventListener('resize', onScrollFx, { passive: true });
  frame();
  if (reduce && steps) { stepItems.forEach(s => s.classList.add('lit')); steps.style.setProperty('--p', '100%'); }
  if (toTop) toTop.addEventListener('click', () => { scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); $('.logo')?.focus({ preventScroll: true }); });

  /* --- Team bio dialog (data-driven from markup data-* attributes) --- */
  const dlg = $('#bio');
  if (dlg) {
    $$('.member').forEach(b => {
      b.addEventListener('click', () => {
        const d = b.dataset;
        $('#bioImg').src = d.img; $('#bioImg').alt = 'Portrait of ' + d.name;
        $('#bioName').textContent = d.name; $('#bioRole').textContent = d.role;
        $('#bioText').textContent = d.bio; $('#bioQual').textContent = d.qual;
        dlg.showModal();
      });
    });
    $('#bioClose')?.addEventListener('click', () => dlg.close());
    dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
  }

  /* --- Contact form ---
     Submits to Web3Forms (https://web3forms.com) when an access key is
     configured in data-access-key on the <form>. Web3Forms is free, has
     no server to run, and delivers straight to the inbox below.
     Until a key is set, or if the request fails (offline, blocked, etc.),
     the form falls back to opening the visitor's email client with the
     message pre-filled, so an enquiry is never silently lost.
     See README.md -> "Making the contact form work" for setup. */
  const form = $('#contactForm');
  if (form) {
    const okMsg = $('#formOk'), errMsg = $('#formError'), submitBtn = $('button[type="submit"]', form);
    const accessKey = form.dataset.accessKey || '';
    const mailTo = form.dataset.mailto || 'info@blueharboradvisory.com';

    const buildMailtoHref = (data) => {
      const subject = `New mandate enquiry — ${data.type || 'General'} — ${data.service || 'Not specified'}`;
      const body = [
        `Name: ${data.name || ''}`,
        `Organisation: ${data.organisation || ''}`,
        `Email: ${data.email || ''}`,
        `Phone: ${data.phone || ''}`,
        `Reaching out as: ${data.type || ''}`,
        `Area of interest: ${data.service || ''}`,
        '',
        data.message || ''
      ].join('\n');
      return `mailto:${mailTo}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    };

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (errMsg) errMsg.style.display = 'none';
      let ok = true;
      $$('[required]', form).forEach(el => {
        const valid = el.type === 'email' ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim()) : el.value.trim().length > 1;
        el.closest('.field').classList.toggle('invalid', !valid); if (!valid) ok = false;
      });
      if (!ok) { $('.field.invalid input, .field.invalid textarea', form)?.focus(); return; }

      const fd = new FormData(form);
      const data = Object.fromEntries(fd.entries());

      const showSuccess = () => {
        if (okMsg) okMsg.style.display = 'block';
        form.reset();
        $$('.field.invalid', form).forEach(f => f.classList.remove('invalid'));
      };

      if (!accessKey || accessKey === 'YOUR_WEB3FORMS_ACCESS_KEY') {
        // No email-delivery key configured yet — open a pre-filled email instead.
        window.location.href = buildMailtoHref(data);
        showSuccess();
        return;
      }

      try {
        if (submitBtn) submitBtn.disabled = true;
        fd.append('access_key', accessKey);
        fd.append('subject', `New mandate enquiry — ${data.type || 'General'} — ${data.service || 'Not specified'}`);
        const res = await fetch('https://api.web3forms.com/submit', {
          method: 'POST',
          headers: { Accept: 'application/json' },
          body: fd
        });
        const json = await res.json();
        if (json.success) {
          showSuccess();
        } else {
          throw new Error(json.message || 'Submission failed');
        }
      } catch (err) {
        if (errMsg) { errMsg.textContent = 'Something went wrong sending that online. Opening an email instead…'; errMsg.style.display = 'block'; }
        window.location.href = buildMailtoHref(data);
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }

  /* --- Lazy-load Google Map only when it nears the viewport --- */
  $$('iframe[data-src]').forEach(frame => {
    const mapIo = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.src = e.target.dataset.src; e.target.removeAttribute('data-src'); mapIo.unobserve(e.target); }
    }), { rootMargin: '200px' });
    mapIo.observe(frame);
  });

  const yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();
})();
