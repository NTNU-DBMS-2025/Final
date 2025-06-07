import apiClient from './axios'

export function login(credentials) {
    return apiClient.post('/auth/login', credentials)
}

export function register(userData) {
    return apiClient.post('/auth/register', userData)
}

export function logout() {
    return apiClient.post('/auth/logout')
}

export function getCurrentUser() {
    return apiClient.get('/auth/current-user')
}

// Compatibility exports
export const authAPI = {
    login,
    register,
    logout,
    getCurrentUser
}

export default authAPI 