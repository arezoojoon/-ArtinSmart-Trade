'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
    LayoutDashboard,
    Users,
    MessageSquare,
    Wallet,
    ShoppingBag,
    Kanban,
    Calendar,
    Settings,
    Menu,
    X,
    PhoneCall,
    Box,
    BookOpen,
    TrendingUp,
    BarChart3,
    Megaphone,
    Flag,
    Shield,
    Bot,
    ScanLine
} from 'lucide-react';
import Image from 'next/image';

const menuItems = [
    { name: 'Dashboard', icon: LayoutDashboard, href: '/' },
    { name: 'Lead Generation', icon: Users, href: '/leads/hunter' },
    { name: 'Smart Scanner', icon: ScanLine, href: '/scan' },
    { name: 'Follow-up', icon: PhoneCall, href: '/follow-up' },
    { name: 'Calendar/Scheduling', icon: Calendar, href: '/calendar' },
    { name: 'Products', icon: Box, href: '/products' },
    { name: 'Knowledge Base', icon: BookOpen, href: '/knowledge' },
    { name: 'Market Insights', icon: TrendingUp, href: '/insights' },
    { name: 'Analytics', icon: BarChart3, href: '/analytics' },
    { name: 'Live Chat', icon: MessageSquare, href: '/whatsapp' },
    { name: 'Broadcast', icon: Megaphone, href: '/broadcast' },
    { name: 'Campaigns', icon: Flag, href: '/campaigns' },
    { name: 'Settings', icon: Settings, href: '/settings' },
];

const adminItems = [
    { name: 'Superadmin Panel', icon: Shield, href: '/admin' },
];

export default function Sidebar() {
    const [collapsed, setCollapsed] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);
    const pathname = usePathname();

    return (
        <>
            <button
                className="fixed top-4 left-4 z-50 md:hidden p-2 bg-card rounded-md text-text"
                onClick={() => setMobileOpen(!mobileOpen)}
            >
                {mobileOpen ? <X size={24} /> : <Menu size={24} />}
            </button>

            <div
                className={cn(
                    "fixed inset-y-0 left-0 z-40 bg-card border-r border-gray-800 transition-all duration-300 ease-in-out flex flex-col",
                    collapsed ? "w-20" : "w-64",
                    mobileOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
                )}
            >
                {/* Logo Area */}
                <div className="h-20 flex items-center justify-center border-b border-gray-800 relative bg-background/50 backdrop-blur-sm">
                    <div className="flex items-center gap-3 font-bold text-xl text-text overflow-hidden px-4">
                        <div className={cn("relative transition-all duration-300", collapsed ? "w-10 h-10" : "w-12 h-12")}>
                            <Image src="/logo.png" alt="ArtinExpo Logo" fill className="object-contain" />
                        </div>
                        {!collapsed && (
                            <div className="flex flex-col leading-none">
                                <span className="text-accent text-lg">Artin<span className="text-white">Expo</span></span>
                                <span className="text-[10px] text-text-muted font-normal tracking-wider">SMART AGENT</span>
                            </div>
                        )}
                    </div>

                    <button
                        onClick={() => setCollapsed(!collapsed)}
                        className="hidden md:block absolute -right-3 top-6 bg-accent rounded-full p-1 text-white hover:bg-accent-hover"
                    >
                        {collapsed ? <Menu size={12} /> : <X size={12} />}
                    </button>
                </div>

                {/* Navigation */}
                <nav className="flex-1 overflow-y-auto py-4 scrollbar-hide">
                    <ul className="space-y-1 px-2">
                        {menuItems.map((item) => {
                            const isActive = pathname === item.href;
                            return (
                                <li key={item.name}>
                                    <Link
                                        href={item.href}
                                        className={cn(
                                            "flex items-center gap-3 px-3 py-3 rounded-xl transition-colors",
                                            isActive
                                                ? "bg-accent/10 text-accent"
                                                : "text-text-muted hover:bg-gray-800 hover:text-white",
                                            collapsed && "justify-center px-0"
                                        )}
                                    >
                                        <item.icon size={20} />
                                        {!collapsed && <span className="font-medium text-sm">{item.name}</span>}
                                    </Link>
                                </li>
                            );
                        })}
                    </ul>

                    {/* Admin Section */}
                    <div className="px-4 py-2 mt-4 mb-2">
                        {!collapsed && (
                            <p className="text-[10px] font-semibold text-text-muted uppercase tracking-wider mb-2 opacity-50">
                                Admin
                            </p>
                        )}
                        <ul className="space-y-1">
                            {adminItems.map((item) => {
                                const isActive = pathname === item.href;
                                return (
                                    <li key={item.name}>
                                        <Link
                                            href={item.href}
                                            className={cn(
                                                "flex items-center gap-3 px-3 py-3 rounded-xl transition-colors",
                                                isActive
                                                    ? "bg-accent/10 text-accent"
                                                    : "text-text-muted hover:bg-gray-800 hover:text-white",
                                                collapsed && "justify-center px-0"
                                            )}
                                        >
                                            <item.icon size={20} />
                                            {!collapsed && <span className="font-medium text-sm">{item.name}</span>}
                                        </Link>
                                    </li>
                                );
                            })}
                        </ul>
                    </div>
                </nav>

                {/* User Profile */}
                <div className="p-4 border-t border-gray-800">
                    <div className={cn("flex items-center gap-3", collapsed && "justify-center")}>
                        <div className="w-10 h-10 rounded-full bg-accent/20 flex items-center justify-center text-accent">
                            <Bot size={20} />
                        </div>
                        {!collapsed && (
                            <div className="overflow-hidden">
                                <p className="text-sm font-medium text-white truncate">Super Admin</p>
                                <p className="text-xs text-text-muted truncate">admin@artin.ai</p>
                            </div>
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
