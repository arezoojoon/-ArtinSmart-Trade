'use client';

import { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import Link from 'next/link';
import { Loader2, TrendingUp } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function SignupPage() {
    const { login } = useAuth();
    const [form, setForm] = useState({ email: '', password: '', full_name: '', tenant_name: '', role: 'buyer' });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const res = await fetch(`${API_URL}/api/v1/auth/signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(form),
            });

            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.detail || 'Signup failed');
            }

            const data = await res.json();
            login(data.access_token, data.refresh_token);
        } catch (err: any) {
            setError(err.message || 'Signup failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-background p-4">
            <div className="w-full max-w-md space-y-8">
                <div className="text-center">
                    <div className="flex items-center justify-center gap-2 mb-4">
                        <TrendingUp className="h-10 w-10 text-primary" />
                        <h1 className="text-3xl font-bold text-primary">Artin Smart Trade</h1>
                    </div>
                    <p className="text-muted-foreground">Create your trade account</p>
                </div>

                <Card>
                    <CardHeader>
                        <CardTitle className="text-xl">Sign Up</CardTitle>
                        <CardDescription>Start trading smarter with AI-powered insights</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            {error && (
                                <div className="bg-destructive/10 border border-destructive/20 text-destructive text-sm p-3 rounded-md">
                                    {error}
                                </div>
                            )}
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Full Name</label>
                                <Input
                                    placeholder="John Doe"
                                    value={form.full_name}
                                    onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Company Name</label>
                                <Input
                                    placeholder="Your Company Ltd."
                                    value={form.tenant_name}
                                    onChange={(e) => setForm({ ...form, tenant_name: e.target.value })}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Email</label>
                                <Input
                                    type="email"
                                    placeholder="trader@company.com"
                                    value={form.email}
                                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Password</label>
                                <Input
                                    type="password"
                                    placeholder="Min 8 characters"
                                    value={form.password}
                                    onChange={(e) => setForm({ ...form, password: e.target.value })}
                                    required
                                    minLength={8}
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium">I am a</label>
                                <div className="grid grid-cols-3 gap-2">
                                    {['buyer', 'seller', 'both'].map((role) => (
                                        <button
                                            key={role}
                                            type="button"
                                            onClick={() => setForm({ ...form, role })}
                                            className={`py-2 px-3 rounded-md border text-sm capitalize transition-colors ${
                                                form.role === role
                                                    ? 'bg-primary text-primary-foreground border-primary'
                                                    : 'bg-secondary border-border hover:bg-secondary/80'
                                            }`}
                                        >
                                            {role}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            <Button type="submit" className="w-full" disabled={loading}>
                                {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                                Create Account
                            </Button>
                        </form>
                        <div className="mt-6 text-center text-sm">
                            Already have an account?{' '}
                            <Link href="/login" className="text-primary hover:underline font-medium">
                                Sign In
                            </Link>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
