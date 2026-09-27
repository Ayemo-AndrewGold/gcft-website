import HeroSection from "@/components/HeroSection";
import AboutSection from "@/components/AboutSection";
import EventsSection from "@/components/EventsSection";
import TeachingsSection from "@/components/TeachingsSection";
import ArchivesSection from "@/components/ArchivesSection";
import ContactSection from "@/components/ContactSection";
import { site } from "@/lib/content";

export default function Home() {
  return (
    <main className="w-full bg-surface">
      <HeroSection videoSrc={site.heroVideo} />
      <AboutSection />
      <EventsSection />
      <TeachingsSection />
      <ArchivesSection />
      <ContactSection />
    </main>
  );
}
