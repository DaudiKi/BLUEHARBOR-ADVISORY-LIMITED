#!/usr/bin/env python3
"""
Static-site generator for the BlueHarbor Advisory Limited website.

Built on the BlueHarbor Advisory Design System (tokens.json +
components/bundle.css, read from the client's design-system Artifact).
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_PATH = os.path.join(ROOT, "content", "site-content.json")

with open(CONTENT_PATH, encoding="utf-8") as f:
    C = json.load(f)

DOMAIN = "https://" + C["site"]["domain"]
FONTS_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Cabin:wght@400;500;600;700&family=Newsreader:'
    'ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&display=swap" rel="stylesheet">'
)

NAV_ITEMS_HOME = [
    ("About", "#about"), ("Services", "#services"), ("Approach", "#approach"),
    ("Experience", "#experience"), ("Contact", "#contact"),
]
NAV_ITEMS_INNER = [
    ("About", "/about.html"), ("Services", "/services.html"), ("Approach", "/services.html#approach"),
    ("Experience", "/experience.html"), ("Contact", "/contact.html"),
]


def _load_logo(path):
    with open(os.path.join(ROOT, "assets", "brand", path), encoding="utf-8") as f:
        return f.read()


def esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def icon(name, extra="", size=""):
    cls = f"bh-i bh-i--{name}"
    if size:
        cls += f" bh-i--{size}"
    if extra:
        cls += f" {extra}"
    return f'<span class="{cls}" aria-hidden="true"></span>'


def bh_logo(href, height=56, aria_label=None):
    """Full-colour BlueHarbor logo (SVG), for light grounds (surface/surface-tint/surface-wash)."""
    label = f' aria-label="{esc(aria_label)}"' if aria_label else ""
    datauri = _logo_data_uri(LOGO_LIGHT_SVG)
    return (f'<a class="bh-logo" href="{href}" style="--bh-logo-h:{height}px"{label}>'
            f'<img src="{datauri}" alt="BlueHarbor Advisory" height="{height}"></a>')


def bh_logo_reverse(href, height=56, aria_label=None):
    """Reverse (white-on-navy) logo, for brand/surface-inverse grounds."""
    label = f' aria-label="{esc(aria_label)}"' if aria_label else ""
    datauri = _logo_data_uri(LOGO_DARK_SVG)
    return (f'<a class="bh-logo" href="{href}" style="--bh-logo-h:{height}px"{label}>'
            f'<img src="{datauri}" alt="BlueHarbor Advisory" height="{height}"></a>')


def _logo_data_uri(svg):
    import base64
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")


LOGO_LIGHT_SVG = _load_logo("logo-full-on-light.svg")
LOGO_DARK_SVG = _load_logo("logo-full-on-dark.svg")

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
<meta name="theme-color" content="#0a2363">
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
{jsonld}"""


# ---------------------------------------------------------------------------
# Header / Footer
# ---------------------------------------------------------------------------

def header_html(active_path, home: bool):
    items = NAV_ITEMS_HOME if home else NAV_ITEMS_INNER
    def link_attrs(href):
        return ' aria-current="page"' if (not home and href == active_path) else ""
    links = "".join(f'<a href="{href}"{link_attrs(href)}>{label}</a>' for label, href in items)
    mobile_links = "".join(f'<a href="{href}"{link_attrs(href)}>{label}</a>' for label, href in items)
    home_href = "#top" if home else "/"
    contact_href = "#contact" if home else "/contact.html"
    phones = C["site"]["contact"]["phones"]
    tel0 = phones[0].replace(" ", "")
    return f"""<header>
<div class="bh-topbar bh-on-inverse small"><div class="bh-container">
<div class="bh-topbar__group"><span class="bh-topbar__item">{icon('map-pin')}{esc(C['site']['contact']['location'])}</span><span class="bh-topbar__item bh-topbar__hide-sm">{icon('clock')}Mon&ndash;Fri</span></div>
<div class="bh-topbar__group"><a class="bh-topbar__item" href="mailto:{C['site']['contact']['email']}">{icon('mail')}{esc(C['site']['contact']['email'])}</a><a class="bh-topbar__item bh-topbar__hide-sm" href="tel:{tel0}">{icon('phone')}{phones[0]}</a></div>
</div></div>
<nav class="bh-nav" aria-label="Main" id="nav"><div class="bh-container">
{bh_logo(home_href, 56, aria_label='BlueHarbor Advisory — home')}
<div class="bh-nav__links" id="navLinks">{links}</div>
<div class="bh-nav__end">
<a class="bh-iconbtn bh-iconbtn--ghost bh-nav__phone" href="tel:{tel0}" aria-label="Call {phones[0]}">{icon('phone')}</a>
<a class="bh-btn bh-btn--primary bh-btn--chip bh-btn--sm" href="{contact_href}">Discuss your mandate<span class="bh-btn__chip">{icon('arrow-right')}</span></a>
<button class="bh-iconbtn bh-iconbtn--sm bh-nav__menu" id="menuBtn" aria-expanded="false" aria-controls="mobileMenu" aria-label="Open menu">{icon('menu')}</button>
</div>
</div></nav>
<div class="bh-mobile-menu" id="mobileMenu">
{mobile_links}
<a class="bh-btn bh-btn--primary bh-btn--block" href="{contact_href}">Discuss your mandate<span class="bh-i bh-i--arrow-right" aria-hidden="true"></span></a>
</div>
</header>"""


