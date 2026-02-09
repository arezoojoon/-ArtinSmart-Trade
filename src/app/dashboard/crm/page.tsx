'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Plus, Loader2, X, Users, Star, Trash2, Search, Zap } from 'lucide-react';

interface Contact {
    id: string;
    type: string;
    company_name: string | null;
    contact_person: string | null;
    email: string | null;
    phone: string | null;
    score: number;
    created_at: string | null;
}

export default function CRMPage() {
    const [contacts, setContacts] = useState<Contact[]>([]);
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [search, setSearch] = useState('');
    const [filter, setFilter] = useState('');
    const [form, setForm] = useState({ type: 'buyer', company_name: '', contact_person: '', email: '', phone: '' });
    const [saving, setSaving] = useState(false);

    const load = async () => {
        try {
            const [c, s] = await Promise.allSettled([
                api.get('/crm/contacts'),
                api.get('/crm/dashboard/stats'),
            ]);
            if (c.status === 'fulfilled') setContacts(c.value);
            if (s.status === 'fulfilled') setStats(s.value);
        } catch {}
        setLoading(false);
    };

    useEffect(() => { load(); }, []);

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        try {
            await api.post('/crm/contacts', form);
            setForm({ type: 'buyer', company_name: '', contact_person: '', email: '', phone: '' });
            setShowForm(false);
            load();
        } catch {}
        setSaving(false);
    };

    const handleDelete = async (id: string) => {
        if (!confirm('Delete this contact?')) return;
        try { await api.delete(`/crm/contacts/${id}`); load(); } catch {}
    };

    const handleScore = async (id: string) => {
        try {
            const res = await api.post(`/crm/contacts/${id}/score`);
            alert(`Score: ${res.score}\n\nReasons:\n${res.reasons.join('\n')}`);
            load();
        } catch {}
    };

    const filtered = contacts.filter(c => {
        const matchesSearch = !search || 
            (c.company_name || '').toLowerCase().includes(search.toLowerCase()) ||
            (c.contact_person || '').toLowerCase().includes(search.toLowerCase()) ||
            (c.email || '').toLowerCase().includes(search.toLowerCase());
        const matchesFilter = !filter || c.type === filter;
        return matchesSearch && matchesFilter;
    });

    const scoreColor = (score: number) => {
        if (score >= 70) return 'text-emerald-400';
        if (score >= 40) return 'text-yellow-400';
        return 'text-muted-foreground';
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold">CRM</h1>
                    <p className="text-muted-foreground text-sm">Manage buyers, sellers, and business contacts</p>
                </div>
                <Button onClick={() => setShowForm(!showForm)}>
                    {showForm ? <X className="h-4 w-4 mr-2" /> : <Plus className="h-4 w-4 mr-2" />}
                    {showForm ? 'Cancel' : 'Add Contact'}
                </Button>
            </div>

            {/* Stats */}
            {stats && (
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    <Card><CardContent className="p-4"><p className="text-2xl font-bold">{stats.total_contacts}</p><p className="text-xs text-muted-foreground">Total Contacts</p></CardContent></Card>
                    <Card><CardContent className="p-4"><p className="text-2xl font-bold text-blue-400">{stats.buyers}</p><p className="text-xs text-muted-foreground">Buyers</p></CardContent></Card>
                    <Card><CardContent className="p-4"><p className="text-2xl font-bold text-emerald-400">{stats.sellers}</p><p className="text-xs text-muted-foreground">Sellers</p></CardContent></Card>
                    <Card><CardContent className="p-4"><p className="text-2xl font-bold text-primary">{stats.avg_score}</p><p className="text-xs text-muted-foreground">Avg Score</p></CardContent></Card>
                    <Card><CardContent className="p-4"><p className="text-2xl font-bold text-yellow-400">{stats.high_score_leads}</p><p className="text-xs text-muted-foreground">Hot Leads (70+)</p></CardContent></Card>
                </div>
            )}

            {showForm && (
                <Card>
                    <CardHeader><CardTitle className="text-lg">New Contact</CardTitle></CardHeader>
                    <CardContent>
                        <form onSubmit={handleCreate} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <select value={form.type} onChange={e => setForm({...form, type: e.target.value})} className="h-10 rounded-md border border-input bg-background px-3 text-sm">
                                <option value="buyer">Buyer</option>
                                <option value="seller">Seller</option>
                                <option value="supplier">Supplier</option>
                                <option value="partner">Partner</option>
                                <option value="other">Other</option>
                            </select>
                            <Input placeholder="Company Name" value={form.company_name} onChange={e => setForm({...form, company_name: e.target.value})} />
                            <Input placeholder="Contact Person" value={form.contact_person} onChange={e => setForm({...form, contact_person: e.target.value})} />
                            <Input placeholder="Email" type="email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} />
                            <Input placeholder="Phone" value={form.phone} onChange={e => setForm({...form, phone: e.target.value})} />
                            <div><Button type="submit" disabled={saving}>{saving ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}Add Contact</Button></div>
                        </form>
                    </CardContent>
                </Card>
            )}

            {/* Search & Filter */}
            <div className="flex gap-3 flex-wrap">
                <div className="relative flex-1 min-w-[200px]">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input placeholder="Search contacts..." className="pl-10" value={search} onChange={e => setSearch(e.target.value)} />
                </div>
                <div className="flex gap-2">
                    {['', 'buyer', 'seller', 'supplier'].map(f => (
                        <button key={f} onClick={() => setFilter(f)}
                            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${filter === f ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'}`}>
                            {f || 'All'}
                        </button>
                    ))}
                </div>
            </div>

            {/* Contacts List */}
            {loading ? (
                <div className="flex justify-center py-12"><Loader2 className="h-6 w-6 animate-spin text-primary" /></div>
            ) : filtered.length === 0 ? (
                <Card><CardContent className="py-12 text-center">
                    <Users className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                    <h3 className="font-semibold text-lg">No contacts found</h3>
                    <p className="text-muted-foreground text-sm mt-1">Add contacts or use the Hunter to find new leads</p>
                </CardContent></Card>
            ) : (
                <div className="space-y-3">
                    {filtered.map(c => (
                        <Card key={c.id} className="hover:border-primary/30 transition-colors">
                            <CardContent className="p-4 flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
                                        {(c.contact_person || c.company_name || '?')[0].toUpperCase()}
                                    </div>
                                    <div>
                                        <div className="flex items-center gap-2">
                                            <h3 className="font-semibold text-sm">{c.contact_person || c.company_name || 'Unknown'}</h3>
                                            <Badge variant="secondary" className="capitalize text-[10px]">{c.type}</Badge>
                                        </div>
                                        <div className="flex gap-3 text-xs text-muted-foreground mt-1">
                                            {c.company_name && <span>{c.company_name}</span>}
                                            {c.email && <span>{c.email}</span>}
                                            {c.phone && <span>{c.phone}</span>}
                                        </div>
                                    </div>
                                </div>
                                <div className="flex items-center gap-3">
                                    <div className="text-center">
                                        <p className={`text-lg font-bold ${scoreColor(c.score)}`}>{c.score}</p>
                                        <p className="text-[10px] text-muted-foreground">Score</p>
                                    </div>
                                    <button onClick={() => handleScore(c.id)} className="p-2 hover:bg-primary/10 rounded-lg transition-colors" title="AI Score">
                                        <Zap className="h-4 w-4 text-primary" />
                                    </button>
                                    <button onClick={() => handleDelete(c.id)} className="p-2 hover:bg-destructive/10 rounded-lg transition-colors">
                                        <Trash2 className="h-4 w-4 text-muted-foreground hover:text-destructive" />
                                    </button>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
}
