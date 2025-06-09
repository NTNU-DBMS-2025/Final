import apiClient from './axios'

// ========== INVENTORY REPORTS ==========
export function fetchExpiredInventory() {
  return apiClient.get('/reports/inventory/expired')
}

export function fetchLowStock() {
  return apiClient.get('/reports/inventory/low-stock')
}

export function fetchOutOfStock() {
  return apiClient.get('/reports/inventory/out-of-stock')
}

export function fetchInventoryByCategory() {
  return apiClient.get('/reports/inventory/by-category')
}

export function fetchDaysOfSupply() {
  return apiClient.get('/reports/inventory/days-of-supply')
}

export function fetchIdleInventory() {
  return apiClient.get('/reports/inventory/idle-60d')
}

export function fetchExpiryAlert() {
  return apiClient.get('/reports/inventory/expiry-alert')
}

// ========== SALES REPORTS ==========
export function fetchSales30d() {
  return apiClient.get('/reports/sales/30d')
}

export function fetchFastMovingProducts() {
  return apiClient.get('/reports/sales/fast-moving-top10')
}

export function fetchAvgOrderValueByCustomerType() {
  return apiClient.get('/reports/sales/avg-order-value-by-customer-type')
}

// ========== ORDER REPORTS ==========
export function fetchPendingOrders() {
  return apiClient.get('/reports/orders/pending')
}

// 沒有要用到的
export function fetchUnshippedToday() {
  return apiClient.get('/reports/orders/unshipped-today')
}

// 新增的
export function fetchOrdersArrivedToday() {
  return apiClient.get('/reports/orders/arrived-today')
}

export function fetchOrdersStatus7d() {
  return apiClient.get('/reports/orders/status-7d')
}

export function fetchDelayedShipping() {
  return apiClient.get('/reports/orders/delayed-shipping')
}

export function fetchOrdersToShipThisWeek() {
  return apiClient.get('/reports/orders/to-ship-this-week')
}

export function fetchAvgProcessingTime() {
  return apiClient.get('/reports/orders/processing-time')
}

// ========== SHIPMENT REPORTS ==========
export function fetchShipmentsToday() {
  return apiClient.get('/reports/shipments/today')
}

export function fetchVendorDelays() {
  return apiClient.get('/reports/shipments/vendor-delays')
}

// ========== LOCATION REPORTS ==========
export function fetchLocationsOverCapacity() {
  return apiClient.get('/reports/locations/over-capacity')
}

// ========== SCRAP REPORTS ==========
export function fetchScrapCostMonth() {
  return apiClient.get('/reports/scrap/cost-month')
}

export function fetchProductScrapRate() {
  return apiClient.get('/reports/scrap/product-scrap-rate')
}

// ========== CUSTOMER REPORTS ==========
export function fetchCustomerLastOrder() {
  return apiClient.get('/reports/customers/last-order')
}

// ========== SUPPLIER REPORTS ==========
export function fetchSupplierProductVariants() {
  return apiClient.get('/reports/suppliers/product-variants')
}

// ========== COMBINED SUMMARY REPORTS ==========
export function fetchInventorySummary() {
  return apiClient.get('/reports/summary/inventory')
}

export function fetchOrdersSummary() {
  return apiClient.get('/reports/summary/orders')
}

export function fetchSalesSummary() {
  return apiClient.get('/reports/summary/sales')
}

export function fetchFinancialSummary() {
  return apiClient.get('/reports/summary/financial')
}
