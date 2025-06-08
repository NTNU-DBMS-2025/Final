/**
 * JWT Authentication Utilities
 */

/**
 * Decode JWT token payload
 * @param {string} token - JWT token
 * @returns {object|null} - Decoded payload or null if invalid
 */
export function decodeJWT(token) {
    if (!token) return null

    try {
        const parts = token.split('.')
        if (parts.length !== 3) return null

        const payload = JSON.parse(atob(parts[1]))
        return payload
    } catch (error) {
        console.warn('Failed to decode JWT token:', error)
        return null
    }
}

/**
 * Check if JWT token is expired
 * @param {string} token - JWT token
 * @returns {boolean} - True if expired or invalid
 */
export function isJWTExpired(token) {
    const payload = decodeJWT(token)
    if (!payload || !payload.exp) return true

    const currentTime = Math.floor(Date.now() / 1000)
    return payload.exp < currentTime
}

/**
 * Get token expiration time
 * @param {string} token - JWT token
 * @returns {Date|null} - Expiration date or null if invalid
 */
export function getJWTExpiration(token) {
    const payload = decodeJWT(token)
    if (!payload || !payload.exp) return null

    return new Date(payload.exp * 1000)
}

/**
 * Get time until token expires
 * @param {string} token - JWT token
 * @returns {number} - Milliseconds until expiration, or 0 if expired
 */
export function getTimeUntilExpiration(token) {
    const expirationDate = getJWTExpiration(token)
    if (!expirationDate) return 0

    const timeLeft = expirationDate.getTime() - Date.now()
    return Math.max(0, timeLeft)
}

/**
 * Get user roles from JWT token
 * @param {string} token - JWT token
 * @returns {string[]} - Array of roles
 */
export function getRolesFromToken(token) {
    const payload = decodeJWT(token)
    if (!payload) return []

    // Handle different possible role field names
    return payload.roles || payload.role || payload.role_name ? [payload.role_name] : []
}

/**
 * Get user ID from JWT token
 * @param {string} token - JWT token
 * @returns {string|number|null} - User ID or null
 */
export function getUserIdFromToken(token) {
    const payload = decodeJWT(token)
    return payload?.user_id || payload?.sub || null
}

/**
 * Format token expiration time for display
 * @param {string} token - JWT token
 * @returns {string} - Formatted expiration time
 */
export function formatTokenExpiration(token) {
    const expirationDate = getJWTExpiration(token)
    if (!expirationDate) return 'Invalid token'

    const now = new Date()
    if (expirationDate < now) return 'Expired'

    const timeDiff = expirationDate.getTime() - now.getTime()
    const hours = Math.floor(timeDiff / (1000 * 60 * 60))
    const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60))

    if (hours > 0) {
        return `Expires in ${hours}h ${minutes}m`
    } else {
        return `Expires in ${minutes}m`
    }
}

/**
 * Check if user has required role
 * @param {string} token - JWT token
 * @param {string|string[]} requiredRoles - Required role(s)
 * @returns {boolean} - True if user has required role
 */
export function hasRole(token, requiredRoles) {
    const userRoles = getRolesFromToken(token)
    const required = Array.isArray(requiredRoles) ? requiredRoles : [requiredRoles]

    return required.some(role => userRoles.includes(role))
}

export default {
    decodeJWT,
    isJWTExpired,
    getJWTExpiration,
    getTimeUntilExpiration,
    getRolesFromToken,
    getUserIdFromToken,
    formatTokenExpiration,
    hasRole
} 