import { Calendar as CalendarIcon } from 'lucide-react';

export default function CalendarPage() {
    return (
        <div className="p-8">
            <div className="flex items-center gap-4 mb-8">
                <div className="p-3 rounded-xl bg-accent/20 text-accent">
                    <CalendarIcon size={32} />
                </div>
                <div>
                    <h1 className="text-3xl font-bold text-white">Calendar & Scheduling</h1>
                    <p className="text-text-muted">Manage appointments and events</p>
                </div>
            </div>

            <div className="bg-card p-8 rounded-2xl border border-gray-800 text-center min-h-[400px] flex flex-col justify-center items-center">
                <p className="text-xl text-gray-400">Calendar Module Coming Soon</p>
            </div>
        </div>
    );
}
