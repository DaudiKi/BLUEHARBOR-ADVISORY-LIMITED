#!/usr/bin/env python3
"""
Static-site generator for the BlueHarbor Advisory Limited website.

Reads copy from content/site-content.json (the single source of truth —
do not hand-edit the generated *.html files, edit this builder or the
JSON and re-run `python3 tools/build.py`) and emits a complete, dependency
-free static website at the repository root: one HTML file per route,
sharing css/styles.css and js/main.js.

Usage:
    python3 tools/build.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_PATH = os.path.join(ROOT, "content", "site-content.json")

with open(CONTENT_PATH, encoding="utf-8") as f:
    C = json.load(f)

DOMAIN = "https://" + C["site"]["domain"]
FONTS_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Newsreader:'
    'ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,500&display=swap" rel="stylesheet">'
)

NAV_ITEMS_HOME = [
    ("About", "#about"), ("Services", "#services"), ("Approach", "#approach"),
    ("Experience", "#experience"), ("Team", "#team"),
]
NAV_ITEMS_INNER = [
    ("About", "/about.html"), ("Services", "/services.html"), ("Approach", "/services.html#approach"),
    ("Experience", "/experience.html"), ("Team", "/team.html"),
]

LOGO_MARK_SVG = (
    '<svg class="logo-mark" viewBox="0 0 36 36" aria-hidden="true">'
    '<rect width="36" height="36" rx="9" style="fill:var(--teal)"/>'
    '<path d="M7 22.5c3.2-2.6 6.6-2.6 9.8 0s6.6 2.6 9.8 0" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
    '<path d="M7 27.5c3.2-2.6 6.6-2.6 9.8 0s6.6 2.6 9.8 0" stroke="#fff" stroke-opacity=".55" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
    '<path d="M18 7v11M18 7l5 7h-5" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    '</svg>'
)

ICON = {
    "arrow-right": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "plus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "map-pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "map-pin-thin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.01"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9S14.5 18.4 12 21M12 3C9.5 5.6 8.2 8.6 8.2 12s1.3 6.4 3.8 9"/></svg>',
    "sectors": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V10l5 3V10l5 3V6l4 2v13"/></svg>',
    "mandate": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 4h6l1 3H8l1-3zM6 7h12v13H6z"/><path d="M9 12h6M9 16h4"/></svg>',
    "excellence": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19V5M4 19h16M8 15l4-4 3 3 5-6"/></svg>',
    "integrity": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v6c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/></svg>',
    "client-focus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h10"/></svg>',
    "arrow-up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M6 11l6-6 6 6"/></svg>',
}


def esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def head(title, description, path, extra_jsonld=None):
    canonical = DOMAIN + path
    og_image = DOMAIN + "/assets/brand/og-image.png"
    jsonld_blocks = [ORG_JSONLD]
    if extra_jsonld:
        jsonld_blocks.append(extra_jsonld)
    jsonld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in jsonld_blocks
    )
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="format-detection" content="telephone=no">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0B1C2B">
<link rel="icon" type="image/svg+xml" href="/assets/brand/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/brand/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(C['site']['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="en_UG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{og_image}">
{FONTS_LINK}
<link rel="stylesheet" href="/css/styles.css">
{jsonld}
<script>document.documentElement.classList.add('js-early')</script>"""


ORG_JSONLD = {
    "@context": "https://schema.org",
    "@type": "FinancialService",
    "name": C["site"]["name"],
    "alternateName": C["site"]["shortName"],
    "url": DOMAIN + "/",
    "logo": DOMAIN + "/assets/brand/logo-mark.svg",
    "image": DOMAIN + "/assets/brand/og-image.png",
    "description": C["site"]["description"],
    "email": C["site"]["contact"]["email"],
    "telephone": C["site"]["contact"]["phones"][0],
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Ntinda, Kampala",
        "addressCountry": "UG",
    },
    "areaServed": ["Uganda", "East Africa"],
}


def nav_html(active_path, home: bool):
    items = NAV_ITEMS_HOME if home else NAV_ITEMS_INNER
    links = "\n        ".join(
        f'<li><a href="{href}"{" class=\"active\"" if (not home and href == active_path) else ""}>{label}</a></li>'
        for label, href in items
    )
    mobile_links = "".join(f'<a href="{href}">{label}</a>' for label, href in items)
    home_href = "#top" if home else "/"
    solid = "false" if home else "true"
    return f"""<header class="nav" id="nav" data-solid="{solid}">
  <div class="container nav-inner">
    <a href="{home_href}" class="logo" aria-label="BlueHarbor Advisory — home">
      {LOGO_MARK_SVG}
      <span class="logo-word"><b>BLUEHARBOR</b><span>ADVISORY</span></span>
    </a>
    <nav aria-label="Primary">
      <ul class="nav-links">
        {links}
      </ul>
    </nav>
    <a href="{'#contact' if home else '/contact.html'}" class="btn btn-primary nav-cta">Discuss a mandate</a>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="mobileMenu" aria-label="Open menu">
      {ICON['menu']}
    </button>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    {mobile_links}
    <a href="{'#contact' if home else '/contact.html'}" class="btn btn-primary">Discuss a mandate</a>
  </div>
</header>"""


