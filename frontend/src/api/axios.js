import axios from 'axios'
import store from '../store'
import router from '../router'

// Create axios instance
const apiClient = axios.create({
    baseURL: 'http://localhost:5000/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// Request interceptor to add auth token
apiClient.interceptors.request.use(
    config => {
        const token = store.state.token
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// Response interceptor to handle errors
apiClient.interceptors.response.use(
    response => {
        return response
    },
    error => {
        if (error.response) {
            // Handle 401 Unauthorized
            if (error.response.status === 401) {
                store.dispatch('logout')
                router.push('/login')
            }

            // Show error notification
            const errorMessage = error.response.data?.error || error.response.data?.message || '發生錯誤'
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
        } else {
            // Other error
            store.dispatch('showNotification', {
                type: 'error',
                message: '發生未知錯誤'
            })
        }

        return Promise.reject(error)
    }
)

export default apiClient 