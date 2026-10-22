# BlueHarbor Advisory Limited — Website

The production marketing website for **BlueHarbor Advisory Limited**, an
investment advisory and corporate finance firm based in Ntinda, Kampala,
Uganda. It is a complete, dependency-free static website: every page is a
plain HTML file, styled by one shared stylesheet and one shared script, so
it runs anywhere — a laptop, GitHub Pages, Netlify, Vercel, or any ordinary
web host — with no build step, server, framework or install required.

The design, copy and assets are taken from the approved design handoff
pack supplied by the client (prototype, design tokens, icons, brand assets,
team photos and `content/site-content.json`, the firm's own company
profile). Nothing on the site has been invented: no stats, client logos,
testimonials or deal counts, per the firm's compliance guidance.

## 1. What's in the site

| Route | Description |
|---|---|
| `/` | Home — the full one-page design (hero, about, services, approach, market orientation, why BlueHarbor, experience, purpose & principles, team, contact). |
| `/about.html` | About, who we support, market orientation, purpose & principles, why BlueHarbor. |
| `/services.html` | Overview of the three service pillars + engagement approach. |
| `/services/corporate-finance.html` | Corporate Finance & Enterprise Advisory detail page. |
| `/services/transaction-advisory.html` | Investment & Transaction Advisory detail page. |
| `/services/development-finance.html` | Development Finance & Programme Advisory detail page. |
| `/experience.html` | Experience & capabilities, with the required disclaimer. |
| `/team.html` | Team grid; each card opens an accessible bio dialog. |
| `/contact.html` | Contact form, contact details and an embedded Google Map. |
| `/privacy.html`, `/terms.html` | Legal pages. **Placeholder copy — see §6.** |
| `/404.html` | Not-found page. |

Every page shares `css/styles.css` and `js/main.js`, so behaviour (mobile
menu, scroll reveals, the services accordion, audience tabs, the team bio
dialog, the contact form, back-to-top, reduced-motion support) is
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
`services_accordion`, `team_section`, etc.) and re-run it the same way.

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

## 5. Making the contact form actually send email

The form (`#contactForm`, in `js/main.js`) already does full client-side
validation, matches the approved design, and is wired to work two ways:

### Option A — Web3Forms (recommended, free, 5 minutes, no backend)

[Web3Forms](https://web3forms.com) delivers form submissions straight to an
inbox with no server of your own.

1. Go to <https://web3forms.com> and enter the inbox that should receive
   enquiries (e.g. `info@blueharboradvisory.com`). You'll get a free
   **Access Key** by email — no account required.
2. Open `tools/build.py`, find this line inside `contact_section(...)`:
   ```python
   data-access-key="YOUR_WEB3FORMS_ACCESS_KEY"
   ```
   and replace `YOUR_WEB3FORMS_ACCESS_KEY` with the real key.
3. Re-run `python3 tools/build.py` and redeploy.

That's it — submissions will POST to Web3Forms' API and arrive by email,
with the subject `New mandate enquiry — {type} — {service}`. Web3Forms'
free tier includes spam filtering and a honeypot; no code changes needed.

### Option B — a form backend you already use (Formspree, Basin, etc.)

Swap the `fetch('https://api.web3forms.com/submit', …)` call in
`js/main.js` (`Contact form` section) for your provider's endpoint — most
work the same way (POST a `FormData`, get back JSON).

### Option C — a serverless function (full control)

If the firm wants submissions written to a database, forwarded to Slack,
etc., replace the fetch target with your own endpoint (e.g. a Vercel/Netlify
function, or a small Node/Express route) that sends mail via
[Resend](https://resend.com), SendGrid, or SMTP. This is closer to what the
original design brief specified (a Next.js Server Action + Resend) — it
requires a bit of backend code and a domain verified for sending, which is
why Option A is the faster path to "fully working" today.

### Fallback behaviour (works right now, with zero setup)

Until an access key is configured (or if the network request fails), the
form automatically falls back to opening the visitor's email client with a
pre-filled message addressed to `info@blueharboradvisory.com` — so no
enquiry is ever silently lost, even before Option A/B/C is wired up.

## 6. Open items before this goes live

Carried over from the client's design brief — **do not treat these as
finished**:

- **Official logo.** `assets/brand/` currently holds a placeholder mark (a
  teal rounded square with a sail/wave motif) and placeholder favicons/OG
  image. Replace the files in `assets/brand/` with the firm's real logo
  (keeping the same filenames) once available.
- **Exact office address / map pin.** See §4 — the map currently centres on
  Ntinda generally.
- **Contact form delivery.** See §5 — pick Option A, B or C and configure it.
- **Team photos.** Emmanuel Opendi's portrait was supplied as an oval,
  edge-filled crop; a reshoot on a neutral background is recommended for
  consistency with the other three.
- **Privacy notice & terms.** `/privacy.html` and `/terms.html` contain
  clearly-marked placeholder drafts for structure only — they are **not**
  legal advice and have not been reviewed by counsel. Have Ugandan legal
  counsel review and approve final wording, and confirm any regulatory
  licence/registration statement the firm wants in the footer.
- **Domain.** Metadata, the sitemap and JSON-LD assume
  `https://blueharboradvisory.com`. Update `site.domain` in
  `content/site-content.json` if the live domain differs, then rebuild.

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

- Semantic landmarks, a skip-to-content link, visible focus rings, and a
  focus-trapping `<dialog>` for team bios (closes on <kbd>Esc</kbd> or
  backdrop click).
- The services accordion and "who we support" tabs are fully keyboard
  operable (arrow keys move between tabs, per WAI-ARIA tabs pattern).
- `prefers-reduced-motion` is respected everywhere — all reveal/scroll
  animation is skipped and content shows in its final state immediately.
- Every page has a unique `<title>`, meta description, canonical URL,
  Open Graph/Twitter card tags, and JSON-LD (`FinancialService` on every
  page; a `Person`/`ItemList` block on the team page).
- `sitemap.xml` and `robots.txt` are generated alongside the HTML.
- No layout-shifting web fonts block render longer than necessary; the
  Google Fonts stylesheet is preconnected. Images are served at their
  natural size with `loading="lazy"` below the fold.

## 9. Project structure

```
index.html, about.html, services.html, experience.html,
team.html, contact.html, privacy.html, terms.html, 404.html   ← generated pages
services/*.html                                                ← generated service detail pages
css/styles.css                                                  ← shared stylesheet (design tokens + components)
js/main.js                                                      ← shared behaviour (nav, reveals, form, map, dialog)
assets/brand/      logo, favicons, OG image
assets/icons/      UI icon set (SVG)
assets/hero/       hero "harbour chart" illustration (SVG)
assets/team/       team portraits (JPG)
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
