"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { navLinks as defaultLinks, site, utilityLinks, type NavItem } from "@/lib/content";
import type { HeaderProps } from "./types";
import { Icon, linkProps } from "./ui";

/**
 * Official GCFT logo.
 * The source is a 1600×1600 JPG with a white background and lots of padding, so we
 * (1) crop to the artwork's bounding box (≈ x 26–74%, y 30–70%) and
 * (2) invert + hue-rotate + screen-blend it so the white drops out and the dark
 *     lettering turns light on the dark header, while the cross stays green.
 */
export function Logo({
  className = "h-12 md:h-14",
  href = "/",
  preload = false,
}: {
  className?: string;
  href?: string;
  preload?: boolean;
}) {
  return (
    <Link href={href} className="flex shrink-0 items-center" aria-label={`${site.fullName} — home`}>
      <span className={`relative block aspect-[48/40] overflow-hidden ${className}`}>
        <Image
          src={site.logo}
          alt={site.fullName}
          width={1600}
          height={1600}
          preload={preload}
          sizes="480px"
          className="absolute max-w-none mix-blend-screen [filter:invert(1)_hue-rotate(180deg)_brightness(1.15)]"
          style={{ width: "208.33%", height: "250%", left: "-54.17%", top: "-75%" }}
        />
      </span>
    </Link>
  );
}

/** Pulsing live dot used inside the Watch Live button. */
function PlayTile() {
  return (
    <span className="relative inline-flex h-2 w-2" aria-hidden="true">
      <span className="absolute inset-0 animate-ping rounded-full bg-error opacity-60" />
      <span className="relative inline-flex h-2 w-2 rounded-full bg-error" />
    </span>
  );
}

/** Which nav item is current — route-based on inner pages, section-based on the home page. */
function useActiveHref(navLinks: NavItem[]) {
  const pathname = usePathname();
  const [section, setSection] = useState<string | null>(null);

  useEffect(() => {
    if (pathname !== "/") return;
    const targets = navLinks
      .filter((l) => l.href.startsWith("/#"))
      .map((l) => document.getElementById(l.href.slice(2)))
      .filter((el): el is HTMLElement => !!el);
    const hero = document.getElementById("top");
    if (hero) targets.unshift(hero);
    const observer = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => e.isIntersecting && setSection(e.target.id === "top" ? "/" : `/#${e.target.id}`)),
      { rootMargin: "-45% 0px -50% 0px" },
    );
    targets.forEach((t) => observer.observe(t));
    return () => observer.disconnect();
  }, [pathname, navLinks]);

  if (pathname === "/") return section ?? "/";
  const match = navLinks.find(
    (l) => l.href !== "/" && !l.href.startsWith("/#") && (pathname === l.href || pathname.startsWith(`${l.href}/`)),
  );
  return match?.href ?? pathname;
}

