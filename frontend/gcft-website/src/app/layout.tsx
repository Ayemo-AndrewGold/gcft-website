import type { Metadata } from "next";
// import { Geist, Geist_Mono, Playfair_Display } from "next/font/google";
import { Cormorant_Garamond, Inter } from "next/font/google";
import "./globals.css";

/* Cormorant Garamond — display serif for all headings and pull-quotes */
const cormorant = Cormorant_Garamond({
  variable: "--font-display",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600"],
  style: ["normal", "italic"],
  display: "swap",
});

/* Inter — clean sans for body, labels, and UI text */
const inter = Inter({
  variable: "--font-body",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
});

// const geistSans = Geist({
//   variable: "--font-geist-sans",
//   subsets: ["latin"],
// });

// const geistMono = Geist_Mono({
//   variable: "--font-geist-mono",
//   subsets: ["latin"],
// });

// const playfairDisplay = Playfair_Display({
//   variable: "--font-playfair",
//   subsets: ["latin"],
// });

export const metadata: Metadata = {
  title: "Chingtok Ishaku Ministries",
  description: "Encounter God. Be Inspired. Be Transformed. Powerful worship, life-changing teaching, and ministry that impacts lives worldwide.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${cormorant.variable} ${inter.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
