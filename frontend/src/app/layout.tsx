import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "VisaAtGlance",
  description: "US visa information, processing trends, and timeline data at a glance.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
