// Import all API modules
import * as auth from './auth'
import * as users from './users'
import * as products from './products'
import * as suppliers from './suppliers'
import * as customers from './customers'
import * as orders from './orders'
import * as shipments from './shipments'
import * as locations from './locations'
import * as inventory from './inventory'
import * as scrap from './scrap'
import * as dashboard from './dashboard'

// Create unified API object
const api = {
    auth,
    users,
    products,
    suppliers,
    customers,
    orders,
    shipments,
    locations,
    inventory,
    scrap,
    dashboard
}

// Vue plugin to install API globally
export default {
    install(app) {
        app.config.globalProperties.$api = api
        app.provide('api', api)
    }
}

// Export individual modules for direct import
export {
    auth,
    users,
    products,
    suppliers,
    customers,
    orders,
    shipments,
    locations,
    inventory,
    scrap,
    dashboard
}

// Export unified API object
export { api } 