def footer_html(home: bool):
    phones = C["site"]["contact"]["phones"]
    phones_html = "<br>".join(phones)
    contact_href = "#contact" if home else "/contact.html"
    home_href = "#top" if home else "/"
    return f"""<footer class="bh-footer bh-on-inverse"><div class="bh-container">
<div class="bh-footer__top">
<div style="display:grid;gap:16px">{bh_logo_reverse('/', 56, aria_label='BlueHarbor Advisory')}<p class="small bh-footer__blurb">{esc(C['site']['description'])}</p></div>
<a class="bh-btn bh-btn--inverse bh-btn--chip" href="{contact_href}">Discuss your mandate<span class="bh-btn__chip">{icon('arrow-right')}</span></a>
</div>
<div class="bh-footer__grid small">
<div><h4 class="h4">Company</h4><ul>
<li><a href="/about.html">About</a></li>
<li><a href="/services.html#approach">Approach</a></li>
<li><a href="/experience.html">Experience</a></li>
<li><a href="{contact_href}">Contact</a></li>
</ul></div>
<div><h4 class="h4">Services</h4><ul>
{''.join(f'<li><a href="/services/{s["slug"]}.html">{esc(s["title"].split(" &")[0].split(" and")[0])}</a></li>' for s in C['services'])}
</ul></div>
<div><h4 class="h4">Contact</h4><ul class="bh-footer__contact">
<li>{icon('mail')}<a href="mailto:{C['site']['contact']['email']}">{esc(C['site']['contact']['email'])}</a></li>
<li>{icon('phone')}<span>{phones_html}</span></li>
<li>{icon('map-pin')}<span>{esc(C['site']['contact']['location'])}</span></li>
</ul></div>
<div><h4 class="h4">Hours</h4><ul class="bh-footer__contact">
<li>{icon('clock')}<span>Monday to Friday</span></li>
</ul></div>
</div>
<div class="bh-footer__base small"><span>&copy; <span id="yr"></span> {esc(C['site']['name'])} &middot; {esc(C['site']['tagline'])}</span>
<a class="bh-iconbtn bh-iconbtn--inverse bh-iconbtn--sm" href="{home_href}" aria-label="Back to top">{icon('arrow-right', extra='bh-i--up')}</a></div>
<p class="caption" style="padding:var(--space-4) 0;color:var(--ink-inverse-muted);max-width:70ch">{esc(C['site']['name'])} provides advisory and analytical services within the applicable regulatory and professional framework. Nothing on this website constitutes an offer of securities or investment advice to any person. &middot; <a href="/privacy.html">Privacy notice</a> &middot; <a href="/terms.html">Terms of use</a></p>
</div></footer>"""


