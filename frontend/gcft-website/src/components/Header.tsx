"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import { navLinks as defaultLinks, site, socials, utilityLinks } from "@/lib/content";
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
  href = "#top",
  preload = false,
}: {
  className?: string;
  href?: string;
  preload?: boolean;
}) {
  return (
    <a href={href} className="flex shrink-0 items-center" aria-label={`${site.fullName} — home`}>
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
    </a>
  );
}

/** Small filled "play" tile used inside the Watch Live button. */
function PlayTile() {
  return (
    <span className="flex h-[18px] w-[18px] items-center justify-center rounded-[4px] bg-primary-container text-on-primary">
      <Icon name="play_arrow" size={14} fill />
    </span>
  );
}

export default function Header({ navLinks = defaultLinks, className = "" }: Partial<HeaderProps>) {
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(navLinks[0]?.href ?? "#top");
  const [scrolled, setScrolled] = useState(false);

  // Transparent over the hero; solid background once the page scrolls a little.
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const solid = scrolled || open;

  // Highlight the nav item for the section currently in view.
  useEffect(() => {
    const sections = navLinks
      .map((l) => document.getElementById(l.href.replace("#", "")))
      .filter((el): el is HTMLElement => !!el);
    if (!sections.length) return;
    const observer = new IntersectionObserver(
      (entries) => entries.forEach((e) => e.isIntersecting && setActive(`#${e.target.id}`)),
      { rootMargin: "-45% 0px -50% 0px" },
    );
    sections.forEach((s) => observer.observe(s));
    return () => observer.disconnect();
  }, [navLinks]);

  // Lock body scroll while the mobile menu is open; close on Escape / desktop resize.
  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
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

  const utilityCls = `transition-colors ${solid ? "hover:text-surface" : "hover:text-white"}`;

  return (
    <header className={`fixed inset-x-0 top-0 z-50 ${className}`}>
      {/* Utility bar (tablet & up) */}
      <div
        className={`hidden border-b transition-colors duration-300 md:block ${
          solid ? "border-white/10 bg-[#f3f1ec]/95" : "border-white/10 bg-transparent"
        }`}
      >
        <div
          className={`mx-auto flex h-10 max-w-shell items-center justify-between px-margin-sm text-[10px] font-bold uppercase tracking-widest transition-colors duration-300 md:px-10 lg:px-margin ${
            solid ? "text-[#475569]" : "text-white/75"
          }`}
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
        className={`border-b transition-[background-color,box-shadow,border-color] duration-300 ${
          solid
            ? "border-white/10 bg-surface/95 shadow-float backdrop-blur-xl"
            : "border-transparent bg-transparent shadow-none"
        }`}
      >
        <div className="mx-auto flex h-[72px] max-w-shell items-center justify-between gap-gutter px-margin-sm md:h-[88px] md:px-10 lg:px-margin">
          <Logo preload />

          <nav className="hidden items-center gap-8 lg:flex" aria-label="Primary">
            {navLinks.map((link) => {
              const isActive = active === link.href;
              return (
                <a
                  key={link.name}
                  href={link.href}
                  aria-current={isActive ? "page" : undefined}
                  className={`text-[15px] font-medium transition-colors ${
                    isActive ? "text-primary-container" : "text-[#e5e7eb] hover:text-primary-container"
                  }`}
                >
                  {link.name}
                </a>
              );
            })}
          </nav>

          <div className="hidden items-center gap-space-sm lg:flex">
            <a
              {...linkProps(socials.youtube)}
              className="inline-flex items-center gap-2 rounded-lg border border-primary-container px-4 py-2 text-[14px] font-bold text-white transition-colors hover:bg-primary-container/10"
            >
              Watch Live
              <PlayTile />
            </a>
            <a
              href="#contact"
              className="inline-flex items-center rounded-lg bg-primary-container px-5 py-2.5 text-[14px] font-semibold text-on-primary shadow-glow transition-all hover:bg-primary-fixed"
            >
              Connect
            </a>
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
        className={`fixed inset-x-0 bottom-0 top-[72px] overflow-y-auto bg-surface-container-low transition-opacity duration-300 md:top-[128px] lg:hidden ${
          open ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
      >
        <nav className="flex flex-col px-margin-sm pt-space-md pb-space-xl md:px-10" aria-label="Mobile">
          {navLinks.map((link) => (
            <a
              key={link.name}
              href={link.href}
              onClick={() => setOpen(false)}
              className={`px-space-md py-3 text-[17px] font-medium transition-colors ${
                active === link.href ? "text-primary-container" : "text-[#e5e7eb] hover:text-primary-container"
              }`}
            >
              {link.name}
            </a>
          ))}
          <div className="mt-space-md flex flex-col gap-3 border-t border-white/10 pt-space-md">
            <a
              {...linkProps(socials.youtube)}
              onClick={() => setOpen(false)}
              className="inline-flex items-center justify-center gap-2 rounded-lg border border-primary-container py-3 text-[16px] font-bold text-white"
            >
              Watch Live
              <PlayTile />
            </a>
            <a
              href="#contact"
              onClick={() => setOpen(false)}
              className="inline-flex items-center justify-center rounded-lg bg-primary-container py-3 text-[16px] font-semibold text-on-primary shadow-glow"
            >
              Connect
            </a>
          </div>
        </nav>
      </div>
    </header>
  );
}
