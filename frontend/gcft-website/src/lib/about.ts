/*
 * Content for the About pages.
 * Facts come from gcftchurch.org and the church's public channels — keep claims
 * conservative and let the church's own publications speak for doctrine.
 */
import { images } from "./images";
import { site, socials } from "./content";

export type AboutIntro = {
  eyebrow: string;
  title: string;
  lead: string[]; // left column paragraphs
  body: string[]; // right column paragraphs
  closing?: string; // emphatic uppercase closing line
};

/** "01 / 02 / 03" outlined link boxes */
export const pathways = [
  { n: "01", kicker: "Worship With Us", title: "Service Times", href: "/#events", icon: "schedule" },
  { n: "02", kicker: "Hear the Undiluted Word", title: "Sermons", href: "/#teachings", icon: "headphones" },
  { n: "03", kicker: "Visit the Tabernacle", title: "Contact Us", href: "/contact", icon: "location_on" },
];

/** "How we help" image cards */
export const ministries = {
  eyebrow: "How We Minister",
  title: "Channels of the Undiluted Word",
  items: [
    {
      image: images.eventWorshipNight,
      title: "Sunday Song Service",
      body: "Song, prayer, and the preaching of the Word — live every Sunday on YouTube.",
      href: socials.youtube,
    },
    {
      image: images.seriesPsalms,
      title: "Audio Sermons",
      body: "Messages by Pastor Billy Joseph on the GCFT podcast on Spotify.",
      href: socials.spotify,
    },
    {
      image: images.seriesPeace,
      title: "GCFT Media",
      body: "Sermon reviews, books, and camp meeting materials on gcftchurch.org.",
      href: site.website,
    },
  ],
};

/** Accent band with scrolling counters */
export const journey = {
  eyebrow: "Where We Stand",
  title: "Our Fellowship in Numbers",
  body: "Week after week we gather to hear the Word and to spread the truths delivered to the early Apostles — in Ijoko and to believers around the world online.",
  cta: { label: "Watch on YouTube", href: socials.youtube },
  counters: [
    { value: 4, suffix: "", label: "Weekly gatherings — Sunday, Tuesday, Thursday & the Friday vigil." },
    { value: 5, suffix: "hrs", label: "Of worship and the Word every Sunday, 9:00 AM – 2:00 PM WAT." },
    { value: 980, suffix: "+", label: "Video sermons and song services on our YouTube channel." },
    { value: 1.1, suffix: "K+", label: "Believers subscribed to GCFT on YouTube worldwide." },
    { value: 2, suffix: "", label: "Scriptures at the heart of our message — Malachi 4:5–6b & Revelation 10:7." },
  ],
};

/* ---------- Page-specific intros ---------- */

export const whoWeAre: AboutIntro = {
  eyebrow: "About GCFT",
  title: "Who We Are",
  lead: [
    `${site.fullName} is an independent, non-denominational, Bible-believing church located at 1 Salvation Avenue, off Onipetesi Road, behind Ijoko Market, in Ijoko, Sango Ota, Ogun State, Nigeria.`,
  ],
  body: [
    "We have no central headquarters and no general overseer. We believe the message of Malachi 4:5 & 6b and Revelation 10:7, and we are on a mandate to preach nothing else but the truth.",
    "Our mission is to preach the undiluted Word of God and to spread the truths that were delivered to the early Apostles — restoring the faith to its original, apostolic foundation.",
  ],
  closing: "Our motto is simple: Back to the Bible. This is where the truth still exists.",
};

export const beliefs: AboutIntro = {
  eyebrow: "What We Believe",
  title: "Back to the Bible",
  lead: [
    "We are a Bible-believing congregation. The Scriptures are our only rule of faith and practice, and our desire is to return to the doctrine and practice of the early Apostles.",
  ],
  body: [
    "Our teaching emphasises the new birth, consecration and holiness, order in the house of God, and the character of the believer — the readiness of the Bride for the coming of the Lord.",
    "For a full treatment of any doctrine, we point you to the Word itself and to the teachings published by GCFT Media.",
  ],
  closing: "Nothing else but the truth.",
};

export const beliefPoints = [
  {
    icon: "menu_book",
    title: "The Word of God",
    body: "The Bible is the final authority. We preach the undiluted Word and test every teaching by the Scriptures.",
  },
  {
    icon: "history_edu",
    title: "Apostolic Doctrine",
    body: "We seek to restore the faith once delivered to the saints — the teachings of the early Apostles.",
  },
  {
    icon: "water_drop",
    title: "The New Birth",
    body: "Every soul must be born again. See our teaching “Why Must We Be Born Again?”",
    href: "https://gcftchurch.org/why-must-we-be-born-again/",
  },
  {
    icon: "diversity_3",
    title: "Order & Character",
    body: "“The Beauty of the Church Is the Character of Her Members” — holiness and orderliness in God’s house.",
  },
  {
    icon: "flight",
    title: "The Blessed Hope",
    body: "We look for the coming of the Lord and exhort one another to readiness for the Rapture.",
  },
  {
    icon: "account_balance",
    title: "Non-Denominational",
    body: "An independent fellowship — no denomination, no central headquarters, no general overseer.",
  },
];

export const theMessage: AboutIntro = {
  eyebrow: "Our Message",
  title: "Malachi 4:5–6b & Revelation 10:7",
  lead: [
    "The congregation's message centres on two scriptures that speak of God restoring His people to the original faith before the coming of the Lord.",
  ],
  body: [
    "We believe God promised to turn the hearts of the children back to the fathers — back to the faith and doctrine of the Apostles — and that the mystery of God would be finished in the days of the seventh angel's message.",
    "This is why our teaching focuses on the end-time: the preparation of the Bride, the translation of the saints, and a life lived in readiness.",
  ],
  closing: "A call to return to the faith of our fathers.",
};

export const messageScriptures = [
  {
    ref: "Malachi 4:5",
    text: "Behold, I will send you Elijah the prophet before the coming of the great and dreadful day of the LORD.",
  },
  {
    ref: "Malachi 4:6",
    text: "And he shall turn the heart of the fathers to the children, and the heart of the children to their fathers…",
  },
  {
    ref: "Revelation 10:7",
    text: "But in the days of the voice of the seventh angel, when he shall begin to sound, the mystery of God should be finished, as he hath declared to his servants the prophets.",
  },
];

export const ministers: AboutIntro = {
  eyebrow: "Leadership",
  title: "Our Ministers",
  lead: [
    "GCFT is an independent congregation served by ministers who labour in the Word and in doctrine, with teaching shared through GCFT Media.",
  ],
  body: [
    "Messages preached at the tabernacle are made available on our YouTube channel, on Spotify, and on gcftchurch.org, together with written sermon reviews and books.",
  ],
};

export const ministerProfiles = [
  {
    name: "Pastor Billy Joseph",
    role: "Teaching Minister",
    body: "Pastor Billy Joseph delivers the primary messages at the tabernacle, including “Living for God”, “Testing for Sincerity”, and “Exhortation on the Rapture”.",
    links: [
      { label: "Listen on Spotify", href: socials.spotify, icon: "podcasts" },
      { label: "Watch on YouTube", href: socials.youtube, icon: "smart_display" },
    ],
  },
  {
    name: "Pastor Gideon Toyosi",
    role: "Writer & Expositor, GCFT Media",
    body: "Pastor Gideon Toyosi writes sermon reviews and teachings for GCFT Media, including the series “A White Linen That Is Seen Through Different Lenses”.",
    links: [{ label: "Read on gcftchurch.org", href: "https://gcftchurch.org/author/admin/", icon: "article" }],
  },
];
