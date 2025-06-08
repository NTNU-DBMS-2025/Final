<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-900">報廢管理</h1>
          <button
            @click="showModal = true"
            class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            <i class="fas fa-plus mr-2"></i>
            新增報廢
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
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
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">狀態</label>
            <select
              v-model="statusFilter"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">全部狀態</option>
              <option value="待處理">待處理</option>
              <option value="處理中">處理中</option>
              <option value="已處理">已處理</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">報廢原因</label>
            <select
              v-model="reasonFilter"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
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
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>
        </div>
      </div>

      <!-- Scrap Table -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <DataTable
          :columns="columns"
          :data="filteredScrapItems"
          :loading="loading"
          @sort="handleSort"
        >
          <template #actions="{ row }">
            <div class="flex space-x-2">
              <button
                @click="viewScrapItem(row)"
                class="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                查看
              </button>
              <button
                v-if="row.status === '待處理'"
                @click="editScrapItem(row)"
                class="text-green-600 hover:text-green-800 text-sm font-medium"
              >
                編輯
              </button>
              <button
                v-if="row.status === '待處理'"
                @click="processScrapItem(row)"
                class="text-orange-600 hover:text-orange-800 text-sm font-medium"
              >
                處理
              </button>
            </div>
          </template>
        </DataTable>
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
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">儲位ID</label>
                <input
                  v-model="form.location_id"
                  type="number"
                  required
                  placeholder="輸入儲位ID"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">建立人</label>
                <input
                  v-model="form.created_by"
                  type="text"
                  placeholder="輸入建立人姓名"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">報廢原因</label>
                <select
                  v-model="form.reason"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">選擇報廢原因</option>
                  <option value="過期">過期</option>
                  <option value="損壞">損壞</option>
                  <option value="品質不良">品質不良</option>
                  <option value="其他">其他</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">預估價值</label>
                <input
                  v-model="form.estimated_value"
                  type="number"
                  min="0"
                  step="0.01"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">詳細描述</label>
              <textarea
                v-model="form.description"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
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
      isEditing: false,
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
    handleSort(column) {
      console.log('Sorting by:', column)
    },
    viewScrapItem(item) {
      console.log('Viewing scrap item:', item)
    },
    editScrapItem(item) {
      this.isEditing = true
      this.form = { ...item }
      this.showModal = true
    },
    async processScrapItem(item) {
      if (confirm('確定要處理此報廢記錄嗎？')) {
        try {
          const response = await processScrapRecord(item.scrap_id)
          if (response.data.success) {
            await this.loadScrapData() // Reload data
            alert('報廢記錄已處理')
          }
        } catch (error) {
          console.error('Failed to process scrap item:', error)
          alert('處理報廢記錄失敗')
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
    }
  },
  mounted() {
    this.loadScrapData()
  }
}
</script> 