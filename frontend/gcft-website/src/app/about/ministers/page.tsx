import type { Metadata } from "next";
import { IntroSplit, MinistryCards, PageHero, Pathways } from "@/components/about/AboutBlocks";
import { MinisterCards } from "@/components/about/SubpageBlocks";
import { ministers } from "@/lib/about";
import { images } from "@/lib/images";

export const metadata: Metadata = {
  title: "Our Ministers",
  description: "The ministers of the Glorious Christian Fellowship Tabernacle — Pastor Billy Joseph and Pastor Gideon Toyosi.",
};

export default function MinistersPage() {
  return (
    <main className="w-full bg-surface">
      <PageHero title="Our Ministers" current="Our Ministers" image={images.aboutWorship} />
      <IntroSplit intro={ministers} />
      <MinisterCards />
      <Pathways />
      <MinistryCards />
    </main>
  );
}
