import { site, socials } from "@/lib/content";
import { Container, Eyebrow, Icon, SectionTitle, linkProps } from "./ui";

const rows = [
  {
    icon: "location_on",
    label: "Address",
    value: (
      <>
        {site.address.line1}
        <br />
        {site.address.line2}
        <br />
        {site.address.line3}
      </>
    ),
    href: site.mapsUrl,
  },
  { icon: "call", label: "Phone", value: site.phone, href: site.phoneHref },
  { icon: "mail", label: "Email", value: site.email, href: `mailto:${site.email}` },
];

export default function ContactSection() {
  return (
    <section id="contact" className="w-full bg-surface py-section">
      <Container>
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-surface-container-low via-surface-container to-surface-container-low p-space-lg shadow-2xl md:p-space-xl">
          <div className="pointer-events-none absolute -right-20 -bottom-20 h-80 w-80 rounded-full bg-primary/10 blur-3xl" />

          <div className="relative z-10 grid grid-cols-1 gap-space-xl lg:grid-cols-2 lg:items-center">
            <div>
              <Eyebrow className="mb-space-xs">Visit Us</Eyebrow>
              <SectionTitle className="mb-space-xs">Worship With Us in Ijoko</SectionTitle>
              <p className="mb-space-lg max-w-xl text-body-md text-on-surface-variant">
                Whether you are visiting for the first time or returning home, you are welcome at the Glorious Christian
                Fellowship Tabernacle. Can&apos;t make it in person? Join the Sunday song service live on YouTube.
              </p>
              <div className="flex flex-col gap-space-sm xs:flex-row xs:flex-wrap">
                <a
                  {...linkProps(site.mapsUrl)}
                  className="inline-flex items-center justify-center gap-space-xs rounded-lg bg-primary-container px-space-lg py-3 text-label-md text-on-primary shadow-glow transition-all hover:bg-primary-fixed"
                >
                  <Icon name="directions" size={18} /> Get Directions
                </a>
                <a
                  {...linkProps(socials.youtube)}
                  className="inline-flex items-center justify-center gap-space-xs rounded-lg border border-primary-container/45 px-space-lg py-3 text-label-md text-on-surface transition-all hover:border-primary-container hover:bg-primary-container/10"
                >
                  <Icon name="live_tv" size={18} /> Watch Online
                </a>
              </div>
            </div>

            <ul className="glass-1 flex flex-col divide-y divide-white/5 rounded-xl">
              {rows.map((r) => (
                <li key={r.label}>
                  <a {...linkProps(r.href)} className="group flex items-start gap-space-md p-space-md transition-colors hover:bg-white/[0.02]">
                    <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary-container/15 text-primary">
                      <Icon name={r.icon} />
                    </span>
                    <span className="min-w-0">
                      <span className="block text-label-sm uppercase tracking-wider text-on-surface-variant">{r.label}</span>
                      <span className="block break-words text-body-md text-on-surface transition-colors group-hover:text-primary">
                        {r.value}
                      </span>
                    </span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </Container>
    </section>
  );
}
