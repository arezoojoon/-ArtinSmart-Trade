'use client'; // Needed for sidebar which uses usePathname

import AdminSidebar from "@/components/Admin/AdminSidebar";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex h-screen bg-black text-white overflow-hidden font-sans">
            <AdminSidebar />
            <main className="flex-1 md:ml-64 overflow-y-auto bg-black p-8 relative">
                {/* Background Gradients for Admin Feel */}
                <div className="absolute top-0 left-0 w-full h-96 bg-gradient-to-b from-red-900/10 to-transparent pointer-events-none" />
                <div className="relative z-10 w-full max-w-7xl mx-auto">
                    {children}
                </div>
            </main>
        </div>
    );
}
