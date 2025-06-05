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
                // Mock login for frontend development
                // This will be replaced with actual API call later
                const mockResponse = await mockLogin(credentials)

                commit('setToken', mockResponse.token)
                commit('setUser', mockResponse.user)
                commit('setRoles', mockResponse.roles)

                return mockResponse
            } catch (error) {
                throw error
            }
        },
        logout({ commit }) {
            commit('clearUser')
        },
        async fetchCurrentUser({ commit, state }) {
            if (!state.token) return null

            try {
                // Mock user fetch for frontend development
                const mockUser = {
                    user_id: 1,
                    account: 'admin',
                    name: 'Administrator'
                }
                commit('setUser', mockUser)
                return mockUser
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

// Mock login function for frontend development
function mockLogin(credentials) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (credentials.account === 'admin' && credentials.password === 'admin') {
                resolve({
                    token: 'mock-jwt-token-admin',
                    user: { user_id: 1, account: 'admin', name: 'Administrator' },
                    roles: ['Admin']
                })
            } else if (credentials.account === 'sales' && credentials.password === 'sales') {
                resolve({
                    token: 'mock-jwt-token-sales',
                    user: { user_id: 2, account: 'sales', name: 'Sales Manager' },
                    roles: ['Sales']
                })
            } else if (credentials.account === 'warehouse' && credentials.password === 'warehouse') {
                resolve({
                    token: 'mock-jwt-token-warehouse',
                    user: { user_id: 3, account: 'warehouse', name: 'Warehouse Staff' },
                    roles: ['Warehouse']
                })
            } else {
                reject(new Error('無效的帳號或密碼'))
            }
        }, 1000)
    })
}

export default store 