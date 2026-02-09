import { PhoneCall } from 'lucide-react';

export default function FollowUpPage() {
    return (
        <div className="p-8">
            <div className="flex items-center gap-4 mb-8">
                <div className="p-3 rounded-xl bg-accent/20 text-accent">
                    <PhoneCall size={32} />
                </div>
                <div>
                    <h1 className="text-3xl font-bold text-white">Follow-up Engine</h1>
                    <p className="text-text-muted">Automated lead nurturing and callback scheduling</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* Placeholder Content */}
                <div className="bg-card p-6 rounded-2xl border border-gray-800">
                    <h3 className="text-xl font-bold mb-4 text-white">Pending Calls</h3>
                    <p className="text-gray-400">No pending calls for today.</p>
                </div>
            </div>
        </div>
    );
}
