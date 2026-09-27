---
name: Sanctuary Modern
colors:
  surface: '#0e131f'
  surface-dim: '#0e131f'
  surface-bright: '#343946'
  surface-container-lowest: '#090e1a'
  surface-container-low: '#161b28'
  surface-container: '#1a1f2c'
  surface-container-high: '#252a37'
  surface-container-highest: '#303542'
  on-surface: '#dee2f3'
  on-surface-variant: '#d3c5b0'
  inverse-surface: '#dee2f3'
  inverse-on-surface: '#2b303d'
  outline: '#9c8f7c'
  outline-variant: '#4f4536'
  surface-tint: '#f5be4e'
  primary: '#ffd894'
  on-primary: '#412d00'
  primary-container: '#f0b94a'
  on-primary-container: '#684a00'
  inverse-primary: '#7c5800'
  secondary: '#dcc2ab'
  on-secondary: '#3e2d1d'
  secondary-container: '#564332'
  on-secondary-container: '#cab19a'
  tertiary: '#c2e2ff'
  on-tertiary: '#00344f'
  tertiary-container: '#84c9ff'
  on-tertiary-container: '#00547e'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdea6'
  primary-fixed-dim: '#f5be4e'
  on-primary-fixed: '#271900'
  on-primary-fixed-variant: '#5e4200'
  secondary-fixed: '#f9dec5'
  secondary-fixed-dim: '#dcc2ab'
  on-secondary-fixed: '#27190a'
  on-secondary-fixed-variant: '#564332'
  tertiary-fixed: '#cbe6ff'
  tertiary-fixed-dim: '#8fcdff'
  on-tertiary-fixed: '#001e30'
  on-tertiary-fixed-variant: '#004b71'
  background: '#0e131f'
  on-background: '#dee2f3'
  surface-variant: '#303542'
typography:
  display-hero:
    fontFamily: Playfair Display
    fontSize: 56px
    fontWeight: '600'
    lineHeight: 64px
    letterSpacing: -0.02em
  display-hero-mobile:
    fontFamily: Playfair Display
    fontSize: 36px
    fontWeight: '600'
    lineHeight: 44px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Playfair Display
    fontSize: 40px
    fontWeight: '500'
    lineHeight: 48px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 28px
    fontWeight: '500'
    lineHeight: 36px
  headline-md:
    fontFamily: Playfair Display
    fontSize: 28px
    fontWeight: '500'
    lineHeight: 36px
  headline-sm:
    fontFamily: Playfair Display
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 30px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.08em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  margin: 4rem
  margin-sm: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system establishes a warm, sacred, and architectural digital presence. It moves away from clinical modernism or casual church templates, leaning into an editorial, reverent aesthetic reminiscent of candlelit stone sanctuaries and contemplative modern spaces.

- **Tone & Mood:** Dignified, hospitable, contemplative, transcendent. The interface feels immersive, calm, and deliberate.
- **Visual Aesthetic:** Editorial elegance fused with tactile modern depth. Heavy use of full-bleed moody photography, rich vignette falloffs, frosted glass surfaces, and restrained luminous gold accents.
- **Target Audience:** First-time seekers, regular congregation members, and community patrons seeking worship details, sermon archives, giving portals, and fellowship events.

## Colors

The palette is rooted in an atmospheric dark navy-charcoal night sky, warmed by rich candlelit ambers and warm stone creams.

- **Primary (`#F0B94A` - Radiant Gold):** Used intentionally for primary calls-to-action, key accents, focus rings, and luminous active states.
- **Secondary (`#3A2A1A` - Smoked Amber Wood):** A deep, warm undertone utilized for tinted glows, frosted overlays, and elevated depth backing.
- **Neutral Base (`#0F1420` - Midnight Charcoal):** The foundational canvas, providing infinite depth and high-contrast support for imagery.
- **Surface Neutrals:**
  - Base Background: `#0F1420`
  - Elevated Container / Glass Surface: `rgba(21, 28, 44, 0.65)`
  - Elevated Border / Hairline: `rgba(240, 185, 74, 0.15)`
  - Active / Focus Border: `rgba(240, 185, 74, 0.45)`
- **Typography & Content:**
  - Primary Content (Altar Cream): `#FBF9F5`
  - Secondary Content (Muted Linen): `#E2DFD8`
  - Tertiary / Subtle Meta: `#8E95A5`

## Typography

The type hierarchy juxtaposes classical literary beauty with clean, modern legibility.

- **Headlines (`Playfair Display`):** Carries sacred, editorial gravitas. Used for sermon series titles, scripture callouts, page headlines, and hero invitations. Tight tracking and generous line heights ensure an architectural feel.
- **Body & Labels (`Plus Jakarta Sans`):** Balanced, open, and friendly geometry creates an effortless reading experience across high-density sermon notes, event calendars, and form inputs.
- **Uppercase Labels:** Used sparingly for categories, service times, and tags (set with `label-sm` tracking at `0.08em` uppercase) to evoke museum and fine-arts cataloging.

## Layout & Spacing

