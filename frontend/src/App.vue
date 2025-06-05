<script>
import { mapState, mapActions, mapGetters } from 'vuex'
import Notification from './components/Notification.vue'

export default {
  name: 'App',
  components: {
    Notification
  },
  data() {
    return {
      mobileMenuOpen: false
    }
  },
  computed: {
    ...mapState(['user']),
    ...mapGetters(['isAuthenticated', 'hasRole']),
    navigationItems() {
      const items = []
      
      // Dashboard routes based on role
      if (this.hasRole('Admin')) {
        items.push({ name: 'dashboard', label: '管理者總覽', to: '/admin' })
      } else if (this.hasRole('Sales')) {
        items.push({ name: 'dashboard', label: '銷售總覽', to: '/sales' })
      } else if (this.hasRole('Warehouse')) {
        items.push({ name: 'dashboard', label: '倉庫總覽', to: '/warehouse' })
      }
      
      // Feature routes based on role
      if (this.hasRole('Admin') || this.hasRole('Warehouse')) {
        items.push({ name: 'products', label: '產品管理', to: '/products' })
        items.push({ name: 'suppliers', label: '供應商管理', to: '/suppliers' })
        items.push({ name: 'inventory', label: '庫存管理', to: '/inventory' })
        items.push({ name: 'locations', label: '儲位管理', to: '/locations' })
        items.push({ name: 'scrap', label: '報廢管理', to: '/scrap' })
      }
      
      if (this.hasRole('Admin') || this.hasRole('Sales')) {
        items.push({ name: 'customers', label: '客戶管理', to: '/customers' })
        items.push({ name: 'orders', label: '訂單管理', to: '/orders' })
        items.push({ name: 'shipments', label: '出貨管理', to: '/shipments' })
      }
      
      // Reports for all authenticated users
      if (this.isAuthenticated) {
        items.push({ name: 'reports', label: '報表', to: '/reports' })
      }
      
      return items
    }
  },
  async created() {
    // Initialize user data if token exists
    if (this.isAuthenticated) {
      try {
        await this.fetchCurrentUser()
        // Redirect to appropriate dashboard if on root or login page
        if (this.$route.path === '/' || this.$route.path === '/login') {
          if (this.hasRole('Admin')) {
            this.$router.push('/admin')
          } else if (this.hasRole('Sales')) {
            this.$router.push('/sales')
          } else if (this.hasRole('Warehouse')) {
            this.$router.push('/warehouse')
          }
        }
      } catch (error) {
        console.error('Failed to fetch user:', error)
        this.logout()
        this.$router.push('/login')
      }
    }
  },
  methods: {
    ...mapActions(['logout', 'fetchCurrentUser', 'showNotification']),
    async handleLogout() {
      try {
        await this.logout()
        this.showNotification({
          type: 'success',
          message: '已成功登出'
        })
        this.$router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
  }
}
</script>

<template>
  <div id="app" class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Navigation Bar -->
    <nav v-if="isAuthenticated" class="bg-gray-800 shadow-lg flex-shrink-0 w-full">
      <div class="w-full px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center min-w-0 flex-1">
            <!-- Logo/Title -->
            <div class="flex-shrink-0">
              <h1 class="text-white text-lg sm:text-xl font-bold truncate">倉儲管理系統</h1>
            </div>
            
            <!-- Desktop Navigation -->
            <div class="hidden lg:block ml-8">
              <div class="flex items-baseline space-x-1">
                <router-link
                  v-for="item in navigationItems"
                  :key="item.name"
                  :to="item.to"
                  :class="[
                    'px-3 py-2 rounded-md text-sm font-medium transition-colors whitespace-nowrap',
                    $route.path === item.to
                      ? 'bg-gray-900 text-white'
                      : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  ]"
                >
                  {{ item.label }}
                </router-link>
              </div>
            </div>
          </div>
          
          <!-- Mobile menu button -->
          <div class="lg:hidden flex items-center">
            <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="text-gray-400 hover:text-white hover:bg-gray-700 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-white"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <!-- User Menu -->
          <div class="hidden lg:flex items-center flex-shrink-0 ml-4">
            <div class="flex items-center space-x-4">
              <span class="text-gray-300 text-sm">
                歡迎，{{ user?.name || 'User' }}
              </span>
              <button
                @click="handleLogout"
                class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                登出
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Mobile Navigation -->
      <div v-show="mobileMenuOpen" class="lg:hidden border-t border-gray-700">
        <div class="px-2 pt-2 pb-3 space-y-1 max-h-96 overflow-y-auto">
          <router-link
            v-for="item in navigationItems"
            :key="item.name"
            :to="item.to"
            @click="mobileMenuOpen = false"
            :class="[
              'block px-3 py-2 rounded-md text-base font-medium transition-colors',
              $route.path === item.to
                ? 'bg-gray-900 text-white'
                : 'text-gray-300 hover:bg-gray-700 hover:text-white'
            ]"
          >
            {{ item.label }}
          </router-link>
          
          <!-- Mobile User Menu -->
          <div class="border-t border-gray-700 pt-4 mt-4">
            <div class="px-3 py-2">
              <span class="text-gray-300 text-sm">
                歡迎，{{ user?.name || 'User' }}
              </span>
            </div>
            <button
              @click="handleLogout"
              class="block w-full text-left px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
            >
              登出
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-1 w-full min-h-0 scroll-container">
      <div class="w-full px-4 sm:px-6 lg:px-8 py-6">
        <!-- Debug info - remove later -->
        <div v-if="isAuthenticated" class="mb-4 p-4 bg-blue-100 rounded-lg text-sm">
          <p><strong>當前路由:</strong> {{ $route.path }}</p>
          <p><strong>用戶角色:</strong> {{ user?.roles?.join(', ') || '未知' }}</p>
          <p><strong>用戶名稱:</strong> {{ user?.name || '未設定' }}</p>
        </div>
        
        <router-view />
      </div>
    </main>

    <!-- Notifications -->
    <Notification />
  </div>
