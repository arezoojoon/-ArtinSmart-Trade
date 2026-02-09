'use client';

import Link from 'next/link';
import {
    Plus,
    Search,
    Filter,
    MoreHorizontal,
    Phone,
    Mail,
    MessageSquare
} from 'lucide-react';

export default function LeadsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white">My Leads</h1>
                    <p className="text-text-muted">Manage your relationships and follow-ups</p>
                </div>
                <Link href="/leads/hunter" className="btn-primary bg-accent hover:bg-accent-hover text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2">
                    <Plus size={18} /> Add New Lead
                </Link>
            </div>

            <div className="bg-card rounded-2xl border border-gray-800 overflow-hidden">
                {/* Toolbar */}
                <div className="p-4 border-b border-gray-800 flex gap-4">
                    <div className="relative flex-1">
                        <Search className="absolute left-3 top-2.5 text-text-muted" size={18} />
                        <input
                            type="text"
                            placeholder="Search leads..."
                            className="w-full bg-background/50 border border-gray-800 rounded-lg pl-10 pr-4 py-2 focus:border-accent outline-none"
                        />
                    </div>
                    <button className="px-4 py-2 border border-gray-800 rounded-lg flex items-center gap-2 hover:bg-background">
                        <Filter size={18} /> Filter
                    </button>
                </div>

                {/* Table */}
                <table className="w-full text-left">
                    <thead className="bg-background/50 text-text-muted text-sm border-b border-gray-800">
                        <tr>
                            <th className="px-6 py-3 font-medium">Name / Company</th>
                            <th className="px-6 py-3 font-medium">Contact</th>
                            <th className="px-6 py-3 font-medium">Status</th>
                            <th className="px-6 py-3 font-medium">Stage</th>
                            <th className="px-6 py-3 font-medium text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-800">
                        {[1, 2, 3, 4, 5, 6].map((i) => (
                            <tr key={i} className="hover:bg-gray-800/30 transition-colors">
                                <td className="px-6 py-4">
                                    <div className="font-medium text-white">Sarah Jenkins</div>
                                    <div className="text-sm text-text-muted">Purchasing Mgr, Grand Hotel</div>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex gap-2">
                                        <button className="p-1.5 bg-background rounded hover:text-accent"><MessageSquare size={16} /></button>
                                        <button className="p-1.5 bg-background rounded hover:text-accent"><Phone size={16} /></button>
                                        <button className="p-1.5 bg-background rounded hover:text-accent"><Mail size={16} /></button>
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-900/30 text-yellow-500">
                                        Warm
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-sm">
                                    Negotiation
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <button className="text-text-muted hover:text-white">
                                        <MoreHorizontal size={20} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
