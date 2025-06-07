import apiClient from './axios'

// Orders API
export function fetchOrders(params = {}) {
    const { page = 1, per_page = 10, status, search, customer_id, user_id } = params

    const queryParams = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString()
    })

    if (status) queryParams.append('status', status)
    if (search) queryParams.append('search', search)
    if (customer_id) queryParams.append('customer_id', customer_id.toString())
    if (user_id) queryParams.append('user_id', user_id.toString())

    return apiClient.get(`/orders?${queryParams}`)
}

export function fetchOrderStats() {
    return apiClient.get('/orders/stats')
}

export function getOrder(orderId) {
    return apiClient.get(`/orders/${orderId}`)
}

export function createOrder(orderData) {
    return apiClient.post('/orders', orderData)
}

export function updateOrder(orderId, orderData) {
    return apiClient.put(`/orders/${orderId}`, orderData)
}

export function deleteOrder(orderId) {
    return apiClient.delete(`/orders/${orderId}`)
}

// Order Items API
export function getOrderItems(orderId) {
    return apiClient.get(`/orders/${orderId}/items`)
}

export function addOrderItem(orderId, itemData) {
    return apiClient.post(`/orders/${orderId}/items`, itemData)
}

export function updateOrderItem(orderId, itemId, itemData) {
    return apiClient.put(`/orders/${orderId}/items/${itemId}`, itemData)
}

export function deleteOrderItem(orderId, itemId) {
    return apiClient.delete(`/orders/${orderId}/items/${itemId}`)
}

export function updateOrderStatus(orderId, status) {
    return apiClient.patch(`/orders/${orderId}/status`, { status })
}

export function bulkUpdateOrders(updates) {
    return apiClient.post('/orders/bulk-update', { updates })
}

// Compatibility exports
export const ordersAPI = {
    fetchOrders,
    getOrders: fetchOrders, // Alias for compatibility
    fetchOrderStats,
    getOrder,
    createOrder,
    updateOrder,
    deleteOrder,
    getOrderItems,
    addOrderItem,
    updateOrderItem,
    deleteOrderItem,
    updateOrderStatus,
    bulkUpdateOrders
}

export default ordersAPI 