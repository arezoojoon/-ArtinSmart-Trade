import { BookOpen } from 'lucide-react';

export default function KnowledgePage() {
    return (
        <div className="p-8">
            <div className="flex items-center gap-4 mb-8">
                <div className="p-3 rounded-xl bg-accent/20 text-accent">
                    <BookOpen size={32} />
                </div>
                <div>
                    <h1 className="text-3xl font-bold text-white">Knowledge Base</h1>
                    <p className="text-text-muted">Training resources and documentation</p>
                </div>
            </div>
            <div className="bg-card p-8 rounded-2xl border border-gray-800 text-center">
                <p className="text-xl text-gray-400">Knowledge Repository</p>
            </div>
        </div>
    );
}
