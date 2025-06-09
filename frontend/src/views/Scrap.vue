<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
     <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">報廢管理</h1>
          <p class="text-gray-600">顯示所有報廢的物品。</p>
        </div>
        <button 
          @click="showModal = true"
          class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          <span class="mr-2">+</span>
          新增報廢
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="space-y-6">
      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6 mt-6">
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center">
            <div class="p-2 bg-red-100 rounded-lg">
              <i class="fas fa-trash text-red-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">本月報廢</p>
              <p class="text-2xl font-bold text-gray-900">{{ monthlyScrap }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center">
            <div class="p-2 bg-orange-100 rounded-lg">
              <i class="fas fa-dollar-sign text-orange-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">報廢價值</p>
              <p class="text-2xl font-bold text-gray-900">NT$ {{ scrapValue.toLocaleString() }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center">
            <div class="p-2 bg-yellow-100 rounded-lg">
              <i class="fas fa-exclamation-triangle text-yellow-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">待處理</p>
              <p class="text-2xl font-bold text-gray-900">{{ pendingScrap }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center">
            <div class="p-2 bg-green-100 rounded-lg">
              <i class="fas fa-check text-green-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">已處理</p>
              <p class="text-2xl font-bold text-gray-900">{{ processedScrap }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">搜尋</label>
            <input
              v-model="searchTerm"
              type="text"
              placeholder="搜尋產品名稱或報廢原因..."
              class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">狀態</label>
            <select
              v-model="statusFilter"
              class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">全部狀態</option>
              <option value="待處理">待處理</option>
              <option value="已處理">已處理</option>
              <option value="已取消">已取消</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">報廢原因</label>
            <select
              v-model="reasonFilter"
              class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">全部原因</option>
              <option value="過期">過期</option>
              <option value="損壞">損壞</option>
              <option value="品質不良">品質不良</option>
              <option value="其他">其他</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">日期範圍</label>
            <input
              v-model="dateFilter"
              type="date"
              class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>
        </div>
      </div>

      <!-- Scrap Table -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <DataTable
          :columns="columns"
          :data="scrapItemsWithActions"
          :loading="loading"
          @sort="handleSort"
          @viewScrapItem="viewScrapItem"
          @editScrapItem="editScrapItem"
          @processScrapItem="processScrapItem"
        />
      </div>
    </div>

    <!-- Modal for Create/Edit -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="closeModal"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ isEditing ? '編輯報廢記錄' : '新增報廢記錄' }}
          </h3>
          
          <form @submit.prevent="submitForm" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">產品ID</label>
                <input
                  v-model="form.product_id"
                  type="number"
                  required
                  placeholder="輸入產品ID"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">儲位ID</label>
                <input
                  v-model="form.location_id"
                  type="number"
                  required
                  placeholder="輸入儲位ID"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">數量</label>
                <input
                  v-model="form.quantity"
                  type="number"
                  min="1"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">建立人</label>
                <input
                  v-model="form.created_by"
                  type="text"
                  placeholder="輸入建立人姓名"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">報廢原因</label>
                <select
                  v-model="form.reason"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">選擇報廢原因</option>
                  <option value="過期">過期</option>
                  <option value="損壞">損壞</option>
                  <option value="品質不良">品質不良</option>
                  <option value="其他">其他</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">狀態</label>
                <select
                  v-model="form.status"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="待處理">待處理</option>
                  <option value="已處理">已處理</option>
                  <option value="已取消">已取消</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">預估價值</label>
                <input
                  v-model="form.estimated_value"
                  type="number"
                  min="0"
                  step="0.01"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">處理日期</label>
                <input
                  v-model="form.processed_date"
                  type="date"
                  :disabled="form.status !== '已處理'"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
                >
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">詳細描述</label>
              <textarea
                v-model="form.description"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              ></textarea>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                取消
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              >
                {{ isEditing ? '更新' : '新增' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- View Modal -->
    <div
      v-if="showViewModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="closeViewModal"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">報廢記錄詳情</h3>
            <button 
              @click="closeViewModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <span class="sr-only">關閉</span>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div v-if="viewingItem" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-gray-50 p-4 rounded-lg">
                <label class="block text-sm font-medium text-gray-700 mb-1">報廢編號</label>
                <p class="text-gray-900">{{ viewingItem.scrap_id }}</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg">
                <label class="block text-sm font-medium text-gray-700 mb-1">產品名稱</label>
                <p class="text-gray-900">{{ viewingItem.product_name }}</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg">
                <label class="block text-sm font-medium text-gray-700 mb-1">產品ID</label>
                <p class="text-gray-900">{{ viewingItem.product_id }}</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg">
                <label class="block text-sm font-medium text-gray-700 mb-1">儲位ID</label>
                <p class="text-gray-900">{{ viewingItem.location_id }}</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg">
                <label class="block text-sm font-medium text-gray-700 mb-1">報廢數量</label>
                <p class="text-gray-900 font-semibold">{{ viewingItem.quantity }}</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg">
                <label class="block text-sm font-medium text-gray-700 mb-1">報廢原因</label>
                <p class="text-gray-900">{{ viewingItem.reason }}</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg">
                <label class="block text-sm font-medium text-gray-700 mb-1">預估價值</label>
                <p class="text-gray-900 font-semibold text-green-600">NT$ {{ Number(viewingItem.estimated_value || 0).toLocaleString() }}</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg">
                <label class="block text-sm font-medium text-gray-700 mb-1">狀態</label>
                <span :class="getStatusClass(viewingItem.status)">
                  {{ viewingItem.status }}
                </span>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg">
                <label class="block text-sm font-medium text-gray-700 mb-1">報廢日期</label>
                <p class="text-gray-900">{{ formatDate(viewingItem.scrap_date) }}</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg">
                <label class="block text-sm font-medium text-gray-700 mb-1">建立人</label>
                <p class="text-gray-900">{{ viewingItem.created_by }}</p>
              </div>
            </div>
            
            <div v-if="viewingItem.description" class="bg-gray-50 p-4 rounded-lg">
              <label class="block text-sm font-medium text-gray-700 mb-1">詳細描述</label>
              <p class="text-gray-900">{{ viewingItem.description }}</p>
            </div>
            
            <div class="flex justify-end space-x-3 pt-4">
              <button
                v-if="viewingItem.status === '待處理'"
                @click="editScrapItem(viewingItem); closeViewModal()"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                編輯此記錄
              </button>
              <button
                v-if="viewingItem.status === '待處理'"
                @click="processScrapItem(viewingItem); closeViewModal()"
                class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              >
                處理此記錄
              </button>
              <button
                @click="closeViewModal"
                class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                關閉
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DataTable from '../components/DataTable.vue'
import { fetchScrapRecords, fetchScrapStats, createScrapRecord, updateScrapRecord, processScrapRecord, deleteScrapRecord } from '@/api/scrap'

export default {
  name: 'Scrap',
  components: {
    DataTable
  },
  data() {
    return {
      loading: false,
      showModal: false,
      showViewModal: false,
      isEditing: false,
      viewingItem: null,
      searchTerm: '',
      statusFilter: '',
      reasonFilter: '',
      dateFilter: '',
      scrapItems: [],
      stats: {
        monthly_scrap: 0,
        total_estimated_value: 0,
        pending_count: 0,
        processed_count: 0
      },
      form: {
        product_id: '',
        location_id: '',
        quantity: 1,
        reason: '',
        estimated_value: 0,
        description: '',
        status: '待處理',
        created_by: ''
      },
      columns: [
        { key: 'scrap_id', label: '報廢編號', sortable: true },
        { key: 'product_name', label: '產品名稱', sortable: true },
        { key: 'quantity', label: '數量', sortable: true },
        { key: 'reason', label: '報廢原因', sortable: true },
        { key: 'status', label: '狀態', sortable: true },
        { key: 'estimated_value', label: '預估價值', sortable: true },
        { key: 'scrap_date', label: '報廢日期', sortable: true },
        { key: 'created_by', label: '建立人', sortable: true },
        { key: 'actions', label: '操作', sortable: false }
      ]
    }
  },
  computed: {
    filteredScrapItems() {
      let filtered = this.scrapItems

      if (this.searchTerm) {
        filtered = filtered.filter(item =>
          item.product_name.includes(this.searchTerm) ||
          item.reason.includes(this.searchTerm) ||
          item.description.includes(this.searchTerm)
        )
      }

      if (this.statusFilter) {
        filtered = filtered.filter(item => item.status === this.statusFilter)
      }

      if (this.reasonFilter) {
        filtered = filtered.filter(item => item.reason === this.reasonFilter)
      }

      if (this.dateFilter) {
        filtered = filtered.filter(item => item.created_date === this.dateFilter)
      }

      return filtered
    },
    scrapItemsWithActions() {
      return this.filteredScrapItems.map(item => ({
        ...item,
        actions: this.getActionsForItem(item)
      }))
    },
    monthlyScrap() {
      return this.stats.monthly_scrap
    },
    scrapValue() {
      return this.stats.total_estimated_value
    },
    pendingScrap() {
      return this.stats.pending_count
    },
    processedScrap() {
      return this.stats.processed_count
    }
  },
  methods: {
    getActionsForItem(item) {
      const actions = [
        {
          label: '查看',
          action: () => this.viewScrapItem(item),
          class: 'text-gray-600 hover:text-gray-900'
        }
      ]

      // Only show edit and process buttons for pending items
      if (item.status === '待處理') {
        actions.push({
          label: '編輯',
          action: () => this.editScrapItem(item),
          class: 'text-blue-600 hover:text-blue-900'
        })
        actions.push({
          label: '處理',
          action: () => this.processScrapItem(item),
          class: 'text-red-600 hover:text-red-900'
        })
      }

      return actions
    },
    async loadScrapData() {
      try {
        this.loading = true
        const [scrapResponse, statsResponse] = await Promise.all([
          fetchScrapRecords({ page: 1, per_page: 100 }),
          fetchScrapStats()
        ])
        
        if (scrapResponse.data.success) {
          this.scrapItems = scrapResponse.data.data
        }
        
        if (statsResponse.data.success) {
          this.stats = statsResponse.data.data
        }
      } catch (error) {
        console.error('Failed to load scrap data:', error)
        alert('載入報廢資料失敗')
      } finally {
        this.loading = false
      }
    },
    handleSort({ sortBy, sortOrder }) {
      console.log('Sorting by:', sortBy, sortOrder)
      // Handle sorting logic here - for now just log it
    },
    viewScrapItem(item) {
      console.log('Viewing scrap item:', item)
      this.viewingItem = item
      this.showViewModal = true
    },
    closeViewModal() {
      this.showViewModal = false
      this.viewingItem = null
    },
    editScrapItem(item) {
      this.isEditing = true
      this.form = { ...item }
      this.showModal = true
    },
    async processScrapItem(item) {
      // Check if already processed
      if (item.status === '已處理') {
        this.$store.dispatch('setNotification', {
          type: 'warning',
          message: '此報廢記錄已經處理過了'
        })
        return
      }

      if (confirm('確定要處理此報廢記錄嗎？處理後將無法再修改。')) {
        try {
          console.log('Processing scrap item:', item)
          const response = await processScrapRecord(item.scrap_id)
          console.log('Process response:', response)
          
          if (response.data.success) {
            await this.loadScrapData() // Reload data
            this.$store.dispatch('setNotification', {
              type: 'success',
              message: '報廢記錄已處理完成'
            })
          } else {
            throw new Error(response.data.error || '處理失敗')
          }
        } catch (error) {
          console.error('Failed to process scrap item:', error)
          
          // Get more specific error message
          let errorMessage = '處理報廢記錄失敗'
          if (error.response?.data?.error) {
            errorMessage = error.response.data.error
            
            // Handle specific error cases
            if (errorMessage.includes('already processed')) {
              errorMessage = '此報廢記錄已經處理過了'
              // Reload data to sync status
              await this.loadScrapData()
            }
          } else if (error.response?.data?.message) {
            errorMessage = error.response.data.message
          } else if (error.message) {
            errorMessage = error.message
          }
          
          this.$store.dispatch('setNotification', {
            type: 'error',
            message: errorMessage
          })
          
          // Log full error details for debugging
          console.error('Full error details:', {
            status: error.response?.status,
            statusText: error.response?.statusText,
            data: error.response?.data,
            config: error.config
          })
        }
      }
    },
    closeModal() {
      this.showModal = false
      this.isEditing = false
      this.resetForm()
    },
    resetForm() {
      this.form = {
        product_id: '',
        location_id: '',
        quantity: 1,
        reason: '',
        estimated_value: 0,
        description: '',
        status: '待處理',
        created_by: ''
      }
    },
    async submitForm() {
      try {
        if (this.isEditing) {
          const response = await updateScrapRecord(this.form.scrap_id, this.form)
          if (response.data.success) {
            await this.loadScrapData()
            alert('報廢記錄已更新')
          }
        } else {
          const response = await createScrapRecord(this.form)
          if (response.data.success) {
            await this.loadScrapData()
            alert('報廢記錄已新增')
          }
        }
        this.closeModal()
      } catch (error) {
        console.error('Failed to submit form:', error)
        alert(this.isEditing ? '更新報廢記錄失敗' : '新增報廢記錄失敗')
      }
    },
    getStatusClass(status) {
      const baseClass = 'inline-flex px-2 py-1 text-xs font-semibold rounded-full'
      switch (status) {
        case '待處理':
          return `${baseClass} bg-yellow-100 text-yellow-800`
        case '已處理':
          return `${baseClass} bg-green-100 text-green-800`
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
  },
  mounted() {
    this.loadScrapData()
  }
}
</script> 