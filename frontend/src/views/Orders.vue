<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">訂單管理</h1>
          <p class="text-gray-600">管理客戶訂單與出貨狀況</p>
        </div>
        <button 
          @click="openAddModal"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center"
        >
          <span class="mr-2">+</span>
          新增訂單
        </button>
      </div>
    </div>

    <!-- Orders DataTable -->
    <div class="bg-white shadow rounded-lg p-6">
      <DataTable
        :columns="columns"
        :data="orders"
        :loading="loading"
        @sort="handleSort"
        @search="handleSearch"
        search-placeholder="搜尋訂單編號、客戶名稱..."
      />
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border w-11/12 md:w-2/3 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">
              {{ isEditMode ? '編輯訂單' : '新增訂單' }}
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
                  訂單編號 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.order_number"
                  type="text"
                  required
                  :disabled="isEditMode"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  客戶 <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="form.customer_id"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">請選擇客戶</option>
                  <option v-for="customer in customers" :key="customer.customer_id" :value="customer.customer_id">
                    {{ customer.name }}
                  </option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  訂單日期 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.order_date"
                  type="date"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  預計交貨日期
                </label>
                <input
                  v-model="form.expected_delivery_date"
                  type="date"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  訂單狀態
                </label>
                <select
                  v-model="form.status"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="pending">待處理</option>
                  <option value="confirmed">已確認</option>
                  <option value="processing">處理中</option>
                  <option value="shipped">已出貨</option>
                  <option value="delivered">已送達</option>
                  <option value="cancelled">已取消</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  優先級
                </label>
                <select
                  v-model="form.priority"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="low">低</option>
                  <option value="normal">普通</option>
                  <option value="high">高</option>
                  <option value="urgent">緊急</option>
                </select>
              </div>

              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  送貨地址 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.ship_to"
                  type="text"
                  required
                  placeholder="請輸入送貨地址"
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

            <!-- Order Items -->
            <div class="border-t pt-4">
              <div class="flex justify-between items-center mb-3">
                <h4 class="text-md font-medium text-gray-900">訂單項目</h4>
                <button
                  type="button"
                  @click="addOrderItem"
                  class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm"
                >
                  新增項目
                </button>
              </div>

              <div class="space-y-3">
                <div 
                  v-for="(item, index) in form.order_items" 
                  :key="index"
                  class="grid grid-cols-1 md:grid-cols-5 gap-3 p-3 border border-gray-200 rounded"
                >
                  <div>
                    <select
                      v-model="item.product_id"
                      class="w-full border border-gray-300 rounded px-2 py-1 text-gray-900 placeholder-gray-500 text-sm"
                      required
                    >
                      <option value="">選擇商品</option>
                      <option v-for="product in products" :key="product.product_id" :value="product.product_id">
                        {{ product.name }}
                      </option>
                    </select>
                  </div>
                  <div>
                    <input
                      v-model.number="item.quantity"
                      type="number"
                      min="1"
                      placeholder="數量"
                      class="w-full border border-gray-300 rounded px-2 py-1 text-gray-900 placeholder-gray-500 text-sm"
                      required
                    />
                  </div>
                  <div>
                    <input
                      v-model.number="item.unit_price"
                      type="number"
                      step="0.01"
                      placeholder="單價"
                      class="w-full border border-gray-300 rounded px-2 py-1 text-gray-900 placeholder-gray-500 text-sm"
                      required
                    />
                  </div>
                  <div class="flex items-center">
                    <span class="text-sm font-medium">
                      ${{ (item.quantity * item.unit_price).toFixed(2) }}
                    </span>
                  </div>
                  <div>
                    <button
                      type="button"
                      @click="removeOrderItem(index)"
                      class="text-red-600 hover:text-red-800 text-sm"
                    >
                      移除
                    </button>
                  </div>
                </div>
              </div>

              <div class="mt-3 text-right">
                <span class="text-lg font-semibold">
                  總金額: ${{ calculateTotal().toFixed(2) }}
                </span>
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
import { ordersAPI } from '../api/orders'

