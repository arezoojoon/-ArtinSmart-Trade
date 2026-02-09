'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Plus, Loader2, X, Briefcase, Calculator, Trash2 } from 'lucide-react';

interface Deal {
    id: string;
    title: string;
    stage: string;
    value: number;
    volume: number;
    unit_price: number;
    currency: string;
    buy_price: number | null;
    sell_price: number | null;
    margin_percent: number | null;
    ai_recommendation: string | null;
    notes: string | null;
    created_at: string | null;
    closed_at: string | null;
}

const stageColors: Record<string, string> = {
    lead: 'bg-gray-500/20 text-gray-400',
    qualified: 'bg-blue-500/20 text-blue-400',
    proposal: 'bg-purple-500/20 text-purple-400',
    negotiation: 'bg-yellow-500/20 text-yellow-400',
    won: 'bg-emerald-500/20 text-emerald-400',
    lost: 'bg-red-500/20 text-red-400',
};

export default function DealsPage() {
    const [deals, setDeals] = useState<Deal[]>([]);
    const [pipeline, setPipeline] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [showCalc, setShowCalc] = useState(false);
    const [calcResult, setCalcResult] = useState<any>(null);
    const [form, setForm] = useState({ title: '', stage: 'lead', value: '', volume: '', unit_price: '', buy_price: '', sell_price: '', notes: '' });
    const [calcForm, setCalcForm] = useState({ buy_price: '', sell_price: '', volume: '' });
    const [saving, setSaving] = useState(false);

    const load = async () => {
        try {
            const [d, p] = await Promise.allSettled([
                api.get('/deals/'),
                api.get('/deals/pipeline/summary'),
            ]);
            if (d.status === 'fulfilled') setDeals(d.value);
            if (p.status === 'fulfilled') setPipeline(p.value);
        } catch {}
        setLoading(false);
    };

    useEffect(() => { load(); }, []);

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        try {
            await api.post('/deals/', {
                title: form.title,
                stage: form.stage,
                value: parseFloat(form.value) || 0,
                volume: parseFloat(form.volume) || 0,
                unit_price: parseFloat(form.unit_price) || 0,
                buy_price: form.buy_price ? parseFloat(form.buy_price) : null,
                sell_price: form.sell_price ? parseFloat(form.sell_price) : null,
                notes: form.notes || null,
            });
            setForm({ title: '', stage: 'lead', value: '', volume: '', unit_price: '', buy_price: '', sell_price: '', notes: '' });
            setShowForm(false);
            load();
        } catch {}
        setSaving(false);
    };

    const handleCalc = async () => {
        try {
            const res = await api.post(`/deals/calculate-margin?buy_price=${calcForm.buy_price}&sell_price=${calcForm.sell_price}&volume=${calcForm.volume}`);
            setCalcResult(res);
        } catch {}
    };

    const updateStage = async (id: string, stage: string) => {
        try {
            await api.put(`/deals/${id}`, { stage });
            load();
        } catch {}
    };

    const handleDelete = async (id: string) => {
        if (!confirm('Delete this deal?')) return;
        try { await api.delete(`/deals/${id}`); load(); } catch {}
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold">Deals & Negotiation</h1>
                    <p className="text-muted-foreground text-sm">{deals.length} deals in pipeline</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" onClick={() => setShowCalc(!showCalc)}>
                        <Calculator className="h-4 w-4 mr-2" /> Margin Calc
                    </Button>
                    <Button onClick={() => setShowForm(!showForm)}>
                        {showForm ? <X className="h-4 w-4 mr-2" /> : <Plus className="h-4 w-4 mr-2" />}
                        {showForm ? 'Cancel' : 'New Deal'}
                    </Button>
                </div>
            </div>

            {/* Pipeline Overview */}
            {pipeline && (
                <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
                    {Object.entries(pipeline).map(([stage, data]: [string, any]) => (
                        <Card key={stage} className="text-center">
                            <CardContent className="p-3">
                                <p className="text-xl font-bold">{data.count}</p>
                                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">{stage}</p>
                                <p className="text-xs text-primary">${data.total_value.toLocaleString()}</p>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}

            {/* Margin Calculator */}
            {showCalc && (
                <Card className="border-primary/30">
                    <CardHeader><CardTitle className="text-lg flex items-center gap-2"><Calculator className="h-5 w-5 text-primary" /> Margin Calculator</CardTitle></CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <Input placeholder="Buy Price" type="number" step="0.01" value={calcForm.buy_price} onChange={e => setCalcForm({...calcForm, buy_price: e.target.value})} />
                            <Input placeholder="Sell Price" type="number" step="0.01" value={calcForm.sell_price} onChange={e => setCalcForm({...calcForm, sell_price: e.target.value})} />
                            <Input placeholder="Volume" type="number" step="0.01" value={calcForm.volume} onChange={e => setCalcForm({...calcForm, volume: e.target.value})} />
                            <Button onClick={handleCalc}>Calculate</Button>
                        </div>
                        {calcResult && (
                            <div className="mt-4 p-4 bg-secondary/30 rounded-lg grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div><p className="text-xs text-muted-foreground">Margin %</p><p className="text-lg font-bold text-primary">{calcResult.margin_percent}%</p></div>
                                <div><p className="text-xs text-muted-foreground">Total Margin</p><p className="text-lg font-bold text-emerald-400">${calcResult.margin_total.toLocaleString()}</p></div>
                                <div className="md:col-span-2"><p className="text-xs text-muted-foreground">AI Recommendation</p><p className="text-sm mt-1">{calcResult.recommendation}</p></div>
                            </div>
                        )}
                    </CardContent>
                </Card>
            )}

            {/* New Deal Form */}
            {showForm && (
                <Card>
                    <CardHeader><CardTitle className="text-lg">New Deal</CardTitle></CardHeader>
                    <CardContent>
                        <form onSubmit={handleCreate} className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <Input placeholder="Deal Title *" value={form.title} onChange={e => setForm({...form, title: e.target.value})} required />
                            <select value={form.stage} onChange={e => setForm({...form, stage: e.target.value})} className="h-10 rounded-md border border-input bg-background px-3 text-sm">
                                {['lead','qualified','proposal','negotiation','won','lost'].map(s => <option key={s} value={s}>{s}</option>)}
                            </select>
                            <Input placeholder="Deal Value" type="number" step="0.01" value={form.value} onChange={e => setForm({...form, value: e.target.value})} />
                            <Input placeholder="Volume" type="number" step="0.01" value={form.volume} onChange={e => setForm({...form, volume: e.target.value})} />
                            <Input placeholder="Buy Price" type="number" step="0.01" value={form.buy_price} onChange={e => setForm({...form, buy_price: e.target.value})} />
                            <Input placeholder="Sell Price" type="number" step="0.01" value={form.sell_price} onChange={e => setForm({...form, sell_price: e.target.value})} />
                            <div className="md:col-span-3"><Input placeholder="Notes" value={form.notes} onChange={e => setForm({...form, notes: e.target.value})} /></div>
                            <div><Button type="submit" disabled={saving}>{saving ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}Create Deal</Button></div>
                        </form>
                    </CardContent>
                </Card>
            )}

            {/* Deals List */}
            {loading ? (
                <div className="flex justify-center py-12"><Loader2 className="h-6 w-6 animate-spin text-primary" /></div>
            ) : deals.length === 0 ? (
                <Card><CardContent className="py-12 text-center">
                    <Briefcase className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                    <h3 className="font-semibold text-lg">No deals yet</h3>
                    <p className="text-muted-foreground text-sm mt-1">Create your first deal to start tracking your pipeline</p>
                </CardContent></Card>
            ) : (
                <div className="space-y-3">
                    {deals.map(d => (
                        <Card key={d.id} className="hover:border-primary/30 transition-colors">
                            <CardContent className="p-4">
                                <div className="flex items-center justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-3">
                                            <h3 className="font-semibold">{d.title}</h3>
                                            <span className={`px-2 py-0.5 rounded text-xs font-medium capitalize ${stageColors[d.stage] || 'bg-secondary'}`}>{d.stage}</span>
                                            {d.margin_percent != null && (
                                                <span className={`text-xs font-mono ${d.margin_percent >= 10 ? 'text-emerald-400' : d.margin_percent >= 5 ? 'text-yellow-400' : 'text-red-400'}`}>
                                                    {d.margin_percent.toFixed(1)}% margin
                                                </span>
                                            )}
                                        </div>
                                        <div className="flex gap-4 mt-2 text-xs text-muted-foreground">
                                            <span>Value: ${d.value.toLocaleString()}</span>
                                            {d.buy_price && <span>Buy: ${d.buy_price}</span>}
                                            {d.sell_price && <span>Sell: ${d.sell_price}</span>}
                                            {d.volume > 0 && <span>Vol: {d.volume}</span>}
                                        </div>
                                        {d.notes && <p className="text-xs text-muted-foreground mt-1">{d.notes}</p>}
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <select value={d.stage} onChange={e => updateStage(d.id, e.target.value)}
                                            className="h-8 rounded border border-input bg-background px-2 text-xs">
                                            {['lead','qualified','proposal','negotiation','won','lost'].map(s => <option key={s} value={s}>{s}</option>)}
                                        </select>
                                        <button onClick={() => handleDelete(d.id)} className="text-muted-foreground hover:text-destructive"><Trash2 className="h-4 w-4" /></button>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
}
