<template>
  <div class="space-y-6">
    <!-- Dashboard Header -->
    <div class="bg-white shadow rounded-lg p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-2">倉庫管理儀表板</h1>
      <p class="text-gray-600">歡迎回來，{{ $store.state.user?.account || 'Warehouse User' }}</p>
    </div>

    <!-- Warehouse Statistics Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <Card 
        title="庫存總量" 
        :value="warehouseStats.totalStock" 
        icon="📦" 
        color="blue"
        :link="{ name: 'Inventory' }"
      />
      <Card 
        title="低庫存商品" 
        :value="warehouseStats.lowStockItems" 
        icon="⚠️" 
        color="red"
        :link="{ name: 'Inventory' }"
      />
      <Card 
        title="待出庫訂單" 
        :value="warehouseStats.pendingShipments" 
        icon="🚚" 
        color="yellow"
        :link="{ name: 'Shipments' }"
      />
      <Card 
        title="庫存位置" 
        :value="warehouseStats.totalLocations" 
        icon="📍" 
        color="green"
        :link="{ name: 'Locations' }"
      />
    </div>

    <!-- Quick Actions for Warehouse -->
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">快速操作</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <button 
          @click="navigateTo('Inventory')"
          class="flex items-center p-4 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors"
        >
          <span class="text-2xl mr-3">📊</span>
          <div class="text-left">
            <div class="font-medium text-blue-900">庫存管理</div>
            <div class="text-sm text-blue-600">查看庫存狀況</div>
          </div>
        </button>
        
        <button 
          @click="navigateTo('Products')"
          class="flex items-center p-4 bg-green-50 border border-green-200 rounded-lg hover:bg-green-100 transition-colors"
        >
          <span class="text-2xl mr-3">📝</span>
          <div class="text-left">
            <div class="font-medium text-green-900">商品管理</div>
            <div class="text-sm text-green-600">新增或編輯商品</div>
          </div>
        </button>
        
        <button 
          @click="navigateTo('Locations')"
          class="flex items-center p-4 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 transition-colors"
        >
          <span class="text-2xl mr-3">🏠</span>
          <div class="text-left">
            <div class="font-medium text-purple-900">倉位管理</div>
            <div class="text-sm text-purple-600">管理倉庫位置</div>
          </div>
        </button>
        
        <button 
          @click="navigateTo('Scrap')"
          class="flex items-center p-4 bg-red-50 border border-red-200 rounded-lg hover:bg-red-100 transition-colors"
        >
          <span class="text-2xl mr-3">🗑️</span>
          <div class="text-left">
            <div class="font-medium text-red-900">報廢管理</div>
            <div class="text-sm text-red-600">處理報廢商品</div>
          </div>
        </button>
      </div>
    </div>

    <!-- Low Stock Alerts -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-gray-900">低庫存警告</h2>
        <router-link 
          :to="{ name: 'Inventory' }" 
          class="text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          查看全部
        </router-link>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full table-auto">
          <thead>
            <tr class="bg-gray-50">
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">商品名稱</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">SKU</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">目前庫存</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">最低庫存</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">位置</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">狀態</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="item in lowStockItems" :key="item.id" class="hover:bg-gray-50">
              <td class="px-4 py-2 text-sm font-medium text-gray-900">{{ item.product_name }}</td>
              <td class="px-4 py-2 text-sm text-gray-900">{{ item.sku }}</td>
              <td class="px-4 py-2 text-sm text-gray-900">{{ item.current_stock }}</td>
              <td class="px-4 py-2 text-sm text-gray-900">{{ item.min_stock }}</td>
              <td class="px-4 py-2 text-sm text-gray-900">{{ item.location }}</td>
              <td class="px-4 py-2 text-sm">
                <span class="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs font-medium">
                  低庫存
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Recent Inventory Movements -->
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">最近庫存異動</h2>
      <div class="space-y-3">
        <div 
          v-for="movement in recentMovements" 
          :key="movement.id"
          class="flex items-center justify-between p-3 border border-gray-200 rounded-lg"
        >
          <div class="flex items-center">
            <div 
              :class="getMovementIconClass(movement.type)"
              class="w-10 h-10 rounded-full flex items-center justify-center mr-3"
            >
              <span class="text-lg">{{ getMovementIcon(movement.type) }}</span>
            </div>
            <div>
              <div class="font-medium text-gray-900">{{ movement.product_name }}</div>
              <div class="text-sm text-gray-500">
                {{ getMovementTypeText(movement.type) }} • {{ movement.location }}
              </div>
            </div>
          </div>
          <div class="text-right">
            <div class="font-medium text-gray-900">
              {{ movement.type === 'out' ? '-' : '+' }}{{ movement.quantity }}
            </div>
            <div class="text-sm text-gray-500">{{ formatDate(movement.created_at) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Warehouse Locations Overview -->
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">倉位概覽</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="location in warehouseLocations" 
          :key="location.id"
          class="p-4 border border-gray-200 rounded-lg"
        >
          <div class="flex items-center justify-between mb-2">
            <h3 class="font-medium text-gray-900">{{ location.name }}</h3>
            <span 
              :class="getLocationStatusClass(location.utilization)"
              class="px-2 py-1 rounded-full text-xs font-medium"
            >
              {{ getLocationStatus(location.utilization) }}
            </span>
          </div>
          <div class="text-sm text-gray-600 mb-2">
            {{ location.zone }} • {{ location.type }}
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="bg-blue-600 h-2 rounded-full" 
              :style="{ width: location.utilization + '%' }"
            ></div>
          </div>
          <div class="text-xs text-gray-500 mt-1">
            使用率: {{ location.utilization }}%
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Card from '../components/Card.vue'
import { inventoryAPI } from '../api/inventory'

export default {
  name: 'WarehouseDashboard',
  components: {
    Card
  },
  data() {
    return {
      warehouseStats: {
        totalStock: 0,
        lowStockItems: 0,
        pendingShipments: 0,
        totalLocations: 0
      },
      lowStockItems: [],
      recentMovements: [],
      warehouseLocations: [],
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
        
        // Load inventory data
        const inventoryResponse = await inventoryAPI.fetchInventory({ per_page: 10 })
        const inventory = inventoryResponse.data.data || []
        
        // Calculate statistics
        this.calculateStats(inventory)
        this.generateLowStockItems()
        this.generateRecentMovements()
        this.generateWarehouseLocations()
        
      } catch (error) {
        console.error('Error loading dashboard data:', error)
        this.$store.dispatch('showNotification', {
          type: 'error',
          message: '載入儀表板資料失敗'
        })
      } finally {
        this.loading = false
      }
    },
    
    calculateStats(inventory) {
      this.warehouseStats.totalStock = inventory.reduce((sum, item) => sum + item.quantity_on_hand, 0)
      this.warehouseStats.lowStockItems = inventory.filter(item => 
        item.quantity_on_hand <= item.reorder_level
      ).length
      this.warehouseStats.pendingShipments = 25 // Mock data
      this.warehouseStats.totalLocations = 48 // Mock data
    },
    
    generateLowStockItems() {
      this.lowStockItems = [
        { id: 1, product_name: 'iPhone 15 Pro', sku: 'IPH15P-256-BLK', current_stock: 5, min_stock: 20, location: 'A1-02' },
        { id: 2, product_name: 'MacBook Air M2', sku: 'MBA-M2-256-SLV', current_stock: 3, min_stock: 15, location: 'B2-15' },
        { id: 3, product_name: 'iPad Pro 12.9', sku: 'IPD12-512-GRY', current_stock: 8, min_stock: 25, location: 'A3-08' },
        { id: 4, product_name: 'AirPods Pro 2', sku: 'APP2-WHT', current_stock: 12, min_stock: 30, location: 'C1-05' },
        { id: 5, product_name: 'Apple Watch Ultra', sku: 'AWU-49-ORG', current_stock: 2, min_stock: 10, location: 'B1-22' }
      ]
    },
    
    generateRecentMovements() {
      this.recentMovements = [
        { id: 1, product_name: 'iPhone 15 Pro', type: 'out', quantity: 10, location: 'A1-02', created_at: new Date() },
        { id: 2, product_name: 'MacBook Air M2', type: 'in', quantity: 25, location: 'B2-15', created_at: new Date(Date.now() - 3600000) },
        { id: 3, product_name: 'iPad Pro 12.9', type: 'out', quantity: 5, location: 'A3-08', created_at: new Date(Date.now() - 7200000) },
        { id: 4, product_name: 'AirPods Pro 2', type: 'in', quantity: 50, location: 'C1-05', created_at: new Date(Date.now() - 10800000) },
        { id: 5, product_name: 'Apple Watch Ultra', type: 'transfer', quantity: 3, location: 'B1-22', created_at: new Date(Date.now() - 14400000) }
      ]
    },
    
    generateWarehouseLocations() {
      this.warehouseLocations = [
        { id: 1, name: 'A1-區域', zone: 'A區', type: '主要倉儲', utilization: 85 },
        { id: 2, name: 'B2-區域', zone: 'B區', type: '次要倉儲', utilization: 72 },
        { id: 3, name: 'C1-區域', zone: 'C區', type: '快速出貨', utilization: 95 },
        { id: 4, name: 'D3-區域', zone: 'D區', type: '退貨處理', utilization: 45 },
        { id: 5, name: 'E1-區域', zone: 'E區', type: '品質檢驗', utilization: 60 },
        { id: 6, name: 'F2-區域', zone: 'F區', type: '預留空間', utilization: 30 }
      ]
    },
    
    navigateTo(routeName) {
      this.$router.push({ name: routeName })
    },
    
    getMovementIcon(type) {
      const icons = {
        'in': '📥',
        'out': '📤',
        'transfer': '🔄'
      }
      return icons[type] || '📦'
    },
    
    getMovementIconClass(type) {
      const classes = {
        'in': 'bg-green-100 text-green-600',
        'out': 'bg-red-100 text-red-600',
        'transfer': 'bg-blue-100 text-blue-600'
      }
      return classes[type] || 'bg-gray-100 text-gray-600'
    },
    
    getMovementTypeText(type) {
      const texts = {
        'in': '入庫',
        'out': '出庫',
        'transfer': '調撥'
      }
      return texts[type] || type
    },
    
    getLocationStatusClass(utilization) {
      if (utilization >= 90) return 'bg-red-100 text-red-800'
      if (utilization >= 70) return 'bg-yellow-100 text-yellow-800'
      return 'bg-green-100 text-green-800'
    },
    
    getLocationStatus(utilization) {
      if (utilization >= 90) return '滿載'
      if (utilization >= 70) return '繁忙'
      return '正常'
    },
    
    formatDate(date) {
      return new Date(date).toLocaleString('zh-TW')
    }
  }
}
</script> 