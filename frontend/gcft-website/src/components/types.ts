export interface NavLink {
  name: string;
  href: string;
  isActive?: boolean;
}

export interface HeaderProps {
  navLinks: NavLink[];
  className?: string;
}

export interface HeroSectionProps {
  videoSrc: string;
  navLinks?: NavLink[];
}