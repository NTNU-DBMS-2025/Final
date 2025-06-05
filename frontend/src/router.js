import { createRouter, createWebHistory } from 'vue-router'
import store from './store'

// Import Views
import Login from './views/Login.vue'
import AdminDashboard from './views/AdminDashboard.vue'
import SalesDashboard from './views/SalesDashboard.vue'
import WarehouseDashboard from './views/WarehouseDashboard.vue'
import Products from './views/Products.vue'
import Suppliers from './views/Suppliers.vue'
import Customers from './views/Customers.vue'
import Orders from './views/Orders.vue'
import Shipments from './views/Shipments.vue'
import Inventory from './views/Inventory.vue'
import Locations from './views/Locations.vue'
import Scrap from './views/Scrap.vue'
import Reports from './views/Reports.vue'

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { requiresAuth: false }
    },
    {
        path: '/admin',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { requiresAuth: true, allowedRoles: ['Admin'] }
    },
    {
        path: '/sales',
        name: 'SalesDashboard',
        component: SalesDashboard,
        meta: { requiresAuth: true, allowedRoles: ['Sales'] }
    },
    {
        path: '/warehouse',
        name: 'WarehouseDashboard',
        component: WarehouseDashboard,
        meta: { requiresAuth: true, allowedRoles: ['Warehouse'] }
    },
    {
        path: '/products',
        name: 'Products',
        component: Products,
        meta: { requiresAuth: true, allowedRoles: ['Admin', 'Warehouse'] }
    },
    {
        path: '/suppliers',
        name: 'Suppliers',
        component: Suppliers,
        meta: { requiresAuth: true, allowedRoles: ['Admin', 'Warehouse'] }
    },
    {
        path: '/customers',
        name: 'Customers',
        component: Customers,
        meta: { requiresAuth: true, allowedRoles: ['Admin', 'Sales'] }
    },
    {
        path: '/orders',
        name: 'Orders',
        component: Orders,
        meta: { requiresAuth: true, allowedRoles: ['Admin', 'Sales'] }
    },
    {
        path: '/shipments',
        name: 'Shipments',
        component: Shipments,
        meta: { requiresAuth: true, allowedRoles: ['Admin', 'Sales', 'Shipping_Vendor'] }
    },
    {
        path: '/inventory',
        name: 'Inventory',
        component: Inventory,
        meta: { requiresAuth: true, allowedRoles: ['Admin', 'Warehouse'] }
    },
    {
        path: '/locations',
        name: 'Locations',
        component: Locations,
        meta: { requiresAuth: true, allowedRoles: ['Admin', 'Warehouse'] }
    },
    {
        path: '/scrap',
        name: 'Scrap',
        component: Scrap,
        meta: { requiresAuth: true, allowedRoles: ['Admin', 'Warehouse'] }
    },
    {
        path: '/reports',
        name: 'Reports',
        component: Reports,
        meta: { requiresAuth: true, allowedRoles: ['Admin', 'Sales', 'Warehouse'] }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Route guards
router.beforeEach((to, from, next) => {
    const token = store.state.token
    const userRoles = store.state.roles

    // If route doesn't require auth, allow access
    if (!to.meta.requiresAuth) {
        // If user is already logged in and trying to access login, redirect to appropriate dashboard
        if (token && to.name === 'Login') {
            if (userRoles.includes('Admin')) {
                return next({ name: 'AdminDashboard' })
            } else if (userRoles.includes('Sales')) {
                return next({ name: 'SalesDashboard' })
            } else if (userRoles.includes('Warehouse')) {
                return next({ name: 'WarehouseDashboard' })
            }
        }
        return next()
    }

    // If route requires auth but user is not logged in
    if (!token) {
        return next({ name: 'Login' })
    }

    // Check role permissions
    if (to.meta.allowedRoles) {
        const hasPermission = to.meta.allowedRoles.some(role => userRoles.includes(role))
        if (!hasPermission) {
            // Redirect to appropriate dashboard based on user role
            if (userRoles.includes('Admin')) {
                return next({ name: 'AdminDashboard' })
            } else if (userRoles.includes('Sales')) {
                return next({ name: 'SalesDashboard' })
            } else if (userRoles.includes('Warehouse')) {
                return next({ name: 'WarehouseDashboard' })
            } else {
                return next({ name: 'Login' })
            }
        }
    }

    next()
})

export default router 