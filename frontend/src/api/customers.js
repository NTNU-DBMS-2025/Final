import apiClient from './axios'

// Customers API
export function fetchCustomers(params = {}) {
    const { page = 1, per_page = 10, search } = params

    const queryParams = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString()
    })

    if (search) queryParams.append('search', search)

    return apiClient.get(`/customers?${queryParams}`)
}

export function fetchCustomerStats() {
    return apiClient.get('/customers/stats')
}

export function getCustomer(customerId) {
    return apiClient.get(`/customers/${customerId}`)
}

export function createCustomer(data) {
    return apiClient.post('/customers', data)
}

export function updateCustomer(customerId, data) {
    return apiClient.put(`/customers/${customerId}`, data)
}

export function deleteCustomer(customerId) {
    return apiClient.delete(`/customers/${customerId}`)
}

export function bulkCreateCustomers(customers) {
    return apiClient.post('/customers/bulk-create', { customers })
}

// Customer orders
export function getCustomerOrders(customerId, params = {}) {
    const { page = 1, per_page = 10 } = params

    const queryParams = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString()
    })

    return apiClient.get(`/customers/${customerId}/orders?${queryParams}`)
}

// Compatibility exports
export const customersAPI = {
    fetchCustomers,
    fetchCustomerStats,
    getCustomer,
    createCustomer,
    updateCustomer,
    deleteCustomer,
    bulkCreateCustomers,
    getCustomerOrders
}

export default customersAPI 