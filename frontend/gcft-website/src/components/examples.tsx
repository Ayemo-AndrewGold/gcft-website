import { Container, Footer, Header, HeroSection, SectionTitle, ServiceBar } from "@/components";

// Example 1: Hero with a custom background video
export function CustomVideoHeroExample() {
  return <HeroSection videoSrc="https://res.cloudinary.com/<cloud>/video/upload/<id>.mp4" />;
}

// Example 2: Page shell (header + footer) for other routes
export function PageShellExample() {
  return (
    <>
      <Header
        navLinks={[
          { name: "Home", href: "/" },
          { name: "About", href: "/about" },
          { name: "Teachings", href: "/teachings" },
        ]}
      />
      <main className="min-h-screen bg-surface pt-20">
        <Container className="py-section">
          <SectionTitle>Page Content</SectionTitle>
          <p className="mt-space-sm text-body-md text-on-surface-variant">Other page content goes here…</p>
        </Container>
      </main>
      <Footer />
      <ServiceBar />
    </>
  );
}
