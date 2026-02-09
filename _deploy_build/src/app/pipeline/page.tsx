'use client';

import { useState } from 'react';
import { Columns, GripVertical, Plus, MoreVertical } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Lead {
    id: number;
    name: string;
    company: string;
    value: string;
}

const mockLeads: Record<string, Lead[]> = {
    'new': [
        { id: 1, name: "Ali Hassan", company: "Carrefour UAE", value: "$50k" },
        { id: 2, name: "John Doe", company: "Spinneys", value: "$12k" },
    ],
    'contacted': [
        { id: 3, name: "Sarah Smith", company: "Waitrose", value: "$25k" },
    ],
    'proposal': [
        { id: 4, name: "Mohammed Zaid", company: "Lulu Hypermarket", value: "$120k" },
    ],
    'negotiation': [],
    'closed': [
        { id: 5, name: "Rami K", company: "Union Coop", value: "$15k" },
    ]
};

const columns = [
    { id: 'new', title: 'New Leads', color: 'border-blue-500' },
    { id: 'contacted', title: 'Contacted', color: 'border-yellow-500' },
    { id: 'proposal', title: 'Proposal Sent', color: 'border-purple-500' },
    { id: 'negotiation', title: 'Negotiation', color: 'border-orange-500' },
    { id: 'closed', title: 'Closed Won', color: 'border-emerald-500' },
];

export default function PipelinePage() {
    const [leads, setLeads] = useState(mockLeads);
    const [draggedLead, setDraggedLead] = useState<{ id: number, sourceCol: string } | null>(null);

    const handleDragStart = (e: React.DragEvent, leadId: number, colId: string) => {
        setDraggedLead({ id: leadId, sourceCol: colId });
        e.dataTransfer.effectAllowed = "move";
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
    };

    const handleDrop = (e: React.DragEvent, targetColId: string) => {
        e.preventDefault();
        if (!draggedLead) return;
        if (draggedLead.sourceCol === targetColId) return;

        const sourceList = [...leads[draggedLead.sourceCol]];
        const targetList = [...leads[targetColId]];

        const leadIndex = sourceList.findIndex(l => l.id === draggedLead.id);
        if (leadIndex === -1) return;

        const [movedLead] = sourceList.splice(leadIndex, 1);
        targetList.push(movedLead);

        setLeads({
            ...leads,
            [draggedLead.sourceCol]: sourceList,
            [targetColId]: targetList
        });
        setDraggedLead(null);
    };

    return (
        <div className="p-8 h-[calc(100vh-2rem)] flex flex-col">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-white">Sales Pipeline</h1>
                <button className="btn-primary bg-accent hover:bg-accent-hover text-white px-4 py-2 rounded-lg font-bold flex items-center gap-2">
                    <Plus size={18} /> Add Deal
                </button>
            </div>

            <div className="flex-1 overflow-x-auto">
                <div className="flex gap-4 min-w-[1200px] h-full">
                    {columns.map(col => (
                        <div
                            key={col.id}
                            className="flex-1 min-w-[250px] bg-card rounded-xl border border-gray-800 flex flex-col"
                            onDragOver={handleDragOver}
                            onDrop={(e) => handleDrop(e, col.id)}
                        >
                            {/* Column Header */}
                            <div className={`p-4 border-b border-gray-800 border-t-4 ${col.color} rounded-t-xl bg-gray-900/50`}>
                                <div className="flex justify-between items-center">
                                    <h3 className="font-bold text-white">{col.title}</h3>
                                    <span className="bg-gray-800 text-text-muted text-xs px-2 py-1 rounded-full">
                                        {leads[col.id].length}
                                    </span>
                                </div>
                            </div>

                            {/* Drop Zone */}
                            <div className="flex-1 p-3 space-y-3 overflow-y-auto bg-gray-900/20">
                                {leads[col.id].map(lead => (
                                    <div
                                        key={lead.id}
                                        draggable
                                        onDragStart={(e) => handleDragStart(e, lead.id, col.id)}
                                        className="bg-card border border-gray-700 p-4 rounded-lg shadow-sm hover:shadow-md cursor-grab active:cursor-grabbing hover:border-accent transition group"
                                    >
                                        <div className="flex justify-between items-start mb-2">
                                            <span className="text-sm font-bold text-white">{lead.company}</span>
                                            <button className="text-gray-600 hover:text-white opacity-0 group-hover:opacity-100 transition"><MoreVertical size={14} /></button>
                                        </div>
                                        <p className="text-sm text-text-muted mb-3">{lead.name}</p>
                                        <div className="flex justify-between items-center">
                                            <span className="bg-emerald-500/10 text-emerald-500 text-xs font-mono font-bold px-2 py-1 rounded">
                                                {lead.value}
                                            </span>
                                            <div className="w-6 h-6 rounded-full bg-gray-700 flex items-center justify-center text-[10px] text-white">
                                                {lead.name.charAt(0)}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                                {leads[col.id].length === 0 && (
                                    <div className="h-full flex items-center justify-center border-2 border-dashed border-gray-800 rounded-lg m-2">
                                        <p className="text-xs text-text-muted">Drop here</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
