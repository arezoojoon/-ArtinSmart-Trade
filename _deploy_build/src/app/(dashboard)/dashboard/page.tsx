import Link from "next/link";
import {
    DollarSign,
    Users,
    TrendingUp,
    Wallet,
    ArrowRight,
    Search,
    MessageSquare
} from "lucide-react";

export default function Dashboard() {
    return (
        <div className="space-y-8 px-4 md:px-8">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-white">Dashboard</h1>
                    <p className="text-text-muted">Welcome back, Admin</p>
                </div>
                <div className="flex gap-3">
                    <Link href="/wallet" className="btn-secondary flex items-center gap-2 px-4 py-2 bg-card rounded-lg hover:bg-gray-800 transition">
                        <Wallet size={18} className="text-accent" />
                        <span>500 Credits</span>
                    </Link>
                    <button className="btn-primary px-4 py-2 bg-accent text-white rounded-lg hover:bg-accent-hover transition font-medium">
                        + New Campaign
                    </button>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Potential Revenue"
                    value="$124,500"
                    trend="Pipeline Value"
                    icon={DollarSign}
                    color="text-emerald-500"
                />
                <StatCard
                    title="Hot Leads (AI)"
                    value="42"
                    trend="High Priority"
                    icon={TrendingUp}
                    color="text-amber-500"
                />
                <StatCard
                    title="Wallet Balance"
                    value="$450.00"
                    trend="Credits Available"
                    icon={Wallet}
                    color="text-blue-500"
                />
                <StatCard
                    title="AI Engine"
                    value="Online"
                    trend="99.9% Uptime"
                    icon={Users}
                    color="text-purple-500"
                />
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gradient-to-br from-indigo-900/50 to-bg-card p-6 rounded-2xl border border-indigo-500/20 relative overflow-hidden group">
                    <div className="relative z-10">
                        <h3 className="text-xl font-bold mb-2">Lead Hunter</h3>
                        <p className="text-text-muted mb-6">Find new B2B leads from Google & Directories.</p>
                        <Link href="/leads/hunter" className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-lg transition font-medium">
                            <Search size={18} /> Start Scraping
                        </Link>
                    </div>
                    <Search className="absolute -bottom-4 -right-4 w-32 h-32 text-indigo-500/10 group-hover:scale-110 transition-transform" />
                </div>

                <div className="bg-gradient-to-br from-emerald-900/50 to-bg-card p-6 rounded-2xl border border-emerald-500/20 relative overflow-hidden group">
                    <div className="relative z-10">
                        <h3 className="text-xl font-bold mb-2">Smart Broadcast</h3>
                        <p className="text-text-muted mb-6">Send AI-personalized campaigns to your leads.</p>
                        <Link href="/broadcast" className="inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-lg transition font-medium">
                            <MessageSquare size={18} /> New Broadcast
                        </Link>
                    </div>
                    <MessageSquare className="absolute -bottom-4 -right-4 w-32 h-32 text-emerald-500/10 group-hover:scale-110 transition-transform" />
                </div>
            </div>

            {/* Recent Activity / Pipeline Preview */}
            <div className="bg-card rounded-2xl p-6 border border-gray-800">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-bold">Recent Leads</h2>
                    <Link href="/leads" className="text-accent hover:underline text-sm flex items-center gap-1">
                        View All <ArrowRight size={14} />
                    </Link>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="border-b border-gray-800 text-text-muted text-sm">
                                <th className="pb-3 pl-2">Name</th>
                                <th className="pb-3">Company</th>
                                <th className="pb-3">Status</th>
                                <th className="pb-3">Source</th>
                                <th className="pb-3">Confidence</th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            {[1, 2, 3, 4, 5].map((i) => (
                                <tr key={i} className="border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors">
                                    <td className="py-4 pl-2 font-medium">Ahmed Al-Mansoori</td>
                                    <td className="py-4 text-text-muted">Al Maya Group</td>
                                    <td className="py-4">
                                        <span className="bg-emerald-500/10 text-emerald-500 px-2 py-1 rounded-full text-xs">New Lead</span>
                                    </td>
                                    <td className="py-4 text-text-muted">Gulfood 2026</td>
                                    <td className="py-4">
                                        <div className="flex items-center gap-2">
                                            <div className="w-16 h-1.5 bg-gray-700 rounded-full overflow-hidden">
                                                <div className="h-full bg-accent" style={{ width: '85%' }}></div>
                                            </div>
                                            <span className="text-xs">85%</span>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

function StatCard({ title, value, trend, icon: Icon, color }: any) {
    return (
        <div className="bg-card p-6 rounded-2xl border border-gray-800 hover:border-accent/30 transition shadow-lg">
            <div className="flex items-start justify-between">
                <div>
                    <p className="text-text-muted text-sm font-medium">{title}</p>
                    <h3 className="text-2xl font-bold mt-2 text-white">{value}</h3>
                </div>
                <div className={`p-3 rounded-xl bg-opacity-10 ${color.replace('text-', 'bg-')}`}>
                    <Icon className={color} size={24} />
                </div>
            </div>
            <div className="mt-4 flex items-center gap-2 text-sm">
                <span className="text-emerald-500 bg-emerald-500/10 px-1.5 py-0.5 rounded flex items-center">
                    {trend}
                </span>
                <span className="text-text-muted">vs last month</span>
            </div>
        </div>
    );
}
