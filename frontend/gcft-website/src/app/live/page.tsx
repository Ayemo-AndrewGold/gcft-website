import type { Metadata } from "next";
import { JourneyBand, Kicker, PageHero, Pathways } from "@/components/about/AboutBlocks";
import { ReplayGrid } from "@/components/live/LiveBlocks";
import { Container, Icon, linkProps } from "@/components/ui";
import { livePages, socials } from "@/lib/content";
import { images } from "@/lib/images";
import { getLatestVideos, liveEmbedUrl } from "@/lib/youtube";

export const metadata: Metadata = {
  title: "Watch Live",
  description: "Watch the Sunday song service and the Word live from the Glorious Christian Fellowship Tabernacle, Ijoko.",
};

const schedule = [
  { day: "Sunday", time: "9:00 AM – 2:00 PM", note: "Song service & the Word · streamed live" },
  { day: "Tuesday", time: "6:30 PM – 8:30 PM", note: "Midweek service" },
  { day: "Thursday", time: "6:30 PM – 8:30 PM", note: "Midweek service" },
  { day: "Friday", time: "2:00 AM – 4:00 AM", note: "Night vigil" },
];

export default async function LivePage() {
  const videos = await getLatestVideos(6);

  return (
    <main className="w-full bg-surface">
      <PageHero title="Live Experience" current="Watch Live" crumbs={[{ name: "Live Experience" }]} tabs={livePages} image={images.hero} />

      {/* Live player */}
      <section className="w-full bg-surface pb-section">
        <Container>
          <div className="mb-space-lg flex items-center gap-space-sm">
            <span className="relative flex h-3 w-3">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-error opacity-75" />
              <span className="relative inline-flex h-3 w-3 rounded-full bg-error" />
            </span>
            <Kicker>Watch Live</Kicker>
          </div>
          <div className="grid grid-cols-1 gap-gutter lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
            <div>
              <div className="relative aspect-video overflow-hidden rounded-xl bg-surface-container-lowest shadow-float ring-1 ring-white/10">
                <iframe
                  src={liveEmbedUrl}
                  title="GCFT live stream"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  allowFullScreen
                  loading="lazy"
                  className="absolute inset-0 h-full w-full border-0"
                />
              </div>
              <p className="mt-space-sm text-body-sm text-on-surface-variant">
                When we are not live, the player shows our most recent stream or an offline notice.{" "}
                <a {...linkProps(socials.youtube)} className="text-primary-container hover:underline">
                  Open the channel on YouTube
                </a>
                .
              </p>
            </div>

            <aside className="flex flex-col rounded-xl border border-white/15 bg-surface-container-low p-space-lg">
              <h2 className="font-display text-headline-md text-on-surface">Sunday Song Service</h2>
              <p className="mt-space-xs text-body-md text-on-surface-variant">
                Join us live from the tabernacle in Ijoko, or wherever you are in the world.
              </p>
              <ul className="mt-space-lg flex flex-col divide-y divide-white/10">
                {schedule.map((s) => (
                  <li key={s.day} className="flex items-start justify-between gap-space-md py-3">
                    <span>
                      <span className="block text-label-md uppercase tracking-wider text-on-surface">{s.day}</span>
                      <span className="block text-body-sm text-on-surface-variant">{s.note}</span>
                    </span>
                    <span className="shrink-0 text-label-md text-primary-container">{s.time}</span>
                  </li>
                ))}
              </ul>
              <p className="mt-space-xs text-label-sm uppercase tracking-wider text-on-surface-variant">All times WAT</p>
              <div className="mt-auto flex flex-col gap-space-sm pt-space-lg">
                <a
                  {...linkProps(`https://www.youtube.com/channel/${socials.youtubeChannelId}?sub_confirmation=1`)}
                  className="inline-flex items-center justify-center gap-space-xs rounded-lg bg-primary-container py-3 text-label-md uppercase tracking-wider text-on-primary shadow-glow hover:bg-primary-fixed"
                >
                  <Icon name="notifications_active" size={18} /> Subscribe on YouTube
                </a>
                <a
                  {...linkProps(socials.facebook)}
                  className="inline-flex items-center justify-center gap-space-xs rounded-lg border border-white/80 py-3 text-label-md uppercase tracking-wider text-on-surface hover:border-primary-container hover:text-primary-container"
                >
                  <Icon name="live_tv" size={18} /> Also live on Facebook
                </a>
              </div>
            </aside>
          </div>
        </Container>
      </section>

      <ReplayGrid videos={videos} />
      <Pathways />
      <JourneyBand />
    </main>
  );
}
