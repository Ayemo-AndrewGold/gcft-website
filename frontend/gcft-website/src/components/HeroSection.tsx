"use client";

import Link from "next/link";
import { useEffect, useRef } from "react";
import { images } from "@/lib/images";
import { site, socials, tickerItems } from "@/lib/content";
import type { HeroSectionProps } from "./types";
import { Container, Icon, linkProps } from "./ui";

const toneClass = {
  primary: "text-primary",
  secondary: "text-secondary",
  muted: "text-on-surface-variant",
} as const;

export default function HeroSection({ videoSrc = site.heroVideo }: Partial<HeroSectionProps>) {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      videoRef.current?.pause();
    }
  }, []);

  return (
    <section id="top" className="relative flex min-h-[100svh] w-full flex-col overflow-hidden bg-surface">
      {/* Background video + layered vignette scrims */}
      <div className="absolute inset-0 z-0">
        <video
          ref={videoRef}
          autoPlay
          muted
          loop
          playsInline
          preload="auto"
          poster={images.hero}
          className="h-full w-full object-cover"
          src={videoSrc}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-surface/60 via-surface/35 to-surface" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_0%,rgba(14,19,31,0.45)_60%,rgba(14,19,31,0.9)_100%)]" />
      </div>

      <Container className="relative z-10 flex min-h-0 flex-1 flex-col justify-center pt-[88px] pb-space-lg md:pt-[128px]">
        {/* Editorial headline */}
        <div className="max-w-3xl">
          <div className="mb-space-md inline-flex items-center md:mb-space-lg gap-space-sm rounded-full bg-surface-container/80 px-space-md py-space-xs backdrop-blur-md">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-primary" />
            </span>
            <span className="text-label-sm uppercase tracking-widest text-primary">Welcome to {site.fullName}</span>
          </div>

          <h1 className="mb-space-md font-display text-display-hero-mobile text-on-surface md:text-display-hero">
            Where the <span className="font-medium italic text-primary-container">Truth</span> Still Exists.
          </h1>

          <p className="mb-space-lg max-w-2xl md:mb-space-xl text-body-md text-on-surface-variant md:text-body-lg">
            We believe the message of Malachi 4:5 &amp; 6b and Revelation 10:7, and we are on a mandate to preach nothing
            else but the truth. Our motto is simple: <span className="text-on-surface">“{site.motto}.”</span>
          </p>

          <div className="flex flex-col gap-space-md xs:flex-row xs:flex-wrap xs:items-center">
            <a
              {...linkProps(socials.youtube)}
              className="inline-flex items-center justify-center gap-space-xs rounded-lg bg-primary-container px-space-xl py-space-md text-label-md text-on-primary shadow-glow-lg transition-all hover:bg-primary-fixed active:scale-95"
            >
              <Icon name="play_arrow" fill />
              Watch Latest Service
            </a>
            <Link
              href="/about"
              className="inline-flex items-center justify-center gap-space-xs rounded-lg px-space-lg py-space-md text-label-md text-secondary transition-all hover:bg-surface-container-high/60 hover:text-primary"
            >
              Learn More About Us
              <Icon name="arrow_forward" size={18} />
            </Link>
          </div>
        </div>

        {/* Scroll cue */}
        <div className="pointer-events-none absolute right-margin-sm bottom-space-lg hidden md:right-10 md:flex lg:right-margin">
          <a
            href="#about"
            className="pointer-events-auto hidden flex-col items-center gap-space-xs pb-2 text-on-surface-variant transition-colors hover:text-primary md:flex"
          >
            <span className="text-[10px] font-semibold uppercase tracking-widest">Scroll Down</span>
            <Icon name="keyboard_arrow_down" className="animate-bounce" />
          </a>
        </div>
      </Container>

      {/* Ambient ticker */}
      <div className="relative z-10 w-full shrink-0 overflow-hidden bg-surface-container-lowest/80 py-space-sm backdrop-blur-md">
        <Container className="flex items-center justify-between gap-space-md">
          <div className="no-scrollbar flex items-center gap-space-md overflow-x-auto py-0.5 text-nowrap">
            {tickerItems.map((item, i) => (
              <span key={item.text} className="inline-flex items-center gap-space-md">
                {i > 0 && <span className="text-surface-bright">•</span>}
                <span className={`inline-flex items-center gap-1 text-label-sm ${toneClass[item.tone]}`}>
                  {"icon" in item && <Icon name={item.icon} size={16} />}
                  {item.text}
                </span>
              </span>
            ))}
          </div>
          <span className="hidden items-center gap-1 text-label-sm tracking-wide text-primary-fixed lg:inline-flex">
            <Icon name="location_on" size={14} />
            {site.location}
          </span>
        </Container>
      </div>
    </section>
  );
}
