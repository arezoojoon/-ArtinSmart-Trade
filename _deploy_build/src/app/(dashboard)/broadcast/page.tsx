'use client';

import { useState } from 'react';
import { Megaphone, Users, FileText, Send, AlertCircle, CheckCircle } from 'lucide-react';

export default function BroadcastPage() {
    const [segment, setSegment] = useState('gulfood');
    const [template, setTemplate] = useState('followup');
    const [sending, setSending] = useState(false);
    const [sent, setSent] = useState(false);

    const segments = {
        'all': { name: 'All Leads', count: 1245 },
        'gulfood': { name: 'Gulfood 2026', count: 500 },
        'vip': { name: 'VIP Distributors', count: 50 }
    };

    const templates = {
        'followup': "Hi {{name}}, it was great meeting you at Gulfood. Here is our catalog...",
        'promo': "Exclusive Offer: Get 10% off on bulk Nutella orders this week!",
        'restock': "Alert: New stock of Ferrero Rocher just arrived. Book now."
    };

    const costPerMsg = 0.05;
    // @ts-ignore
    const totalCost = (segments[segment].count * costPerMsg).toFixed(2);

    const handleSend = () => {
        setSending(true);
        setTimeout(() => {
            setSending(false);
            setSent(true);
        }, 2000);
    };

    if (sent) {
        return (
            <div className="h-[calc(100vh-6rem)] flex flex-col items-center justify-center text-center space-y-6">
                <div className="w-24 h-24 bg-emerald-500/10 rounded-full flex items-center justify-center text-emerald-500 animate-in zoom-in duration-300">
                    <CheckCircle size={48} />
                </div>
                <div>
                    <h2 className="text-3xl font-bold text-white">Campaign Sent!</h2>
                    {/* @ts-ignore */}
                    <p className="text-text-muted mt-2">Successfully broadcasted to {segments[segment].count} recipients.</p>
                </div>
                <button onClick={() => setSent(false)} className="btn-secondary px-6 py-2 rounded-lg bg-card border border-gray-700 hover:bg-gray-800">
                    Start New Campaign
                </button>
            </div>
        );
    }

    return (
        <div className="max-w-5xl mx-auto p-4 space-y-8">
            <div className="flex items-center gap-4">
                <div className="p-3 rounded-xl bg-accent/20 text-accent">
                    <Megaphone size={32} />
                </div>
                <div>
                    <h1 className="text-3xl font-bold text-white">Smart Broadcast</h1>
                    <p className="text-text-muted">AI-Powered Mass Messaging Campaigns</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Configuration Panel */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Segment Selector */}
                    <div className="bg-card p-6 rounded-2xl border border-gray-800">
                        <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
                            <Users size={20} className="text-blue-500" /> Target Audience
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {Object.entries(segments).map(([key, data]) => (
                                <div
                                    key={key}
                                    onClick={() => setSegment(key)}
                                    className={`p-4 rounded-xl border cursor-pointer transition ${segment === key ? 'bg-blue-500/10 border-blue-500 text-blue-400' : 'bg-background border-gray-800 hover:border-gray-600'}`}
                                >
                                    <div className="font-bold mb-1">{data.name}</div>
                                    <div className="text-sm opacity-70">{data.count} Leads</div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Template Selector */}
                    <div className="bg-card p-6 rounded-2xl border border-gray-800">
                        <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
                            <FileText size={20} className="text-purple-500" /> Message Content
                        </h3>
                        <div className="space-y-4">
                            <label className="text-sm text-text-muted">Select Template</label>
                            <div className="flex gap-2 overflow-x-auto pb-2">
                                {Object.keys(templates).map(key => (
                                    <button
                                        key={key}
                                        onClick={() => setTemplate(key)}
                                        className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap border transition ${template === key ? 'bg-purple-500/10 border-purple-500 text-purple-400' : 'bg-background border-gray-800 hover:border-gray-600'}`}
                                    >
                                        {key.charAt(0).toUpperCase() + key.slice(1)}
                                    </button>
                                ))}
                            </div>

                            <div className="relative">
                                {/* @ts-ignore */}
                                <textarea
                                    className="w-full h-32 bg-background border border-gray-800 rounded-xl p-4 focus:border-accent outline-none font-mono text-sm leading-relaxed"
                                    // @ts-ignore
                                    value={templates[template]}
                                    readOnly
                                />
                                <div className="absolute bottom-3 right-3 text-xs text-text-muted bg-card px-2 py-1 rounded border border-gray-800">
                                    AI Optimized
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Summary & Send */}
                <div className="space-y-6">
                    <div className="bg-card p-6 rounded-2xl border border-gray-800">
                        <h3 className="font-bold text-lg mb-6">Campaign Summary</h3>

                        <div className="space-y-4 mb-8">
                            <div className="flex justify-between text-sm">
                                <span className="text-text-muted">Target Segment</span>
                                {/* @ts-ignore */}
                                <span className="font-medium">{segments[segment].name}</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-text-muted">Recipients</span>
                                {/* @ts-ignore */}
                                <span className="font-medium">{segments[segment].count}</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-text-muted">Cost per msg</span>
                                <span className="font-medium">${costPerMsg}</span>
                            </div>
                            <div className="h-px bg-gray-800 my-4"></div>
                            <div className="flex justify-between text-lg font-bold">
                                <span>Total Cost</span>
                                <span className="text-accent">${totalCost}</span>
                            </div>
                        </div>

                        <div className="bg-amber-500/10 border border-amber-500/20 p-4 rounded-xl mb-6">
                            <div className="flex gap-2 items-start">
                                <AlertCircle size={16} className="text-amber-500 mt-0.5" />
                                <p className="text-xs text-amber-500/90 leading-relaxed">
                                    Credits will be deducted immediately. Ensure your wallet balance (${(Number(totalCost) + 100).toFixed(2)}) is sufficient.
                                </p>
                            </div>
                        </div>

                        <button
                            onClick={handleSend}
                            disabled={sending}
                            className="w-full btn-primary bg-emerald-600 hover:bg-emerald-700 text-white py-4 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {sending ? 'Broadcasting...' : (
                                <>
                                    <Send size={20} /> Launch Campaign
                                </>
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
