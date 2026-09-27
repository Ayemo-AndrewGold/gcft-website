import type { Metadata } from "next";
import { IntroSplit, MinistryCards, PageHero, Pathways } from "@/components/about/AboutBlocks";
import { ScriptureList } from "@/components/about/SubpageBlocks";
import { theMessage } from "@/lib/about";
import { images } from "@/lib/images";

export const metadata: Metadata = {
  title: "The Message",
  description: "The end-time message of Malachi 4:5–6b and Revelation 10:7 at the Glorious Christian Fellowship Tabernacle.",
};

export default function MessagePage() {
  return (
    <main className="w-full bg-surface">
      <PageHero title="The Message" current="The Message" image={images.seriesJohn} />
      <IntroSplit intro={theMessage} />
      <ScriptureList />
      <Pathways />
      <MinistryCards />
    </main>
  );
}
