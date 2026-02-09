import { NextResponse } from 'next/server';

export async function POST(req: Request) {
    try {
        const { query, source } = await req.json();

        // Call Python Backend
        // Ensure the Python server is running on port 8000
        const pythonServiceUrl = process.env.PYTHON_SERVICE_URL || 'http://127.0.0.1:8000';

        try {
            const res = await fetch(`${pythonServiceUrl}/api/scrape`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query,
                    source: source || 'google_maps',
                    tenant_id: 'default' // Todo: Get from session
                }),
            });

            if (!res.ok) {
                console.error("Python Backend Error:", res.status, res.statusText);
                return NextResponse.json(
                    { success: false, error: 'Hunter Engine Offline or Error' },
                    { status: 502 } // Bad Gateway
                );
            }

            const data = await res.json();
            return NextResponse.json(data);

        } catch (fetchError) {
            console.error("Connection to Python Backend Failed", fetchError);
            return NextResponse.json(
                { success: false, error: 'Hunter Engine Unreachable. Is main.py running?' },
                { status: 503 } // Service Unavailable
            );
        }

    } catch (error) {
        console.error('[Hunter API Error]', error);
        return NextResponse.json(
            { success: false, error: 'Internal Server Error' },
            { status: 500 }
        );
    }
}
