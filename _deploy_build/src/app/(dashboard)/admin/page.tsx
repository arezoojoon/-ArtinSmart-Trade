import { Activity, Database, Server, Users, Zap } from "lucide-react";

export default function AdminOverview() {
    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold mb-2">System Overview</h1>
                    <p className="text-gray-400">Real-time platform metrics and status.</p>
                </div>
                <div className="flex items-center gap-2 px-3 py-1 bg-green-500/10 border border-green-500/20 rounded-full text-green-500 text-sm font-mono animate-pulse">
                    <div className="w-2 h-2 bg-green-500 rounded-full" />
                    ALL SYSTEMS OPERATIONAL
                </div>
            </div>

            {/* KPI Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <KPIItem title="Active Tenants" value="12" icon={Database} trend="+2 this week" color="blue" />
                <KPIItem title="Total Users" value="1,248" icon={Users} trend="+18% growth" color="purple" />
                <KPIItem title="AI Requests (24h)" value="45.2k" icon={Zap} trend="Gemini 1.5 Pro" color="amber" />
                <KPIItem title="Server Load" value="24%" icon={Server} trend="Healthy" color="green" />
            </div>

            {/* Recent Activity Log Mockup */}
            <div className="bg-zinc-900/50 border border-white/5 rounded-2xl p-6">
                <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                    <Activity size={20} className="text-gray-400" />
                    System Events
                </h2>
                <div className="space-y-0">
                    {[1, 2, 3, 4, 5].map((i) => (
                        <div key={i} className="flex items-center justify-between py-4 border-b border-white/5 last:border-0 hover:bg-white/5 px-4 -mx-4 transition-colors">
                            <div className="flex items-center gap-4">
                                <div className="px-2 py-1 bg-blue-500/10 text-blue-500 text-xs font-mono rounded border border-blue-500/20">INFO</div>
                                <span className="text-sm text-gray-300">Tenant #04 triggered a bulk scrape of Google Maps.</span>
                            </div>
                            <span className="text-xs text-gray-500 font-mono">10:4{i} AM</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

function KPIItem({ title, value, icon: Icon, trend, color }: any) {
    const colorClasses: Record<string, string> = {
        blue: "text-blue-500 bg-blue-500/10 border-blue-500/20",
        purple: "text-purple-500 bg-purple-500/10 border-purple-500/20",
        amber: "text-amber-500 bg-amber-500/10 border-amber-500/20",
        green: "text-green-500 bg-green-500/10 border-green-500/20",
    };

    const style = colorClasses[color] || colorClasses.blue;

    return (
        <div className="bg-zinc-900/50 border border-white/5 p-6 rounded-2xl hover:bg-zinc-900 transition duration-300">
            <div className="flex justify-between items-start mb-4">
                <div className={`p-3 rounded-xl ${style.split(' ').slice(1).join(' ')}`}>
                    <Icon className={style.split(' ')[0]} size={24} />
                </div>
                <span className={`text-xs px-2 py-1 rounded-full ${style}`}>
                    {trend}
                </span>
            </div>
            <h3 className="text-3xl font-bold text-white mb-1">{value}</h3>
            <p className="text-gray-500 text-sm">{title}</p>
        </div>
    )
}
