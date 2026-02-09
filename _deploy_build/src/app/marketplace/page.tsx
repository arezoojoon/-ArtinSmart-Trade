'use client';

import { useState } from 'react';
import { Search, Filter, ShoppingCart, Tag, Globe, Star } from 'lucide-react';
import Image from 'next/image';
import Link from 'next/link';

const mockProducts = [
    { id: 1, name: "Nutella Hazelnut Spread", category: "Confectionery", price: 3.50, moq: "500 Cases", origin: "Italy", rating: 4.9, image: "/products/nutella.png" },
    { id: 2, name: "Ferrero Rocher T24", category: "Confectionery", price: 8.20, moq: "200 Cases", origin: "Italy", rating: 4.8, image: "/products/ferrero.png" },
    { id: 3, name: "Red Bull Energy Drink", category: "Beverages", price: 1.10, moq: "1000 Cases", origin: "Austria", rating: 4.7, image: "/products/redbull.png" },
    { id: 4, name: "Kinder Bueno Box", category: "Confectionery", price: 18.50, moq: "100 Cases", origin: "Germany", rating: 4.9, image: "/products/kinder.png" },
    { id: 5, name: "Nestle KitKat 4 Finger", category: "Confectionery", price: 0.45, moq: "800 Cases", origin: "UK", rating: 4.6, image: "/products/kitkat.png" },
    { id: 6, name: "Coca Cola 330ml Can", category: "Beverages", price: 0.35, moq: "20 Pallets", origin: "USA", rating: 4.5, image: "/products/coke.png" },
];

export default function MarketplacePage() {
    const [category, setCategory] = useState("All");

    const categories = ["All", "Confectionery", "Beverages", "Snacks", "Dairy", "Personal Care"];

    const filteredProducts = category === "All"
        ? mockProducts
        : mockProducts.filter(p => p.category === category);

    return (
        <div className="p-8 max-w-7xl mx-auto space-y-8">
            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2">B2B Marketplace</h1>
                    <p className="text-text-muted">Source premium FMCG products directly from verified manufacturers.</p>
                </div>
                <div className="flex gap-3">
                    <button className="btn-secondary px-4 py-2 rounded-lg bg-card border border-gray-700 hover:bg-gray-800 flex items-center gap-2">
                        <ShoppingCart size={18} /> My RFQs
                    </button>
                    <button className="btn-primary bg-accent hover:bg-accent-hover text-white px-4 py-2 rounded-lg font-bold">
                        Post Request
                    </button>
                </div>
            </div>

            {/* Search & Filters */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                {/* Sidebar Filter */}
                <div className="bg-card p-6 rounded-2xl border border-gray-800 h-fit space-y-8">
                    <div>
                        <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                            <Filter size={18} className="text-accent" /> Categories
                        </h3>
                        <div className="space-y-2">
                            {categories.map(c => (
                                <button
                                    key={c}
                                    onClick={() => setCategory(c)}
                                    className={`w-full text-left px-3 py-2 rounded-lg text-sm transition ${category === c ? 'bg-accent/10 text-accent font-medium' : 'text-text-muted hover:bg-gray-800'}`}
                                >
                                    {c}
                                </button>
                            ))}
                        </div>
                    </div>

                    <div>
                        <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                            <Globe size={18} className="text-accent" /> Origin
                        </h3>
                        <div className="space-y-2 text-sm text-text-muted">
                            <label className="flex items-center gap-2 cursor-pointer hover:text-white">
                                <input type="checkbox" className="rounded border-gray-700 bg-background" /> Italy
                            </label>
                            <label className="flex items-center gap-2 cursor-pointer hover:text-white">
                                <input type="checkbox" className="rounded border-gray-700 bg-background" /> Germany
                            </label>
                            <label className="flex items-center gap-2 cursor-pointer hover:text-white">
                                <input type="checkbox" className="rounded border-gray-700 bg-background" /> Turkey
                            </label>
                            <label className="flex items-center gap-2 cursor-pointer hover:text-white">
                                <input type="checkbox" className="rounded border-gray-700 bg-background" /> USA
                            </label>
                        </div>
                    </div>
                </div>

                {/* Product Grid */}
                <div className="lg:col-span-3 space-y-6">
                    {/* Search Bar */}
                    <div className="relative">
                        <Search className="absolute left-4 top-3.5 text-text-muted" size={20} />
                        <input
                            type="text"
                            placeholder="Search products, brands, or suppliers..."
                            className="w-full bg-card border border-gray-800 rounded-xl pl-12 pr-4 py-3 text-white focus:border-accent outline-none"
                        />
                    </div>

                    {/* Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                        {filteredProducts.map(product => (
                            <Link href={`/marketplace/product/${product.id}`} key={product.id} className="group">
                                <div className="bg-card rounded-2xl border border-gray-800 overflow-hidden hover:border-accent/50 transition duration-300">
                                    <div className="h-48 bg-gray-900 relative">
                                        {/* Placeholder Image since we don't have real assets yet */}
                                        <div className="w-full h-full flex items-center justify-center text-gray-700 bg-gray-800">
                                            {product.name}
                                        </div>
                                        <div className="absolute top-3 right-3 bg-black/60 backdrop-blur-md px-2 py-1 rounded text-xs font-bold text-white flex items-center gap-1">
                                            <Star size={12} className="text-yellow-400 fill-yellow-400" /> {product.rating}
                                        </div>
                                    </div>
                                    <div className="p-5 space-y-4">
                                        <div>
                                            <div className="text-xs text-text-muted mb-1 flex items-center gap-2">
                                                <span>{product.category}</span>
                                                <span className="w-1 h-1 rounded-full bg-gray-600"></span>
                                                <span>{product.origin}</span>
                                            </div>
                                            <h3 className="font-bold text-lg text-white group-hover:text-accent transition">{product.name}</h3>
                                        </div>

                                        <div className="flex justify-between items-end">
                                            <div>
                                                <p className="text-xs text-text-muted">Target Price</p>
                                                <p className="text-xl font-mono text-white">${product.price.toFixed(2)}</p>
                                            </div>
                                            <div className="text-right">
                                                <p className="text-xs text-text-muted">MOQ</p>
                                                <p className="font-medium text-white">{product.moq}</p>
                                            </div>
                                        </div>

                                        <button className="w-full py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-sm transition">
                                            Add to Quote
                                        </button>
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
