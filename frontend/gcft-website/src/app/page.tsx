import Hero from "@/components/home/Hero";
import { Gatherings, Library, NewsletterBand, Pulpit, Scripture, Statement, Visit } from "@/components/home/Sections";
import { site } from "@/lib/content";
import { getLatestVideos } from "@/lib/youtube";

export default async function Home() {
  const videos = await getLatestVideos(5);

  return (
    <main className="w-full bg-surface">
      <Hero videoSrc={site.heroVideo} />
      <Statement />
      <Gatherings />
      <Scripture />
      <Pulpit videos={videos} />
      <Library />
      <NewsletterBand />
      <Visit />
    </main>
  );
}
