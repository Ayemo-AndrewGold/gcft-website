import { footerLinks, serviceBarItems, site, socials } from "@/lib/content";
import { Logo } from "./Header";
import { Container, Icon, linkProps } from "./ui";

const toneCls = {
  primary: "text-primary font-medium",
  secondary: "text-secondary",
  muted: "text-on-surface-variant",
} as const;

/** Frosted "live" bar pinned to the bottom of the viewport. */
export function ServiceBar() {
  const items = serviceBarItems.map((it) => ({ text: it.text, cls: toneCls[it.tone] }));
  return (
    <aside className="fixed inset-x-0 bottom-0 z-40 border-t border-outline-variant/30 bg-surface-container-lowest/90 py-space-xs backdrop-blur-md">
      <Container className="flex items-center justify-between gap-space-md">
        <div className="flex min-w-0 flex-1 items-center gap-space-md text-label-sm text-nowrap">
          <span className="inline-flex shrink-0 items-center gap-space-xs rounded bg-error-container px-space-xs py-0.5 text-[10px] font-bold uppercase tracking-wider text-on-error-container">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-error" />
            Live Sundays
          </span>

          {/* Infinite marquee carousel — content is duplicated so the loop is seamless */}
          <div
            className="group relative min-w-0 flex-1 overflow-hidden [mask-image:linear-gradient(to_right,transparent,black_24px,black_calc(100%-24px),transparent)]"
            aria-label="Service announcements"
            role="marquee"
          >
            <div className="flex w-max animate-marquee group-hover:[animation-play-state:paused] motion-reduce:animate-none">
              {[0, 1].map((copy) => (
                <ul key={copy} aria-hidden={copy === 1} className="flex shrink-0 items-center">
                  {items.map((it) => (
                    <li key={it.text} className="inline-flex items-center">
                      <span className={it.cls}>{it.text}</span>
                      <span className="px-space-md text-outline-variant" aria-hidden="true">
                        •
                      </span>
                    </li>
                  ))}
                </ul>
              ))}
            </div>
          </div>
        </div>
        <a {...linkProps(socials.youtube)} className="hidden shrink-0 items-center gap-space-xs text-label-sm text-primary hover:underline sm:inline-flex">
          <Icon name="live_tv" size={16} />
          Join Stream
        </a>
      </Container>
    </aside>
  );
}

export default function Footer() {
  const linkCls = "text-body-sm text-on-surface-variant transition-colors hover:text-on-surface";
  const headCls = "mb-space-xs text-label-md uppercase tracking-wider text-primary";

  return (
    <footer className="w-full border-t border-outline-variant/20 bg-surface-container-lowest pt-space-xl pb-24">
      <Container className="mb-space-xl grid grid-cols-1 gap-space-xl sm:grid-cols-2 lg:grid-cols-4 lg:gap-gutter">
        <div className="flex flex-col gap-space-sm">
          <Logo className="h-24" />
          <p className="mt-space-xs max-w-xs font-display text-body-lg italic text-primary">{site.tagline}</p>
          <p className="max-w-xs text-body-sm text-on-surface-variant">{site.description}</p>
        </div>

        <nav className="flex flex-col gap-space-xs" aria-label="Quick links">
          <span className={headCls}>Quick Links</span>
          {footerLinks.quick.map((l) => (
            <a key={l.name} {...linkProps(l.href)} className={linkCls}>
              {l.name}
            </a>
          ))}
        </nav>

        <nav className="flex flex-col gap-space-xs" aria-label="Get involved">
          <span className={headCls}>Media</span>
          {footerLinks.involved.map((l) => (
            <a key={l.name} {...linkProps(l.href)} className={linkCls}>
              {l.name}
            </a>
          ))}
        </nav>

        <div className="flex flex-col gap-space-md">
          <span className="text-label-md uppercase tracking-wider text-primary">Connect</span>
          <div className="flex items-center gap-space-md">
            {footerLinks.social.map((s) => (
              <a
                key={s.label}
                {...linkProps(s.href)}
                aria-label={s.label}
                className="flex h-9 w-9 items-center justify-center rounded-full bg-surface-container text-on-surface-variant transition-colors hover:bg-surface-container-high hover:text-primary"
              >
                <Icon name={s.icon} size={18} />
              </a>
            ))}
          </div>
          <address className="flex flex-col gap-space-xs text-body-sm not-italic text-on-surface-variant">
            <a {...linkProps(site.phoneHref)} className="inline-flex items-center gap-space-xs hover:text-on-surface">
              <Icon name="call" size={16} className="text-primary" /> {site.phone}
            </a>
            <a {...linkProps(`mailto:${site.email}`)} className="inline-flex items-center gap-space-xs break-all hover:text-on-surface">
              <Icon name="mail" size={16} className="text-primary" /> {site.email}
            </a>
            <a {...linkProps(site.mapsUrl)} className="inline-flex items-start gap-space-xs hover:text-on-surface">
              <Icon name="location_on" size={16} className="mt-0.5 text-primary" />
              <span>
                {site.address.line1}, {site.address.line2}, {site.address.line3}
              </span>
            </a>
          </address>
        </div>
      </Container>

      <Container className="flex flex-col items-center justify-between gap-space-md border-t border-outline-variant/10 pt-space-lg text-center md:flex-row md:text-left">
        <p className="text-label-sm text-secondary">{site.serviceSummary}</p>
        <p className="text-label-sm text-on-surface-variant">
          © {new Date().getFullYear()} {site.fullName}. All rights reserved.
        </p>
      </Container>
    </footer>
  );
}
