import type { Metadata } from "next";
import { IntroSplit, JourneyBand, PageHero, Pathways } from "@/components/about/AboutBlocks";
import { BeliefGrid } from "@/components/about/SubpageBlocks";
import { beliefs } from "@/lib/about";
import { images } from "@/lib/images";

export const metadata: Metadata = {
  title: "Our Beliefs",
  description: "Back to the Bible — what the Glorious Christian Fellowship Tabernacle believes.",
};

export default function BeliefsPage() {
  return (
    <main className="w-full bg-surface">
      <PageHero title="Our Beliefs" current="Our Beliefs" image={images.seriesPsalms} />
      <IntroSplit intro={beliefs} />
      <BeliefGrid />
      <Pathways />
      <JourneyBand />
    </main>
  );
}
