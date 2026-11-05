#!/usr/bin/env python3
"""
Builds a single self-contained HTML file so the BlueHarbor Advisory home
page (BlueHarbor Advisory Design System build) can be opened and clicked
through live inside an Artifact preview.

This is a DEMO build only — not part of the deployed site. It reuses the
exact same section markup/content as the real build (tools/build.py), but:
  - inlines css/styles.css and js/main.js so nothing depends on external paths
  - swaps the live Google Maps iframe (blocked inside an artifact sandbox)
    for a static map-style placeholder card
  - the contact form validates and shows success locally instead of
    calling the Web3Forms API (cross-origin fetches are blocked in preview)

Logos and all 32 icons are already embedded as data: URIs by the real
build (see tools/build.py / css/styles.css), so — unlike the old prototype
— nothing else needs inlining here.

Run: python3 tools/build_artifact_preview.py
Output: writes to the path given as sys.argv[1]
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build as B  # noqa: E402

OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "artifact-preview.html")

with open(os.path.join(ROOT, "css", "styles.css"), encoding="utf-8") as f:
    CSS = f.read()

with open(os.path.join(ROOT, "js", "main.js"), encoding="utf-8") as f:
    JS = f.read()

# --- Build body from the exact same section renderers as the real site ---
sections = [
    B.hero_section(),
    B.who_we_support_section(),
    B.market_orientation_section(),
    B.purpose_section(),
    B.services_section(),
    B.approach_section(),
    B.experience_section(),
    B.why_section(),
]
body_main = "\n".join(sections)

# --- Contact: same CTA band, but a static map card + a locally-validated form ---
phones = B.C["site"]["contact"]["phones"]
phones_line = " &middot; ".join(phones)
services_opts = "".join(f"<option>{B.esc(s['title'])}</option>" for s in B.C["services"]) + "<option>Not sure yet</option>"

cta = f"""<section class="bh-cta" id="contact"><div class="bh-container"><div class="bh-cta__card bh-on-inverse">
<div class="bh-cta__copy"><span class="bh-tag bh-tag--inverse bh-tag--dot">Contact</span><h2 class="display-lg">Let's discuss your <span class="bh-em">mandate</span></h2><p class="body-lg">{B.esc(B.C['cta']['text'])}</p>
<div class="bh-cta__actions"><a class="bh-btn bh-btn--inverse bh-btn--chip bh-btn--lg" href="#contact-form">Discuss your mandate<span class="bh-btn__chip">{B.icon('arrow-right')}</span></a><a class="bh-btn bh-btn--inverse-outline bh-btn--lg" href="mailto:{B.C['site']['contact']['email']}">{B.icon('mail')}Email the team</a></div></div>
<div class="bh-cta__details">
<a class="bh-cta__item" href="mailto:{B.C['site']['contact']['email']}"><span class="bh-tile bh-tile--inverse">{B.icon('mail')}</span><span><small>Email</small><span>{B.esc(B.C['site']['contact']['email'])}</span></span></a>
<a class="bh-cta__item" href="tel:{phones[0].replace(' ', '')}"><span class="bh-tile bh-tile--inverse">{B.icon('phone')}</span><span><small>Phone</small><span>{B.esc(phones_line)}</span></span></a>
<div class="bh-cta__item"><span class="bh-tile bh-tile--inverse">{B.icon('map-pin')}</span><span><small>Location</small><span>{B.esc(B.C['site']['contact']['location'])}</span></span></div>
</div>
</div></div></section>"""

form_section = f"""<section class="bh-pv" id="contact-form" style="padding-block:var(--space-9)"><div class="bh-container" style="display:grid;gap:var(--space-7);max-width:var(--container-narrow);margin-inline:auto">
<div class="bh-formcard" style="max-width:none">
<form class="bh-form" id="contactForm" novalidate data-preview="true">
<h3 class="h3">Tell us about your requirement</h3>
<div class="bh-form__row">
<div class="bh-field"><label for="f-name">Full name</label><div class="bh-input">{B.icon('users')}<input id="f-name" name="name" autocomplete="name" required></div><span class="small bh-field__error" hidden>{B.icon('close')}Please enter your name.</span></div>
<div class="bh-field"><label for="f-org">Organisation</label><div class="bh-input">{B.icon('building')}<input id="f-org" name="organisation" autocomplete="organization"></div></div>
</div>
<div class="bh-form__row">
<div class="bh-field"><label for="f-email">Work email</label><div class="bh-input">{B.icon('mail')}<input id="f-email" name="email" type="email" autocomplete="email" required></div><span class="small bh-field__error" hidden>{B.icon('close')}Enter a full email address, for example name@company.com.</span></div>
<div class="bh-field"><label for="f-phone">Phone <span class="bh-muted" style="font-weight:400">(optional)</span></label><div class="bh-input">{B.icon('phone')}<input id="f-phone" name="phone" type="tel" autocomplete="tel"></div></div>
</div>
<fieldset class="bh-field"><legend>I am a</legend><div class="bh-seg">
<label><input type="radio" name="type" id="r1" value="Enterprise" checked><span>{B.icon('building')}Enterprise</span></label>
<label><input type="radio" name="type" id="r2" value="Investor"><span>{B.icon('trending-up')}Investor</span></label>
<label><input type="radio" name="type" id="r3" value="Institution"><span>{B.icon('landmark')}Institution</span></label>
</div></fieldset>
<div class="bh-field"><label for="f-svc">Area of interest</label><select id="f-svc" name="service">{services_opts}</select></div>
<div class="bh-field"><label for="f-msg">Message</label><textarea id="f-msg" name="message" required placeholder="Your mandate, sector, stage of growth and timing" aria-describedby="m-h"></textarea><span id="m-h" class="caption bh-field__hint">Tell us about your mandate, sector and timing.</span><span class="small bh-field__error" hidden>{B.icon('close')}Please add a short description.</span></div>
<p class="bh-form-banner bh-form-banner--ok" id="formOk" role="status">Thank you &mdash; your enquiry has been received. A member of the BlueHarbor team will be in touch.</p>
<div class="bh-form__foot"><span class="caption bh-form__note">{B.icon('shield-check')}Enquiries are treated as confidential. (Preview only &mdash; see the deployed site for real delivery.)</span><button class="bh-btn bh-btn--accent" type="submit">Send enquiry{B.icon('send')}</button></div>
</form>
</div>
<div class="bh-map">
  <div class="bh-map-static">
    <span class="bh-map-pin">{B.icon('map-pin', size='lg')}</span>
    <span class="bh-map-note">Live Google Map on the deployed site &middot; preview shown here</span>
  </div>
  <div class="bh-map-bar"><span class="small">{B.esc(B.C['site']['contact']['location'])}</span><a class="bh-arrowlink" href="{B.C['site']['contact']['directionsUrl']}" target="_blank" rel="noopener">Get directions{B.icon('arrow-right')}</a></div>
