'use client';

import { useState, useRef } from 'react';
import { Camera, Upload, X, Check, Loader2, ScanLine } from 'lucide-react';
import Image from 'next/image';

export default function SmartScannerPage() {
    const [image, setImage] = useState<string | null>(null);
    const [isScanning, setIsScanning] = useState(false);
    const [scanResult, setScanResult] = useState<any | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => setImage(e.target?.result as string);
            reader.readAsDataURL(file);
            setScanResult(null);
        }
    };

    const handleScan = async () => {
        if (!image) return;
        setIsScanning(true);
        setScanResult(null);

        try {
            // Convert Base64 (remove prefix)
            const base64Data = image.split(',')[1];

            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: "Analyze this business card image and extract JSON data.",
                    context: "Extract: Name, Company, Role, Phone, Email, Website. If not visible, use null.",
                    image: base64Data
                })
            });

            const data = await response.json();

            if (data.success && data.data.extracted_data) {
                setScanResult({
                    ...data.data.extracted_data,
                    confidence: data.data.confidence
                });
            } else {
                // Fallback if structure is different
                setScanResult({
                    name: "Extraction Failed",
                    company: "Try again",
                    role: "",
                    confidence: 0
                });
            }

        } catch (error) {
            console.error("Scan Error:", error);
            alert("Failed to analyze image");
        } finally {
            setIsScanning(false);
        }
    };

    return (
        <div className="p-4 md:p-8 max-w-2xl mx-auto space-y-6">
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
                <ScanLine className="text-accent" /> Smart Scanner
            </h1>
            <p className="text-text-muted text-sm">Capture business cards or documents to extract data instantly.</p>

            {/* Camera Area */}
            <div className="relative aspect-[4/3] bg-card border-2 border-dashed border-gray-700 rounded-2xl flex flex-col items-center justify-center overflow-hidden">
                {image ? (
                    <>
                        <Image src={image} alt="Scan preview" fill className="object-cover" />
                        <button
                            onClick={() => setImage(null)}
                            className="absolute top-4 right-4 bg-black/60 p-2 rounded-full text-white hover:bg-black/80"
                        >
                            <X size={20} />
                        </button>
                    </>
                ) : (
                    <div className="text-center space-y-4">
                        <div className="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center mx-auto text-accent">
                            <Camera size={32} />
                        </div>
                        <div>
                            <button
                                onClick={() => fileInputRef.current?.click()}
                                className="btn-primary bg-accent hover:bg-accent-hover text-white px-6 py-3 rounded-xl font-bold"
                            >
                                Open Camera / Upload
                            </button>
                            <input
                                type="file"
                                accept="image/*"
                                capture="environment"
                                className="hidden"
                                ref={fileInputRef}
                                onChange={handleFileUpload}
                            />
                        </div>
                    </div>
                )}

                {isScanning && (
                    <div className="absolute inset-0 bg-black/80 flex flex-col items-center justify-center z-10">
                        <Loader2 size={48} className="text-accent animate-spin mb-4" />
                        <p className="text-white font-medium animate-pulse">Analyzing with Gemini Vision...</p>
                    </div>
                )}
            </div>

            {/* Actions */}
            {image && !scanResult && !isScanning && (
                <button
                    onClick={handleScan}
                    className="w-full btn-primary bg-emerald-600 hover:bg-emerald-700 text-white py-4 rounded-xl font-bold text-lg flex items-center justify-center gap-2"
                >
                    <ScanLine size={24} /> Extract Data
                </button>
            )}

            {/* Results Card */}
            {scanResult && (
                <div className="bg-card rounded-xl border border-gray-800 p-6 space-y-4 animate-in slide-in-from-bottom-5 fade-in duration-500">
                    <div className="flex items-center justify-between border-b border-gray-800 pb-4">
                        <h3 className="font-bold text-lg text-white flex items-center gap-2">
                            <Check className="text-emerald-500" /> Lead Detected
                        </h3>
                        <span className="text-xs bg-emerald-500/10 text-emerald-500 px-2 py-1 rounded">
                            {Math.round(scanResult.confidence * 100)}% Confidence
                        </span>
                    </div>

                    <div className="space-y-3">
                        <div className="grid grid-cols-3 gap-2 text-sm">
                            <span className="text-text-muted">Name</span>
                            <span className="col-span-2 text-white font-medium">{scanResult.name}</span>
                        </div>
                        <div className="grid grid-cols-3 gap-2 text-sm">
                            <span className="text-text-muted">Company</span>
                            <span className="col-span-2 text-white font-medium">{scanResult.company}</span>
                        </div>
                        <div className="grid grid-cols-3 gap-2 text-sm">
                            <span className="text-text-muted">Role</span>
                            <span className="col-span-2 text-white font-medium">{scanResult.role}</span>
                        </div>
                        <div className="grid grid-cols-3 gap-2 text-sm">
                            <span className="text-text-muted">Phone</span>
                            <span className="col-span-2 text-white font-medium">{scanResult.phone}</span>
                        </div>
                    </div>

                    <div className="pt-4 flex gap-3">
                        <button className="flex-1 bg-gray-800 hover:bg-gray-700 text-white py-3 rounded-lg font-medium">
                            Edit
                        </button>
                        <button className="flex-1 bg-accent hover:bg-accent-hover text-white py-3 rounded-lg font-bold">
                            Save to CRM
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