def footer_html():
    phones = C["site"]["contact"]["phones"]
    phones_html = "".join(f'<li><a href="tel:{p.replace(" ", "")}">{p}</a></li>' for p in phones)
    return f"""<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="/" class="logo" aria-label="BlueHarbor Advisory">
          {LOGO_MARK_SVG}
          <span class="logo-word"><b>BLUEHARBOR</b><span>ADVISORY</span></span>
        </a>
        <p class="tagline">{esc(C['site']['tagline'])}</p>
        <p>Investment advisory &amp; corporate finance — Kampala, Uganda.</p>
      </div>
      <div><h4>Services</h4><ul>
        <li><a href="/services/corporate-finance.html">Corporate Finance &amp; Enterprise</a></li>
        <li><a href="/services/transaction-advisory.html">Investment &amp; Transaction</a></li>
        <li><a href="/services/development-finance.html">Development Finance &amp; Programmes</a></li>
      </ul></div>
      <div><h4>Firm</h4><ul>
        <li><a href="/about.html">About</a></li>
        <li><a href="/services.html#approach">Approach</a></li>
        <li><a href="/experience.html">Experience</a></li>
        <li><a href="/team.html">Team</a></li>
      </ul></div>
      <div><h4>Contact</h4><ul>
        <li><a href="mailto:{C['site']['contact']['email']}">{C['site']['contact']['email']}</a></li>
        {phones_html}
        <li>{esc(C['site']['contact']['location'])}</li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <p>© <span id="yr"></span> {esc(C['site']['name'])}. BlueHarbor provides advisory and analytical services within the applicable regulatory and professional framework. Nothing on this website constitutes an offer of securities or investment advice to any person.</p>
      <p><a href="/privacy.html">Privacy notice</a> &nbsp;·&nbsp; <a href="/terms.html">Terms of use</a></p>
    </div>
  </div>
</footer>"""


def page(title, description, path, body, home=False, extra_jsonld=None, extra_body_attrs=""):
    active_path = "/" + path.lstrip("/") if path != "/" else "/"
    return f"""<!doctype html>
<html lang="en-UG">
<head>
{head(title, description, path, extra_jsonld)}
</head>
<body{extra_body_attrs}>
<a href="#main" class="skip">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"></div>
<button class="to-top" id="toTop" aria-label="Back to top">{ICON['arrow-up']}</button>

{nav_html(active_path, home)}

<main id="main">
{body}
</main>

{footer_html()}
<script src="/js/main.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Reusable section renderers
# ---------------------------------------------------------------------------

def section_head(eyebrow, h2_html, lead=None, extra_class=""):
    lead_html = f'<p class="lead reveal" data-d="2">{lead}</p>' if lead else ""
    h2 = f'<h2 class="h2 reveal" data-d="1">{h2_html}</h2>' if h2_html else ""
    return f"""<div class="section-head {extra_class}">
      <span class="eyebrow reveal">{esc(eyebrow)}</span>
      {h2}
      {lead_html}
    </div>"""


def about_who_we_support(id_attr="about", show_heading=True):
    a = C["about"]
    auds = C["audiences"]
    svc_by_pillar = {s["slug"]: s for s in C["services"]}
    tabs = []
    panels = []
    labels = {"enterprises": "t-ent", "investors": "t-inv", "institutions": "t-ins"}
    panel_ids = {"enterprises": "p-ent", "investors": "p-inv", "institutions": "p-ins"}
    for i, aud in enumerate(auds):
        tid, pid = labels[aud["id"]], panel_ids[aud["id"]]
        selected = "true" if i == 0 else "false"
        tabindex = "" if i == 0 else ' tabindex="-1"'
        tabs.append(f'<button class="aud-tab" role="tab" id="{tid}" aria-controls="{pid}" aria-selected="{selected}"{tabindex}>{aud["label"]}</button>')
        pillar = svc_by_pillar[aud["servicePillar"]]
        hidden = "" if i == 0 else " hidden"
        panels.append(f"""<div class="aud-panel" role="tabpanel" id="{pid}" aria-labelledby="{tid}"{hidden}>
        <p class="kicker">Who we support</p>
        <h3 class="h3">{esc(aud['text'].split('.')[0])}.</h3>
        <p>{esc(aud['text'])}</p>
        <div class="aud-match"><span class="num">{pillar['number']}</span><div><b>{esc(pillar['title'])}</b><span>{esc(', '.join(pillar['deliverables'][:4]))}.</span></div></div>
      </div>""")
    head_html = section_head('About BlueHarbor', 'Practical, locally grounded advice <span class="serif">for capital decisions.</span>') if show_heading else ""
    lead_html = f'<p class="lead reveal">{esc(a["summary"])}</p>' if show_heading else ""
    return f"""<section class="section" id="{id_attr}">
  <div class="container about-grid">
    <div class="about-copy">
      {head_html}
      {lead_html}
      <p class="muted reveal">{esc(a['detail'])}</p>
    </div>
    <div class="audience reveal" data-reveal="right" data-d="1">
      <div class="aud-tabs" role="tablist" aria-label="Who we support">
        {''.join(tabs)}
      </div>
      {''.join(panels)}
    </div>
  </div>
