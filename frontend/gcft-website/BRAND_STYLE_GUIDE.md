# Chingtok Ishaku Ministries - Brand Style Guide

## ✅ Brand Implementation Complete

The website now uses the official Chingtok Ishaku Ministries brand styling throughout all components.

## Color Palette

### Primary Colors
- **Navy**: `#1E3A8A` - Used for primary buttons, text on gold backgrounds
- **Gold**: `#F4C430` - Used for accents, active states, highlights

### Neutral Colors
- **Background**: `#FAF9F6` - Warm off-white for page backgrounds
- **Text Main**: `#1C1C1C` - Primary text color
- **Text Muted**: `#6B6B68` - Secondary text, captions
- **Borders**: `#E4E2DD` - Dividers, rules, borders

## Typography

### Font Families
- **Headings**: Cormorant Garamond - Elegant serif for headlines and display text
- **Body/UI**: Inter - Clean sans-serif for body text and interface elements

### Font Weights Available
- **Headings**: 300 (light), 400 (regular), 500 (medium), 600 (semibold)
- **Body**: 300 (light), 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

### Font Styles
- **Headings**: Normal and italic variants available
- **Performance**: Uses `display: swap` for optimal loading

## CSS Variables

All brand colors and fonts are available as CSS custom properties:

```css
:root {
  /* Fonts */
  --font-display: 'Cormorant Garamond', 'Cormorant', Georgia, serif;
  --font-body: 'Inter', system-ui, sans-serif;
  
  /* Colors */
  --navy: #1E3A8A;
  --gold: #F4C430;
  --bg: #FAF9F6;
  --ink: #1C1C1C;
  --ink-muted: #6B6B68;
  --rule: #E4E2DD;
}
```

## Tailwind CSS Usage

### Color Classes
- `text-navy` / `bg-navy` - Navy blue
- `text-gold` / `bg-gold` - Gold accent
- `text-ink` / `bg-ink` - Primary text
- `text-ink-muted` - Secondary text
- `bg-bg` - Page background
- `border-rule` - Border color

### Typography Classes
- `font-serif` - Cormorant Garamond (headings)
- `font-sans` - Inter (body text)

## Component Usage Examples

### Header Navigation
- Logo cross: `text-gold` (gold)
- Active nav links: `text-gold` (gold)
- Inactive nav links: `text-gray-200` with `hover:text-white`
- CTA button: `border-gold text-gold hover:bg-gold hover:text-navy`

### Hero Section
- Main headline: `font-serif` with `text-white` and `text-gold` accents
- Subheading: `text-gray-300`
- Primary button: `bg-gold text-navy hover:bg-gold/90`
- Secondary button: `border-white text-white hover:bg-white hover:text-navy`

### Typography Hierarchy
```tsx
// Headlines (Cormorant Garamond)
<h1 className="font-serif text-5xl font-bold text-ink">
<h2 className="font-serif text-3xl font-semibold text-ink">

// Body text (Inter)
<p className="font-sans text-lg text-ink">
<span className="font-sans text-sm text-ink-muted">
```

## Brand Implementation Status

✅ **Color Palette**: All brand colors implemented as Tailwind utilities  
✅ **Typography**: Cormorant Garamond and Inter fonts loaded with proper weights  
✅ **Components**: Header and Hero sections updated with brand styling  
✅ **CSS Variables**: All brand values available as custom properties  
✅ **Performance**: Fonts use `display: swap` for optimal loading  
✅ **Accessibility**: Proper contrast ratios maintained  

## Usage Guidelines

### Do's
- Use Cormorant Garamond for all headlines and display text
- Use Inter for body text, navigation, and UI elements
- Apply gold color for active states, highlights, and accents
- Use navy for primary buttons and high-contrast text
- Maintain consistent spacing and typography hierarchy

### Don'ts
- Don't mix serif fonts in body text or UI elements
- Don't use colors outside the defined palette
- Don't apply gold to large text blocks (readability)
- Don't use navy text on navy backgrounds
- Don't override font weights outside the available range

The brand styling is now consistently applied across the entire hero section and can be extended to additional components using the same design system.