A 12-column responsive fluid grid anchored by generous outer gutters that preserve open breathing space.

- **Grid Layout:**
  - **Desktop (1024px+):** 12 columns, `margin: 4rem`, `gutter: 1.5rem`. Max container bound at `1320px`.
  - **Tablet (768px - 1023px):** 8 columns, `margin: 2.5rem`, `gutter: 1.25rem`.
  - **Mobile (< 768px):** 4 columns, `margin: 1.25rem`, `gutter-sm: 1rem`.
- **Rhythm & Cadence:** Generous vertical section padding (`space-xl` scaled up to `5rem` for major section transitions) gives every narrative beat room to land.
- **Full-Bleed Bleed-Throughs:** Hero banners and media players stretch edge-to-edge with inner content aligned strictly to the container bounds.

## Elevation & Depth

Depth is established through translucent atmospheric layers rather than heavy drop shadows:

- **Surface Tiers:**
  - **Base Canvas:** Solid `#0F1420`.
  - **Level 1 (Cards, Modules):** Background `rgba(21, 28, 44, 0.65)`, blurred with `backdrop-filter: blur(16px)`, bordered by `1px solid rgba(240, 185, 74, 0.12)`.
  - **Level 2 (Popovers, Navigation Bars, Modals):** Background `rgba(15, 20, 32, 0.85)`, `backdrop-filter: blur(24px)`, bordered by `1px solid rgba(240, 185, 74, 0.22)`.
- **Luminous Highlights:** Subtle radial gradients (`radial-gradient(circle at top, rgba(240, 185, 74, 0.08) 0%, transparent 70%)`) wash behind key cards and hero elements to simulate soft ambient candlelight.
- **Shadows:** Minimal soft diffusions. When required for elevated menus or floating audio bars: `0 12px 32px -8px rgba(5, 8, 14, 0.7)`.

## Shapes

The design system maintains architectural discipline with gentle, understated softness (`roundedness: 1`).

- **Base Radius (0.25rem / 4px):** Form fields, badges, tags, and tertiary controls.
- **Medium Radius (`rounded-lg` / 0.5rem / 8px):** Primary buttons, interactive cards, media player controls, dropdown menus.
- **Large Radius (`rounded-xl` / 0.75rem / 12px):** Modal dialogs, major editorial image containers, frosted hero panels.
- **Avoidances:** Complete pill capsules and bubble shapes are avoided to preserve the dignified, structural aesthetic.

## Components

- **Buttons:**
  - *Primary (Gold Fill):* Background `#F0B94A`, text `#0F1420`, font-weight 600. On hover: background `#F7CA6E` with subtle ambient glow (`0 0 16px rgba(240, 185, 74, 0.3)`).
  - *Secondary (Delicate Wireframe):* Border `1px solid rgba(240, 185, 74, 0.45)`, background transparent, text `#FBF9F5`. On hover: border-color `#F0B94A`, background `rgba(240, 185, 74, 0.08)`.
  - *Ghost / Text:* Warm cream `#E2DFD8` text with subtle gold underline hover transitions.

- **Cards (Sermons, Events, Ministries):**
  - Frosted surface (`rgba(21, 28, 44, 0.65)` with `16px` backdrop blur).
  - Border: `1px solid rgba(240, 185, 74, 0.12)`.
  - Media container includes subtle bottom inner vignette (`linear-gradient(to top, rgba(15, 20, 32, 0.9), transparent)`).
  - Hover: Border shifts to `rgba(240, 185, 74, 0.35)` with an ambient warm halo.

- **Input Fields & Form Elements:**
  - Background: `rgba(15, 20, 32, 0.6)`.
  - Border: `1px solid rgba(226, 223, 216, 0.15)`.
  - Text: `#FBF9F5`, placeholder `#8E95A5`.
  - Focus: Border `#F0B94A`, glow `0 0 0 1px rgba(240, 185, 74, 0.35)`.

- **Tabs & Navigation:**
  - Unselected: Text `#E2DFD8`, transparent background.
  - Active: Text `#FBF9F5`, underlined with a 2px `#F0B94A` accent bar featuring a faint vertical blur halo.
  - Smooth spring or linear easing transitions between tab panels.

- **Checkboxes & Radios:**
  - Base: `1px solid rgba(240, 185, 74, 0.3)`, background `rgba(15, 20, 32, 0.5)`.
  - Checked: Solid `#F0B94A` fill with `#0F1420` checkmark indicator.

- **Skeleton Shimmer (Loading States):**
  - Base gradient: `#151C2C`.
  - Highlight sweep: `linear-gradient(90deg, rgba(21, 28, 44, 0) 0%, rgba(240, 185, 74, 0.08) 50%, rgba(21, 28, 44, 0) 100%)`.

- **Domain-Specific Components:**
  - *Scripture Callout Box:* Italic Playfair Display with left warm-gold border rule (`2px solid #F0B94A`) and subtle parchment-tinted dark background.
  - *Persistent Audio/Media Bar:* Frosted glass dock pinned to bottom viewport with gold scrubber track and minimal playback controls.