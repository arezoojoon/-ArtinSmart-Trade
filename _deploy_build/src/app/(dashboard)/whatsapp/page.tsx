'use client';

import { useState, useRef } from 'react';
import {
    MessageSquare,
    Send,
    MoreVertical,
    Search,
    Paperclip,
    Mic,
    Bot,
    Users,
    Check,
    CheckCheck,
    Plus
} from 'lucide-react';
import { cn } from '@/lib/utils';
import Image from 'next/image';

const mockChats = [
    { id: 1, name: "Ahmed Al-Mansoori", lastMessage: "Can you send the price list for Nutella?", time: "10:30 AM", unread: 2, status: 'online' },
    { id: 2, name: "John Smith (Carrefour)", lastMessage: "Thanks, we will review the proposal.", time: "Yesterday", unread: 0, status: 'offline' },
    { id: 3, name: "Sarah Jenkins", lastMessage: "Is the MOQ negotiable?", time: "Yesterday", unread: 0, status: 'offline' },
];

const mockMessages = [
    { id: 1, sender: 'them', text: "Hi, do you have stock of Nutella 750g?", time: "10:28 AM" },
    { id: 2, sender: 'me', text: "Yes, we have 500 cases ready for immediate delivery.", time: "10:29 AM", status: 'read' },
    { id: 3, sender: 'them', text: "Great. Can you send the price list for Nutella?", time: "10:30 AM" },
];

