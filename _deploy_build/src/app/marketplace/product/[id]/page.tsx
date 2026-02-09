'use client';

import { ArrowLeft, Star, ShieldCheck, Truck, MessageSquare, Download } from 'lucide-react';
import Link from 'next/link';

export default function ProductDetailPage({ params }: { params: { id: string } }) {
    // Mock Data Lookup
    const product = {
        id: params.id,
        name: "Nutella Hazelnut Spread 750g",
        category: "Confectionery",
        price: 3.50,
        moq: "500 Cases",
        origin: "Italy",
        rating: 4.9,
        supplier: "Ferrero SpA",
        description: "Original Nutella hazelnut spread with cocoa. Standard 750g jars, 12 jars per case. Fresh stock with 12 months shelf life. Direct from Italian factory.",
        specs: {
            "Case Size": "12 x 750g",
            "Cases per Pallet": "64",
            "Pallets per Truck": "33",
            "Lead Time": "7 Days",
            "Shelf Life": "12 Months"
        }
    };

    return (
        <div className="p-8 max-w-6xl mx-auto space-y-8">
            <Link href="/marketplace" className="inline-flex items-center gap-2 text-text-muted hover:text-white mb-4">
                <ArrowLeft size={18} /> Back to Marketplace
            </Link>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                {/* Product Image Stage */}
                <div className="space-y-4">
                    <div className="relative aspect-square bg-gray-800 rounded-2xl border border-gray-700 flex items-center justify-center text-gray-500 font-bold text-2xl">
                        {product.name} Image
                        <div className="absolute top-4 left-4 bg-accent text-white px-3 py-1 rounded-full text-xs font-bold">
                            Best Seller
                        </div>
                    </div>
                    <div className="grid grid-cols-4 gap-4">
                        {[1, 2, 3, 4].map(i => (
                            <div key={i} className="aspect-square bg-gray-800 rounded-xl border border-gray-800 cursor-pointer hover:border-accent transition"></div>
                        ))}
                    </div>
                </div>

                {/* Info */}
                <div className="space-y-8">
                    <div>
                        <div className="flex items-center gap-4 mb-2">
                            <span className="text-accent text-sm font-bold tracking-wider uppercase">{product.category}</span>
                            <div className="flex items-center gap-1 text-yellow-500 text-sm">
                                <Star size={14} className="fill-current" /> 4.9 (120 Verified Reviews)
                            </div>
                        </div>
                        <h1 className="text-4xl font-bold text-white mb-4">{product.name}</h1>
                        <p className="text-text-muted leading-relaxed text-lg">{product.description}</p>
                    </div>

                    <div className="bg-card p-6 rounded-2xl border border-gray-800 grid grid-cols-2 gap-6">
                        <div>
                            <p className="text-sm text-text-muted mb-1">Target Price</p>
                            <p className="text-3xl font-mono text-white font-bold">${product.price.toFixed(2)}</p>
                        </div>
                        <div>
                            <p className="text-sm text-text-muted mb-1">Minimum Order</p>
                            <p className="text-3xl font-mono text-white font-bold">{product.moq}</p>
                        </div>
                    </div>

                    {/* Specs */}
                    <div>
                        <h3 className="font-bold text-white text-lg mb-4">Specifications</h3>
                        <div className="grid grid-cols-2 gap-4">
                            {Object.entries(product.specs).map(([key, val]) => (
                                <div key={key} className="flex justify-between border-b border-gray-800 pb-2">
                                    <span className="text-text-muted">{key}</span>
                                    <span className="text-white font-medium">{val}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Supplier Info */}
                    <div className="bg-gray-800/30 p-4 rounded-xl flex items-center gap-4 border border-gray-700">
                        <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center text-black font-bold">F</div>
                        <div className="flex-1">
                            <h4 className="font-bold text-white flex items-center gap-2">
                                {product.supplier} <ShieldCheck size={16} className="text-blue-500" />
                            </h4>
                            <p className="text-xs text-text-muted">Verified Manufacturer • 15 Years on Platform</p>
                        </div>
                        <button className="text-sm text-blue-400 hover:text-blue-300">View Profile</button>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-4">
                        <button className="flex-1 btn-primary bg-accent hover:bg-accent-hover text-white py-4 rounded-xl font-bold flex items-center justify-center gap-2">
                            <MessageSquare size={20} /> Request Quote
                        </button>
                        <button className="px-6 py-4 rounded-xl bg-gray-800 text-white font-bold hover:bg-gray-700 flex items-center gap-2">
                            <Download size={20} /> Spec Sheet
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
