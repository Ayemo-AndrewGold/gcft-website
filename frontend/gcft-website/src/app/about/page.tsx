import type { Metadata } from "next";
import { IntroSplit, JourneyBand, MinistryCards, PageHero, Pathways } from "@/components/about/AboutBlocks";
import { whoWeAre } from "@/lib/about";
import { images } from "@/lib/images";

export const metadata: Metadata = {
  title: "About — Who We Are",
  description:
    "Glorious Christian Fellowship Tabernacle is an independent, non-denominational, Bible-believing church in Ijoko, Sango Ota, Ogun State.",
};

export default function AboutPage() {
  return (
    <main className="w-full bg-surface">
      <PageHero title="About GCFT" current="Who We Are" image={images.hero} />
      <IntroSplit intro={whoWeAre} />
      <Pathways />
      <MinistryCards />
      <JourneyBand />
    </main>
  );
}
