import apiClient from './axios'

export function fetchSuppliers(params = {}) {
    // Real API call to backend
    return apiClient.get('/suppliers', { params })
}

export function getSupplier(supplierId) {
    // Real API call to backend
    return apiClient.get(`/suppliers/${supplierId}`)
}

export function createSupplier(supplierData) {
    // Real API call to backend
    return apiClient.post('/suppliers', supplierData)
}

export function updateSupplier(supplierId, supplierData) {
    // Real API call to backend
    return apiClient.put(`/suppliers/${supplierId}`, supplierData)
}

export function deleteSupplier(supplierId) {
    // Real API call to backend
    return apiClient.delete(`/suppliers/${supplierId}`)
}

export function getSupplierProducts(supplierId) {
    // Real API call to backend
    return apiClient.get(`/suppliers/${supplierId}/products`)
}

export function addProductToSupplier(supplierId, productId) {
    // Real API call to backend
    return apiClient.post(`/suppliers/${supplierId}/products`, { product_id: productId })
}

export function removeProductFromSupplier(supplierId, productId) {
    // Real API call to backend
    return apiClient.delete(`/suppliers/${supplierId}/products/${productId}`)
} 