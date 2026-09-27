/*
 * About-page building blocks, modelled on the structure of
 * feedbackfromthefuture.com/the-mission — split hero frame, two-column intro,
 * numbered pathway boxes, image cards, and an accent band with rolling counters.
 */
import Link from "next/link";
import type { ReactNode } from "react";
import { aboutPages } from "@/lib/content";
import { images } from "@/lib/images";
import { journey, ministries, pathways, type AboutIntro } from "@/lib/about";
import { Container, CoverImage, Icon, linkProps } from "../ui";
import CountUp from "./CountUp";

/** Red-dot style overline, left or centred. */
export function Kicker({ children, center = false }: { children: ReactNode; center?: boolean }) {
  return (
    <p
      className={`text-[13px] font-bold uppercase tracking-[0.2em] text-primary-container ${center ? "text-center" : ""}`}
    >
      {children}
    </p>
  );
}

/* ------------------------------------------------------------------ */
/* 1. Page hero — split background (dark | accent) with a framed image */
/* ------------------------------------------------------------------ */
export function PageHero({
  image = images.hero,
  title,
  current,
  crumbs,
  showAboutTabs = true,
}: {
  image?: string;
  title: string;
  current: string;
  /** Breadcrumb trail after "Home"; defaults to the About trail. */
  crumbs?: { name: string; href?: string }[];
  showAboutTabs?: boolean;
}) {
  const trail =
    crumbs ?? [{ name: "About", href: "/about" }, ...(current !== "Who We Are" ? [{ name: current }] : [])];
  return (
    <section className="relative w-full overflow-hidden bg-surface pt-[88px] md:pt-[128px]">
      {/* Split background: accent block covers the right ~45% */}
      <div aria-hidden="true" className="absolute top-[88px] right-0 bottom-0 w-[45%] bg-primary-container md:top-[128px]" />
      <div
        aria-hidden="true"
        className="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-b from-transparent to-surface md:h-32"
      />

      <Container className="relative z-10 pt-space-md pb-section">
        <div className="relative aspect-[4/3] overflow-hidden rounded-xl shadow-float sm:aspect-[16/9] lg:aspect-[21/9]">
          <CoverImage src={image} alt="" className="group-hover:scale-100" />
          <div className="absolute inset-0 bg-gradient-to-t from-surface/90 via-surface/20 to-transparent" />
          <div className="absolute inset-x-0 bottom-0 p-space-lg md:p-space-xl">
            <nav aria-label="Breadcrumb" className="mb-space-sm text-label-sm uppercase tracking-widest text-on-surface-variant">
              <Link href="/" className="hover:text-primary-container">
                Home
              </Link>
              {trail.map((c) => (
                <span key={c.name}>
                  <span className="mx-2 text-primary-container">/</span>
                  {c.href ? (
                    <Link href={c.href} className="hover:text-primary-container">
                      {c.name}
                    </Link>
                  ) : (
                    <span className="text-on-surface">{c.name}</span>
                  )}
                </span>
              ))}
            </nav>
            <h1 className="font-display text-display-hero-mobile text-on-surface md:text-display-hero">{title}</h1>
          </div>
        </div>

        {/* Sub-page tabs */}
        {showAboutTabs && (
        <nav aria-label="About sections" className="no-scrollbar mt-space-lg flex gap-space-xs overflow-x-auto">
          {aboutPages.map((p) => {
            const isCurrent = p.name === current;
            return (
              <Link
                key={p.href}
                href={p.href}
                aria-current={isCurrent ? "page" : undefined}
                className={`shrink-0 rounded-lg border px-space-md py-2 text-label-md uppercase tracking-wider transition-colors ${
                  isCurrent
                    ? "border-primary-container bg-primary-container text-on-primary"
                    : "border-white/15 bg-surface/70 text-on-surface backdrop-blur-md hover:border-primary-container hover:text-primary-container"
                }`}
              >
                {p.name}
              </Link>
            );
          })}
        </nav>
        )}
      </Container>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* 2. Two-column intro: heading + lead on the left, body on the right  */
/* ------------------------------------------------------------------ */
export function IntroSplit({ intro }: { intro: AboutIntro }) {
  return (
    <section className="w-full bg-surface pb-section">
      <Container>
        <div className="grid grid-cols-1 gap-space-lg lg:grid-cols-2 lg:gap-12">
          <div>
            <Kicker>{intro.eyebrow}</Kicker>
            <h2 className="mt-space-sm mb-space-lg font-display text-headline-lg-mobile text-on-surface md:text-[44px] md:leading-[52px]">
              {intro.title}
            </h2>
            {intro.lead.map((p) => (
              <p key={p} className="text-body-md text-on-surface-variant md:text-body-lg">
                {p}
              </p>
            ))}
          </div>
          <div className="flex flex-col gap-space-md lg:pt-[6.5rem]">
            {intro.body.map((p) => (
              <p key={p} className="text-body-md text-on-surface-variant md:text-body-lg">
                {p}
              </p>
            ))}
            {intro.closing && (
              <p className="border-l-2 border-primary-container pl-space-md font-display text-headline-sm uppercase tracking-wide text-on-surface">
                {intro.closing}
              </p>
            )}
          </div>
        </div>
      </Container>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* 3. Numbered pathway boxes (01 / 02 / 03)                            */
/* ------------------------------------------------------------------ */
export function Pathways() {
  return (
    <section className="w-full bg-surface pb-section">
      <Container>
        <div className="grid grid-cols-1 gap-gutter md:grid-cols-3">
          {pathways.map((p) => (
            <Link
              key={p.n}
              href={p.href}
              className="group relative flex flex-col justify-between gap-space-xl rounded-xl border border-white/80 px-10 py-8 transition-all duration-300 hover:-translate-y-1 hover:border-primary-container hover:shadow-glow"
            >
              <div className="flex items-start justify-between">
                <span className="font-display text-[56px] leading-none text-white/15 transition-colors group-hover:text-primary-container/40">
                  {p.n}
                </span>
                <Icon name={p.icon} size={28} className="text-primary-container" />
              </div>
              <div>
                <p className="text-[20px] font-semibold text-on-surface md:text-[22px]">{p.kicker}</p>
                <div className="mt-1 flex items-center justify-between gap-space-sm">
                  <h3 className="font-body text-[24px] font-bold uppercase tracking-wide text-on-surface transition-colors group-hover:text-primary-container md:text-[28px]">
                    {p.title}
                  </h3>
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-white/30 transition-all group-hover:border-primary-container group-hover:bg-primary-container group-hover:text-on-primary">
                    <Icon name="arrow_outward" size={20} />
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </Container>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* 4. "How we help" — centred heading + 3 image cards                  */
/* ------------------------------------------------------------------ */
export function MinistryCards({ className = "bg-surface-container-lowest" }: { className?: string }) {
  return (
    <section className={`w-full py-section ${className}`}>
      <Container>
        <Kicker center>{ministries.eyebrow}</Kicker>
        <h2 className="mx-auto mt-space-sm mb-space-xl max-w-3xl text-center font-display text-headline-lg-mobile text-on-surface md:text-[44px] md:leading-[52px]">
          {ministries.title}
        </h2>
        <div className="grid grid-cols-1 gap-gutter md:grid-cols-3">
          {ministries.items.map((m) => (
            <a key={m.title} {...linkProps(m.href)} className="group block text-center">
              <div className="relative aspect-square overflow-hidden rounded-xl">
                <CoverImage src={m.image} alt={m.title} />
                <div className="absolute inset-0 bg-gradient-to-t from-surface/70 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
                <span className="absolute right-4 bottom-4 flex h-11 w-11 translate-y-2 items-center justify-center rounded-full bg-primary-container text-on-primary opacity-0 transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100">
                  <Icon name="arrow_outward" size={20} />
                </span>
              </div>
              <div className="mx-auto max-w-[260px] pt-space-lg">
                <h3 className="font-body text-[26px] font-semibold text-primary-container md:text-[28px]">{m.title}</h3>
                <p className="mt-space-xs text-body-md text-on-surface-variant">{m.body}</p>
              </div>
            </a>
          ))}
        </div>
      </Container>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* 5. Accent band — heading + CTA left, rolling counters right         */
/* ------------------------------------------------------------------ */
export function JourneyBand() {
  return (
    <section className="w-full overflow-hidden bg-primary-container text-on-primary">
      <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,380px)_minmax(0,1fr)]">
        <div className="px-margin-sm py-section md:px-10 lg:pr-0 lg:pl-margin">
          <p className="text-[13px] font-bold uppercase tracking-[0.2em] text-on-primary/80">{journey.eyebrow}</p>
          <h2 className="mt-space-sm font-display text-headline-lg-mobile md:text-[44px] md:leading-[52px]">
            {journey.title}
          </h2>
          <p className="mt-space-md text-body-md text-on-primary/80">{journey.body}</p>
          <a
            {...linkProps(journey.cta.href)}
            className="mt-space-lg inline-flex items-center gap-space-xs rounded-lg bg-surface px-space-lg py-3 text-label-md uppercase tracking-wider text-on-surface transition-colors hover:bg-surface-container-high"
          >
            {journey.cta.label} <Icon name="arrow_forward" size={18} />
          </a>
        </div>

        {/* Rolling counters (duplicated for a seamless loop) */}
        <div className="group relative flex items-center overflow-hidden pb-section lg:py-section">
          <div className="flex w-max animate-marquee [animation-duration:45s] group-hover:[animation-play-state:paused] motion-reduce:animate-none">
            {[0, 1].map((copy) => (
              <ul key={copy} aria-hidden={copy === 1} className="flex shrink-0">
                {journey.counters.map((c) => (
                  <li key={c.label} className="w-[240px] shrink-0 border-l border-on-primary/15 px-space-lg">
                    <CountUp
                      value={c.value}
                      suffix={c.suffix}
                      className="font-display text-[64px] leading-none font-semibold md:text-[69px]"
                    />
                    <p className="mt-space-md text-[17px] leading-snug text-on-primary/85">{c.label}</p>
                  </li>
                ))}
              </ul>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
