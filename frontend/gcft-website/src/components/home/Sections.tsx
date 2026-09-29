/*
 * Landing page sections (v2). Server components; client islands are imported.
 */
import { messages, resources, site, socials } from "@/lib/content";
import { images } from "@/lib/images";
import { mapEmbed } from "@/lib/pages";
import { gatherings, to12h } from "@/lib/schedule";
import type { YouTubeVideo } from "@/lib/youtube";
import { NewsletterSignup } from "../forms/MailtoForms";
import { Container, Icon, linkProps } from "../ui";
import { Accent, ArrowLink, Button, LiveDot, SectionHead } from "./primitives";
import Reveal from "./Reveal";

/* ------------------------------------------------------------------ */
/* 01 — Who we are                                                     */
/* ------------------------------------------------------------------ */
const pillars = [
  { k: "Non-denominational", v: "An independent fellowship with no central headquarters and no general overseer." },
  { k: "Apostolic doctrine", v: "Restoring the faith to the truths delivered to the early Apostles." },
  { k: "End-time message", v: "Grounded in Malachi 4:5–6b and Revelation 10:7." },
];

export function Statement() {
  return (
    <section id="about" className="bg-surface py-24 md:py-36">
      <Container>
        <SectionHead index="01" label="Who we are" aside={<ArrowLink href="/about">About GCFT</ArrowLink>} />
        <Reveal>
          <p className="mt-12 max-w-5xl text-[28px] leading-[1.25] font-normal tracking-[-0.025em] text-on-surface md:mt-16 md:text-[44px] md:leading-[1.15]">
            {site.fullName} is a non-denominational, Bible-believing church in Ijoko, Sango Ota.{" "}
            <span className="text-on-surface-variant">
              We exist to preach the undiluted Word of God — and to call a generation <Accent>back to the Bible.</Accent>
            </span>
          </p>
        </Reveal>

        <dl className="mt-16 grid grid-cols-1 border-t border-hairline md:mt-24 md:grid-cols-3">
          {pillars.map((p, i) => (
            <Reveal
              key={p.k}
              delay={i * 90}
              className={`py-8 md:py-10 ${i > 0 ? "border-t border-hairline md:border-t-0 md:border-l md:pl-8" : ""} ${
                i < pillars.length - 1 ? "md:pr-8" : ""
              }`}
            >
              <dt className="flex items-baseline gap-3">
                <span className="font-mono text-[11px] text-on-surface-variant">0{i + 1}</span>
                <span className="text-[20px] font-medium tracking-[-0.015em] text-on-surface">{p.k}</span>
              </dt>
              <dd className="mt-3 max-w-sm text-body-md text-on-surface-variant">{p.v}</dd>
            </Reveal>
          ))}
        </dl>
      </Container>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* 02 — Worship with us                                                */
/* ------------------------------------------------------------------ */
export function Gatherings() {
  return (
    <section id="events" className="bg-surface pb-24 md:pb-36">
      <Container>
        <SectionHead
          index="02"
          label="Worship with us"
          title={
            <>
              Four gatherings, <Accent>every week.</Accent>
            </>
          }
        />

        <div className="mt-14 grid grid-cols-1 gap-10 md:mt-20 lg:grid-cols-12 lg:gap-16">
          {/* Image */}
          <Reveal className="lg:col-span-5">
            <figure className="group relative aspect-[4/5] overflow-hidden rounded-2xl bg-surface-container">
              <div
                role="img"
                aria-label="Worship at the tabernacle"
                className="absolute inset-0 bg-cover bg-center transition-transform duration-[1.6s] ease-out-expo group-hover:scale-[1.04]"
                style={{ backgroundImage: `url('${images.aboutWorship}')` }}
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent" />
              <figcaption className="absolute inset-x-0 bottom-0 flex items-end justify-between gap-4 p-6">
                <span>
                  <span className="eyebrow block text-white/70">The Tabernacle</span>
                  <span className="mt-1 block text-[17px] text-white">{site.address.line1}</span>
                </span>
                <a
                  {...linkProps(site.mapsUrl)}
                  aria-label="Get directions"
                  className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-white text-surface transition-transform hover:scale-105"
                >
                  <Icon name="arrow_outward" size={18} />
                </a>
              </figcaption>
            </figure>
          </Reveal>

          {/* Schedule */}
          <div className="lg:col-span-7">
            <ol className="border-t border-hairline">
              {gatherings.map((g, i) => (
                <Reveal as="li" key={`${g.day}-${g.start}`} delay={i * 80} className="border-b border-hairline">
                  <div className="grid grid-cols-[72px_1fr_auto] items-baseline gap-4 py-7 md:grid-cols-[120px_1fr_auto] md:py-9">
                    <span className="eyebrow text-on-surface-variant">{g.dayName.slice(0, 3)}</span>
                    <div>
                      <p className="flex flex-wrap items-center gap-3 text-[22px] font-medium tracking-[-0.02em] text-on-surface md:text-[28px]">
                        {g.name}
                        {g.live && (
                          <span className="eyebrow inline-flex items-center gap-1.5 rounded-full border border-hairline-strong px-2.5 py-1 text-[10px] text-on-surface-variant">
                            <LiveDot /> Streamed
                          </span>
                        )}
                      </p>
                      <p className="mt-1 text-body-sm text-on-surface-variant">{g.note}</p>
                    </div>
                    <p className="text-right font-mono text-[13px] text-on-surface tabular-nums md:text-[15px]">
                      {to12h(g.start)}
                      <span className="block text-on-surface-variant">– {to12h(g.end)}</span>
                    </p>
                  </div>
                </Reveal>
              ))}
            </ol>
            <div className="mt-8 flex flex-col justify-between gap-6 sm:flex-row sm:items-center">
              <p className="eyebrow text-on-surface-variant">All times West Africa Time (UTC+1)</p>
              <div className="flex gap-6">
                <ArrowLink href={site.mapsUrl} external>
                  Directions
                </ArrowLink>
                <ArrowLink href="/live">Watch online</ArrowLink>
              </div>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* Interlude — scripture                                               */
/* ------------------------------------------------------------------ */
export function Scripture() {
  return (
    <section className="relative overflow-hidden border-y border-hairline bg-surface-container-lowest py-28 md:py-44">
      <div
        aria-hidden="true"
        className="pointer-events-none absolute top-1/2 left-1/2 h-[600px] w-[900px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-primary-container/[0.05] blur-[120px]"
      />
      <Container className="relative">
        <Reveal>
          <figure className="mx-auto max-w-5xl text-center">
            <blockquote className="font-serif text-[30px] leading-[1.2] font-light tracking-[-0.02em] text-on-surface italic md:text-[58px] md:leading-[1.1]">
              “Behold, I will send you Elijah the prophet… and he shall turn the heart of the fathers to the children, and
              the heart of the children to their fathers.”
            </blockquote>
            <figcaption className="eyebrow mt-10 flex items-center justify-center gap-3 text-on-surface-variant">
              <span className="h-px w-8 bg-primary-container" />
              Malachi 4:5–6 · KJV
              <span className="h-px w-8 bg-primary-container" />
            </figcaption>
          </figure>
        </Reveal>
      </Container>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* 03 — From the pulpit                                                */
/* ------------------------------------------------------------------ */
function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
}

export function Pulpit({ videos }: { videos: YouTubeVideo[] }) {
  const [feature, ...rest] = videos;
  return (
    <section id="teachings" className="bg-surface py-24 md:py-36">
      <Container>
        <SectionHead
          index="03"
          label="From the pulpit"
          title={
            <>
              The Word, preached <Accent>without dilution.</Accent>
            </>
          }
          aside={
            <ArrowLink href={socials.youtube} external>
              All messages
            </ArrowLink>
          }
        />

        {feature ? (
          <div className="mt-14 grid grid-cols-1 gap-10 md:mt-20 lg:grid-cols-12 lg:gap-12">
            {/* Featured video */}
            <Reveal className="lg:col-span-7">
              <a {...linkProps(feature.url)} className="group block">
                <div className="relative aspect-video overflow-hidden rounded-2xl bg-surface-container">
                  <div
                    className="absolute inset-0 bg-cover bg-center transition-transform duration-[1.6s] ease-out-expo group-hover:scale-[1.03]"
                    style={{ backgroundImage: `url('${feature.thumbnail}')` }}
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  <span className="absolute bottom-5 left-5 flex h-14 w-14 items-center justify-center rounded-full bg-white text-surface transition-transform duration-500 ease-out-expo group-hover:scale-110">
                    <Icon name="play_arrow" size={28} fill />
                  </span>
                  <span className="eyebrow absolute top-5 left-5 rounded-full bg-black/50 px-3 py-1.5 text-white backdrop-blur">
                    Latest
                  </span>
                </div>
                <p className="eyebrow mt-6 text-on-surface-variant">{formatDate(feature.published)}</p>
                <h3 className="mt-2 max-w-2xl text-[24px] leading-[1.2] font-medium tracking-[-0.02em] text-on-surface transition-colors group-hover:text-primary-container md:text-[30px]">
                  {feature.title}
                </h3>
              </a>
            </Reveal>

            {/* More */}
            <ol className="flex flex-col border-t border-hairline lg:col-span-5">
              {rest.slice(0, 4).map((v, i) => (
                <Reveal as="li" key={v.id} delay={i * 80} className="border-b border-hairline">
                  <a {...linkProps(v.url)} className="group grid grid-cols-[112px_1fr] gap-5 py-5">
                    <div className="relative aspect-video overflow-hidden rounded-lg bg-surface-container">
                      <div
                        className="absolute inset-0 bg-cover bg-center transition-transform duration-700 group-hover:scale-105"
                        style={{ backgroundImage: `url('${v.thumbnail}')` }}
                      />
                    </div>
                    <div className="min-w-0">
                      <p className="eyebrow text-on-surface-variant">{formatDate(v.published)}</p>
                      <p className="mt-1.5 line-clamp-2 text-[16px] leading-snug font-medium text-on-surface transition-colors group-hover:text-primary-container">
                        {v.title}
                      </p>
                    </div>
                  </a>
                </Reveal>
              ))}
            </ol>
          </div>
        ) : (
          /* Fallback when the YouTube feed is unavailable */
          <ol className="mt-14 border-t border-hairline md:mt-20">
            {messages.map((m, i) => (
              <Reveal as="li" key={m.title} delay={i * 60} className="border-b border-hairline">
                <a {...linkProps(m.href)} className="group grid grid-cols-[40px_1fr_auto] items-center gap-4 py-6 md:grid-cols-[80px_1fr_200px_auto]">
                  <span className="font-mono text-[12px] text-on-surface-variant">{String(i + 1).padStart(2, "0")}</span>
                  <span className="text-[20px] font-medium tracking-[-0.015em] text-on-surface transition-colors group-hover:text-primary-container md:text-[24px]">
                    {m.title}
                  </span>
                  <span className="hidden text-body-sm text-on-surface-variant md:block">{m.topic}</span>
                  <Icon name="arrow_outward" size={20} className="text-on-surface-variant transition-colors group-hover:text-primary-container" />
                </a>
              </Reveal>
            ))}
          </ol>
        )}

        {/* Platforms */}
        <div className="mt-14 flex flex-wrap items-center gap-x-8 gap-y-4 md:mt-20">
          <span className="eyebrow text-on-surface-variant">Listen & watch on</span>
          <ArrowLink href={socials.youtube} external>
            YouTube
          </ArrowLink>
          <ArrowLink href={socials.spotify} external>
            Spotify
          </ArrowLink>
          <ArrowLink href={socials.facebook} external>
            Facebook
          </ArrowLink>
          <ArrowLink href={site.website} external>
            gcftchurch.org
          </ArrowLink>
        </div>
      </Container>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* 04 — Library                                                        */
/* ------------------------------------------------------------------ */
const shelves = [
  { title: "Read", type: "guides" as const, icon: "menu_book" },
  { title: "Listen", type: "audio" as const, icon: "headphones" },
  { title: "Watch", type: "video" as const, icon: "smart_display" },
];

export function Library() {
  return (
    <section id="archives" className="border-t border-hairline bg-surface-container-lowest py-24 md:py-36">
      <Container>
        <SectionHead
          index="04"
          label="GCFT Media"
          title={
            <>
              Read. Listen. <Accent>Watch.</Accent>
            </>
          }
          aside={
            <ArrowLink href="https://gcftchurch.org/sermons/" external>
              Sermon library
            </ArrowLink>
          }
        />
        <div className="mt-14 grid grid-cols-1 gap-12 md:mt-20 md:grid-cols-3 md:gap-8">
          {shelves.map((shelf, si) => (
            <Reveal key={shelf.title} delay={si * 100}>
              <div className="flex items-center justify-between border-b border-hairline-strong pb-4">
                <h3 className="text-[22px] font-medium tracking-[-0.02em] text-on-surface">{shelf.title}</h3>
                <Icon name={shelf.icon} size={20} className="text-on-surface-variant" />
              </div>
              <ul>
                {resources
                  .filter((r) => r.type === shelf.type)
                  .map((r) => (
                    <li key={r.title} className="border-b border-hairline">
                      <a {...linkProps(r.href)} className="group flex items-start justify-between gap-4 py-5">
                        <span className="min-w-0">
                          <span className="eyebrow block text-on-surface-variant">{r.kind}</span>
                          <span className="mt-1.5 block text-[17px] leading-snug text-on-surface transition-colors group-hover:text-primary-container">
                            {r.title}
                          </span>
                          <span className="mt-1 block text-body-sm text-on-surface-variant">{r.author}</span>
                        </span>
                        <Icon
                          name="arrow_outward"
                          size={18}
                          className="mt-5 shrink-0 text-on-surface-variant transition-all duration-500 ease-out-expo group-hover:translate-x-0.5 group-hover:-translate-y-0.5 group-hover:text-primary-container"
                        />
                      </a>
                    </li>
                  ))}
              </ul>
            </Reveal>
          ))}
        </div>
      </Container>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* Newsletter band                                                     */
/* ------------------------------------------------------------------ */
export function NewsletterBand() {
  return (
    <section className="bg-surface py-24 md:py-32">
      <Container>
        <Reveal className="grid grid-cols-1 items-end gap-10 rounded-3xl border border-hairline bg-surface-container-low p-8 md:p-14 lg:grid-cols-12">
          <div className="lg:col-span-6">
            <p className="eyebrow text-primary-container">GCFT Weekly</p>
            <h2 className="mt-5 text-[32px] leading-[1.05] font-medium tracking-[-0.035em] text-on-surface md:text-[48px]">
              Stay rooted in the Word, <Accent>all week.</Accent>
            </h2>
            <p className="mt-5 max-w-md text-body-md text-on-surface-variant">
              Sermon reviews, the Word for the week, and news of services, vigils and camp meetings.
            </p>
          </div>
          <div className="lg:col-span-6">
            <NewsletterSignup cta="Subscribe" compact />
            <p className="mt-4 text-body-sm text-on-surface-variant">
              Or read it online —{" "}
              <a href="/newsletter" className="text-on-surface underline decoration-hairline-strong underline-offset-4 hover:decoration-current">
                see what’s inside
              </a>
              .
            </p>
          </div>
        </Reveal>
      </Container>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* 05 — Visit                                                          */
/* ------------------------------------------------------------------ */
export function Visit() {
  return (
    <section id="contact" className="bg-surface pb-24 md:pb-36">
      <Container>
        <SectionHead index="05" label="Visit" />
        <div className="mt-12 grid grid-cols-1 gap-12 md:mt-16 lg:grid-cols-12 lg:gap-16">
          <Reveal className="lg:col-span-5">
            <h2 className="text-[34px] leading-[1.05] font-medium tracking-[-0.035em] text-on-surface md:text-[56px]">
              Come as you are. <Accent>You’re welcome here.</Accent>
            </h2>
            <address className="mt-12 grid grid-cols-1 gap-8 not-italic sm:grid-cols-2 lg:grid-cols-1">
              <div>
                <p className="eyebrow text-on-surface-variant">Address</p>
                <p className="mt-2 text-[17px] leading-relaxed text-on-surface">
                  {site.address.line1}
                  <br />
                  {site.address.line2}
                  <br />
                  {site.address.line3}
                </p>
              </div>
              <div>
                <p className="eyebrow text-on-surface-variant">Contact</p>
                <p className="mt-2 flex flex-col gap-1 text-[17px] text-on-surface">
                  <a href={site.phoneHref} className="hover:text-primary-container">
                    {site.phone}
                  </a>
                  <a href={`mailto:${site.email}`} className="break-all hover:text-primary-container">
                    {site.email}
                  </a>
                </p>
              </div>
            </address>
            <div className="mt-12 flex flex-col gap-3 xs:flex-row">
              <Button href={site.mapsUrl} variant="light" icon={<Icon name="near_me" size={18} />}>
                Get directions
              </Button>
              <Button href="/contact" variant="ghost">
                Send a message
              </Button>
            </div>
          </Reveal>

          <Reveal delay={120} className="lg:col-span-7">
            <div className="relative h-[380px] overflow-hidden rounded-2xl border border-hairline bg-surface-container md:h-full md:min-h-[520px]">
              <iframe
                title="Map to the Glorious Christian Fellowship Tabernacle"
                src={mapEmbed}
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
                className="absolute inset-0 h-full w-full border-0 [filter:grayscale(1)_invert(0.92)_contrast(0.9)]"
              />
              <div className="pointer-events-none absolute inset-0 ring-1 ring-inset ring-white/5" />
            </div>
          </Reveal>
        </div>
      </Container>
    </section>
  );
}
