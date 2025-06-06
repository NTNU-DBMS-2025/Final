<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">供應商管理</h1>
          <p class="text-gray-600">管理所有供應商資料與聯絡資訊</p>
        </div>
        <button 
          @click="openAddModal"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center"
        >
          <span class="mr-2">+</span>
          新增供應商
        </button>
      </div>
    </div>

    <!-- Suppliers DataTable -->
    <div class="bg-white shadow rounded-lg p-6">
      <DataTable
        :columns="columns"
        :data="suppliers"
        :actions="actions"
        :loading="loading"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        @page-change="handlePageChange"
        @sort="handleSort"
        @search="handleSearch"
        @edit="editSupplier"
        @delete="deleteSupplier"
        search-placeholder="搜尋供應商名稱、聯絡人或電話..."
      />
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">
              {{ isEditMode ? '編輯供應商' : '新增供應商' }}
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
                  供應商名稱 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.supplier_name"
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
                  供應商類型
                </label>
                <select
                  v-model="form.supplier_type"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">請選擇類型</option>
                  <option value="manufacturer">製造商</option>
                  <option value="wholesaler">批發商</option>
                  <option value="distributor">經銷商</option>
                  <option value="service">服務商</option>
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
                  <option value="active">啟用</option>
                  <option value="inactive">停用</option>
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
              您確定要刪除供應商「{{ deleteItem?.supplier_name }}」嗎？此操作無法復原。
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
import { fetchSuppliers, createSupplier, updateSupplier, deleteSupplier } from '../api/suppliers'
import { mapActions } from 'vuex'

export default {
  name: 'Suppliers',
  components: {
    DataTable
  },
  data() {
    return {
      suppliers: [],
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
        supplier_name: '',
        contact_name: '',
        phone: '',
        email: '',
        address: '',
        supplier_type: '',
        status: 'active',
        notes: ''
      },
      columns: [
        { key: 'supplier_name', label: '供應商名稱', sortable: true },
        { key: 'contact_name', label: '聯絡人', sortable: true },
        { key: 'phone', label: '電話', sortable: false },
        { key: 'email', label: '電子郵件', sortable: false },
        { key: 'supplier_type_display', label: '類型', sortable: true },
        { key: 'status_display', label: '狀態', sortable: true },
        { key: 'created_at_display', label: '建立時間', sortable: true }
      ],
      actions: [
        {
          name: 'edit',
          label: '編輯',
          event: 'edit',
          type: 'edit'
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
    await this.loadSuppliers()
  },
  methods: {
    ...mapActions(['showNotification']),
    
    async loadSuppliers() {
      try {
        this.loading = true
        
        // Real API call to backend
        const params = {}
        if (this.searchQuery) {
          params.search = this.searchQuery
        }
        if (this.sortBy) {
          params.sort = this.sortBy
          params.order = this.sortOrder
        }
        params.page = this.currentPage
        params.per_page = this.pageSize
        
        const response = await fetchSuppliers(params)
        
        if (response.data.success) {
          // Add formatted data for display
          this.suppliers = response.data.data.map(supplier => ({
            ...supplier,
            supplier_type_display: this.getSupplierTypeText(supplier.supplier_type),
            status_display: this.getStatusText(supplier.status),
            created_at_display: this.formatDate(supplier.created_at)
          }))
          
          this.total = response.data.pagination?.total || this.suppliers.length
        } else {
          throw new Error(response.data.error || 'Failed to load suppliers')
        }
        
      } catch (error) {
        console.error('Error loading suppliers:', error)
        this.showNotification({
          type: 'error',
          message: '載入供應商資料失敗'
        })
      } finally {
        this.loading = false
      }
    },

    handlePageChange(page) {
      this.currentPage = page
      this.loadSuppliers()
    },

    handleSort({ sortBy, sortOrder }) {
      this.sortBy = sortBy
      this.sortOrder = sortOrder
      this.loadSuppliers()
    },

    handleSearch(query) {
      this.searchQuery = query
      this.currentPage = 1
      this.loadSuppliers()
    },

    openAddModal() {
      this.isEditMode = false
      this.editingId = null
      this.resetForm()
      this.showModal = true
    },

    editSupplier(supplier) {
      this.isEditMode = true
      this.editingId = supplier.supplier_id
      this.form = {
        supplier_name: supplier.supplier_name,
        contact_name: supplier.contact_name,
        phone: supplier.phone,
        email: supplier.email,
        address: supplier.address || '',
        supplier_type: supplier.supplier_type || '',
        status: supplier.status || 'active',
        notes: supplier.notes || ''
      }
      this.showModal = true
    },

    deleteSupplier(supplier) {
      this.deleteItem = supplier
      this.showDeleteModal = true
    },

    async handleSubmit() {
      try {
        this.submitting = true

        // Real API call
        if (this.isEditMode) {
          await updateSupplier(this.editingId, this.form)
          this.showNotification({
            type: 'success',
            message: '供應商更新成功'
          })
        } else {
          await createSupplier(this.form)
          this.showNotification({
            type: 'success',
            message: '供應商新增成功'
          })
        }

        this.closeModal()
        await this.loadSuppliers()

      } catch (error) {
        console.error('Error saving supplier:', error)
        this.showNotification({
          type: 'error',
          message: '供應商儲存失敗'
        })
      } finally {
        this.submitting = false
      }
    },

    async confirmDelete() {
      try {
        this.submitting = true

        // Real API call
        await deleteSupplier(this.deleteItem.supplier_id)

        this.showNotification({
          type: 'success',
          message: '供應商刪除成功'
        })

        this.closeDeleteModal()
        await this.loadSuppliers()

      } catch (error) {
        console.error('Error deleting supplier:', error)
        this.showNotification({
          type: 'error',
          message: '供應商刪除失敗'
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
        supplier_name: '',
        contact_name: '',
        phone: '',
        email: '',
        address: '',
        supplier_type: '',
        status: 'active',
        notes: ''
      }
    },

    getSupplierTypeText(type) {
      const types = {
        'manufacturer': '製造商',
        'wholesaler': '批發商',
        'distributor': '經銷商',
        'service': '服務商'
      }
      return types[type] || type
    },

    getStatusText(status) {
      const statuses = {
        'active': '啟用',
        'inactive': '停用'
      }
      return statuses[status] || status
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString('zh-TW')
    }
  }
}
</script> 