/* =========================================================
   BlueHarbor Advisory — shared site behaviour
   Built for the BlueHarbor Advisory Design System, whose motion
   guidance is "200–300ms transitions on hover and focus only...
   nothing moves on scroll or by itself" — so unlike the previous
   build, there is no scroll-driven reveal/parallax JS here at all.
   What's left: the mobile nav menu, the nav active-link spy on the
   home page, the contact form, and lazy-loading the map iframe.
   ========================================================= */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  /* --- Mobile menu --- */
  const menuBtn = $('#menuBtn'), menu = $('#mobileMenu');
  if (menuBtn && menu) {
    menuBtn.addEventListener('click', () => {
      const open = menu.classList.toggle('is-open');
      document.body.classList.toggle('bh-menu-open', open);
      menuBtn.setAttribute('aria-expanded', open);
      menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      menuBtn.querySelector('.bh-i').classList.toggle('bh-i--close', open);
      menuBtn.querySelector('.bh-i').classList.toggle('bh-i--menu', !open);
    });
    $$('#mobileMenu a').forEach(a => a.addEventListener('click', () => {
      if (menu.classList.contains('is-open')) menuBtn.click();
    }));
    matchMedia('(min-width: 1000px)').addEventListener('change', e => {
      if (e.matches && menu.classList.contains('is-open')) menuBtn.click();
    });
  }

  /* --- Active nav link on the home page (in-view section spy) --- */
  const navLinks = $$('.bh-nav__links a, .bh-mobile-menu a');
  const sectionIds = ['about', 'services', 'approach', 'experience', 'contact'];
  const sectionsPresent = sectionIds.filter(id => document.getElementById(id));
  if (sectionsPresent.length && navLinks.length) {
    const spy = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) navLinks.forEach(l => {
        const match = l.getAttribute('href') === '#' + e.target.id;
        if (match) l.setAttribute('aria-current', 'page'); else l.removeAttribute('aria-current');
      });
    }), { rootMargin: '-45% 0px -50% 0px' });
    sectionsPresent.forEach(id => spy.observe(document.getElementById(id)));
  }

  /* --- Lazy-load the Google Map only when it nears the viewport --- */
  $$('iframe[data-src]').forEach(frame => {
    const mapIo = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.src = e.target.dataset.src; e.target.removeAttribute('data-src'); mapIo.unobserve(e.target); }
    }), { rootMargin: '200px' });
    mapIo.observe(frame);
  });

  /* --- Contact form ---
     Submits to Web3Forms (https://web3forms.com) when an access key is
     configured in data-access-key on the <form>. Web3Forms is free, has
     no server to run, and delivers straight to the inbox below.
     Until a key is set, or if the request fails, the form falls back to
     opening the visitor's email client with the message pre-filled, so
     an enquiry is never silently lost. See README.md -> "Making the
     contact form work" for setup. */
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
        const field = el.closest('.bh-field');
        field.classList.toggle('bh-field--error', !valid);
        const err = field.querySelector('.bh-field__error');
        if (err) err.hidden = valid;
        if (!valid) ok = false;
      });
      if (!ok) { $('.bh-field--error input, .bh-field--error textarea', form)?.focus(); return; }

      const fd = new FormData(form);
      const data = Object.fromEntries(fd.entries());

      const showSuccess = () => {
        if (okMsg) okMsg.style.display = 'block';
        form.reset();
        $$('.bh-field--error', form).forEach(f => { f.classList.remove('bh-field--error'); const err = f.querySelector('.bh-field__error'); if (err) err.hidden = true; });
      };

      if (!accessKey || accessKey === 'YOUR_WEB3FORMS_ACCESS_KEY') {
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

  const yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();
})();