</section>"""


def services_accordion(id_attr="services", default_open=0, show_heading=True):
    s = C["services"]
    items = []
    for i, svc in enumerate(s):
        open_attr = "true" if i == default_open else "false"
        aria = "true" if i == default_open else "false"
        deliv = "".join(f"<li>{esc(d)}</li>" for d in svc["deliverables"])
        items.append(f"""<article class="svc reveal" data-open="{open_attr}">
        <button class="svc-head" aria-expanded="{aria}" aria-controls="svc{i+1}">
          <span class="svc-num">{svc['number']}</span><span class="svc-title">{esc(svc['title'])}</span>
          <span class="svc-toggle">{ICON['plus']}</span>
        </button>
        <div class="svc-body" id="svc{i+1}"><div><div class="svc-content">
          <p>{esc(svc['body'])}</p>
          <div class="deliv"><h4>Typical deliverables</h4><ul>{deliv}</ul></div>
        </div></div></div>
        <p style="padding:0 0 28px"><a class="link-arrow" href="/services/{svc['slug']}.html">Learn more about this service {ICON['arrow-right']}</a></p>
      </article>""")
    head_html = section_head('Our advisory services', 'Three pillars, <span class="serif">from preparation to execution.</span>', esc(C['servicesIntro'])) if show_heading else ""
    return f"""<section class="section services" id="{id_attr}">
  <div class="container">
    {head_html}
    <div class="svc-list">
      {''.join(items)}
    </div>
  </div>
</section>"""


def approach_section(id_attr="approach"):
    steps = C["approach"]["steps"]
    items = "".join(
        f'<li class="step"><span class="step-dot">{s["n"]}</span><div><h3>{esc(s["title"])}</h3><p>{esc(s["text"])}</p></div></li>'
        for s in steps
    )
    return f"""<section class="section approach on-dark" id="{id_attr}">
  <div class="container">
    {section_head('Our engagement approach', 'A clear course, <span class="serif">agreed from the outset.</span>')}
    <ol class="steps" id="steps">
      <li class="progress" aria-hidden="true"></li>
      {items}
    </ol>
    <div class="principle reveal">
      <span class="tag">{esc(C['headings']['operatingPrincipleLabel'])}</span>
      <p>{esc(C['approach']['operatingPrinciple'])}</p>
    </div>
  </div>
</section>"""


def markets_section(id_attr="markets"):
    mo = C["marketOrientation"]
    geo, sectors, mandate = mo[0], mo[1], mo[2]
    chips = "".join(f'<span class="chip">{esc(x)}</span>' for x in sectors["items"])
    return f"""<section class="section" id="{id_attr}">
  <div class="container">
    {section_head('Market orientation', 'Rooted in Uganda. <span class="serif">Regional in perspective.</span>')}
    <div class="markets-grid">
      <div class="mk reveal" data-reveal="scale">
        <span class="mk-icon">{ICON['globe']}</span>
        <h3>{esc(geo['label'])}</h3>
        <p>{esc(geo['text'])}</p>
      </div>
      <div class="mk reveal" data-reveal="scale" data-d="1">
        <span class="mk-icon">{ICON['sectors']}</span>
        <h3>{esc(sectors['label'])}</h3>
        <div class="chips">{chips}</div>
      </div>
      <div class="mk reveal" data-reveal="scale" data-d="2">
        <span class="mk-icon">{ICON['mandate']}</span>
        <h3>{esc(mandate['label'])}</h3>
        <p>{esc(mandate['text'])}</p>
      </div>
    </div>
  </div>
