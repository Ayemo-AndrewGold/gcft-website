import Link from "next/link";
import { footerLinks, serviceBarItems, site, socials } from "@/lib/content";
import { gatherings, to12h } from "@/lib/schedule";
import { Logo } from "./Header";
import { Container, Icon, linkProps } from "./ui";

/** Slim frosted bar pinned to the bottom of the viewport with a looping announcement marquee. */
export function ServiceBar() {
  return (
    <aside className="fixed inset-x-0 bottom-0 z-40 border-t border-hairline bg-surface/85 backdrop-blur-xl backdrop-saturate-150">
      <Container className="flex h-10 items-center justify-between gap-6">
        <div className="flex min-w-0 flex-1 items-center gap-4">
          <span className="eyebrow inline-flex shrink-0 items-center gap-2 text-[10px] text-error">
            <span className="relative inline-flex h-1.5 w-1.5">
              <span className="absolute inset-0 animate-ping rounded-full bg-error opacity-60" />
              <span className="relative h-1.5 w-1.5 rounded-full bg-error" />
            </span>
            Live Sundays
          </span>
          <span aria-hidden="true" className="h-3 w-px shrink-0 bg-hairline-strong" />
          <div
            role="marquee"
            aria-label="Service announcements"
            className="group relative min-w-0 flex-1 overflow-hidden [mask-image:linear-gradient(to_right,transparent,black_32px,black_calc(100%-32px),transparent)]"
          >
            <div className="flex w-max animate-marquee [animation-duration:45s] group-hover:[animation-play-state:paused] motion-reduce:animate-none">
              {[0, 1].map((copy) => (
                <ul key={copy} aria-hidden={copy === 1} className="flex shrink-0 items-center">
                  {serviceBarItems.map((it) => (
                    <li key={it.text} className="eyebrow inline-flex items-center text-[10px] text-white/60">
                      {it.text}
                      <span aria-hidden="true" className="px-6 text-white/20">
                        /
                      </span>
                    </li>
                  ))}
                </ul>
              ))}
            </div>
          </div>
        </div>
        <Link
          href="/live"
          className="eyebrow hidden shrink-0 items-center gap-1.5 text-[10px] text-white transition-colors hover:text-primary-container sm:inline-flex"
        >
          Join stream <Icon name="arrow_outward" size={14} />
        </Link>
      </Container>
    </aside>
  );
}

export default function Footer() {
  const colHead = "eyebrow mb-5 text-on-surface-variant";
  const linkCls = "text-[15px] text-on-surface/80 transition-colors hover:text-white";

  return (
    <footer className="relative w-full overflow-hidden border-t border-hairline bg-surface-container-lowest pt-20 pb-16 md:pt-28">
      <Container>
        {/* CTA row */}
        <div className="grid grid-cols-1 gap-10 border-b border-hairline pb-16 md:grid-cols-12 md:pb-20">
          <div className="md:col-span-7">
            <h2 className="text-[34px] leading-[1.05] font-medium tracking-[-0.035em] text-on-surface md:text-[52px]">
              Join us this Sunday
              <span className="font-serif font-light text-on-surface-variant italic"> — 9:00 AM WAT.</span>
            </h2>
          </div>
          <div className="flex flex-col gap-3 xs:flex-row md:col-span-5 md:items-end md:justify-end">
            <Link
              href="/live"
              className="inline-flex h-12 items-center justify-center gap-2 rounded-full bg-primary-container px-6 text-[15px] font-medium text-on-primary transition-colors hover:bg-primary-fixed"
            >
              Watch live
            </Link>
            <a
              {...linkProps(site.mapsUrl)}
              className="inline-flex h-12 items-center justify-center gap-2 rounded-full border border-hairline-strong px-6 text-[15px] text-on-surface transition-colors hover:border-white/40"
            >
              Get directions
            </a>
          </div>
        </div>

        {/* Columns */}
        <div className="grid grid-cols-2 gap-x-6 gap-y-12 py-16 md:grid-cols-12 md:py-20">
          <div className="col-span-2 md:col-span-4">
            <Logo className="h-20" />
            <p className="mt-6 max-w-xs font-serif text-[19px] leading-snug font-light text-on-surface italic">{site.tagline}</p>
            <div className="mt-8 flex gap-2">
              {footerLinks.social.map((s) => (
                <a
                  key={s.label}
                  {...linkProps(s.href)}
                  aria-label={s.label}
                  className="flex h-10 w-10 items-center justify-center rounded-full border border-hairline text-on-surface-variant transition-colors hover:border-white/40 hover:text-white"
                >
                  <Icon name={s.icon} size={18} />
                </a>
              ))}
            </div>
          </div>

          <nav aria-label="Explore" className="md:col-span-2">
            <p className={colHead}>Explore</p>
            <ul className="flex flex-col gap-3">
              {footerLinks.quick.map((l) => (
                <li key={l.name}>
                  <Link href={l.href} className={linkCls}>
                    {l.name}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          <nav aria-label="Media" className="md:col-span-2">
            <p className={colHead}>Media</p>
            <ul className="flex flex-col gap-3">
              {footerLinks.involved.map((l) => (
                <li key={l.name}>
                  <a {...linkProps(l.href)} className={linkCls}>
                    {l.name}
                  </a>
                </li>
              ))}
            </ul>
          </nav>

          <div className="col-span-2 md:col-span-4">
            <p className={colHead}>Gatherings · WAT</p>
            <ul className="border-t border-hairline">
              {gatherings.map((g) => (
                <li key={`${g.day}-${g.start}`} className="flex items-baseline justify-between gap-4 border-b border-hairline py-3">
                  <span className="text-[15px] text-on-surface">{g.dayName}</span>
                  <span className="font-mono text-[13px] text-on-surface-variant tabular-nums">
                    {to12h(g.start)} – {to12h(g.end)}
                  </span>
                </li>
              ))}
            </ul>
            <address className="mt-6 text-[15px] leading-relaxed text-on-surface-variant not-italic">
              {site.address.line1}, {site.address.line2}, {site.address.line3}
              <br />
              <a href={site.phoneHref} className="text-on-surface hover:text-white">
                {site.phone}
              </a>
              {" · "}
              <a href={`mailto:${site.email}`} className="break-all text-on-surface hover:text-white">
                {site.email}
              </a>
            </address>
          </div>
        </div>

        {/* Legal */}
        <div className="flex flex-col justify-between gap-4 border-t border-hairline pt-8 md:flex-row md:items-center">
          <p className="eyebrow text-on-surface-variant">
            © {new Date().getFullYear()} {site.fullName}
          </p>
          <p className="eyebrow text-on-surface-variant">
            Malachi 4:5–6b · Revelation 10:7 ·{" "}
            <a {...linkProps(socials.youtube)} className="hover:text-white">
              @christftchurch
            </a>
          </p>
        </div>
      </Container>

      {/* Oversized wordmark */}
      <p
        aria-hidden="true"
        className="pointer-events-none mt-16 text-center text-[27vw] leading-[0.75] font-semibold tracking-[-0.07em] text-white/[0.035] select-none"
      >
        GCFT
      </p>
    </footer>
  );
}
