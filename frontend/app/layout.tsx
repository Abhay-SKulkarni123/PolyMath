import type { Metadata } from "next";
import Navbar from "@/components/Navbar";
import MagicBackground from "@/components/MagicBackground";
import "./globals.css";

export const metadata: Metadata = {
  title: "Polymath — Cinema Universe & Knowledge Marketplace",
  description: "Explore curated cinematic universes and premium knowledge books.",
};

// Navbar and MagicBackground render here ONCE, at the true root of the app,
// outside and above every individual page's own wrapper div. This is the
// correct Next.js pattern - it fixes the structural overlap risk that came
// from each of the 13 pages rendering its own <Navbar /> as a child of its
// own div, which made stacking context fragile and hard to reason about.
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-scroll-behavior="smooth">
      <body style={{ margin: 0, backgroundColor: "#0a0612" }}>
        <MagicBackground />
        <Navbar />
        <main style={{ position: "relative", zIndex: 1}}>
          {children}
        </main>
      </body>
    </html>
  );
}