</section>"""


def why_section(id_attr="why"):
    items = C["why"]
    romans = ["i.", "ii.", "iii."]
    blocks = "".join(
        f'<div class="why-item reveal" data-d="{i}"><span class="idx">{romans[i]}</span><h3 class="h3">{esc(it["title"])}</h3><p>{esc(it["text"])}</p></div>'
        for i, it in enumerate(items)
    )
    return f"""<section class="section why" id="{id_attr}">
  <div class="container">
    {section_head('Why work with BlueHarbor', 'From analysis <span class="serif">to decisions.</span>')}
    <div class="why-grid">
      {blocks}
    </div>
  </div>
</section>"""


def experience_section(id_attr="experience"):
    exp = C["experience"]
    rows = "".join(f"""<div class="exp-row reveal"><div><h3>{esc(a['title'])}</h3><span class="exp-region">{ICON['map-pin-thin']}{esc(a['region'])}</span></div><p>{esc(a['text'])}</p></div>""" for a in exp["areas"])
    return f"""<section class="section" id="{id_attr}">
  <div class="container">
    {section_head('Experience & capabilities', 'Relevant professional <span class="serif">experience.</span>', esc(exp['intro']))}
    <p class="disclaimer reveal" style="margin:0 0 28px">{ICON['info']}{esc(exp['disclaimer'])}</p>
    <div class="exp-table">
      {rows}
    </div>
  </div>
</section>"""


def purpose_section(id_attr="purpose"):
    p = C["purpose"]
    icons = ["excellence", "integrity", "client-focus"]
    values = "".join(f"""<div class="value reveal" data-reveal="right" data-d="{i}"><span class="value-icon">{ICON[icons[i]]}</span><div><h3>{esc(v['name'])}</h3><p>{esc(v['text'])}</p></div></div>""" for i, v in enumerate(p["values"]))
    return f"""<section class="section purpose on-dark" id="{id_attr}">
  <div class="container">
    {section_head('Purpose & principles', '')}
    <div class="purpose-grid">
      <div class="mv">
        <div class="mv-item reveal" data-reveal="left"><p class="label">Mission</p><p>{esc(p['mission'])}</p></div>
        <div class="mv-item reveal" data-reveal="left" data-d="1"><p class="label">Vision</p><p>{esc(p['vision'])}</p></div>
      </div>
      <div class="values">
        {values}
      </div>
    </div>
  </div>
</section>"""


def team_section(id_attr="team", show_heading=True):
    members = []
    for i, m in enumerate(C["team"]):
        bio = esc(m["bio"]).replace('"', "&quot;")
        qual = esc(m["qualifications"]).replace('"', "&quot;")
        name = esc(m["name"]).replace('"', "&quot;")
        role = esc(m["role"]).replace('"', "&quot;")
        members.append(f"""<button type="button" class="member reveal" data-d="{i % 4}" aria-haspopup="dialog"
        data-img="/assets{m['photo']}" data-name="{name}" data-role="{role}" data-bio="{bio}" data-qual="{qual}">
        <div class="member-photo"><img src="/assets{m['photo']}" alt="Portrait of {esc(m['name'])}" loading="lazy" width="640" height="800"></div>
        <div class="member-info"><span class="member-role">{esc(m['role'])}</span><h3>{esc(m['name'])}</h3>
        <span class="member-more">Read profile {ICON['arrow-right']}</span></div>
      </button>""")
    head_html = section_head('Our team', 'A multidisciplinary <span class="serif">advisory team.</span>', esc(C['teamIntro'])) if show_heading else ""
    return f"""<section class="section" id="{id_attr}">
  <div class="container">
    {head_html}
    <div class="team-grid" id="teamGrid">
      {''.join(members)}
    </div>
  </div>
</section>

<dialog class="bio" id="bio" aria-labelledby="bioName">
  <button class="bio-close" id="bioClose" aria-label="Close">{ICON['close']}</button>
  <div class="bio-grid">
    <img id="bioImg" alt="">
    <div class="bio-body">
      <span class="member-role" id="bioRole"></span>
      <h3 id="bioName"></h3>
      <p id="bioText"></p>
      <div class="bio-qual"><b>Qualifications</b><span id="bioQual"></span></div>
    </div>
  </div>
