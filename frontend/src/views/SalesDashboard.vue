<template>
  <div class="space-y-6">
    <!-- Dashboard Header -->
    <div class="bg-white shadow rounded-lg p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-2">銷售管理儀表板</h1>
      <p class="text-gray-600">歡迎回來，{{ $store.state.user?.username || 'Sales User' }}</p>
    </div>

    <!-- Sales Statistics Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <Card 
        title="今日訂單" 
        :value="salesStats.todayOrders" 
        icon="📊" 
        color="blue"
        :link="{ name: 'Orders' }"
      />
      <Card 
        title="本月銷售額" 
        :value="`$${salesStats.monthlyRevenue.toLocaleString()}`" 
        icon="💰" 
        color="green"
      />
      <Card 
        title="待處理訂單" 
        :value="salesStats.pendingOrders" 
        icon="⏳" 
        color="yellow"
        :link="{ name: 'Orders' }"
      />
      <Card 
        title="客戶總數" 
        :value="salesStats.totalCustomers" 
        icon="👥" 
        color="purple"
        :link="{ name: 'Customers' }"
      />
    </div>

    <!-- Quick Actions for Sales -->
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">快速操作</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <button 
          @click="navigateTo('Orders')"
          class="flex items-center p-4 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors"
        >
          <span class="text-2xl mr-3">📝</span>
          <div class="text-left">
            <div class="font-medium text-blue-900">新增訂單</div>
            <div class="text-sm text-blue-600">建立新的客戶訂單</div>
          </div>
        </button>
        
        <button 
          @click="navigateTo('Customers')"
          class="flex items-center p-4 bg-green-50 border border-green-200 rounded-lg hover:bg-green-100 transition-colors"
        >
          <span class="text-2xl mr-3">👤</span>
          <div class="text-left">
            <div class="font-medium text-green-900">客戶管理</div>
            <div class="text-sm text-green-600">查看和管理客戶資料</div>
          </div>
        </button>
        
        <button 
          @click="navigateTo('Reports')"
          class="flex items-center p-4 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 transition-colors"
        >
          <span class="text-2xl mr-3">📈</span>
          <div class="text-left">
            <div class="font-medium text-purple-900">銷售報表</div>
            <div class="text-sm text-purple-600">查看銷售績效報表</div>
          </div>
        </button>
      </div>
    </div>

    <!-- Recent Orders -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-gray-900">最近訂單</h2>
        <router-link 
          :to="{ name: 'Orders' }" 
          class="text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          查看全部
        </router-link>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full table-auto">
          <thead>
            <tr class="bg-gray-50">
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">訂單編號</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">客戶</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">金額</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">狀態</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">日期</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="order in recentOrders" :key="order.id" class="hover:bg-gray-50">
              <td class="px-4 py-2 text-sm font-medium text-gray-900">{{ order.order_number }}</td>
              <td class="px-4 py-2 text-sm text-gray-900">{{ order.customer_name }}</td>
              <td class="px-4 py-2 text-sm text-gray-900">${{ order.total_amount.toLocaleString() }}</td>
              <td class="px-4 py-2 text-sm">
                <span 
                  :class="getStatusClass(order.status)"
                  class="px-2 py-1 rounded-full text-xs font-medium"
                >
                  {{ getStatusText(order.status) }}
                </span>
              </td>
              <td class="px-4 py-2 text-sm text-gray-900">{{ formatDate(order.order_date) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Top Customers -->
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">主要客戶</h2>
      <div class="space-y-3">
        <div 
          v-for="customer in topCustomers" 
          :key="customer.id"
          class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
        >
          <div class="flex items-center">
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
              <span class="text-blue-600 font-semibold">{{ customer.name.charAt(0) }}</span>
            </div>
            <div>
              <div class="font-medium text-gray-900">{{ customer.name }}</div>
              <div class="text-sm text-gray-500">{{ customer.email }}</div>
            </div>
          </div>
          <div class="text-right">
            <div class="font-medium text-gray-900">${{ customer.total_orders.toLocaleString() }}</div>
            <div class="text-sm text-gray-500">{{ customer.order_count }} 訂單</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Card from '../components/Card.vue'
import { ordersAPI } from '../api/orders'

export default {
  name: 'SalesDashboard',
  components: {
    Card
  },
  data() {
    return {
      salesStats: {
        todayOrders: 0,
        monthlyRevenue: 0,
        pendingOrders: 0,
        totalCustomers: 0
      },
      recentOrders: [],
      topCustomers: [],
      loading: true
    }
  },
  async created() {
    await this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      try {
        this.loading = true
        
        // Load recent orders
        const ordersResponse = await ordersAPI.getOrders({ limit: 5 })
        this.recentOrders = ordersResponse.data
        
        // Calculate statistics from orders data
        this.calculateStats()
        this.generateTopCustomers()
        
      } catch (error) {
        console.error('Error loading dashboard data:', error)
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: '載入儀表板資料失敗'
        })
      } finally {
        this.loading = false
      }
    },
    
    calculateStats() {
      const today = new Date().toDateString()
      const currentMonth = new Date().getMonth()
      
      this.salesStats.todayOrders = this.recentOrders.filter(order => 
        new Date(order.order_date).toDateString() === today
      ).length
      
      this.salesStats.monthlyRevenue = this.recentOrders
        .filter(order => new Date(order.order_date).getMonth() === currentMonth)
        .reduce((sum, order) => sum + order.total_amount, 0)
      
      this.salesStats.pendingOrders = this.recentOrders.filter(order => 
        order.status === 'pending'
      ).length
      
      this.salesStats.totalCustomers = new Set(this.recentOrders.map(order => order.customer_id)).size
    },
    
    generateTopCustomers() {
      // Generate mock top customers data
      this.topCustomers = [
        { id: 1, name: '台積電', email: 'tsmc@example.com', total_orders: 150000, order_count: 12 },
        { id: 2, name: '鴻海科技', email: 'foxconn@example.com', total_orders: 120000, order_count: 8 },
        { id: 3, name: '聯發科', email: 'mediatek@example.com', total_orders: 95000, order_count: 6 },
        { id: 4, name: '華碩電腦', email: 'asus@example.com', total_orders: 78000, order_count: 9 },
        { id: 5, name: '宏碁', email: 'acer@example.com', total_orders: 65000, order_count: 7 }
      ]
    },
    
    navigateTo(routeName) {
      this.$router.push({ name: routeName })
    },
    
    getStatusClass(status) {
      const statusClasses = {
        'pending': 'bg-yellow-100 text-yellow-800',
        'confirmed': 'bg-blue-100 text-blue-800',
        'shipped': 'bg-green-100 text-green-800',
        'delivered': 'bg-green-100 text-green-800',
        'cancelled': 'bg-red-100 text-red-800'
      }
      return statusClasses[status] || 'bg-gray-100 text-gray-800'
    },
    
    getStatusText(status) {
      const statusTexts = {
        'pending': '待處理',
        'confirmed': '已確認',
        'shipped': '已出貨',
        'delivered': '已送達',
        'cancelled': '已取消'
      }
      return statusTexts[status] || status
    },
    
    formatDate(date) {
      return new Date(date).toLocaleDateString('zh-TW')
    }
  }
}
</script> 