"use client";

import { useState } from "react";
import { upcomingEvents, weeklyGatherings } from "@/lib/content";
import { Container, CoverImage, Eyebrow, Icon, SectionTitle, linkProps } from "./ui";

type Tab = "week" | "upcoming";

export default function EventsSection() {
  const [tab, setTab] = useState<Tab>("week");

  const tabBtn = (id: Tab, label: string) => (
    <button
      type="button"
      role="tab"
      aria-selected={tab === id}
      onClick={() => setTab(id)}
      className={`rounded-full px-space-md py-space-xs text-label-md transition-all ${
        tab === id ? "bg-primary-container text-on-primary" : "text-on-surface-variant hover:text-on-surface"
      }`}
    >
      {label}
    </button>
  );

  return (
    <section id="events" className="w-full bg-surface-container-lowest py-section">
      <Container>
        <div className="mb-space-xl flex flex-col justify-between gap-space-md md:flex-row md:items-end">
          <div>
            <Eyebrow variant="dot" className="mb-space-xs">
              Worship With Us
            </Eyebrow>
            <SectionTitle>Service Times</SectionTitle>
            <p className="mt-space-xs text-body-sm text-on-surface-variant">All times are West Africa Time (WAT).</p>
          </div>
          <div role="tablist" className="flex items-center self-start rounded-full bg-surface-container-high p-1 md:self-auto">
            {tabBtn("week", "Weekly Services")}
            {tabBtn("upcoming", "Special Gatherings")}
          </div>
        </div>

        {tab === "week" ? (
          <div role="tabpanel" className="grid grid-cols-1 gap-gutter md:grid-cols-2 lg:grid-cols-4">
            {weeklyGatherings.map((g) => (
              <article
                key={g.title}
                className="group flex flex-col justify-between overflow-hidden rounded-xl bg-surface-container-low shadow-md transition-all hover:bg-surface-container"
              >
                <div className="p-space-lg">
                  <div className="mb-space-sm flex items-center justify-between">
                    <span
                      className={`rounded px-space-xs py-0.5 text-label-sm font-bold uppercase ${
                        g.featured ? "bg-primary/20 text-primary" : "bg-surface-bright text-on-surface"
                      }`}
                    >
                      {g.day}
                    </span>
                    <Icon name={g.icon} className={g.featured ? "text-primary" : "text-secondary"} />
                  </div>
                  <h3 className="font-display text-headline-sm text-on-surface transition-colors group-hover:text-primary">
                    {g.title}
                  </h3>
                  <p className="mt-space-xs text-body-sm text-on-surface-variant">{g.body}</p>
                </div>
                <div className="flex items-center justify-between bg-surface-container/50 p-space-md">
                  <span className="text-label-sm text-primary">{g.time}</span>
                  <span className="text-label-sm text-secondary">{g.place}</span>
                </div>
              </article>
            ))}
          </div>
        ) : (
          <div role="tabpanel" className="grid grid-cols-1 gap-gutter md:grid-cols-3">
            {upcomingEvents.map((e) => (
              <article
                key={e.title}
                className="group flex flex-col overflow-hidden rounded-xl bg-surface-container-low shadow-lg transition-transform duration-300 hover:-translate-y-1"
              >
                <div className="relative h-48 overflow-hidden">
                  <CoverImage src={e.image} alt={e.title} />
                  <span
                    className={`absolute top-space-sm left-space-sm rounded px-space-xs py-0.5 text-label-sm font-bold uppercase ${
                      e.featured ? "bg-primary-container text-on-primary" : "bg-surface-bright text-on-surface"
                    }`}
                  >
                    {e.badge}
                  </span>
                </div>
                <div className="flex flex-1 flex-col justify-between p-space-md">
                  <div>
                    <span className="text-label-sm text-primary">{e.when}</span>
                    <h3 className="mt-1 font-display text-headline-sm text-on-surface transition-colors group-hover:text-primary">
                      {e.title}
                    </h3>
                    <p className="mt-space-xs text-body-sm text-on-surface-variant">{e.body}</p>
                  </div>
                  <div className="mt-space-md flex items-center justify-between pt-space-md">
                    <span className="text-label-sm text-on-surface-variant">{e.note}</span>
                    <a {...linkProps(e.cta.href)} className="inline-flex items-center gap-1 text-label-sm font-bold text-primary hover:underline">
                      {e.cta.label} <Icon name="arrow_forward" size={14} />
                    </a>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </Container>
    </section>
  );
}