</dialog>"""


def map_embed(compact=False):
    q = C["site"]["contact"]["mapQuery"].replace(" ", "+")
    src = f"https://www.google.com/maps?q={q}&z=15&output=embed"
    return f"""<div class="map reveal">
        <iframe title="Map showing BlueHarbor Advisory in {esc(C['site']['contact']['location'])}"
          data-src="{src}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        <div class="map-bar"><span>{esc(C['site']['contact']['location'])}</span>
          <a class="link-arrow" href="{C['site']['contact']['directionsUrl']}" target="_blank" rel="noopener">Get directions {ICON['arrow-right']}</a></div>
      </div>"""


def contact_section(id_attr="contact", heading_tag="h2", crumbs_html="", show_heading=True):
    phones = C["site"]["contact"]["phones"]
    phones_html = " &nbsp;·&nbsp; ".join(f'<a href="tel:{p.replace(" ", "")}">{p}</a>' for p in phones)
    services_opts = "".join(f"<option>{esc(s['title'])}</option>" for s in C["services"]) + "<option>Not sure yet</option>"
    heading_html = f"""<span class="eyebrow reveal">Contact</span>
      <{heading_tag} class="h2 reveal" data-d="1" style="margin-top:20px">Let's discuss <span class="serif">your mandate.</span></{heading_tag}>
      <p class="lead reveal" data-d="2" style="margin-top:20px">{esc(C['cta']['text'])}</p>""" if show_heading else ""
    return f"""<section class="section contact on-dark" id="{id_attr}">
  <div class="container contact-grid">
    <div>
      {crumbs_html}
      {heading_html}
      <div class="contact-details">
        <div class="cd reveal" data-reveal="left"><span class="cd-icon">{ICON['mail']}</span><div><small>Email</small><a href="mailto:{C['site']['contact']['email']}">{C['site']['contact']['email']}</a></div></div>
        <div class="cd reveal" data-reveal="left" data-d="1"><span class="cd-icon">{ICON['phone']}</span><div><small>Phone</small>{phones_html}</div></div>
        <div class="cd reveal" data-reveal="left" data-d="2"><span class="cd-icon">{ICON['map-pin']}</span><div><small>Office</small><span>{esc(C['site']['contact']['location'])}</span></div></div>
      </div>
      {map_embed()}
    </div>

    <form class="form reveal" data-reveal="right" id="contactForm" novalidate
      data-access-key="YOUR_WEB3FORMS_ACCESS_KEY" data-mailto="{C['site']['contact']['email']}">
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
      <div class="field full"><label for="f-msg">Briefly describe your mandate</label><textarea id="f-msg" name="message" required placeholder="Objectives, sector, stage of growth, financing needs, timing…"></textarea><span class="err">Please add a short description.</span></div>
      <div class="form-foot">
        <small>Information you share is treated confidentially and used only to respond to your enquiry.</small>
        <button class="btn btn-primary" type="submit">Send enquiry {ICON['arrow-right']}</button>
      </div>
      <p class="form-error" id="formError" role="alert"></p>
      <p class="form-success" id="formOk" role="status">Thank you — your enquiry has been received. A member of the BlueHarbor team will be in touch.</p>
    </form>
  </div>
</section>
<script>
(function(){{
  var p = new URLSearchParams(location.search).get('service');
  if(!p) return;
  var map = {{
    'corporate-finance': 'Corporate Finance & Enterprise Advisory',
    'transaction-advisory': 'Investment & Transaction Advisory',
    'development-finance': 'Development Finance & Programme Advisory'
  }};
  var want = map[p];
  if(!want) return;
  var sel = document.getElementById('f-svc');
  if(!sel) return;
  for (var i=0;i<sel.options.length;i++){{ if(sel.options[i].text.replace(/&amp;/g,'&') === want){{ sel.selectedIndex = i; break; }} }}
}})();
</script>"""


def cta_band(path=""):
    return f"""<section class="section-sm" style="background:var(--mist)">
  <div class="container" style="display:flex;flex-wrap:wrap;gap:24px;align-items:center;justify-content:space-between">
    <div>
      <h2 class="h3" style="margin-bottom:6px">{esc(C['cta']['title'])}</h2>
      <p class="muted">{esc(C['cta']['text'])}</p>
    </div>
    <a href="/contact.html{('?service=' + path) if path else ''}" class="btn btn-outline">Discuss a mandate {ICON['arrow-right']}</a>
  </div>
</section>"""


def crumbs(*pairs):
    parts = ['<a href="/">Home</a>']
    for label, href in pairs:
        parts.append('<span>/</span>')
        parts.append(f'<a href="{href}">{label}</a>' if href else f"<span>{esc(label)}</span>")
    return f'<div class="crumbs">{"".join(parts)}</div>'


def page_hero(eyebrow, h1, lead, crumbs_html=""):
    return f"""<section class="page-hero on-dark">
  <div class="container">
    {crumbs_html}
    <span class="eyebrow reveal">{esc(eyebrow)}</span>
    <h1 class="h2 reveal" data-d="1">{h1}</h1>
    <p class="lead reveal" data-d="2">{lead}</p>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# Home page (matches prototype section-for-section)
