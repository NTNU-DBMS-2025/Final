<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">庫存管理</h1>
          <p class="text-gray-600">管理商品庫存數量、位置與異動記錄</p>
        </div>
        <div class="flex space-x-3">
          <button 
            @click="openAdjustmentModal"
            class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center"
          >
            <span class="mr-2">📝</span>
            庫存調整
          </button>
          <button 
            @click="openMovementModal"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center"
          >
            <span class="mr-2">🔄</span>
            庫存異動
          </button>
        </div>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <Card 
        title="總庫存值" 
        icon="inventory" 
        color="bg-white"
      >
        <p class="text-3xl font-bold text-green-600">${{ totalInventoryValue.toLocaleString() }}</p>
        <p class="text-sm text-gray-500">總價值</p>
      </Card>
      
      <Card 
        title="庫存品項" 
        icon="products" 
        color="bg-white"
      >
        <p class="text-3xl font-bold text-blue-600">{{ totalItems }}</p>
        <p class="text-sm text-gray-500">個品項</p>
      </Card>
      
      <Card 
        title="低庫存警告" 
        icon="warning" 
        color="bg-white"
      >
        <p class="text-3xl font-bold text-red-600">{{ lowStockCount }}</p>
        <p class="text-sm text-gray-500">項商品</p>
      </Card>
      
      <Card 
        title="缺貨品項" 
        icon="warning" 
        color="bg-white"
      >
        <p class="text-3xl font-bold text-red-600">{{ outOfStockCount }}</p>
        <p class="text-sm text-gray-500">項商品</p>
      </Card>
    </div>

    <!-- Inventory DataTable -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-gray-900">庫存明細</h2>
        <div class="flex space-x-2">
          <select
            v-model="statusFilter"
            @change="loadInventory"
            class="border border-gray-300 rounded-md px-3 py-2 text-sm"
          >
            <option value="">全部狀態</option>
            <option value="in_stock">有庫存</option>
            <option value="low_stock">低庫存</option>
            <option value="out_of_stock">缺貨</option>
          </select>
          <select
            v-model="locationFilter"
            @change="loadInventory"
            class="border border-gray-300 rounded-md px-3 py-2 text-sm"
          >
            <option value="">全部位置</option>
            <option value="A1">A1區</option>
            <option value="B2">B2區</option>
            <option value="C3">C3區</option>
          </select>
        </div>
      </div>

      <DataTable
        :columns="columns"
        :data="inventory"
        :loading="loading"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        @page-change="handlePageChange"
        @sort="handleSort"
        @search="handleSearch"
        search-placeholder="搜尋商品名稱、SKU或位置..."
      />
    </div>

    <!-- Stock Adjustment Modal -->
    <div v-if="showAdjustmentModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">庫存調整</h3>
            <button 
              @click="closeAdjustmentModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <span class="sr-only">關閉</span>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="handleAdjustment" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  商品 <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="adjustmentForm.product_id"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">請選擇商品</option>
                  <option value="1">iPhone 15 Pro</option>
                  <option value="2">MacBook Air M2</option>
                  <option value="3">iPad Pro 12.9</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  調整類型 <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="adjustmentForm.adjustment_type"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="increase">增加</option>
                  <option value="decrease">減少</option>
                  <option value="set">設定</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  數量 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model.number="adjustmentForm.quantity"
                  type="number"
                  min="1"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  位置
                </label>
                <select
                  v-model="adjustmentForm.location"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="A1-01">A1-01</option>
                  <option value="A1-02">A1-02</option>
                  <option value="B2-15">B2-15</option>
                  <option value="C3-08">C3-08</option>
                </select>
              </div>

              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  調整原因 <span class="text-red-500">*</span>
                </label>
                <textarea
                  v-model="adjustmentForm.reason"
                  rows="3"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="請說明調整原因..."
                ></textarea>
              </div>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeAdjustmentModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-md disabled:opacity-50"
              >
                {{ submitting ? '處理中...' : '確認調整' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Movement Modal -->
    <div v-if="showMovementModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">庫存異動</h3>
            <button 
              @click="closeMovementModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <span class="sr-only">關閉</span>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="handleMovement" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  商品 <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="movementForm.product_id"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">請選擇商品</option>
                  <option value="1">iPhone 15 Pro</option>
                  <option value="2">MacBook Air M2</option>
                  <option value="3">iPad Pro 12.9</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  異動類型 <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="movementForm.movement_type"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="in">入庫</option>
                  <option value="out">出庫</option>
                  <option value="transfer">調撥</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  數量 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model.number="movementForm.quantity"
                  type="number"
                  min="1"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ movementForm.movement_type === 'transfer' ? '目標位置' : '位置' }}
                </label>
                <select
                  v-model="movementForm.location"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="A1-01">A1-01</option>
                  <option value="A1-02">A1-02</option>
                  <option value="B2-15">B2-15</option>
                  <option value="C3-08">C3-08</option>
                </select>
              </div>

              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  備註
                </label>
                <textarea
                  v-model="movementForm.notes"
                  rows="3"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="輸入異動備註..."
                ></textarea>
              </div>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeMovementModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50"
              >
                {{ submitting ? '處理中...' : '確認異動' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Card from '../components/Card.vue'
import DataTable from '../components/DataTable.vue'
import { inventoryAPI } from '../api/inventory'

export default {
  name: 'Inventory',
  components: {
    Card,
    DataTable
  },
  data() {
    return {
      inventory: [],
      loading: false,
      total: 0,
      currentPage: 1,
      pageSize: 10,
      searchQuery: '',
      sortBy: '',
      sortOrder: 'asc',
      statusFilter: '',
      locationFilter: '',
      showAdjustmentModal: false,
      showMovementModal: false,
      submitting: false,
      totalInventoryValue: 0,
      totalItems: 0,
      lowStockCount: 0,
      outOfStockCount: 0,
      adjustmentForm: {
        product_id: '',
        adjustment_type: 'increase',
        quantity: 1,
        location: '',
        reason: ''
      },
      movementForm: {
        product_id: '',
        movement_type: 'in',
        quantity: 1,
        location: '',
        notes: ''
      },
      columns: [
        { key: 'product_name', label: '商品名稱', sortable: true },
        { key: 'sku', label: 'SKU', sortable: true },
        { key: 'quantity_on_hand', label: '現有庫存', sortable: true },
        { key: 'reorder_level', label: '再訂購點', sortable: true },
        { key: 'location', label: '位置', sortable: true },
        { key: 'unit_cost', label: '成本', sortable: true },
        { key: 'total_value', label: '總值', sortable: true },
        { key: 'status', label: '狀態', sortable: true },
        { key: 'last_updated', label: '最後更新', sortable: true },
        { key: 'actions', label: '操作', sortable: false }
      ]
    }
  },
  async created() {
    await this.loadInventory()
    await this.loadStatistics()
  },
  methods: {
    async loadInventory() {
      try {
        this.loading = true
        
        const params = {
          page: this.currentPage,
          per_page: this.pageSize
        }
        
        if (this.searchQuery) params.search = this.searchQuery
        if (this.statusFilter === 'low_stock') params.low_stock = true
        if (this.locationFilter) params.location_id = this.locationFilter
        
        const response = await inventoryAPI.fetchInventory(params)
        
        // Format data for display
        this.inventory = response.data.data.map(item => ({
          ...item,
          sku: `SKU-${item.product_id}`,
          quantity_on_hand: item.quantity,
          reorder_level: 10, // Default reorder level
          location: `${item.location_zone}-${item.location_shelf}`,
          unit_cost: 50, // Default unit cost
          total_value: `$${(item.quantity * 50).toFixed(2)}`,
          status: this.getStockStatusFromAPI(item.stock_status),
          last_updated: this.formatDate(new Date()),
          actions: [
            {
              label: '調整',
              action: () => this.adjustStock(item),
              class: 'text-green-600 hover:text-green-900'
            },
            {
              label: '異動',
              action: () => this.moveStock(item),
              class: 'text-blue-600 hover:text-blue-900'
            },
            {
              label: '記錄',
              action: () => this.viewHistory(item),
              class: 'text-purple-600 hover:text-purple-900'
            }
          ]
        }))
        
        this.total = response.data.pagination.total
        
      } catch (error) {
        console.error('Error loading inventory:', error)
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: '載入庫存資料失敗'
        })
      } finally {
        this.loading = false
      }
    },

    async loadStatistics() {
      try {
        const response = await inventoryAPI.fetchInventoryStats()
        const stats = response.data.data
        
        this.totalInventoryValue = parseInt(stats.total_items) * 50 // Rough estimate
        this.totalItems = parseInt(stats.total_items)
        this.lowStockCount = stats.low_stock_items
        this.outOfStockCount = stats.critical_stock_items
      } catch (error) {
        console.error('Error loading statistics:', error)
      }
    },

    calculateStatistics(inventoryData) {
      // This method is now replaced by loadStatistics()
    },

    handlePageChange(page) {
      this.currentPage = page
      this.loadInventory()
    },

    handleSort({ sortBy, sortOrder }) {
      this.sortBy = sortBy
      this.sortOrder = sortOrder
      this.loadInventory()
    },

    handleSearch(query) {
      this.searchQuery = query
      this.currentPage = 1
      this.loadInventory()
    },

    getStockStatusFromAPI(status) {
      const statusMap = {
        'Critical': '缺貨',
        'Low': '低庫存',
        'Good': '正常'
      }
      return statusMap[status] || '正常'
    },

    openAdjustmentModal() {
      this.resetAdjustmentForm()
      this.showAdjustmentModal = true
    },

    openMovementModal() {
      this.resetMovementForm()
      this.showMovementModal = true
    },

    closeAdjustmentModal() {
      this.showAdjustmentModal = false
      this.resetAdjustmentForm()
    },

    closeMovementModal() {
      this.showMovementModal = false
      this.resetMovementForm()
    },

    adjustStock(item) {
      this.adjustmentForm.product_id = item.id
      this.adjustmentForm.location = item.location
      this.showAdjustmentModal = true
    },

    moveStock(item) {
      this.movementForm.product_id = item.id
      this.movementForm.location = item.location
      this.showMovementModal = true
    },

    viewHistory(item) {
      console.log('Viewing history for item:', item.id)
    },

    async handleAdjustment() {
      try {
        this.submitting = true
        
        console.log('Processing stock adjustment:', this.adjustmentForm)
        
        this.$store.dispatch('setNotification', {
          type: 'success',
          message: '庫存調整成功'
        })
        
        this.closeAdjustmentModal()
        await this.loadInventory()
        await this.loadStatistics()
        
      } catch (error) {
        console.error('Error adjusting stock:', error)
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: '庫存調整失敗'
        })
      } finally {
        this.submitting = false
      }
    },

    async handleMovement() {
      try {
        this.submitting = true
        
        console.log('Processing stock movement:', this.movementForm)
        
        this.$store.dispatch('setNotification', {
          type: 'success',
          message: '庫存異動成功'
        })
        
        this.closeMovementModal()
        await this.loadInventory()
        await this.loadStatistics()
        
      } catch (error) {
        console.error('Error processing movement:', error)
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: '庫存異動失敗'
        })
      } finally {
        this.submitting = false
      }
    },

    resetAdjustmentForm() {
      this.adjustmentForm = {
        product_id: '',
        adjustment_type: 'increase',
        quantity: 1,
        location: '',
        reason: ''
      }
    },

    resetMovementForm() {
      this.movementForm = {
        product_id: '',
        movement_type: 'in',
        quantity: 1,
        location: '',
        notes: ''
      }
    },

    getStockStatus(item) {
      if (item.quantity_on_hand === 0) {
        return '缺貨'
      } else if (item.quantity_on_hand <= item.reorder_level) {
        return '低庫存'
      } else {
        return '正常'
      }
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString('zh-TW')
    }
  }
}
</script> 