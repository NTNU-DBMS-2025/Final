<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">客戶管理</h1>
          <p class="text-gray-600">管理所有客戶資料與聯絡資訊</p>
        </div>
        <button 
          @click="openAddModal"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center"
        >
          <span class="mr-2">+</span>
          新增客戶
        </button>
      </div>
    </div>

    <!-- Customers DataTable -->
    <div class="bg-white shadow rounded-lg p-6">
      <DataTable
        :columns="columns"
        :data="customers"
        :actions="actions"
        :loading="loading"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        @page-change="handlePageChange"
        @sort="handleSort"
        @search="handleSearch"
        @edit="editCustomer"
        @view="viewOrders"
        @delete="deleteCustomer"
        search-placeholder="搜尋客戶名稱、聯絡人或電話..."
      />
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">
              {{ isEditMode ? '編輯客戶' : '新增客戶' }}
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
                  客戶名稱 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.customer_name"
                  type="text"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  聯絡人姓名 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.contact_name"
                  type="text"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  聯絡電話 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.phone"
                  type="tel"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  電子郵件 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.email"
                  type="email"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  地址
                </label>
                <textarea
                  v-model="form.address"
                  rows="3"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                ></textarea>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  客戶類型
                </label>
                <select
                  v-model="form.customer_type"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">請選擇類型</option>
                  <option value="individual">個人</option>
                  <option value="business">企業</option>
                  <option value="government">政府機關</option>
                  <option value="educational">教育機構</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  客戶等級
                </label>
                <select
                  v-model="form.customer_level"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">請選擇等級</option>
                  <option value="bronze">銅級</option>
                  <option value="silver">銀級</option>
                  <option value="gold">金級</option>
                  <option value="platinum">白金級</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  統一編號
                </label>
                <input
                  v-model="form.tax_id"
                  type="text"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  狀態
                </label>
                <select
                  v-model="form.status"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="active">啟用</option>
                  <option value="inactive">停用</option>
                  <option value="suspended">暫停</option>
                </select>
              </div>

              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  備註
                </label>
                <textarea
                  v-model="form.notes"
                  rows="2"
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

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
            <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 19.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mt-2">確認刪除</h3>
          <div class="mt-2 px-7 py-3">
            <p class="text-sm text-gray-500">
              您確定要刪除客戶「{{ deleteItem?.customer_name }}」嗎？此操作無法復原。
            </p>
          </div>
          <div class="flex justify-center space-x-3 mt-4">
            <button
              @click="closeDeleteModal"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
            >
              取消
            </button>
            <button
              @click="confirmDelete"
              :disabled="submitting"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-md disabled:opacity-50"
            >
              {{ submitting ? '刪除中...' : '確認刪除' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DataTable from '../components/DataTable.vue'

export default {
  name: 'Customers',
  components: {
    DataTable
  },
  data() {
    return {
      customers: [],
      loading: false,
      total: 0,
      currentPage: 1,
      pageSize: 10,
      searchQuery: '',
      sortBy: '',
      sortOrder: 'asc',
      showModal: false,
      showDeleteModal: false,
      isEditMode: false,
      submitting: false,
      editingId: null,
      deleteItem: null,
      form: {
        customer_name: '',
        contact_name: '',
        phone: '',
        email: '',
        address: '',
        customer_type: '',
        customer_level: '',
        tax_id: '',
        status: 'active',
        notes: ''
      },
      columns: [
        { key: 'customer_name', label: '客戶名稱', sortable: true },
        { key: 'contact_name', label: '聯絡人', sortable: true },
        { key: 'phone', label: '電話', sortable: false },
        { key: 'email', label: '電子郵件', sortable: false },
        { key: 'customer_type', label: '類型', sortable: true },
        { key: 'customer_level', label: '等級', sortable: true },
        { key: 'status', label: '狀態', sortable: true },
        { key: 'created_at', label: '建立時間', sortable: true }
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
          label: '訂單',
          event: 'view',
          type: 'view'
        },
        {
          name: 'delete',
          label: '刪除',
          event: 'delete',
          type: 'delete'
        }
      ]
    }
  },
  async created() {
    await this.loadCustomers()
  },
  methods: {
    async loadCustomers() {
      try {
        this.loading = true
        
        // Mock API call - replace with actual API
        const mockCustomers = [
          {
            id: 1,
            customer_name: '台積電股份有限公司',
            contact_name: '林經理',
            phone: '03-5636688',
            email: 'manager@tsmc.com',
            address: '新竹市力行三路8號',
            customer_type: 'business',
            customer_level: 'platinum',
            tax_id: '11883105',
            status: 'active',
            notes: 'VIP客戶',
            created_at: '2024-01-10'
          },
          {
            id: 2,
            customer_name: '鴻海精密工業股份有限公司',
            contact_name: '陳副理',
            phone: '02-22680013',
            email: 'procurement@foxconn.com',
            address: '新北市土城區中山路66號',
            customer_type: 'business',
            customer_level: 'gold',
            tax_id: '04128089',
            status: 'active',
            notes: '長期合作夥伴',
            created_at: '2024-01-25'
          },
          {
            id: 3,
            customer_name: '張小明',
            contact_name: '張小明',
            phone: '0912-345-678',
            email: 'xiaoming@gmail.com',
            address: '台北市大安區敦化南路二段77號',
            customer_type: 'individual',
            customer_level: 'silver',
            tax_id: '',
            status: 'active',
            notes: '個人客戶',
            created_at: '2024-02-15'
          },
          {
            id: 4,
            customer_name: '台灣大學',
            contact_name: '王教授',
            phone: '02-33662001',
            email: 'admin@ntu.edu.tw',
            address: '台北市大安區羅斯福路四段一號',
            customer_type: 'educational',
            customer_level: 'gold',
            tax_id: '03722103',
            status: 'active',
            notes: '教育採購',
            created_at: '2024-03-01'
          }
        ]
        
        // Apply search filter
        let filtered = mockCustomers
        if (this.searchQuery) {
          filtered = mockCustomers.filter(customer =>
            customer.customer_name.includes(this.searchQuery) ||
            customer.contact_name.includes(this.searchQuery) ||
            customer.phone.includes(this.searchQuery)
          )
        }
        
        // Apply sorting
        if (this.sortBy) {
          filtered.sort((a, b) => {
            const aVal = a[this.sortBy]
            const bVal = b[this.sortBy]
            if (this.sortOrder === 'asc') {
              return aVal > bVal ? 1 : -1
            } else {
              return aVal < bVal ? 1 : -1
            }
          })
        }
        
        // Add formatted data
        this.customers = filtered.map(customer => ({
          ...customer,
          customer_type_key: customer.customer_type, // Keep original key for editing
          customer_level_key: customer.customer_level, // Keep original key for editing
          status_key: customer.status, // Keep original key for editing
          customer_type: this.getCustomerTypeText(customer.customer_type),
          customer_level: this.getCustomerLevelText(customer.customer_level),
          status: this.getStatusText(customer.status),
          created_at: this.formatDate(customer.created_at)
        }))
        
        this.total = filtered.length
        
      } catch (error) {
        console.error('Error loading customers:', error)
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: '載入客戶資料失敗'
        })
      } finally {
        this.loading = false
      }
    },

    handlePageChange(page) {
      this.currentPage = page
      this.loadCustomers()
    },

    handleSort({ sortBy, sortOrder }) {
      this.sortBy = sortBy
      this.sortOrder = sortOrder
      this.loadCustomers()
    },

    handleSearch(query) {
      this.searchQuery = query
      this.currentPage = 1
      this.loadCustomers()
    },

    openAddModal() {
      this.isEditMode = false
      this.editingId = null
      this.resetForm()
      this.showModal = true
    },

    editCustomer(customer) {
      this.isEditMode = true
      this.editingId = customer.id
      this.form = {
        customer_name: customer.customer_name,
        contact_name: customer.contact_name,
        phone: customer.phone,
        email: customer.email,
        address: customer.address || '',
        customer_type: customer.customer_type_key || '',
        customer_level: customer.customer_level_key || '',
        tax_id: customer.tax_id || '',
        status: customer.status_key || 'active',
        notes: customer.notes || ''
      }
      this.showModal = true
    },

    deleteCustomer(customer) {
      this.deleteItem = customer
      this.showDeleteModal = true
    },

    viewOrders(customer) {
      this.$router.push({ name: 'Orders', query: { customer_id: customer.id } })
    },

    async handleSubmit() {
      try {
        this.submitting = true

        // Mock API call
        if (this.isEditMode) {
          console.log('Updating customer:', this.editingId, this.form)
        } else {
          console.log('Creating customer:', this.form)
        }

        this.$store.dispatch('setNotification', {
          type: 'success',
          message: this.isEditMode ? '客戶更新成功' : '客戶新增成功'
        })

        this.closeModal()
        await this.loadCustomers()

      } catch (error) {
        console.error('Error saving customer:', error)
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: '客戶儲存失敗'
        })
      } finally {
        this.submitting = false
      }
    },

    async confirmDelete() {
      try {
        this.submitting = true

        // Mock API call
        console.log('Deleting customer:', this.deleteItem.id)

        this.$store.dispatch('setNotification', {
          type: 'success',
          message: '客戶刪除成功'
        })

        this.closeDeleteModal()
        await this.loadCustomers()

      } catch (error) {
        console.error('Error deleting customer:', error)
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: '客戶刪除失敗'
        })
      } finally {
        this.submitting = false
      }
    },

    closeModal() {
      this.showModal = false
      this.resetForm()
    },

    closeDeleteModal() {
      this.showDeleteModal = false
      this.deleteItem = null
    },

    resetForm() {
      this.form = {
        customer_name: '',
        contact_name: '',
        phone: '',
        email: '',
        address: '',
        customer_type: '',
        customer_level: '',
        tax_id: '',
        status: 'active',
        notes: ''
      }
    },

    getCustomerTypeText(type) {
      const types = {
        'individual': '個人',
        'business': '企業',
        'government': '政府機關',
        'educational': '教育機構'
      }
      return types[type] || type
    },

    getCustomerLevelText(level) {
      const levels = {
        'bronze': '銅級',
        'silver': '銀級',
        'gold': '金級',
        'platinum': '白金級'
      }
      return levels[level] || level
    },

    getStatusText(status) {
      const statuses = {
        'active': '啟用',
        'inactive': '停用',
        'suspended': '暫停'
      }
      return statuses[status] || status
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString('zh-TW')
    }
  }
}
</script> 