export default {
  name: 'Orders',
  components: {
    DataTable
  },
  data() {
    return {
      orders: [],
      customers: [],
      products: [],
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
        order_number: '',
        customer_id: '',
        order_date: new Date().toISOString().split('T')[0],
        expected_delivery_date: '',
        status: 'pending',
        priority: 'normal',
        ship_to: '',
        notes: '',
        order_items: []
      },
      columns: [
        { key: 'order_number', label: '訂單編號', sortable: true },
        { key: 'customer_name', label: '客戶', sortable: true },
        { key: 'order_date', label: '訂單日期', sortable: true },
        { key: 'expected_delivery_date', label: '預計交貨日期', sortable: true },
        { key: 'total_amount', label: '總金額', sortable: true },
        { key: 'status', label: '狀態', sortable: true },
        { key: 'priority', label: '優先級', sortable: true },
        { key: 'actions', label: '操作', sortable: false }
      ]
    }
  },
  async created() {
    await this.loadOrders()
    await this.loadCustomers()
    await this.loadProducts()
  },
  methods: {
    async loadOrders() {
      try {
        this.loading = true
        
        const response = await ordersAPI.getOrders({
          per_page: 1000 // Load all orders for client-side sorting
        })
        
        // Fix: Access the response data correctly
        const ordersData = response.data.data || response.data || []
        
        this.orders = ordersData.map(order => ({
          ...order,
          order_date: this.formatDate(order.order_date),
          expected_delivery_date: order.expected_delivery_date ? this.formatDate(order.expected_delivery_date) : '未設定',
          total_amount: `$${order.total_amount.toLocaleString()}`,
          status: this.getStatusText(order.status_key || order.status),
          priority: this.getPriorityText(order.priority_key || order.priority),
          actions: [
            {
              label: '查看',
              action: () => this.viewOrder(order),
              class: 'text-green-600 hover:text-green-900'
            },
            {
              label: '編輯',
              action: () => this.editOrder(order),
              class: 'text-blue-600 hover:text-blue-900'
            },
            {
              label: '取消',
              action: () => this.cancelOrder(order),
              class: 'text-red-600 hover:text-red-900'
            }
          ]
        }))
        
        // Remove total for client-side mode
        
      } catch (error) {
        console.error('Error loading orders:', error)
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: '載入訂單資料失敗: ' + (error.response?.data?.error || error.message)
        })
      } finally {
        this.loading = false
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
      this.generateOrderNumber()
      this.showModal = true
    },

    editOrder(order) {
      this.isEditMode = true
      this.editingId = order.id
      this.form = {
        order_number: order.order_number,
        customer_id: order.customer_id,
        order_date: order.order_date_raw || order.order_date,
        expected_delivery_date: order.expected_delivery_date || '',
        status: order.status_key || 'pending',
        priority: order.priority_key || 'normal',
        ship_to: order.ship_to || '',
        notes: order.notes || '',
        order_items: order.order_items || []
      }
      this.showModal = true
    },

    viewOrder(order) {
      console.log('Viewing order:', order)
    },

    cancelOrder(order) {
      if (confirm(`確定要取消訂單 ${order.order_number} 嗎？`)) {
        console.log('Cancelling order:', order.id)
        this.loadOrders()
      }
    },

    async handleSubmit() {
      try {
        this.submitting = true

        const orderData = {
          order_number: this.form.order_number,
          customer_id: parseInt(this.form.customer_id),
          user_id: 1, // Default to first user, should be current logged in user
          order_date: this.form.order_date,
          expected_delivery_date: this.form.expected_delivery_date || null,
          status: this.form.status,
          priority: this.form.priority,
          ship_to: this.form.ship_to || `Customer ${this.form.customer_id} Address`,
          notes: this.form.notes,
          order_items: this.form.order_items.map(item => ({
            product_id: parseInt(item.product_id),
            quantity: parseInt(item.quantity),
            unit_price: parseFloat(item.unit_price)
          }))
        }

        if (this.isEditMode) {
          await ordersAPI.updateOrder(this.editingId, orderData)
        } else {
          await ordersAPI.createOrder(orderData)
        }

        this.$store.dispatch('setNotification', {
          type: 'success',
          message: this.isEditMode ? '訂單更新成功' : '訂單新增成功'
        })

        this.closeModal()
        await this.loadOrders()

      } catch (error) {
        console.error('Error saving order:', error)
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: '訂單儲存失敗: ' + (error.response?.data?.error || error.message)
        })
      } finally {
        this.submitting = false
      }
    },

    async loadCustomers() {
      try {
        const { fetchCustomers } = await import('../api/customers')
        const response = await fetchCustomers()
        if (response.data.success) {
          this.customers = response.data.data
        } else {
          // Handle cases where response doesn't have success flag
          this.customers = response.data || []
        }
      } catch (error) {
        console.error('Error loading customers:', error)
      }
    },

    async loadProducts() {
      try {
        const { fetchProducts } = await import('../api/products')
        const response = await fetchProducts()
        if (response.data.success) {
          this.products = response.data.data
        } else {
          // Handle cases where response doesn't have success flag
          this.products = response.data || []
        }
      } catch (error) {
        console.error('Error loading products:', error)
      }
    },

    closeModal() {
      this.showModal = false
      this.resetForm()
    },

    resetForm() {
      this.form = {
        order_number: '',
        customer_id: '',
        order_date: new Date().toISOString().split('T')[0],
        expected_delivery_date: '',
        status: 'pending',
        priority: 'normal',
        ship_to: '',
        notes: '',
        order_items: []
      }
    },

    generateOrderNumber() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const time = String(now.getTime()).slice(-4)
      this.form.order_number = `ORD${year}${month}${day}${time}`
    },

    addOrderItem() {
      this.form.order_items.push({
        product_id: '',
        quantity: 1,
        unit_price: 0
      })
    },

    removeOrderItem(index) {
      this.form.order_items.splice(index, 1)
    },

    calculateTotal() {
      return this.form.order_items.reduce((total, item) => {
        return total + (item.quantity * item.unit_price)
      }, 0)
    },

    getStatusText(status) {
      const statuses = {
        'pending': '待處理',
        'confirmed': '已確認',
        'processing': '處理中',
        'shipped': '已出貨',
        'delivered': '已送達',
        'cancelled': '已取消'
      }
      return statuses[status] || status
    },

    getPriorityText(priority) {
      const priorities = {
        'low': '低',
        'normal': '普通',
        'high': '高',
        'urgent': '緊急'
      }
      return priorities[priority] || priority
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString('zh-TW')
    }
  }
}
</script> 