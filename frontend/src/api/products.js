import apiClient from './axios'

// Mock products data
const mockProducts = [
    {
        product_id: 1,
        name: '筆記型電腦',
        category: '電子產品',
        warranty_years: 2,
        image_url: 'https://via.placeholder.com/150'
    },
    {
        product_id: 2,
        name: '智慧型手機',
        category: '電子產品',
        warranty_years: 1,
        image_url: 'https://via.placeholder.com/150'
    },
    {
        product_id: 3,
        name: '辦公椅',
        category: '家具',
        warranty_years: 3,
        image_url: 'https://via.placeholder.com/150'
    },
    {
        product_id: 4,
        name: '桌上型電腦',
        category: '電子產品',
        warranty_years: 2,
        image_url: 'https://via.placeholder.com/150'
    },
    {
        product_id: 5,
        name: '會議桌',
        category: '家具',
        warranty_years: 5,
        image_url: 'https://via.placeholder.com/150'
    }
]

export function fetchProducts(params = {}) {
    // Real API call to backend
    return apiClient.get('/products', { params })
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