def page(title, description, path, body, home=False, extra_jsonld=None):
    active_path = "/" + path.lstrip("/") if path != "/" else "/"
    return f"""<!doctype html>
<html lang="en-UG">
<head>
{head(title, description, path, extra_jsonld)}
</head>
<body class="bh-root">
<a href="#main" class="skip">Skip to content</a>
{header_html(active_path, home)}
<main id="main">
{body}
</main>
{footer_html(home)}
<script src="/js/main.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Shared section components
# ---------------------------------------------------------------------------

def section_header(eyebrow_text, heading_html, lead=None, split_link=None, center=False, label_dot=True):
    tag_cls = "bh-tag bh-tag--label bh-tag--dot" if label_dot else "eyebrow bh-eyebrow"
    tag = f'<span class="{tag_cls}">{esc(eyebrow_text)}</span>' if label_dot else f'<span class="eyebrow bh-eyebrow">{esc(eyebrow_text)}</span>'
    lead_html = f'<p class="body-lg bh-sh__lead">{lead}</p>' if lead else ""
    sh_cls = "bh-sh" + (" bh-sh--center" if center else "")
    inner = f"""<div class="{sh_cls}">
      {tag}
      <h2 class="h2">{heading_html}</h2>
      {lead_html}
    </div>"""
    if split_link:
        label, href = split_link
        return f"""<div class="bh-sh-split">{inner}<a class="bh-arrowlink" href="{href}">{label}{icon('arrow-right')}</a></div>"""
    return inner


def audience_card(idx, audience_id, eyebrow_text, heading, body_text, icon_name, href, foot_label,
                   feature=False):
    tile_cls = "bh-tile bh-tile--inverse" if feature else "bh-tile"
    btn_cls = "bh-iconbtn bh-iconbtn--sm bh-iconbtn--inverse" if feature else "bh-iconbtn bh-iconbtn--sm"
    card_cls = "bh-card bh-card--feature bh-on-inverse" if feature else "bh-card"
    foot = ""
    if foot_label:
        foot = f"""<div class="bh-card__foot"><span>{esc(foot_label)}</span><span class="{btn_cls}">{icon('arrow-up-right')}</span></div>"""
    tag = f'<a class="{card_cls}" href="{href}">' if href else f'<div class="{card_cls}">'
    close = '</a>' if href else '</div>'
    return f"""{tag}<div class="bh-card__top"><span class="{tile_cls}">{icon(icon_name)}</span><span class="bh-card__index">{idx:02d}</span></div><span class="eyebrow bh-eyebrow">{esc(eyebrow_text)}</span><h3 class="h3">{esc(heading)}</h3><p class="body bh-muted">{esc(body_text)}</p>{foot}{close}"""


def plain_icon_card(heading, body_text, icon_name, navy=False):
    tile_cls = "bh-tile bh-tile--navy" if navy else "bh-tile"
    return f"""<div class="bh-card" style="cursor:default"><span class="{tile_cls}">{icon(icon_name)}</span><h3 class="h3" style="margin-top:var(--space-2)">{esc(heading)}</h3><p class="body bh-muted">{esc(body_text)}</p></div>"""


# ---------------------------------------------------------------------------
# Home-page sections
# ---------------------------------------------------------------------------

AUDIENCE_META = {
    "enterprises": {"icon": "building", "headline": "Ready your business for capital", "foot": "Explore support"},
    "investors": {"icon": "trending-up", "headline": "Decide with discipline", "foot": "Explore support"},
    "institutions": {"icon": "landmark", "headline": "Widen access to finance", "foot": "Explore support"},
}

SECTOR_ICONS = {
    "Agribusiness": "leaf",
    "Manufacturing": "factory",
    "Technology-enabled services": "cpu",
    "Financial inclusion": "coins",
    "Climate-related enterprises": "globe",
}

SERVICE_ICONS = ["calculator", "layers", "globe"]
STEP_ICONS = ["target", "search", "file-text", "check"]
EXPERIENCE_ICONS = ["trending-up", "building", "coins"]
WHY_ICONS = ["map-pin", "layers", "file-text"]
VALUE_ICONS = {"Excellence": "award", "Integrity": "shield-check", "Client focus": "target"}


def hero_section():
    mo = C["marketOrientation"][0]
    rows = []
    for aud in C["audiences"]:
        meta = AUDIENCE_META[aud["id"]]
        svc = next(s for s in C["services"] if s["slug"] == aud["servicePillar"])
        short = aud["text"].split(".")[0] + "."
        rows.append(f"""<a class="bh-hero__row" href="/services/{svc['slug']}.html"><span class="bh-tile bh-tile--inverse">{icon(meta['icon'])}</span><span><b>{esc(aud['label'])}</b><small>{esc(short)}</small></span><span class="bh-iconbtn bh-iconbtn--inverse bh-iconbtn--sm">{icon('arrow-up-right')}</span></a>""")
    return f"""<section class="bh-hero" id="top"><div class="bh-container"><div class="bh-hero__grid">
