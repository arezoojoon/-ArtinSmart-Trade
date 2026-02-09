import { NextResponse } from 'next/server';
import { generateAIResponse } from '@/lib/gemini';

export async function POST(req: Request) {
    try {
        const { message, context, image, audio } = await req.json();

        console.log(`[AI Engine] Processing: "${message.substring(0, 50)}..." | Image: ${!!image} | Audio: ${!!audio}`);

        // Call Real Gemini 1.5 Pro API
        const aiResult = await generateAIResponse(message, context, image, audio);

        return NextResponse.json({
            success: true,
            data: {
                reply_suggestion: aiResult.reply,
                intent: aiResult.intent,
                confidence: aiResult.confidence,
                extracted_data: aiResult.data,
                timestamp: new Date().toISOString()
            }
        });

    } catch (error) {
        console.error('[AI API Error]', error);
        return NextResponse.json(
            { success: false, error: 'Internal AI Processing Error' },
            { status: 500 }
        );
    }
}
