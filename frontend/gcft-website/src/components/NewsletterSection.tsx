"use client";

import { useEffect, useState } from "react";
import { site } from "@/lib/content";
import { Container, Icon } from "./ui";

export default function NewsletterSection() {
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (!done) return;
    const t = setTimeout(() => setDone(false), 5000);
    return () => clearTimeout(t);
  }, [done]);

  return (
    <section className="w-full bg-surface py-section">
      <Container>
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-surface-container-low via-surface-container to-surface-container-low p-space-lg shadow-2xl md:p-space-xl">
          <div className="pointer-events-none absolute -right-20 -bottom-20 h-80 w-80 rounded-full bg-primary/10 blur-3xl" />
          <div className="relative z-10 max-w-2xl">
            <div className="mb-space-xs inline-flex items-center gap-space-xs">
              <Icon name="mark_email_read" size={18} className="text-primary" />
              <span className="text-label-sm uppercase tracking-widest text-primary">Weekly Pastoral Letter</span>
            </div>
            <h2 className="mb-space-xs font-display text-headline-lg-mobile text-on-surface md:text-headline-lg">
              Reflections for the Weary &amp; Curious
            </h2>
            <p className="mb-space-md text-body-md text-on-surface-variant">
              Every Thursday morning, we send a short scripture reflection, upcoming gathering details, and recommended
              reading straight from our pastoral elders.
            </p>
            <form
              className="flex max-w-lg flex-col gap-space-xs sm:flex-row"
              onSubmit={(e) => {
                e.preventDefault();
                // TODO: connect to the backend newsletter endpoint.
                e.currentTarget.reset();
                setDone(true);
              }}
            >
              <label htmlFor="newsletter-email" className="sr-only">
                Email address
              </label>
              <input
                id="newsletter-email"
                type="email"
                required
                placeholder="Enter your email address"
                className="w-full rounded-lg border border-on-surface/15 bg-surface-container-lowest px-space-md py-3 text-body-sm text-on-surface placeholder:text-[#8e95a5] focus:border-primary-container focus:ring-1 focus:ring-primary-container/35 focus:outline-none"
              />
              <button
                type="submit"
                className="flex shrink-0 items-center justify-center gap-1 rounded-lg bg-primary-container px-space-xl py-3 text-label-md text-on-primary shadow-glow transition-all hover:bg-primary-fixed"
              >
                Subscribe Free
                <Icon name="arrow_forward" size={16} />
              </button>
            </form>
            {done && (
              <div
                role="status"
                className="mt-space-sm flex items-center gap-space-xs rounded-lg bg-surface-container-high p-space-sm text-body-sm text-primary"
              >
                <Icon name="check_circle" className="text-primary" />
                <span>Thank you for subscribing to {site.name} Weekly. Peace be with you.</span>
              </div>
            )}
          </div>
        </div>
      </Container>
    </section>
  );
}
