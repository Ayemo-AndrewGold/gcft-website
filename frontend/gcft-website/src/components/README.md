# Hero Section Components

This directory contains the Header and Hero section components for the Chingtok Ishaku Ministries website.

## Components

### HeroSection
The main component that provides a full-screen hero section with video background and integrated header navigation.

```tsx
import { HeroSection } from '@/components';

<HeroSection 
  videoSrc="/hero-video.mp4" 
  posterSrc="/hero-poster.jpg"
/>
```

**Props:**
- `videoSrc` (string, required): Path to the hero video file
- `posterSrc` (string, optional): Path to the poster image shown while video loads
- `navLinks` (NavLink[], optional): Custom navigation links (defaults to ministry navigation)

**Structure:**
- **Layer 0**: Video background (z-0)
- **Layer 10**: Dark gradient overlay (z-10) 
- **Layer 50**: Fixed header navigation (z-50, h-20)
- **Layer 20**: Hero content with pt-20 to avoid header overlap (z-20)

### Header
Transparent header component that can be used standalone or as part of HeroSection.

**Features:**
- Transparent background overlaying video
- Logo with cross icon and two-line text lockup
- Horizontal navigation on desktop (≥1024px)
- Hamburger menu on mobile
- "Watch Now" CTA button
- Accepts `className` prop for positioning

**Props:**
- `navLinks` (NavLink[], required): Navigation links array
- `className` (string, optional): Additional CSS classes

## Key Architecture

The critical fix implemented ensures **no text overlap**:

1. **Header** is fixed to the top (z-50) in its own layer
2. **Hero content** starts at `pt-20` to account for the 20-unit-high header
3. Both use identical horizontal padding (`px-6 sm:px-8 lg:px-12`) for alignment
4. Navigation links and headline text are in completely separate containers

This structure guarantees the navigation bar sits in a clean strip at the top, with "Encounter God. Be" starting well below it.

## Typography

The components use a mixed typography approach:
- **Headlines**: Playfair Display serif font for elegance and impact
- **Body text**: Geist Sans for readability and modern feel
- **Monospace**: Geist Mono for code elements

## Color Palette

- **Background**: Near-black (#0a0e1a) for dramatic effect
- **Text**: White and gray-200 for contrast and hierarchy
- **Accent**: Gold/Amber (#e5b93c) for emphasis and branding
- **Overlay**: Black with opacity for video readability

## Accessibility

- Semantic HTML5 elements (`<header>`, `<nav>`, `<section>`)
- ARIA labels on icon-only buttons
- Proper contrast ratios for text readability
- Reduced motion support for animations
- Keyboard navigation support

## Performance

- Video preload="auto" for above-the-fold content
- Optimized for Core Web Vitals
- Responsive images and video
- Efficient CSS animations
- Proper z-index layering

## File Requirements

Place these files in your `/public` directory:
- `hero-video.mp4`: Hero background video (recommended: 1080p, under 5MB, 10-30s loop)
- `hero-poster.jpg`: Fallback image while video loads

## Responsive Breakpoints

- Mobile: < 1024px (hamburger menu, stacked content)
- Desktop: ≥ 1024px (horizontal nav, optimized layout)
- Large screens: Proper scaling for 4K+ displays

## Customization

All styling uses Tailwind CSS classes and can be customized through:
1. Tailwind configuration for colors, fonts, and spacing
2. Component props for content and links
3. CSS custom properties for theme variables

## Browser Support

- Modern browsers with video element support
- Fallback poster image for slow connections
- Progressive enhancement approach