const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_V1 = `${API_BASE}/api/v1`;

function getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
}

function setTokens(access: string, refresh: string) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    document.cookie = `access_token=${access}; path=/; max-age=86400; SameSite=Lax`;
}

function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    document.cookie = 'access_token=; path=/; max-age=0';
}

async function apiFetch<T = any>(
    endpoint: string,
    options: RequestInit = {},
): Promise<T> {
    const token = getToken();
    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...(options.headers as Record<string, string> || {}),
    };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const res = await fetch(`${API_V1}${endpoint}`, {
        ...options,
        headers,
    });

    if (res.status === 401) {
        clearTokens();
        if (typeof window !== 'undefined') {
            window.location.href = '/login';
        }
        throw new Error('Unauthorized');
    }

    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(err.detail || `Error ${res.status}`);
    }

    if (res.status === 204) return {} as T;
    return res.json();
}

export const api = {
    get: <T = any>(url: string) => apiFetch<T>(url),
    post: <T = any>(url: string, data?: any) =>
        apiFetch<T>(url, { method: 'POST', body: data ? JSON.stringify(data) : undefined }),
    put: <T = any>(url: string, data?: any) =>
        apiFetch<T>(url, { method: 'PUT', body: data ? JSON.stringify(data) : undefined }),
    delete: <T = any>(url: string) =>
        apiFetch<T>(url, { method: 'DELETE' }),
};

export { setTokens, clearTokens, getToken, API_V1 };
export default api;
