// src/api/reports.js
import apiClient from './axios'

export function fetchShipmentsToday() {
  return apiClient.get('/reports/shipments/today')
}