</template>

<style scoped>
/* Ensure proper scrolling and layout */
#app {
  width: 100%;
  min-width: 100vw;
  height: 100vh;
  max-height: 100vh;
  margin: 0;
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
}

/* Ensure body has no margins and prevent bounce scrolling */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: fixed;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: none;
}

/* Better responsive text scaling */
@media (max-width: 640px) {
  .truncate {
    max-width: 150px;
  }
}

/* Navigation improvements */
nav {
  position: relative;
  flex-shrink: 0;
  z-index: 50;
  width: 100%;
  min-height: 64px; /* Ensure consistent nav height */
}

/* Main content area */
main {
  flex: 1;
  width: 100%;
  height: 0; /* Force flex item to respect flex-basis */
  overflow-y: auto;
  overflow-x: hidden;
  background-color: #f9fafb;
  margin: 0;
  padding: 0;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior-y: contain;
}

/* Container improvements */
.container {
  max-width: none;
  width: 100%;
  margin: 0;
}

/* Desktop navigation spacing */
@media (min-width: 1024px) {
  .lg\:block .flex {
    min-width: 0;
  }
  
  /* Better spacing for navigation items */
  nav .space-x-1 > * + * {
    margin-left: 0.5rem;
  }
}

/* Mobile navigation improvements */
@media (max-width: 1023px) {
  /* Mobile menu slide animation */
  .lg\:hidden > div {
    animation: slideDown 0.2s ease-out;
  }
  
  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
}

/* Custom scrollbar for mobile nav */
.lg\:hidden .overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.lg\:hidden .overflow-y-auto::-webkit-scrollbar-track {
  background: #374151;
}

.lg\:hidden .overflow-y-auto::-webkit-scrollbar-thumb {
  background: #6b7280;
  border-radius: 2px;
}

/* Navigation link hover effects */
nav a {
  transition: all 0.2s ease-in-out;
}

nav a:hover {
  transform: translateY(-1px);
}

/* Mobile menu button animation */
.lg\:hidden button svg {
  transition: transform 0.2s ease-in-out;
}

/* Prevent scroll bounce and over-scrolling */
.scroll-container {
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
}

/* Ensure no unwanted scrollbars or overflow */
* {
  -webkit-overflow-scrolling: touch;
}

/* For Webkit browsers - prevent bounce scrolling */
body {
  -webkit-overflow-scrolling: touch;
  overscroll-behavior-y: none;
}

/* Prevent pull-to-refresh on mobile */
html {
  overscroll-behavior: none;
}
</style>
