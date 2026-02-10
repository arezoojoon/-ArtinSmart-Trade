"use client"

import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Plus, Search, Filter, TrendingUp } from 'lucide-react'

interface Product {
  id: string
  name: string
  description?: string
  category: string
  subcategory?: string
  price_per_unit: number
  currency: string
  min_order_quantity: number
  max_order_quantity?: number
  sku?: string
  demand_score?: number
  margin_recommendation?: number
  ai_tags?: string[]
  is_active: boolean
  is_featured: boolean
  created_at: string
  updated_at: string
}

interface ProductResponse {
  products: Product[]
  total: number
  page: number
  per_page: number
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [showCreateModal, setShowCreateModal] = useState(false)
  
  const categories = [
    'Food & Beverage',
    'FMCG',
    'Electronics',
    'Industrial Goods',
    'Raw Materials',
    'Pharmaceuticals',
    'Cosmetics',
    'Agriculture',
    'Packaging',
    'Building Materials'
  ]

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams({
        skip: '0',
        limit: '50',
        is_active: 'true'
      })
      
      if (searchQuery) params.append('search', searchQuery)
      if (selectedCategory) params.append('category', selectedCategory)
      
      const response = await fetch(`/api/v2/trade/products?${params}`)
      if (!response.ok) throw new Error('Failed to fetch products')
      
      const data: ProductResponse = await response.json()
      setProducts(data.products)
    } catch (error) {
      console.error('Failed to load products')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = () => {
    fetchProducts()
  }

  const getDemandScoreColor = (score?: number) => {
    if (!score) return 'bg-gray-100 text-gray-800'
    if (score >= 8) return 'bg-green-100 text-green-800'
    if (score >= 6) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  const formatPrice = (price: number, currency: string) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency
    }).format(price)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Products</h1>
          <p className="text-gray-600">Manage your product catalog</p>
        </div>
        <Button 
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 hover:bg-blue-700"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Product
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <TrendingUp className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Products</p>
                <p className="text-2xl font-bold text-gray-900">{products.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <TrendingUp className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active</p>
                <p className="text-2xl font-bold text-gray-900">
                  {products.filter(p => p.is_active).length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <TrendingUp className="h-6 w-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Featured</p>
                <p className="text-2xl font-bold text-gray-900">
                  {products.filter(p => p.is_featured).length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <TrendingUp className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Categories</p>
                <p className="text-2xl font-bold text-gray-900">
                  {new Set(products.map(p => p.category)).size}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search products..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Categories</option>
              {categories.map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
            
            <Button onClick={handleSearch} variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              Apply Filters
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Products Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map((product) => (
          <Card key={product.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <CardTitle className="text-lg">{product.name}</CardTitle>
                  <p className="text-sm text-gray-600 mt-1">{product.sku}</p>
                </div>
                <div className="flex gap-2">
                  {product.is_featured && (
                    <Badge variant="secondary">Featured</Badge>
                  )}
                  {product.demand_score && (
                    <Badge className={getDemandScoreColor(product.demand_score)}>
                      Demand: {product.demand_score}/10
                    </Badge>
                  )}
                </div>
              </div>
            </CardHeader>
            
            <CardContent>
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-600">Price</p>
                  <p className="text-xl font-bold text-blue-600">
                    {formatPrice(product.price_per_unit, product.currency)}
                  </p>
                </div>
                
                <div>
                  <p className="text-sm text-gray-600">Category</p>
                  <Badge variant="outline">{product.category}</Badge>
                </div>
                
                <div>
                  <p className="text-sm text-gray-600">Min Order</p>
                  <p className="font-medium">{product.min_order_quantity} units</p>
                </div>
                
                {product.ai_tags && product.ai_tags.length > 0 && (
                  <div>
                    <p className="text-sm text-gray-600 mb-2">AI Tags</p>
                    <div className="flex flex-wrap gap-1">
                      {product.ai_tags.slice(0, 3).map((tag, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                      {product.ai_tags.length > 3 && (
                        <Badge variant="secondary" className="text-xs">
                          +{product.ai_tags.length - 3}
                        </Badge>
                      )}
                    </div>
                  </div>
                )}
                
                {product.margin_recommendation && (
                  <div>
                    <p className="text-sm text-gray-600">AI Margin Recommendation</p>
                    <p className="font-medium text-green-600">
                      {product.margin_recommendation}%
                    </p>
                  </div>
                )}
              </div>
              
              <div className="mt-4 flex gap-2">
                <Button variant="outline" size="sm" className="flex-1">
                  Edit
                </Button>
                <Button variant="outline" size="sm" className="flex-1">
                  View Details
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {products.length === 0 && !loading && (
        <Card>
          <CardContent className="p-12 text-center">
            <div className="text-gray-500">
              <div className="text-6xl mb-4">📦</div>
              <h3 className="text-lg font-medium mb-2">No products found</h3>
              <p className="text-sm mb-4">Get started by adding your first product</p>
              <Button onClick={() => setShowCreateModal(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Add Product
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
