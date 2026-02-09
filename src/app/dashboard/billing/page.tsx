'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Loader2, Check, Crown, Zap, Shield } from 'lucide-react';

interface Plan {
    name: string;
    price: number;
    max_products: number;
    max_trades: number;
    max_contacts: number;
    hunter_enabled: boolean;
    ai_queries_per_day: number;
}

interface Usage {
    products_used: number;
    products_limit: number;
    trades_used: number;
    trades_limit: number;
    contacts_used: number;
    contacts_limit: number;
    ai_queries_today: number;
    ai_queries_limit: number;
    hunter_enabled: boolean;
}

const planIcons: Record<string, any> = {
    free: Zap,
    starter: Zap,
    pro: Crown,
    enterprise: Shield,
};

const planHighlights: Record<string, string> = {
    free: 'Get started with basic features',
    starter: 'For growing trade businesses',
    pro: 'Full power for serious traders',
    enterprise: 'Unlimited everything for teams',
};

export default function BillingPage() {
    const [plans, setPlans] = useState<Plan[]>([]);
    const [usage, setUsage] = useState<Usage | null>(null);
    const [currentPlan, setCurrentPlan] = useState<string>('free');
    const [loading, setLoading] = useState(true);
    const [upgrading, setUpgrading] = useState('');

    useEffect(() => {
        async function load() {
            try {
                const [p, u, s] = await Promise.allSettled([
                    api.get('/billing/plans'),
                    api.get('/billing/usage'),
                    api.get('/billing/subscription'),
                ]);
                if (p.status === 'fulfilled') setPlans(p.value);
                if (u.status === 'fulfilled') setUsage(u.value);
                if (s.status === 'fulfilled') setCurrentPlan(s.value.plan || 'free');
            } catch {}
            setLoading(false);
        }
        load();
    }, []);

    const handleUpgrade = async (planName: string) => {
        setUpgrading(planName);
        try {
            await api.post('/billing/upgrade', { plan: planName });
            setCurrentPlan(planName);
            const u = await api.get('/billing/usage');
            setUsage(u);
        } catch {}
        setUpgrading('');
    };

    const usagePercent = (used: number, limit: number) => {
        if (limit <= 0) return 0;
        return Math.min((used / limit) * 100, 100);
    };

    const usageColor = (pct: number) => {
        if (pct >= 90) return 'bg-red-500';
        if (pct >= 70) return 'bg-yellow-500';
        return 'bg-primary';
    };

    if (loading) {
        return <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>;
    }

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Billing & Subscription</h1>
                <p className="text-muted-foreground text-sm">
                    Current plan: <span className="text-primary font-medium capitalize">{currentPlan}</span>
                </p>
            </div>

            {/* Usage Overview */}
            {usage && (
                <Card>
                    <CardHeader><CardTitle className="text-lg">Current Usage</CardTitle></CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                            {[
                                { label: 'Products', used: usage.products_used, limit: usage.products_limit },
                                { label: 'Trades', used: usage.trades_used, limit: usage.trades_limit },
                                { label: 'Contacts', used: usage.contacts_used, limit: usage.contacts_limit },
                                { label: 'AI Queries Today', used: usage.ai_queries_today, limit: usage.ai_queries_limit },
                            ].map(item => {
                                const pct = usagePercent(item.used, item.limit);
                                return (
                                    <div key={item.label}>
                                        <div className="flex justify-between text-sm mb-1">
                                            <span className="text-muted-foreground">{item.label}</span>
                                            <span className="font-mono">{item.used}/{item.limit === 999999 ? '∞' : item.limit}</span>
                                        </div>
                                        <div className="h-2 bg-secondary rounded-full overflow-hidden">
                                            <div className={`h-full rounded-full transition-all ${usageColor(pct)}`} style={{ width: `${pct}%` }} />
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                        <div className="mt-4 flex items-center gap-2 text-sm">
                            <span className="text-muted-foreground">Hunter Access:</span>
                            <Badge variant={usage.hunter_enabled ? 'default' : 'secondary'}>
                                {usage.hunter_enabled ? 'Enabled' : 'Disabled'}
                            </Badge>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Plans */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {plans.map(plan => {
                    const Icon = planIcons[plan.name] || Zap;
                    const isCurrent = plan.name === currentPlan;
                    return (
                        <Card key={plan.name} className={`relative ${isCurrent ? 'border-primary ring-1 ring-primary/30' : 'hover:border-primary/30'} transition-all`}>
                            {isCurrent && (
                                <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                                    <Badge variant="default">Current</Badge>
                                </div>
                            )}
                            <CardContent className="p-6 text-center">
                                <Icon className="h-8 w-8 mx-auto text-primary mb-3" />
                                <h3 className="text-lg font-bold capitalize">{plan.name}</h3>
                                <p className="text-xs text-muted-foreground mb-4">{planHighlights[plan.name] || ''}</p>
                                <div className="mb-4">
                                    <span className="text-3xl font-bold">${plan.price}</span>
                                    <span className="text-muted-foreground text-sm">/mo</span>
                                </div>
                                <div className="space-y-2 text-sm text-left mb-6">
                                    <div className="flex items-center gap-2"><Check className="h-4 w-4 text-primary" /><span>{plan.max_products === 999999 ? 'Unlimited' : plan.max_products} products</span></div>
                                    <div className="flex items-center gap-2"><Check className="h-4 w-4 text-primary" /><span>{plan.max_trades === 999999 ? 'Unlimited' : plan.max_trades} trades</span></div>
                                    <div className="flex items-center gap-2"><Check className="h-4 w-4 text-primary" /><span>{plan.max_contacts === 999999 ? 'Unlimited' : plan.max_contacts} contacts</span></div>
                                    <div className="flex items-center gap-2"><Check className="h-4 w-4 text-primary" /><span>{plan.ai_queries_per_day === 999999 ? 'Unlimited' : plan.ai_queries_per_day} AI queries/day</span></div>
                                    <div className="flex items-center gap-2">
                                        <Check className={`h-4 w-4 ${plan.hunter_enabled ? 'text-primary' : 'text-muted-foreground'}`} />
                                        <span className={plan.hunter_enabled ? '' : 'text-muted-foreground line-through'}>Hunter Engine</span>
                                    </div>
                                </div>
                                {isCurrent ? (
                                    <Button variant="outline" className="w-full" disabled>Current Plan</Button>
                                ) : (
                                    <Button className="w-full" onClick={() => handleUpgrade(plan.name)} disabled={!!upgrading}>
                                        {upgrading === plan.name ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                                        {plan.price === 0 ? 'Downgrade' : 'Upgrade'}
                                    </Button>
                                )}
                            </CardContent>
                        </Card>
                    );
                })}
            </div>
        </div>
    );
}
