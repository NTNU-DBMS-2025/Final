import { createStore } from 'vuex'

console.log('Store: Starting store creation')

// Safely access localStorage
function getFromLocalStorage(key, defaultValue) {
    try {
        const value = localStorage.getItem(key)
        return value || defaultValue
    } catch (error) {
        console.warn('localStorage access failed:', error)
        return defaultValue
    }
}

function parseFromLocalStorage(key, defaultValue) {
    try {
        const value = localStorage.getItem(key)
        return value ? JSON.parse(value) : defaultValue
    } catch (error) {
        console.warn('localStorage parse failed:', error)
        return defaultValue
    }
}

const store = createStore({
    state: {
        user: null,
        token: getFromLocalStorage('token', null),
        roles: parseFromLocalStorage('roles', []),
        notifications: []
    },
    mutations: {
        setUser(state, user) {
            state.user = user
        },
        setToken(state, token) {
            state.token = token
            try {
                if (token) {
                    localStorage.setItem('token', token)
                } else {
                    localStorage.removeItem('token')
                }
            } catch (error) {
                console.warn('localStorage setToken failed:', error)
            }
        },
        setRoles(state, roles) {
            state.roles = roles
            try {
                localStorage.setItem('roles', JSON.stringify(roles))
            } catch (error) {
                console.warn('localStorage setRoles failed:', error)
            }
        },
        clearUser(state) {
            state.user = null
            state.token = null
            state.roles = []
            try {
                localStorage.removeItem('token')
                localStorage.removeItem('roles')
            } catch (error) {
                console.warn('localStorage clearUser failed:', error)
            }
        },
        addNotification(state, notification) {
            state.notifications.push({
                id: Date.now(),
                type: notification.type || 'info',
                message: notification.message,
                duration: notification.duration || 5000
            })
        },
        removeNotification(state, notificationId) {
            state.notifications = state.notifications.filter(n => n.id !== notificationId)
        }
    },
    actions: {
        async login({ commit }, credentials) {
            try {
                // Real API call to backend
                const { login } = await import('../api/auth')
                const response = await login(credentials)

                if (response.data.success) {
                    const userData = response.data.data
                    // Session-based auth - no token needed, server handles sessions
                    commit('setUser', userData)
                    commit('setRoles', [userData.role_name])
                    commit('setToken', 'session-based') // Just to mark as authenticated

                    return userData
                } else {
                    throw new Error(response.data.error || 'Login failed')
                }
            } catch (error) {
                throw error
            }
        },
        async logout({ commit }) {
            try {
                // Real API call to backend
                const { logout } = await import('../api/auth')
                await logout()
            } catch (error) {
                console.error('Logout error:', error)
            } finally {
                commit('clearUser')
            }
        },
        async fetchCurrentUser({ commit }) {
            try {
                // Real API call to backend
                const { getCurrentUser } = await import('../api/auth')
                const response = await getCurrentUser()

                if (response.data.success) {
                    const userData = response.data.data
                    commit('setUser', userData)
                    commit('setRoles', [userData.role_name])
                    commit('setToken', 'session-based')
                    return userData
                } else {
                    commit('clearUser')
                    return null
                }
            } catch (error) {
                commit('clearUser')
                throw error
            }
        },
        showNotification({ commit }, notification) {
            commit('addNotification', notification)
            setTimeout(() => {
                commit('removeNotification', notification.id || Date.now())
            }, notification.duration || 5000)
        }
    },
    getters: {
        isAuthenticated: state => !!state.token,
        hasRole: state => role => state.roles.includes(role),
        hasAnyRole: state => roles => roles.some(role => state.roles.includes(role))
    }
})

console.log('Store: Store created successfully')

export default store 