import apiClient from './axios'

// Dashboard API functions
export const fetchDashboardStats = async () => {
    return apiClient.get('/dashboard/stats')
}

export const fetchSalesDashboardStats = async () => {
    return apiClient.get('/dashboard/sales-stats')
}

export const fetchRecentOrders = async (params = {}) => {
    const { page = 1, per_page = 5 } = params
    return apiClient.get('/orders', { params: { page, per_page } })
}

export const fetchLowStockItems = async (params = {}) => {
    const { threshold = 10, limit = 5 } = params
    return apiClient.get('/inventory/low-stock', { params: { threshold, limit } })
} 