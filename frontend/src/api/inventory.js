import apiClient from './axios'

// Mock inventory data
const mockInventory = [
    {
        product_id: 1,
        product_name: '筆記型電腦',
        location_id: 1,
        location_name: 'A-01-01',
        zone: 'A區',
        shelf: '01-01',
        quantity: 45,
        expiry_date: '2025-12-31'
    },
    {
        product_id: 2,
        product_name: '智慧型手機',
        location_id: 2,
        location_name: 'A-01-02',
        zone: 'A區',
        shelf: '01-02',
        quantity: 8,
        expiry_date: '2024-06-30'
    },
    {
        product_id: 3,
        product_name: '辦公椅',
        location_id: 3,
        location_name: 'B-02-01',
        zone: 'B區',
        shelf: '02-01',
        quantity: 120,
        expiry_date: null
    }
]

const mockLocations = [
    { location_id: 1, zone: 'A區', shelf: '01-01' },
    { location_id: 2, zone: 'A區', shelf: '01-02' },
    { location_id: 3, zone: 'B區', shelf: '02-01' },
    { location_id: 4, zone: 'B區', shelf: '02-02' },
    { location_id: 5, zone: 'C區', shelf: '03-01' }
]

export function fetchInventory(params = {}) {
    return new Promise((resolve) => {
        setTimeout(() => {
            const { page = 1, pageSize = 10, lowStock = false } = params
            let filteredInventory = mockInventory

            if (lowStock) {
                filteredInventory = mockInventory.filter(item => item.quantity < 20)
            }

            const startIndex = (page - 1) * pageSize
            const endIndex = startIndex + pageSize
            const paginatedInventory = filteredInventory.slice(startIndex, endIndex)

            resolve({
                data: {
                    success: true,
                    data: {
                        inventory: paginatedInventory,
                        total: filteredInventory.length,
                        page,
                        pageSize
                    }
                }
            })
        }, 500)
    })
}

export function updateInventory(productId, locationId, updateData) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const index = mockInventory.findIndex(
                item => item.product_id === parseInt(productId) && item.location_id === parseInt(locationId)
            )
            if (index !== -1) {
                mockInventory[index] = { ...mockInventory[index], ...updateData }
                resolve({
                    data: {
                        success: true,
                        data: mockInventory[index],
                        message: '庫存更新成功'
                    }
                })
            } else {
                reject({
                    response: {
                        data: { error: '庫存記錄不存在' }
                    }
                })
            }
        }, 500)
    })
}

export function fetchLocations() {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                data: {
                    success: true,
                    data: mockLocations
                }
            })
        }, 300)
    })
}

// Export as inventoryAPI for compatibility
export const inventoryAPI = {
    fetchInventory,
    updateInventory,
    fetchLocations
} 