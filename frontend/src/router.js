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
import AccountManage from './views/AccountManage.vue'
import UserSettings from './views/UserSettings.vue'

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { requiresAuth: false, title: '登入' }
    },
    {
        path: '/admin',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { requiresAuth: true, allowedRoles: ['Owner', 'Admin'], title: '管理者總覽' }
    },
    {
        path: '/sales',
        name: 'SalesDashboard',
        component: SalesDashboard,
        meta: { requiresAuth: true, allowedRoles: ['Sales'], title: '銷售總覽' }
    },
    {
        path: '/warehouse',
        name: 'WarehouseDashboard',
        component: WarehouseDashboard,
        meta: { requiresAuth: true, allowedRoles: ['Warehouse'], title: '倉庫總覽' }
    },
    {
        path: '/products',
        name: 'Products',
        component: Products,
        meta: { requiresAuth: true, allowedRoles: ['Owner', 'Admin', 'Warehouse'], title: '產品管理' }
    },
    {
        path: '/suppliers',
        name: 'Suppliers',
        component: Suppliers,
        meta: { requiresAuth: true, allowedRoles: ['Owner', 'Admin', 'Warehouse'], title: '供應商管理' }
    },
    {
        path: '/customers',
        name: 'Customers',
        component: Customers,
        meta: { requiresAuth: true, allowedRoles: ['Owner', 'Admin', 'Sales'], title: '客戶管理' }
    },
    {
        path: '/orders',
        name: 'Orders',
        component: Orders,
        meta: { requiresAuth: true, allowedRoles: ['Owner', 'Admin', 'Sales'], title: '訂單管理' }
    },
    {
        path: '/shipments',
        name: 'Shipments',
        component: Shipments,
        meta: { requiresAuth: true, allowedRoles: ['Owner', 'Admin', 'Sales', 'Shipping_Vendor'], title: '出貨管理' }
    },
    {
        path: '/inventory',
        name: 'Inventory',
        component: Inventory,
        meta: { requiresAuth: true, allowedRoles: ['Owner', 'Admin', 'Warehouse'], title: '庫存管理' }
    },
    {
        path: '/locations',
        name: 'Locations',
        component: Locations,
        meta: { requiresAuth: true, allowedRoles: ['Owner', 'Admin', 'Warehouse'], title: '倉位管理' }
    },
    {
        path: '/scrap',
        name: 'Scrap',
        component: Scrap,
        meta: { requiresAuth: true, allowedRoles: ['Owner', 'Admin', 'Warehouse'], title: '報廢管理' }
    },
    {
        path: '/reports',
        name: 'Reports',
        component: Reports,
        meta: { requiresAuth: true, allowedRoles: ['Owner', 'Admin', 'Sales', 'Warehouse'], title: '報表' }
    },
    {
        path: '/AccountManage',
        name: 'AccountManage',
        component: AccountManage,
        meta: { requiresAuth: true, allowedRoles: ['Owner', 'Admin'], title: '帳號管理' }
    },
    {
        path: '/settings',
        name: 'UserSettings',
        component: UserSettings,
        meta: { requiresAuth: true, allowedRoles: ['Owner', 'Admin', 'Sales', 'Warehouse'], title: '用戶設定' }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Route guards
router.beforeEach(async (to, from, next) => {
    const isAuthenticated = store.getters.isAuthenticated
    const userRoles = store.state.roles

    // Check token expiration
    if (store.state.token && !store.dispatch('checkTokenExpiration')) {
        return next({ name: 'Login' })
    }

    // If route doesn't require auth, allow access
    if (!to.meta.requiresAuth) {
        // If user is already logged in and trying to access login, redirect to appropriate dashboard
        if (isAuthenticated && to.name === 'Login') {
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

    // If route requires auth but user is not authenticated
    if (!isAuthenticated) {
        // Clear any invalid tokens
        await store.dispatch('logout')
        return next({ name: 'Login' })
    }

    // Check role permissions
    if (to.meta.allowedRoles) {
        const hasPermission = to.meta.allowedRoles.some(role => userRoles.includes(role))
        if (!hasPermission) {
            // Show notification about insufficient permissions
            store.dispatch('showNotification', {
                type: 'error',
                message: '您沒有權限訪問此頁面'
            })

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

// Update document title after each navigation
router.afterEach((to) => {
    const baseTitle = '倉儲管理系統'
    if (to.meta.title) {
        document.title = `${to.meta.title} - ${baseTitle}`
    } else {
        document.title = baseTitle
    }
})

export default router 