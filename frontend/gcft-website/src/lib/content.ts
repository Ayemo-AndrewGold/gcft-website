/*
 * Site content for the GCFT home page.
 * Church details verified against gcftchurch.org (Sept 2026).
 * Photos are still placeholders — see images.ts.
 */
import { images } from "./images";

const mapsQuery = encodeURIComponent(
  "1 Salvation Avenue, Off Onipetesi Road, Behind Ijoko Market, Ijoko, Sango Ota, Ogun State, Nigeria",
);

export const site = {
  name: "GCFT",
  fullName: "Glorious Christian Fellowship Tabernacle",
  tagline: "Where the truth still exists…",
  motto: "Back to the Bible",
  logo: "https://gcftchurch.org/wp-content/uploads/2023/04/GCFT-LOGO.jpg",
  description:
    "An independent, non-denominational, Bible-believing church in Ijoko, Sango Ota — preaching the undiluted Word of God and the truths delivered to the early Apostles.",
  heroVideo:
    "https://res.cloudinary.com/yaovkmpi/video/upload/f_auto,q_auto/v1789908498/SONG_SERVICE____NOVEMBER_16_2025_kzhdp0.mp4",
  location: "Ijoko, Sango Ota, Ogun State",
  address: {
    line1: "1 Salvation Avenue, Off Onipetesi Road",
    line2: "Behind Ijoko Market, Ijoko",
    line3: "Sango Ota, Ogun State, Nigeria",
  },
  mapsUrl: `https://www.google.com/maps/search/?api=1&query=${mapsQuery}`,
  phone: "+234 806 438 9914",
  phoneHref: "tel:+2348064389914",
  email: "christftchurchtv@gmail.com",
  website: "https://gcftchurch.org/",
  serviceSummary: "Sundays 9:00 AM – 2:00 PM • Tuesdays & Thursdays 6:30 PM – 8:30 PM • Friday Vigil 2:00 AM – 4:00 AM (WAT)",
};

export const socials = {
  youtube: "https://www.youtube.com/c/GloriousChristianFellowshipTabernacle",
  youtubeChannelId: "UCbtIQ5Uv5KwTKxdbZaKbH1Q",
  facebook: "https://www.facebook.com/christftchurch/",
  spotify: "https://open.spotify.com/show/4CaXpWmHpD67C47FKq8Jt9",
  instagram: "https://www.instagram.com/christftchurch/",
  twitter: "https://twitter.com/christftchurch",
};

export type NavItem = { name: string; href: string; children?: { name: string; href: string; description?: string }[] };

/* About sub-pages (dropdown under "About") */
export const aboutPages = [
  { name: "Who We Are", href: "/about", description: "Our identity, mission & motto" },
  { name: "Our Beliefs", href: "/about/beliefs", description: "Back to the Bible" },
  { name: "The Message", href: "/about/the-message", description: "Malachi 4:5–6b & Revelation 10:7" },
  { name: "Our Ministers", href: "/about/ministers", description: "Those who labour in the Word" },
];

/* Live Experience sub-pages (dropdown under "Live Experience") */
export const livePages = [
  { name: "Watch Live", href: "/live", description: "Sunday song service & the Word, streamed" },
  { name: "Camp Meeting", href: "/live/camp-meeting", description: "Our annual gathering" },
  { name: "Conventions", href: "/live/conventions", description: "Convention messages & replays" },
];

export const navLinks: NavItem[] = [
  { name: "Home", href: "/" },
  { name: "About", href: "/about", children: aboutPages },
  { name: "Live Experience", href: "/live", children: livePages },
  { name: "Services", href: "/#events" },
  { name: "Sermons", href: "/#teachings" },
  { name: "Newsletter", href: "/newsletter" },
  { name: "Contact", href: "/contact" },
];

/* Slim utility bar above the main header */
export const utilityLinks = {
  left: [
    { name: "Get Directions", href: site.mapsUrl, external: true },
    { name: "Audio Sermons", href: socials.spotify, external: true },
  ],
  right: [
    { name: "Prayer Request", href: `mailto:${site.email}?subject=Prayer%20Request` },
    { name: "Schedule", href: "/#events" },
  ],
};

export const tickerItems = [
  { text: "Sundays: 9:00 AM – 2:00 PM", tone: "primary", icon: "schedule" },
  { text: "Tuesdays & Thursdays: 6:30 PM – 8:30 PM", tone: "muted" },
  { text: "Friday Vigil: 2:00 AM – 4:00 AM", tone: "secondary" },
  { text: "Song Service Live on YouTube Every Sunday", tone: "muted" },
] as const;

/* Bottom service bar carousel */
export const serviceBarItems = [
  { text: "Sundays 9:00 AM – 2:00 PM WAT", tone: "primary" },
  { text: "Watch the Song Service Live on YouTube Every Sunday", tone: "muted" },
  { text: `Call Us: ${site.phone}`, tone: "muted" },
  { text: "Tuesdays & Thursdays 6:30 PM – 8:30 PM", tone: "secondary" },
  { text: "Friday Night Vigil 2:00 AM – 4:00 AM", tone: "muted" },
] as const;

