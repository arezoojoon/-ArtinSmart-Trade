'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Plus, Search, Package, Loader2, Trash2, X } from 'lucide-react';

interface Product {
    id: string;
    name: string;
    category: string | null;
    industry: string | null;
    unit: string | null;
    description: string | null;
}

export default function ProductsPage() {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [search, setSearch] = useState('');
    const [form, setForm] = useState({ name: '', category: '', industry: '', unit: '', description: '' });
    const [saving, setSaving] = useState(false);

    const load = async () => {
        try {
            const data = await api.get('/products/');
            setProducts(data);
        } catch {}
        setLoading(false);
    };

    useEffect(() => { load(); }, []);

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        try {
            await api.post('/products/', form);
            setForm({ name: '', category: '', industry: '', unit: '', description: '' });
            setShowForm(false);
            load();
        } catch {}
        setSaving(false);
    };

    const handleDelete = async (id: string) => {
        if (!confirm('Delete this product?')) return;
        try {
            await api.delete(`/products/${id}`);
            load();
        } catch {}
    };

    const filtered = products.filter(p =>
        p.name.toLowerCase().includes(search.toLowerCase()) ||
        (p.category || '').toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold">Products</h1>
                    <p className="text-muted-foreground text-sm">{products.length} products in your catalog</p>
                </div>
                <Button onClick={() => setShowForm(!showForm)}>
                    {showForm ? <X className="h-4 w-4 mr-2" /> : <Plus className="h-4 w-4 mr-2" />}
                    {showForm ? 'Cancel' : 'Add Product'}
                </Button>
            </div>

            {showForm && (
                <Card>
                    <CardHeader><CardTitle className="text-lg">New Product</CardTitle></CardHeader>
                    <CardContent>
                        <form onSubmit={handleCreate} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <Input placeholder="Product Name *" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required />
                            <Input placeholder="Category (e.g. FMCG, Commodity)" value={form.category} onChange={e => setForm({...form, category: e.target.value})} />
                            <Input placeholder="Industry" value={form.industry} onChange={e => setForm({...form, industry: e.target.value})} />
                            <Input placeholder="Unit (kg, MT, pcs)" value={form.unit} onChange={e => setForm({...form, unit: e.target.value})} />
                            <div className="md:col-span-2">
                                <Input placeholder="Description" value={form.description} onChange={e => setForm({...form, description: e.target.value})} />
                            </div>
                            <div className="md:col-span-2">
                                <Button type="submit" disabled={saving}>
                                    {saving ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                                    Create Product
                                </Button>
                            </div>
                        </form>
                    </CardContent>
                </Card>
            )}

            <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input placeholder="Search products..." className="pl-10" value={search} onChange={e => setSearch(e.target.value)} />
            </div>

            {loading ? (
                <div className="flex justify-center py-12"><Loader2 className="h-6 w-6 animate-spin text-primary" /></div>
            ) : filtered.length === 0 ? (
                <Card>
                    <CardContent className="py-12 text-center">
                        <Package className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                        <h3 className="font-semibold text-lg">No products found</h3>
                        <p className="text-muted-foreground text-sm mt-1">Add your first product to get started</p>
                    </CardContent>
                </Card>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {filtered.map(p => (
                        <Card key={p.id} className="hover:border-primary/30 transition-colors">
                            <CardContent className="p-4">
                                <div className="flex items-start justify-between">
                                    <div>
                                        <h3 className="font-semibold">{p.name}</h3>
                                        <div className="flex gap-2 mt-2">
                                            {p.category && <Badge variant="secondary">{p.category}</Badge>}
                                            {p.industry && <Badge variant="outline">{p.industry}</Badge>}
                                        </div>
                                        {p.unit && <p className="text-xs text-muted-foreground mt-2">Unit: {p.unit}</p>}
                                        {p.description && <p className="text-xs text-muted-foreground mt-1">{p.description}</p>}
                                    </div>
                                    <button onClick={() => handleDelete(p.id)} className="text-muted-foreground hover:text-destructive transition-colors">
                                        <Trash2 className="h-4 w-4" />
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
