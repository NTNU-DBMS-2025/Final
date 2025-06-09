<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">產品管理</h1>
          <p class="text-gray-600">管理所有產品資訊，包含產品基本資料、保固年限等。</p>
        </div>
        <button 
          @click="openAddModal"
          class="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-4 py-2 rounded-lg flex items-center shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
        >
          <span class="mr-2">+</span>
          新增產品
        </button>
      </div>
    </div>

    <!-- Products DataTable -->
    <div class="bg-white shadow rounded-lg p-6">
      <DataTable
        :columns="columns"
        :data="products"
        :actions="actions"
        :loading="loading"
        @edit="openEditModal"
        @delete="handleDelete"
        @search="handleSearch"
        @sort="handleSort"
        search-placeholder="搜尋產品名稱、分類..."
      />
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ isEditing ? '編輯產品' : '新增產品' }}
          </h3>
          
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">產品名稱</label>
              <input
                v-model="form.name"
                type="text"
                required
                class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="請輸入產品名稱"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">分類</label>
              <select
                v-model="form.category"
                required
                class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">請選擇分類</option>
                <option value="Electronics">電子產品</option>
                <option value="Furniture">家具</option>
                <option value="Office Supplies">辦公用品</option>
                <option value="Others">其他</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">保固年限</label>
              <input
                v-model.number="form.warranty_years"
                type="number"
                min="0"
                required
                class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="0"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">單價 (NT$)</label>
              <input
                v-model.number="form.price"
                type="number"
                min="0"
                step="0.01"
                required
                class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="0.00"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">圖片網址</label>
              <input
                v-model="form.image_url"
                type="url"
                class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="https://example.com/image.jpg"
              />
            </div>
            
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-400"
              >
                {{ submitting ? '處理中...' : (isEditing ? '更新' : '新增') }}
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
          <h3 class="text-lg font-medium text-gray-900">確認刪除</h3>
          <div class="mt-2 px-7 py-3">
            <p class="text-sm text-gray-500">
              確定要刪除產品「{{ deleteTarget?.name }}」嗎？此操作無法復原。
            </p>
          </div>
          <div class="items-center px-4 py-3 flex justify-center space-x-3">
            <button
              @click="showDeleteModal = false"
              class="px-4 py-2 bg-gray-300 text-gray-800 text-base font-medium rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300"
            >
              取消
            </button>
            <button
              @click="confirmDelete"
              :disabled="submitting"
              class="px-4 py-2 bg-red-600 text-white text-base font-medium rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-600 disabled:bg-red-400"
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
import { mapActions } from 'vuex'
import DataTable from '../components/DataTable.vue'
import { fetchProducts, createProduct, updateProduct, deleteProduct } from '../api/products'

export default {
  name: 'Products',
  components: {
    DataTable
  },
  data() {
    return {
      products: [],
      loading: false,
      total: 0,
      currentPage: 1,
      pageSize: 10,
      searchQuery: '',
      showModal: false,
      showDeleteModal: false,
      isEditing: false,
      submitting: false,
      deleteTarget: null,
      form: {
        name: '',
        category: '',
        warranty_years: 0,
        price: 0,
        image_url: ''
      },
      columns: [
        { key: 'product_id', label: '產品ID', sortable: true },
        { key: 'name', label: '產品名稱', sortable: true },
        { key: 'category', label: '分類', sortable: true },
        { key: 'warranty_years', label: '保固年限', sortable: true },
        { key: 'price', label: '單價 (NT$)', sortable: true, type: 'currency' },
        { key: 'image_url', label: '圖片', sortable: false }
      ],
      actions: [
        { name: 'edit', label: '編輯', event: 'edit', type: 'edit' },
        { name: 'delete', label: '刪除', event: 'delete', type: 'delete' }
      ]
    }
  },
  async created() {
    await this.loadProducts()
  },
  methods: {
    ...mapActions(['showNotification']),
    
    async loadProducts() {
      this.loading = true
      try {
        // Load all products for client-side sorting and pagination
        const params = {
          per_page: 1000 // Load a large number to get all products
        }
        const response = await fetchProducts(params)
        this.products = response.data.data
      } catch (error) {
        console.error('Failed to load products:', error)
        this.showNotification({
          type: 'error',
          message: '載入產品列表失敗'
        })
      } finally {
        this.loading = false
      }
    },
    
    async handleSearch(query) {
      this.searchQuery = query
      this.currentPage = 1 // Reset to first page when searching
      await this.loadProducts()
    },
    
    async handlePageChange(page) {
      this.currentPage = page
      await this.loadProducts()
    },
    
    openAddModal() {
      this.isEditing = false
      this.form = {
        name: '',
        category: '',
        warranty_years: 0,
        price: 0,
        image_url: ''
      }
      this.showModal = true
    },
    
    openEditModal(product) {
      this.isEditing = true
      this.form = { ...product }
      this.showModal = true
    },
    
    closeModal() {
      this.showModal = false
      this.form = {
        name: '',
        category: '',
        warranty_years: 0,
        price: 0,
        image_url: ''
      }
    },
    
    async handleSubmit() {
      this.submitting = true
      try {
        if (this.isEditing) {
          await updateProduct(this.form.product_id, this.form)
          this.showNotification({
            type: 'success',
            message: '產品更新成功'
          })
        } else {
          await createProduct(this.form)
          this.showNotification({
            type: 'success',
            message: '產品新增成功'
          })
        }
        
        this.closeModal()
        await this.loadProducts()
      } catch (error) {
        console.error('Submit failed:', error)
        this.showNotification({
          type: 'error',
          message: this.isEditing ? '產品更新失敗' : '產品新增失敗'
        })
      } finally {
        this.submitting = false
      }
    },
    
    handleDelete(product) {
      this.deleteTarget = product
      this.showDeleteModal = true
    },
    
    async confirmDelete() {
      this.submitting = true
      try {
        await deleteProduct(this.deleteTarget.product_id)
        this.showNotification({
          type: 'success',
          message: '產品刪除成功'
        })
        this.showDeleteModal = false
        this.deleteTarget = null
        await this.loadProducts()
      } catch (error) {
        console.error('Delete failed:', error)
        this.showNotification({
          type: 'error',
          message: '產品刪除失敗'
        })
      } finally {
        this.submitting = false
      }
    },
    
    async handleSearch(query) {
      this.searchQuery = query
      this.currentPage = 1 // Reset to first page when searching
      await this.loadProducts()
    },
    
    async handlePageChange(page) {
      this.currentPage = page
      await this.loadProducts()
    },
  }
}
</script> 