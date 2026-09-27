"use client";

import { useRef, useState } from "react";
import { messages, sermonSeries, teachingTopics } from "@/lib/content";
import { CarouselControls, Container, CoverImage, Eyebrow, Icon, SectionTitle, linkProps } from "./ui";
import { socials } from "@/lib/content";

export default function TeachingsSection() {
  const trackRef = useRef<HTMLDivElement>(null);
  const [topic, setTopic] = useState(teachingTopics[0]);

  const scroll = (dir: 1 | -1) => trackRef.current?.scrollBy({ left: dir * 380, behavior: "smooth" });
  const visible = topic === teachingTopics[0] ? messages : messages.filter((m) => m.topic === topic);

  return (
    <section id="teachings" className="w-full bg-surface py-section">
      <Container>
        <div className="mb-space-lg max-w-2xl">
          <Eyebrow className="mb-space-xs">The Word &amp; Spirit</Eyebrow>
          <SectionTitle>Sermons &amp; Teachings</SectionTitle>
          <p className="mt-space-xs text-body-md text-on-surface-variant">
            Messages preached by Pastor Billy Joseph and sermon reviews from GCFT Media — on the end-time message, church
            order, and Christian character.
          </p>
        </div>

        {/* Series carousel */}
        <div className="relative mb-space-xl">
          <div className="mb-space-sm flex items-center justify-between">
            <span className="text-label-sm uppercase tracking-wider text-on-surface-variant">Featured Messages</span>
            <CarouselControls small label="series" onPrev={() => scroll(-1)} onNext={() => scroll(1)} />
          </div>
          <div ref={trackRef} className="no-scrollbar flex snap-x snap-mandatory gap-gutter overflow-x-auto scroll-smooth py-2">
            {sermonSeries.map((s) => (
              <article
                key={s.title}
                className="group min-w-[90%] snap-start overflow-hidden rounded-xl bg-surface-container-low shadow-lg md:min-w-[48%] lg:min-w-[32%]"
              >
                <div className="relative h-52 overflow-hidden">
                  <CoverImage src={s.image} alt={s.title} />
                  <div className="absolute inset-0 bg-gradient-to-t from-surface-container-low via-surface-container-low/30 to-transparent" />
                  <div className="absolute right-space-sm bottom-space-sm left-space-sm flex items-center justify-between">
                    <span
                      className={`rounded px-space-xs py-0.5 text-label-sm ${
                        s.current ? "bg-primary-container font-bold text-on-primary" : "bg-surface-bright font-medium text-on-surface"
                      }`}
                    >
                      {s.status}
                    </span>
                    {s.parts && (
                      <span className="rounded bg-surface/80 px-space-xs py-0.5 text-label-sm text-on-surface backdrop-blur-md">
                        {s.parts} Parts
                      </span>
                    )}
                  </div>
                </div>
                <div className="p-space-md">
                  <span className="text-label-sm font-medium text-secondary">{s.byline}</span>
                  <h3 className="mt-1 font-display text-headline-sm text-on-surface transition-colors group-hover:text-primary">
                    {s.title}
                  </h3>
                  <p className="mt-space-xs line-clamp-2 text-body-sm text-on-surface-variant">{s.body}</p>
                  <div className="mt-space-md flex items-center justify-between pt-space-xs">
                    <span className="text-label-sm text-on-surface-variant">{s.meta}</span>
                    <a {...linkProps(s.href)} className="inline-flex items-center gap-1 text-label-sm font-bold text-primary hover:underline">
                      {s.parts ? "Read Series" : "Listen"} <Icon name={s.parts ? "arrow_forward" : "play_circle"} size={16} />
                    </a>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>

        {/* Topic filter */}
        <div className="no-scrollbar mb-space-lg flex items-center gap-space-xs overflow-x-auto py-2">
          {teachingTopics.map((t) => (
            <button
              key={t}
              type="button"
              aria-pressed={topic === t}
              onClick={() => setTopic(t)}
              className={`shrink-0 rounded-full px-space-md py-1.5 text-label-sm transition-all ${
                topic === t
                  ? "bg-primary-container font-semibold text-on-primary"
                  : "bg-surface-container text-on-surface-variant hover:text-on-surface"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        {/* Message list */}
        <div className="space-y-space-sm">
          {visible.length === 0 && (
            <p className="rounded-xl bg-surface-container-low p-space-lg text-center text-body-sm text-on-surface-variant">
              No messages in this topic yet — check back soon.
            </p>
          )}
          {visible.map((m) => (
            <article
              key={m.title}
              className="group flex flex-col justify-between gap-space-md rounded-xl bg-surface-container-low p-space-md shadow-sm transition-all hover:bg-surface-container md:flex-row md:items-center"
            >
              <div className="flex items-start gap-space-md md:items-center">
                <a
                  {...linkProps(m.href)}
                  aria-label={`Listen to ${m.title} on Spotify`}
                  className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-surface-container text-primary transition-all group-hover:bg-primary-container group-hover:text-on-primary"
                >
                  <Icon name="play_arrow" size={24} fill />
                </a>
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-x-space-xs text-label-sm text-on-surface-variant">
                    <span>{m.label}</span>
                    <span>•</span>
                    <span className="font-medium text-primary">{m.topic}</span>
                  </div>
                  <h3 className="font-display text-headline-sm text-on-surface transition-colors group-hover:text-primary">
                    {m.title}
                  </h3>
                  <p className="text-body-sm text-on-surface-variant">{m.speaker}</p>
                </div>
              </div>
              <div className="flex items-center gap-space-sm pl-16 md:pl-0">
                <a
                  {...linkProps(m.href)}
                  className="inline-flex items-center gap-1 rounded-lg px-space-sm py-2 text-label-sm font-bold text-primary transition-colors hover:bg-surface-container-high"
                >
                  <Icon name="podcasts" size={18} /> Spotify
                </a>
                <a
                  {...linkProps(socials.youtube)}
                  title="Watch on YouTube"
                  aria-label="Watch on YouTube"
                  className="rounded-lg p-2 text-on-surface-variant transition-colors hover:bg-surface-container-high hover:text-on-surface"
                >
                  <Icon name="smart_display" />
                </a>
              </div>
            </article>
          ))}
        </div>
      </Container>
    </section>
  );
}
