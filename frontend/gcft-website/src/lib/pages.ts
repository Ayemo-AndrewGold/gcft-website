/* Content for the Contact and Newsletter pages. */
import { images } from "./images";
import { site, socials } from "./content";

export const contactCards = [
  {
    icon: "mail",
    label: "Email Us",
    title: "We'd Love to Hear From You.",
    body: "Write to the Glorious Christian Fellowship Tabernacle for enquiries, prayer requests, sermon materials, or directions to the tabernacle.",
    link: { text: site.email, href: `mailto:${site.email}` },
  },
  {
    icon: "call",
    label: "Call Us",
    title: "Need to Speak With Someone?",
    body: "Call the church for service information, camp meeting and convention details, or help finding your way to Ijoko.",
    link: { text: site.phone, href: site.phoneHref },
  },
];

export const enquiryTopics = ["General Enquiry", "Prayer Request", "Visiting the Tabernacle", "Sermons & Media", "Camp Meeting / Convention"];

export const mapEmbed = `https://www.google.com/maps?q=${encodeURIComponent(
  "Ijoko Market, Ijoko, Sango Ota, Ogun State, Nigeria",
)}&z=15&output=embed`;

/* ---------------- Newsletter ---------------- */

export const newsletter = {
  name: "GCFT Weekly",
  headline: "The Undiluted Word, Delivered to Your Inbox.",
  lead: "A short weekly letter from the Glorious Christian Fellowship Tabernacle — sermon reviews, the Word for the week, and news of services, vigils, camp meetings and conventions.",
  flyer: images.seriesJohn,
  trust: "Read by believers who want to stay rooted in the Word between services.",
  segmentsIntro: "Each edition is built around the Word, in seven short segments:",
  segments: [
    { title: "“The Word for the Week”", body: "A scripture to meditate on through the week." },
    { title: "“From the Pulpit”", body: "Highlights from the latest message preached at the tabernacle." },
    { title: "“Sermon Review”", body: "A written review from GCFT Media, like “A White Linen That Is Seen Through Different Lenses”." },
    { title: "“The Message”", body: "A thought on Malachi 4:5–6b and Revelation 10:7 for our day." },
    { title: "“Service & Vigil Times”", body: "Sunday, Tuesday, Thursday and the Friday vigil — and any changes." },
    { title: "“Camp Meeting & Convention News”", body: "Dates, materials, and convention messages as they are published." },
    { title: "“From the Library”", body: "A book, article, or audio sermon worth your time." },
  ],
  audience: "GCFT Weekly is written for everyone who wants to go “Back to the Bible.”",
  sampleCta: { label: "Read Recent Sermon Reviews", href: "https://gcftchurch.org/category/sermon-reviews/" },
  editor: {
    name: "GCFT Media",
    body: "GCFT Media is the publishing arm of the Glorious Christian Fellowship Tabernacle — sermon reviews, teachings, books and camp meeting materials, with writing from Pastor Gideon Toyosi and messages preached by Pastor Billy Joseph.",
    links: [
      { label: "gcftchurch.org", href: site.website, icon: "public" },
      { label: "Spotify", href: socials.spotify, icon: "podcasts" },
      { label: "YouTube", href: socials.youtube, icon: "smart_display" },
    ],
  },
  closingLine: "Stay rooted in the Word all week long.",
  finalTitle: "Where the Truth Still Exists.",
};