<div class="bh-hero__copy">
<span class="bh-tag bh-tag--dot">Investment advisory &middot; Corporate finance</span>
<h1 class="display-xl">Navigating <span class="bh-em">growth</span>. Empowering success.</h1>
<p class="body-lg bh-muted" style="max-width:60ch">{esc(C['site']['description'])}</p>
<div class="bh-hero__actions"><a class="bh-btn bh-btn--primary bh-btn--chip bh-btn--lg" href="#contact">Discuss your mandate<span class="bh-btn__chip">{icon('arrow-right')}</span></a><a class="bh-btn bh-btn--secondary bh-btn--lg" href="#services">Explore our services</a></div>
<ul class="bh-hero__proof"><li>{icon('check')}Locally grounded advice</li><li>{icon('check')}Scoped to each mandate</li><li>{icon('check')}Client confidentiality</li></ul>
</div>
<div class="bh-hero__visual">
<aside class="bh-hero__panel bh-on-inverse"><div class="bh-hero__panel-head"><span class="eyebrow bh-eyebrow">Who we support</span><span class="bh-tag bh-tag--inverse">3 audiences</span></div>
<div class="bh-hero__rows">{''.join(rows)}</div></aside>
<div class="bh-hero__badge"><span class="bh-tile bh-tile--sm">{icon('globe')}</span><span><b>Uganda &amp; East Africa</b><small>Based in Kampala</small></span></div>
</div>
</div></div></section>"""


def who_we_support_section(show_header=True):
    cards = []
    for i, aud in enumerate(C["audiences"]):
        meta = AUDIENCE_META[aud["id"]]
        svc = next(s for s in C["services"] if s["slug"] == aud["servicePillar"])
        feature = (i == 1)
        cards.append(audience_card(i + 1, aud["id"], aud["label"], meta["headline"], aud["text"],
                                    meta["icon"], f"/services/{svc['slug']}.html", meta["foot"], feature=feature))
    head_html = section_header("Who we support", 'Routed to the right <span class="bh-em">advisory</span> pillar') if show_header else ""
    return f"""<section class="bh-pv" id="who-we-support" style="padding-block:var(--space-9)"><div class="bh-container">
{head_html}
<div class="bh-grid-3" style="margin-top:{'var(--space-7)' if show_header else '0'}">{''.join(cards)}</div>
</div></section>"""


def market_orientation_section(show_header=True):
    mo = C["marketOrientation"]
    chips = "".join(f'<span class="bh-tag">{icon(SECTOR_ICONS.get(x, "layers"))}{esc(x)}</span>' for x in mo[1]["items"])
    head_html = section_header("Market orientation", 'Rooted in Uganda, <span class="bh-em">regional</span> in perspective') if show_header else ""
    return f"""<section class="bh-pv" style="background:var(--surface-wash);padding-block:var(--space-9)"><div class="bh-container">
{head_html}
<div class="bh-facts" style="margin-top:{'var(--space-7)' if show_header else '0'}">
<div class="bh-fact"><span class="bh-tile">{icon('map-pin')}</span><span class="eyebrow bh-eyebrow">{esc(mo[0]['label'])}</span><p class="body">{esc(mo[0]['text'])}</p></div>
<div class="bh-fact"><span class="bh-tile">{icon('layers')}</span><span class="eyebrow bh-eyebrow">{esc(mo[1]['label'])}</span><div class="bh-tags">{chips}</div></div>
<div class="bh-fact"><span class="bh-tile">{icon('target')}</span><span class="eyebrow bh-eyebrow">{esc(mo[2]['label'])}</span><p class="body">{esc(mo[2]['text'])}</p></div>
</div>
</div></section>"""


def purpose_section(show_header=True):
    p = C["purpose"]
    values = "".join(plain_icon_card(v["name"], v["text"], VALUE_ICONS.get(v["name"], "award"), navy=True) for v in p["values"])
    head_html = section_header("Purpose & principles", 'What we stand <span class="bh-em">for</span>') if show_header else ""
    return f"""<section class="bh-pv" id="purpose" style="padding-block:var(--space-9)"><div class="bh-container">
{head_html}
<div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-8);margin-top:{'var(--space-7)' if show_header else '0'};align-items:start">
<div style="display:grid;gap:var(--space-6)">
<div><span class="eyebrow bh-eyebrow">Mission</span><p class="display-lg" style="margin-top:var(--space-3)">{esc(p['mission'])}</p></div>
<div><span class="eyebrow bh-eyebrow">Vision</span><p class="display-lg" style="margin-top:var(--space-3)">{esc(p['vision'])}</p></div>
</div>
<div class="bh-grid-3" style="grid-template-columns:1fr">{values}</div>
</div>
</div></section>"""


def services_section(show_header=True, default_open=True):
    pillars = []
    for i, svc in enumerate(C["services"]):
        deliv = "".join(f'<span class="bh-tag">{icon("check")}{esc(d)}</span>' for d in svc["deliverables"])
        pillars.append(f"""<article class="bh-pillar"><div class="bh-pillar__main"><div class="bh-pillar__head"><span class="bh-tile bh-tile--lg">{icon(SERVICE_ICONS[i])}</span><span class="bh-pillar__num">{svc['number']}</span></div><h3 class="h3">{esc(svc['title'])}</h3><p class="body bh-muted">{esc(svc['body'])}</p><a class="bh-arrowlink" href="/services/{svc['slug']}.html">Learn more about this service{icon('arrow-right')}</a></div><div class="bh-pillar__deliv"><span class="eyebrow bh-eyebrow">{esc(C['headings']['deliverablesLabel'])}</span><div class="bh-tags">{deliv}</div></div></article>""")
    head_html = section_header(C["headings"]["services"], 'Three pillars, from <span class="bh-em">preparation</span> to execution', C["servicesIntro"]) if show_header else ""
    return f"""<section class="bh-pv" id="services" style="background:var(--surface-tint);padding-block:var(--space-9)"><div class="bh-container">
{head_html}
<div class="bh-pillars" style="margin-top:{'var(--space-7)' if show_header else '0'}">{''.join(pillars)}</div>
</div></section>"""


def approach_section(show_header=True):
    steps = C["approach"]["steps"]
    items = "".join(f"""<li><div class="bh-steps__icon"><span class="bh-tile">{icon(STEP_ICONS[i])}</span><span class="bh-steps__n">{s['n']}</span></div><h4 class="h4">{esc(s['title'])}</h4><p class="body bh-muted">{esc(s['text'])}</p></li>""" for i, s in enumerate(steps))
    head_html = section_header(C["headings"]["approach"], 'A clear course, <span class="bh-em">agreed</span> from the outset') if show_header else ""
    return f"""<section class="bh-pv" id="approach" style="padding-block:var(--space-9)"><div class="bh-container">
{head_html}
<ol class="bh-steps" style="margin-top:{'var(--space-7)' if show_header else '0'}">{items}</ol>
<div class="bh-callout" style="margin-top:var(--space-7)"><span class="bh-tile bh-tile--navy">{icon('shield-check')}</span><div class="bh-callout__body"><span class="eyebrow bh-eyebrow">{esc(C['headings']['operatingPrincipleLabel'])}</span><p class="body">{esc(C['approach']['operatingPrinciple'])}</p></div></div>
</div></section>"""


def experience_section(show_header=True):
    exp = C["experience"]
    rows = []
    for i, a in enumerate(exp["areas"]):
        open_attr = " open" if i == 0 else ""
        rows.append(f"""<details class="bh-cap"{open_attr}><summary><span class="bh-tile">{icon(EXPERIENCE_ICONS[i])}</span><span><h4 class="h4">{esc(a['title'])}</h4><span class="bh-tag bh-tag--soft">{icon('map-pin')}{esc(a['region'])}</span></span><span class="bh-iconbtn bh-iconbtn--sm">{icon('plus')}</span></summary><p class="body bh-cap__body">{esc(a['text'])}</p></details>""")
    head_html = section_header(C["headings"]["experience"], 'Relevant professional <span class="bh-em">experience</span>', exp["intro"]) if show_header else ""
    return f"""<section class="bh-pv" style="background:var(--surface-wash);padding-block:var(--space-9)"><div class="bh-container">
{head_html}
<div class="bh-callout" style="margin:{'var(--space-7)' if show_header else '0'} 0 var(--space-5)"><span class="bh-tile bh-tile--navy">{icon('shield-check')}</span><div class="bh-callout__body"><p class="body">{esc(exp['disclaimer'])}</p></div></div>
<div class="bh-caps">{''.join(rows)}</div>
</div></section>"""


def why_section(show_header=True):
    cards = []
    for i, w in enumerate(C["why"]):
        cards.append(audience_card(i + 1, "why", w["title"].split(",")[0], w["title"], w["text"], WHY_ICONS[i],
                                    "/contact.html", "Get in touch"))
    head_html = section_header(C["headings"]["why"], 'From analysis to <span class="bh-em">decisions</span>') if show_header else ""
    return f"""<section class="bh-pv" style="padding-block:var(--space-9)"><div class="bh-container">
{head_html}
<div class="bh-grid-3" style="margin-top:{'var(--space-7)' if show_header else '0'}">{''.join(cards)}</div>
</div></section>"""


def map_card():
    q = C["site"]["contact"]["mapQuery"].replace(" ", "+")
    src = f"https://www.google.com/maps?q={q}&z=15&output=embed"
    return f"""<div class="bh-map">
  <iframe title="Map showing BlueHarbor Advisory in {esc(C['site']['contact']['location'])}" data-src="{src}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
  <div class="bh-map-bar"><span class="small">{esc(C['site']['contact']['location'])}</span><a class="bh-arrowlink" href="{C['site']['contact']['directionsUrl']}" target="_blank" rel="noopener">Get directions{icon('arrow-right')}</a></div>
