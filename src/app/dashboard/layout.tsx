'use client';

import Sidebar from '@/components/Layout/Sidebar';
import { useAuth } from '@/context/AuthContext';
import { Loader2 } from 'lucide-react';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    const { isLoading, isAuthenticated } = useAuth();

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    if (!isAuthenticated) {
        return null;
    }

    return (
        <div className="min-h-screen bg-background">
            <Sidebar />
            <main className="md:ml-64 min-h-screen transition-all duration-300">
                <div className="p-6">
                    {children}
                </div>
            </main>
        </div>
    );
}
