#!/usr/bin/env python3
"""
Builds a single self-contained HTML file so the BlueHarbor Advisory home
page can be opened and clicked through live inside an Artifact preview.

This is a DEMO build only — not part of the deployed site. It reuses the
exact same section markup/content as the real build (tools/build.py), but:
  - inlines css/styles.css and js/main.js so nothing depends on external paths
  - inlines team photos as base64 data URIs (artifacts can't fetch /assets/*)
  - swaps the live Google Maps iframe (blocked inside an artifact sandbox)
    for a static map-style placeholder card
  - the contact form validates and shows success locally instead of
    calling the Web3Forms API (cross-origin fetches are blocked in preview)

Run: python3 tools/build_artifact_preview.py
Output: writes to the path given as sys.argv[1]
"""
import base64
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


def data_uri_for(path):
    with open(path, "rb") as f:
        b = f.read()
    return "data:image/jpeg;base64," + base64.b64encode(b).decode("ascii")


# --- Build body: reuse the exact same section renderers as the real site ---
sections = [
    B.hero_section(),
    B.about_who_we_support(),
    B.services_accordion(),
    B.approach_section(),
    B.markets_section(),
    B.why_section(),
    B.experience_section(),
    B.purpose_section(),
    B.team_section(),
]
body_main = "\n".join(sections)

# Inline team photos as base64 so they render inside the artifact sandbox
for m in B.C["team"]:
    local_path = os.path.join(ROOT, "assets", m["photo"].lstrip("/"))
    uri = data_uri_for(local_path)
    body_main = body_main.replace(f"/assets{m['photo']}", uri)

# --- Contact section: same copy, but a static map card + local-only form ---
phones = B.C["site"]["contact"]["phones"]
phones_html = " &nbsp;&middot;&nbsp; ".join(
    f'<a href="tel:{p.replace(" ", "")}">{p}</a>' for p in phones
)
services_opts = "".join(f"<option>{B.esc(s['title'])}</option>" for s in B.C["services"]) + "<option>Not sure yet</option>"

contact_preview = f"""<section class="section contact on-dark" id="contact">
  <div class="container contact-grid">
    <div>
      <span class="eyebrow reveal">Contact</span>
      <h2 class="h2 reveal" data-d="1" style="margin-top:20px">Let's discuss <span class="serif">your mandate.</span></h2>
      <p class="lead reveal" data-d="2" style="margin-top:20px">{B.esc(B.C['cta']['text'])}</p>
      <div class="contact-details">
        <div class="cd reveal" data-reveal="left"><span class="cd-icon">{B.ICON['mail']}</span><div><small>Email</small><a href="mailto:{B.C['site']['contact']['email']}">{B.C['site']['contact']['email']}</a></div></div>
        <div class="cd reveal" data-reveal="left" data-d="1"><span class="cd-icon">{B.ICON['phone']}</span><div><small>Phone</small>{phones_html}</div></div>
        <div class="cd reveal" data-reveal="left" data-d="2"><span class="cd-icon">{B.ICON['map-pin']}</span><div><small>Office</small><span>{B.esc(B.C['site']['contact']['location'])}</span></div></div>
      </div>
      <div class="map reveal">
        <div class="map-static" aria-label="Map showing BlueHarbor Advisory in {B.esc(B.C['site']['contact']['location'])}">
          <div class="map-static-grid"></div>
          <div class="map-static-pin">{B.ICON['map-pin']}</div>
          <span class="map-static-note">Live Google Map on the deployed site &middot; preview shown here</span>
        </div>
        <div class="map-bar"><span>{B.esc(B.C['site']['contact']['location'])}</span>
          <a class="link-arrow" href="{B.C['site']['contact']['directionsUrl']}" target="_blank" rel="noopener">Get directions {B.ICON['arrow-right']}</a></div>
      </div>
    </div>

    <form class="form reveal" data-reveal="right" id="contactForm" novalidate data-preview="true">
      <h3>Tell us about your requirement</h3>
      <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" autocomplete="name" required><span class="err">Please enter your name.</span></div>
      <div class="field"><label for="f-org">Organisation</label><input id="f-org" name="organisation" autocomplete="organization"></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required><span class="err">Please enter a valid email.</span></div>
      <div class="field"><label for="f-phone">Phone <span class="muted" style="font-weight:400">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      <fieldset class="field full" style="border:0;padding:0;margin:0">
        <legend style="font-size:13.5px;font-weight:600;color:var(--navy);margin-bottom:7px">I am reaching out as</legend>
        <div class="seg">
          <input type="radio" name="type" id="r1" value="Enterprise" checked><label for="r1">An enterprise</label>
          <input type="radio" name="type" id="r2" value="Investor"><label for="r2">An investor</label>
          <input type="radio" name="type" id="r3" value="Institution"><label for="r3">An institution / programme</label>
        </div>
      </fieldset>
      <div class="field full"><label for="f-svc">Area of interest</label>
        <select id="f-svc" name="service">{services_opts}</select></div>
      <div class="field full"><label for="f-msg">Briefly describe your mandate</label><textarea id="f-msg" name="message" required placeholder="Objectives, sector, stage of growth, financing needs, timing&hellip;"></textarea><span class="err">Please add a short description.</span></div>
      <div class="form-foot">
        <small>Preview only &mdash; on the live site this delivers to the firm's inbox (see README).</small>
        <button class="btn btn-primary" type="submit">Send enquiry {B.ICON['arrow-right']}</button>
      </div>
      <p class="form-success" id="formOk" role="status">Thank you &mdash; your enquiry has been received. A member of the BlueHarbor team will be in touch.</p>
    </form>
  </div>
</section>"""

