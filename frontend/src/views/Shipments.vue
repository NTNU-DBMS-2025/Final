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
                <input
                  v-model="form.order_id"
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
      shipments: [
        {
          shipment_id: 1,
          order_id: 'ORD-2024-001',
          customer_name: '王小明',
          shipping_address: '台北市信義區信義路五段7號',
          shipping_method: '標準配送',
          status: '運送中',
          estimated_shipping_date: '2024-01-15',
          estimated_delivery_date: '2024-01-17',
          actual_shipping_date: '2024-01-15',
          tracking_number: 'TRK123456789',
          notes: ''
        },
        {
          shipment_id: 2,
          order_id: 'ORD-2024-002',
          customer_name: '李小華',
          shipping_address: '新北市板橋區中山路一段152號',
          shipping_method: '快速配送',
          status: '已送達',
          estimated_shipping_date: '2024-01-14',
          estimated_delivery_date: '2024-01-15',
          actual_shipping_date: '2024-01-14',
          actual_delivery_date: '2024-01-15',
          tracking_number: 'TRK987654321',
          notes: '客戶要求下午送達'
        }
      ],
      form: {
        order_id: '',
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
  computed: {
    filteredShipments() {
      let filtered = this.shipments

      if (this.searchTerm) {
        filtered = filtered.filter(shipment =>
          shipment.order_id.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          shipment.customer_name.includes(this.searchTerm) ||
          shipment.tracking_number.toLowerCase().includes(this.searchTerm.toLowerCase())
        )
      }

      if (this.statusFilter) {
        filtered = filtered.filter(shipment => shipment.status === this.statusFilter)
      }

      if (this.shippingMethodFilter) {
        filtered = filtered.filter(shipment => shipment.shipping_method === this.shippingMethodFilter)
      }

      if (this.dateFilter) {
        filtered = filtered.filter(shipment => shipment.estimated_shipping_date === this.dateFilter)
      }

      return filtered
    }
  },
  methods: {
    handleSort(column) {
      // Handle sorting logic
      console.log('Sorting by:', column)
    },
    viewShipment(shipment) {
      console.log('Viewing shipment:', shipment)
    },
    editShipment(shipment) {
      this.isEditing = true
      this.form = { ...shipment }
      this.showModal = true
    },
    cancelShipment(shipment) {
      if (confirm('確定要取消此出貨嗎？')) {
        const index = this.shipments.findIndex(s => s.shipment_id === shipment.shipment_id)
        if (index !== -1) {
          this.shipments[index].status = '已取消'
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
        shipping_method: '',
        shipping_address: '',
        estimated_shipping_date: '',
        estimated_delivery_date: '',
        notes: ''
      }
    },
    submitForm() {
      if (this.isEditing) {
        // Update shipment
        const index = this.shipments.findIndex(s => s.shipment_id === this.form.shipment_id)
        if (index !== -1) {
          this.shipments[index] = { ...this.form }
        }
      } else {
        // Create new shipment
        const newShipment = {
          ...this.form,
          shipment_id: this.shipments.length + 1,
          status: '待出貨',
          tracking_number: 'TRK' + Date.now()
        }
        this.shipments.unshift(newShipment)
      }
      this.closeModal()
    }
  }
}
</script> 