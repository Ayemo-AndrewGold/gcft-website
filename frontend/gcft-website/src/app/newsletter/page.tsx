import type { Metadata } from "next";
import Link from "next/link";
import { Kicker } from "@/components/about/AboutBlocks";
import { NewsletterSignup } from "@/components/forms/MailtoForms";
import { Container, CoverImage, Icon, linkProps } from "@/components/ui";
import { site } from "@/lib/content";
import { newsletter as nl } from "@/lib/pages";

export const metadata: Metadata = {
  title: "Newsletter — GCFT Weekly",
  description: nl.lead,
};

function CtaLink({ href, children, variant = "solid" }: { href: string; children: React.ReactNode; variant?: "solid" | "outline" }) {
  const cls =
    variant === "solid"
      ? "bg-primary-container text-on-primary shadow-glow hover:bg-primary-fixed"
      : "border border-primary-container text-on-surface hover:bg-primary-container/10";
  const props = href.startsWith("#") ? { href } : linkProps(href);
  return (
    <a
      {...props}
      className={`inline-flex items-center justify-center gap-space-xs rounded-lg px-space-xl py-3 text-label-md uppercase tracking-wider transition-all ${cls}`}
    >
      {children} <Icon name="arrow_forward" size={18} />
    </a>
  );
}

