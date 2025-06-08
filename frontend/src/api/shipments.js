import apiClient from './axios'

// Shipments API
export function fetchShipments(params = {}) {
    const { page = 1, per_page = 10, status, search, order_id, vendor_id } = params

    const queryParams = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString()
    })

    if (status) queryParams.append('status', status)
    if (search) queryParams.append('search', search)
    if (order_id) queryParams.append('order_id', order_id.toString())
    if (vendor_id) queryParams.append('vendor_id', vendor_id.toString())

    return apiClient.get(`/shipments?${queryParams}`)
}

export function fetchShipmentStats() {
    return apiClient.get('/shipments/stats')
}

export function getShipment(shipmentId) {
    return apiClient.get(`/shipments/${shipmentId}`)
}

export function createShipment(data) {
    return apiClient.post('/shipments', data)
}

export function updateShipment(shipmentId, data) {
    return apiClient.put(`/shipments/${shipmentId}`, data)
}

export function deleteShipment(shipmentId) {
    return apiClient.delete(`/shipments/${shipmentId}`)
}

export function updateShipmentStatus(shipmentId, status) {
    return apiClient.patch(`/shipments/${shipmentId}/status`, { status })
}

export function bulkUpdateShipments(updates) {
    return apiClient.post('/shipments/bulk-update', { updates })
}

// Shipping Vendors API
export function fetchShippingVendors(params = {}) {
    const { page = 1, per_page = 20, search, mode } = params

    const queryParams = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString()
    })

    if (search) queryParams.append('search', search)
    if (mode) queryParams.append('mode', mode)

    return apiClient.get(`/shipments/vendors?${queryParams}`)
}

export function getShippingVendor(vendorId) {
    return apiClient.get(`/shipments/vendors/${vendorId}`)
}

export function createShippingVendor(data) {
    return apiClient.post('/shipments/vendors', data)
}

export function updateShippingVendor(vendorId, data) {
    return apiClient.put(`/shipments/vendors/${vendorId}`, data)
}

export function deleteShippingVendor(vendorId) {
    return apiClient.delete(`/shipments/vendors/${vendorId}`)
}

// Compatibility exports
export const shipmentsAPI = {
    fetchShipments,
    fetchShipmentStats,
    getShipment,
    createShipment,
    updateShipment,
    deleteShipment,
    updateShipmentStatus,
    bulkUpdateShipments,
    fetchShippingVendors,
    getShippingVendor,
    createShippingVendor,
    updateShippingVendor,
    deleteShippingVendor
}

export default shipmentsAPI
