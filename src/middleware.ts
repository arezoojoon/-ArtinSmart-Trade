import { NextResponse, type NextRequest } from 'next/server';

const publicPaths = ['/login', '/signup', '/forgot-password', '/reset-password'];

export async function middleware(req: NextRequest) {
    const { pathname } = req.nextUrl;

    // Allow public paths
    if (publicPaths.some(p => pathname.startsWith(p)) || pathname === '/') {
        return NextResponse.next();
    }

    // Check for token in cookies
    const token = req.cookies.get('access_token')?.value;

    if (!token && pathname.startsWith('/dashboard')) {
        return NextResponse.redirect(new URL('/login', req.url));
    }

    // Admin routes protection (basic check — real auth happens server-side)
    if (pathname.startsWith('/dashboard/admin') && token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            if (!['admin', 'super_admin'].includes(payload.role)) {
                return NextResponse.redirect(new URL('/dashboard', req.url));
            }
        } catch {
            return NextResponse.redirect(new URL('/login', req.url));
        }
    }

    return NextResponse.next();
}

export const config = {
    matcher: ['/((?!api|_next/static|_next/image|favicon.ico|manifest.json|icons).*)'],
};