export default function NewsletterPage() {
  return (
    <main className="w-full bg-surface">
      {/* 1. Landing hero — split background, copy + signup left, flyer right */}
      <section className="relative w-full overflow-hidden bg-surface pt-[88px] md:pt-[128px]">
        <div aria-hidden="true" className="absolute top-[88px] right-0 bottom-0 hidden w-[38%] bg-primary-container md:top-[128px] lg:block" />
        <Container className="relative z-10 grid grid-cols-1 items-center gap-space-xl py-section lg:grid-cols-[minmax(0,7fr)_minmax(0,5fr)]">
          <div>
            <nav aria-label="Breadcrumb" className="mb-space-lg text-label-sm uppercase tracking-widest text-on-surface-variant">
              <Link href="/" className="hover:text-primary-container">
                Home
              </Link>
              <span className="mx-2 text-primary-container">/</span>
              <span className="text-on-surface">Newsletter</span>
            </nav>
            <div className="mb-space-md inline-flex items-center gap-space-sm rounded-full border border-primary-container/40 px-space-md py-1.5">
              <Icon name="mark_email_unread" size={18} className="text-primary-container" />
              <span className="text-[13px] font-bold uppercase tracking-[0.2em] text-primary-container">{nl.name}</span>
            </div>
            <h1 className="font-display text-display-hero-mobile text-on-surface md:text-display-hero">{nl.headline}</h1>
            <p className="mt-space-md max-w-2xl text-body-md text-on-surface-variant md:text-body-lg">{nl.lead}</p>
            <div id="subscribe" className="mt-space-xl max-w-2xl scroll-mt-40">
              <NewsletterSignup cta="Join Them" />
            </div>
          </div>
          <div className="relative mx-auto w-full max-w-md lg:max-w-none">
            <div className="relative aspect-[4/5] overflow-hidden rounded-xl shadow-float ring-1 ring-white/10">
              <CoverImage src={nl.flyer} alt={`${nl.name} flyer`} />
              <div className="absolute inset-0 bg-gradient-to-t from-surface via-surface/30 to-transparent" />
              <div className="absolute inset-x-0 bottom-0 p-space-lg">
                <p className="text-[13px] font-bold uppercase tracking-[0.2em] text-primary-container">This Week</p>
                <p className="mt-1 font-display text-headline-md text-on-surface">“Back to the Bible.”</p>
                <p className="mt-1 text-body-sm text-on-surface-variant">Malachi 4:5–6b · Revelation 10:7</p>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* 2. Trust band */}
      <section className="w-full border-y border-white/10 bg-surface-container-lowest py-space-xl">
        <Container className="flex flex-col items-start justify-between gap-space-lg md:flex-row md:items-center">
          <h2 className="max-w-2xl font-display text-headline-md text-on-surface">{nl.trust}</h2>
          <div className="flex flex-wrap gap-space-sm">
            <CtaLink href="#subscribe">Subscribe Free</CtaLink>
            <CtaLink href={nl.sampleCta.href} variant="outline">
              See the Latest
            </CtaLink>
          </div>
        </Container>
      </section>

      {/* 3. Seven segments */}
      <section className="w-full bg-surface py-section">
        <Container>
          <Kicker center>Inside Every Edition</Kicker>
          <h2 className="mx-auto mt-space-sm mb-space-xl max-w-3xl text-center font-display text-headline-lg-mobile text-on-surface md:text-[44px] md:leading-[52px]">
            {nl.segmentsIntro}
          </h2>
          <ol className="grid grid-cols-1 gap-gutter sm:grid-cols-2 lg:grid-cols-4">
            {nl.segments.map((s, i) => (
              <li
                key={s.title}
                className="group rounded-xl border border-white/15 p-space-lg transition-all duration-300 hover:-translate-y-1 hover:border-primary-container"
              >
                <span className="font-display text-[44px] leading-none text-white/15 transition-colors group-hover:text-primary-container/50">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <h3 className="mt-space-md font-display text-headline-sm italic text-on-surface">{s.title}</h3>
                <p className="mt-space-xs text-body-sm text-on-surface-variant">{s.body}</p>
              </li>
            ))}
            <li className="flex flex-col justify-between gap-space-md rounded-xl bg-primary-container p-space-lg text-on-primary">
              <Icon name="mark_email_read" size={36} />
              <div>
                <p className="font-display text-headline-sm">Get the latest issue</p>
                <a href="#subscribe" className="mt-space-sm inline-flex items-center gap-1 text-label-md uppercase tracking-wider underline underline-offset-4">
                  Subscribe <Icon name="arrow_forward" size={16} />
                </a>
              </div>
            </li>
          </ol>
        </Container>
      </section>

      {/* 4. Audience + sample */}
      <section className="w-full bg-surface-container-lowest py-section">
        <Container className="grid grid-cols-1 gap-gutter lg:grid-cols-2">
          <div className="candle-glow flex flex-col justify-between gap-space-lg rounded-xl border border-white/10 p-space-lg md:p-space-xl">
            <h2 className="font-display text-headline-lg-mobile text-on-surface md:text-headline-lg">{nl.audience}</h2>
            <div>
              <CtaLink href="#subscribe">Join Them</CtaLink>
            </div>
          </div>
          <div className="flex flex-col justify-between gap-space-lg rounded-xl border border-white/10 p-space-lg md:p-space-xl">
            <h2 className="font-display text-headline-lg-mobile text-on-surface md:text-headline-lg">
              The best way to understand it is to read it.
            </h2>
            <div>
              <CtaLink href={nl.sampleCta.href} variant="outline">
                {nl.sampleCta.label}
              </CtaLink>
            </div>
          </div>
        </Container>
      </section>

      {/* 5. Editor */}
      <section className="w-full bg-surface py-section">
        <Container className="grid grid-cols-1 items-center gap-space-xl lg:grid-cols-[minmax(0,5fr)_minmax(0,7fr)] lg:gap-16">
          <div className="relative mx-auto aspect-square w-full max-w-sm overflow-hidden rounded-xl bg-[#fbfbfb]">
            {/* Official logo on its native white background */}
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={site.logo} alt={site.fullName} className="h-full w-full scale-[1.6] object-contain" />
          </div>
          <div>
            <Kicker>From the Editors</Kicker>
            <h2 className="mt-space-sm font-display text-headline-lg-mobile text-on-surface md:text-[44px] md:leading-[52px]">
              {nl.editor.name}
            </h2>
            <p className="mt-space-md text-body-md text-on-surface-variant md:text-body-lg">{nl.editor.body}</p>
            <div className="mt-space-lg flex flex-wrap gap-space-sm">
              {nl.editor.links.map((l) => (
                <a
                  key={l.label}
                  {...linkProps(l.href)}
                  className="inline-flex items-center gap-1 rounded-lg border border-white/15 px-space-md py-2 text-label-sm text-on-surface transition-colors hover:border-primary-container hover:text-primary-container"
                >
                  <Icon name={l.icon} size={16} className="text-primary-container" /> {l.label}
                </a>
              ))}
            </div>
            <div className="mt-space-lg">
              <CtaLink href="#subscribe">Receive GCFT Weekly</CtaLink>
            </div>
          </div>
        </Container>
      </section>

      {/* 6. Final call — accent band */}
      <section className="w-full bg-primary-container py-section text-on-primary">
        <Container className="grid grid-cols-1 items-center gap-space-xl lg:grid-cols-2">
          <div>
            <p className="text-[13px] font-bold uppercase tracking-[0.2em] text-on-primary/80">{nl.closingLine}</p>
            <h2 className="mt-space-sm font-display text-headline-lg-mobile md:text-[48px] md:leading-[56px]">{nl.finalTitle}</h2>
          </div>
          <div className="rounded-xl bg-surface p-space-lg shadow-float md:p-space-xl">
            <p className="mb-space-md text-label-md uppercase tracking-wider text-on-surface">Send me {nl.name}</p>
            <NewsletterSignup cta="Subscribe" compact />
          </div>
        </Container>
      </section>
    </main>
  );
}
