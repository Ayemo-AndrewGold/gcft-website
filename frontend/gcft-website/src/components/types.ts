import type { NavItem } from "@/lib/content";

export type { NavItem };

/** @deprecated use NavItem */
export type NavLink = NavItem;

export interface HeaderProps {
  navLinks: NavItem[];
  className?: string;
}

export interface HeroSectionProps {
  videoSrc: string;
}
