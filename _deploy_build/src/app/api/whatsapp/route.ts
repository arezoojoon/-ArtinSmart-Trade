import { NextResponse } from 'next/server';
import { Marketplace } from '@/lib/marketplace';
import { generateAIResponse } from '@/lib/gemini';

export async function POST(req: Request) {
    try {
        const { message, phone, token, image, audio } = await req.json();

        if (!phone) {
            return NextResponse.json({ error: 'Phone number required' }, { status: 400 });
        }

        // 1. Get or Create Session
        const session = Marketplace.getSession(phone);

        // 2. Entry Control (Strict)
        if (session.state === 'INIT') {
            if (!token) {
                return NextResponse.json({
                    reply: "⛔ Access Denied. Please use a valid Campaign or RFQ link to enter the marketplace."
                });
            }
            const isValid = await Marketplace.validateEntryToken(token);
            if (!isValid) {
                return NextResponse.json({
                    reply: "⛔ Invalid Entry Token. Connection Refused."
                });
            }
            // Valid Token -> Move to Role Selection
            Marketplace.updateSession(phone, { state: 'ROLE_SELECTION' });
        }

        // 3. Handle Role Selection
        if (session.state === 'ROLE_SELECTION') {
            const lowerMsg = message.toLowerCase();
            if (lowerMsg.includes('sell')) {
                Marketplace.updateSession(phone, { role: 'seller', state: 'SELLER_FLOW', context: { stage: 'product_details' } });
                return NextResponse.json({
                    reply: "✅ Role Set: SELLER. \nI can help you list your products. Please send me a photo of your product or describe it (Name, Price, MOQ).",
                    intent: "ROLE_SET_SELLER"
                });
            } else if (lowerMsg.includes('buy')) {
                Marketplace.updateSession(phone, { role: 'buyer', state: 'BUYER_FLOW', context: { stage: 'sourcing_request' } });
                return NextResponse.json({
                    reply: "✅ Role Set: BUYER. \nI can help you source products. What are you looking for today? (e.g. 'Tomato Paste for Dubai')",
                    intent: "ROLE_SET_BUYER"
                });
            }
        }

        // 4. AI Processing (Role-Based)
        // Inject current context into AI
        const aiResponse = await generateAIResponse(
            message,
            session.role,
            session.context,
            image, // Base64
            audio  // Base64
        );

        // 5. Update Context based on AI Output
        if (aiResponse.extracted_data) {
            const newContext = { ...session.context, ...aiResponse.extracted_data };
            Marketplace.updateSession(phone, { context: newContext });
        }

        // 6. Handle Specific Intents (e.g. Database Insert)
        if (aiResponse.intent === 'CREATE_PRODUCT' && session.role === 'seller') {
            await Marketplace.createProduct(phone, session.context); // phone as temp ID
            return NextResponse.json({
                reply: `🎉 Product Created! \n${aiResponse.reply} \nIt is now live for buyers.`,
                intent: "PRODUCT_CREATED"
            });
        }

        if (aiResponse.intent === 'CREATE_REQUEST' && session.role === 'buyer') {
            await Marketplace.createSourcingRequest(phone, session.context);
            return NextResponse.json({
                reply: `🚀 Sourcing Request Live! \n${aiResponse.reply} \nI will notify you when I find a match.`,
                intent: "REQUEST_CREATED"
            });
        }

        return NextResponse.json(aiResponse);

    } catch (error) {
        console.error('[WhatsApp Webhook Error]', error);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
