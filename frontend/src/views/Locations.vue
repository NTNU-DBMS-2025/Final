<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">倉位管理</h1>
          <p class="text-gray-600">管理倉庫位置、區域與空間配置</p>
        </div>
        <button 
          @click="openAddModal"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center"
        >
          <span class="mr-2">+</span>
          新增倉位
        </button>
      </div>
    </div>

    <!-- Locations DataTable -->
    <div class="bg-white shadow rounded-lg p-6">
      <DataTable
        :columns="columns"
        :data="locations"
        :actions="actions"
        :loading="loading"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        @page-change="handlePageChange"
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
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  區域
                </label>
                <select
                  v-model="form.zone"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  備註
                </label>
                <textarea
                  v-model="form.notes"
                  rows="3"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
  </div>
</template>

<script>
import DataTable from '../components/DataTable.vue'

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
      isEditMode: false,
      submitting: false,
      editingId: null,
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
        this.loading = true
        
        // Mock API call
        const mockLocations = [
          {
            id: 1,
            location_code: 'A1-01',
            location_name: 'A區第1排第1位',
            zone: 'A',
            location_type: 'storage',
            capacity: 100,
            current_stock: 85,
            status: 'occupied',
            notes: '主要儲存區'
          },
          {
            id: 2,
            location_code: 'A1-02',
            location_name: 'A區第1排第2位',
            zone: 'A',
            location_type: 'storage',
            capacity: 100,
            current_stock: 20,
            status: 'active',
            notes: ''
          },
          {
            id: 3,
            location_code: 'B2-15',
            location_name: 'B區第2排第15位',
            zone: 'B',
            location_type: 'picking',
            capacity: 50,
            current_stock: 45,
            status: 'occupied',
            notes: '揀貨專用區'
          }
        ]
        
        this.locations = mockLocations.map(location => ({
          ...location,
          location_type: this.getLocationTypeText(location.location_type),
          utilization: `${Math.round((location.current_stock / location.capacity) * 100)}%`,
          status: this.getStatusText(location.status)
        }))
        
        this.total = mockLocations.length
        
      } catch (error) {
        console.error('Error loading locations:', error)
      } finally {
        this.loading = false
      }
    },

    handlePageChange(page) {
      this.currentPage = page
      this.loadLocations()
    },

    handleSort({ sortBy, sortOrder }) {
      this.sortBy = sortBy
      this.sortOrder = sortOrder
      this.loadLocations()
    },

    handleSearch(query) {
      this.searchQuery = query
      this.currentPage = 1
      this.loadLocations()
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
      console.log('Viewing location:', location.id)
    },

    async handleSubmit() {
      try {
        this.submitting = true
        console.log(this.isEditMode ? 'Updating' : 'Creating', this.form)
        this.closeModal()
        await this.loadLocations()
      } catch (error) {
        console.error('Error saving location:', error)
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
    }
  }
}
</script> 