'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Loader2, TrendingUp, AlertTriangle, Calendar, BarChart3 } from 'lucide-react';

export default function AnalyticsPage() {
    const [seasonal, setSeasonal] = useState<any>(null);
    const [risks, setRisks] = useState<any[]>([]);
    const [heatmap, setHeatmap] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function load() {
            try {
                const [s, r, h] = await Promise.allSettled([
                    api.get('/analytics/seasonal/current'),
                    api.get('/analytics/risk-overview'),
                    api.get('/analytics/demand-heatmap'),
                ]);
                if (s.status === 'fulfilled') setSeasonal(s.value);
                if (r.status === 'fulfilled') setRisks(r.value);
                if (h.status === 'fulfilled') setHeatmap(h.value);
            } catch {}
            setLoading(false);
        }
        load();
    }, []);

    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const severityColors: Record<string, string> = {
        low: 'bg-yellow-500/20 text-yellow-400',
        medium: 'bg-orange-500/20 text-orange-400',
        high: 'bg-red-500/20 text-red-400',
        critical: 'bg-red-600/30 text-red-300',
    };
    const demandColors: Record<string, string> = {
        low: 'bg-blue-900/50',
        medium: 'bg-primary/30',
        high: 'bg-primary/70',
    };

    if (loading) {
        return <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>;
    }

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Market Analytics & Seasonality</h1>
                <p className="text-muted-foreground text-sm">
                    Current month: <span className="text-primary font-medium">{monthNames[(seasonal?.month ?? 1) - 1]}</span>
                </p>
            </div>

            {/* Current Seasonal Insights */}
            <Card>
                <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                        <Calendar className="h-5 w-5 text-primary" />
                        Seasonal Insights — {monthNames[(seasonal?.month ?? 1) - 1]}
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    {seasonal?.insights?.length > 0 ? (
                        <div className="space-y-4">
                            {seasonal.insights.map((ins: any, i: number) => (
                                <div key={i} className="p-4 bg-secondary/30 rounded-lg border border-border">
                                    <div className="flex items-center justify-between mb-2">
                                        <h3 className="font-semibold">{ins.product}</h3>
                                        <Badge variant={ins.in_season ? 'default' : 'secondary'}>
                                            {ins.in_season ? 'In Season' : 'Off Season'}
                                        </Badge>
                                    </div>
                                    {ins.demand_levels?.length > 0 && (
                                        <div className="flex gap-2 flex-wrap mt-2">
                                            {ins.demand_levels.map((d: any, j: number) => (
                                                <span key={j} className="text-xs bg-primary/10 text-primary px-2 py-1 rounded">
                                                    {d.region}: {d.level}
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                    {ins.price_indices?.length > 0 && (
                                        <div className="flex gap-2 flex-wrap mt-2">
                                            {ins.price_indices.map((p: any, j: number) => (
                                                <span key={j} className="text-xs bg-emerald-500/10 text-emerald-400 px-2 py-1 rounded">
                                                    {p.region}: ${p.avg_price} (vol: {p.volatility})
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                    {ins.risk_alerts?.length > 0 && (
                                        <div className="flex gap-2 flex-wrap mt-2">
                                            {ins.risk_alerts.map((r: any, j: number) => (
                                                <span key={j} className={`text-xs px-2 py-1 rounded ${severityColors[r.severity] || 'bg-secondary'}`}>
                                                    {r.region}: {r.type} ({r.severity})
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-muted-foreground text-sm py-4 text-center">
                            No seasonal data yet. Add product seasons and price indices to see insights.
                        </p>
                    )}
                </CardContent>
            </Card>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Risk Overview */}
                <Card>
                    <CardHeader>
                        <CardTitle className="text-lg flex items-center gap-2">
                            <AlertTriangle className="h-5 w-5 text-red-400" />
                            Risk Alerts
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        {risks.length > 0 ? (
                            <div className="space-y-2 max-h-80 overflow-y-auto">
                                {risks.map((r, i) => (
                                    <div key={i} className={`p-3 rounded-lg flex items-center justify-between ${r.is_current ? 'border border-red-500/30' : 'border border-border'}`}>
                                        <div>
                                            <p className="text-sm font-medium">{r.risk_type}</p>
                                            <p className="text-xs text-muted-foreground">{r.region} — {monthNames[(r.month || 1) - 1]}</p>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            {r.is_current && <Badge variant="destructive">Active</Badge>}
                                            <span className={`text-xs px-2 py-1 rounded capitalize ${severityColors[r.severity] || 'bg-secondary'}`}>
                                                {r.severity}
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-muted-foreground text-sm py-4 text-center">No risk alerts configured.</p>
                        )}
                    </CardContent>
                </Card>

                {/* Demand Heatmap */}
                <Card>
                    <CardHeader>
                        <CardTitle className="text-lg flex items-center gap-2">
                            <BarChart3 className="h-5 w-5 text-primary" />
                            Demand Heatmap
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        {heatmap.length > 0 ? (
                            <div className="space-y-2 max-h-80 overflow-y-auto">
                                {heatmap.map((h, i) => (
                                    <div key={i} className={`p-2 rounded flex items-center justify-between ${demandColors[h.demand_level] || 'bg-secondary/30'}`}>
                                        <div>
                                            <span className="text-sm font-medium">{h.product}</span>
                                            <span className="text-xs text-muted-foreground ml-2">({h.region})</span>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <span className="text-xs">{monthNames[(h.month || 1) - 1]}</span>
                                            <Badge variant={h.demand_level === 'high' ? 'default' : 'secondary'}>
                                                {h.demand_level}
                                            </Badge>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-muted-foreground text-sm py-4 text-center">Add product seasonal data to view demand patterns.</p>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
