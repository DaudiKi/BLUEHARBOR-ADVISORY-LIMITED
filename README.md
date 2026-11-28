# BlueHarbor Advisory Limited — Website

The production marketing website for **BlueHarbor Advisory Limited**, an
investment advisory and corporate finance firm based in Ntinda, Kampala,
Uganda. It is a complete, dependency-free static website: every page is a
plain HTML file, styled by one shared stylesheet and one shared script, so
it runs anywhere — a laptop, GitHub Pages, Netlify, Vercel, or any ordinary
web host — with no build step, server, framework or install required.

The copy and contact details are taken from the firm's own company profile
(`content/site-content.json`). Nothing on the site has been invented: no
stats, client logos, testimonials or deal counts, per the firm's compliance
guidance.

**Visual design**: the site keeps its original layout, components and
typography (Figtree + Newsreader) — only the **color palette and logo**
have been updated to match the **BlueHarbor Advisory Design System** (a
separate Claude Design System artifact, maintained by the client): navy
`#0A2363` as the primary brand color and gold `#D6AA56`&ndash;`#E2C17D` as
the accent, replacing the earlier navy/turquoise palette. These live as
CSS custom properties at the top of `css/styles.css` (`--navy`, `--teal`,
etc. — the variable names are historical and now hold the new hex values)
and in the recolored SVGs under `assets/brand/` and `assets/hero/`. The
design system's own component framework (`bundle.css`), spacing/radius
scale and Cabin/Newsreader type pairing were **not** adopted — this site's
existing accordion, tabs and card markup were kept as-is.
`design-system/tokens.css` and `design-system/theme.css` in this repo are
an **older, superseded** reference (an earlier navy/teal direction) kept
only for history; ignore them for anything visual.

## 1. What's in the site

| Route | Description |
|---|---|
| `/` | Home — the full one-page design (hero, about, services, approach, market orientation, why BlueHarbor, experience, purpose & principles, contact). |
| `/about.html` | About, who we support, market orientation, purpose & principles, why BlueHarbor. |
| `/services.html` | Overview of the three service pillars + engagement approach. |
| `/services/corporate-finance.html` | Corporate Finance & Enterprise Advisory detail page. |
| `/services/transaction-advisory.html` | Investment & Transaction Advisory detail page. |
| `/services/development-finance.html` | Development Finance & Programme Advisory detail page. |
| `/experience.html` | Experience & capabilities, with the required disclaimer. |
| `/contact.html` | Contact form, contact details and an embedded Google Map. |
| `/privacy.html`, `/terms.html` | Legal pages. **Placeholder copy — see §6.** |
| `/404.html` | Not-found page. |

There is no dedicated team page — the client asked for the team section to
be removed from the site. The team's data still lives in
`content/site-content.json` (`team` / `teamIntro`) in case it needs to come
back later; `tools/build.py` simply doesn't render it anywhere right now.

Every page shares `css/styles.css` and `js/main.js`, so behaviour (mobile
menu, scroll reveals, the services accordion, audience tabs,
the contact form, back-to-top, reduced-motion support) is
identical everywhere.

## 2. Running it locally

No install, no build. From the project root:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Any other static server works too (`npx serve`, VS Code's "Live Server",
etc.) — just serve the repository root.

## 3. How content is managed

**Do not hand-edit the generated `*.html` files directly.** All copy lives
in [`content/site-content.json`](content/site-content.json) — the firm's
company profile, transcribed verbatim — and the HTML pages are generated
from it by [`tools/build.py`](tools/build.py), a small, dependency-free
Python script (standard library only).

To change copy (a phone number, a team bio, a service description, the map
address, etc.):

1. Edit `content/site-content.json`.
2. Re-run the generator:
   ```bash
   python3 tools/build.py
   ```
3. Commit the updated JSON **and** the regenerated HTML files.

To change layout, add a new section, or add a new page, edit
`tools/build.py` (it has one small function per section — `hero_section`,
`services_accordion`, etc.) and re-run it the same way.

Design tokens (`design-system/tokens.css`, `design-system/theme.css`) and
the original approved visual prototype (`prototype/` — kept for
reference) are included from the client's design handoff pack; the live
styles in `css/styles.css` mirror them exactly.

## 4. Google Maps

