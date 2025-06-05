import apiClient from './axios'

// Mock orders data
const mockOrders = [
    {
        order_id: 1,
        order_date: '2024-01-15T10:30:00',
        status: '待出貨',
        ship_to: '台北市信義區信義路五段7號',
        customer_id: 1,
        customer_name: '王小明',
        user_id: 2,
        user_name: 'Sales Manager',
        items: [
            { order_item_id: 1, product_id: 1, product_name: '筆記型電腦', quantity: 2 },
            { order_item_id: 2, product_id: 2, product_name: '智慧型手機', quantity: 1 }
        ]
    },
    {
        order_id: 2,
        order_date: '2024-01-14T14:20:00',
        status: '已出貨',
        ship_to: '新北市板橋區中山路一段152號',
        customer_id: 2,
        customer_name: '李小華',
        user_id: 2,
        user_name: 'Sales Manager',
        items: [
            { order_item_id: 3, product_id: 3, product_name: '辦公椅', quantity: 4 }
        ]
    },
    {
        order_id: 3,
        order_date: '2024-01-13T09:15:00',
        status: '處理中',
        ship_to: '桃園市中壢區中大路300號',
        customer_id: 3,
        customer_name: '張小美',
        user_id: 2,
        user_name: 'Sales Manager',
        items: [
            { order_item_id: 4, product_id: 4, product_name: '桌上型電腦', quantity: 1 },
            { order_item_id: 5, product_id: 5, product_name: '會議桌', quantity: 2 }
        ]
    }
]

export function fetchOrders(params = {}) {
    return new Promise((resolve) => {
        setTimeout(() => {
            const { page = 1, pageSize = 10, status = '', search = '' } = params
            let filteredOrders = mockOrders

            if (status) {
                filteredOrders = filteredOrders.filter(o => o.status === status)
            }

            if (search) {
                filteredOrders = filteredOrders.filter(o =>
                    o.customer_name.includes(search) ||
                    o.ship_to.includes(search) ||
                    o.order_id.toString().includes(search)
                )
            }

            const startIndex = (page - 1) * pageSize
            const endIndex = startIndex + pageSize
            const paginatedOrders = filteredOrders.slice(startIndex, endIndex)

            resolve({
                data: {
                    success: true,
                    data: {
                        orders: paginatedOrders,
                        total: filteredOrders.length,
                        page,
                        pageSize
                    }
                }
            })
        }, 500)
    })

    // Real API call:
    // return apiClient.get('/orders', { params })
}

export function getOrder(orderId) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const order = mockOrders.find(o => o.order_id === parseInt(orderId))
            if (order) {
                resolve({
                    data: {
                        success: true,
                        data: order
                    }
                })
            } else {
                reject({
                    response: {
                        data: { error: '訂單不存在' }
                    }
                })
            }
        }, 300)
    })

    // Real API call:
    // return apiClient.get(`/orders/${orderId}`)
}

export function createOrder(orderData) {
    return new Promise((resolve) => {
        setTimeout(() => {
            const newOrder = {
                order_id: mockOrders.length + 1,
                order_date: new Date().toISOString(),
                status: '處理中',
                ...orderData
            }
            mockOrders.push(newOrder)
            resolve({
                data: {
                    success: true,
                    data: newOrder,
                    message: '訂單新增成功'
                }
            })
        }, 800)
    })

    // Real API call:
    // return apiClient.post('/orders', orderData)
}

export function updateOrder(orderId, orderData) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const index = mockOrders.findIndex(o => o.order_id === parseInt(orderId))
            if (index !== -1) {
                mockOrders[index] = { ...mockOrders[index], ...orderData }
                resolve({
                    data: {
                        success: true,
                        data: mockOrders[index],
                        message: '訂單更新成功'
                    }
                })
            } else {
                reject({
                    response: {
                        data: { error: '訂單不存在' }
                    }
                })
            }
        }, 800)
    })

    // Real API call:
    // return apiClient.put(`/orders/${orderId}`, orderData)
}

export function deleteOrder(orderId) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const index = mockOrders.findIndex(o => o.order_id === parseInt(orderId))
            if (index !== -1) {
                mockOrders.splice(index, 1)
                resolve({
                    data: {
                        success: true,
                        message: '訂單刪除成功'
                    }
                })
            } else {
                reject({
                    response: {
                        data: { error: '訂單不存在' }
                    }
                })
            }
        }, 500)
    })

    // Real API call:
    // return apiClient.delete(`/orders/${orderId}`)
}

export function getOrderItems(orderId) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const order = mockOrders.find(o => o.order_id === parseInt(orderId))
            if (order) {
                resolve({
                    data: {
                        success: true,
                        data: order.items
                    }
                })
            } else {
                reject({
                    response: {
                        data: { error: '訂單不存在' }
                    }
                })
            }
        }, 300)
    })

    // Real API call:
    // return apiClient.get(`/orders/${orderId}/items`)
}

// Export as ordersAPI for compatibility
export const ordersAPI = {
    fetchOrders,
    getOrder,
    createOrder,
    updateOrder,
    deleteOrder,
    getOrderItems
} 