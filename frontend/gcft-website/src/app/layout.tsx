import type { Metadata } from "next";
import { Playfair_Display, Plus_Jakarta_Sans } from "next/font/google";
import Header from "@/components/Header";
import Footer, { ServiceBar } from "@/components/Footer";
import "./globals.css";

/* Playfair Display — editorial serif for headlines & scripture */
const playfair = Playfair_Display({
  variable: "--font-playfair",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  style: ["normal", "italic"],
  display: "swap",
});

/* Plus Jakarta Sans — body, labels, and UI */
const jakarta = Plus_Jakarta_Sans({
  variable: "--font-jakarta",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "Glorious Christian Fellowship Tabernacle (GCFT) — Where the Truth Still Exists",
    template: "%s | GCFT",
  },
  description:
    "GCFT is an independent, non-denominational, Bible-believing church at 1 Salvation Avenue, Ijoko, Sango Ota, Ogun State, Nigeria. Sundays 9 AM – 2 PM WAT.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${playfair.variable} ${jakarta.variable} h-full antialiased`}
    >
      <head>
        {/* Icon font used throughout the design */}
        {/* eslint-disable-next-line @next/next/no-page-custom-font */}
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block"
        />
      </head>
      <body className="min-h-full flex flex-col bg-surface font-body text-on-surface">
        <Header />
        {children}
        <Footer />
        <ServiceBar />
      </body>
    </html>
  );
}