body_main += "\n" + contact_preview

# --- Footer (page links become in-page anchors in this single-file preview) ---
footer_html = f"""<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="#top" class="logo" aria-label="BlueHarbor Advisory">
          {B.LOGO_MARK_SVG}
          <span class="logo-word"><b>BLUEHARBOR</b><span>ADVISORY</span></span>
        </a>
        <p class="tagline">{B.esc(B.C['site']['tagline'])}</p>
        <p>Investment advisory &amp; corporate finance &mdash; Kampala, Uganda.</p>
      </div>
      <div><h4>Services</h4><ul>
        <li><a href="#services">Corporate Finance &amp; Enterprise</a></li>
        <li><a href="#services">Investment &amp; Transaction</a></li>
        <li><a href="#services">Development Finance &amp; Programmes</a></li>
      </ul></div>
      <div><h4>Firm</h4><ul>
        <li><a href="#about">About</a></li>
        <li><a href="#approach">Approach</a></li>
        <li><a href="#experience">Experience</a></li>
        <li><a href="#team">Team</a></li>
      </ul></div>
      <div><h4>Contact</h4><ul>
        <li><a href="mailto:{B.C['site']['contact']['email']}">{B.C['site']['contact']['email']}</a></li>
        {''.join(f'<li><a href="tel:{p.replace(" ", "")}">{p}</a></li>' for p in phones)}
        <li>{B.esc(B.C['site']['contact']['location'])}</li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span id="yr"></span> {B.esc(B.C['site']['name'])}. BlueHarbor provides advisory and analytical services within the applicable regulatory and professional framework. Nothing on this website constitutes an offer of securities or investment advice to any person.</p>
      <p>This is a live, in-chat preview of the real site &mdash; see the repository for the full multi-page build.</p>
    </div>
  </div>
</footer>"""

# --- Nav (home-style, anchor links — identical to the real home page) ---
nav_items = [("About", "#about"), ("Services", "#services"), ("Approach", "#approach"),
             ("Experience", "#experience"), ("Team", "#team")]
