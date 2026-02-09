import Sidebar from "@/components/Layout/Sidebar";
import MobileNav from "@/components/Layout/MobileNav"; // Updated import

export default function DashboardLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <div className="flex h-screen overflow-hidden bg-background">
            <Sidebar />
            <main className="flex-1 overflow-auto md:ml-64 pb-24 md:pb-8 pt-20 md:pt-8 transition-all duration-300 touch-pan-y relative z-0">
                {/* pb-24 accounts for MobileNav (h-16 + spacing) */}
                {children}
            </main>
            <MobileNav />
        </div>
    );
}
