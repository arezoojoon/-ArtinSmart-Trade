'use client';

import { useEffect, useState, useCallback } from 'react';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
    Loader2, Search, MapPin, Linkedin, Globe, Crosshair, Zap, Star, FileText,
    Users, Bell, Mail, Eye, Flame, CheckCircle, XCircle, Clock, BarChart3,
    ChevronDown, ChevronUp, ExternalLink, Shield,
} from 'lucide-react';

// ── Source definitions matching backend AVAILABLE_SOURCES ─────────
const SOURCES = [
    { id: 'maps_grid', name: 'Google Maps', desc: 'Local Distributors & Warehouses', icon: MapPin, color: 'text-red-400' },
    { id: 'linkedin_serp', name: 'LinkedIn (SERP)', desc: 'Profiles via Google Dorks', icon: Linkedin, color: 'text-blue-400' },
    { id: 'pdf_parser', name: 'TradeMap / PDFs', desc: 'Customs Manifests & Exhibitor Lists', icon: FileText, color: 'text-orange-400' },
    { id: 'competitor_audience', name: 'Competitor Audiences', desc: 'Facebook/Instagram Engagement', icon: Users, color: 'text-purple-400' },
    { id: 'technographic', name: 'Tech Stack Analysis', desc: 'Company Website Profiling', icon: Globe, color: 'text-cyan-400' },
    { id: 'review_mining', name: 'Review Mining', desc: 'Trustpilot/Google 1-2★ Reviews', icon: Star, color: 'text-yellow-400' },
    { id: 'intent_signals', name: 'Intent Signals', desc: 'Twitter/Reddit Buying Intent', icon: Zap, color: 'text-emerald-400' },
    { id: 'change_detection', name: 'Change Detection', desc: 'Job Changes & New Products', icon: Bell, color: 'text-pink-400' },
    { id: 'email_validator', name: 'Email Validation', desc: 'Permutation & SMTP Check', icon: Mail, color: 'text-teal-400' },
    { id: 'image_reverse_search', name: 'Image Search', desc: 'Reverse Image Supply Chain', icon: Eye, color: 'text-indigo-400' },
];

interface Lead {
    id: string;
    name: string;
    email: string | null;
    email_verified: boolean;
    phone: string | null;
    company: string | null;
    position: string | null;
    source: string;
    score: number;
    confidence: number;
    intent_score: number;
    lead_type: string;
    company_size: string | null;
    website: string | null;
    profile_url: string | null;
    tech_stack: string[];
    address: string | null;
    pain_points: string | null;
}

interface HunterStats {
    total_leads: number;
    hot_leads: number;
    warm_leads: number;
    cold_leads: number;
    verified_emails: number;
    total_jobs: number;
    by_source: Record<string, number>;
}

interface Job {
    job_id: string;
    status: string;
    query: string;
    location: string;
    sources: string[];
    results_count: number;
    created_at: string;
}

