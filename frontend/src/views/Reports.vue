<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-900">報表管理</h1>
          <button
            @click="refreshAllData"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            <i class="fas fa-sync-alt mr-2"></i>
            刷新資料
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Quick Report Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div 
          @click="showReport('inventory')"
          class="bg-white rounded-lg shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow"
        >
          <div class="flex items-center">
            <div class="p-3 bg-blue-100 rounded-lg">
              <i class="fas fa-boxes text-blue-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">庫存報表</h3>
              <p class="text-sm text-gray-600">目前庫存狀況</p>
              <p class="text-xs text-blue-600 mt-1" v-if="summaryData.inventory">
                {{ summaryData.inventory.expired_count || 0 }} 過期 / 
                {{ summaryData.inventory.low_stock_count || 0 }} 低庫存
              </p>
            </div>
          </div>
        </div>

        <div 
          @click="showReport('sales')"
          class="bg-white rounded-lg shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow"
        >
          <div class="flex items-center">
            <div class="p-3 bg-green-100 rounded-lg">
              <i class="fas fa-chart-line text-green-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">銷售報表</h3>
              <p class="text-sm text-gray-600">銷售績效分析</p>
              <p class="text-xs text-green-600 mt-1" v-if="summaryData.sales">
                {{ summaryData.sales.sales_days_count || 0 }} 天資料 / 
                {{ summaryData.sales.top_products_count || 0 }} 熱銷商品
              </p>
            </div>
          </div>
        </div>

        <div 
          @click="showReport('orders')"
          class="bg-white rounded-lg shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow"
        >
          <div class="flex items-center">
            <div class="p-3 bg-yellow-100 rounded-lg">
              <i class="fas fa-shopping-cart text-yellow-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">訂單報表</h3>
              <p class="text-sm text-gray-600">訂單處理狀況</p>
              <p class="text-xs text-yellow-600 mt-1" v-if="summaryData.orders">
                {{ summaryData.orders.pending_count || 0 }} 待處理 / 
                {{ summaryData.orders.delayed_count || 0 }} 延遲出貨
              </p>
            </div>
          </div>
        </div>

        <div 
          @click="showReport('financial')"
          class="bg-white rounded-lg shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow"
        >
          <div class="flex items-center">
            <div class="p-3 bg-purple-100 rounded-lg">
              <i class="fas fa-dollar-sign text-purple-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">財務報表</h3>
              <p class="text-sm text-gray-600">收入支出分析</p>
              <p class="text-xs text-purple-600 mt-1" v-if="summaryData.financial">
                {{ summaryData.financial.scrap_cost_records || 0 }} 報廢記錄 / 
                {{ summaryData.financial.products_with_scrap || 0 }} 有報廢產品
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Report Details Section -->
      <div v-if="activeReport" class="bg-white rounded-lg shadow-sm overflow-hidden mb-6">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h2 class="text-lg font-semibold text-gray-900">{{ getReportTitle(activeReport) }}</h2>
          <button
            @click="activeReport = null"
            class="text-gray-400 hover:text-gray-600"
          >
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <!-- Loading State -->
        <div v-if="loading" class="p-8 text-center">
          <i class="fas fa-spinner fa-spin text-gray-400 text-2xl mb-4"></i>
          <p class="text-gray-600">載入報表資料中...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="p-8 text-center">
          <i class="fas fa-exclamation-triangle text-red-400 text-2xl mb-4"></i>
          <p class="text-red-600">{{ error }}</p>
          <button
            @click="loadReportData(activeReport)"
            class="mt-4 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded"
          >
            重試
          </button>
        </div>

        <!-- Report Content -->
        <div v-else-if="reportData">
          <!-- Inventory Report -->
          <div v-if="activeReport === 'inventory'" class="p-6 space-y-6">
            <!-- Summary Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div class="bg-red-50 p-4 rounded-lg">
                <h4 class="font-medium text-red-800">已過期庫存</h4>
                <p class="text-2xl font-bold text-red-600">{{ reportData.expired_items?.length || 0 }}</p>
              </div>
              <div class="bg-yellow-50 p-4 rounded-lg">
                <h4 class="font-medium text-yellow-800">低庫存商品</h4>
                <p class="text-2xl font-bold text-yellow-600">{{ reportData.low_stock_items?.length || 0 }}</p>
              </div>
              <div class="bg-orange-50 p-4 rounded-lg">
                <h4 class="font-medium text-orange-800">零庫存商品</h4>
                <p class="text-2xl font-bold text-orange-600">{{ reportData.out_of_stock_products?.length || 0 }}</p>
              </div>
              <div class="bg-purple-50 p-4 rounded-lg">
                <h4 class="font-medium text-purple-800">超載倉位</h4>
                <p class="text-2xl font-bold text-purple-600">{{ reportData.over_capacity_locations?.length || 0 }}</p>
              </div>
            </div>

            <!-- Detailed Tables -->
            <div class="space-y-6">
              <!-- Expired Items -->
              <div v-if="reportData.expired_items?.length">
                <h4 class="text-lg font-medium text-gray-900 mb-3">已過期庫存</h4>
                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                      <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">產品名稱</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">位置</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">數量</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">過期日期</th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr v-for="item in reportData.expired_items" :key="`${item.product_id}-${item.location_id}`">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {{ item.product_name }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {{ item.location_name }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {{ item.quantity }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-red-600">
                          {{ formatDate(item.expiry_date) }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Low Stock Items -->
              <div v-if="reportData.low_stock_items?.length">
                <h4 class="text-lg font-medium text-gray-900 mb-3">低庫存商品</h4>
                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                      <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">產品名稱</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">區域</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">目前庫存</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">過期日期</th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr v-for="item in reportData.low_stock_items" :key="`${item.product_id}-${item.location_id}`">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {{ item.product_name }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {{ item.zone }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-yellow-600 font-medium">
                          {{ item.quantity }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {{ formatDate(item.expiry_date) }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <!-- Sales Report -->
          <div v-if="activeReport === 'sales'" class="p-6 space-y-6">
            <!-- Sales 30d -->
            <div v-if="reportData.sales_30d?.length">
              <h4 class="text-lg font-medium text-gray-900 mb-3">近30天銷售報告</h4>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">日期</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">訂單數</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">銷售數量</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">銷售金額</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="day in reportData.sales_30d" :key="day.sales_day">
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {{ formatDate(day.sales_day) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ day.orders_cnt }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ day.units_sold }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">
                        ${{ formatCurrency(day.total_amount) }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Fast Moving Products -->
            <div v-if="reportData.fast_moving_products?.length">
              <h4 class="text-lg font-medium text-gray-900 mb-3">熱銷商品TOP10</h4>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">排名</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">產品名稱</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">30天銷量</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="(product, index) in reportData.fast_moving_products" :key="product.product_id">
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {{ index + 1 }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {{ product.name }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">
                        {{ product.sold_qty_30d }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Orders Report -->
          <div v-if="activeReport === 'orders'" class="p-6 space-y-6">
            <!-- Summary Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div class="bg-blue-50 p-4 rounded-lg">
                <h4 class="font-medium text-blue-800">待處理訂單</h4>
                <p class="text-2xl font-bold text-blue-600">{{ reportData.pending_orders?.length || 0 }}</p>
              </div>
              <div class="bg-yellow-50 p-4 rounded-lg">
                <h4 class="font-medium text-yellow-800">今日未出貨</h4>
                <p class="text-2xl font-bold text-yellow-600">{{ reportData.unshipped_today?.length || 0 }}</p>
              </div>
              <div class="bg-red-50 p-4 rounded-lg">
                <h4 class="font-medium text-red-800">延遲出貨</h4>
                <p class="text-2xl font-bold text-red-600">{{ reportData.delayed_orders?.length || 0 }}</p>
              </div>
              <div class="bg-green-50 p-4 rounded-lg">
                <h4 class="font-medium text-green-800">本週預計出貨</h4>
                <p class="text-2xl font-bold text-green-600">{{ reportData.this_week_shipments?.length || 0 }}</p>
              </div>
            </div>

            <!-- Pending Orders -->
            <div v-if="reportData.pending_orders?.length">
              <h4 class="text-lg font-medium text-gray-900 mb-3">待處理訂單</h4>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">訂單編號</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">預計交貨日</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">優先級</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">運送地址</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">總金額</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="order in reportData.pending_orders" :key="order.order_id">
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {{ order.order_number }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ formatDate(order.expected_delivery_date) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm">
                        <span :class="getPriorityClass(order.priority)">
                          {{ order.priority }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ order.ship_to }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">
                        ${{ formatCurrency(order.total_amount) }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Financial Report -->
          <div v-if="activeReport === 'financial'" class="p-6 space-y-6">
            <!-- Monthly Scrap Cost -->
            <div v-if="reportData.monthly_scrap_cost?.length">
              <h4 class="text-lg font-medium text-gray-900 mb-3">本月報廢成本</h4>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">月份</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">報廢記錄數</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">總報廢成本</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="item in reportData.monthly_scrap_cost" :key="item.month">
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {{ item.month }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ item.scrap_records }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-red-600 font-medium">
                        ${{ formatCurrency(item.total_scrap_cost) }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Average Order Values -->
            <div v-if="reportData.avg_order_values?.length">
              <h4 class="text-lg font-medium text-gray-900 mb-3">客戶類型平均訂單金額</h4>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">客戶類型</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">平均訂單金額</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">訂單數量</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="item in reportData.avg_order_values" :key="item.customer_type">
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {{ item.customer_type }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">
                        ${{ formatCurrency(item.avg_order_value) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ item.orders_cnt }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reports } from '@/api'

export default {
  name: 'Reports',
  data() {
    return {
      loading: false,
      error: null,
      activeReport: null,
      reportData: null,
      summaryData: {
        inventory: null,
        sales: null,
        orders: null,
        financial: null
      }
    }
  },
  methods: {
    async refreshAllData() {
      await this.loadSummaryData()
      if (this.activeReport) {
        await this.loadReportData(this.activeReport)
      }
    },
    
    async loadSummaryData() {
      try {
        const [inventoryRes, salesRes, ordersRes, financialRes] = await Promise.all([
          reports.fetchInventorySummary(),
          reports.fetchSalesSummary(),
          reports.fetchOrdersSummary(),
          reports.fetchFinancialSummary()
        ])

        this.summaryData.inventory = inventoryRes.data.success ? inventoryRes.data.data.summary : null
        this.summaryData.sales = salesRes.data.success ? salesRes.data.data.summary : null
        this.summaryData.orders = ordersRes.data.success ? ordersRes.data.data.summary : null
        this.summaryData.financial = financialRes.data.success ? financialRes.data.data.summary : null

        // Force reactivity update
        this.$forceUpdate()
      } catch (error) {
        console.error('Error loading summary data:', error)
      }
    },
    
    async showReport(type) {
      this.activeReport = type
      this.reportData = null
      this.error = null
      await this.loadReportData(type)
    },
    
    async loadReportData(type) {
      this.loading = true
      this.error = null
      
      try {
        let response
        switch (type) {
          case 'inventory':
            response = await reports.fetchInventorySummary()
            break
          case 'sales':
            response = await reports.fetchSalesSummary()
            break
          case 'orders':
            response = await reports.fetchOrdersSummary()
            break
          case 'financial':
            response = await reports.fetchFinancialSummary()
            break
          default:
            throw new Error('Unknown report type')
        }
        
        if (response.data.success) {
          this.reportData = response.data.data
        } else {
          this.error = response.data.error || '載入報表資料失敗'
        }
      } catch (error) {
        console.error('Error loading report data:', error)
        this.error = '無法連接到伺服器，請稍後再試'
      } finally {
        this.loading = false
      }
    },
    
    getReportTitle(type) {
      const titles = {
        inventory: '庫存報表',
        sales: '銷售報表', 
        orders: '訂單報表',
        financial: '財務報表'
      }
      return titles[type] || type
    },
    
    formatDate(date) {
      if (!date) return '-'
      return new Date(date).toLocaleDateString('zh-TW')
    },
    
    formatCurrency(amount) {
      if (!amount) return '0'
      return new Intl.NumberFormat('zh-TW').format(amount)
    },
    
    getPriorityClass(priority) {
      const classes = {
        'high': 'px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800',
        'normal': 'px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800',
        'low': 'px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800'
      }
      return classes[priority] || classes['normal']
    }
  },
  
  async mounted() {
    await this.loadSummaryData()
  }
}
</script> 