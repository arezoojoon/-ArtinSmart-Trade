
import { GoogleGenerativeAI } from '@google/generative-ai';

// API Keys - Round Robin
const API_KEYS = [
    'AIzaSyCmxOmUH3gzrVScB78vXOTR-KKiMBdKo1c',
    'AIzaSyAJZry8SoLbEXj_tnVhC5FdfaKj2PBAeP8',
    'AIzaSyDhM6nnAKgwQXiIiocUaMVCbtKzaLhCYHc'
];

let currentKeyIndex = 0;

export const getGeminiClient = () => {
    const key = API_KEYS[currentKeyIndex];
    currentKeyIndex = (currentKeyIndex + 1) % API_KEYS.length;
    return new GoogleGenerativeAI(key);
};

// System Prompts
const PROMPTS = {
    GENERAL: `You are TradeMate, the AI Gateway for the Artin Expo Marketplace.
    Your goal is to route users to the correct role: SELLER or BUYER.
    - Identify the user by name if known.
    - If they haven't selected a role, ask: "Are you here to SELL products or BUY products?"
    - Keep responses short and professional.
    - If they provide a token (e.g. "I have a campaign link"), validate it (simulated).`,

    SELLER: `You are the TradeMate Sales Assistant.
    Your User is a SELLER (Manufacturer/Distributor).
    GOAL: Extract product details to build a catalog entry.
    
    REQUIRED DATA to extract (if missing, ask one by one):
    - Product Name
    - Category
    - Packaging (e.g. 24x250ml)
    - MOQ (Minimum Order Quantity)
    - Price Range
    - Production Capacity
    
    BEHAVIOR:
    - If the user sends an image, analyze it for these details.
    - If the user sends audio, transcribe and extract.
    - Once all data is gathered, output intent: "CREATE_PRODUCT".`,

    BUYER: `You are the TradeMate Sourcing Agent.
    Your User is a BUYER (Retailer/Wholesaler).
    GOAL: Find the best suppliers for their demand.
    
    REQUIRED DATA to extract:
    - Target Product
    - Destination Country
    - Target Price / Budget
    - Volume Needed
    
    BEHAVIOR:
    - Suggest similar products if exact match isn't found (simulate).
    - Compare suppliers based on 'Value Score'.
    - Once details are clear, output intent: "CREATE_REQUEST".`
};

export const generateAIResponse = async (
    prompt: string,
    role: 'guest' | 'seller' | 'buyer' = 'guest',
    context: any = {},
    imageBase64?: string,
    audioBase64?: string
) => {
    try {
        const genAI = getGeminiClient();
        const model = genAI.getGenerativeModel({ model: 'gemini-1.5-pro' });

        const systemPrompt = PROMPTS[role.toUpperCase() as keyof typeof PROMPTS] || PROMPTS.GENERAL;

        const fullPrompt = `
        ${systemPrompt}
        
        CURRENT CONTEXT: ${JSON.stringify(context)}
        
        USER MESSAGE: ${prompt}
        
        OUTPUT FORMAT (JSON ONLY):
        {
            "reply": "Text response to user",
            "intent": "DETECTED_INTENT", 
            "extracted_data": {Field: Value} (Only if actionable data found),
            "missing_fields": ["List", "Of", "Missing", "Data"] (If incomplete)
        }
        `;

        const parts: any[] = [{ text: fullPrompt }];

        if (imageBase64) {
            parts.push({
                inlineData: { mimeType: "image/jpeg", data: imageBase64 }
            });
        }

        if (audioBase64) {
            parts.push({
                inlineData: { mimeType: "audio/mp3", data: audioBase64 }
            });
        }

        const result = await model.generateContent(parts);
        const text = result.response.text();

        // Sanitize JSON
        const cleanText = text.replace(/```json/g, '').replace(/```/g, '').trim();
        return JSON.parse(cleanText);

    } catch (error) {
        console.error('[Gemini Error]', error);
        return {
            reply: "I am processing a high volume of trades. Please try again.",
            intent: "ERROR"
        };
    }
};
