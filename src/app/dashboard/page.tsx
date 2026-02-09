'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import Link from 'next/link';
import {
    ShoppingBag, BarChart3, TrendingUp, Users, Briefcase,
    Search, BrainCircuit, AlertTriangle, ArrowUpRight
} from 'lucide-react';

interface DashboardStats {
    total_products: number;
    total_trades: number;
    total_trade_value: number;
    active_risk_alerts: number;
    current_month: number;
}

interface PipelineData {
    [key: string]: { count: number; total_value: number };
}

export default function DashboardPage() {
    const { user } = useAuth();
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [pipeline, setPipeline] = useState<PipelineData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function load() {
            try {
                const [s, p] = await Promise.allSettled([
                    api.get('/analytics/dashboard/summary'),
                    api.get('/deals/pipeline/summary'),
                ]);
                if (s.status === 'fulfilled') setStats(s.value);
                if (p.status === 'fulfilled') setPipeline(p.value);
            } catch {}
            setLoading(false);
        }
        load();
    }, []);

    const statCards = [
        { label: 'Products', value: stats?.total_products ?? 0, icon: ShoppingBag, href: '/dashboard/products', color: 'text-blue-400' },
        { label: 'Total Trades', value: stats?.total_trades ?? 0, icon: BarChart3, href: '/dashboard/trades', color: 'text-emerald-400' },
        { label: 'Trade Value', value: `$${(stats?.total_trade_value ?? 0).toLocaleString()}`, icon: TrendingUp, href: '/dashboard/analytics', color: 'text-primary' },
        { label: 'Risk Alerts', value: stats?.active_risk_alerts ?? 0, icon: AlertTriangle, href: '/dashboard/analytics', color: 'text-red-400' },
    ];

    const quickLinks = [
        { name: 'AI Assistant', desc: 'Ask trade questions', icon: BrainCircuit, href: '/dashboard/ai-chat' },
        { name: 'Find Suppliers', desc: 'Hunter lead gen', icon: Search, href: '/dashboard/hunter' },
        { name: 'CRM Contacts', desc: 'Manage relationships', icon: Users, href: '/dashboard/crm' },
        { name: 'Deal Pipeline', desc: 'Track negotiations', icon: Briefcase, href: '/dashboard/deals' },
    ];

    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold">Welcome back{user?.full_name ? `, ${user.full_name}` : ''}</h1>
                    <p className="text-muted-foreground text-sm mt-1">
                        {monthNames[(stats?.current_month ?? 1) - 1]} Market Overview &bull; Role: <span className="capitalize text-primary">{user?.role}</span>
                    </p>
                </div>
                <Badge variant="default" className="text-sm">{user?.plan || 'Free'} Plan</Badge>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                {statCards.map((s) => (
                    <Link key={s.label} href={s.href}>
                        <Card className="hover:border-primary/50 transition-colors cursor-pointer">
                            <CardContent className="p-4">
                                <div className="flex items-center justify-between">
                                    <s.icon className={`h-5 w-5 ${s.color}`} />
                                    <ArrowUpRight className="h-3 w-3 text-muted-foreground" />
                                </div>
                                <div className="mt-3">
                                    <p className="text-2xl font-bold">{loading ? '...' : s.value}</p>
                                    <p className="text-xs text-muted-foreground">{s.label}</p>
                                </div>
                            </CardContent>
                        </Card>
                    </Link>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Deal Pipeline */}
                <Card className="lg:col-span-2">
                    <CardHeader>
                        <CardTitle className="text-lg">Deal Pipeline</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {pipeline ? (
                            <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
                                {Object.entries(pipeline).map(([stage, data]) => (
                                    <div key={stage} className="text-center p-3 bg-secondary/50 rounded-lg">
                                        <p className="text-lg font-bold">{data.count}</p>
                                        <p className="text-[10px] text-muted-foreground uppercase tracking-wider">{stage}</p>
                                        <p className="text-xs text-primary mt-1">${data.total_value.toLocaleString()}</p>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-muted-foreground text-sm">
                                {loading ? 'Loading pipeline...' : 'No deals yet. Start creating deals to see your pipeline.'}
                            </p>
                        )}
                    </CardContent>
                </Card>

                {/* Quick Actions */}
                <Card>
                    <CardHeader>
                        <CardTitle className="text-lg">Quick Actions</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                        {quickLinks.map((link) => (
                            <Link key={link.name} href={link.href}>
                                <div className="flex items-center gap-3 p-3 rounded-lg hover:bg-secondary/50 transition-colors cursor-pointer">
                                    <link.icon className="h-5 w-5 text-primary" />
                                    <div>
                                        <p className="text-sm font-medium">{link.name}</p>
                                        <p className="text-xs text-muted-foreground">{link.desc}</p>
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </CardContent>
                </Card>
            </div>

            {/* AI Assistant Prompt */}
            <Card className="bg-gradient-to-r from-primary/10 via-card to-card border-primary/20">
                <CardContent className="p-6 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <BrainCircuit className="h-10 w-10 text-primary" />
                        <div>
                            <h3 className="font-bold text-lg">Artin AI Trade Assistant</h3>
                            <p className="text-sm text-muted-foreground">Get AI-powered insights on pricing, seasonality, and supplier discovery</p>
                        </div>
                    </div>
                    <Link href="/dashboard/ai-chat">
                        <button className="px-6 py-2 bg-primary text-primary-foreground font-semibold rounded-lg hover:bg-primary/90 transition-all whitespace-nowrap">
                            Ask AI
                        </button>
                    </Link>
                </CardContent>
            </Card>
        </div>
    );
}
