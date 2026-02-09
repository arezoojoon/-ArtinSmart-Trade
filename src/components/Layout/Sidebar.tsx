
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { useAuth } from '@/context/AuthContext';
import {
    LayoutDashboard,
    ShoppingBag,
    BarChart3,
    MessageSquare,
    Settings,
    Menu,
    X,
    TrendingUp,
    Users,
    Briefcase,
    Shield,
    LogOut,
    Search,
    BrainCircuit
} from 'lucide-react';
import Image from 'next/image';

const menuItems = [
    { name: 'Dashboard', icon: LayoutDashboard, href: '/dashboard', roles: ['buyer', 'seller', 'both', 'admin'] },
    { name: 'Products', icon: ShoppingBag, href: '/dashboard/products', roles: ['buyer', 'seller', 'both', 'admin'] },
    { name: 'Trades', icon: BarChart3, href: '/dashboard/trades', roles: ['buyer', 'seller', 'both', 'admin'] },
    { name: 'Analytics', icon: TrendingUp, href: '/dashboard/analytics', roles: ['buyer', 'seller', 'both', 'admin'] },
    { name: 'AI Assistant', icon: BrainCircuit, href: '/dashboard/ai-chat', roles: ['buyer', 'seller', 'both', 'admin'] },
    { name: 'Deals', icon: Briefcase, href: '/dashboard/deals', roles: ['buyer', 'seller', 'both', 'admin'] },
    { name: 'CRM', icon: Users, href: '/dashboard/crm', roles: ['buyer', 'seller', 'both', 'admin'] },
    { name: 'Hunter', icon: Search, href: '/dashboard/hunter', roles: ['buyer', 'seller', 'both', 'admin'] },
    { name: 'Billing', icon: Settings, href: '/dashboard/billing', roles: ['buyer', 'seller', 'both', 'admin'] },
    { name: 'Admin', icon: Shield, href: '/dashboard/admin', roles: ['admin', 'super_admin'] },
];

export default function Sidebar() {
    const [collapsed, setCollapsed] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);
    const { user, logout } = useAuth();
    const pathname = usePathname();

    const filteredItems = menuItems.filter(item => {
        if (!user) return false;
        return item.roles.includes(user.role) || user.role === 'super_admin';
    });

    return (
        <>
            <button
                className="fixed top-4 left-4 z-50 md:hidden p-2 bg-card rounded-md text-foreground"
                onClick={() => setMobileOpen(!mobileOpen)}
            >
                {mobileOpen ? <X size={24} /> : <Menu size={24} />}
            </button>

            <div
                className={cn(
                    "fixed inset-y-0 left-0 z-40 bg-card border-r border-border transition-all duration-300 ease-in-out flex flex-col",
                    collapsed ? "w-20" : "w-64",
                    mobileOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
                )}
            >
                {/* Logo Area */}
                <div className="h-20 flex items-center justify-center border-b border-border relative bg-background/50 backdrop-blur-sm">
                    <div className="flex items-center gap-3 font-bold text-xl text-foreground overflow-hidden px-4">
                        <div className={cn("relative transition-all duration-300", collapsed ? "w-8 h-8" : "w-10 h-10")}>
                            {/* Ensure logo.png exists in public folder, or use text fallback */}
                            <Image src="/logo.png" alt="Logo" width={40} height={40} className="object-contain" onError={(e) => { e.currentTarget.style.display = 'none' }} />
                        </div>
                        {!collapsed && (
                            <div className="flex flex-col leading-none">
                                <span className="text-primary text-lg">Artin <span className="text-foreground">Smart Trade</span></span>
                                <span className="text-[10px] text-muted-foreground font-normal tracking-wider">AI OPERATING SYSTEM</span>
                            </div>
                        )}
                    </div>

                    <button
                        onClick={() => setCollapsed(!collapsed)}
                        className="hidden md:block absolute -right-3 top-6 bg-primary rounded-full p-1 text-primary-foreground hover:bg-primary/90"
                    >
                        {collapsed ? <Menu size={12} /> : <X size={12} />}
                    </button>
                </div>

                {/* Navigation */}
                <nav className="flex-1 overflow-y-auto py-4">
                    <ul className="space-y-1 px-2">
                        {filteredItems.map((item) => {
                            const isActive = pathname === item.href || pathname?.startsWith(item.href + '/');
                            return (
                                <li key={item.name}>
                                    <Link
                                        href={item.href}
                                        className={cn(
                                            "flex items-center gap-3 px-3 py-3 rounded-xl transition-colors",
                                            isActive
                                                ? "bg-primary/10 text-primary"
                                                : "text-muted-foreground hover:bg-muted hover:text-foreground",
                                            collapsed && "justify-center px-0"
                                        )}
                                        title={collapsed ? item.name : undefined}
                                    >
                                        <item.icon size={20} />
                                        {!collapsed && <span className="font-medium text-sm">{item.name}</span>}
                                    </Link>
                                </li>
                            );
                        })}
                    </ul>
                </nav>

                {/* User Profile */}
                <div className="p-4 border-t border-border">
                    <div className={cn("flex items-center gap-3", collapsed && "justify-center")}>
                        <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary">
                            <span className="font-bold text-lg">{user?.email?.[0].toUpperCase() || 'U'}</span>
                        </div>
                        {!collapsed && (
                            <div className="overflow-hidden flex-1">
                                <p className="text-sm font-medium text-foreground truncate capitalize">{user?.role || 'Guest'}</p>
                                <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
                            </div>
                        )}
                        {!collapsed && (
                            <button
                                onClick={logout}
                                className="p-2 text-destructive hover:bg-destructive/10 rounded-lg transition-colors flex items-center gap-2"
                                title="Log Out"
                            >
                                <LogOut size={16} />
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* Overlay for mobile */}
            {mobileOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-30 md:hidden"
                    onClick={() => setMobileOpen(false)}
                />
            )}
        </>
    );
}
