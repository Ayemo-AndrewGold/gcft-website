"use client";

import { useEffect, useRef, useState } from "react";
import { site } from "@/lib/content";
import { images } from "@/lib/images";
import { Container, Icon } from "../ui";
import NextService from "./NextService";
import { Accent, Button, LiveDot } from "./primitives";

export default function Hero({ videoSrc = site.heroVideo }: { videoSrc?: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [paused, setPaused] = useState(false);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      videoRef.current?.pause();
    }
  }, []);

  const toggle = () => {
    const v = videoRef.current;
    if (!v) return;
    if (v.paused) {
      v.play();
      setPaused(false);
    } else {
      v.pause();
      setPaused(true);
    }
  };

  return (
    <section id="top" className="relative isolate flex min-h-[100svh] w-full flex-col overflow-hidden bg-surface">
      {/* Media */}
      <div className="absolute inset-0 -z-10">
        <video
          ref={videoRef}
          autoPlay
          muted
          loop
          playsInline
          preload="metadata"
          poster={images.hero}
          className="h-full w-full scale-[1.02] object-cover"
          src={videoSrc}
          onPause={() => setPaused(true)}
          onPlay={() => setPaused(false)}
        />
        {/* Legibility: soft top vignette for the nav, strong floor for type */}
        <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(10,11,13,0.55)_0%,rgba(10,11,13,0.15)_28%,rgba(10,11,13,0.35)_55%,#0a0b0d_100%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(90%_60%_at_20%_100%,rgba(10,11,13,0.7),transparent)]" />
        <div className="grain absolute inset-0" />
      </div>

      <Container className="flex flex-1 flex-col justify-end pt-[128px] pb-10 md:pt-[160px] md:pb-14">
        {/* Kicker */}
        <p className="eyebrow mb-8 flex items-center gap-3 text-white/70 md:mb-10">
          <span className="h-1.5 w-1.5 rounded-full bg-primary-container" />
          {site.fullName}
        </p>

        {/* Display headline */}
        <h1 className="max-w-[14ch] text-[clamp(3.25rem,9vw,9rem)] leading-[0.9] font-medium tracking-[-0.055em] text-white">
          Where the <Accent>truth</Accent> still exists.
        </h1>

        <div className="mt-10 grid grid-cols-1 items-end gap-8 md:mt-14 md:grid-cols-12">
          <p className="max-w-md text-[17px] leading-[1.6] text-white/75 md:col-span-6 lg:col-span-5">
            An independent, Bible-believing church in Ijoko, Ogun State — on a mandate to preach nothing but the
            undiluted Word. <span className="text-white">Back to the Bible.</span>
          </p>
          <div className="flex flex-col gap-3 xs:flex-row md:col-span-6 md:justify-end lg:col-span-7">
            <Button href="/live" icon={<LiveDot />}>
              Watch live
            </Button>
            <Button href="/contact" variant="ghost">
              Plan a visit
            </Button>
          </div>
        </div>

        {/* Meta strip */}
        <dl className="mt-12 grid grid-cols-2 gap-x-6 gap-y-6 border-t border-white/15 pt-6 md:mt-16 md:grid-cols-4">
          <div>
            <NextService />
          </div>
          <div>
            <dt className="eyebrow text-on-surface-variant">Midweek</dt>
            <dd className="mt-2 text-[15px] text-on-surface">Tue & Thu · 6:30 PM</dd>
          </div>
          <div>
            <dt className="eyebrow text-on-surface-variant">Our message</dt>
            <dd className="mt-2 text-[15px] text-on-surface">Malachi 4:5–6b · Rev 10:7</dd>
          </div>
          <div className="flex items-end justify-between gap-4">
            <div>
              <dt className="eyebrow text-on-surface-variant">Location</dt>
              <dd className="mt-2 text-[15px] text-on-surface">Ijoko, Sango Ota</dd>
            </div>
            <button
              type="button"
              onClick={toggle}
              aria-label={paused ? "Play background video" : "Pause background video"}
              className="hidden h-10 w-10 shrink-0 items-center justify-center rounded-full border border-white/20 text-white/80 transition-colors hover:border-white/50 hover:text-white md:flex"
            >
              <Icon name={paused ? "play_arrow" : "pause"} size={18} fill />
            </button>
          </div>
        </dl>
      </Container>
    </section>
  );
}
