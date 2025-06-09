<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-900">出貨管理</h1>
          <button
            @click="showModal = true"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            <i class="fas fa-plus mr-2"></i>
            新增出貨
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Filters -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">搜尋</label>
            <input
              v-model="searchTerm"
              type="text"
              placeholder="搜尋出貨單號或客戶..."
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
              <option value="待出貨">待出貨</option>
              <option value="運送中">運送中</option>
              <option value="已送達">已送達</option>
              <option value="已取消">已取消</option>
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
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">運送方式</label>
            <select
              v-model="shippingMethodFilter"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">全部方式</option>
              <option value="標準配送">標準配送</option>
              <option value="快速配送">快速配送</option>
              <option value="特殊配送">特殊配送</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Shipments Table -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <DataTable
          :columns="columns"
          :data="filteredShipments"
          :loading="loading"
          @sort="handleSort"
        >
          <template #actions="{ row }">
            <div class="flex space-x-2">
              <button
                @click="viewShipment(row)"
                class="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                查看
              </button>
              <button
                v-if="row.status === '待出貨'"
                @click="editShipment(row)"
                class="text-green-600 hover:text-green-800 text-sm font-medium"
              >
                編輯
              </button>
              <button
                v-if="row.status !== '已取消' && row.status !== '已送達'"
                @click="cancelShipment(row)"
                class="text-red-600 hover:text-red-800 text-sm font-medium"
              >
                取消
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
            {{ isEditing ? '編輯出貨' : '新增出貨' }}
          </h3>
          
          <form @submit.prevent="submitForm" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">訂單編號</label>
                <select
                  v-model="form.order_id"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">請選擇訂單</option>
                  <option v-for="order in orders" :key="order.order_id" :value="order.order_id">
                    {{ order.order_number }} - {{ order.customer_name }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">追蹤號碼</label>
                <input
                  v-model="form.tracking_number"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">運送方式</label>
                <select
                  v-model="form.shipping_method"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">選擇運送方式</option>
                  <option value="標準配送">標準配送</option>
                  <option value="快速配送">快速配送</option>
                  <option value="特殊配送">特殊配送</option>
                </select>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">收件地址</label>
              <textarea
                v-model="form.shipping_address"
                rows="3"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              ></textarea>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">預計出貨日期</label>
                <input
                  v-model="form.estimated_shipping_date"
                  type="date"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">預計送達日期</label>
                <input
                  v-model="form.estimated_delivery_date"
                  type="date"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">備註</label>
              <textarea
                v-model="form.notes"
                rows="2"
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
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
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
import { shipmentsAPI } from '../api/shipments'

export default {
  name: 'Shipments',
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
      dateFilter: '',
      shippingMethodFilter: '',
      shipments: [],
      orders: [],
      shippingVendors: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      form: {
        order_id: '',
        tracking_number: '',
        shipping_method: '',
        shipping_address: '',
        estimated_shipping_date: '',
        estimated_delivery_date: '',
        notes: ''
      },
      columns: [
        { key: 'shipment_id', label: '出貨單號', sortable: true },
        { key: 'order_id', label: '訂單編號', sortable: true },
        { key: 'customer_name', label: '客戶姓名', sortable: true },
        { key: 'shipping_method', label: '運送方式', sortable: true },
        { key: 'status', label: '狀態', sortable: true },
        { key: 'estimated_shipping_date', label: '預計出貨日期', sortable: true },
        { key: 'tracking_number', label: '追蹤號碼', sortable: false },
        { key: 'actions', label: '操作', sortable: false }
      ]
    }
  },
  async created() {
    try {
      await this.loadShipments()
      await this.loadOrders()
      await this.loadShippingVendors()
    } catch (error) {
      console.error('Error during component initialization:', error)
      // Don't show alert here since loadShipments already handles errors
    }
  },
  computed: {
    filteredShipments() {
      return this.shipments // API handles filtering now
    }
  },
  methods: {
    async loadShipments() {
      try {
        this.loading = true
        const response = await shipmentsAPI.fetchShipments({
          page: this.currentPage,
          per_page: this.pageSize,
          status: this.statusFilter,
          search: this.searchTerm
        })

        const shipmentsData = response.data.data || response.data || []
        this.shipments = shipmentsData.map(shipment => ({
          ...shipment,
          // Map Chinese status
          status: this.getStatusText(shipment.status),
          // Ensure tracking_number field exists for frontend compatibility
          tracking_number: shipment.tracking_number || shipment.tracking_no || ''
        }))
        this.total = response.data.total || response.total || shipmentsData.length

      } catch (error) {
        console.error('Error loading shipments:', error)
        // Simple alert instead of store notification
        alert('載入出貨資料失敗: ' + (error.response?.data?.error || error.message))
      } finally {
        this.loading = false
      }
    },

    async loadOrders() {
      try {
        const response = await fetch('http://localhost:5001/api/orders')
        const data = await response.json()
        if (data.success) {
          this.orders = data.data
        }
      } catch (error) {
        console.error('Error loading orders:', error)
      }
    },

    async loadShippingVendors() {
      try {
        const response = await shipmentsAPI.fetchShippingVendors()
        const vendorsData = response.data.data || response.data || []
        this.shippingVendors = vendorsData
      } catch (error) {
        console.error('Error loading shipping vendors:', error)
      }
    },

    getStatusText(status) {
      const statusMap = {
        'pending': '待出貨',
        'in_transit': '運送中',
        'delivered': '已送達',
        'cancelled': '已取消'
      }
      return statusMap[status?.toLowerCase()] || status || '未知狀態'
    },

    handleSort({ sortBy, sortOrder }) {
      // Handle sorting logic
      console.log('Sorting by:', sortBy, sortOrder)
      this.loadShipments()
    },
    viewShipment(shipment) {
      console.log('Viewing shipment:', shipment)
    },
    editShipment(shipment) {
      this.isEditing = true
      this.form = { ...shipment }
      this.showModal = true
    },
    async cancelShipment(shipment) {
      if (confirm('確定要取消此出貨嗎？')) {
        try {
          await shipmentsAPI.updateShipmentStatus(shipment.shipment_id, 'cancelled')
          alert('出貨已取消')
          await this.loadShipments()
        } catch (error) {
          console.error('Error cancelling shipment:', error)
          alert('取消出貨失敗')
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
        order_id: '',
        tracking_number: '',
        shipping_method: '',
        shipping_address: '',
        estimated_shipping_date: '',
        estimated_delivery_date: '',
        notes: ''
      }
    },
    async submitForm() {
      try {
        this.loading = true
        
        const shipmentData = {
          order_id: parseInt(this.form.order_id),
          shipping_vendor_id: this.shippingVendors[0]?.user_id || 1, // Default to first vendor
          tracking_no: this.form.tracking_number || 'TRK' + Date.now(),
          shipping_method: this.form.shipping_method,
          shipping_address: this.form.shipping_address,
          estimated_shipping_date: this.form.estimated_shipping_date,
          estimated_delivery_date: this.form.estimated_delivery_date,
          notes: this.form.notes,
          status: 'pending'
        }

        if (this.isEditing) {
          await shipmentsAPI.updateShipment(this.form.shipment_id, shipmentData)
        } else {
          await shipmentsAPI.createShipment(shipmentData)
        }

        alert(this.isEditing ? '出貨更新成功' : '出貨新增成功')

        this.closeModal()
        await this.loadShipments()

      } catch (error) {
        console.error('Error saving shipment:', error)
        alert('出貨儲存失敗: ' + (error.response?.data?.error || error.message))
      } finally {
        this.loading = false
      }
    }
  }
}
</script> 