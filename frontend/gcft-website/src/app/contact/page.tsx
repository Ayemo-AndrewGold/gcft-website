import type { Metadata } from "next";
import { JourneyBand, Kicker, MinistryCards, PageHero } from "@/components/about/AboutBlocks";
import { EnquiryForm } from "@/components/forms/MailtoForms";
import { Container, Icon, linkProps } from "@/components/ui";
import { site } from "@/lib/content";
import { images } from "@/lib/images";
import { contactCards, mapEmbed } from "@/lib/pages";

export const metadata: Metadata = {
  title: "Contact Us",
  description: `Contact the Glorious Christian Fellowship Tabernacle — ${site.phone}, ${site.email}. 1 Salvation Avenue, Ijoko, Sango Ota, Ogun State.`,
};

export default function ContactPage() {
  return (
    <main className="w-full bg-surface">
      <PageHero title="Contact Us" current="Contact Us" crumbs={[{ name: "Contact Us" }]} showAboutTabs={false} image={images.aboutFellowship} />

      {/* 1. Highlight cards (Email / Call) */}
      <section className="w-full bg-surface pb-section">
        <Container>
          <div className="grid grid-cols-1 gap-gutter md:grid-cols-2">
            {contactCards.map((c) => (
              <article
                key={c.label}
                className="group flex flex-col gap-space-lg rounded-xl border border-white/15 bg-surface-container-low p-space-lg transition-all duration-300 hover:-translate-y-1 hover:border-primary-container sm:flex-row md:p-space-xl"
              >
                <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-primary-container text-on-primary shadow-glow">
                  <Icon name={c.icon} size={30} />
                </span>
                <div className="min-w-0">
                  <span className="text-[13px] font-bold uppercase tracking-[0.2em] text-primary-container">{c.label}</span>
                  <h2 className="mt-space-xs font-display text-headline-md text-on-surface">{c.title}</h2>
                  <p className="mt-space-sm text-body-md text-on-surface-variant">{c.body}</p>
                  <a
                    {...linkProps(c.link.href)}
                    className="mt-space-md inline-block break-all font-body text-[20px] font-semibold text-on-surface underline decoration-primary-container decoration-2 underline-offset-4 transition-colors hover:text-primary-container"
                  >
                    {c.link.text}
                  </a>
                </div>
              </article>
            ))}
          </div>
        </Container>
      </section>

      {/* 2. Enquiry form */}
      <section className="w-full bg-surface-container-lowest py-section">
        <Container>
          <div className="grid grid-cols-1 gap-space-xl lg:grid-cols-[minmax(0,5fr)_minmax(0,7fr)] lg:gap-16">
            <div>
              <Kicker>Contact Us</Kicker>
              <h2 className="mt-space-sm font-display text-headline-lg-mobile text-on-surface md:text-[44px] md:leading-[52px]">
                Make An Enquiry
              </h2>
              <p className="mt-space-md text-body-md text-on-surface-variant md:text-body-lg">
                Whether you have a question about our services, want prayer, or are planning your first visit, send us a
                message and we will respond.
              </p>
              <ul className="mt-space-lg flex flex-col gap-space-md text-body-md text-on-surface">
                <li className="flex items-start gap-space-sm">
                  <Icon name="location_on" className="mt-0.5 text-primary-container" />
                  <span>
                    {site.address.line1}
                    <br />
                    {site.address.line2}
                    <br />
                    {site.address.line3}
                  </span>
                </li>
                <li className="flex items-start gap-space-sm">
                  <Icon name="schedule" className="mt-0.5 text-primary-container" />
                  <span>
                    Sundays 9:00 AM – 2:00 PM
                    <br />
                    Tue & Thu 6:30 PM – 8:30 PM
                    <br />
                    Friday Vigil 2:00 AM – 4:00 AM <span className="text-on-surface-variant">(WAT)</span>
                  </span>
                </li>
              </ul>
            </div>
            <div className="rounded-xl border border-white/10 bg-surface-container-low p-space-lg md:p-space-xl">
              <EnquiryForm />
            </div>
          </div>
        </Container>
      </section>

      {/* 3. Map */}
      <section className="relative w-full bg-surface">
        <iframe
          title="Map to the Glorious Christian Fellowship Tabernacle, Ijoko"
          src={mapEmbed}
          loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
          className="block h-[420px] w-full border-0 grayscale-[70%] invert-[90%] hue-rotate-180 md:h-[480px]"
        />
        <div className="pointer-events-none absolute inset-x-0 bottom-0 p-margin-sm md:p-10 lg:p-margin">
          <a
            {...linkProps(site.mapsUrl)}
            className="glass-2 pointer-events-auto inline-flex max-w-md items-start gap-space-sm rounded-xl p-space-md shadow-float"
          >
            <Icon name="directions" className="text-primary-container" />
            <span>
              <span className="block text-label-sm uppercase tracking-wider text-primary-container">Get Directions</span>
              <span className="block text-body-sm text-on-surface">
                {site.address.line1}, {site.address.line2}
              </span>
            </span>
          </a>
        </div>
      </section>

      {/* 4–5. Shared blocks */}
      <MinistryCards className="bg-surface" />
      <JourneyBand />
    </main>
  );
}
