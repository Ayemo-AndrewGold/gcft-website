import type { Metadata } from "next";
import { JourneyBand, PageHero } from "@/components/about/AboutBlocks";
import { RecapIntro, ReplayGrid, WideBanner } from "@/components/live/LiveBlocks";
import { livePages, socials } from "@/lib/content";
import { images } from "@/lib/images";
import { getLatestVideos } from "@/lib/youtube";

export const metadata: Metadata = {
  title: "Conventions",
  description: "Convention messages from the Glorious Christian Fellowship Tabernacle — listen back and watch replays.",
};

export default async function ConventionsPage() {
  const videos = await getLatestVideos(6, /convention/i);

  return (
    <main className="w-full bg-surface">
      <PageHero
        title="Conventions"
        current="Conventions"
        crumbs={[{ name: "Live Experience", href: "/live" }, { name: "Conventions" }]}
        tabs={livePages}
        image={images.eventSummit}
      />

      <RecapIntro
        image={images.seriesJohn}
        badge="Convention Messages"
        kicker="Replay the Experience"
        title="Convention Messages"
        primary={{ label: "Browse Messages", href: "https://gcftchurch.org/convention-messages/", icon: "headphones" }}
        secondary={{ label: "Listen on Spotify", href: socials.spotify, icon: "podcasts" }}
      >
        <p>
          Messages preached at GCFT conventions are available to stream on gcftchurch.org, on our YouTube channel, and on
          the GCFT podcast.
        </p>
        <p>Missed a session? Listen back, share it with a friend, and stay rooted in the undiluted Word.</p>
      </RecapIntro>

      <WideBanner image={images.hero} caption="The Undiluted Word, Preached." sub="Malachi 4:5–6b · Revelation 10:7" />
      <ReplayGrid videos={videos} title="Convention Replays" />
      <JourneyBand />
    </main>
  );
}
