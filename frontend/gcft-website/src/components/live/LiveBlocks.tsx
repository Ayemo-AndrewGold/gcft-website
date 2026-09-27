/*
 * "Live Experience" blocks, modelled on feedbackfromthefuture.com's event
 * recap pages (INDABA): flyer + "Replay the experience" copy + CTAs, a wide
 * banner, and a grid of replays.
 */
import type { ReactNode } from "react";
import { socials } from "@/lib/content";
import type { YouTubeVideo } from "@/lib/youtube";
import { Kicker } from "../about/AboutBlocks";
import { Container, CoverImage, Icon, linkProps } from "../ui";

type Cta = { label: string; href: string; icon?: string };

function Button({ cta, variant }: { cta: Cta; variant: "solid" | "outline" }) {
  return (
    <a
      {...linkProps(cta.href)}
      className={`inline-flex items-center justify-center gap-space-xs rounded-lg px-space-xl py-3 text-label-md uppercase tracking-wider transition-all ${
        variant === "solid"
          ? "bg-primary-container text-on-primary shadow-glow hover:bg-primary-fixed"
          : "border border-white/80 text-on-surface hover:border-primary-container hover:text-primary-container"
      }`}
    >
      {cta.icon && <Icon name={cta.icon} size={18} />}
      {cta.label}
    </a>
  );
}

/** Flyer on the left, recap copy + two CTAs on the right. */
export function RecapIntro({
  image,
  badge,
  kicker,
  title,
  children,
  primary,
  secondary,
}: {
  image: string;
  badge?: string;
  kicker: string;
  title: string;
  children: ReactNode;
  primary: Cta;
  secondary?: Cta;
}) {
  return (
    <section className="w-full bg-surface pb-section">
      <Container className="grid grid-cols-1 items-center gap-space-xl lg:grid-cols-2 lg:gap-16">
        <div className="relative aspect-[4/5] overflow-hidden rounded-xl shadow-float ring-1 ring-white/10 sm:aspect-[4/3] lg:aspect-[4/5]">
          <CoverImage src={image} alt={title} />
          <div className="absolute inset-0 bg-gradient-to-t from-surface/80 to-transparent" />
          {badge && (
            <span className="absolute top-space-md left-space-md rounded bg-primary-container px-space-sm py-1 text-label-sm font-bold uppercase text-on-primary">
              {badge}
            </span>
          )}
        </div>
        <div>
          <Kicker>{kicker}</Kicker>
          <h2 className="mt-space-sm font-display text-headline-lg-mobile text-on-surface md:text-[44px] md:leading-[52px]">
            {title}
          </h2>
          <div className="mt-space-md flex flex-col gap-space-md text-body-md text-on-surface-variant md:text-body-lg">{children}</div>
          <div className="mt-space-xl flex flex-col gap-space-sm xs:flex-row xs:flex-wrap">
            <Button cta={primary} variant="solid" />
            {secondary && <Button cta={secondary} variant="outline" />}
          </div>
        </div>
      </Container>
    </section>
  );
}

/** Full-width banner image with a caption band. */
export function WideBanner({ image, caption, sub }: { image: string; caption: string; sub?: string }) {
  return (
    <section className="w-full bg-surface pb-section">
      <Container>
        <div className="relative aspect-[16/9] overflow-hidden rounded-xl md:aspect-[1536/863]">
          <CoverImage src={image} alt={caption} />
          <div className="absolute inset-0 bg-gradient-to-r from-surface/90 via-surface/40 to-transparent" />
          <div className="absolute inset-y-0 left-0 flex max-w-xl flex-col justify-center p-space-lg md:p-space-xl">
            <p className="font-display text-headline-lg-mobile text-on-surface md:text-headline-lg">{caption}</p>
            {sub && <p className="mt-space-sm text-body-md text-on-surface-variant">{sub}</p>}
          </div>
        </div>
      </Container>
    </section>
  );
}

/** Grid of recent YouTube uploads (falls back to a channel link). */
export function ReplayGrid({
  videos,
  kicker = "Replay the Experience",
  title = "Recent Services & Messages",
}: {
  videos: YouTubeVideo[];
  kicker?: string;
  title?: string;
}) {
  return (
    <section className="w-full bg-surface-container-lowest py-section">
      <Container>
        <div className="mb-space-xl flex flex-col justify-between gap-space-md md:flex-row md:items-end">
          <div>
            <Kicker>{kicker}</Kicker>
            <h2 className="mt-space-sm font-display text-headline-lg-mobile text-on-surface md:text-[44px] md:leading-[52px]">
              {title}
            </h2>
          </div>
          <a
            {...linkProps(socials.youtube)}
            className="inline-flex items-center gap-1 self-start text-label-md uppercase tracking-wider text-primary-container hover:underline md:self-auto"
          >
            All videos on YouTube <Icon name="arrow_outward" size={18} />
          </a>
        </div>

        {videos.length ? (
          <div className="grid grid-cols-1 gap-gutter sm:grid-cols-2 lg:grid-cols-3">
            {videos.map((v) => (
              <a key={v.id} {...linkProps(v.url)} className="group block">
                <div className="relative aspect-video overflow-hidden rounded-xl bg-surface-container">
                  <CoverImage src={v.thumbnail} alt={v.title} />
                  <div className="absolute inset-0 bg-surface/20 transition-colors group-hover:bg-surface/0" />
                  <span className="absolute inset-0 m-auto flex h-14 w-14 items-center justify-center rounded-full bg-primary-container text-on-primary shadow-glow transition-transform group-hover:scale-110">
                    <Icon name="play_arrow" size={30} fill />
                  </span>
                </div>
                <p className="mt-space-sm text-label-sm uppercase tracking-wider text-on-surface-variant">
                  {v.published &&
                    new Date(v.published).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
                </p>
                <h3 className="mt-1 line-clamp-2 font-body text-[18px] font-semibold text-on-surface transition-colors group-hover:text-primary-container">
                  {v.title}
                </h3>
              </a>
            ))}
          </div>
        ) : (
          <a
            {...linkProps(socials.youtube)}
            className="flex flex-col items-center gap-space-sm rounded-xl border border-white/15 p-space-xl text-center transition-colors hover:border-primary-container"
          >
            <Icon name="smart_display" size={40} className="text-primary-container" />
            <span className="font-display text-headline-sm text-on-surface">Watch replays on our YouTube channel</span>
            <span className="text-body-sm text-on-surface-variant">Nearly a thousand services and messages, free to stream.</span>
          </a>
        )}
      </Container>
    </section>
  );
}