# ---------------------------------------------------------------------------

def hero_section():
    mo = C["marketOrientation"]
    with open(os.path.join(ROOT, "assets", "hero", "harbour-chart.svg"), encoding="utf-8") as f:
        chart_svg = f.read()
    # strip xml prolog / outer <svg> wrapper attrs we don't want duplicated; keep as-is, it's already a full <svg>
    return f"""<section class="hero on-dark" id="top">
  <div class="container hero-grid">
    <div class="hero-copy">
      <span class="eyebrow reveal">Investment advisory &amp; corporate finance · Kampala</span>
      <h1 class="reveal" data-d="1">Navigating growth.<br><span class="serif">Empowering success.</span></h1>
      <p class="lead reveal" data-d="2">{esc(C['site']['description'])}</p>
      <div class="hero-ctas reveal" data-d="3">
        <a href="#contact" class="btn btn-primary">Discuss your mandate {ICON['arrow-right']}</a>
        <a href="#services" class="btn btn-ghost">Explore our services</a>
      </div>
    </div>
    <div class="hero-art" aria-hidden="true">
      {chart_svg}
    </div>
  </div>
  <span class="coord">0°21′N · 32°37′E — NTINDA, KAMPALA</span>
  <div class="hero-bar">
    <dl class="container">
      <div class="hero-fact reveal"><dt>{esc(mo[0]['label'])}</dt><dd>{esc(mo[0]['text'])}</dd></div>
      <div class="hero-fact reveal" data-d="1"><dt>{esc(mo[1]['label'])}</dt><dd>{esc(', '.join(mo[1]['items']))}.</dd></div>
      <div class="hero-fact reveal" data-d="2"><dt>{esc(mo[2]['label'])}</dt><dd>{esc(mo[2]['text'])}</dd></div>
    </dl>
  </div>
</section>"""


def build_home():
    body = "\n".join([
        hero_section(),
        about_who_we_support(),
        services_accordion(),
        approach_section(),
        markets_section(),
        why_section(),
        experience_section(),
        purpose_section(),
        team_section(),
        contact_section(),
    ])
    desc = C["site"]["description"]
    return page(
        f"{C['site']['shortName']} — Investment Advisory & Corporate Finance, Kampala",
        desc, "/", body, home=True,
    )


def build_about():
    body = "\n".join([
        page_hero("About BlueHarbor", 'Practical, locally grounded <span class="serif">advice for capital decisions.</span>',
                  esc(C["about"]["summary"]), crumbs(("About", ""))),
        about_who_we_support(id_attr="who-we-support", show_heading=False),
        markets_section(),
        purpose_section(),
        why_section(),
        cta_band(),
    ])
    return page(
        "About BlueHarbor Advisory — Investment Advisory Firm in Kampala, Uganda",
        C["about"]["summary"], "/about.html", body,
    )


def build_services_overview():
    body = "\n".join([
        page_hero("Our advisory services", 'Three pillars, <span class="serif">from preparation to execution.</span>',
                  esc(C["servicesIntro"]), crumbs(("Services", ""))),
        services_accordion(id_attr="services-list", show_heading=False),
        approach_section(),
        cta_band(),
    ])
    return page(
        "Advisory Services — Corporate Finance, Transaction Advisory & Development Finance",
        C["servicesIntro"], "/services.html", body,
    )


def build_service_detail(svc, prev_svc, next_svc):
    deliv = "".join(f'<li>{ICON["arrow-right"]}{esc(d)}</li>' for d in svc["deliverables"])
    audience = next((a for a in C["audiences"] if a["servicePillar"] == svc["slug"]), None)
    audience_html = ""
    if audience:
        audience_html = f"""<div class="aud-match" style="margin-top:28px"><span class="num">{svc['number']}</span><div><b>Typically for {esc(audience['label'].lower())}</b><span>{esc(audience['text'])}</span></div></div>"""
    nav_links = f"""<div class="svc-nav">
      <a href="/services/{prev_svc['slug']}.html"><span><span class="n">{prev_svc['number']}</span>{esc(prev_svc['title'])}</span><span>{ICON['arrow-right']}</span></a>
      <a href="/services/{next_svc['slug']}.html"><span><span class="n">{next_svc['number']}</span>{esc(next_svc['title'])}</span><span>{ICON['arrow-right']}</span></a>
    </div>"""
    body = "\n".join([
        page_hero("Service " + svc["number"], esc(svc["title"]), esc(svc["body"]),
                  crumbs(("Services", "/services.html"), (svc["title"], ""))),
        f"""<section class="section">
  <div class="container">
    <div class="svc-detail">
      <div class="reveal">
        <p class="lead" style="color:var(--ink)">{esc(svc['body'])}</p>
        {audience_html}
        {nav_links}
      </div>
      <div class="deliv reveal" data-reveal="right">
        <h4>{esc(C['headings']['deliverablesLabel'])}</h4>
        <ul>{deliv}</ul>
      </div>
    </div>
  </div>
</section>""",
        cta_band(svc["slug"]),
    ])
    return page(
        f"{svc['title']} — BlueHarbor Advisory",
        svc["body"], f"/services/{svc['slug']}.html", body,
    )


