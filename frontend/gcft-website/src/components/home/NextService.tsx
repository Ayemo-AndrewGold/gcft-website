"use client";

import { useSyncExternalStore } from "react";
import { formatUntil, nextGathering, to12h } from "@/lib/schedule";
import { LiveDot } from "./primitives";

/* A minute-resolution clock shared by all subscribers (null on the server). */
const clock = {
  subscribe(cb: () => void) {
    const id = setInterval(cb, 30_000);
    return () => clearInterval(id);
  },
  snapshot: () => Math.floor(Date.now() / 60_000),
  server: () => null,
};

/** Live "next gathering" readout, computed in WAT. */
export default function NextService() {
  const minute = useSyncExternalStore(clock.subscribe, clock.snapshot, clock.server);

  if (minute === null) {
    return (
      <>
        <dt className="eyebrow text-on-surface-variant">Next gathering</dt>
        <dd className="mt-2 text-[15px] text-on-surface">Sunday · 9:00 AM WAT</dd>
      </>
    );
  }

  const { gathering: g, live, minutesUntil } = nextGathering(new Date(minute * 60_000));
  return (
    <>
      <dt className="eyebrow flex items-center gap-2 text-on-surface-variant">
        {live ? (
          <>
            <LiveDot /> <span className="text-error">Happening now</span>
          </>
        ) : (
          <>Next gathering · {formatUntil(minutesUntil)}</>
        )}
      </dt>
      <dd className="mt-2 text-[15px] text-on-surface" aria-live="polite">
        {g.dayName} · {to12h(g.start)} WAT
      </dd>
    </>
  );
}
