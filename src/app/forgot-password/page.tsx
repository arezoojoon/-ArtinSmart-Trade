'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import Link from 'next/link';
import { Loader2, TrendingUp, ArrowLeft } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function ForgotPasswordPage() {
    const [email, setEmail] = useState('');
    const [sent, setSent] = useState(false);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const res = await fetch(`${API_URL}/api/v1/auth/forgot-password`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email }),
            });

            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.detail || 'Request failed');
            }

            setSent(true);
        } catch (err: any) {
            setError(err.message || 'Failed to send reset email');
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
                </div>

                <Card>
                    <CardHeader>
                        <CardTitle className="text-xl">Reset Password</CardTitle>
                        <CardDescription>
                            {sent ? 'Check your email for a reset link' : 'Enter your email to receive a password reset link'}
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        {sent ? (
                            <div className="text-center space-y-4">
                                <div className="bg-primary/10 border border-primary/20 text-primary text-sm p-4 rounded-md">
                                    If an account exists with {email}, you will receive a password reset link shortly.
                                </div>
                                <Link href="/login">
                                    <Button variant="outline" className="w-full mt-4">
                                        <ArrowLeft className="h-4 w-4 mr-2" /> Back to Login
                                    </Button>
                                </Link>
                            </div>
                        ) : (
                            <form onSubmit={handleSubmit} className="space-y-4">
                                {error && (
                                    <div className="bg-destructive/10 border border-destructive/20 text-destructive text-sm p-3 rounded-md">
                                        {error}
                                    </div>
                                )}
                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Email</label>
                                    <Input
                                        type="email"
                                        placeholder="trader@company.com"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        required
                                    />
                                </div>
                                <Button type="submit" className="w-full" disabled={loading}>
                                    {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                                    Send Reset Link
                                </Button>
                                <Link href="/login" className="block text-center text-sm text-primary hover:underline">
                                    <ArrowLeft className="h-3 w-3 inline mr-1" /> Back to Login
                                </Link>
                            </form>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
