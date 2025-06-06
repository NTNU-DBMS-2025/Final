import { createStore } from 'vuex'

const store = createStore({
    state: {
        user: null,
        token: localStorage.getItem('token') || null,
        roles: JSON.parse(localStorage.getItem('roles') || '[]'),
        notifications: []
    },
    mutations: {
        setUser(state, user) {
            state.user = user
        },
        setToken(state, token) {
            state.token = token
            if (token) {
                localStorage.setItem('token', token)
            } else {
                localStorage.removeItem('token')
            }
        },
        setRoles(state, roles) {
            state.roles = roles
            localStorage.setItem('roles', JSON.stringify(roles))
        },
        clearUser(state) {
            state.user = null
            state.token = null
            state.roles = []
            localStorage.removeItem('token')
            localStorage.removeItem('roles')
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

export default store 