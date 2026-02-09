'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Eye, EyeOff, Lock, Mail, User, Building, ArrowRight, ArrowLeft } from 'lucide-react';
import { cn } from '@/lib/utils';
import { supabase } from '@/lib/supabase';

export default function RegisterPage() {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    // Form State
    const [fullName, setFullName] = useState('');
    const [companyName, setCompanyName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const { error } = await supabase.auth.signUp({
                email,
                password,
                options: {
                    data: {
                        full_name: fullName,
                        company_name: companyName,
                    },
                },
            });

            if (error) throw error;

            alert('Registration successful! Please check your email to verify your account.');
            router.push('/login');
        } catch (error) {
            console.error('Registration error:', error);
            alert('Registration failed. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-gray-900 via-black to-gray-800 relative">
            <div className="absolute inset-0 bg-black/60 backdrop-blur-sm z-0"></div>

            <div className="relative z-10 w-full max-w-lg p-8 bg-black/40 border border-white/10 backdrop-blur-md rounded-3xl shadow-2xl animate-in fade-in zoom-in duration-500">
                <Link href="/" className="inline-flex items-center text-gray-400 hover:text-white mb-6 text-sm transition-colors">
                    <ArrowLeft size={16} className="mr-1" /> Back to Home
                </Link>

                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-white tracking-tight">Create Account</h1>
                    <p className="text-text-muted mt-2">Join the future of B2B trade</p>
                </div>

                <form onSubmit={handleRegister} className="space-y-5">

                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-300 ml-1">Full Name</label>
                            <div className="relative group">
                                <User className="absolute left-3 top-3.5 text-gray-500 group-focus-within:text-accent transition-colors" size={20} />
                                <input
                                    type="text"
                                    placeholder="John Doe"
                                    className="w-full bg-black/50 border border-gray-700 rounded-xl py-3 pl-10 pr-4 text-white placeholder-gray-500 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all"
                                    value={fullName}
                                    onChange={(e) => setFullName(e.target.value)}
                                    required
                                />
                            </div>
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-300 ml-1">Company</label>
                            <div className="relative group">
                                <Building className="absolute left-3 top-3.5 text-gray-500 group-focus-within:text-accent transition-colors" size={20} />
                                <input
                                    type="text"
                                    placeholder="Acme Corp"
                                    className="w-full bg-black/50 border border-gray-700 rounded-xl py-3 pl-10 pr-4 text-white placeholder-gray-500 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all"
                                    value={companyName}
                                    onChange={(e) => setCompanyName(e.target.value)}
                                    required
                                />
                            </div>
                        </div>
                    </div>

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
                        <label className="text-sm font-medium text-gray-300 ml-1">Password</label>
                        <div className="relative group">
                            <Lock className="absolute left-3 top-3.5 text-gray-500 group-focus-within:text-accent transition-colors" size={20} />
                            <input
                                type={showPassword ? "text" : "password"}
                                placeholder="Create a strong password"
                                className="w-full bg-black/50 border border-gray-700 rounded-xl py-3 pl-10 pr-12 text-white placeholder-gray-500 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                minLength={6}
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute right-3 top-3.5 text-gray-500 hover:text-white transition-colors"
                            >
                                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                            </button>
                        </div>
                        <p className="text-xs text-gray-500 ml-1">Must be at least 6 characters long.</p>
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full bg-accent hover:bg-accent-hover text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-accent/20 flex items-center justify-center gap-2 group mt-4"
                    >
                        {isLoading ? (
                            <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                            <>
                                Create Account <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                            </>
                        )}
                    </button>
                </form>

                <div className="mt-8 text-center">
                    <p className="text-text-muted text-sm">
                        Already have an account?{' '}
                        <Link href="/login" className="text-white font-medium hover:text-accent transition-colors">
                            Sign In
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
