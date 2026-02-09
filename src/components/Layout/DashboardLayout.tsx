
'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';
import Sidebar from './Sidebar';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return <div className="min-h-screen bg-background flex items-center justify-center text-primary">Loading...</div>;
  }

  if (!isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-background flex">
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 lg:ml-64">
        {/* Adjusted left margin since sidebar is fixed */}
        {/* If sidebar is static (not fixed), then no margin needed if flex is working, 
            but the sidebar implementation uses fixed positioning for transition support typically. 
            Let's accept Sidebar is fixed for now or update it. 
            Actually Sidebar in previous step was fixed/sticky. 
            In the new Sidebar code, it uses fixed. So we need margin-left. 
        */}

        <main className="flex-1 overflow-y-auto p-4 md:p-8 bg-background">
          <div className="max-w-7xl mx-auto animate-in fade-in duration-500">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
