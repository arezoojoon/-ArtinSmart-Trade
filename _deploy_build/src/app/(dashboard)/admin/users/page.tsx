import { MoreVertical, Shield, User, Search, Filter } from "lucide-react";

export default function UserManagement() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold">User Management</h1>
                <button className="bg-white text-black px-4 py-2 rounded-lg font-bold hover:bg-gray-200 transition">
                    + Add New User
                </button>
            </div>

            {/* Filters & Search */}
            <div className="flex items-center gap-4 bg-zinc-900/50 p-4 rounded-xl border border-white/5">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
                    <input
                        type="text"
                        placeholder="Search users by name, email, or tenant..."
                        className="w-full bg-black/50 border border-white/10 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-red-500 transition-colors"
                    />
                </div>
                <button className="flex items-center gap-2 px-4 py-2 bg-black/50 border border-white/10 rounded-lg text-sm text-gray-400 hover:text-white transition">
                    <Filter size={16} /> Filters
                </button>
            </div>

            {/* Users Table */}
            <div className="bg-zinc-900/50 border border-white/5 rounded-2xl overflow-hidden">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-white/5 border-b border-white/5 text-gray-400 text-sm">
                            <th className="p-4 font-medium">User</th>
                            <th className="p-4 font-medium">Role</th>
                            <th className="p-4 font-medium">Status</th>
                            <th className="p-4 font-medium">Last Active</th>
                            <th className="p-4 font-medium text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                        {[1, 2, 3, 4, 5].map((i) => (
                            <tr key={i} className="hover:bg-white/5 transition-colors group">
                                <td className="p-4">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 bg-gradient-to-br from-gray-700 to-gray-900 rounded-full flex items-center justify-center text-gray-300">
                                            <User size={18} />
                                        </div>
                                        <div>
                                            <p className="font-bold text-white">Alex Johnson</p>
                                            <p className="text-xs text-gray-500">alex@example.com</p>
                                        </div>
                                    </div>
                                </td>
                                <td className="p-4">
                                    <div className="flex items-center gap-2">
                                        <Shield size={14} className="text-blue-500" />
                                        <span className="text-sm">Admin</span>
                                    </div>
                                </td>
                                <td className="p-4">
                                    <span className="px-2 py-1 bg-green-500/10 text-green-500 text-xs rounded border border-green-500/20">Active</span>
                                </td>
                                <td className="p-4 text-sm text-gray-500">
                                    2 hours ago
                                </td>
                                <td className="p-4 text-right">
                                    <button className="p-2 hover:bg-white/10 rounded-lg transition-colors text-gray-500 hover:text-white">
                                        <MoreVertical size={18} />
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
