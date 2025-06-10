import apiClient from './axios'

// Real API functions
export function fetchInventory(params = {}) {
    const { page = 1, per_page = 10, low_stock, search, product_id, location_id, zone } = params

    const queryParams = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString()
    })

    if (low_stock) queryParams.append('low_stock', 'true')
    if (search) queryParams.append('search', search)
    if (product_id) queryParams.append('product_id', product_id.toString())
    if (location_id) queryParams.append('location_id', location_id.toString())
    if (zone) queryParams.append('zone', zone)

    return apiClient.get(`/inventory?${queryParams}`)
}

export function fetchInventoryStats() {
    return apiClient.get('/inventory/stats')
}

export function fetchLowStockItems(threshold = 10) {
    return apiClient.get(`/inventory/low-stock?threshold=${threshold}`)
}

export function fetchExpiringItems(days = 30) {
    return apiClient.get(`/inventory/expiring?days=${days}`)
}

export function getInventoryLot(productId, locationId) {
    return apiClient.get(`/inventory/${productId}/${locationId}`)
}

export function createInventoryLot(data) {
    return apiClient.post('/inventory', data)
}

export function updateInventoryLot(productId, locationId, data) {
    return apiClient.put(`/inventory/${productId}/${locationId}`, data)
}

export function deleteInventoryLot(productId, locationId) {
    return apiClient.delete(`/inventory/${productId}/${locationId}`)
}

export function bulkUpdateInventory(updates) {
    return apiClient.post('/inventory/bulk-update', { updates })
}

export function fetchInventoryMovements(productId, params = {}) {
    const { page = 1, per_page = 50, start_date, end_date } = params

    const queryParams = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString()
    })

    if (start_date) queryParams.append('start_date', start_date)
    if (end_date) queryParams.append('end_date', end_date)

    return apiClient.get(`/inventory/movements/${productId}?${queryParams}`)
}

export function createInventoryMovement(data) {
    return apiClient.post('/inventory/movements', data)
}

// Locations API
export function fetchLocations(params = {}) {
    const { page = 1, per_page = 20, zone, search, include_stats } = params

    const queryParams = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString()
    })

    if (zone) queryParams.append('zone', zone)
    if (search) queryParams.append('search', search)
    if (include_stats) queryParams.append('include_stats', 'true')

    return apiClient.get(`/locations?${queryParams}`)
}

export function fetchLocationStats() {
    return apiClient.get('/locations/stats')
}

export function fetchZones(includeStats = false) {
    const params = includeStats ? '?include_stats=true' : ''
    return apiClient.get(`/locations/zones${params}`)
}

export function getLocation(locationId) {
    return apiClient.get(`/locations/${locationId}`)
}

export function createLocation(data) {
    return apiClient.post('/locations', data)
}

export function updateLocation(locationId, data) {
    return apiClient.put(`/locations/${locationId}`, data)
}

export function deleteLocation(locationId) {
    return apiClient.delete(`/locations/${locationId}`)
}

export function bulkCreateLocations(locations) {
    return apiClient.post('/locations/bulk-create', { locations })
}

// Compatibility exports
export const inventoryAPI = {
    fetchInventory,
    fetchInventoryStats,
    fetchLowStockItems,
    fetchExpiringItems,
    getInventoryLot,
    createInventoryLot,
    updateInventoryLot: updateInventoryLot,
    deleteInventoryLot,
    bulkUpdateInventory,
    fetchInventoryMovements,
    createInventoryMovement,
    fetchLocations,
    fetchLocationStats,
    fetchZones,
    getLocation,
    createLocation,
    updateLocation,
    deleteLocation,
    bulkCreateLocations
}

export default inventoryAPI 