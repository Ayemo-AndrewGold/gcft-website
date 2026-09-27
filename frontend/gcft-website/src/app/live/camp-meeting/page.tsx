import type { Metadata } from "next";
import { MinistryCards, PageHero } from "@/components/about/AboutBlocks";
import { RecapIntro, ReplayGrid, WideBanner } from "@/components/live/LiveBlocks";
import { livePages, socials } from "@/lib/content";
import { images } from "@/lib/images";
import { getLatestVideos } from "@/lib/youtube";

export const metadata: Metadata = {
  title: "Camp Meeting",
  description: "The annual GCFT Camp Meeting — days set apart for teaching, consecration and fellowship.",
};

export default async function CampMeetingPage() {
  const videos = await getLatestVideos(6, /camp/i);

  return (
    <main className="w-full bg-surface">
      <PageHero
        title="Camp Meeting"
        current="Camp Meeting"
        crumbs={[{ name: "Live Experience", href: "/live" }, { name: "Camp Meeting" }]}
        tabs={livePages}
        image={images.eventRetreat}
      />

      <RecapIntro
        image={images.eventWorshipNight}
        badge="Annual Gathering"
        kicker="Replay the Experience"
        title="GCFT Camp Meeting"
        primary={{ label: "Camp Meeting Materials", href: "https://gcftchurch.org/category/camp-meeting/", icon: "menu_book" }}
        secondary={{ label: "Watch on YouTube", href: socials.youtube, icon: "smart_display" }}
      >
        <p>
          Each year the Glorious Christian Fellowship Tabernacle sets apart days for camp meeting — a season of teaching,
          consecration and fellowship with believers of like precious faith.
        </p>
        <p>
          Messages and study materials from past camp meetings are published by GCFT Media. Dates for the next camp
          meeting are announced on our channels and in GCFT Weekly.
        </p>
      </RecapIntro>

      <WideBanner image={images.eventRetreat} caption="Come Apart & Rest Awhile." sub="Mark 6:31 — dates announced on our channels." />
      <ReplayGrid videos={videos} title="Camp Meeting Replays" />
      <MinistryCards className="bg-surface" />
    </main>
  );
}
