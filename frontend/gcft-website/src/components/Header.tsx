'use client';

import { useState } from 'react';
import { HeaderProps } from './types';

interface ExtendedHeaderProps extends HeaderProps {
  className?: string;
}

export default function Header({ navLinks, className = "" }: ExtendedHeaderProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <header className={`bg-transparent ${className}`}>
      <nav className="flex items-center justify-between px-4 py-3 sm:px-6 sm:py-4 lg:px-12">
        {/* Logo - Mobile Optimized */}
        <div className="flex items-center space-x-2 sm:space-x-3">
          <div className="text-gold text-xl sm:text-2xl font-bold">✝</div>
          <div className="flex flex-col leading-tight">
            <span className="text-white font-bold text-sm sm:text-lg tracking-tight">
              GCFT
            </span>
          </div>
        </div>

        {/* Desktop Navigation */}
        <div className="hidden lg:flex items-center space-x-8">
          {navLinks.map((link) => (
            <a
              key={link.name}
              href={link.href}
              className={`text-sm font-medium transition-colors duration-200 ${
                link.isActive
                  ? 'text-gold'
                  : 'text-gray-200 hover:text-white'
              }`}
            >
              {link.name}
            </a>
          ))}
        </div>

        {/* Desktop Watch Now Button */}
        <button className="hidden lg:block px-6 py-2 border border-gold text-gold text-sm font-bold uppercase tracking-wider rounded-md hover:bg-gold hover:text-navy transition-all duration-200">
          Watch Now
        </button>

        {/* Mobile Hamburger - Improved Touch Target */}
        <button
          onClick={toggleMobileMenu}
          className="lg:hidden p-3 text-white hover:text-gold transition-colors duration-200 -mr-3"
          aria-label="Toggle mobile menu"
        >
          <div className="w-6 h-6 flex flex-col justify-center space-y-1">
            <span
              className={`block h-0.5 w-6 bg-current transform transition-transform duration-200 ${
                isMobileMenuOpen ? 'rotate-45 translate-y-1' : ''
              }`}
            />
            <span
              className={`block h-0.5 w-6 bg-current transition-opacity duration-200 ${
                isMobileMenuOpen ? 'opacity-0' : ''
              }`}
            />
            <span
              className={`block h-0.5 w-6 bg-current transform transition-transform duration-200 ${
                isMobileMenuOpen ? '-rotate-45 -translate-y-1' : ''
              }`}
            />
          </div>
        </button>
      </nav>

      {/* Mobile Menu - Improved */}
      <div
        className={`lg:hidden bg-black/95 backdrop-blur-sm transform transition-transform duration-300 ease-in-out ${
          isMobileMenuOpen ? 'translate-y-0' : '-translate-y-full'
        }`}
      >
        <div className="px-4 py-6 space-y-4 sm:px-6 lg:px-12 max-h-screen overflow-y-auto">
          {navLinks.map((link) => (
            <a
              key={link.name}
              href={link.href}
              className={`block text-lg font-medium transition-colors duration-200 py-2 ${
                link.isActive
                  ? 'text-gold'
                  : 'text-gray-200 hover:text-white'
              }`}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              {link.name}
            </a>
          ))}
          <div className="pt-4 border-t border-white/20">
            <button className="w-full px-6 py-3 border border-gold text-gold text-sm font-bold uppercase tracking-wider rounded-md hover:bg-gold hover:text-navy transition-all duration-200">
              Watch Now
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}