import { createStore } from 'vuex'

console.log('Store: Starting store creation')

// Safely access localStorage
function getFromLocalStorage(key, defaultValue) {
    try {
        const value = localStorage.getItem(key)
        console.log(`Loading ${key} from localStorage:`, value || defaultValue)
        return value || defaultValue
    } catch (error) {
        console.warn('localStorage access failed:', error)
        return defaultValue
    }
}

function parseFromLocalStorage(key, defaultValue) {
    try {
        const value = localStorage.getItem(key)
        const parsed = value ? JSON.parse(value) : defaultValue
        console.log(`Parsing ${key} from localStorage:`, parsed)
        return parsed
    } catch (error) {
        console.warn('localStorage parse failed:', error)
        return defaultValue
    }
}

// JWT Token utilities
function isTokenExpired(token) {
    if (!token) return true

    try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        const currentTime = Date.now() / 1000
        const isExpired = payload.exp < currentTime
        console.log('Token expiration check:', {
            exp: payload.exp,
            now: currentTime,
            isExpired
        })
        return isExpired
    } catch (error) {
        console.warn('Token validation failed:', error)
        return true
    }
}

function getTokenExpiration(token) {
    if (!token) return null

    try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        return new Date(payload.exp * 1000)
    } catch (error) {
        console.warn('Token expiration check failed:', error)
        return null
    }
}

const store = createStore({
    state: {
        user: parseFromLocalStorage('user', null),
        token: getFromLocalStorage('token', null),
        roles: parseFromLocalStorage('roles', []),
        notifications: [],
        isLoading: false
    },
    mutations: {
        setUser(state, user) {
            state.user = user
            try {
                if (user) {
                    localStorage.setItem('user', JSON.stringify(user))
                } else {
                    localStorage.removeItem('user')
                }
            } catch (error) {
                console.warn('localStorage setUser failed:', error)
            }
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
        setLoading(state, loading) {
            state.isLoading = loading
        },
        clearUser(state) {
            state.user = null
            state.token = null
            state.roles = []
            try {
                localStorage.removeItem('token')
                localStorage.removeItem('roles')
                localStorage.removeItem('user')
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
        async login({ commit, dispatch }, credentials) {
            commit('setLoading', true)
            try {
                const { login } = await import('../api/auth')
                const response = await login(credentials)

                if (response.data.success) {
                    const userData = response.data.data
                    const token = response.data.token || response.data.access_token

                    if (!token) {
                        throw new Error('No token received from server')
                    }

                    commit('setUser', userData)
                    commit('setRoles', [userData.role_name])
                    commit('setToken', token)

                    dispatch('showNotification', {
                        type: 'success',
                        message: `歡迎回來，${userData.account}！`
                    })

                    return userData
                } else {
                    throw new Error(response.data.error || 'Login failed')
                }
            } catch (error) {
                const errorMessage = error.response?.data?.error || error.message || 'Login failed'
                dispatch('showNotification', {
                    type: 'error',
                    message: errorMessage
                })
                throw error
            } finally {
                commit('setLoading', false)
            }
        },
        async logout({ commit, dispatch }) {
            try {
                const { logout } = await import('../api/auth')
                await logout()

                dispatch('showNotification', {
                    type: 'success',
                    message: '已成功登出'
                })
            } catch (error) {
                console.error('Logout error:', error)
            } finally {
                commit('clearUser')
            }
        },
        async fetchCurrentUser({ commit, state, dispatch }) {
            // Check if token exists and is valid
            if (!state.token || isTokenExpired(state.token)) {
                commit('clearUser')
                return null
            }

            try {
                const { getCurrentUser } = await import('../api/auth')
                const response = await getCurrentUser()

                if (response.data.success) {
                    const userData = response.data.data
                    commit('setUser', userData)
                    commit('setRoles', [userData.role_name])
                    return userData
                } else {
                    commit('clearUser')
                    return null
                }
            } catch (error) {
                console.error('Failed to fetch current user:', error)
                commit('clearUser')
                return null
            }
        },
        async initializeAuth({ dispatch, state }) {
            console.log('🔄 Initializing authentication...')
            console.log('Initial state:', {
                token: state.token,
                user: state.user,
                roles: state.roles
            })

            // Initialize authentication state on app startup
            if (state.token && !isTokenExpired(state.token)) {
                console.log('✅ Valid token found, fetching current user...')
                await dispatch('fetchCurrentUser')
            } else {
                console.log('❌ No valid token found, logging out...')
                dispatch('logout')
            }

            console.log('🏁 Authentication initialization complete')
        },
        checkTokenExpiration({ state, dispatch }) {
            if (state.token && isTokenExpired(state.token)) {
                dispatch('showNotification', {
                    type: 'warning',
                    message: '登入已過期，請重新登入'
                })
                dispatch('logout')
                return false
            }
            return true
        },
        showNotification({ commit }, notification) {
            const id = Date.now()
            commit('addNotification', { ...notification, id })
            setTimeout(() => {
                commit('removeNotification', id)
            }, notification.duration || 5000)
        }
    },
    getters: {
        isAuthenticated: state => !!state.token && !isTokenExpired(state.token),
        hasRole: state => role => state.roles.includes(role),
        hasAnyRole: state => roles => roles.some(role => state.roles.includes(role)),
        tokenExpiration: state => getTokenExpiration(state.token),
        userDisplayName: state => state.user?.account || 'Unknown User'
    }
})

console.log('Store: Store created successfully')

export default store 