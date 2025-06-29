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
      mobileMenuOpen: false,
      userMenuOpen: false
    }
  },
  computed: {
    ...mapState(['user']),
    ...mapGetters(['isAuthenticated', 'hasRole']),
    navigationItems() {
      const items = []
      
      // Dashboard routes based on role
      if (this.hasRole('Owner') || this.hasRole('Admin')) {
        items.push({ name: 'dashboard', label: '管理者總覽', to: '/admin' })
      } else if (this.hasRole('Sales')) {
        items.push({ name: 'dashboard', label: '銷售總覽', to: '/sales' })
      } else if (this.hasRole('Warehouse')) {
        items.push({ name: 'dashboard', label: '倉庫總覽', to: '/warehouse' })
      }
      
      // Feature routes based on role
      if (this.hasRole('Owner') || this.hasRole('Admin') || this.hasRole('Warehouse')) {
        items.push({ name: 'products', label: '產品管理', to: '/products' })
        items.push({ name: 'suppliers', label: '供應商管理', to: '/suppliers' })
        items.push({ name: 'inventory', label: '庫存管理', to: '/inventory' })
        items.push({ name: 'locations', label: '倉位管理', to: '/locations' })
        items.push({ name: 'scrap', label: '報廢管理', to: '/scrap' })
      }
      
      if (this.hasRole('Owner') || this.hasRole('Admin') || this.hasRole('Sales')) {
        items.push({ name: 'customers', label: '客戶管理', to: '/customers' })
        items.push({ name: 'orders', label: '訂單管理', to: '/orders' })
        items.push({ name: 'shipments', label: '出貨管理', to: '/shipments' })
      }
      
      // Reports for all authenticated users
      if (this.isAuthenticated) {
        items.push({ name: 'reports', label: '報表', to: '/reports' })
      }

      // Account management for admin and owner users only
      if (this.hasRole('Owner') || this.hasRole('Admin')) {
        items.push({ name: 'AccountManage', label: '帳號管理', to: '/AccountManage' })
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
          if (this.hasRole('Owner') || this.hasRole('Admin')) {
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
  mounted() {
    // Fix stuck hover states and cursor issues
    this.fixHoverStates()
    
    // Handle click outside user menu
    document.addEventListener('click', () => {
      this.userMenuOpen = false
    })
  },
  methods: {
    ...mapActions(['logout', 'fetchCurrentUser', 'showNotification']),
    
    fixHoverStates() {
      // Reset any stuck hover states
      document.addEventListener('mousemove', () => {
        // Force refresh of hover states by briefly removing and re-adding hover class
        const hoveredElements = document.querySelectorAll(':hover')
        hoveredElements.forEach(el => {
          if (el.classList.contains('group') || el.classList.contains('card-hover')) {
            el.style.pointerEvents = 'none'
            setTimeout(() => {
              el.style.pointerEvents = 'auto'
            }, 1)
          }
        })
      }, { passive: true })
      
      // Fix touch device hover states
      document.addEventListener('touchstart', () => {
        document.body.classList.add('touching')
      }, { passive: true })
      
      document.addEventListener('touchend', () => {
        setTimeout(() => {
          document.body.classList.remove('touching')
        }, 100)
      }, { passive: true })
    },
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
              <div class="relative" @click.stop>
                <button
                  @click="userMenuOpen = !userMenuOpen"
                  class="text-gray-300 text-sm hover:text-white transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1"
                >
                  歡迎，{{ user?.account || 'User' }} ▼
                </button>
                
                <!-- Dropdown Menu -->
                <div
                  v-show="userMenuOpen"
                  @click.stop="userMenuOpen = false"
                  class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50 border"
                >
                  <router-link
                    to="/settings"
                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                  >
                    <svg class="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                    用戶設定
                  </router-link>
                  <button
                    @click="handleLogout"
                    class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                  >
                    <svg class="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                    </svg>
                    登出
                  </button>
                </div>
              </div>
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
                歡迎，{{ user?.account || 'User' }}
              </span>
            </div>
            <router-link
              to="/settings"
              @click="mobileMenuOpen = false"
              class="block px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
            >
              <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
              用戶設定
            </router-link>
            <button
              @click="handleLogout"
              class="block w-full text-left px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
            >
              <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
              </svg>
              登出
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-1 w-full min-h-0">
      <div class="w-full px-4 sm:px-6 lg:px-8 py-6">
        <!-- Debug info - remove later -->
        <div v-if="isAuthenticated" class="mb-4 p-4 bg-blue-100 rounded-lg text-sm">
          <p><strong>當前路由:</strong> {{ $route.path }}</p>
          <p><strong>用戶角色:</strong> {{ user?.role_name || '未知' }}</p>
          <p><strong>用戶名稱:</strong> {{ user?.account || '未設定' }}</p>
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

/* Prevent pull-to-refresh on mobile */
html {
  overscroll-behavior: none;
}

/* Fix cursor and hover behavior issues */
* {
  -webkit-tap-highlight-color: transparent;
}

/* Reset cursor and pointer behavior */
body, html, #app {
  cursor: default;
}

/* Ensure proper cursor behavior for interactive elements */
button, a, [role="button"] {
  cursor: pointer;
}

button:disabled, a[disabled] {
  cursor: not-allowed;
}

/* Fix hover states being stuck */
@media (hover: hover) and (pointer: fine) {
  /* Only apply hover effects on devices that actually support hovering */
  .hover\:bg-blue-100:hover {
    background-color: rgb(219 234 254);
  }
  
  .hover\:bg-green-100:hover {
    background-color: rgb(220 252 231);
  }
  
  .hover\:bg-purple-100:hover {
    background-color: rgb(243 232 255);
  }
  
  .hover\:bg-yellow-100:hover {
    background-color: rgb(254 249 195);
  }
  
  .hover\:bg-indigo-100:hover {
    background-color: rgb(224 231 255);
  }
  
  .hover\:bg-pink-100:hover {
    background-color: rgb(252 231 243);
  }
  
  .hover\:shadow-xl:hover {
    box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  }
}

/* Reset any stuck hover states on touch devices */
@media (hover: none) {
  .hover\:bg-blue-100:hover,
  .hover\:bg-green-100:hover,
  .hover\:bg-purple-100:hover,
  .hover\:bg-yellow-100:hover,
  .hover\:bg-indigo-100:hover,
  .hover\:bg-pink-100:hover,
  .hover\:shadow-xl:hover {
    /* Reset to default state on touch devices */
  }
}

/* Fix navigation hover effects */
nav a {
  transition: all 0.2s ease-in-out;
  cursor: pointer;
}

@media (hover: hover) and (pointer: fine) {
  nav a:hover {
    transform: translateY(-1px);
  }
}

/* Ensure buttons have proper cursor */
.bg-blue-500, .bg-red-600, .bg-green-600 {
  cursor: pointer;
}

/* Fix any z-index issues that might cause phantom clicks */
.relative {
  z-index: auto;
}

/* Ensure no invisible elements are capturing events */
.group::before,
.group::after {
  content: none;
}
</style>
