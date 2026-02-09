'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Loader2, Shield, Users, ShoppingBag, BarChart3, Briefcase, Search, Globe, Ban, Check } from 'lucide-react';

export default function AdminPage() {
    const { user } = useAuth();
    const [dashboard, setDashboard] = useState<any>(null);
    const [users, setUsers] = useState<any[]>([]);
    const [auditLogs, setAuditLogs] = useState<any[]>([]);
    const [superStats, setSuperStats] = useState<any>(null);
    const [tenants, setTenants] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [tab, setTab] = useState<'overview' | 'users' | 'audit' | 'tenants'>('overview');

    const isSuperAdmin = user?.role === 'super_admin';

    useEffect(() => {
        async function load() {
            try {
                const [d, u, a] = await Promise.allSettled([
                    api.get('/admin/dashboard'),
                    api.get('/admin/users'),
                    api.get('/admin/audit-logs?limit=50'),
                ]);
                if (d.status === 'fulfilled') setDashboard(d.value);
                if (u.status === 'fulfilled') setUsers(u.value);
                if (a.status === 'fulfilled') setAuditLogs(a.value);

                if (isSuperAdmin) {
                    const [ss, t] = await Promise.allSettled([
                        api.get('/admin/super/stats'),
                        api.get('/admin/super/tenants'),
                    ]);
                    if (ss.status === 'fulfilled') setSuperStats(ss.value);
                    if (t.status === 'fulfilled') setTenants(t.value);
                }
            } catch {}
            setLoading(false);
        }
        load();
    }, [isSuperAdmin]);

    const updateRole = async (userId: string, role: string) => {
        try {
            await api.put(`/admin/users/${userId}/role?role=${role}`);
            const u = await api.get('/admin/users');
            setUsers(u);
        } catch {}
    };

    const toggleActive = async (userId: string) => {
        try {
            await api.put(`/admin/users/${userId}/toggle-active`);
            const u = await api.get('/admin/users');
            setUsers(u);
        } catch {}
    };

    const suspendTenant = async (tenantId: string) => {
        try {
            await api.put(`/admin/super/tenants/${tenantId}/suspend`);
            const t = await api.get('/admin/super/tenants');
            setTenants(t);
        } catch {}
    };

    const activateTenant = async (tenantId: string) => {
        try {
            await api.put(`/admin/super/tenants/${tenantId}/activate`);
            const t = await api.get('/admin/super/tenants');
            setTenants(t);
        } catch {}
    };

    if (loading) {
        return <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>;
    }

    const tabs = [
        { id: 'overview' as const, label: 'Overview' },
        { id: 'users' as const, label: 'Users' },
        { id: 'audit' as const, label: 'Audit Logs' },
        ...(isSuperAdmin ? [{ id: 'tenants' as const, label: 'Tenants (Super)' }] : []),
    ];

    return (
        <div className="space-y-6">
            <div className="flex items-center gap-3">
                <Shield className="h-7 w-7 text-primary" />
                <div>
                    <h1 className="text-2xl font-bold">Admin Panel</h1>
                    <p className="text-muted-foreground text-sm">
                        {isSuperAdmin ? 'Super Admin — Full platform control' : 'Tenant administration'}
                    </p>
                </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 border-b border-border pb-2">
                {tabs.map(t => (
                    <button key={t.id} onClick={() => setTab(t.id)}
                        className={`px-4 py-2 rounded-t-lg text-sm font-medium transition-colors ${
                            tab === t.id ? 'bg-primary text-primary-foreground' : 'text-muted-foreground hover:text-foreground hover:bg-secondary/50'
                        }`}>
                        {t.label}
                    </button>
                ))}
            </div>

            {/* Overview Tab */}
            {tab === 'overview' && (
                <div className="space-y-6">
                    {dashboard && (
                        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                            {[
                                { label: 'Users', value: dashboard.total_users, icon: Users },
                                { label: 'Products', value: dashboard.total_products, icon: ShoppingBag },
                                { label: 'Trades', value: dashboard.total_trades, icon: BarChart3 },
                                { label: 'Deals', value: dashboard.total_deals, icon: Briefcase },
                                { label: 'Contacts', value: dashboard.total_contacts, icon: Users },
                                { label: 'Leads', value: dashboard.total_leads, icon: Search },
                            ].map(s => (
                                <Card key={s.label}>
                                    <CardContent className="p-4 text-center">
                                        <s.icon className="h-5 w-5 mx-auto text-primary mb-2" />
                                        <p className="text-2xl font-bold">{s.value}</p>
                                        <p className="text-xs text-muted-foreground">{s.label}</p>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    )}

                    {/* Super Admin Global Stats */}
                    {isSuperAdmin && superStats && (
                        <Card className="border-primary/30">
                            <CardHeader><CardTitle className="text-lg flex items-center gap-2"><Globe className="h-5 w-5 text-primary" /> Global Platform Stats</CardTitle></CardHeader>
                            <CardContent>
                                <div className="grid grid-cols-3 md:grid-cols-5 gap-4">
                                    {Object.entries(superStats).map(([key, val]) => (
                                        <div key={key} className="text-center">
                                            <p className="text-xl font-bold text-primary">{val as number}</p>
                                            <p className="text-[10px] text-muted-foreground uppercase tracking-wider">{key.replace(/_/g, ' ')}</p>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    )}
                </div>
            )}

            {/* Users Tab */}
            {tab === 'users' && (
                <div className="space-y-3">
                    {users.map(u => (
                        <Card key={u.id} className="hover:border-primary/30 transition-colors">
                            <CardContent className="p-4 flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <div className="w-9 h-9 rounded-full bg-primary/20 flex items-center justify-center text-primary text-sm font-bold">
                                        {(u.full_name || u.email || '?')[0].toUpperCase()}
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium">{u.full_name || u.email}</p>
                                        <p className="text-xs text-muted-foreground">{u.email}</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-3">
                                    <select value={u.role} onChange={e => updateRole(u.id, e.target.value)}
                                        className="h-8 rounded border border-input bg-background px-2 text-xs">
                                        {['buyer', 'seller', 'both', 'admin'].map(r => <option key={r} value={r}>{r}</option>)}
                                    </select>
                                    <Badge variant={u.is_active ? 'success' : 'destructive'}>
                                        {u.is_active ? 'Active' : 'Inactive'}
                                    </Badge>
                                    <Button size="sm" variant={u.is_active ? 'destructive' : 'default'} onClick={() => toggleActive(u.id)}>
                                        {u.is_active ? <Ban className="h-3 w-3" /> : <Check className="h-3 w-3" />}
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                    {users.length === 0 && <p className="text-muted-foreground text-center py-8">No users found</p>}
                </div>
            )}

            {/* Audit Logs Tab */}
            {tab === 'audit' && (
                <div className="space-y-2 max-h-[600px] overflow-y-auto">
                    {auditLogs.map(log => (
                        <div key={log.id} className="p-3 rounded-lg border border-border flex items-center justify-between text-sm">
                            <div>
                                <span className="font-medium">{log.action}</span>
                                {log.entity && <span className="text-muted-foreground ml-2">({log.entity})</span>}
                                {log.details && <p className="text-xs text-muted-foreground mt-1">{log.details}</p>}
                            </div>
                            <span className="text-xs text-muted-foreground whitespace-nowrap">{log.timestamp}</span>
                        </div>
                    ))}
                    {auditLogs.length === 0 && <p className="text-muted-foreground text-center py-8">No audit logs yet</p>}
                </div>
            )}

            {/* Tenants Tab (Super Admin Only) */}
            {tab === 'tenants' && isSuperAdmin && (
                <div className="space-y-3">
                    {tenants.map(t => (
                        <Card key={t.id} className="hover:border-primary/30 transition-colors">
                            <CardContent className="p-4 flex items-center justify-between">
                                <div>
                                    <h3 className="font-semibold">{t.name}</h3>
                                    <div className="flex gap-3 text-xs text-muted-foreground mt-1">
                                        <span>{t.user_count} users</span>
                                        <span>Plan: {t.plan}</span>
                                        <span>Created: {t.created_at}</span>
                                    </div>
                                </div>
                                <div className="flex items-center gap-3">
                                    <Badge variant={t.status === 'active' ? 'success' : 'destructive'}>{t.status}</Badge>
                                    {t.status === 'active' ? (
                                        <Button size="sm" variant="destructive" onClick={() => suspendTenant(t.id)}>Suspend</Button>
                                    ) : (
                                        <Button size="sm" onClick={() => activateTenant(t.id)}>Activate</Button>
                                    )}
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                    {tenants.length === 0 && <p className="text-muted-foreground text-center py-8">No tenants found</p>}
                </div>
            )}
        </div>
    );
}
