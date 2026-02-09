'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Users, ScanLine, MessageSquare, Menu } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useState } from 'react';

export default function MobileNav() {
    const pathname = usePathname();
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const navItems = [
        { name: 'Home', href: '/dashboard', icon: LayoutDashboard },
        { name: 'Leads', href: '/leads/hunter', icon: Users },
        { name: 'Scan', href: '/scan', icon: ScanLine }, // Center action
        { name: 'Chat', href: '/whatsapp', icon: MessageSquare },
        { name: 'Menu', href: '#menu', icon: Menu, action: () => setIsMenuOpen(!isMenuOpen) },
    ];

    return (
        <>
            {/* Safe Area Spacer */}
            <div className="h-20 w-full md:hidden" />

            {/* Bottom Nav */}
            <div className="fixed bottom-0 left-0 right-0 h-16 bg-card/90 backdrop-blur-lg border-t border-white/10 flex items-center justify-around px-2 z-50 md:hidden pb-safe">
                {navItems.map((item) => {
                    const isActive = pathname === item.href;
                    const Icon = item.icon;
                    return (
                        <Link
                            key={item.name}
                            href={item.href}
                            onClick={item.action}
                            className={cn(
                                "flex flex-col items-center justify-center w-full h-full space-y-1",
                                isActive ? "text-accent" : "text-gray-400 hover:text-white"
                            )}
                        >
                            <div className={cn(
                                "p-1 rounded-xl transition-all",
                                isActive && "bg-accent/10",
                                item.name === 'Scan' && "bg-accent text-white -mt-8 shadow-lg shadow-accent/50 p-3 rounded-full border-4 border-black"
                            )}>
                                <Icon size={item.name === 'Scan' ? 24 : 22} />
                            </div>
                            {item.name !== 'Scan' && <span className="text-[10px] font-medium">{item.name}</span>}
                        </Link>
                    );
                })}
            </div>
        </>
    );
}
