'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Eye, EyeOff, Lock, Mail, ArrowRight, CheckCircle2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { supabase } from '@/lib/supabase';

export default function LoginPage() {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            // Integrate Supabase Auth
            const { error } = await supabase.auth.signInWithPassword({
                email,
                password,
            });

            if (error) throw error;

            router.push('/dashboard');
        } catch (error) {
            console.error('Login error:', error);
            alert('Login failed. Please check your credentials.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-gray-900 via-black to-gray-800 relative">
            {/* Dark Overlay */}
            <div className="absolute inset-0 bg-black/60 backdrop-blur-sm z-0"></div>

            <div className="relative z-10 w-full max-w-md p-8 bg-black/40 border border-white/10 backdrop-blur-md rounded-3xl shadow-2xl animate-in fade-in zoom-in duration-500">
                <div className="text-center mb-8">
                    <div className="w-20 h-20 relative mx-auto mb-4">
                        <img src="/logo.png" alt="Logo" className="object-contain w-full h-full" />
                    </div>
                    <h1 className="text-3xl font-bold text-white tracking-tight">Welcome Back</h1>
                    <p className="text-text-muted mt-2">Sign in to your TradeMate account</p>
                </div>

                <form onSubmit={handleLogin} className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-sm font-medium text-gray-300 ml-1">Email Address</label>
                        <div className="relative group">
                            <Mail className="absolute left-3 top-3.5 text-gray-500 group-focus-within:text-accent transition-colors" size={20} />
                            <input
                                type="email"
                                placeholder="name@company.com"
                                className="w-full bg-black/50 border border-gray-700 rounded-xl py-3 pl-10 pr-4 text-white placeholder-gray-500 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <div className="flex justify-between items-center ml-1">
                            <label className="text-sm font-medium text-gray-300">Password</label>
                            <Link href="/forgot-password" className="text-xs text-accent hover:text-accent-hover transition-colors">
                                Forgot password?
                            </Link>
                        </div>
                        <div className="relative group">
                            <Lock className="absolute left-3 top-3.5 text-gray-500 group-focus-within:text-accent transition-colors" size={20} />
                            <input
                                type={showPassword ? "text" : "password"}
                                placeholder="••••••••"
                                className="w-full bg-black/50 border border-gray-700 rounded-xl py-3 pl-10 pr-12 text-white placeholder-gray-500 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute right-3 top-3.5 text-gray-500 hover:text-white transition-colors"
                            >
                                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                            </button>
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full bg-accent hover:bg-accent-hover text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-accent/20 flex items-center justify-center gap-2 group"
                    >
                        {isLoading ? (
                            <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                            <>
                                Sign In <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                            </>
                        )}
                    </button>
                </form>

                <div className="mt-8 text-center">
                    <p className="text-text-muted text-sm">
                        Don't have an account?{' '}
                        <Link href="/register" className="text-white font-medium hover:text-accent transition-colors">
                            Create an account
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
