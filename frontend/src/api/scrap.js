import apiClient from './axios'

// Scrap API
export function fetchScrapRecords(params = {}) {
    const { page = 1, per_page = 10, search, product_id, location_id, date_from, date_to, reason } = params

    const queryParams = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString()
    })

    if (search) queryParams.append('search', search)
    if (product_id) queryParams.append('product_id', product_id.toString())
    if (location_id) queryParams.append('location_id', location_id.toString())
    if (date_from) queryParams.append('date_from', date_from)
    if (date_to) queryParams.append('date_to', date_to)
    if (reason) queryParams.append('reason', reason)

    return apiClient.get(`/scrap?${queryParams}`)
}

export function fetchScrapStats() {
    return apiClient.get('/scrap/stats')
}

export function fetchScrapAnalytics(params = {}) {
    const { period = 'month', group_by = 'product' } = params

    const queryParams = new URLSearchParams({
        period,
        group_by
    })

    return apiClient.get(`/scrap/analytics?${queryParams}`)
}

export function getScrapRecord(scrapId) {
    return apiClient.get(`/scrap/${scrapId}`)
}

export function createScrapRecord(data) {
    return apiClient.post('/scrap', data)
}

export function updateScrapRecord(scrapId, data) {
    return apiClient.put(`/scrap/${scrapId}`, data)
}

export function deleteScrapRecord(scrapId) {
    return apiClient.delete(`/scrap/${scrapId}`)
}

export function bulkCreateScrapRecords(records) {
    return apiClient.post('/scrap/bulk-create', { records })
}

// Scrap reasons API
export function fetchScrapReasons() {
    return apiClient.get('/scrap/reasons')
}

// Compatibility exports
export const scrapAPI = {
    fetchScrapRecords,
    fetchScrapStats,
    fetchScrapAnalytics,
    getScrapRecord,
    createScrapRecord,
    updateScrapRecord,
    deleteScrapRecord,
    bulkCreateScrapRecords,
    fetchScrapReasons
}

export default scrapAPI 