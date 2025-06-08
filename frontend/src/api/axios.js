import axios from 'axios'
import store from '../store'
import router from '../router'

// Create axios instance
const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api',
    timeout: 10000,
    withCredentials: false, // Switch to token-based auth instead of session cookies
    headers: {
        'Content-Type': 'application/json'
    }
})

// Request interceptor to add Authorization header
apiClient.interceptors.request.use(
    config => {
        console.log('🔄 Axios interceptor running...')

        // Add Authorization header if token exists and is valid
        const token = store.state.token
        console.log('Token from store:', token)
        console.log('Token type:', typeof token)
        console.log('Is session-based?', token === 'session-based')

        if (token && token !== 'session-based') {
            // Check if token is expired before making request
            if (!store.getters.isAuthenticated) {
                console.log('❌ Token expired, logging out...')
                store.dispatch('logout')
                router.push('/login')
                return Promise.reject(new Error('Token expired'))
            }
            console.log('✅ Adding Authorization header:', `Bearer ${token.substring(0, 20)}...`)
            config.headers.Authorization = `Bearer ${token}`
        } else {
            console.log('❌ No valid token found for request')
        }

        console.log('Final request headers:', config.headers)
        return config
    },
    error => {
        console.error('Axios request interceptor error:', error)
        return Promise.reject(error)
    }
)

// Response interceptor to handle errors
apiClient.interceptors.response.use(
    response => {
        return response
    },
    async error => {
        if (error.response) {
            // Handle 401 Unauthorized - token expired or invalid
            if (error.response.status === 401) {
                console.warn('Authentication failed, logging out...')
                await store.dispatch('logout')
                router.push('/login')

                // Don't show error notification for logout redirect
                return Promise.reject(error)
            }

            // Handle 403 Forbidden - insufficient permissions
            if (error.response.status === 403) {
                store.dispatch('showNotification', {
                    type: 'error',
                    message: '您沒有權限執行此操作'
                })
                return Promise.reject(error)
            }

            // Show error notification for other errors
            const errorMessage = error.response.data?.error || error.response.data?.message || '伺服器錯誤'
            store.dispatch('showNotification', {
                type: 'error',
                message: errorMessage
            })
        } else if (error.request) {
            // Network error
            store.dispatch('showNotification', {
                type: 'error',
                message: '網路連線錯誤，請檢查您的網路連線'
            })
        } else if (error.message !== 'Token expired') {
            // Other error (but not our token expiration error)
            store.dispatch('showNotification', {
                type: 'error',
                message: '發生未知錯誤'
            })
        }

        return Promise.reject(error)
    }
)

export default apiClient 