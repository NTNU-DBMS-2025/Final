import apiClient from './axios'

// Reports API
export function fetchShipmentsToday() {
  return apiClient.get('/reports/shipments/today')
}
