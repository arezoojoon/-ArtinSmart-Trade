'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Mic, Image as ImageIcon, Phone, MoreVertical, Paperclip } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function WhatsAppSimulator() {
    const [messages, setMessages] = useState<any[]>([
        { text: "System: Waiting for connection...", sender: 'system' }
    ]);
    const [input, setInput] = useState('');
    const [phone] = useState('971501234567'); // Simulated Phone
    const [token, setToken] = useState('camp_summer_2026'); // Simulated Token
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;
        const userMsg = input;

        // Add user message to UI
        const newMessages = [...messages, { text: userMsg, sender: 'user' }];
        setMessages(newMessages);
        setInput('');
        setIsTyping(true);

        try {
            const res = await fetch('/api/whatsapp', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: userMsg,
                    phone: phone,
                    token: token // This simulates the entry link
                })
            });

            const data = await res.json();

            setMessages(prev => [...prev, {
                text: data.reply || (data.error ? `Error: ${data.error}` : 'No response'),
                sender: 'bot',
                intent: data.intent
            }]);

        } catch (error) {
            setMessages(prev => [...prev, { text: "Error connecting to server", sender: 'system' }]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="flex h-screen bg-[#0c1317] justify-center items-center p-4">
            {/* Phone Frame */}
            <div className="w-full max-w-md h-[800px] bg-[#111b21] rounded-[30px] border-[8px] border-[#2a2f32] overflow-hidden flex flex-col shadow-2xl relative">

                {/* Header */}
                <div className="h-16 bg-[#202c33] flex items-center px-4 justify-between shrink-0 z-10">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-accent flex items-center justify-center text-white font-bold">
                            TM
                        </div>
                        <div>
                            <p className="text-[#e9edef] font-medium">TradeMate AI</p>
                            <p className="text-[#8696a0] text-xs">Business Account</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-4 text-[#aebac1]">
                        <Phone size={20} />
                        <Paperclip size={20} />
                        <MoreVertical size={20} />
                    </div>
                </div>

                {/* Wallpaper */}
                <div className="absolute inset-0 z-0 opacity-10 bg-[url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png')] bg-repeat" />

                {/* Messages Area */}
                <div className="flex-1 overflow-y-auto p-4 space-y-2 z-10 scrollbar-hide">
                    {messages.map((msg, i) => (
                        <div
                            key={i}
                            className={cn(
                                "max-w-[80%] p-2 px-3 rounded-lg text-sm relative mb-2 shadow-sm break-words",
                                msg.sender === 'user' ? "ml-auto bg-[#005c4b] text-[#e9edef] rounded-tr-none" :
                                    msg.sender === 'bot' ? "bg-[#202c33] text-[#e9edef] rounded-tl-none" :
                                        "bg-[#182229] text-[#ffd279] text-xs text-center mx-auto w-fit"
                            )}
                        >
                            {msg.text}
                            {msg.sender !== 'system' && (
                                <span className="text-[10px] text-[#ffffff99] float-right mt-2 ml-2">12:0{i}</span>
                            )}
                        </div>
                    ))}
                    {isTyping && (
                        <div className="bg-[#202c33] text-[#e9edef] rounded-tl-none p-2 px-4 w-fit text-xs animate-pulse">
                            TradeMate is typing...
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="bg-[#202c33] p-2 flex items-center gap-2 shrink-0 z-10">
                    <button className="p-2 text-[#8696a0] hover:bg-[#2a3942] rounded-full">
                        <ImageIcon size={24} />
                    </button>
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Type a message..."
                        className="flex-1 bg-[#2a3942] text-[#d1d7db] rounded-lg px-4 py-2 border-none focus:outline-none placeholder-[#8696a0]"
                    />
                    {input.trim() ? (
                        <button onClick={handleSend} className="p-2 bg-[#00a884] text-white rounded-full">
                            <Send size={20} />
                        </button>
                    ) : (
                        <button className="p-2 text-[#8696a0] hover:bg-[#2a3942] rounded-full">
                            <Mic size={24} />
                        </button>
                    )}
                </div>

                {/* Controls Overlay (For Demo) */}
                <div className="absolute top-20 left-4 bg-black/50 p-2 rounded text-xs text-white z-20">
                    <p>Token: <span className="font-mono text-green-400">{token}</span></p>
                    <button onClick={() => setToken('')} className="underline text-red-400">Clear Token (Simulate Unauthorized)</button>
                    <br />
                    <button onClick={() => setToken('camp_valid')} className="underline text-green-400">Set Valid Token</button>
                </div>
            </div>
        </div>
    );
}
