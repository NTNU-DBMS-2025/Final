import apiClient from './axios'

// Users API
export function fetchUsers(params = {}) {
    const { page = 1, per_page = 10, search, role_id } = params

    const queryParams = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString()
    })

    if (search) queryParams.append('search', search)
    if (role_id) queryParams.append('role_id', role_id.toString())

    return apiClient.get(`/users?${queryParams}`)
}

export function fetchUserStats() {
    return apiClient.get('/users/stats')
}

export function getUser(userId) {
    return apiClient.get(`/users/${userId}`)
}

export function createUser(data) {
    return apiClient.post('/users', data)
}

export function updateUser(userId, data) {
    return apiClient.put(`/users/${userId}`, data)
}

export function deleteUser(userId) {
    return apiClient.delete(`/users/${userId}`)
}

export function changePassword(userId, passwordData) {
    return apiClient.put(`/users/${userId}/change-password`, passwordData)
}

export function resetPassword(userId) {
    return apiClient.put(`/users/${userId}/reset-password`)
}

// User Roles API
export function getUserRoles(userId) {
    return apiClient.get(`/users/${userId}/roles`)
}

export function assignRole(userId, roleId) {
    return apiClient.post(`/users/${userId}/roles`, { role_id: roleId })
}

export function removeRole(userId, roleId) {
    return apiClient.delete(`/users/${userId}/roles/${roleId}`)
}

// Roles API
export function fetchRoles(params = {}) {
    const { page = 1, per_page = 20, search } = params

    const queryParams = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString()
    })

    if (search) queryParams.append('search', search)

    return apiClient.get(`/users/roles?${queryParams}`)
}

export function getRole(roleId) {
    return apiClient.get(`/users/roles/${roleId}`)
}

export function createRole(data) {
    return apiClient.post('/users/roles', data)
}

export function updateRole(roleId, data) {
    return apiClient.put(`/users/roles/${roleId}`, data)
}

export function deleteRole(roleId) {
    return apiClient.delete(`/users/roles/${roleId}`)
}

// Compatibility exports
export const usersAPI = {
    fetchUsers,
    fetchUserStats,
    getUser,
    createUser,
    updateUser,
    deleteUser,
    changePassword,
    resetPassword,
    getUserRoles,
    assignRole,
    removeRole,
    fetchRoles,
    getRole,
    createRole,
    updateRole,
    deleteRole
}

export default usersAPI 