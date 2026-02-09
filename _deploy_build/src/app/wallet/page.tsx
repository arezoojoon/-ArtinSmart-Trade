'use client';

import { useState } from 'react';
import {
    Wallet,
    CreditCard,
    History,
    TrendingUp,
    TrendingDown,
    Plus,
    CheckCircle,
    AlertCircle
} from 'lucide-react';
import { cn } from '@/lib/utils';

export default function WalletPage() {
    const [balance, setBalance] = useState(500);
    const [showTopUp, setShowTopUp] = useState(false);
    const [amount, setAmount] = useState(100);

    const transactions = [
        { id: 1, type: 'debit', amount: 50, desc: 'WhatsApp Broadcast (500 recipients)', date: 'Today, 10:30 AM' },
        { id: 2, type: 'credit', amount: 200, desc: 'Wallet Top-up (Stripe)', date: 'Yesterday' },
        { id: 3, type: 'debit', amount: 25, desc: 'Lead Scraper Job (UAE)', date: 'Feb 4, 2026' },
        { id: 4, type: 'debit', amount: 10, desc: 'AI Analysis Credits', date: 'Feb 3, 2026' },
    ];

    const handleTopUp = () => {
        // Simulate Stripe payment
        setTimeout(() => {
            setBalance(prev => prev + Number(amount));
            setShowTopUp(false);
            alert(`Successfully added $${amount} to your wallet!`);
        }, 1000);
    };

    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold text-white">Billing & Wallet</h1>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Balance Card */}
                <div className="bg-gradient-to-br from-accent/20 to-bg-card border border-accent/30 p-8 rounded-2xl flex flex-col justify-between relative overflow-hidden">
                    <div className="relative z-10">
                        <p className="text-accent font-medium mb-1 flex items-center gap-2"><Wallet size={20} /> Current Balance</p>
                        <h2 className="text-5xl font-bold text-white">${balance.toFixed(2)}</h2>
                        <p className="text-text-muted mt-2 text-sm">Credits available for AI & Messaging</p>

                        <button
                            onClick={() => setShowTopUp(true)}
                            className="mt-6 bg-accent hover:bg-accent-hover text-white px-6 py-3 rounded-lg font-bold w-full transition flex items-center justify-center gap-2"
                        >
                            <Plus size={20} /> Top Up Wallet
                        </button>
                    </div>
                    <Wallet className="absolute -bottom-8 -right-8 w-64 h-64 text-accent/5 opacity-50 rotate-12" />
                </div>

                {/* Stats */}
                <div className="md:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="bg-card p-6 rounded-2xl border border-gray-800">
                        <div className="flex items-start justify-between">
                            <div>
                                <p className="text-text-muted text-sm">Monthly Spend</p>
                                <h3 className="text-2xl font-bold text-white mt-1">$1,245.00</h3>
                            </div>
                            <div className="p-2 bg-red-500/10 rounded-lg text-red-500">
                                <TrendingDown size={24} />
                            </div>
                        </div>
                        <div className="mt-4 text-sm text-text-muted">
                            High usage in <strong>WhatsApp Broadcasts</strong>
                        </div>
                    </div>
                    <div className="bg-card p-6 rounded-2xl border border-gray-800">
                        <div className="flex items-start justify-between">
                            <div>
                                <p className="text-text-muted text-sm">Estimated Run-out</p>
                                <h3 className="text-2xl font-bold text-white mt-1">14 Days</h3>
                            </div>
                            <div className="p-2 bg-blue-500/10 rounded-lg text-blue-500">
                                <History size={24} />
                            </div>
                        </div>
                        <div className="mt-4 text-sm text-text-muted">
                            Based on average daily usage of $35
                        </div>
                    </div>
                </div>

                {/* Unit Costs / Estimator */}
                <div className="bg-card p-6 rounded-2xl border border-gray-800 md:col-span-3">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <AlertCircle size={18} className="text-accent" /> Cost Estimator
                    </h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="p-3 bg-background rounded-lg border border-gray-800">
                            <p className="text-xs text-text-muted">Lead Scraper</p>
                            <p className="font-mono text-white">$0.50 <span className="text-[10px] text-gray-500">/ lead</span></p>
                        </div>
                        <div className="p-3 bg-background rounded-lg border border-gray-800">
                            <p className="text-xs text-text-muted">WhatsApp Broadcast</p>
                            <p className="font-mono text-white">$0.05 <span className="text-[10px] text-gray-500">/ msg</span></p>
                        </div>
                        <div className="p-3 bg-background rounded-lg border border-gray-800">
                            <p className="text-xs text-text-muted">AI Auto-Reply</p>
                            <p className="font-mono text-white">$0.02 <span className="text-[10px] text-gray-500">/ reply</span></p>
                        </div>
                        <div className="p-3 bg-background rounded-lg border border-gray-800">
                            <p className="text-xs text-text-muted">Business Card OCR</p>
                            <p className="font-mono text-white">$0.10 <span className="text-[10px] text-gray-500">/ scan</span></p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Transaction History */}
            <div className="bg-card rounded-2xl border border-gray-800 p-6">
                <h2 className="text-xl font-bold mb-6">Transaction History</h2>
                <div className="space-y-4">
                    {transactions.map(tx => (
                        <div key={tx.id} className="flex items-center justify-between p-4 bg-background/50 rounded-xl hover:bg-background transition">
                            <div className="flex items-center gap-4">
                                <div className={cn("p-2 rounded-full", tx.type === 'credit' ? "bg-emerald-500/10 text-emerald-500" : "bg-red-500/10 text-red-500")}>
                                    {tx.type === 'credit' ? <TrendingUp size={20} /> : <TrendingDown size={20} />}
                                </div>
                                <div>
                                    <p className="font-medium text-white">{tx.desc}</p>
                                    <p className="text-sm text-text-muted">{tx.date}</p>
                                </div>
                            </div>
                            <div className={cn("font-bold text-lg", tx.type === 'credit' ? "text-emerald-500" : "text-white")}>
                                {tx.type === 'credit' ? '+' : '-'}${tx.amount}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Top Up Modal */}
            {showTopUp && (
                <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4" onClick={() => setShowTopUp(false)}>
                    <div className="bg-card border border-gray-700 w-full max-w-md rounded-2xl p-6" onClick={e => e.stopPropagation()}>
                        <h2 className="text-2xl font-bold mb-2">Add Funds</h2>
                        <p className="text-text-muted mb-6">Secure payment via Stripe</p>

                        <div className="grid grid-cols-3 gap-3 mb-6">
                            {[50, 100, 200, 500].map(val => (
                                <button
                                    key={val}
                                    onClick={() => setAmount(val)}
                                    className={cn(
                                        "py-2 rounded-lg border font-medium transition",
                                        amount === val ? "bg-accent text-white border-accent" : "bg-transparent border-gray-700 hover:border-accent"
                                    )}
                                >
                                    ${val}
                                </button>
                            ))}
                        </div>

                        <div className="mb-6">
                            <label className="block text-sm text-text-muted mb-2">Custom Amount</label>
                            <div className="relative">
                                <span className="absolute left-4 top-3 text-text-muted">$</span>
                                <input
                                    type="number"
                                    value={amount}
                                    onChange={e => setAmount(Number(e.target.value))}
                                    className="w-full bg-background border border-gray-700 rounded-lg pl-8 pr-4 py-3 focus:border-accent outline-none text-lg font-bold"
                                />
                            </div>
                        </div>

                        <button onClick={handleTopUp} className="w-full btn-primary bg-emerald-600 hover:bg-emerald-700 text-white py-4 rounded-xl font-bold text-lg flex items-center justify-center gap-2">
                            <CreditCard size={20} /> Pay ${amount}
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
