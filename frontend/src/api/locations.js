import apiClient from './axios'

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

// Location inventory
export function getLocationInventory(locationId, params = {}) {
    const { page = 1, per_page = 10 } = params

    const queryParams = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString()
    })

    return apiClient.get(`/locations/${locationId}/inventory?${queryParams}`)
}

// Compatibility exports
export const locationsAPI = {
    fetchLocations,
    fetchLocationStats,
    fetchZones,
    getLocation,
    createLocation,
    updateLocation,
    deleteLocation,
    bulkCreateLocations,
    getLocationInventory
}

export default locationsAPI 