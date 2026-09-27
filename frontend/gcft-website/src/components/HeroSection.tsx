'use client';

import { useEffect, useRef } from 'react';
import Header from './Header';
import { NavLink } from './types';

const defaultNavLinks: NavLink[] = [
  { name: 'Home', href: '/', isActive: true },
  { name: 'About', href: '/about' },
  { name: 'Messages', href: '/messages' },
  { name: 'Music', href: '/music' },
  { name: 'Mentorship', href: '/mentorship' },
  { name: 'Give', href: '/give' },
  { name: 'Events', href: '/events' },
];

interface HeroSectionProps {
  videoSrc: string;
  navLinks?: NavLink[];
}

export default function HeroSection({
  videoSrc,
  navLinks = defaultNavLinks,
}: HeroSectionProps) {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    // Respect prefers-reduced-motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    if (prefersReducedMotion && videoRef.current) {
      videoRef.current.pause();
    }
  }, []);

  return (
    <section className="relative h-screen w-full overflow-hidden">
      {/* Layer 0: video */}
      <video
        ref={videoRef}
        autoPlay
        muted
        loop
        playsInline
        preload="auto"
        className="absolute inset-0 z-0 h-full w-full object-cover"
        src={videoSrc}
      >
        Your browser does not support the video tag.
      </video>

      {/* Layer 10: overlay */}
<div className="absolute inset-0 z-10 bg-gradient-to-r from-[#0a1128]/85 via-[#0a1128]/85 to-[#0a1128]/85" />

      {/* Layer 50: header, fixed, its OWN row, never mixed into hero content */}
      <Header navLinks={navLinks} className="fixed top-0 left-0 z-50 h-20 w-full" />

      {/* Layer 20: hero content, pushed below the header with pt-20, centered in the rest */}
      <div className="relative z-20 flex h-full w-full flex-col justify-center px-6 pt-20 pb-12 sm:px-8 lg:px-12">
        {/* Main Headline */}
        <h1 className="font-serif text-5xl md:text-6xl lg:text-7xl font-bold leading-tight mb-6">
          <span className="block text-white">
            Where <span className="text-gold">The Truth.</span>
          </span>
          <span className="block">
            <span className="text-gold">Still</span>{' '}
            <span className="text-white">Exist. </span>
            {/* <span className="text-gold">Transformed.</span> */}
          </span>
        </h1>

        {/* Subheading */}
        <p className="text-gray-300 text-lg md:text-xl max-w-xl mb-8 leading-relaxed">
          Powerful worship, life-changing teaching, and ministry that impacts lives worldwide.
        </p>

        {/* Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 mb-12">
          <button className="flex items-center justify-center gap-2 bg-gold hover:bg-gold/90 text-navy font-bold text-sm uppercase tracking-wider px-8 py-4 rounded-md transition-all duration-200">
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z"/>
            </svg>
            Watch Latest
          </button>
          <button className="border border-white text-white hover:bg-white hover:text-navy font-bold text-sm uppercase tracking-wider px-8 py-4 rounded-md transition-all duration-200">
            Learn More
          </button>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 mb-3 transform -translate-x-1/2 z-20">
        <button
          className="w-10 h-10 border border-white/30 rounded-full flex items-center justify-center text-white/70 hover:text-white hover:border-white/50 transition-all duration-200 animate-bounce"
          aria-label="Scroll down"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
        </button>
      </div>

      {/* Ticker/Marquee */}
      <div className="fixed bottom-0 left-0 right-0 z-50 bg-black/90 backdrop-blur-sm overflow-hidden">
        <div className="flex animate-marquee whitespace-nowrap py-3 text-sm text-gray-300">
          <span className="mx-8 flex items-center gap-2">
            🕐 Tuesday Bible Study — 4:30 PM
          </span>
          <span className="mx-8 flex items-center gap-2">
            ▶ Watch Live on YouTube Every Sunday
          </span>
          <span className="mx-8 flex items-center gap-2">
            ⛪ Sunday Services — 8:45 AM
          </span>
          <span className="mx-8 flex items-center gap-2">
            🕐 Tuesday Bible Study — 4:30 PM
          </span>
          <span className="mx-8 flex items-center gap-2">
            ▶ Watch Live on YouTube Every Sunday
          </span>
          <span className="mx-8 flex items-center gap-2">
            ⛪ Sunday Services — 8:45 AM
          </span>
        </div>
      </div>
    </section>
  );
}