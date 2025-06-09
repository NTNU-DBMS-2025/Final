<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">倉位管理</h1>
          <p class="text-gray-600">管理倉庫位置、區域與空間配置</p>
        </div>
        <div class="flex space-x-2">
          <button 
            @click="loadLocations"
            class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center"
          >
            <span class="mr-2">🔄</span>
            重新載入
          </button>
        <button 
          @click="openAddModal"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center"
        >
          <span class="mr-2">+</span>
          新增倉位
        </button>
        </div>
      </div>
    </div>

    <!-- Locations DataTable -->
    <div class="bg-white shadow rounded-lg p-6">
      <DataTable
        :columns="columns"
        :data="locations"
        :actions="actions"
        :loading="loading"
        @sort="handleSort"
        @search="handleSearch"
        @edit="editLocation"
        @view="viewLocation"
        search-placeholder="搜尋位置編號、區域或類型..."
      />
      

    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">
              {{ isEditMode ? '編輯倉位' : '新增倉位' }}
            </h3>
            <button 
              @click="closeModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <span class="sr-only">關閉</span>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  位置編號 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.location_code"
                  type="text"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  位置名稱 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.location_name"
                  type="text"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  區域
                </label>
                <select
                  v-model="form.zone"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">請選擇區域</option>
                  <option value="A">A區</option>
                  <option value="B">B區</option>
                  <option value="C">C區</option>
                  <option value="D">D區</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  位置類型
                </label>
                <select
                  v-model="form.location_type"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">請選擇類型</option>
                  <option value="storage">一般儲存</option>
                  <option value="picking">揀貨區</option>
                  <option value="receiving">收貨區</option>
                  <option value="shipping">出貨區</option>
                  <option value="staging">暫存區</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  狀態
                </label>
                <select
                  v-model="form.status"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="active">可用</option>
                  <option value="occupied">使用中</option>
                  <option value="maintenance">維護中</option>
                  <option value="disabled">停用</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  容量
                </label>
                <input
                  v-model.number="form.capacity"
                  type="number"
                  min="0"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  備註
                </label>
                <textarea
                  v-model="form.notes"
                  rows="3"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                ></textarea>
              </div>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50"
              >
                {{ submitting ? '處理中...' : (isEditMode ? '更新' : '新增') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- View Location Details Modal -->
    <div v-if="showViewModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-2/3 lg:w-1/2 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">
              倉位詳細資訊
            </h3>
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

          <div v-if="selectedLocation" class="space-y-6">
            <!-- Basic Information -->
            <div class="bg-blue-50 rounded-lg p-4">
              <h4 class="text-md font-semibold text-blue-900 mb-3">基本資訊</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="font-medium text-gray-700">位置編號:</span>
                    <span class="text-gray-900">{{ selectedLocation.location_code }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="font-medium text-gray-700">位置名稱:</span>
                    <span class="text-gray-900">{{ selectedLocation.location_name }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="font-medium text-gray-700">區域:</span>
                    <span class="text-gray-900">{{ selectedLocation.zone }}</span>
                  </div>
                </div>
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="font-medium text-gray-700">類型:</span>
                    <span class="text-gray-900">{{ selectedLocation.location_type }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="font-medium text-gray-700">容量:</span>
                    <span class="text-gray-900">{{ selectedLocation.capacity || 'N/A' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="font-medium text-gray-700">狀態:</span>
                    <span :class="getStatusBadgeClass(selectedLocation.status_key)" class="px-2 py-1 rounded-full text-xs font-medium">
                      {{ selectedLocation.status }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Utilization Information -->
            <div class="bg-green-50 rounded-lg p-4">
              <h4 class="text-md font-semibold text-green-900 mb-3">使用率資訊</h4>
              <div class="space-y-3">
                <div class="flex justify-between items-center">
                  <span class="font-medium text-gray-700">目前使用率:</span>
                  <span class="text-lg font-bold text-green-600">{{ selectedLocation.utilization }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-3">
                  <div 
                    class="bg-green-500 h-3 rounded-full transition-all duration-300" 
                    :style="{ width: selectedLocation.utilization }"
                  ></div>
                </div>
                <div class="text-sm text-gray-600">
                  <span v-if="getUtilizationRate(selectedLocation.utilization) >= 90" class="text-red-600">⚠️ 使用率過高</span>
                  <span v-else-if="getUtilizationRate(selectedLocation.utilization) >= 70" class="text-yellow-600">⚡ 使用率偏高</span>
                  <span v-else class="text-green-600">✅ 使用率正常</span>
                </div>
              </div>
            </div>

            <!-- Additional Information -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="text-md font-semibold text-gray-900 mb-3">其他資訊</h4>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span class="font-medium text-gray-700">建立時間:</span>
                  <span class="text-gray-900">{{ formatDateTime(selectedLocation.created_at) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="font-medium text-gray-700">最後更新:</span>
                  <span class="text-gray-900">{{ formatDateTime(selectedLocation.updated_at) }}</span>
                </div>
                <div v-if="selectedLocation.notes" class="mt-3">
                  <span class="font-medium text-gray-700">備註:</span>
                  <p class="mt-1 text-gray-900 bg-white p-2 rounded border">{{ selectedLocation.notes }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="flex justify-end pt-4 border-t border-gray-200 mt-6">
            <button
              @click="closeViewModal"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors mr-3"
            >
              關閉
            </button>
            <button
              @click="editFromView"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md transition-colors"
            >
              編輯此倉位
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DataTable from '../components/DataTable.vue'
import { fetchLocations, createLocation, updateLocation } from '../api/locations'

export default {
  name: 'Locations',
  components: {
    DataTable
  },
  data() {
    return {
      locations: [],
      loading: false,
      total: 0,
      currentPage: 1,
      pageSize: 10,
      searchQuery: '',
      sortBy: '',
      sortOrder: 'asc',
      showModal: false,
      showViewModal: false,
      isEditMode: false,
      submitting: false,
      editingId: null,
      selectedLocation: null,
      form: {
        location_code: '',
        location_name: '',
        zone: '',
        location_type: '',
        status: 'active',
        capacity: 0,
        notes: ''
      },
      columns: [
        { key: 'location_code', label: '位置編號', sortable: true },
        { key: 'location_name', label: '位置名稱', sortable: true },
        { key: 'zone', label: '區域', sortable: true },
        { key: 'location_type', label: '類型', sortable: true },
        { key: 'capacity', label: '容量', sortable: true },
        { key: 'utilization', label: '使用率', sortable: true },
        { key: 'status', label: '狀態', sortable: true }
      ],
             actions: [
         {
           name: 'edit',
           label: '編輯',
           event: 'edit',
           type: 'edit'
         },
         {
           name: 'view',
           label: '查看',
           event: 'view',
           type: 'view'
         }
       ]
    }
  },
  async created() {
    await this.loadLocations()
  },
  methods: {
    async loadLocations() {
      try {
        console.log('🔄 Starting to load locations...')
        this.loading = true
        
        const params = {
          per_page: 1000 // Load all locations for client-side sorting
        }
        
        console.log('📡 Calling API with params:', params)
        const response = await fetchLocations(params)
        console.log('📦 Raw API response:', response)
        
        if (response && response.data && response.data.success && response.data.data) {
          console.log('✅ API call successful, processing data...')
          
          this.locations = response.data.data.map(location => {
            const processed = {
              ...location,
              id: location.location_id,
              location_type_key: location.location_type,
          location_type: this.getLocationTypeText(location.location_type),
              status_key: location.status,
              status: this.getStatusText(location.status),
              utilization: `${location.utilization_rate}%`
            }
            console.log('📍 Processed location:', processed)
            return processed
          })
          
          // Remove total for client-side mode
          console.log(`📊 Loaded ${this.locations.length} locations, total: ${this.total}`)
          
        } else {
          console.error('❌ Invalid API response structure:', response)
          this.locations = []
          this.total = 0
        }
        
      } catch (error) {
        console.error('💥 Error loading locations:', error)
        this.$message && this.$message.error('載入倉位資料失敗: ' + error.message)
        this.locations = []
        this.total = 0
      } finally {
        this.loading = false
        console.log('🏁 Loading complete. Final locations:', this.locations)
      }
    },

    handleSort({ sortBy, sortOrder }) {
      // Client-side sorting handled by DataTable
      console.log('Sorting by:', sortBy, sortOrder)
    },

    handleSearch(query) {
      this.searchQuery = query
      // Client-side search handled by DataTable
    },

    openAddModal() {
      this.isEditMode = false
      this.editingId = null
      this.resetForm()
      this.showModal = true
    },

    editLocation(location) {
      this.isEditMode = true
      this.editingId = location.id
      this.form = {
        location_code: location.location_code,
        location_name: location.location_name,
        zone: location.zone,
        location_type: location.location_type_key || '',
        status: location.status_key || 'active',
        capacity: location.capacity,
        notes: location.notes || ''
      }
      this.showModal = true
    },

    viewLocation(location) {
      console.log('Viewing location:', location)
      this.selectedLocation = location
      this.showViewModal = true
    },

    closeViewModal() {
      this.showViewModal = false
      this.selectedLocation = null
    },

    editFromView() {
      // Close view modal and open edit modal with current location
      this.closeViewModal()
      this.editLocation(this.selectedLocation)
    },

    async handleSubmit() {
      try {
        this.submitting = true
        
        if (this.isEditMode) {
          await updateLocation(this.editingId, this.form)
          this.$message && this.$message.success('倉位更新成功')
        } else {
          await createLocation(this.form)
          this.$message && this.$message.success('倉位建立成功')
        }
        
        this.closeModal()
        await this.loadLocations()
        
      } catch (error) {
        console.error('Error saving location:', error)
        this.$message && this.$message.error(this.isEditMode ? '倉位更新失敗' : '倉位建立失敗')
      } finally {
        this.submitting = false
      }
    },

    closeModal() {
      this.showModal = false
      this.resetForm()
    },

    resetForm() {
      this.form = {
        location_code: '',
        location_name: '',
        zone: '',
        location_type: '',
        status: 'active',
        capacity: 0,
        notes: ''
      }
    },

    getLocationTypeText(type) {
      const types = {
        'storage': '一般儲存',
        'picking': '揀貨區',
        'receiving': '收貨區',
        'shipping': '出貨區',
        'staging': '暫存區'
      }
      return types[type] || type
    },

    getStatusText(status) {
      const statuses = {
        'active': '可用',
        'occupied': '使用中',
        'maintenance': '維護中',
        'disabled': '停用'
      }
      return statuses[status] || status
    },

    getStatusBadgeClass(status) {
      const classes = {
        'active': 'bg-green-100 text-green-800',
        'occupied': 'bg-yellow-100 text-yellow-800',
        'maintenance': 'bg-orange-100 text-orange-800',
        'disabled': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },

    getUtilizationRate(utilization) {
      // Extract percentage number from string like "80%"
      return parseInt(utilization.replace('%', ''))
    },

    formatDateTime(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script> 