nav_links = "\n        ".join(f'<li><a href="{href}">{label}</a></li>' for label, href in nav_items)
mobile_links = "".join(f'<a href="{href}">{label}</a>' for label, href in nav_items)

nav_html = f"""<header class="nav" id="nav" data-solid="false">
  <div class="container nav-inner">
    <a href="#top" class="logo" aria-label="BlueHarbor Advisory — home">
      {B.LOGO_MARK_SVG}
      <span class="logo-word"><b>BLUEHARBOR</b><span>ADVISORY</span></span>
    </a>
    <nav aria-label="Primary">
      <ul class="nav-links">
        {nav_links}
      </ul>
    </nav>
    <a href="#contact" class="btn btn-primary nav-cta">Discuss a mandate</a>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="mobileMenu" aria-label="Open menu">
      {B.ICON['menu']}
    </button>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    {mobile_links}
    <a href="#contact" class="btn btn-primary">Discuss a mandate</a>
  </div>
</header>"""

extra_css = """
/* ---- preview-only additions (not in the deployed site) ---- */
.preview-banner{position:fixed;top:0;left:0;right:0;z-index:90;background:var(--navy-950);color:var(--slate-300);font-size:12.5px;line-height:1.5;text-align:center;padding:8px max(16px,env(safe-area-inset-left,0px)) 8px max(16px,env(safe-area-inset-right,0px));border-bottom:1px solid var(--line-dark)}
.preview-banner strong{color:var(--teal-300)}
#nav.nav{top:var(--pb-h,40px)}
@media (max-width:980px){.mobile-menu{top:calc(76px + var(--pb-h,40px))}}
.map-static{position:relative;height:260px;overflow:hidden;background:
  linear-gradient(rgba(79,194,192,.10),rgba(79,194,192,.10)),
  repeating-linear-gradient(0deg,rgba(255,255,255,.05) 0 1px,transparent 1px 34px),
  repeating-linear-gradient(90deg,rgba(255,255,255,.05) 0 1px,transparent 1px 34px),
  var(--navy-900)}
.map-static-pin{position:absolute;left:50%;top:48%;transform:translate(-50%,-100%);width:40px;height:40px;color:var(--teal-300);filter:drop-shadow(0 6px 14px rgba(0,0,0,.4))}
.map-static-note{position:absolute;left:16px;bottom:14px;font-size:12px;color:var(--slate-300);background:rgba(11,28,43,.6);padding:6px 10px;border-radius:999px;border:1px solid var(--line-dark)}
@media (max-width:560px){.map-static{height:220px}}
"""

extra_js = """
/* ---- preview-only: size the nav offset to the banner's real height ---- */
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
  const $ = (s) => form.querySelector(s);
  const $$ = (s) => [...form.querySelectorAll(s)];
  const okMsg = document.getElementById('formOk');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    let ok = true;
    $$('[required]').forEach(el => {
      const valid = el.type === 'email' ? /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(el.value.trim()) : el.value.trim().length > 1;
      el.closest('.field').classList.toggle('invalid', !valid); if (!valid) ok = false;
    });
    if (!ok) { form.querySelector('.field.invalid input, .field.invalid textarea')?.focus(); return; }
    okMsg.style.display = 'block';
    form.reset();
    $$('.field.invalid').forEach(f => f.classList.remove('invalid'));
  });
})();
"""

PAGE = f"""<meta name="claude:viewport-fit-sides" content="cover">
<title>BlueHarbor Advisory Preview</title>
<style>
{CSS}
{extra_css}
</style>

<div class="preview-banner">You're viewing a live, in-chat preview of the BlueHarbor Advisory home page &mdash; click the nav, open a team profile, expand a service. <strong>The real multi-page site lives in the repository.</strong></div>

<a href="#main" class="skip">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"></div>
<button class="to-top" id="toTop" aria-label="Back to top">{B.ICON['arrow-up']}</button>

{nav_html}

<main id="main">
{body_main}
</main>

{footer_html}

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
