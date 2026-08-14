import type { Metadata } from "next";
import { IBM_Plex_Mono, Manrope } from "next/font/google";
import { siteUrl } from "@/lib/site";
import "./globals.css";

const sans = Manrope({ subsets: ["latin"], variable: "--font-sans", display: "swap" });
const mono = IBM_Plex_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl()),
  title: "QueryProof — Answers with evidence",
  description: "Traceable analytics over synthetic data: visible SQL, sources, row counts and evaluation cases.",
  authors: [{ name: "Jordan Andrade", url: "https://jord-andrade.dev" }],
  openGraph: {
    title: "QueryProof — Answers with evidence",
    description: "Ask a structured dataset and audit every number.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "QueryProof — Answers with evidence",
    description: "Ask a structured dataset and audit every number.",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html className={`${sans.variable} ${mono.variable}`} lang="en">
      <body>{children}</body>
    </html>
  );
}