The map on `/contact.html` and in the home page's contact section uses
Google's **keyless embed** — no API key, billing account or Google Cloud
project required:

```
https://www.google.com/maps?q=Ntinda,+Kampala,+Uganda&z=15&output=embed
```

This is driven by `site.contact.mapQuery` in `content/site-content.json`.
It currently centres on **Ntinda, Kampala** generally, since the firm's
exact office address/pin was not supplied. **To pin the exact office:**

1. Find the location on [Google Maps](https://www.google.com/maps), right-click
   the exact spot, and copy the address (or the lat/lng).
2. Update `site.contact.mapQuery` in `content/site-content.json` (e.g.
   `"Plot 12, Ntinda Road, Kampala, Uganda"` or `"0.3476,32.6111"`), and
   update `site.contact.directionsUrl` the same way.
3. Re-run `python3 tools/build.py`.

The map `<iframe>` is lazy-loaded (it only fetches once scrolled near the
viewport) and desaturated slightly with CSS to sit with the site's navy/teal
palette. A **"Get directions"** link next to it opens Google Maps
directions in a new tab.

If the firm later wants a styled, interactive map (custom markers, brand
colours, etc.) that requires the paid **Maps Embed/JavaScript API** and a
`NEXT_PUBLIC`-style key — the keyless embed above is deliberately the
simpler, zero-cost option for a marketing site like this one.

## 5. Contact form (emails info@blueharboradvisory.com)

The form (`#contactForm`, in `js/main.js`) validates in the browser and POSTs
JSON to **`/api/contact`** — a Vercel serverless function in
[`api/contact.js`](api/contact.js) that emails the enquiry to
`info@blueharboradvisory.com` through [Resend](https://resend.com). The visitor's
address is set as Reply-To, so replying goes straight to them. A hidden
`website` field traps simple spam bots.

**One-time setup** (Vercel → project → Settings → Environment Variables, then
redeploy):

| Variable | Required | Value |
|---|---|---|
| `RESEND_API_KEY` | yes | API key from your Resend account |
| `RESEND_FROM` | recommended | e.g. `BlueHarbor Website <enquiries@blueharboradvisory.com>` — the domain must be verified in Resend (Resend → Domains → add DNS records) |
| `CONTACT_TO` | no | recipient override (default `info@blueharboradvisory.com`) |

Until the domain is verified, leave `RESEND_FROM` unset: Resend's test sender
(`onboarding@resend.dev`) only delivers to the email address of the Resend
account itself, so real enquiries to `info@…` will not arrive until the domain
is verified and `RESEND_FROM` is set.

**Fallback (no setup needed):** if the request fails or the key is missing, the
form opens the visitor's email client with the message pre-filled and addressed
to `info@blueharboradvisory.com`, so no enquiry is silently lost.

## 5b. Logo

The nav and footer use the BlueHarbor Advisory Design System's logo (the
wave-and-sun emblem + "Blueharbor Advisory" wordmark, navy `#0A2363` +
gold `#D6AA56`), inlined as SVG so it's crisp at any size with no extra
request. It's loaded from `assets/brand/logo-full-on-light.svg` by
`tools/build.py` — to swap in a revised logo, replace that file (and
`assets/brand/logo-mark.svg`, the icon-only emblem used for JSON-LD) and
re-run the build.

The delivered logo kit included more variants than the site currently uses
(a reverse/white-on-dark lockup, navy-only and white-only emblem/wordmark
versions). Since every section of the site shares one light background,
only the on-light lockup and the plain emblem are wired in; the rest are
kept in `assets/brand/kit/` in case a future dark section, a letterhead, or
a social template needs them (it also holds the kit's raw PNG exports and
a square `social-avatar.png` for social profile use).
`assets/brand/og-image.png` (the link-preview image) is composed from the
kit's reverse lockup (`logo-full-on-dark.svg`) on the brand navy gradient.

## 6. Open items before this goes live

Carried over from the client's design brief — **do not treat these as
finished**:

- **Exact office address / map pin.** See §4 — the map currently centres on
  Ntinda generally.
- **Contact form delivery.** See §5 — add `RESEND_API_KEY` (and verify the sending domain) in Vercel.
- **Privacy notice & terms.** `/privacy.html` and `/terms.html` contain
  clearly-marked placeholder drafts for structure only — they are **not**
  legal advice and have not been reviewed by counsel. Have Ugandan legal
  counsel review and approve final wording, and confirm any regulatory
  licence/registration statement the firm wants in the footer.
- **Domain.** Metadata, the sitemap and JSON-LD assume
  `https://blueharboradvisory.com`. Update `site.domain` in
  `content/site-content.json` if the live domain differs, then rebuild.
- **About page photo & service card photos.** `assets/about/about-team.jpg`
  and the three images in `assets/services/` (`transaction-advisory.jpg`,
  `development-finance.jpg`, `corporate-finance.jpg`) are **temporary
  stand-ins**, not the client's own photography. See the licensing note
  in §10 — all four are CC-licensed stock photos that carry an attribution
  requirement for as long as they're live; swap them for the firm's own
  images (or properly licensed stock) before launch, keeping the same
  filenames and roughly the same crop (4:3 for the About photo, 3:2 for
  the service cards), then re-run the build.

## 7. Deployment

Any static host works. A few options:

- **Vercel / Netlify:** connect the repository, leave the build command
  empty (there is nothing to build), and set the output directory to the
  repository root.
- **GitHub Pages:** enable Pages on this repository (Settings → Pages →
  deploy from branch), serving from the root of the default branch.
- **Any other static host / CDN:** upload the repository contents as-is.

There is no environment variable, database or server process required for
the site to work. (Only the contact-form email delivery in §5 depends on an
external key, and even that has a working fallback without one.)

## 8. Accessibility, SEO & performance notes

- Semantic landmarks, a skip-to-content link, and visible focus rings
  throughout.
- The services accordion and "who we support" tabs are fully keyboard
  operable (arrow keys move between tabs, per WAI-ARIA tabs pattern).
- `prefers-reduced-motion` is respected everywhere — all reveal/scroll
  animation is skipped and content shows in its final state immediately.
- Every page has a unique `<title>`, meta description, canonical URL,
  Open Graph/Twitter card tags, and JSON-LD (`FinancialService` on every
  page).
- `sitemap.xml` and `robots.txt` are generated alongside the HTML.
- No layout-shifting web fonts block render longer than necessary; the
  Google Fonts stylesheet is preconnected. Images are served at their
  natural size with `loading="lazy"` below the fold.

## 9. Project structure

```
index.html, about.html, services.html, experience.html,
contact.html, privacy.html, terms.html, 404.html               ← generated pages
services/*.html                                                ← generated service detail pages
css/styles.css                                                  ← shared stylesheet (design tokens + components)
js/main.js                                                      ← shared behaviour (nav, reveals, form, map)
assets/brand/      the firm's real logo kit — see note below
assets/brand/kit/  every lockup/variant from the delivered logo kit (bonus, not all wired into the HTML)
assets/icons/      UI icon set (SVG)
assets/hero/       hero "harbour chart" illustration (SVG)
assets/team/       team portraits (JPG) — unused since the team section was removed; kept in case it returns
content/site-content.json                                      ← single source of truth for all copy
design-system/tokens.css, theme.css                             ← original design tokens from the handoff pack (reference)
prototype/index.html                                             ← the originally approved visual prototype (reference only)
DESIGN_BRIEF.md                                                  ← the original design/build brief from the handoff pack (reference)
tools/build.py                                                  ← static site generator — run this after editing content
sitemap.xml, robots.txt, site.webmanifest                       ← generated
```

## 10. Credits

Design, copy and brand assets: BlueHarbor Advisory Limited design handoff
pack. Fonts: [Figtree](https://fonts.google.com/specimen/Figtree) and
[Newsreader](https://fonts.google.com/specimen/Newsreader) via Google
Fonts.

**Temporary photos** (`assets/about/`, `assets/services/`, cropped from the
originals — see §6, replace before launch):
- `about-team.jpg` — team meeting photo supplied by the client
  (source/licence to be confirmed by the client).
- `transaction-advisory.jpg` — coffee-plant photo supplied by the client
  (source/licence to be confirmed by the client).
- `development-finance.jpg` — container port photo supplied by the client
  (source/licence to be confirmed by the client).
- `corporate-finance.jpg` — skyscrapers photo supplied by the client
  (source/licence to be confirmed by the client).
