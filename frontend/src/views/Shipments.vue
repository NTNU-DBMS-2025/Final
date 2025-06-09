<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">出貨管理</h1>
          <p class="text-gray-600">顯示所有出貨的物品。</p>
        </div>
        <button 
          @click="showModal = true"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          <span class="mr-2">+</span>
          新增出貨
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="space-y-6">
      <!-- Filters -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6 mt-6">
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
          :actions="actions"
          :loading="loading"
          @sort="handleSort"
          @view="viewShipment"
          @edit="handleEditShipment"
          @cancel="handleCancelShipment"
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

    <!-- 出貨詳細資訊彈窗 -->
    <div v-if="showShipmentDetailModal" class="modal-overlay" @click="closeShipmentDetailModal">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3>出貨詳細資訊</h3>
          <button @click="closeShipmentDetailModal" class="close-btn">×</button>
        </div>
        
        <div class="modal-body" v-if="selectedShipment">
          <div v-if="loadingShipmentDetails" class="loading-spinner">
            載入中...
          </div>
          
          <div v-else>
            <!-- 出貨摘要資訊 -->
            <div class="shipment-summary">
              <div class="summary-row">
                <span class="summary-label">出貨編號：</span>
                <span class="summary-value">{{ selectedShipment.shipment_id }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">訂單編號：</span>
                <span class="summary-value">{{ selectedShipment.order_id }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">客戶名稱：</span>
                <span class="summary-value">{{ selectedShipment.customer_name }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">運送方式：</span>
                <span class="summary-value">{{ selectedShipment.shipping_method }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">出貨狀態：</span>
                <span class="summary-value status" :class="getStatusClass(selectedShipment.status)">
                  {{ selectedShipment.status }}
                </span>
              </div>
              <div class="summary-row">
                <span class="summary-label">追蹤號碼：</span>
                <span class="summary-value">{{ selectedShipment.tracking_number || '無' }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">預計出貨日期：</span>
                <span class="summary-value">{{ selectedShipment.estimated_shipping_date || '未設定' }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">實際出貨日期：</span>
                <span class="summary-value">{{ selectedShipment.actual_shipping_date || '未出貨' }}</span>
              </div>
              <div class="summary-row" v-if="selectedShipment.notes">
                <span class="summary-label">備註：</span>
                <span class="summary-value">{{ selectedShipment.notes }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="closeShipmentDetailModal" class="btn btn-secondary">關閉</button>
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
      showShipmentDetailModal: false,
      isEditing: false,
      selectedShipment: null,
      loadingShipmentDetails: false,
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
        { key: 'tracking_number', label: '追蹤號碼', sortable: false }
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
        const URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api'
        const response = await fetch(`${URL}/orders`)
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
    
    getStatusClass(status) {
      const statusClassMap = {
        '待出貨': 'pending',
        '運送中': 'in_transit', 
        '已送達': 'delivered',
        '已取消': 'cancelled'
      }
      return statusClassMap[status] || 'pending'
    },

    handleSort({ sortBy, sortOrder }) {
      // Handle sorting logic
      console.log('Sorting by:', sortBy, sortOrder)
      this.loadShipments()
    },
    async viewShipment(shipment) {
      this.selectedShipment = shipment
      this.showShipmentDetailModal = true
      
      // Load additional shipment details if needed
      await this.loadShipmentDetails(shipment.shipment_id)
    },
    async loadShipmentDetails(shipmentId) {
      this.loadingShipmentDetails = true
      try {
        // If you have an API endpoint for detailed shipment info, call it here
        // For now, we'll use the existing data
        console.log('Loading details for shipment:', shipmentId)
      } catch (error) {
        console.error('Error loading shipment details:', error)
        this.$message.error('載入出貨詳細資訊失敗')
      } finally {
        this.loadingShipmentDetails = false
      }
    },
    closeShipmentDetailModal() {
      this.showShipmentDetailModal = false
      this.selectedShipment = null
    },
    handleEditShipment(shipment) {
      // Check if shipment can be edited
      if (shipment.status === '已送達' || shipment.status === '已取消') {
        alert(`出貨狀態為「${shipment.status}」，無法編輯`)
        return
      }
      this.editShipment(shipment)
    },

    editShipment(shipment) {
      this.isEditing = true
      this.form = { ...shipment }
      this.showModal = true
    },
    handleCancelShipment(shipment) {
      // Check if shipment can be canceled
      if (shipment.status === '已送達' || shipment.status === '已取消') {
        alert(`出貨狀態為「${shipment.status}」，無法取消`)
        return
      }
      this.cancelShipment(shipment)
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

<style scoped>
.disabled-button {
  cursor: not-allowed !important;
}

/* 出貨詳細資訊彈窗樣式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  background-color: #f8f9fa;
  border-radius: 8px 8px 0 0;
}

.modal-header h3 {
  margin: 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: #e0e0e0;
  color: #333;
}

.modal-body {
  padding: 20px;
}

.loading-spinner {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 16px;
}

.shipment-summary {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.summary-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #e9ecef;
}

.summary-row:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.summary-label {
  font-weight: 600;
  color: #495057;
  width: 120px;
  flex-shrink: 0;
}

.summary-value {
  color: #333;
  flex: 1;
}

.summary-value.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  display: inline-block;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: flex-end;
  background-color: #f8f9fa;
  border-radius: 0 0 8px 8px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
}

/* Status color classes to match the existing theme */
.status.pending { background-color: #fff3cd; color: #856404; }
.status.in_transit { background-color: #cce5ff; color: #004085; }
.status.delivered { background-color: #d4edda; color: #155724; }
.status.cancelled { background-color: #f8d7da; color: #721c24; }
</style> 