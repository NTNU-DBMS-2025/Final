<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">訂單管理</h1>
          <p class="text-gray-600">
            {{ filteredCustomerName ? `顯示客戶「${filteredCustomerName}」的訂單` : '管理客戶訂單與出貨狀況' }}
          </p>
          <div v-if="$route.query.customer_id" class="mt-2">
            <button 
              @click="clearCustomerFilter"
              class="bg-gray-500 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm"
            >
              顯示所有訂單
            </button>
          </div>
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
        :actions="actions"
        :loading="loading"
        @sort="handleSort"
        @search="handleSearch"
        @view="viewOrder"
        @edit="editOrder"
        @cancel="cancelOrder"
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
                <h4 class="text-md font-medium text-gray-900">訂單項目 ({{ products.length }} products available)</h4>
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
                      @change="onProductChange(item)"
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
                      class="w-full border border-gray-300 rounded px-2 py-1 text-gray-800 placeholder-gray-500 text-sm bg-gray-50"
                      readonly
                      required
                    />
                  </div>
                  <div class="flex items-center">
                    <span class="text-sm font-medium text-gray-800">
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
                <span class="text-lg font-semibold text-gray-900">
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

    <!-- Order Detail Modal -->
    <div v-if="showOrderDetailModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border w-11/12 md:w-4/5 lg:w-3/4 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">
              訂單詳細資訊 - {{ selectedOrder?.order_number }}
            </h3>
            <button 
              @click="closeOrderDetailModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <span class="sr-only">關閉</span>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Order Summary Info -->
          <div class="bg-gray-50 rounded-lg p-4 mb-4">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p class="text-sm text-gray-500">客戶名稱</p>
                <p class="text-lg font-semibold text-gray-900">{{ selectedOrder?.customer_name }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">訂單日期</p>
                <p class="text-lg font-semibold text-gray-900">{{ selectedOrder?.order_date }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">狀態</p>
                <p class="text-lg font-semibold" :class="getStatusClass(selectedOrder?.status)">{{ selectedOrder?.status }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">總金額</p>
                <p class="text-lg font-semibold text-green-600">{{ selectedOrder?.total_amount }}</p>
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <p class="text-sm text-gray-500">優先級</p>
                <p class="text-lg font-semibold text-gray-900">{{ selectedOrder?.priority }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">預計交貨日期</p>
                <p class="text-lg font-semibold text-gray-900">{{ selectedOrder?.expected_delivery_date }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">送貨地址</p>
                <p class="text-lg font-semibold text-gray-900">{{ selectedOrder?.ship_to }}</p>
              </div>
            </div>
            <div v-if="selectedOrder?.notes" class="mt-4">
              <p class="text-sm text-gray-500">備註</p>
              <p class="text-lg font-semibold text-gray-900">{{ selectedOrder?.notes }}</p>
            </div>
          </div>

          <!-- Order Items Table -->
          <div class="overflow-x-auto">
            <div v-if="loadingOrderDetails" class="text-center py-8">
              <div class="text-gray-500">載入中...</div>
            </div>
            <div v-else-if="orderItems.length === 0" class="text-center py-8">
              <div class="text-gray-500">此訂單尚無商品項目</div>
            </div>
            <table v-else class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">商品名稱</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">類別</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">數量</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">單價</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">小計</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="item in orderItems" :key="item.order_item_id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ item.product_name }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ item.category }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-medium">
                    {{ item.quantity }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                    ${{ parseFloat(item.unit_price || 0).toLocaleString() }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-medium">
                    ${{ (parseFloat(item.unit_price || 0) * parseInt(item.quantity || 0)).toLocaleString() }}
                  </td>
                </tr>
              </tbody>
              <tfoot class="bg-gray-50">
                <tr>
                  <td colspan="4" class="px-6 py-4 text-sm font-medium text-gray-900 text-right">總計：</td>
                  <td class="px-6 py-4 text-sm font-bold text-gray-900 text-right">
                    {{ selectedOrder?.total_amount }}
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>

          <!-- Footer -->
          <div class="flex justify-end pt-4 border-t border-gray-200 mt-6">
            <button
              @click="closeOrderDetailModal"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
            >
              關閉
            </button>
          </div>
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
      showOrderDetailModal: false,
      isEditMode: false,
      submitting: false,
      editingId: null,
      selectedOrder: null,
      orderItems: [],
      loadingOrderDetails: false,
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
      ],
      actions: [
        {
          name: 'view',
          label: '查看',
          event: 'view',
          type: 'view'
        },
        {
          name: 'edit',
          label: '編輯',
          event: 'edit',
          type: 'edit'
        },
        {
          name: 'cancel',
          label: '取消',
          event: 'cancel',
          type: 'delete'
        }
      ]
    }
  },
  computed: {
    filteredCustomerName() {
      const customerId = this.$route.query.customer_id
      if (customerId && this.customers.length > 0) {
        const customer = this.customers.find(c => c.customer_id.toString() === customerId.toString())
        return customer ? customer.name : null
      }
      return null
    }
  },
  async created() {
    await this.loadOrders()
    await this.loadCustomers()
    await this.loadProducts()
  },
  watch: {
    '$route.query.customer_id': {
      handler() {
        this.loadOrders()
      },
      immediate: false
    }
  },
  methods: {
    async loadOrders() {
      try {
        this.loading = true
        
        // Check if we have a customer_id filter from the route query
        const customerId = this.$route.query.customer_id
        const queryParams = { per_page: 1000 } // Load all orders for client-side sorting
        
        if (customerId) {
          queryParams.customer_id = customerId
        }
        
        const response = await ordersAPI.getOrders(queryParams)
        
        // Fix: Access the response data correctly
        let ordersData = response.data.data || response.data || []
        
        // If we have a customer_id filter but the API doesn't support filtering,
        // filter client-side as fallback
        if (customerId && ordersData.length > 0) {
          ordersData = ordersData.filter(order => 
            order.customer_id && order.customer_id.toString() === customerId.toString()
          )
        }
        
        this.orders = ordersData.map(order => ({
          ...order,
          order_date: this.formatDate(order.order_date),
          expected_delivery_date: order.expected_delivery_date ? this.formatDate(order.expected_delivery_date) : '未設定',
          total_amount: `$${order.total_amount.toLocaleString()}`,
          status: this.getStatusText(order.status_key || order.status),
          priority: this.getPriorityText(order.priority_key || order.priority)
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
      
      // Pre-populate customer if we're viewing a specific customer's orders
      const customerId = this.$route.query.customer_id
      if (customerId) {
        this.form.customer_id = customerId
      }
      
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

    async viewOrder(order) {
      this.selectedOrder = order
      this.showOrderDetailModal = true
      
      // Load detailed order items
      await this.loadOrderDetails(order.order_id)
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

        // Get current user from store
        const currentUser = this.$store.state.user
        if (!currentUser) {
          this.$store.dispatch('setNotification', {
            type: 'error',
            message: '用戶未登入，請重新登入'
          })
          return
        }

        const orderData = {
          order_number: this.form.order_number,
          customer_id: parseInt(this.form.customer_id),
          user_id: currentUser.user_id,
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
        // Request more products for order creation - get all available products
        const response = await fetchProducts({ per_page: 1000 })
        console.log('Products API response:', response.data)
        if (response.data.success) {
          this.products = response.data.data
          console.log('Products loaded:', this.products)
        } else {
          // Handle cases where response doesn't have success flag
          this.products = response.data || []
          console.log('Products loaded (fallback):', this.products)
        }
      } catch (error) {
        console.error('Error loading products:', error)
        this.products = []
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

    onProductChange(item) {
      if (item.product_id) {
        const selectedProduct = this.products.find(product => product.product_id == item.product_id)
        if (selectedProduct && selectedProduct.price) {
          item.unit_price = selectedProduct.price
        }
      } else {
        item.unit_price = 0
      }
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

    async loadOrderDetails(orderId) {
      try {
        this.loadingOrderDetails = true
        const response = await ordersAPI.getOrder(orderId)
        
        if (response.data.success) {
          this.orderItems = response.data.data.order_items || []
        } else {
          console.error('Failed to load order details:', response.data.error)
          this.orderItems = []
        }
      } catch (error) {
        console.error('Error loading order details:', error)
        this.orderItems = []
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: '載入訂單詳細資料失敗'
        })
      } finally {
        this.loadingOrderDetails = false
      }
    },

    closeOrderDetailModal() {
      this.showOrderDetailModal = false
      this.selectedOrder = null
      this.orderItems = []
    },

    getStatusClass(status) {
      const statusClasses = {
        '待處理': 'text-yellow-600',
        '已確認': 'text-blue-600', 
        '處理中': 'text-purple-600',
        '已出貨': 'text-indigo-600',
        '已送達': 'text-green-600',
        '已取消': 'text-red-600'
      }
      return statusClasses[status] || 'text-gray-600'
    },

    clearCustomerFilter() {
      this.$router.push({ name: 'Orders', query: {} })
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString('zh-TW')
    }
  }
}
</script> 