'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Scan, MessageSquare, BarChart, ShoppingBag } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function BottomNav() {
    const pathname = usePathname();

    const navItems = [
        { name: 'Home', href: '/', icon: Home },
        { name: 'Leads', href: '/leads', icon: BarChart },
        { name: 'Scan', href: '/leads/hunter', icon: Scan },
        { name: 'Chat', href: '/whatsapp', icon: MessageSquare },
        { name: 'Trade', href: '/marketplace', icon: ShoppingBag },
    ];

    // Hide on desktop (md and up)
    return (
        <div className="md:hidden fixed bottom-0 left-0 right-0 bg-card border-t border-gray-800 pb-safe z-50">
            <div className="flex justify-around items-center h-16">
                {navItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.name}
                            href={item.href}
                            className={cn(
                                "flex flex-col items-center justify-center w-full h-full space-y-1",
                                isActive ? "text-accent" : "text-gray-500 hover:text-gray-300"
                            )}
                        >
                            <item.icon size={20} className={cn(isActive && "fill-current/20")} />
                            <span className="text-[10px] font-medium">{item.name}</span>
                        </Link>
                    );
                })}
            </div>
        </div>
    );
}
