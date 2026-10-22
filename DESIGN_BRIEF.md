# BlueHarbor Advisory — Website Build Brief

You are building the production marketing website for **BlueHarbor Advisory Limited**, an investment advisory and corporate finance firm in Ntinda, Kampala, Uganda.

This folder contains everything you need:

| Path | What it is |
|---|---|
| `prototype/index.html` | **Approved visual design.** A self-contained, high-fidelity prototype (open it in a browser). Match its look, spacing, motion and interactions. Treat it as the design source of truth. |
| `content/site-content.json` | **All copy**, taken word for word from the client's company profile. Use it as the single content source. Do not rewrite or invent copy. |
| `design-system/tokens.css` | Every design token (colour, type, radius, shadow, motion, layout), extracted from the prototype. |
| `design-system/theme.css` | The same tokens as a Tailwind v4 `@theme` block. Paste it into `globals.css`. |
| `assets/icons/*.svg` + `icons.json` | All 15 UI icons used in the prototype, as exact SVGs. `icons.json` maps each icon to where it is used and its stroke width. |
| `assets/brand/` | `logo-mark.svg`, `logo-full-on-dark.svg`, `logo-full-on-light.svg`, `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `og-image.png` (1200×630). |
| `assets/hero/harbour-chart.svg` | The hero contour chart (11 contours, dotted course line, 4 waypoints). |
| `assets/team/*.jpg` | Team portraits, cropped to 4:5 at 640×800. |
| `CLAUDE.md` | This brief. |

**Use every asset in this pack as supplied.** Do not substitute icon libraries, recolour assets or introduce colours outside the tokens. The audit in §11 confirms the prototype uses all 30 tokens, all 15 icons, all brand assets and every line of the client brief.

---

## 1. Goals

1. A modern, credible, calm website for an advisory firm. It should feel more like a boutique investment bank than a startup.
2. Cover **everything in the brief**: about, audiences, market orientation, purpose and principles, three service pillars, engagement approach, experience and capabilities (with its disclaimer), why BlueHarbor, team, and contact.
3. Turn visitors into enquiries. The main action across the site is **"Discuss a mandate"**, which leads to the contact form.
4. Fast, accessible and SEO-ready: Lighthouse ≥ 95 in every category on mobile.

## 2. Non-negotiable content rules (compliance)

The client wrote this profile carefully. Keep these rules:

- **Do not invent** stats, deal counts, AUM figures, client logos, testimonials, case studies or "trusted by" strips. The firm deliberately makes no such claims.
- The Experience section **must** show this disclaimer verbatim, next to the list: *"The areas below describe relevant team experience and service capabilities; they are not represented as transactions completed or contracted by BlueHarbor itself."* (On the page it can say "above" if it sits under the list.)
- Keep the **Operating principle** statement and the line in Transaction Advisory: *"introductions are distinguished from advisory and execution services."*
- Footer legal line: *"Nothing on this website constitutes an offer of securities or investment advice to any person."*
- Use British/Ugandan English spelling throughout (organisation, programme, judgement, recognised).
- Team qualifications must be shown exactly as written. "In progress" and "candidate" stay as they are.

## 3. Tech stack

- **Next.js 15 (App Router) + TypeScript**, static-first (SSG). Deploy to **Vercel**.
- **Tailwind CSS v4**. Put the design tokens from §5 in `@theme` in `globals.css`.
- **next/font/google**: `Figtree` (400/500/600/700) and `Newsreader` (italic 400/500, opsz axis).
- **Motion**: `motion` (Framer Motion) for reveal-on-scroll and the hero contour draw. Respect `prefers-reduced-motion`.
- **Contact form**: a Server Action, validated with `zod`, that sends email via **Resend** to `info@blueharboradvisory.com`. Add a honeypot field and basic rate limiting. Env vars: `RESEND_API_KEY`, `CONTACT_TO`, `CONTACT_FROM`.
- **Icons**: the exact SVGs in `assets/icons/`. Do **not** use lucide or another library. Build a typed `<Icon name="globe" />` component (or import the files with SVGR). Each icon is drawn on a 24×24 grid with `stroke="currentColor"`, so its colour comes from CSS. Keep the stroke widths given in `icons.json`.
- No CMS for v1. Content comes from `content/site-content.json`, imported through a typed `lib/content.ts`.

## 4. Information architecture

Multi-page for SEO. The home page summarises everything and links deeper.

```
/                      Home (prototype = this page, full length)
/about                 About + Who we support + Market orientation + Purpose & principles + Why BlueHarbor
/services              Overview of 3 pillars + Approach
/services/[slug]       corporate-finance | transaction-advisory | development-finance
/experience            Experience & capabilities (+ disclaimer)
/team                  Team grid; each card opens a bio dialog (also /team/[slug] for shareable URLs, optional)
/contact               Contact form + details + map
/privacy, /terms       Simple legal pages (placeholder copy, clearly marked for client review)
```

The primary nav is About · Services · Approach · Experience · Team, with a **Discuss a mandate** button. On the home page the nav links scroll to their sections. On inner pages they go to the routes above.

### Home page section order (matches prototype)
1. **Hero**: dark navy. Eyebrow, H1 "Navigating growth. / *Empowering success.*", lead text, two CTAs, animated contour-line "harbour chart" with a dotted course through 4 waypoints (Define → Evaluate → Prepare → Support), and a coordinate label `0°21′N · 32°37′E — NTINDA, KAMPALA`. A bottom bar shows the 3 market-orientation facts.
2. **About + Who we support**: about copy on the left. On the right, a tabbed card (Enterprises / Investors / Institutions). Each tab shows its audience and the matching service pillar.
3. **Services**: accordion with 3 numbered pillars. The first is open by default. Deliverables show as chips.
4. **Approach**: dark. A 4-step horizontal timeline whose progress line fills on scroll (vertical on mobile), plus the Operating principle card.
5. **Market orientation**: 3 cards. Sectors show as chips.
6. **Why BlueHarbor**: mist background. 3 columns with roman-numeral indexes.
7. **Experience & capabilities**: table rows with region tags, plus the disclaimer.
8. **Purpose & principles**: navy. Mission and Vision in large serif on the left, 3 value cards on the right.
9. **Team**: 4 portrait cards. Clicking a card opens an accessible `<dialog>` with the bio and qualifications.
10. **Contact**: dark. Details on the left with an embedded **Google Map** below them; form on the right (name, organisation, email, phone, "I am reaching out as" segmented radio, area of interest select, message).
11. **Footer**: logo, tagline, 3 link columns, legal line.

## 5. Design system

### Colour (brand colours sampled from the client's profile document)
| Token | Hex | Use |
|---|---|---|
| `navy-950` | `#0B1C2B` | Darkest sections (approach, contact, footer) |
| `navy-900` | `#0F2537` | Hero gradient |
| `navy` | `#17334D` | **Brand primary**: headings on light, Purpose section |
| `navy-700` | `#21486A` | Hover / gradient highlight |
| `teal` | `#008C92` | **Brand accent**: buttons, eyebrows, numbers |
| `teal-600` | `#007379` | Button hover |
| `teal-300` | `#4FC2C0` | Accent on dark backgrounds |
| `teal-50` | `#E5F3F3` | Icon tiles |
| `slate` | `#576B7B` | Body copy on light |
| `slate-300` | `#A7B4BF` | Body copy on dark |
| `mist` | `#EDF4F6` | Tinted sections, chips |
| `paper` | `#F7FAFB` | Page background |
| `ink` | `#0F1E2B` | Strong body text |
| `white` | `#FFFFFF` | Text on dark, cards, inputs on focus |
| `danger` | `#B42318` | Form validation errors only |
| `line` | `rgba(23,51,77,.12)` | Borders on light |
| `line-dark` | `rgba(255,255,255,.12)` | Borders on dark |

The site is light-first, with dark "anchor" sections alternating for rhythm. There is no dark-mode toggle in v1.

### Typography
- **Sans (UI + headings):** Figtree. Headings are weight 600 with tracking −0.02em to −0.035em. If the client licenses **Gill Sans Nova** (their document font), swap it in as the sans font. The layout is designed to tolerate it.
- **Serif accent:** Newsreader italic, used only for the *second half of headings* ("…*for capital decisions.*"), Mission and Vision statements, and service numbers. Do not overuse it.
- Scale (fluid with `clamp`): H1 42→82px · H2 32→52px · H3 21→25px · lead 18→20px · body 17px · eyebrow 12.5px uppercase, +0.16em tracking, with a 22px rule before it.

### Layout and shape
- Container 1200px. Gutter `clamp(16px,4vw,40px)`. Section padding `clamp(72px,10vw,136px)`.
- Radii: `sm` 12px (inputs, icon tiles) · `md` 14px (callouts) · `lg` 22px (cards, form, dialog) · `pill` 999px (buttons, chips, tabs). Buttons are 50px tall (44px in the nav).
- Shadows: `sm` · `md` · `lg`, all navy-tinted. Exact values are in `tokens.css`.
- Alpha tints such as `rgba(0,140,146,.14)` are transparent versions of the tokens. They are listed at the bottom of `theme.css`.
- Breakpoints: ≤300 · ≤360 · ≤520 · ≤599 · 600–900 · ≤980 (nav collapses) · ≤1024 (team becomes 2 columns) · ≥1600 · ≥2200, plus a short-landscape query and foldable segment queries. See §5b.

### Logo
The client's profile contained no logo file, so `assets/brand/` holds a **placeholder mark**: a teal rounded square with a sail and two waves, next to the stacked wordmark "BLUEHARBOR / ADVISORY". Use `logo-full-on-dark.svg` in the header and footer and `logo-full-on-light.svg` on light backgrounds. Use `favicon.svg`, `favicon-32.png` and `apple-touch-icon.png` in `app/` metadata, and `og-image.png` as the default OpenGraph and Twitter image. The SVG wordmarks use live text, so convert the text to outlines, or rebuild the wordmark in JSX with Figtree, for consistent rendering. If the client supplies an official logo later, replace these files and keep the filenames.

### Hero chart
`assets/hero/harbour-chart.svg` is the exact artwork. Inline it as a React component so the contour paths can animate (stroke-dashoffset draw-in, staggered 120ms) and the first and last waypoints can pulse. Keep the `0°21′N · 32°37′E — NTINDA, KAMPALA` label.

### Motion (scroll-driven; mirror exactly)
Every effect animates only `transform` and `opacity`, and uses `cubic-bezier(.2,.7,.2,1)`. Reveal styles apply only under `html.js`, so content is never hidden if JS fails.

| Effect | Where | Behaviour |
|---|---|---|
| Scroll progress bar | Top of the viewport | 2px `teal-300` bar, `scaleX` = page scroll progress |
| Headline word reveal | Hero H1 and every section H2 | Words rise out of a mask, 55ms stagger, 1s. The serif span and `<br>` are preserved, and the heading keeps an `aria-label` with the full text |
| Eyebrow rule | All eyebrows | The 22px rule draws left to right as the eyebrow reveals |
| Hero parallax | Hero | As the hero scrolls away (`--hp` 0→1), the copy drifts down 70px and fades 80%, and the chart drifts up 60px, rotates 8° and scales 1.08 |
| Hero chart draw | Hero | Contours draw in on load, 120ms stagger; first and last waypoints pulse |
| Reveal variants | Most blocks | `up` 24px (default) · `left` (mission/vision, contact details) · `right` (audience card, values, form) · `scale` .95 (market cards). 0.9s, staggered 80ms with `data-d` |
| Chip stagger | Sector chips, service deliverables | Chips rise 8px in turn, 45ms apart, when the card reveals or a service opens |
| Rule draw | Why-items (top rule), experience rows (bottom rule) | Lines draw left to right, 1.2s |
| Approach timeline | Approach | **Scroll-scrubbed**: the progress line tracks scroll position and each step lights up as the line reaches it |
| Mission/vision read-along | Purpose section | Words go from 22% to 100% opacity, scrubbed to scroll |
| Team photo settle | Team cards | Photo eases from scale 1.14 to 1 over 1.6s on reveal; hover zooms to 1.04 on pointer devices only |
| Back-to-top | Floating button, bottom right | Appears after 1.2 viewports of scroll, respects safe areas, smooth-scrolls to the top |

Implementation in Next.js: use `motion` (`useScroll`, `useTransform`, `whileInView` with `viewport={{ once: true, margin: "0px 0px -6% 0px" }}`) or one rAF-throttled scroll listener, as the prototype does. Do not attach a scroll listener per component.
**Reduced motion:** no splitting, no parallax, no scrubbing, and every element shows in its final state. **Print:** all content visible, with the nav, map and form hidden.

## 5b. Device support (must pass)

| Class | Test viewports (CSS px) | Key adaptations |
|---|---|---|
| Fold cover screens | 280×653, 344×882 | 14px gutter, H1 32–40px, smaller wordmark, full-width CTAs, compact tabs and accordion, long emails wrap |
| Phones / Z Flip | 360×780, 375×667, 393×852, 402×874, 440×956 | Stacked layouts, 44px minimum tap targets, bio dialog becomes a bottom sheet |
| iPhone notch / Dynamic Island | All iPhones | `viewport-fit=cover`; `env(safe-area-inset-*)` on container, mobile menu, footer and back-to-top |
| Landscape phones | 874×402 | Compact hero and 64px nav; menu scrolls within `100dvh` |
| Unfolded foldables / small tablets | 690×838, 744×1133, 820×1180 | 2-column market, why and value grids; 3-column hero facts from 700px; chart labels hidden behind text |
| Dual-screen spanning | `horizontal-viewport-segments: 2` | Hero, about, contact and purpose grids split exactly at the hinge using `env(viewport-segment-*)` |
| Tablets landscape / laptops | 1180×820, 1280×800, 1366×1024 | Full nav from 981px, 2-column hero |
| Large screens | 1920×1080, 2560×1440 | Container 1320px (≥1600) / 1480px (≥2200), 18px body |

General rules:
- Use `100dvh`, not `vh`.
- Hover effects only under `(hover:hover)`. Touch devices get a press `scale(.97)` instead.
- Inputs are ≥16px so iOS does not zoom on focus.
- Lock body scroll while the menu or dialog is open.
- Close the mobile menu automatically when the viewport widens past 980px (tablet rotation, fold opening).
- **Acceptance:** zero horizontal scroll on every viewport above. This was verified on the prototype.

## 6. Components to build

`ScrollProgress` · `BackToTop` · `SplitHeading` · `Reveal` (variants up/left/right/scale) · `SiteHeader` (transparent over the hero, blurred navy after 24px of scroll, mobile sheet menu) · `Eyebrow` · `SectionHeading` (sans + serif split) · `Button` (primary / ghost / outline) · `HeroChart` (SVG contours generated from a seeded function, so make it a component) · `AudienceTabs` (ARIA tabs with arrow-key navigation) · `ServiceAccordion` (uses `aria-expanded` and a grid-rows animation) · `ApproachTimeline` · `MarketCard` · `WhyItem` · `ExperienceRow` · `Disclaimer` · `ValueCard` · `TeamCard` + `BioDialog` · `ContactForm` · `MapEmbed` · `SiteFooter`.

## 7. Accessibility and SEO

- WCAG 2.2 AA. Every interactive element must be reachable by keyboard and show a visible teal focus ring. Include a skip link. The dialog traps focus and closes on Esc.
- Portrait alt text: "Portrait of {name}".
- Metadata for every route. Add OpenGraph images (navy background with the wordmark and tagline). Add JSON-LD: `ProfessionalService` / `FinancialService` with address (Ntinda, Kampala, UG), telephone and email, plus `Person` entries for the team.
- Include `sitemap.xml`, `robots.txt`, a canonical domain `https://blueharboradvisory.com`, and `en-UG` as the language.

## 8. Contact form behaviour

- Fields: name\*, organisation, email\*, phone, type (Enterprise | Investor | Institution), service (3 pillars + "Not sure yet"), message\*.
- Validate on the client and the server. Show inline errors as in the prototype. Show the success message in place, without a redirect.
- Pre-select the service when the user arrives from a service page (`/contact?service=transaction-advisory`).
- Email subject: `New mandate enquiry — {type} — {service}`.

## 8b. Google Maps widget (Contact section and `/contact`)

- Use the keyless Google Maps embed, so no API key or billing is needed:
  `https://www.google.com/maps?q={MAP_QUERY}&z=15&output=embed`, with `MAP_QUERY = "Ntinda, Kampala, Uganda"` stored in `site-content.json` as `site.contact.mapQuery`. If the client later wants a styled or interactive map, switch to the Maps Embed API (`/maps/embed/v1/place`) with `NEXT_PUBLIC_GOOGLE_MAPS_KEY`.
- `MapEmbed` component: rounded `lg` card with a `line-dark` border on a `navy-900` background. The iframe is 260px tall (220px at ≤560px) and uses `loading="lazy"`, `referrerpolicy="no-referrer-when-downgrade"`, `allowfullscreen`, and the title "Map showing BlueHarbor Advisory in Ntinda, Kampala". Apply a subtle CSS filter (`grayscale(.35) contrast(1.05) saturate(.9)`) so it sits with the palette.
- Below the map, a bar shows the address on the left and a **Get directions** link on the right (`arrow-right` icon, `teal-300`). The link goes to `https://www.google.com/maps/dir/?api=1&destination=Ntinda%2C+Kampala%2C+Uganda` and opens in a new tab with `rel="noopener"`.
- Performance: load the iframe only when it scrolls near the viewport (lazy, or click-to-load if Lighthouse drops). Add `frame-src https://www.google.com` to the CSP.

## 9. Open items for the client (show these as TODO comments, never as fake content)

- Official logo files (SVG). The supplied mark, favicon and OG image are placeholders.
- Licence for Gill Sans Nova, if they want exact brand typography.
- Higher-resolution, consistent portraits. Emmanuel's photo came from an oval crop and was edge-filled, so a reshoot on a neutral grey background is recommended.
- Exact office address or Google Maps pin for Ntinda. The map currently centres on the Ntinda area, so update `MAP_QUERY` once the exact pin is confirmed.
- Privacy notice and terms wording. Confirm any regulatory licence or registration statement they want in the footer.
- Domain and email (`blueharboradvisory.com`) DNS access for Resend.

## 10. Definition of done

- [ ] Home page matches `prototype/index.html` on every viewport in §5b, with no horizontal scroll.
- [ ] All scroll animations in the Motion table are implemented, and degrade correctly with reduced motion and with no JS.
- [ ] All routes in §4 exist and are populated only from `site-content.json`.
- [ ] Compliance rules in §2 are all met.
- [ ] The contact form delivers email end-to-end on Vercel preview.
- [ ] Lighthouse mobile ≥ 95 in every category, and axe reports no violations.
- [ ] Reduced-motion is respected, and the dialog and tabs work fully by keyboard.
- [ ] All 30 tokens, 15 icons, brand files, hero chart and 4 portraits from this pack are used; no other colours or icon sets appear.

## 11. Design-system audit (prototype vs this pack)

```
Content: 107/107 brief strings present verbatim in prototype
Tokens: 30/30 used; hard-coded hex outside tokens: 0
Brand colours from profile doc present as tokens: #17334D ✓, #008C92 ✓, #576B7B ✓, #EDF4F6 ✓, #F7FAFB ✓, #FFFFFF ✓
Tailwind theme mirrors every colour token: ✓
Icons: 15 unique in prototype, 15 exported SVGs; missing exports: 0; exported-but-unused: 0
Team photos: 4/4 exported, all 4 embedded in prototype: ✓; content.json paths match files: ✓
Brand assets: apple-touch-icon.png, favicon-32.png, favicon.svg, logo-full-on-dark.svg, logo-full-on-light.svg, logo-mark.svg, og-image.png
Hero chart: 11 contour paths + course line exported (matches prototype: ✓)
```

Re-run the same checks against the built site before handover.

### Suggested first prompt in Claude Code
> Read CLAUDE.md, open prototype/index.html and content/site-content.json. Scaffold the Next.js 15 + Tailwind v4 project described, paste design-system/theme.css into globals.css, copy assets/team to public/team, assets/brand into app/ metadata and public/, and build the Icon component from assets/icons, implement the home page to match the prototype exactly, then build the remaining routes.
