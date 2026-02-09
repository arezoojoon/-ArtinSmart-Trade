'use client';

import { useState } from 'react';
import { Search, MapPin, Globe, Loader2, Database, Download } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function LeadHunterPage() {
    const [query, setQuery] = useState('');
    const [isSearching, setIsSearching] = useState(false);
    const [results, setResults] = useState<any[]>([]);
    const [error, setError] = useState<string | null>(null);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        setIsSearching(true);
        setError(null);
        setResults([]);

        try {
            const res = await fetch('/api/hunter', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, source: 'google_maps' })
            });

            const data = await res.json();

            if (data.success) {
                setResults(data.data);
            } else {
                setError(data.error || "Search failed");
            }

        } catch (err) {
            setError("Failed to connect to Hunter Engine.");
        } finally {
            setIsSearching(false);
        }
    };

    return (
        <div className="space-y-6 max-w-5xl mx-auto p-4 md:p-8">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold flex items-center gap-2">
                        <Search className="text-accent" /> Lead Hunter
                    </h1>
                    <p className="text-text-muted mt-1">A.I. Powered Lead Scraper (Google Maps & Directories)</p>
                </div>
                <div className="flex items-center gap-2 text-xs font-mono bg-zinc-900 border border-zinc-800 px-3 py-1 rounded-full">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                    ENGINE ONLINE
                </div>
            </div>

            {/* Search Bar */}
            <div className="bg-card border border-gray-800 p-6 rounded-2xl shadow-lg">
                <form onSubmit={handleSearch} className="flex gap-4">
                    <div className="relative flex-1">
                        <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" />
                        <input
                            type="text"
                            placeholder="e.g. 'FMCG Distributors in Dubai' or 'Supermarkets in Riyadh'"
                            className="w-full bg-black/50 border border-gray-700 rounded-xl py-4 pl-12 pr-4 text-lg focus:outline-none focus:border-accent transition-all"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            disabled={isSearching}
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={isSearching}
                        className="bg-accent hover:bg-accent-hover text-white px-8 rounded-xl font-bold text-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                        {isSearching ? <Loader2 className="animate-spin" /> : <Search />}
                        <span>Hunt</span>
                    </button>
                </form>
            </div>

            {/* Error Message */}
            {error && (
                <div className="p-4 bg-red-900/20 border border-red-900/50 text-red-400 rounded-xl flex items-center gap-2">
                    <Database size={18} /> {error}
                </div>
            )}

            {/* Results Grid */}
            {results.length > 0 && (
                <div className="space-y-4">
                    <div className="flex items-center justify-between">
                        <h2 className="text-xl font-bold">{results.length} Leads Found</h2>
                        <button className="flex items-center gap-2 text-sm text-accent hover:text-white transition-colors">
                            <Download size={16} /> Export to CSV
                        </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {results.map((lead, idx) => (
                            <div key={idx} className="bg-card border border-gray-800 p-5 rounded-xl hover:border-accent/40 transition-colors animate-in fade-in slide-in-from-bottom-4 duration-500" style={{ animationDelay: `${idx * 50}ms` }}>
                                <div className="flex items-start justify-between mb-3">
                                    <h3 className="font-bold text-lg line-clamp-1" title={lead.name}>{lead.name}</h3>
                                    <span className="text-xs bg-gray-800 text-gray-400 px-2 py-1 rounded">
                                        {lead.source.split(' ')[0]}
                                    </span>
                                </div>

                                <div className="space-y-2 text-sm text-gray-300">
                                    {lead.address && (
                                        <div className="flex items-start gap-2">
                                            <MapPin size={14} className="mt-1 text-gray-500 shrink-0" />
                                            <span className="line-clamp-2">{lead.address}</span>
                                        </div>
                                    )}
                                    {lead.website && (
                                        <div className="flex items-center gap-2">
                                            <Globe size={14} className="text-gray-500 shrink-0" />
                                            <a href={lead.website} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline truncate">
                                                {lead.website.replace('https://', '')}
                                            </a>
                                        </div>
                                    )}
                                </div>

                                <button className="w-full mt-4 py-2 bg-gray-800 hover:bg-gray-700 text-white text-sm font-medium rounded-lg transition-colors">
                                    Add to CRM
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Empty State */}
            {!isSearching && results.length === 0 && !error && (
                <div className="text-center py-20 opacity-30">
                    <Search size={64} className="mx-auto mb-4" />
                    <p className="text-xl">Enter a keyword to start hunting</p>
                </div>
            )}
        </div>
    );
}