export default function Header({ navLinks = defaultLinks, className = "" }: Partial<HeaderProps>) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [dropdown, setDropdown] = useState<string | null>(null);
  const [mobileSub, setMobileSub] = useState<string | null>(null);
  const active = useActiveHref(navLinks);

  // Transparent over the hero; solid background once the page scrolls a little.
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Close menus on route change (state adjusted during render, not in an effect).
  const [lastPath, setLastPath] = useState(pathname);
  if (lastPath !== pathname) {
    setLastPath(pathname);
    setOpen(false);
    setDropdown(null);
  }

  // Lock body scroll while the mobile menu is open; close on Escape / desktop resize.
  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== "Escape") return;
      setOpen(false);
      setDropdown(null);
    };
    const mq = window.matchMedia("(min-width: 1024px)");
    const onMq = () => mq.matches && setOpen(false);
    window.addEventListener("keydown", onKey);
    mq.addEventListener("change", onMq);
    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", onKey);
      mq.removeEventListener("change", onMq);
    };
  }, [open]);

  const solid = scrolled || open;
  const utilityCls = "transition-colors hover:text-white";
  const linkCls = (isActive: boolean) =>
    `relative text-[14px] tracking-[-0.005em] transition-colors duration-300 ${
      isActive
        ? "text-white after:absolute after:-bottom-2.5 after:left-1/2 after:h-1 after:w-1 after:-translate-x-1/2 after:rounded-full after:bg-primary-container"
        : "text-white/65 hover:text-white"
    }`;
  const mobileCls = (isActive: boolean) =>
    `text-[26px] font-medium tracking-[-0.03em] transition-colors ${isActive ? "text-white" : "text-white/60 hover:text-white"}`;

  return (
    <header
      className={`fixed inset-x-0 top-0 z-50 transition-[background-color,border-color,backdrop-filter] duration-500 ${
        solid ? "border-b border-hairline bg-surface/80 backdrop-blur-xl backdrop-saturate-150" : "border-b border-transparent"
      } ${className}`}
    >
      {/* Utility bar (tablet & up) */}
      <div
        className="hidden border-b border-hairline md:block"
      >
        <div
          className="eyebrow mx-auto flex h-10 max-w-shell items-center justify-between px-margin-sm text-[10.5px] text-white/55 md:px-10 lg:px-margin"
        >
          <div className="flex gap-6">
            {utilityLinks.left.map((l) => (
              <a key={l.name} {...linkProps(l.href)} className={utilityCls}>
                {l.name}
              </a>
            ))}
          </div>
          <div className="flex items-center gap-6">
            {utilityLinks.right.map((l) => (
              <a key={l.name} {...linkProps(l.href)} className={utilityCls}>
                {l.name}
              </a>
            ))}
            <button type="button" className={`flex items-center gap-1 ${utilityCls}`} aria-label="Language: English">
              <Icon name="language" size={13} />
              EN
            </button>
          </div>
        </div>
      </div>

      {/* Main bar */}
      <div
        className="relative"
      >
        <div className="mx-auto flex h-[72px] max-w-shell items-center justify-between gap-gutter px-margin-sm md:h-[88px] md:px-10 lg:px-margin">
          <Logo preload />

          <nav className="hidden items-center gap-6 lg:flex xl:gap-9" aria-label="Primary">
            {navLinks.map((link) => {
              const isActive = active === link.href;
              if (!link.children?.length) {
                return (
                  <Link key={link.name} href={link.href} aria-current={isActive ? "page" : undefined} className={linkCls(isActive)}>
                    {link.name}
                  </Link>
                );
              }
              const isOpen = dropdown === link.name;
              return (
                <div
                  key={link.name}
                  className="relative"
                  onMouseEnter={() => setDropdown(link.name)}
                  onMouseLeave={() => setDropdown(null)}
                >
                  <button
                    type="button"
                    aria-expanded={isOpen}
                    aria-haspopup="true"
                    onClick={() => setDropdown(isOpen ? null : link.name)}
                    className={`inline-flex items-center gap-0.5 ${linkCls(isActive)}`}
                  >
                    {link.name}
                    <Icon name="expand_more" size={16} className={`opacity-60 transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`} />
                  </button>

                  {/* Dropdown panel (pt bridges the hover gap) */}
                  <div
                    className={`absolute top-full left-1/2 w-72 -translate-x-1/2 pt-5 transition-all duration-200 ${
                      isOpen ? "visible translate-y-0 opacity-100" : "invisible -translate-y-1 opacity-0"
                    }`}
                  >
                    <ul className="glass-2 overflow-hidden rounded-2xl p-1.5 shadow-float">
                      {link.children.map((child) => {
                        const childActive = pathname === child.href;
                        return (
                          <li key={child.href}>
                            <Link
                              href={child.href}
                              onClick={() => setDropdown(null)}
                              aria-current={childActive ? "page" : undefined}
                              className={`group flex items-center justify-between gap-space-sm rounded-xl px-4 py-3 transition-colors hover:bg-white/[0.05] ${
                                childActive ? "bg-white/[0.04]" : ""
                              }`}
                            >
                              <span className="min-w-0">
                                <span
                                  className={`flex items-center gap-2 text-[15px] tracking-[-0.01em] text-on-surface`}
                                >
                                  {child.name}
                                </span>
                                {child.description && (
                                  <span className="mt-0.5 block truncate text-body-sm text-on-surface-variant">
                                    {child.description}
                                  </span>
                                )}
                              </span>
                              <Icon
                                name="arrow_forward"
                                size={16}
                                className="shrink-0 -translate-x-1 text-primary-container opacity-0 transition-all group-hover:translate-x-0 group-hover:opacity-100"
                              />
                            </Link>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                </div>
              );
            })}
          </nav>

          <div className="hidden items-center gap-space-sm lg:flex">
            <Link
              href="/live"
              className="inline-flex h-10 items-center gap-2.5 rounded-full border border-white/20 px-4 text-[14px] text-white transition-colors hover:border-white/50"
            >
              <PlayTile />
              Watch live
            </Link>
            <Link
              href="/contact"
              className="inline-flex h-10 items-center rounded-full bg-primary-container px-5 text-[14px] font-medium text-on-primary transition-colors hover:bg-primary-fixed"
            >
              Connect
            </Link>
          </div>

          <button
            type="button"
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            aria-controls="mobile-menu"
            aria-label={open ? "Close menu" : "Open menu"}
            className="-mr-2 flex h-11 w-11 items-center justify-center text-white transition-colors hover:text-primary-container lg:hidden"
          >
            <Icon name={open ? "close" : "menu"} size={28} />
          </button>
        </div>
      </div>

      {/* Mobile menu panel */}
      <div
        id="mobile-menu"
        className={`fixed inset-x-0 bottom-0 top-[72px] overflow-y-auto bg-surface transition-opacity duration-300 md:top-[128px] lg:hidden ${
          open ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
      >
        <nav className="flex flex-col px-margin-sm pt-space-md pb-space-xl md:px-10" aria-label="Mobile">
          {navLinks.map((link) =>
            link.children?.length ? (
              <div key={link.name}>
                <button
                  type="button"
                  aria-expanded={mobileSub === link.name}
                  onClick={() => setMobileSub(mobileSub === link.name ? null : link.name)}
                  className={`flex w-full items-center justify-between px-space-md py-3 text-left ${mobileCls(active === link.href)}`}
                >
                  {link.name}
                  <Icon
                    name="expand_more"
                    size={22}
                    className={`transition-transform duration-200 ${mobileSub === link.name ? "rotate-180" : ""}`}
                  />
                </button>
                <div
                  className={`grid transition-[grid-template-rows] duration-300 ${
                    mobileSub === link.name ? "grid-rows-[1fr]" : "grid-rows-[0fr]"
                  }`}
                >
                  <ul className="overflow-hidden">
                    {link.children.map((child) => (
                      <li key={child.href}>
                        <Link
                          href={child.href}
                          onClick={() => setOpen(false)}
                          className={`ml-space-md block border-l px-space-md py-2.5 text-[16px] transition-colors ${
                            pathname === child.href
                              ? "border-primary-container text-primary-container"
                              : "border-white/10 text-on-surface-variant hover:text-primary-container"
                          }`}
                        >
                          {child.name}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : (
              <Link
                key={link.name}
                href={link.href}
                onClick={() => setOpen(false)}
                className={`px-space-md py-3 ${mobileCls(active === link.href)}`}
              >
                {link.name}
              </Link>
            ),
          )}
          <div className="mt-space-md flex flex-col gap-3 border-t border-white/10 pt-space-md">
            <Link
              href="/live"
              onClick={() => setOpen(false)}
              className="inline-flex h-12 items-center justify-center gap-2.5 rounded-full border border-white/20 text-[15px] text-white"
            >
              <PlayTile />
              Watch live
            </Link>
            <Link
              href="/contact"
              onClick={() => setOpen(false)}
              className="inline-flex h-12 items-center justify-center rounded-full bg-primary-container text-[15px] font-medium text-on-primary"
            >
              Connect
            </Link>
          </div>
        </nav>
      </div>
    </header>
  );
}
