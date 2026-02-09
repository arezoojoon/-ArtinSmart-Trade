'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import Link from "next/link";
import { ArrowRight, CheckCircle2, Globe, Shield, Zap, Loader2, TrendingUp } from "lucide-react";
import Image from "next/image";

export default function LandingPage() {
  const router = useRouter();
  const { user, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && user) {
      router.push('/dashboard');
    }
  }, [user, isLoading]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background text-white selection:bg-accent selection:text-white flex justify-center items-center">
        <Loader2 size={50} />
      </div>
    );
  }

  if (user) {
    return (
      <div className="min-h-screen bg-background text-white selection:bg-accent selection:text-white flex justify-center items-center">
        <TrendingUp size={50} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-white selection:bg-accent selection:text-white">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-lg border-b border-white/10">
        <div className="container mx-auto px-6 h-24 flex items-center justify-between"> {/* Increased height from h-16 to h-24 */}
          <div className="flex items-center gap-4"> {/* Increased gap */}
            <div className="w-20 h-20 relative"> {/* Logo size 20 */}
              <img src="/logo.png" alt="Artin Trade" className="object-contain w-full h-full" />
            </div>
            <span className="font-bold text-3xl tracking-tight"> {/* Text size 3xl */}
              <span className="text-accent">Artin</span><span className="text-white">Smart Trade</span>
            </span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login" className="text-sm font-medium text-gray-300 hover:text-white transition">
              Sign In
            </Link>
            <Link href="/register" className="btn-primary bg-white text-black hover:bg-gray-200 px-4 py-2 rounded-full text-sm font-bold transition">
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative pt-40 pb-20 overflow-hidden"> {/* Increased padding top */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-accent/20 rounded-[100%] blur-[100px] pointer-events-none" />

        <div className="container mx-auto px-6 text-center relative z-10">

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6 bg-gradient-to-b from-white to-gray-400 bg-clip-text text-transparent animate-in fade-in slide-in-from-bottom-6 duration-700 delay-100">
            The World's First <br />
            <span className="text-white">AI Trade Operating System</span>
          </h1>

          <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-10 animate-in fade-in slide-in-from-bottom-7 duration-700 delay-200">
            Automate your B2B sales, find leads with AI, and close deals on WhatsApp.
            Powered by Gemini Vision & Voice.
          </p>

          <div className="flex flex-col md:flex-row items-center justify-center gap-4 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-300">
            <Link href="/register" className="w-full md:w-auto bg-accent hover:bg-accent-hover text-white px-8 py-4 rounded-full font-bold text-lg transition flex items-center justify-center gap-2">
              Start Free Trial <ArrowRight size={20} />
            </Link>
            <Link href="#features" className="w-full md:w-auto bg-white/5 hover:bg-white/10 border border-white/10 text-white px-8 py-4 rounded-full font-medium text-lg transition">
              View Demo
            </Link>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <section id="features" className="py-20 bg-black/50 border-t border-white/10">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard
              icon={Globe}
              title="Global Lead Hunter"
              desc="Scrape thousands of verified leads from Google Maps & Directories in seconds."
            />
            <FeatureCard
              icon={Zap} // Vision
              title="Smart Scanner"
              desc="Scan business cards with Gemini Vision. Extracts data with 99% accuracy."
            />
            <FeatureCard
              icon={Shield}
              title="Verified Marketplace"
              desc="Connect with trusted suppliers and buyers in a secure environment."
            />
          </div>
        </div>
      </section>

      {/* Mobile App Preview Section */}
      <section className="py-24 relative overflow-hidden">
        <div className="container mx-auto px-6 flex flex-col md:flex-row items-center gap-12">
          <div className="flex-1 space-y-8">
            <h2 className="text-4xl font-bold">Your Business, <br /> <span className="text-accent">In Your Pocket.</span></h2>
            <p className="text-gray-400 text-lg">
              Access your entire trade operation from anywhere.
              Chat with leads via Voice Notes, scan cards instantly, and manage deals on the go.
            </p>
            <div className="space-y-4">
              <CheckItem text="Works Offline (PWA)" />
              <CheckItem text="Real-time Voice Translation" />
              <CheckItem text="WhatsApp Integration" />
            </div>
          </div>
          <div className="flex-1 flex justify-center relative">
            <div className="w-[300px] h-[600px] bg-gray-900 border-8 border-gray-800 rounded-[3rem] p-4 relative shadow-2xl rotate-3 hover:rotate-0 transition duration-500">
              <div className="w-full h-full bg-black rounded-[2rem] overflow-hidden relative">
                {/* Mock Screen Content */}
                <div className="absolute inset-0 bg-gradient-to-b from-background to-card flex items-center justify-center text-gray-500">
                  App Preview
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-white/10 text-center text-gray-500 text-sm">
        <p>&copy; 2026 Artin Smart Trade. All rights reserved.</p>
      </footer>
    </div>
  );
}

function FeatureCard({ icon: Icon, title, desc }: any) {
  return (
    <div className="bg-white/5 border border-white/10 p-8 rounded-3xl hover:bg-white/10 transition duration-300">
      <div className="w-12 h-12 bg-accent/20 rounded-xl flex items-center justify-center mb-6 text-accent">
        <Icon size={24} />
      </div>
      <h3 className="text-xl font-bold mb-3">{title}</h3>
      <p className="text-gray-400 leading-relaxed">{desc}</p>
    </div>
  )
}

function CheckItem({ text }: { text: string }) {
  return (
    <div className="flex items-center gap-3">
      <div className="w-6 h-6 rounded-full bg-green-500/20 flex items-center justify-center text-green-500">
        <CheckCircle2 size={14} />
      </div>
      <span className="font-medium text-gray-300">{text}</span>
    </div>
  )
}
