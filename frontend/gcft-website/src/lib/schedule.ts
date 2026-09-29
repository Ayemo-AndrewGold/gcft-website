/*
 * Weekly schedule, in West Africa Time (UTC+1, no DST).
 * `day` uses JS numbering: 0 = Sunday … 6 = Saturday.
 */
export type Gathering = {
  day: number;
  dayName: string;
  name: string;
  start: string; // "HH:MM" WAT
  end: string;
  note: string;
  live?: boolean;
};

export const gatherings: Gathering[] = [
  { day: 0, dayName: "Sunday", name: "Sunday Service", start: "09:00", end: "14:00", note: "Song service & the Word", live: true },
  { day: 2, dayName: "Tuesday", name: "Midweek Service", start: "18:30", end: "20:30", note: "Teaching & prayer" },
  { day: 4, dayName: "Thursday", name: "Midweek Service", start: "18:30", end: "20:30", note: "Teaching & prayer" },
  { day: 5, dayName: "Friday", name: "Night Vigil", start: "02:00", end: "04:00", note: "Watching & praying" },
];

const WAT_OFFSET_MIN = 60;

/** Current time expressed as minutes into the WAT week (0 = Sunday 00:00 WAT). */
function watWeekMinutes(now: Date) {
  const wat = new Date(now.getTime() + WAT_OFFSET_MIN * 60_000);
  return wat.getUTCDay() * 1440 + wat.getUTCHours() * 60 + wat.getUTCMinutes();
}

const toMin = (g: Gathering, key: "start" | "end") => {
  const [h, m] = g[key].split(":").map(Number);
  return g.day * 1440 + h * 60 + m;
};

/** The gathering happening now, or the next one, with minutes until it starts. */
export function nextGathering(now = new Date()) {
  const t = watWeekMinutes(now);
  const current = gatherings.find((g) => t >= toMin(g, "start") && t < toMin(g, "end"));
  if (current) return { gathering: current, live: true, minutesUntil: 0 };
  const WEEK = 7 * 1440;
  const upcoming = gatherings
    .map((g) => ({ g, delta: (toMin(g, "start") - t + WEEK) % WEEK }))
    .sort((a, b) => a.delta - b.delta)[0];
  return { gathering: upcoming.g, live: false, minutesUntil: upcoming.delta };
}

export function formatUntil(minutes: number) {
  const d = Math.floor(minutes / 1440);
  const h = Math.floor((minutes % 1440) / 60);
  const m = minutes % 60;
  if (d > 0) return `in ${d}d ${h}h`;
  if (h > 0) return `in ${h}h ${m}m`;
  return `in ${m}m`;
}

/** "09:00" → "9:00 AM" */
export function to12h(hhmm: string) {
  const [h, m] = hhmm.split(":").map(Number);
  const suffix = h >= 12 ? "PM" : "AM";
  return `${((h + 11) % 12) + 1}:${String(m).padStart(2, "0")} ${suffix}`;
}