export default function HunterPage() {
    const [query, setQuery] = useState('');
    const [location, setLocation] = useState('');
    const [imageUrl, setImageUrl] = useState('');
    const [selectedSources, setSelectedSources] = useState<string[]>(['linkedin_serp', 'maps_grid']);
    const [running, setRunning] = useState(false);
    const [activeJob, setActiveJob] = useState<any>(null);
    const [leads, setLeads] = useState<Lead[]>([]);
    const [stats, setStats] = useState<HunterStats | null>(null);
    const [jobs, setJobs] = useState<Job[]>([]);
    const [loading, setLoading] = useState(true);
    const [filterSource, setFilterSource] = useState('');
    const [filterType, setFilterType] = useState('');
    const [showConfig, setShowConfig] = useState(true);
    const [expandedLead, setExpandedLead] = useState<string | null>(null);

    const loadData = useCallback(async () => {
        try {
            const [l, s, j] = await Promise.allSettled([
                api.get('/hunter/leads?limit=100'),
                api.get('/hunter/stats'),
                api.get('/hunter/jobs?limit=10'),
            ]);
            if (l.status === 'fulfilled') setLeads(l.value);
            if (s.status === 'fulfilled') setStats(s.value);
            if (j.status === 'fulfilled') setJobs(j.value);
        } catch {}
        setLoading(false);
    }, []);

    useEffect(() => { loadData(); }, [loadData]);

    const toggleSource = (id: string) => {
        setSelectedSources(prev => prev.includes(id) ? prev.filter(s => s !== id) : [...prev, id]);
    };

    const selectAll = () => setSelectedSources(SOURCES.map(s => s.id));
    const selectNone = () => setSelectedSources([]);

    const startHunt = async () => {
        if (!query.trim() || selectedSources.length === 0) return;
        setRunning(true);
        setActiveJob(null);
        try {
            const payload: any = {
                keywords: query,
                location: location || '',
                sources: selectedSources,
                max_results: 50,
            };
            if (imageUrl) payload.image_url = imageUrl;

            const res = await api.post('/hunter/start', payload);
            setActiveJob(res);

            // Poll for completion
            const pollInterval = setInterval(async () => {
                try {
                    const jobStatus = await api.get(`/hunter/jobs/${res.job_id}`);
                    setActiveJob(jobStatus);
                    if (jobStatus.status !== 'queued' && jobStatus.status !== 'running') {
                        clearInterval(pollInterval);
                        setRunning(false);
                        loadData();
                    }
                } catch {
                    clearInterval(pollInterval);
                    setRunning(false);
                }
            }, 5000);

            // Safety timeout
            setTimeout(() => { clearInterval(pollInterval); setRunning(false); loadData(); }, 300000);
        } catch {
            setRunning(false);
        }
    };

    const filteredLeads = leads.filter(l => {
        if (filterSource && l.source !== filterSource) return false;
        if (filterType && l.lead_type !== filterType) return false;
        return true;
    });

    const typeColor = (type: string) => {
        if (type === 'hot') return 'bg-red-500/20 text-red-400 border-red-500/30';
        if (type === 'warm') return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
        return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
    };

    const scoreColor = (score: number) => {
        if (score >= 80) return 'text-emerald-400';
        if (score >= 50) return 'text-yellow-400';
        return 'text-muted-foreground';
    };

    const statusIcon = (status: string) => {
        if (status === 'completed') return <CheckCircle className="h-4 w-4 text-emerald-400" />;
        if (status === 'failed') return <XCircle className="h-4 w-4 text-red-400" />;
        if (status === 'running') return <Loader2 className="h-4 w-4 animate-spin text-primary" />;
        return <Clock className="h-4 w-4 text-muted-foreground" />;
    };

    if (loading) {
        return <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>;
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold flex items-center gap-2">
                        <Crosshair className="h-7 w-7 text-primary" /> Hunter — Lead Generation Engine
                    </h1>
                    <p className="text-muted-foreground text-sm">10-source OSINT & growth hacking lead discovery</p>
                </div>
                <Button variant="outline" size="sm" onClick={() => setShowConfig(!showConfig)}>
                    {showConfig ? <ChevronUp className="h-4 w-4 mr-1" /> : <ChevronDown className="h-4 w-4 mr-1" />}
                    {showConfig ? 'Hide Config' : 'Show Config'}
                </Button>
            </div>

            {/* Stats Bar */}
            {stats && (
                <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
                    {[
                        { label: 'Total Leads', value: stats.total_leads, icon: Users },
                        { label: 'Hot', value: stats.hot_leads, icon: Flame },
                        { label: 'Warm', value: stats.warm_leads, icon: Zap },
                        { label: 'Cold', value: stats.cold_leads, icon: Search },
                        { label: 'Verified Emails', value: stats.verified_emails, icon: CheckCircle },
                        { label: 'Jobs Run', value: stats.total_jobs, icon: BarChart3 },
                    ].map(s => (
                        <Card key={s.label}>
                            <CardContent className="p-3 text-center">
                                <s.icon className="h-4 w-4 mx-auto text-primary mb-1" />
                                <p className="text-xl font-bold">{s.value}</p>
                                <p className="text-[10px] text-muted-foreground">{s.label}</p>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}

            {/* Hunt Configuration */}
            {showConfig && (
                <Card className="border-primary/20">
                    <CardHeader className="pb-3">
                        <CardTitle className="text-lg">Configure Hunt</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div>
                                <label className="text-sm font-medium mb-1 block">Keywords</label>
                                <Input placeholder="e.g. Sugar, FMCG distributors..." value={query} onChange={e => setQuery(e.target.value)} />
                            </div>
                            <div>
                                <label className="text-sm font-medium mb-1 block">Location</label>
                                <Input placeholder="e.g. Dubai, UAE..." value={location} onChange={e => setLocation(e.target.value)} />
                            </div>
                            <div>
                                <label className="text-sm font-medium mb-1 block">Image URL (optional)</label>
                                <Input placeholder="https://example.com/product.jpg" value={imageUrl} onChange={e => setImageUrl(e.target.value)} />
                            </div>
                        </div>

                        {/* Source Selection Panel */}
                        <div>
                            <div className="flex items-center justify-between mb-2">
                                <label className="text-sm font-medium">Select Data Sources ({selectedSources.length}/10)</label>
                                <div className="flex gap-2">
                                    <button onClick={selectAll} className="text-xs text-primary hover:underline">Select All</button>
                                    <button onClick={selectNone} className="text-xs text-muted-foreground hover:underline">Clear</button>
                                </div>
                            </div>
                            <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                                {SOURCES.map(s => (
                                    <button key={s.id} onClick={() => toggleSource(s.id)}
                                        className={`p-2.5 rounded-lg border text-left transition-all ${
                                            selectedSources.includes(s.id)
                                                ? 'border-primary bg-primary/10 ring-1 ring-primary/30'
                                                : 'border-border bg-card hover:border-primary/20'
                                        }`}>
                                        <div className="flex items-center gap-1.5 mb-0.5">
                                            <s.icon className={`h-3.5 w-3.5 ${selectedSources.includes(s.id) ? s.color : 'text-muted-foreground'}`} />
                                            <span className="text-xs font-medium truncate">{s.name}</span>
                                        </div>
                                        <p className="text-[9px] text-muted-foreground leading-tight">{s.desc}</p>
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className="flex items-center gap-3">
                            <Button onClick={startHunt} disabled={running || !query.trim() || selectedSources.length === 0}>
                                {running ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : <Crosshair className="h-4 w-4 mr-2" />}
                                {running ? 'Hunting...' : 'Start Hunt'}
                            </Button>
                            <span className="text-xs text-muted-foreground">
                                Est. time: ~{selectedSources.length * 3}min for {selectedSources.length} sources
                            </span>
                        </div>

                        {activeJob && (
                            <div className="p-3 bg-primary/10 border border-primary/20 rounded-lg text-sm flex items-center gap-3">
                                {statusIcon(activeJob.status)}
                                <span>Job <span className="font-mono text-primary">{activeJob.job_id?.slice(0, 8)}...</span></span>
                                <Badge variant="outline">{activeJob.status}</Badge>
                                {activeJob.results_count > 0 && <span className="text-muted-foreground">{activeJob.results_count} leads found</span>}
                                {activeJob.estimated_time && <span className="text-muted-foreground">~{activeJob.estimated_time}</span>}
                            </div>
                        )}
                    </CardContent>
                </Card>
            )}

            {/* Recent Jobs */}
            {jobs.length > 0 && (
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">Recent Jobs</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex gap-2 overflow-x-auto pb-1">
                            {jobs.slice(0, 5).map(j => (
                                <div key={j.job_id} className="flex-shrink-0 p-2 rounded-lg border border-border bg-card text-xs min-w-[180px]">
                                    <div className="flex items-center gap-1.5 mb-1">
                                        {statusIcon(j.status)}
                                        <span className="font-medium truncate">{j.query}</span>
                                    </div>
                                    <div className="text-muted-foreground">
                                        {j.location} · {j.results_count} leads · {j.sources.length} sources
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Leads Results */}
            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between flex-wrap gap-2">
                        <CardTitle className="text-lg">Discovered Leads ({filteredLeads.length})</CardTitle>
                        <div className="flex gap-2">
                            <select value={filterSource} onChange={e => setFilterSource(e.target.value)}
                                className="h-8 rounded border border-input bg-background px-2 text-xs">
                                <option value="">All Sources</option>
                                {SOURCES.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                            </select>
                            <select value={filterType} onChange={e => setFilterType(e.target.value)}
                                className="h-8 rounded border border-input bg-background px-2 text-xs">
                                <option value="">All Types</option>
                                <option value="hot">🔥 Hot</option>
                                <option value="warm">⚡ Warm</option>
                                <option value="cold">❄️ Cold</option>
                            </select>
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    {filteredLeads.length === 0 ? (
                        <div className="text-center py-12">
                            <Search className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                            <h3 className="font-semibold text-lg">No leads yet</h3>
                            <p className="text-muted-foreground text-sm mt-1">Configure your search above and start hunting</p>
                        </div>
                    ) : (
                        <div className="space-y-2 max-h-[600px] overflow-y-auto">
                            {filteredLeads.map(lead => (
                                <div key={lead.id} className="rounded-lg border border-border hover:border-primary/30 transition-colors">
                                    <div className="p-3 flex items-center justify-between cursor-pointer" onClick={() => setExpandedLead(expandedLead === lead.id ? null : lead.id)}>
                                        <div className="flex items-center gap-3 min-w-0">
                                            <div className="w-9 h-9 rounded-full bg-primary/20 flex items-center justify-center text-primary text-sm font-bold flex-shrink-0">
                                                {(lead.name || '?')[0].toUpperCase()}
                                            </div>
                                            <div className="min-w-0">
                                                <div className="flex items-center gap-2">
                                                    <p className="text-sm font-medium truncate">{lead.name}</p>
                                                    {lead.email_verified && <CheckCircle className="h-3 w-3 text-emerald-400 flex-shrink-0" />}
                                                </div>
                                                <div className="flex gap-2 text-xs text-muted-foreground flex-wrap">
                                                    {lead.company && <span>{lead.company}</span>}
                                                    {lead.position && <span>· {lead.position}</span>}
                                                    {lead.email && <span>· {lead.email}</span>}
                                                </div>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-2 flex-shrink-0">
                                            <Badge className={`text-[10px] border ${typeColor(lead.lead_type)}`}>{lead.lead_type}</Badge>
                                            <Badge variant="outline" className="text-[10px]">{lead.source?.replace('_', ' ')}</Badge>
                                            <span className={`text-sm font-bold ${scoreColor(lead.score)}`}>{lead.score}</span>
                                            {lead.intent_score > 0 && (
                                                <span className="text-[10px] text-yellow-400 font-medium">⚡{Math.round(lead.intent_score)}</span>
                                            )}
                                        </div>
                                    </div>

                                    {/* Expanded Details */}
                                    {expandedLead === lead.id && (
                                        <div className="px-3 pb-3 pt-1 border-t border-border/50 text-xs space-y-2">
                                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                                {lead.phone && <div><span className="text-muted-foreground">Phone:</span> {lead.phone}</div>}
                                                {lead.address && <div><span className="text-muted-foreground">Address:</span> {lead.address}</div>}
                                                {lead.company_size && <div><span className="text-muted-foreground">Size:</span> <Badge variant="outline" className="text-[9px]">{lead.company_size}</Badge></div>}
                                                <div><span className="text-muted-foreground">Confidence:</span> <span className={scoreColor(lead.confidence)}>{lead.confidence?.toFixed(0)}%</span></div>
                                            </div>
                                            {lead.tech_stack && lead.tech_stack.length > 0 && (
                                                <div className="flex items-center gap-1 flex-wrap">
                                                    <span className="text-muted-foreground">Tech:</span>
                                                    {lead.tech_stack.map(t => <Badge key={t} variant="outline" className="text-[9px]">{t}</Badge>)}
                                                </div>
                                            )}
                                            {lead.pain_points && (
                                                <div><span className="text-muted-foreground">Pain Points:</span> <span className="text-red-400">{lead.pain_points}</span></div>
                                            )}
                                            <div className="flex gap-2 pt-1">
                                                {lead.website && (
                                                    <a href={lead.website} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline flex items-center gap-1">
                                                        <Globe className="h-3 w-3" /> Website <ExternalLink className="h-2.5 w-2.5" />
                                                    </a>
                                                )}
                                                {lead.profile_url && (
                                                    <a href={lead.profile_url} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline flex items-center gap-1">
                                                        <Linkedin className="h-3 w-3" /> Profile <ExternalLink className="h-2.5 w-2.5" />
                                                    </a>
                                                )}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