export const moments = [
  {
    image: images.aboutWorship,
    tag: "Sunday Song Service",
    title: "Worship in Spirit & Truth",
    body: "Every Sunday we gather to sing, pray, and hear the Word — streamed live on YouTube for those far away.",
  },
  {
    image: images.aboutFellowship,
    tag: "Fellowship",
    title: "One Family in the Word",
    body: "An independent congregation with no central headquarters — bound together by the Word, not a denomination.",
  },
  {
    image: images.aboutOutreach,
    tag: "Camp Meeting",
    title: "Annual Camp Meeting",
    body: "Days set apart for teaching, consecration, and fellowship with believers of like precious faith.",
  },
];

export const stats = [
  { value: 4, suffix: "", label: "Weekly Gatherings", sub: "Sun • Tue • Thu • Fri Vigil" },
  { value: 5, suffix: " hrs", label: "Sunday Worship", sub: "9:00 AM – 2:00 PM WAT" },
  { value: 980, suffix: "+", label: "Video Sermons", sub: "On our YouTube channel" },
  { value: 1150, suffix: "+", label: "YouTube Family", sub: "Subscribers worldwide" },
];

export const weeklyGatherings = [
  {
    day: "Sunday",
    icon: "church",
    featured: true,
    title: "Sunday Service",
    body: "Song service, prayer, and the preaching of the Word. Streamed live on our YouTube channel.",
    time: "9:00 AM – 2:00 PM",
    place: "Main Tabernacle",
  },
  {
    day: "Tuesday",
    icon: "menu_book",
    title: "Tuesday Service",
    body: "A midweek evening in the Scriptures — teaching, prayer, and fellowship.",
    time: "6:30 PM – 8:30 PM",
    place: "WAT",
  },
  {
    day: "Thursday",
    icon: "auto_stories",
    title: "Thursday Service",
    body: "Continuing in the Word through the week, grounded in the teachings of the early Apostles.",
    time: "6:30 PM – 8:30 PM",
    place: "WAT",
  },
  {
    day: "Friday",
    icon: "nights_stay",
    title: "Friday Night Vigil",
    body: "Watching and praying together in the early hours of Friday morning.",
    time: "2:00 AM – 4:00 AM",
    place: "WAT",
  },
];

export const upcomingEvents = [
  {
    image: images.eventWorshipNight,
    badge: "Every Sunday",
    featured: true,
    when: "Sundays • 9:00 AM WAT",
    title: "Sunday Song Service — Live",
    body: "Join the song service and Sunday message live from the tabernacle in Ijoko, or watch on YouTube.",
    note: "In person & online",
    cta: { label: "Watch on YouTube", href: socials.youtube },
  },
  {
    image: images.eventRetreat,
    badge: "Annual Camp Meeting",
    when: "Dates announced on our channels",
    title: "GCFT Camp Meeting",
    body: "Our yearly gathering for teaching and consecration. Camp meeting materials are published by GCFT Media.",
    note: "All are welcome",
    cta: { label: "Camp Meeting Archive", href: "https://gcftchurch.org/category/camp-meeting/" },
  },
  {
    image: images.eventSummit,
    badge: "Convention",
    when: "Convention Messages",
    title: "Convention Messages",
    body: "Listen back to messages preached at past conventions of the Glorious Christian Fellowship Tabernacle.",
    note: "Free to stream",
    cta: { label: "Browse Messages", href: "https://gcftchurch.org/convention-messages/" },
  },
];

export const sermonSeries = [
  {
    image: images.seriesJohn,
    status: "Sermon Review Series",
    current: true,
    parts: 6,
    byline: "Pastor Gideon Toyosi • GCFT Media",
    title: "A White Linen That Is Seen Through Different Lenses",
    body: "A study of the Bride of Christ and the order governing spiritual gifts — honouring the Giver and the Word above the blessings.",
    meta: "Latest: Part VI",
    href: "https://gcftchurch.org/tag/the-bridegroom/",
  },
  {
    image: images.seriesPeace,
    status: "End-Time Message",
    byline: "Pastor Billy Joseph",
    title: "Why It Had to Be Enoch the Seventh and Elijah the Tishbite",
    body: "Biblical typology from the lives of Enoch and Elijah and what they reveal about the translation of the saints.",
    meta: "Audio sermon",
    href: socials.spotify,
  },
  {
    image: images.seriesPsalms,
    status: "End-Time Message",
    byline: "Pastor Billy Joseph",
    title: "Exhortation on the Rapture",
    body: "A sober exhortation to readiness for the catching away of the Bride — Malachi 4:5–6 and Revelation 10:7.",
    meta: "Audio sermon",
    href: socials.spotify,
  },
];

export const teachingTopics = ["All Messages", "Christian Character", "Church Order", "End-Time Message"];

