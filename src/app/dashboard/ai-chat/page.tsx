'use client';

import { useState, useRef, useEffect } from 'react';
import { api } from '@/lib/api';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Send, BrainCircuit, Loader2, Clock, Sparkles } from 'lucide-react';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    confidence?: number;
    sources?: string[];
    suggestions?: string[];
    timestamp: Date;
}

const quickPrompts = [
    "What products are in season right now?",
    "Find me the best suppliers for sugar in Dubai",
    "Analyze my current margins and suggest improvements",
    "What's the market outlook for FMCG this quarter?",
    "When is the best time to buy rice?",
    "Help me negotiate a better deal on cooking oil",
];

export default function AIChatPage() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [history, setHistory] = useState<any[]>([]);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        api.get('/ai/history?limit=10').then(setHistory).catch(() => {});
    }, []);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const sendMessage = async (text?: string) => {
        const msg = text || input;
        if (!msg.trim()) return;

        const userMsg: Message = { role: 'user', content: msg, timestamp: new Date() };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            const res = await api.post('/ai/chat', { message: msg });
            const aiMsg: Message = {
                role: 'assistant',
                content: res.reply,
                confidence: res.confidence,
                sources: res.sources,
                suggestions: res.suggestions,
                timestamp: new Date(),
            };
            setMessages(prev => [...prev, aiMsg]);
        } catch (err: any) {
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please try again.',
                timestamp: new Date(),
            }]);
        }
        setLoading(false);
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="flex flex-col h-[calc(100vh-6rem)]">
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                    <BrainCircuit className="h-7 w-7 text-primary" />
                    <div>
                        <h1 className="text-2xl font-bold">Artin AI Assistant</h1>
                        <p className="text-muted-foreground text-sm">Your AI-powered trade advisor</p>
                    </div>
                </div>
                <Badge variant="default">Gemini Powered</Badge>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto space-y-4 pr-2">
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full text-center space-y-6">
                        <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center">
                            <Sparkles className="h-10 w-10 text-primary" />
                        </div>
                        <div>
                            <h2 className="text-xl font-bold mb-2">How can I help you trade smarter?</h2>
                            <p className="text-muted-foreground text-sm max-w-md">
                                I analyze your products, market data, and trade history to give you actionable insights.
                            </p>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 max-w-lg w-full">
                            {quickPrompts.map((prompt, i) => (
                                <button
                                    key={i}
                                    onClick={() => sendMessage(prompt)}
                                    className="text-left p-3 rounded-lg border border-border bg-card hover:border-primary/50 hover:bg-primary/5 transition-colors text-sm"
                                >
                                    {prompt}
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {messages.map((msg, i) => (
                    <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] rounded-2xl p-4 ${
                            msg.role === 'user'
                                ? 'bg-primary text-primary-foreground rounded-br-sm'
                                : 'bg-card border border-border rounded-bl-sm'
                        }`}>
                            <div className="whitespace-pre-wrap text-sm">{msg.content}</div>
                            {msg.confidence && (
                                <div className="mt-2 flex items-center gap-2">
                                    <div className="h-1.5 flex-1 bg-secondary rounded-full overflow-hidden">
                                        <div className="h-full bg-primary rounded-full" style={{ width: `${msg.confidence * 100}%` }} />
                                    </div>
                                    <span className="text-[10px] text-muted-foreground">{(msg.confidence * 100).toFixed(0)}%</span>
                                </div>
                            )}
                            {msg.sources && msg.sources.length > 0 && (
                                <div className="mt-2 flex gap-1 flex-wrap">
                                    {msg.sources.map((s, j) => (
                                        <span key={j} className="text-[10px] bg-secondary/50 px-1.5 py-0.5 rounded">{s}</span>
                                    ))}
                                </div>
                            )}
                            {msg.suggestions && msg.suggestions.length > 0 && (
                                <div className="mt-3 space-y-1">
                                    <p className="text-[10px] text-muted-foreground uppercase tracking-wider">Suggestions:</p>
                                    {msg.suggestions.map((s, j) => (
                                        <button
                                            key={j}
                                            onClick={() => sendMessage(s)}
                                            className="block w-full text-left text-xs p-2 rounded bg-secondary/30 hover:bg-secondary/50 transition-colors"
                                        >
                                            {s}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-card border border-border rounded-2xl rounded-bl-sm p-4">
                            <div className="flex items-center gap-2">
                                <Loader2 className="h-4 w-4 animate-spin text-primary" />
                                <span className="text-sm text-muted-foreground">Analyzing...</span>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="mt-4 flex gap-2">
                <Input
                    placeholder="Ask about pricing, seasonality, suppliers, deals..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    className="flex-1"
                    disabled={loading}
                />
                <Button onClick={() => sendMessage()} disabled={loading || !input.trim()}>
                    <Send className="h-4 w-4" />
                </Button>
            </div>
        </div>
    );
}
