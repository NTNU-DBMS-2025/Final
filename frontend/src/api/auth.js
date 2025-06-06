import apiClient from './axios'

// Mock data for frontend development
const mockUsers = [
    { user_id: 1, account: 'admin', name: 'Administrator', roles: ['Admin'] },
    { user_id: 2, account: 'sales', name: 'Sales Manager', roles: ['Sales'] },
    { user_id: 3, account: 'warehouse', name: 'Warehouse Staff', roles: ['Warehouse'] }
]

export function login(credentials) {
    // Real API call to backend
    return apiClient.post('/auth/login', credentials)
}

export function register(userData) {
    // Mock register for frontend development
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                data: {
                    success: true,
                    message: '註冊成功'
                }
            })
        }, 1000)
    })

    // Real API call:
    // return apiClient.post('/auth/register', userData)
}

export function logout() {
    // Real API call to backend
    return apiClient.post('/auth/logout')
}

export function getCurrentUser() {
    // Real API call to backend
    return apiClient.get('/auth/current-user')
} 