def build_experience():
    body = "\n".join([
        page_hero("Experience & capabilities", 'Relevant professional <span class="serif">experience.</span>',
                  esc(C["experience"]["intro"]), crumbs(("Experience", ""))),
        f"""<section class="section" style="padding-top:0">
  <div class="container">
    <p class="disclaimer reveal">{ICON['info']}{esc(C['experience']['disclaimer'])}</p>
    <div class="exp-table">
      {''.join(f'''<div class="exp-row reveal"><div><h3>{esc(a["title"])}</h3><span class="exp-region">{ICON['map-pin-thin']}{esc(a["region"])}</span></div><p>{esc(a["text"])}</p></div>''' for a in C["experience"]["areas"])}
    </div>
  </div>
</section>""",
        why_section(),
        cta_band(),
    ])
    return page(
        "Experience & Capabilities — BlueHarbor Advisory",
        C["experience"]["intro"], "/experience.html", body,
    )


def build_team():
    body = "\n".join([
        page_hero("Our team", 'A multidisciplinary <span class="serif">advisory team.</span>',
                  esc(C["teamIntro"]), crumbs(("Team", ""))),
        team_section(id_attr="team-grid-section", show_heading=False),
        cta_band(),
    ])
    person_jsonld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": [
            {
                "@type": "Person",
                "name": m["name"],
                "jobTitle": m["role"],
                "image": DOMAIN + "/assets" + m["photo"],
                "worksFor": {"@type": "Organization", "name": C["site"]["name"]},
            }
            for m in C["team"]
        ],
    }
    return page(
        "Our Team — BlueHarbor Advisory",
        C["teamIntro"], "/team.html", body, extra_jsonld=person_jsonld,
    )


def build_contact():
    body = contact_section(
        id_attr="contact-form-section",
        heading_tag="h1",
        crumbs_html=crumbs(("Contact", "")),
    )
    # pad the top so the fixed nav never overlaps the crumbs on this single-section page
    body = f'<div style="padding-top:clamp(64px,10vw,96px)"></div>\n{body}'
    return page(
        "Contact BlueHarbor Advisory — Ntinda, Kampala, Uganda",
        C["cta"]["text"], "/contact.html", body,
    )


LEGAL_PLACEHOLDER = """<p><em>This page is a placeholder drafted for structure and formatting only. It is not legal advice
and has not been reviewed by a lawyer or by BlueHarbor Advisory Limited. Please replace this text with
wording approved by the firm (and, ideally, reviewed by Ugandan legal counsel) before the site goes live.</em></p>"""


def build_privacy():
    body = "\n".join([
        page_hero("Legal", "Privacy notice", "How BlueHarbor Advisory Limited collects, uses and protects information shared through this website.", crumbs(("Privacy notice", ""))),
        f"""<section class="section">
  <div class="container legal">
    {LEGAL_PLACEHOLDER}
    <h2>1. Who we are</h2>
    <p>{esc(C['site']['name'])} ("BlueHarbor", "we", "us") is an investment advisory and corporate finance firm based in
    {esc(C['site']['contact']['location'])}. This notice explains how we handle personal information submitted through
    this website, for example via the contact form.</p>
    <h2>2. Information we collect</h2>
    <ul>
      <li>Contact details you provide (name, organisation, email, phone number).</li>
      <li>The content of your enquiry, including the nature of your mandate.</li>
      <li>Standard technical data collected by our hosting provider (e.g. IP address, browser type) for security
      and analytics purposes.</li>
    </ul>
    <h2>3. How we use it</h2>
    <p>We use information you submit solely to respond to your enquiry and, where an engagement proceeds, to
    deliver the advisory services agreed with you. We do not sell personal information to third parties.</p>
    <h2>4. Confidentiality</h2>
    <p>Consistent with our operating principle of integrity, information you share is treated confidentially and
    is only shared internally, or with external specialists engaged on a mandate, on a need-to-know basis.</p>
    <h2>5. Your rights</h2>
    <p>You may ask us at any time to access, correct or delete personal information we hold about you by emailing
    <a href="mailto:{esc(C['site']['contact']['email'])}">{esc(C['site']['contact']['email'])}</a>.</p>
    <h2>6. Contact</h2>
    <p>Questions about this notice can be sent to <a href="mailto:{esc(C['site']['contact']['email'])}">{esc(C['site']['contact']['email'])}</a>
    or to our office in {esc(C['site']['contact']['location'])}.</p>
  </div>
</section>""",
    ])
    return page("Privacy Notice — BlueHarbor Advisory", "How BlueHarbor Advisory Limited handles personal information.", "/privacy.html", body)


