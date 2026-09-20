import { HeroSection, NavLink } from '@/components';

// Example 1: Basic usage with default navigation
export function BasicHeroExample() {
  return (
    <HeroSection 
      videoSrc="https://www.instagram.com/reel/DZxediGojDl/?utm_source=ig_web_copy_link&stkn=NTc4MTIwNjQ2YQ=="
    />
  );
}

// Example 2: Custom navigation links
export function CustomNavigationExample() {
  const customNavLinks: NavLink[] = [
    { name: 'Home', href: '/', isActive: true },
    { name: 'About Us', href: '/about' },
    { name: 'Sermons', href: '/sermons' },
    { name: 'Worship', href: '/worship' },
    { name: 'Connect', href: '/connect' },
    { name: 'Donate', href: '/donate' },
  ];

  return (
    <HeroSection 
      videoSrc="https://www.instagram.com/reel/DZxediGojDl/?utm_source=ig_web_copy_link&stkn=NTc4MTIwNjQ2YQ=="
      navLinks={customNavLinks}
    />
  );
}

// Example 3: Different video source
export function AlternativeVideoExample() {
  return (
    <HeroSection 
      videoSrc="https://www.instagram.com/reel/DZxediGojDl/?utm_source=ig_web_copy_link&stkn=NTc4MTIwNjQ2YQ=="
    />
  );
}

// Example 4: Using header component separately (if needed for other pages)
import { Header } from '@/components';

export function HeaderOnlyExample() {
  const navLinks: NavLink[] = [
    { name: 'Home', href: '/', isActive: true },
    { name: 'About', href: '/about' },
    { name: 'Messages', href: '/messages' },
  ];

  return (
    <div className="min-h-screen bg-bg">
      <Header navLinks={navLinks} className="fixed top-0 left-0 z-50 h-20 w-full" />
      <main className="pt-20 px-6 sm:px-8 lg:px-12">
        <h1 className="text-ink font-serif text-3xl">Page Content</h1>
        <p className="text-ink-muted">Other page content goes here...</p>
      </main>
    </div>
  );
}