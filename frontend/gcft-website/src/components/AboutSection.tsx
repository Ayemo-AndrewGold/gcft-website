"use client";

import { useEffect, useRef, useState } from "react";
import { moments, site, stats } from "@/lib/content";
import { CarouselControls, Container, CoverImage, Eyebrow, Icon, SectionTitle } from "./ui";

function useCountUp(target: number, start: boolean, duration = 1800) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    if (!start) return;
    let raf = 0;
    const t0 = performance.now();
    const tick = (now: number) => {
      const p = Math.min((now - t0) / duration, 1);
      setValue(Math.floor((1 - Math.pow(1 - p, 3)) * target));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [start, target, duration]);
  return value;
}

function Stat({ value, suffix, label, sub, start }: (typeof stats)[number] & { start: boolean }) {
  const n = useCountUp(value, start);
  return (
    <div className="flex flex-col items-center text-center md:items-start md:text-left">
      <div className="flex items-baseline gap-1">
        <span className="font-display text-headline-lg text-primary tabular-nums md:text-display-hero">
          {value >= 1000 ? n.toLocaleString("en-US") : n}
        </span>
        {suffix && <span className="font-display text-headline-sm text-primary">{suffix}</span>}
      </div>
      <span className="mt-1 text-label-md text-on-surface">{label}</span>
      <span className="text-body-sm text-on-surface-variant">{sub}</span>
    </div>
  );
}

export default function AboutSection() {
  const trackRef = useRef<HTMLDivElement>(null);
  const statsRef = useRef<HTMLDivElement>(null);
  const [counted, setCounted] = useState(false);

  useEffect(() => {
    const el = statsRef.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setCounted(true);
          obs.disconnect();
        }
      },
      { threshold: 0.3 },
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  const scroll = (dir: 1 | -1) => trackRef.current?.scrollBy({ left: dir * 340, behavior: "smooth" });

  return (
    <section id="about" className="w-full bg-surface py-section">
      <Container>
        <div className="mb-space-xl grid grid-cols-1 items-center gap-gutter lg:grid-cols-12 lg:gap-12">
          {/* Narrative */}
          <div className="flex flex-col gap-space-md lg:col-span-6">
            <Eyebrow>Who We Are</Eyebrow>
            <SectionTitle>Back to the Bible</SectionTitle>
            <p className="text-body-md text-on-surface-variant md:text-body-lg">
              {site.fullName} is an independent, non-denominational, Bible-believing church with no central headquarters or
              general overseer. We hold to the end-time message of Malachi 4:5–6b and Revelation 10:7, and our mission is
              to preach the undiluted Word of God — restoring the faith to the truths delivered to the early Apostles.
            </p>

            {/* Scripture callout */}
            <figure className="rounded-lg border-l-2 border-primary-container bg-surface-container-low p-space-md pl-space-lg">
              <blockquote className="mb-space-xs font-display text-headline-sm italic leading-snug text-primary">
                “Behold, I will send you Elijah the prophet before the coming of the great and dreadful day of the LORD.”
              </blockquote>
              <figcaption className="text-label-sm uppercase tracking-wider text-on-surface-variant">
                — Malachi 4:5
              </figcaption>
            </figure>

            <div className="flex flex-wrap items-center gap-x-space-lg gap-y-space-sm pt-space-sm">
              <div className="flex items-center gap-space-xs text-on-surface">
                <Icon name="menu_book" size={22} className="text-primary" />
                <span className="text-label-md font-medium">Non-Denominational</span>
              </div>
              <div className="flex items-center gap-space-xs text-on-surface">
                <Icon name="history_edu" size={22} className="text-primary" />
                <span className="text-label-md font-medium">Apostolic Doctrine</span>
              </div>
            </div>
          </div>

          {/* Moments carousel */}
          <div className="flex min-w-0 flex-col gap-space-md lg:col-span-6">
            <div className="flex items-center justify-between">
              <span className="text-label-sm uppercase tracking-wider text-on-surface-variant">
                Life at {site.name}
              </span>
              <CarouselControls label="slide" onPrev={() => scroll(-1)} onNext={() => scroll(1)} />
            </div>
            <div ref={trackRef} className="no-scrollbar flex snap-x snap-mandatory gap-space-md overflow-x-auto scroll-smooth py-2">
              {moments.map((m) => (
                <article
                  key={m.title}
                  className="group min-w-[85%] snap-center overflow-hidden rounded-xl bg-surface-container-low shadow-md md:min-w-[70%]"
                >
                  <div className="relative h-64 overflow-hidden">
                    <CoverImage src={m.image} alt={m.title} />
                    <div className="absolute inset-0 bg-gradient-to-t from-surface-container-low via-transparent to-transparent" />
                  </div>
                  <div className="p-space-md">
                    <span className="text-label-sm font-bold uppercase tracking-wider text-primary">{m.tag}</span>
                    <h3 className="mt-1 font-display text-headline-sm text-on-surface">{m.title}</h3>
                    <p className="mt-space-xs text-body-sm text-on-surface-variant">{m.body}</p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </div>

        {/* Stats */}
        <div
          ref={statsRef}
          className="candle-glow grid grid-cols-2 gap-gutter rounded-xl bg-surface-container-low/80 p-space-lg shadow-lg backdrop-blur-md md:grid-cols-4 md:p-space-xl"
        >
          {stats.map((s) => (
            <Stat key={s.label} {...s} start={counted} />
          ))}
        </div>
      </Container>
    </section>
  );
}