export const messages = [
  {
    label: "Audio Sermon",
    title: "Living for God",
    speaker: "Preached by Pastor Billy Joseph",
    topic: "Christian Character",
  },
  {
    label: "Audio Sermon",
    title: "Testing for Sincerity",
    speaker: "Preached by Pastor Billy Joseph",
    topic: "Christian Character",
  },
  {
    label: "Audio Sermon",
    title: "The Beauty of the Church Is the Character of Her Members",
    speaker: "Preached by Pastor Billy Joseph",
    topic: "Church Order",
  },
  {
    label: "Audio Sermon",
    title: "Orderliness in the House of God",
    speaker: "Preached by Pastor Billy Joseph",
    topic: "Church Order",
  },
  {
    label: "Audio Sermon",
    title: "Restitution",
    speaker: "Preached by Pastor Billy Joseph",
    topic: "Christian Character",
  },
  {
    label: "Audio Sermon",
    title: "Exhortation on the Rapture",
    speaker: "Preached by Pastor Billy Joseph",
    topic: "End-Time Message",
  },
].map((m) => ({ ...m, href: socials.spotify }));

export type ResourceType = "audio" | "guides" | "video";

export const resourceTabs: { id: "all" | ResourceType; label: string }[] = [
  { id: "all", label: "All Formats" },
  { id: "audio", label: "Audio Sermons" },
  { id: "guides", label: "Articles & Books" },
  { id: "video", label: "Video Sermons" },
];

export const searchSuggestions = ["Born Again", "Spiritual Gifts", "Rapture", "Gospel"];

export const resources: {
  type: ResourceType;
  format: string;
  kind: string;
  title: string;
  body: string;
  author: string;
  keywords: string;
  href: string;
}[] = [
  {
    type: "guides",
    format: "Article",
    kind: "Sermon Review",
    title: "Broken But Not Beyond Repair",
    body: "We are chosen by God to be a little light here and there that gives a darkening world hope.",
    author: "Pastor Gideon Toyosi",
    keywords: "hope light restoration teaching",
    href: "https://gcftchurch.org/broken-but-not-beyond-repair/",
  },
  {
    type: "guides",
    format: "Article",
    kind: "Sermon Review",
    title: "The Sixfold Purpose of the Gospel",
    body: "“The Spirit of the Lord is upon me…” — a study of Luke 4:18 and the purpose of the Gospel.",
    author: "Pastor Gideon Toyosi",
    keywords: "gospel luke 4 purpose anointing",
    href: "https://gcftchurch.org/the-sixfold-purpose-of-the-gospel/",
  },
  {
    type: "guides",
    format: "Article",
    kind: "Teaching",
    title: "Why Must We Be Born Again?",
    body: "A foundational teaching on the fall of man and the necessity of the new birth.",
    author: "GCFT Media",
    keywords: "born again new birth fall eden salvation",
    href: "https://gcftchurch.org/why-must-we-be-born-again/",
  },
  {
    type: "audio",
    format: "Podcast",
    kind: "Spotify",
    title: "GCFT on Spotify",
    body: "Stream sermons such as Living for God, Testing for Sincerity, and Restitution on the GCFT podcast.",
    author: "Pastor Billy Joseph",
    keywords: "podcast audio living for god sincerity restitution rapture",
    href: socials.spotify,
  },
  {
    type: "video",
    format: "Video",
    kind: "YouTube",
    title: "Sunday Song Services",
    body: "Watch the Sunday song service and messages live or on demand — nearly a thousand videos and counting.",
    author: "GCFT on YouTube",
    keywords: "video song service sunday live youtube",
    href: socials.youtube,
  },
  {
    type: "guides",
    format: "Library",
    kind: "Books",
    title: "Books & Sermon Library",
    body: "Download and read inspired books to deepen your spiritual understanding.",
    author: "GCFT Media",
    keywords: "books library download read",
    href: "https://gcftchurch.org/books/",
  },
];

export const footerLinks = {
  quick: [
    { name: "Home", href: "/" },
    { name: "About Us", href: "/about" },
    { name: "Our Beliefs", href: "/about/beliefs" },
    { name: "Service Times", href: "/#events" },
    { name: "Sermons", href: "/#teachings" },
    { name: "Newsletter", href: "/newsletter" },
    { name: "Contact", href: "/contact" },
  ],
  involved: [
    { name: "Audio Sermons", href: socials.spotify },
    { name: "Video Sermons", href: socials.youtube },
    { name: "Convention Messages", href: "https://gcftchurch.org/convention-messages/" },
    { name: "Testimonies", href: "https://gcftchurch.org/testimonies/" },
    { name: "Books", href: "https://gcftchurch.org/books/" },
  ],
  social: [
    { icon: "smart_display", label: "YouTube", href: socials.youtube },
    { icon: "thumb_up", label: "Facebook", href: socials.facebook },
    { icon: "podcasts", label: "Spotify", href: socials.spotify },
    { icon: "photo_camera", label: "Instagram", href: socials.instagram },
  ],
};
