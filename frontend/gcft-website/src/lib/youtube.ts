import { socials } from "./content";

export type YouTubeVideo = {
  id: string;
  title: string;
  published: string;
  thumbnail: string;
  url: string;
};

const decode = (s: string) =>
  s
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">");

/**
 * Latest uploads from the GCFT YouTube channel via the public RSS feed
 * (no API key). Cached for an hour; returns [] if YouTube is unreachable.
 */
export async function getLatestVideos(limit = 6, filter?: RegExp): Promise<YouTubeVideo[]> {
  try {
    const res = await fetch(`https://www.youtube.com/feeds/videos.xml?channel_id=${socials.youtubeChannelId}`, {
      next: { revalidate: 3600 },
    });
    if (!res.ok) return [];
    const xml = await res.text();
    const entries = xml.split("<entry>").slice(1);
    const videos = entries.map((e) => {
      const id = e.match(/<yt:videoId>([^<]+)<\/yt:videoId>/)?.[1] ?? "";
      return {
        id,
        title: decode(e.match(/<title>([^<]+)<\/title>/)?.[1] ?? ""),
        published: e.match(/<published>([^<]+)<\/published>/)?.[1] ?? "",
        thumbnail: `https://i.ytimg.com/vi/${id}/hqdefault.jpg`,
        url: `https://www.youtube.com/watch?v=${id}`,
      };
    });
    return videos.filter((v) => v.id && (!filter || filter.test(v.title))).slice(0, limit);
  } catch {
    return [];
  }
}

export const liveEmbedUrl = `https://www.youtube.com/embed/live_stream?channel=${socials.youtubeChannelId}`;