</div>"""


def contact_cta_and_form(show_header=False):
    phones = C["site"]["contact"]["phones"]
    phones_line = " &middot; ".join(phones)
    services_opts = "".join(f"<option>{esc(s['title'])}</option>" for s in C["services"]) + "<option>Not sure yet</option>"
    cta = f"""<section class="bh-cta" id="contact"><div class="bh-container"><div class="bh-cta__card bh-on-inverse">
<div class="bh-cta__copy"><span class="bh-tag bh-tag--inverse bh-tag--dot">Contact</span><h2 class="display-lg">Let's discuss your <span class="bh-em">mandate</span></h2><p class="body-lg">{esc(C['cta']['text'])}</p>
<div class="bh-cta__actions"><a class="bh-btn bh-btn--inverse bh-btn--chip bh-btn--lg" href="#contact-form">Discuss your mandate<span class="bh-btn__chip">{icon('arrow-right')}</span></a><a class="bh-btn bh-btn--inverse-outline bh-btn--lg" href="mailto:{C['site']['contact']['email']}">{icon('mail')}Email the team</a></div></div>
<div class="bh-cta__details">
<a class="bh-cta__item" href="mailto:{C['site']['contact']['email']}"><span class="bh-tile bh-tile--inverse">{icon('mail')}</span><span><small>Email</small><span>{esc(C['site']['contact']['email'])}</span></span></a>
<a class="bh-cta__item" href="tel:{phones[0].replace(' ', '')}"><span class="bh-tile bh-tile--inverse">{icon('phone')}</span><span><small>Phone</small><span>{esc(phones_line)}</span></span></a>
<div class="bh-cta__item"><span class="bh-tile bh-tile--inverse">{icon('map-pin')}</span><span><small>Location</small><span>{esc(C['site']['contact']['location'])}</span></span></div>
</div>
</div></div></section>"""

    form = f"""<section class="bh-pv" id="contact-form" style="padding-block:var(--space-9)"><div class="bh-container" style="display:grid;gap:var(--space-7);max-width:var(--container-narrow);margin-inline:auto">
