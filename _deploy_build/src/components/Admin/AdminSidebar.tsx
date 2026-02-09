import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    LayoutDashboard,
    Users,
    Settings,
    Database,
    ShieldAlert,
    LogOut,
    Activity
} from 'lucide-react';
import { cn } from '@/lib/utils'; // Keep using shared utils

const menuItems = [
    { icon: LayoutDashboard, label: 'Overview', href: '/admin' },
    { icon: Users, label: 'User Management', href: '/admin/users' },
    { icon: Database, label: 'Tenants & Data', href: '/admin/tenants' },
    { icon: Activity, label: 'System Health', href: '/admin/health' },
    { icon: Settings, label: 'Configuration', href: '/admin/settings' },
];

export default function AdminSidebar() {
    const pathname = usePathname(); // This hook works in client components

    return (
        <aside className="hidden md:flex flex-col w-64 bg-zinc-950 border-r border-red-900/20 h-screen fixed left-0 top-0 z-50">
            <div className="p-6 flex items-center gap-3">
                <div className="w-10 h-10 bg-red-600 rounded-xl flex items-center justify-center shadow-lg shadow-red-600/20">
                    <ShieldAlert className="text-white" size={24} />
                </div>
                <div>
                    <h1 className="font-bold text-white text-lg tracking-tight">Super Admin</h1>
                    <p className="text-xs text-red-500 font-mono">GOD MODE</p>
                </div>
            </div>

            <nav className="flex-1 px-4 py-4 space-y-2 overflow-y-auto">
                {menuItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group relative overflow-hidden",
                                isActive
                                    ? "bg-red-900/20 text-red-500 font-medium border border-red-900/30"
                                    : "text-gray-400 hover:text-white hover:bg-white/5"
                            )}
                        >
                            <item.icon size={20} className={cn("transition-colors", isActive ? "text-red-500" : "group-hover:text-white")} />
                            <span>{item.label}</span>
                            {isActive && (
                                <div className="absolute right-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-red-500 rounded-l-full shadow-[0_0_10px_#ef4444]" />
                            )}
                        </Link>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-red-900/20">
                <button className="flex items-center gap-3 px-4 py-3 w-full text-left text-gray-400 hover:text-red-400 hover:bg-red-900/10 rounded-xl transition-all">
                    <LogOut size={20} />
                    <span>Exit God Mode</span>
                </button>
            </div>
        </aside>
    );
}
