'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { setTokens, clearTokens } from '@/lib/api';

interface User {
    id: string;
    email: string;
    role: string;
    tenant_id: string;
    tenant_name?: string;
    full_name?: string;
    plan?: string;
}

interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (token: string, refreshToken: string) => void;
    logout: () => void;
    isAuthenticated: boolean;
    isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

function decodeToken(token: string): User | null {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return {
            id: payload.user_id || '',
            email: payload.sub || payload.email || '',
            role: payload.role || 'buyer',
            tenant_id: payload.tenant_id || '',
        };
    } catch {
        return null;
    }
}

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        const storedToken = localStorage.getItem('access_token');
        if (storedToken) {
            const decoded = decodeToken(storedToken);
            if (decoded) {
                setUser(decoded);
                setToken(storedToken);
            } else {
                clearTokens();
            }
        }
        setIsLoading(false);
    }, []);

    const login = (accessToken: string, refreshToken: string) => {
        setTokens(accessToken, refreshToken);
        setToken(accessToken);
        const decoded = decodeToken(accessToken);
        if (decoded) {
            setUser(decoded);
        }
        router.push('/dashboard');
    };

    const logout = () => {
        clearTokens();
        setUser(null);
        setToken(null);
        router.push('/login');
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!user, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