<div class="bh-formcard" style="max-width:none">
<form class="bh-form" id="contactForm" novalidate data-access-key="YOUR_WEB3FORMS_ACCESS_KEY" data-mailto="{C['site']['contact']['email']}">
<h3 class="h3">Tell us about your requirement</h3>
<div class="bh-form__row">
<div class="bh-field"><label for="f-name">Full name</label><div class="bh-input">{icon('users')}<input id="f-name" name="name" autocomplete="name" required></div><span class="small bh-field__error" hidden>{icon('close')}Please enter your name.</span></div>
<div class="bh-field"><label for="f-org">Organisation</label><div class="bh-input">{icon('building')}<input id="f-org" name="organisation" autocomplete="organization"></div></div>
</div>
<div class="bh-form__row">
<div class="bh-field"><label for="f-email">Work email</label><div class="bh-input">{icon('mail')}<input id="f-email" name="email" type="email" autocomplete="email" required></div><span class="small bh-field__error" hidden>{icon('close')}Enter a full email address, for example name@company.com.</span></div>
<div class="bh-field"><label for="f-phone">Phone <span class="bh-muted" style="font-weight:400">(optional)</span></label><div class="bh-input">{icon('phone')}<input id="f-phone" name="phone" type="tel" autocomplete="tel"></div></div>
</div>
<fieldset class="bh-field"><legend>I am a</legend><div class="bh-seg">
<label><input type="radio" name="type" id="r1" value="Enterprise" checked><span>{icon('building')}Enterprise</span></label>
<label><input type="radio" name="type" id="r2" value="Investor"><span>{icon('trending-up')}Investor</span></label>
<label><input type="radio" name="type" id="r3" value="Institution"><span>{icon('landmark')}Institution</span></label>
</div></fieldset>
<div class="bh-field"><label for="f-svc">Area of interest</label><select id="f-svc" name="service">{services_opts}</select></div>
<div class="bh-field"><label for="f-msg">Message</label><textarea id="f-msg" name="message" required placeholder="Your mandate, sector, stage of growth and timing" aria-describedby="m-h"></textarea><span id="m-h" class="caption bh-field__hint">Tell us about your mandate, sector and timing.</span><span class="small bh-field__error" hidden>{icon('close')}Please add a short description.</span></div>
<p class="bh-form-banner bh-form-banner--ok" id="formOk" role="status">Thank you &mdash; your enquiry has been received. A member of the BlueHarbor team will be in touch.</p>
<p class="bh-form-banner bh-form-banner--err" id="formError" role="alert"></p>
<div class="bh-form__foot"><span class="caption bh-form__note">{icon('shield-check')}Enquiries are treated as confidential.</span><button class="bh-btn bh-btn--accent" type="submit">Send enquiry{icon('send')}</button></div>
</form>
</div>
{map_card()}
</div></section>
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
    return cta + "\n" + form


