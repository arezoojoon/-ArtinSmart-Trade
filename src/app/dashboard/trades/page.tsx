'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Plus, Loader2, X, ArrowUpDown } from 'lucide-react';

interface Trade {
    id: string;
    product_id: string;
    volume: number;
    price: number;
    status: string;
    buyer_name: string | null;
    seller_name: string | null;
    created_at: string | null;
}

const statusColors: Record<string, string> = {
    pending: 'bg-yellow-500/20 text-yellow-400',
    confirmed: 'bg-blue-500/20 text-blue-400',
    completed: 'bg-emerald-500/20 text-emerald-400',
    cancelled: 'bg-red-500/20 text-red-400',
    disputed: 'bg-orange-500/20 text-orange-400',
};

export default function TradesPage() {
    const [trades, setTrades] = useState<Trade[]>([]);
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [form, setForm] = useState({ product_id: '', volume: '', price: '', buyer_name: '', seller_name: '' });
    const [saving, setSaving] = useState(false);
    const [filter, setFilter] = useState('');

    const load = async () => {
        try {
            const [t, s] = await Promise.allSettled([
                api.get('/trades/'),
                api.get('/trades/summary/stats'),
            ]);
            if (t.status === 'fulfilled') setTrades(t.value);
            if (s.status === 'fulfilled') setStats(s.value);
        } catch {}
        setLoading(false);
    };

    useEffect(() => { load(); }, []);

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        try {
            await api.post('/trades/', {
                product_id: form.product_id,
                volume: parseFloat(form.volume),
                price: parseFloat(form.price),
                buyer_name: form.buyer_name || null,
                seller_name: form.seller_name || null,
            });
            setForm({ product_id: '', volume: '', price: '', buyer_name: '', seller_name: '' });
            setShowForm(false);
            load();
        } catch {}
        setSaving(false);
    };

    const filtered = filter ? trades.filter(t => t.status === filter) : trades;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold">Trades</h1>
                    <p className="text-muted-foreground text-sm">{trades.length} total trades</p>
                </div>
                <Button onClick={() => setShowForm(!showForm)}>
                    {showForm ? <X className="h-4 w-4 mr-2" /> : <Plus className="h-4 w-4 mr-2" />}
                    {showForm ? 'Cancel' : 'New Trade'}
                </Button>
            </div>

            {/* Stats */}
            {stats && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <Card><CardContent className="p-4"><p className="text-2xl font-bold">{stats.total_trades}</p><p className="text-xs text-muted-foreground">Total Trades</p></CardContent></Card>
                    <Card><CardContent className="p-4"><p className="text-2xl font-bold">{stats.total_volume?.toLocaleString()}</p><p className="text-xs text-muted-foreground">Total Volume</p></CardContent></Card>
                    <Card><CardContent className="p-4"><p className="text-2xl font-bold text-primary">${stats.total_value?.toLocaleString()}</p><p className="text-xs text-muted-foreground">Total Value</p></CardContent></Card>
                    <Card><CardContent className="p-4"><p className="text-2xl font-bold text-emerald-400">{stats.by_status?.completed || 0}</p><p className="text-xs text-muted-foreground">Completed</p></CardContent></Card>
                </div>
            )}

            {showForm && (
                <Card>
                    <CardHeader><CardTitle className="text-lg">New Trade</CardTitle></CardHeader>
                    <CardContent>
                        <form onSubmit={handleCreate} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <Input placeholder="Product ID *" value={form.product_id} onChange={e => setForm({...form, product_id: e.target.value})} required />
                            <Input placeholder="Volume *" type="number" step="0.01" value={form.volume} onChange={e => setForm({...form, volume: e.target.value})} required />
                            <Input placeholder="Price *" type="number" step="0.01" value={form.price} onChange={e => setForm({...form, price: e.target.value})} required />
                            <Input placeholder="Buyer Name" value={form.buyer_name} onChange={e => setForm({...form, buyer_name: e.target.value})} />
                            <Input placeholder="Seller Name" value={form.seller_name} onChange={e => setForm({...form, seller_name: e.target.value})} />
                            <div>
                                <Button type="submit" disabled={saving}>
                                    {saving ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                                    Create Trade
                                </Button>
                            </div>
                        </form>
                    </CardContent>
                </Card>
            )}

            {/* Filter */}
            <div className="flex gap-2 flex-wrap">
                {['', 'pending', 'confirmed', 'completed', 'cancelled'].map(s => (
                    <button key={s} onClick={() => setFilter(s)}
                        className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${filter === s ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'}`}>
                        {s || 'All'}
                    </button>
                ))}
            </div>

            {loading ? (
                <div className="flex justify-center py-12"><Loader2 className="h-6 w-6 animate-spin text-primary" /></div>
            ) : filtered.length === 0 ? (
                <Card><CardContent className="py-12 text-center">
                    <ArrowUpDown className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                    <h3 className="font-semibold text-lg">No trades found</h3>
                    <p className="text-muted-foreground text-sm mt-1">Create your first trade to get started</p>
                </CardContent></Card>
            ) : (
                <div className="space-y-3">
                    {filtered.map(t => (
                        <Card key={t.id} className="hover:border-primary/30 transition-colors">
                            <CardContent className="p-4 flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div>
                                        <p className="font-medium text-sm">Vol: {t.volume?.toLocaleString()} @ ${t.price}</p>
                                        <p className="text-xs text-muted-foreground">Value: ${((t.volume || 0) * (t.price || 0)).toLocaleString()}</p>
                                        {t.buyer_name && <p className="text-xs text-muted-foreground">Buyer: {t.buyer_name}</p>}
                                    </div>
                                </div>
                                <div className="flex items-center gap-3">
                                    <span className={`px-2 py-1 rounded text-xs font-medium capitalize ${statusColors[t.status] || 'bg-secondary'}`}>
                                        {t.status}
                                    </span>
                                    {t.created_at && <span className="text-xs text-muted-foreground">{new Date(t.created_at).toLocaleDateString()}</span>}
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
}
