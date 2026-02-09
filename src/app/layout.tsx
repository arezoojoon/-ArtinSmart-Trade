
import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { AuthProvider } from "@/context/AuthContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: {
    default: 'Artin Smart Trade - AI Intelligence Platform',
    template: '%s | Artin Smart Trade',
  },
  description: 'Advanced AI Trade Intelligence & Lead Generation Platform for FMCG',
  manifest: "/manifest.json",
};

export const viewport: Viewport = {
  themeColor: "#0f172a",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false, // App-like feel
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={cn(inter.className, "bg-background text-foreground min-h-screen overscroll-none")}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