def cta_band_mini(service_slug=""):
    """A compact closing band for inner pages that already have their own hero/section-header."""
    q = f"?service={service_slug}" if service_slug else ""
    return f"""<section class="bh-pv" style="padding-block:var(--space-8)"><div class="bh-container">
<div class="bh-callout" style="grid-template-columns:auto 1fr auto;align-items:center"><span class="bh-tile bh-tile--navy">{icon('send')}</span><div class="bh-callout__body"><span class="eyebrow bh-eyebrow">{esc(C['cta']['title'])}</span><p class="body bh-muted">{esc(C['cta']['text'])}</p></div><a class="bh-btn bh-btn--primary bh-btn--chip" href="/contact.html{q}">Discuss your mandate<span class="bh-btn__chip">{icon('arrow-right')}</span></a></div>
</div></section>"""


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def build_home():
    body = "\n".join([
        hero_section(),
        who_we_support_section(),
        market_orientation_section(),
        purpose_section(),
        services_section(),
        approach_section(),
        experience_section(),
        why_section(),
        contact_cta_and_form(),
    ])
    return page(
        f"{C['site']['shortName']} — Investment Advisory & Corporate Finance, Kampala",
        C["site"]["description"], "/", body, home=True,
    )


def inner_hero(eyebrow_text, heading_html, lead=""):
    return f"""<section class="bh-pv" style="background:var(--surface-tint);padding-block:var(--space-8)"><div class="bh-container">
{section_header(eyebrow_text, heading_html, lead)}
</div></section>"""


def build_about():
    body = "\n".join([
        inner_hero("About BlueHarbor", 'Practical, locally grounded <span class="bh-em">advice</span>', C["about"]["summary"]),
        f"""<section class="bh-pv" style="padding-block:var(--space-8) var(--space-9)"><div class="bh-container"><p class="body-lg bh-muted" style="max-width:var(--container-narrow)">{esc(C['about']['detail'])}</p></div></section>""",
        who_we_support_section(show_header=False),
        market_orientation_section(),
        purpose_section(),
        why_section(),
        cta_band_mini(),
    ])
    return page(
        "About BlueHarbor Advisory — Investment Advisory Firm in Kampala, Uganda",
        C["about"]["summary"], "/about.html", body,
    )


def build_services_overview():
    body = "\n".join([
        inner_hero("Our advisory services", 'Three pillars, from <span class="bh-em">preparation</span> to execution', C["servicesIntro"]),
        services_section(show_header=False),
        approach_section(),
        cta_band_mini(),
    ])
    return page(
        "Advisory Services — Corporate Finance, Transaction Advisory & Development Finance",
        C["servicesIntro"], "/services.html", body,
    )


def build_service_detail(svc, idx, prev_svc, next_svc):
    deliv = "".join(f'<span class="bh-tag">{icon("check")}{esc(d)}</span>' for d in svc["deliverables"])
    audience = next((a for a in C["audiences"] if a["servicePillar"] == svc["slug"]), None)
    aud_html = ""
    if audience:
        aud_html = f"""<div class="bh-callout" style="margin-top:var(--space-6)"><span class="bh-tile bh-tile--navy">{icon(AUDIENCE_META[audience['id']]['icon'])}</span><div class="bh-callout__body"><span class="eyebrow bh-eyebrow">Typically for {esc(audience['label'].lower())}</span><p class="body">{esc(audience['text'])}</p></div></div>"""
    nav_links = f"""<div style="display:grid;gap:var(--space-3);margin-top:var(--space-6)">
<a class="bh-cta__item" style="background:var(--surface-wash);color:var(--ink)" href="/services/{prev_svc['slug']}.html"><span class="bh-tile">{icon(SERVICE_ICONS[(idx - 1) % 3])}</span><span><small style="color:var(--accent-text)">{prev_svc['number']}</small><span>{esc(prev_svc['title'])}</span></span></a>
<a class="bh-cta__item" style="background:var(--surface-wash);color:var(--ink)" href="/services/{next_svc['slug']}.html"><span class="bh-tile">{icon(SERVICE_ICONS[(idx + 1) % 3])}</span><span><small style="color:var(--accent-text)">{next_svc['number']}</small><span>{esc(next_svc['title'])}</span></span></a>
</div>"""
    body = "\n".join([
        inner_hero(f"Service {svc['number']}", esc(svc["title"]), svc["body"]),
        f"""<section class="bh-pv" style="padding-block:0 var(--space-9)"><div class="bh-container">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-8)">
    <div>{aud_html}{nav_links}</div>
    <div class="bh-pillar__deliv"><span class="eyebrow bh-eyebrow">{esc(C['headings']['deliverablesLabel'])}</span><div class="bh-tags">{deliv}</div></div>
  </div>
</div></section>""",
        cta_band_mini(svc["slug"]),
    ])
    return page(
        f"{svc['title']} — BlueHarbor Advisory",
        svc["body"], f"/services/{svc['slug']}.html", body,
    )


