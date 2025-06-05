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
    return new Promise((resolve) => {
        setTimeout(() => {
            const { page = 1, pageSize = 10, search = '' } = params
            let filteredProducts = mockProducts

            if (search) {
                filteredProducts = mockProducts.filter(p =>
                    p.name.includes(search) || p.category.includes(search)
                )
            }

            const startIndex = (page - 1) * pageSize
            const endIndex = startIndex + pageSize
            const paginatedProducts = filteredProducts.slice(startIndex, endIndex)

            resolve({
                data: {
                    success: true,
                    data: {
                        products: paginatedProducts,
                        total: filteredProducts.length,
                        page,
                        pageSize
                    }
                }
            })
        }, 500)
    })

    // Real API call:
    // return apiClient.get('/products', { params })
}

export function getProduct(productId) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const product = mockProducts.find(p => p.product_id === parseInt(productId))
            if (product) {
                resolve({
                    data: {
                        success: true,
                        data: product
                    }
                })
            } else {
                reject({
                    response: {
                        data: { error: '產品不存在' }
                    }
                })
            }
        }, 300)
    })

    // Real API call:
    // return apiClient.get(`/products/${productId}`)
}

export function createProduct(productData) {
    return new Promise((resolve) => {
        setTimeout(() => {
            const newProduct = {
                product_id: mockProducts.length + 1,
                ...productData
            }
            mockProducts.push(newProduct)
            resolve({
                data: {
                    success: true,
                    data: newProduct,
                    message: '產品新增成功'
                }
            })
        }, 800)
    })

    // Real API call:
    // return apiClient.post('/products', productData)
}

export function updateProduct(productId, productData) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const index = mockProducts.findIndex(p => p.product_id === parseInt(productId))
            if (index !== -1) {
                mockProducts[index] = { ...mockProducts[index], ...productData }
                resolve({
                    data: {
                        success: true,
                        data: mockProducts[index],
                        message: '產品更新成功'
                    }
                })
            } else {
                reject({
                    response: {
                        data: { error: '產品不存在' }
                    }
                })
            }
        }, 800)
    })

    // Real API call:
    // return apiClient.put(`/products/${productId}`, productData)
}

export function deleteProduct(productId) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const index = mockProducts.findIndex(p => p.product_id === parseInt(productId))
            if (index !== -1) {
                mockProducts.splice(index, 1)
                resolve({
                    data: {
                        success: true,
                        message: '產品刪除成功'
                    }
                })
            } else {
                reject({
                    response: {
                        data: { error: '產品不存在' }
                    }
                })
            }
        }, 500)
    })

    // Real API call:
    // return apiClient.delete(`/products/${productId}`)
} 