import apiClient from './axios'

// Mock products data
const mockProducts = [
    {
        product_id: 1,
        name: 'Laptop Dell XPS 13',
        category: 'Electronics',
        warranty_years: 3,
        image_url: 'https://example.com/dell-xps13.jpg'
    },
    {
        product_id: 2,
        name: 'Office Chair Ergonomic',
        category: 'Furniture',
        warranty_years: 2,
        image_url: 'https://example.com/office-chair.jpg'
    },
    {
        product_id: 3,
        name: 'Wireless Mouse Logitech',
        category: 'Electronics',
        warranty_years: 1,
        image_url: 'https://example.com/mouse.jpg'
    },
    {
        product_id: 4,
        name: 'Monitor 24 inch LG',
        category: 'Electronics',
        warranty_years: 2,
        image_url: 'https://example.com/monitor.jpg'
    },
    {
        product_id: 5,
        name: 'iPhone 15 Pro',
        category: 'Electronics',
        warranty_years: 1,
        image_url: 'https://example.com/iphone15.jpg'
    },
    {
        product_id: 6,
        name: 'MacBook Pro M3',
        category: 'Electronics',
        warranty_years: 3,
        image_url: 'https://example.com/macbook.jpg'
    },
    {
        product_id: 7,
        name: 'Standing Desk',
        category: 'Furniture',
        warranty_years: 5,
        image_url: 'https://example.com/standing-desk.jpg'
    },
    {
        product_id: 8,
        name: 'Wireless Keyboard',
        category: 'Electronics',
        warranty_years: 2,
        image_url: 'https://example.com/keyboard.jpg'
    },
    {
        product_id: 9,
        name: 'Conference Table',
        category: 'Furniture',
        warranty_years: 10,
        image_url: 'https://example.com/conference-table.jpg'
    },
    {
        product_id: 10,
        name: 'Printer HP LaserJet',
        category: 'Electronics',
        warranty_years: 2,
        image_url: 'https://example.com/printer.jpg'
    },
    {
        product_id: 11,
        name: 'Gaming Chair RGB',
        category: 'Furniture',
        warranty_years: 3,
        image_url: 'https://example.com/gaming-chair.jpg'
    },
    {
        product_id: 12,
        name: 'Tablet iPad Pro',
        category: 'Electronics',
        warranty_years: 1,
        image_url: 'https://example.com/ipad.jpg'
    },
    {
        product_id: 13,
        name: 'Webcam HD 1080p',
        category: 'Electronics',
        warranty_years: 2,
        image_url: 'https://example.com/webcam.jpg'
    },
    {
        product_id: 14,
        name: 'Desk Lamp LED',
        category: 'Furniture',
        warranty_years: 3,
        image_url: 'https://example.com/desk-lamp.jpg'
    },
    {
        product_id: 15,
        name: 'External Hard Drive 2TB',
        category: 'Electronics',
        warranty_years: 2,
        image_url: 'https://example.com/hard-drive.jpg'
    },
    {
        product_id: 16,
        name: 'Office Whiteboard',
        category: 'Furniture',
        warranty_years: 5,
        image_url: 'https://example.com/whiteboard.jpg'
    },
    {
        product_id: 17,
        name: 'Bluetooth Speaker',
        category: 'Electronics',
        warranty_years: 1,
        image_url: 'https://example.com/speaker.jpg'
    },
    {
        product_id: 18,
        name: 'File Cabinet Metal',
        category: 'Furniture',
        warranty_years: 10,
        image_url: 'https://example.com/file-cabinet.jpg'
    },
    {
        product_id: 19,
        name: 'Graphics Card RTX 4080',
        category: 'Electronics',
        warranty_years: 3,
        image_url: 'https://example.com/graphics-card.jpg'
    },
    {
        product_id: 20,
        name: 'Ergonomic Footrest',
        category: 'Furniture',
        warranty_years: 2,
        image_url: 'https://example.com/footrest.jpg'
    },
    {
        product_id: 21,
        name: 'Smart Watch Apple',
        category: 'Electronics',
        warranty_years: 1,
        image_url: 'https://example.com/apple-watch.jpg'
    },
    {
        product_id: 22,
        name: 'Bookshelf Oak Wood',
        category: 'Furniture',
        warranty_years: 15,
        image_url: 'https://example.com/bookshelf.jpg'
    }
]

export function fetchProducts(params = {}) {
    // Try real API call to backend
    return apiClient.get('/products', { params }).catch(error => {
        // Fallback to mock data if backend is not available
        console.warn('Backend not available, using mock data:', error.message)

        const page = params.page || 1
        const per_page = params.per_page || 10
        const search = params.search || ''

        // Filter mock data based on search
        let filteredProducts = mockProducts
        if (search) {
            filteredProducts = mockProducts.filter(product =>
                product.name.toLowerCase().includes(search.toLowerCase()) ||
                product.category.toLowerCase().includes(search.toLowerCase())
            )
        }

        // Simulate pagination
        const total = filteredProducts.length
        const totalPages = Math.ceil(total / per_page)
        const startIndex = (page - 1) * per_page
        const endIndex = startIndex + per_page
        const paginatedProducts = filteredProducts.slice(startIndex, endIndex)

        // Return mock response in the same format as backend
        return Promise.resolve({
            data: {
                success: true,
                data: paginatedProducts,
                pagination: {
                    page: page,
                    pages: totalPages,
                    per_page: per_page,
                    total: total
                }
            }
        })
    })
}

export function getProduct(productId) {
    // Real API call to backend
    return apiClient.get(`/products/${productId}`)
}

export function createProduct(productData) {
    // Real API call to backend
    return apiClient.post('/products', productData)
}

export function updateProduct(productId, productData) {
    // Real API call to backend
    return apiClient.put(`/products/${productId}`, productData)
}

export function deleteProduct(productId) {
    // Real API call to backend
    return apiClient.delete(`/products/${productId}`)
} 