def build_experience():
    body = "\n".join([
        inner_hero("Experience & capabilities", 'Relevant professional <span class="bh-em">experience</span>', C["experience"]["intro"]),
        experience_section(show_header=False),
        why_section(),
        cta_band_mini(),
    ])
    return page(
        "Experience & Capabilities — BlueHarbor Advisory",
        C["experience"]["intro"], "/experience.html", body,
    )


def build_contact():
    body = "\n".join([
        inner_hero("Contact", "Let's discuss your <span class=\"bh-em\">mandate</span>", C["cta"]["text"]),
        contact_cta_and_form(),
    ])
    return page(
        "Contact BlueHarbor Advisory — Ntinda, Kampala, Uganda",
        C["cta"]["text"], "/contact.html", body,
    )


LEGAL_PLACEHOLDER = """<p><em>This page is a placeholder drafted for structure and formatting only. It is not legal advice
and has not been reviewed by a lawyer or by BlueHarbor Advisory Limited. Please replace this text with
wording approved by the firm (and, ideally, reviewed by Ugandan legal counsel) before the site goes live.</em></p>"""


def build_privacy():
    body = "\n".join([
        inner_hero("Legal", "Privacy notice", "How BlueHarbor Advisory Limited collects, uses and protects information shared through this website."),
        f"""<section class="bh-pv" style="padding-block:0 var(--space-9)"><div class="bh-container legal bh-legal">
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
    <a class="bh-link" href="mailto:{esc(C['site']['contact']['email'])}">{esc(C['site']['contact']['email'])}</a>.</p>
    <h2>6. Contact</h2>
    <p>Questions about this notice can be sent to <a class="bh-link" href="mailto:{esc(C['site']['contact']['email'])}">{esc(C['site']['contact']['email'])}</a>
    or to our office in {esc(C['site']['contact']['location'])}.</p>
  </div></section>""",
    ])
    return page("Privacy Notice — BlueHarbor Advisory", "How BlueHarbor Advisory Limited handles personal information.", "/privacy.html", body)


def build_terms():
    body = "\n".join([
        inner_hero("Legal", "Terms of use", "The terms that apply to your use of this website."),
        f"""<section class="bh-pv" style="padding-block:0 var(--space-9)"><div class="bh-container legal bh-legal">
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
    <p>Questions about these terms can be sent to <a class="bh-link" href="mailto:{esc(C['site']['contact']['email'])}">{esc(C['site']['contact']['email'])}</a>.</p>
  </div></section>""",
    ])
    return page("Terms of Use — BlueHarbor Advisory", "The terms that apply to use of this website.", "/terms.html", body)


def build_404():
    body = f"""<section class="bh-pv bh-notfound"><div class="bh-container" style="text-align:center">
    <span class="bh-code">404</span>
    <h1 class="h2" style="margin:var(--space-4) 0">Page not found</h1>
    <p class="body-lg bh-muted" style="max-width:48ch;margin:0 auto var(--space-6)">The page you're looking for may have moved. Try the homepage, or get in touch directly.</p>
    <div style="display:flex;gap:var(--space-3);justify-content:center;flex-wrap:wrap">
      <a class="bh-btn bh-btn--primary" href="/">Back to homepage</a>
      <a class="bh-btn bh-btn--secondary" href="/contact.html">Contact us</a>
    </div>
  </div></section>"""
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
        write(f"services/{svc['slug']}.html", build_service_detail(svc, i, prev_svc, next_svc))

    write("experience.html", build_experience())
    write("contact.html", build_contact())
    write("privacy.html", build_privacy())
    write("terms.html", build_terms())
    write("404.html", build_404())

    paths = ["/", "/about.html", "/services.html", "/experience.html", "/contact.html",
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
            {"src": "/assets/brand/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
        "theme_color": "#0a2363",
        "background_color": "#ffffff",
        "display": "browser",
    }
    write("site.webmanifest", json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
