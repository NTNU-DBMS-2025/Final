<template>
  <div class="w-full space-y-4 sm:space-y-6">
    <!-- Page Header -->
    <div class="px-1">
      <h1 class="text-xl sm:text-2xl font-bold text-gray-900">管理者總覽</h1>
      <p class="mt-1 text-sm text-gray-500">
        歡迎回來，{{ user?.name }}！這是您的系統總覽。
      </p>
    </div>

    <!-- Stats Overview -->
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <Card 
        title="總庫存" 
        icon="inventory" 
        color="bg-white"
        link="/inventory"
        linkText="查看庫存"
      >
        <p class="text-3xl font-bold text-gray-900">{{ totalInventory }}</p>
        <p class="text-sm text-gray-500">件商品</p>
      </Card>

      <Card 
        title="低庫存警示" 
        icon="warning" 
        color="bg-white"
        link="/inventory?lowStock=true"
        linkText="查看詳情"
      >
        <p class="text-3xl font-bold text-red-600">{{ lowStockCount }}</p>
        <p class="text-sm text-gray-500">項商品</p>
      </Card>

      <Card 
        title="待處理訂單" 
        icon="orders" 
        color="bg-white"
        link="/orders"
        linkText="查看訂單"
      >
        <p class="text-3xl font-bold text-blue-600">{{ pendingOrders }}</p>
        <p class="text-sm text-gray-500">筆訂單</p>
      </Card>

      <Card 
        title="本月報廢" 
        icon="warning" 
        color="bg-white"
        link="/scrap"
        linkText="查看報廢"
      >
        <p class="text-3xl font-bold text-orange-600">{{ monthlyScrap }}</p>
        <p class="text-sm text-gray-500">件商品</p>
      </Card>
    </div>

    <!-- Quick Actions -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
          快速操作
        </h3>
        <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
          <router-link
            to="/products"
            class="relative group bg-blue-50 hover:bg-blue-100 p-3 rounded-lg transition-colors"
          >
            <div class="text-blue-600 font-medium text-sm">產品管理</div>
          </router-link>
          
          <router-link
            to="/suppliers"
            class="relative group bg-green-50 hover:bg-green-100 p-3 rounded-lg transition-colors"
          >
            <div class="text-green-600 font-medium text-sm">供應商管理</div>
          </router-link>
          
          <router-link
            to="/customers"
            class="relative group bg-purple-50 hover:bg-purple-100 p-3 rounded-lg transition-colors"
          >
            <div class="text-purple-600 font-medium text-sm">客戶管理</div>
          </router-link>
          
          <router-link
            to="/inventory"
            class="relative group bg-yellow-50 hover:bg-yellow-100 p-3 rounded-lg transition-colors"
          >
            <div class="text-yellow-600 font-medium text-sm">庫存管理</div>
          </router-link>
          
          <router-link
            to="/orders"
            class="relative group bg-indigo-50 hover:bg-indigo-100 p-3 rounded-lg transition-colors"
          >
            <div class="text-indigo-600 font-medium text-sm">訂單管理</div>
          </router-link>
          
          <router-link
            to="/reports"
            class="relative group bg-pink-50 hover:bg-pink-100 p-3 rounded-lg transition-colors"
          >
            <div class="text-pink-600 font-medium text-sm">報表分析</div>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-6">
      <!-- Recent Orders -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
            最近訂單
          </h3>
          <div class="space-y-3">
            <div 
              v-for="order in recentOrders" 
              :key="order.order_id"
              class="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0"
            >
              <div>
                <p class="font-medium text-gray-900">#{{ order.order_id }}</p>
                <p class="text-sm text-gray-500">{{ order.customer_name }}</p>
              </div>
              <div class="text-right">
                <span :class="getStatusClass(order.status)">
                  {{ order.status }}
                </span>
                <p class="text-sm text-gray-500">{{ formatDate(order.order_date) }}</p>
              </div>
            </div>
          </div>
          <div class="mt-4">
            <router-link 
              to="/orders" 
              class="text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              查看所有訂單 →
            </router-link>
          </div>
        </div>
      </div>

      <!-- Low Stock Items -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
            低庫存商品
          </h3>
          <div class="space-y-3">
            <div 
              v-for="item in lowStockItems" 
              :key="item.product_id"
              class="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0"
            >
              <div>
                <p class="font-medium text-gray-900">{{ item.product_name }}</p>
                <p class="text-sm text-gray-500">{{ item.location_name }}</p>
              </div>
              <div class="text-right">
                <span class="text-red-600 font-semibold">{{ item.quantity }}</span>
                <p class="text-sm text-gray-500">剩餘</p>
              </div>
            </div>
          </div>
          <div class="mt-4">
            <router-link 
              to="/inventory?lowStock=true" 
              class="text-red-600 hover:text-red-800 text-sm font-medium"
            >
              查看所有低庫存 →
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Card from '../components/Card.vue'
import { fetchOrders } from '../api/orders'
import { fetchInventory } from '../api/inventory'

export default {
  name: 'AdminDashboard',
  components: {
    Card
  },
  data() {
    return {
      totalInventory: 173,
      lowStockCount: 3,
      pendingOrders: 8,
      monthlyScrap: 12,
      recentOrders: [],
      lowStockItems: [],
      loading: false
    }
  },
  computed: {
    ...mapState(['user'])
  },
  async created() {
    await this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      this.loading = true
      try {
        // Load recent orders
        const ordersResponse = await fetchOrders({ page: 1, pageSize: 5 })
        this.recentOrders = ordersResponse.data.data.orders

        // Load low stock items
        const inventoryResponse = await fetchInventory({ lowStock: true, pageSize: 5 })
        this.lowStockItems = inventoryResponse.data.data.inventory
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
      } finally {
        this.loading = false
      }
    },
    getStatusClass(status) {
      const baseClass = 'inline-flex px-2 py-1 text-xs font-semibold rounded-full'
      switch (status) {
        case '已完成':
        case '已出貨':
          return `${baseClass} bg-green-100 text-green-800`
        case '處理中':
        case '待出貨':
          return `${baseClass} bg-yellow-100 text-yellow-800`
        case '已取消':
          return `${baseClass} bg-red-100 text-red-800`
        default:
          return `${baseClass} bg-gray-100 text-gray-800`
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-TW')
    }
  }
}
</script> 