def build_terms():
    body = "\n".join([
        page_hero("Legal", "Terms of use", "The terms that apply to your use of this website.", crumbs(("Terms of use", ""))),
        f"""<section class="section">
  <div class="container legal">
    {LEGAL_PLACEHOLDER}
    <h2>1. Purpose of this website</h2>
    <p>This website describes the advisory services offered by {esc(C['site']['name'])}. It is provided for general
    information purposes only.</p>
    <h2>2. No offer or advice</h2>
    <p>Nothing on this website constitutes an offer of securities, a solicitation, or investment, legal, tax or
    financial advice to any person. Engagement-specific advice is only provided under a written mandate agreed
    directly with BlueHarbor Advisory Limited.</p>
    <h2>3. No representation of past transactions</h2>
    <p>Descriptions of team experience and service capabilities on this website describe relevant professional
    background; they are not represented as transactions completed or contracted by BlueHarbor Advisory Limited
    itself.</p>
    <h2>4. Intellectual property</h2>
    <p>The content, design and branding of this website belong to BlueHarbor Advisory Limited or its licensors and
    may not be reproduced without permission.</p>
    <h2>5. Limitation of liability</h2>
    <p>While we take care to keep this website accurate and up to date, BlueHarbor Advisory Limited accepts no
    liability for errors, omissions, or reliance placed on website content in the absence of a formal engagement.</p>
    <h2>6. Governing law</h2>
    <p>These terms are governed by the laws of the Republic of Uganda.</p>
    <h2>7. Contact</h2>
    <p>Questions about these terms can be sent to <a href="mailto:{esc(C['site']['contact']['email'])}">{esc(C['site']['contact']['email'])}</a>.</p>
  </div>
</section>""",
    ])
    return page("Terms of Use — BlueHarbor Advisory", "The terms that apply to use of this website.", "/terms.html", body)


def build_404():
    body = f"""<section class="notfound container">
  <div>
    <span class="code">404</span>
    <h1 class="h2" style="margin:12px 0 16px">Page not found</h1>
    <p class="lead" style="margin:0 auto 28px">The page you're looking for may have moved. Try the homepage, or get in touch directly.</p>
    <div class="hero-ctas" style="justify-content:center">
      <a href="/" class="btn btn-primary">Back to homepage</a>
      <a href="/contact.html" class="btn btn-outline">Contact us</a>
    </div>
  </div>
</section>"""
    return page("Page not found — BlueHarbor Advisory", "The page you're looking for could not be found.", "/404.html", body)


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)


def build_sitemap(paths):
    urls = "\n".join(f"  <url><loc>{DOMAIN}{p}</loc></url>" for p in paths)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""


def main():
    write("index.html", build_home())
    write("about.html", build_about())
    write("services.html", build_services_overview())

    services = C["services"]
    n = len(services)
    for i, svc in enumerate(services):
        prev_svc = services[(i - 1) % n]
        next_svc = services[(i + 1) % n]
        write(f"services/{svc['slug']}.html", build_service_detail(svc, prev_svc, next_svc))

    write("experience.html", build_experience())
    write("team.html", build_team())
    write("contact.html", build_contact())
    write("privacy.html", build_privacy())
    write("terms.html", build_terms())
    write("404.html", build_404())

    paths = ["/", "/about.html", "/services.html", "/experience.html", "/team.html", "/contact.html",
             "/privacy.html", "/terms.html"] + [f"/services/{s['slug']}.html" for s in services]
    write("sitemap.xml", build_sitemap(paths))

    robots = f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n"
    write("robots.txt", robots)

    manifest = {
        "name": C["site"]["name"],
        "short_name": C["site"]["shortName"],
        "icons": [
            {"src": "/assets/brand/favicon-32.png", "sizes": "32x32", "type": "image/png"},
            {"src": "/assets/brand/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
        ],
        "theme_color": "#0B1C2B",
        "background_color": "#0B1C2B",
        "display": "browser",
    }
    write("site.webmanifest", json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
