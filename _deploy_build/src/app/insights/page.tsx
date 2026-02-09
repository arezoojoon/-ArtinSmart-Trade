import { TrendingUp } from 'lucide-react';

export default function InsightsPage() {
    return (
        <div className="p-8">
            <div className="flex items-center gap-4 mb-8">
                <div className="p-3 rounded-xl bg-accent/20 text-accent">
                    <TrendingUp size={32} />
                </div>
                <div>
                    <h1 className="text-3xl font-bold text-white">Market Insights</h1>
                    <p className="text-text-muted">AI-driven market trends and analysis</p>
                </div>
            </div>

            <div className="bg-card p-6 rounded-2xl border border-gray-800">
                <h2 className="text-xl font-semibold text-white mb-4">Competitor Analysis</h2>
                <div className="h-64 bg-gray-900/50 rounded-xl flex items-center justify-center text-gray-500">
                    Chart Placeholder
                </div>
            </div>
        </div>
    );
}