export default function WhatsAppPage() {
    const [activeChat, setActiveChat] = useState<number | null>(1);
    const [messages, setMessages] = useState(mockMessages);
    const [inputText, setInputText] = useState("");
    const [isAiTyping, setIsAiTyping] = useState(false);
    const [isRecording, setIsRecording] = useState(false);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const chunksRef = useRef<Blob[]>([]);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorderRef.current = mediaRecorder;
            chunksRef.current = [];

            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) chunksRef.current.push(e.data);
            };

            mediaRecorder.onstop = async () => {
                const blob = new Blob(chunksRef.current, { type: 'audio/webm' }); // Chrome records in webm
                // Convert to Base64
                const reader = new FileReader();
                reader.readAsDataURL(blob);
                reader.onloadend = () => {
                    const base64Audio = (reader.result as string).split(',')[1];
                    sendAudioMessage(base64Audio);
                };
            };

            mediaRecorder.start();
            setIsRecording(true);
        } catch (err) {
            console.error("Error accessing microphone:", err);
            alert("Could not access microphone.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
            // Stop all tracks
            mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
        }
    };

    const sendAudioMessage = (base64Audio: string) => {
        const newMsg = { id: Date.now(), sender: 'me', text: "🎤 Voice Message", time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), status: 'sent' };
        // @ts-ignore
        setMessages(prev => [...prev, newMsg]);
        setIsAiTyping(true);

        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: "User sent a voice message. Transcribe and reply.", // Fallback prompt
                context: "Voice Interaction",
                audio: base64Audio
            })
        })
            .then(res => res.json())
            .then(data => {
                const aiMsg = {
                    id: Date.now() + 1,
                    sender: 'ai',
                    text: data.data?.reply_suggestion || "I didn't quite catch that.",
                    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                };
                // @ts-ignore
                setMessages(prev => [...prev, aiMsg]);
            })
            .finally(() => setIsAiTyping(false));
    };

    const handleSend = () => {
        if (!inputText.trim()) return;

        const newMsg = { id: Date.now(), sender: 'me', text: inputText, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), status: 'sent' };
        setMessages([...messages, newMsg]);
        setInputText("");

        // Call Real AI API
        if (inputText.toLowerCase().includes('price') || inputText.toLowerCase().includes('catalog') || inputText.toLowerCase().includes('stock') || inputText.toLowerCase().includes('hi')) {
            setIsAiTyping(true);

            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: inputText,
                    context: "User is a potential buyer from Gulfood 2026."
                })
            })
                .then(res => res.json())
                .then(data => {
                    const aiMsg = {
                        id: Date.now() + 1,
                        sender: 'ai',
                        text: data.data?.reply_suggestion || "I'm having trouble connecting. Please try again.",
                        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                    };
                    // @ts-ignore
                    setMessages(prev => [...prev, aiMsg]);
                })
                .catch(err => {
                    console.error("AI Error:", err);
                })
                .finally(() => {
                    setIsAiTyping(false);
                });
        }
    };

    return (
        <div className="h-[calc(100vh-6rem)] bg-card rounded-2xl border border-gray-800 overflow-hidden flex">
            {/* Sidebar / Chat List */}
            <div className="w-80 border-r border-gray-800 flex flex-col">
                <div className="p-4 border-b border-gray-800 bg-gray-900/50">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="font-bold text-lg">Chats</h2>
                        <div className="flex gap-2">
                            <button className="p-2 hover:bg-gray-800 rounded-full" title="New Broadcast"><Users size={20} /></button>
                            <button className="p-2 hover:bg-gray-800 rounded-full"><Plus size={20} /></button>
                        </div>
                    </div>
                    <div className="relative">
                        <Search className="absolute left-3 top-2.5 text-text-muted" size={16} />
                        <input type="text" placeholder="Search or start new chat" className="w-full bg-background border border-gray-800 rounded-lg pl-9 pr-3 py-2 text-sm focus:border-accent outline-none" />
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto">
                    {mockChats.map(chat => (
                        <div
                            key={chat.id}
                            onClick={() => setActiveChat(chat.id)}
                            className={cn(
                                "p-4 border-b border-gray-800 cursor-pointer hover:bg-gray-800/50 transition flex gap-3",
                                activeChat === chat.id && "bg-gray-800/50 border-emerald-500/30 border-l-2"
                            )}
                        >
                            <div className="relative">
                                <div className="w-12 h-12 rounded-full bg-gray-700 flex items-center justify-center text-white font-medium">
                                    {chat.name.charAt(0)}
                                </div>
                                {chat.status === 'online' && <div className="absolute bottom-0 right-0 w-3 h-3 bg-emerald-500 rounded-full border-2 border-card"></div>}
                            </div>
                            <div className="flex-1 min-w-0">
                                <div className="flex justify-between items-baseline mb-1">
                                    <h3 className="font-semibold truncate">{chat.name}</h3>
                                    <span className="text-xs text-text-muted">{chat.time}</span>
                                </div>
                                <p className="text-sm text-text-muted truncate">{chat.lastMessage}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Chat Area */}
            <div className="flex-1 flex flex-col bg-[#0b141a]"> {/* WhatsApp Dark Bg */}
                {/* Chat Header */}
                <div className="p-4 border-b border-gray-800 bg-card flex justify-between items-center">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center text-white">A</div>
                        <div>
                            <h3 className="font-bold">Ahmed Al-Mansoori</h3>
                            <span className="text-xs text-text-muted">Online</span>
                        </div>
                    </div>
                    <div className="flex gap-4 text-text-muted">
                        <Search size={20} />
                        <MoreVertical size={20} />
                    </div>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-[url('/whatsapp-bg-dark.png')] bg-repeat">
                    {messages.map(msg => (
                        <div key={msg.id} className={cn("flex", msg.sender === 'me' ? "justify-end" : "justify-start")}>
                            {msg.sender === 'ai' ? (
                                <div className="bg-accent/10 border border-accent/20 text-accent p-3 rounded-lg max-w-md text-sm flex gap-2">
                                    <Bot size={16} className="mt-1 flex-shrink-0" />
                                    <div>{msg.text}</div>
                                </div>
                            ) : (
                                <div className={cn(
                                    "max-w-md p-3 rounded-lg shadow-sm relative",
                                    msg.sender === 'me' ? "bg-emerald-700 text-white rounded-tr-none" : "bg-gray-800 text-white rounded-tl-none"
                                )}>
                                    <p className="text-sm leading-relaxed">{msg.text}</p>
                                    <div className="flex justify-end items-center gap-1 mt-1">
                                        <span className="text-[10px] text-white/70">{msg.time}</span>
                                        {msg.sender === 'me' && (
                                            msg.status === 'read' ? <CheckCheck size={12} className="text-blue-400" /> : <Check size={12} className="text-white/70" />
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                    {isAiTyping && (
                        <div className="flex justify-start">
                            <div className="bg-gray-800 p-3 rounded-lg rounded-tl-none">
                                <div className="flex gap-1">
                                    <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></span>
                                    <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75"></span>
                                    <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150"></span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Input Area */}
                <div className="p-4 bg-card border-t border-gray-800 flex items-center gap-4">
                    <button className="text-text-muted hover:text-white"><Plus size={24} /></button>
                    <div className="flex-1 bg-gray-800 rounded-lg flex items-center px-4 py-2">
                        <input
                            type="text"
                            placeholder={isRecording ? "Recording... (Tap Mic to Stop)" : "Type a message"}
                            className="bg-transparent border-none outline-none flex-1 text-white placeholder-text-muted"
                            value={inputText}
                            onChange={e => setInputText(e.target.value)}
                            onKeyDown={e => e.key === 'Enter' && handleSend()}
                            disabled={isRecording}
                        />
                    </div>
                    {inputText ? (
                        <button onClick={handleSend} className="text-emerald-500 hover:text-emerald-400"><Send size={24} /></button>
                    ) : (
                        <button
                            onClick={isRecording ? stopRecording : startRecording}
                            className={cn("text-text-muted hover:text-white transition-all", isRecording && "text-red-500 animate-pulse")}
                        >
                            <Mic size={24} fill={isRecording ? "currentColor" : "none"} />
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