</div>
</div></section>"""

body_main += "\n" + cta + "\n" + form_section

extra_css = """
/* ---- preview-only additions (not in the deployed site) ---- */
.preview-banner{position:fixed;top:0;left:0;right:0;z-index:90;background:var(--surface-inverse);color:var(--ink-inverse-muted);font-size:12.5px;line-height:1.5;text-align:center;padding:8px max(16px,env(safe-area-inset-left,0px)) 8px max(16px,env(safe-area-inset-right,0px));border-bottom:1px solid var(--inverse-line)}
.preview-banner strong{color:var(--accent-on-inverse)}
.bh-topbar{top:var(--pb-h,34px);position:relative}
#nav.bh-nav{top:var(--pb-h,34px)}
@container (max-width:1000px){.bh-mobile-menu{top:calc(var(--pb-h,34px) + var(--nav-height))}}
"""

extra_js = """
/* ---- preview-only: size the header offset to the banner's real height ---- */
(() => {
  const banner = document.querySelector('.preview-banner');
  if (!banner) return;
  const sync = () => document.documentElement.style.setProperty('--pb-h', banner.offsetHeight + 'px');
  sync();
  addEventListener('resize', sync);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(sync);
})();

/* ---- preview-only contact form: validate, then show success locally ---- */
(() => {
  const form = document.getElementById('contactForm');
  if (!form || form.dataset.preview !== 'true') return;
  const okMsg = document.getElementById('formOk');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    let ok = true;
    [...form.querySelectorAll('[required]')].forEach(el => {
      const valid = el.type === 'email' ? /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(el.value.trim()) : el.value.trim().length > 1;
      const field = el.closest('.bh-field');
      field.classList.toggle('bh-field--error', !valid);
      const err = field.querySelector('.bh-field__error');
      if (err) err.hidden = valid;
      if (!valid) ok = false;
    });
    if (!ok) { form.querySelector('.bh-field--error input, .bh-field--error textarea')?.focus(); return; }
    okMsg.style.display = 'block';
    form.reset();
    [...form.querySelectorAll('.bh-field--error')].forEach(f => { f.classList.remove('bh-field--error'); const err = f.querySelector('.bh-field__error'); if (err) err.hidden = true; });
  });
})();
"""

nav_html = B.header_html("/", True)
footer_html = B.footer_html(True)

PAGE = f"""<meta name="claude:viewport-fit-sides" content="cover">
<title>BlueHarbor Advisory Preview</title>
{B.FONTS_LINK}
<style>
{CSS}
{extra_css}
</style>

<div class="preview-banner">You're viewing a live, in-chat preview of the BlueHarbor Advisory home page &mdash; click the nav, expand a service, try the form. <strong>The real multi-page site lives in the repository.</strong></div>

<div class="bh-root">
<a href="#main" class="skip">Skip to content</a>
{nav_html}
<main id="main">
{body_main}
</main>
{footer_html}
</div>

<script>
{JS}
</script>
<script>
{extra_js}
</script>
"""

os.makedirs(os.path.dirname(OUT_PATH) or ".", exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(PAGE)
print("wrote", OUT_PATH, "-", len(PAGE), "bytes")
