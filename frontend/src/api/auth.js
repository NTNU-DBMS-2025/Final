import apiClient from './axios'

// Mock data for frontend development
const mockUsers = [
    { user_id: 1, account: 'admin', name: 'Administrator', roles: ['Admin'] },
    { user_id: 2, account: 'sales', name: 'Sales Manager', roles: ['Sales'] },
    { user_id: 3, account: 'warehouse', name: 'Warehouse Staff', roles: ['Warehouse'] }
]

export function login(credentials) {
    // For now, use mock login. Replace with real API call later
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const user = mockUsers.find(u => u.account === credentials.account)
            if (user && credentials.password === credentials.account) {
                resolve({
                    data: {
                        success: true,
                        data: {
                            access_token: `mock-jwt-token-${user.account}`,
                            user: user,
                            roles: user.roles
                        }
                    }
                })
            } else {
                reject({
                    response: {
                        data: { error: '無效的帳號或密碼' }
                    }
                })
            }
        }, 1000)
    })

    // Real API call (to be used when backend is ready):
    // return apiClient.post('/auth/login', credentials)
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
    // Mock logout
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                data: {
                    success: true,
                    message: '登出成功'
                }
            })
        }, 500)
    })

    // Real API call:
    // return apiClient.post('/auth/logout')
}

export function getCurrentUser() {
    // Mock current user fetch
    return new Promise((resolve) => {
        const token = localStorage.getItem('token')
        if (token) {
            const mockUser = {
                user_id: 1,
                account: 'admin',
                name: 'Administrator'
            }
            resolve({
                data: {
                    success: true,
                    data: mockUser
                }
            })
        } else {
            resolve({
                data: {
                    success: false,
                    error: 'No token found'
                }
            })
        }
    })

    // Real API call:
    // return apiClient.get('/auth/me')
} 