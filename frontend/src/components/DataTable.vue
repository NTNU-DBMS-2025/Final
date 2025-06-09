<template>
  <div class="bg-white shadow-lg rounded-lg overflow-hidden responsive-container">
    <!-- Table Header -->
    <div class="px-4 sm:px-6 py-4 border-b border-gray-200">
      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center space-y-3 sm:space-y-0">
        <h3 class="responsive-title text-gray-900">{{ title }}</h3>
        <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2">
          <input
            v-if="searchable"
            v-model="searchQuery"
            @input="handleSearch"
            type="text"
            placeholder="輸入要尋找的內容..."
            class="border border-gray-300 rounded-lg px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm w-full sm:w-auto min-w-0"
          />
          <button 
            v-if="showAddButton"
            @click="$emit('search', searchQuery)"
            type="button"
            class="bg-blue-500 hover:bg-blue-600 text-white px-3 sm:px-4 py-2 rounded-lg transition-colors text-sm w-full sm:w-auto"
          >
            搜尋
          </button>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-responsive">
      <table class="min-w-full divide-y divide-gray-200 text-center">
        <thead class="bg-gray-50">
          <tr>
            <th 
              v-for="column in columns" 
              :key="column.key"
              @click="column.sortable ? handleSort(column.key) : null"
              :class="[
                'px-3 sm:px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap',
                column.sortable ? 'cursor-pointer hover:bg-gray-100 transition-colors duration-200' : ''
              ]"
            >
              <div class="flex justify-center items-center">
                {{ column.label }}
                <span v-if="column.sortable && sortKey === column.key" class="ml-2">
                  {{ sortOrder === 'asc' ? '↑' : '↓' }}
                </span>
              </div>
            </th>
            <th v-if="actions.length > 0" 
              class="px-3 sm:px-6 py-3 text-center text-xs font-medium text-gray-500">
              操作
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="loading" class="text-center">
            <td :colspan="columns.length + (actions.length > 0 ? 1 : 0)" class="px-6 py-4">
              <div class="text-gray-500">載入中...</div>
            </td>
          </tr>
          <tr v-else-if="paginatedData.length === 0" class="text-center">
            <td :colspan="columns.length + (actions.length > 0 ? 1 : 0)" class="px-6 py-4">
              <div class="text-gray-500">沒有資料</div>
            </td>
          </tr>
          <tr v-else v-for="(row, index) in paginatedData" :key="index" class="hover:bg-gray-50 transition-colors duration-200">
            <td v-for="column in columns" :key="column.key" class="px-3 sm:px-6 py-3 sm:py-4 text-sm">
              <div v-if="column.key === 'status'" :class="getStatusClass(row[column.key])">
                {{ row[column.key] }}
              </div>
              <div v-else-if="column.key === 'quantity'" :class="getQuantityClass(row[column.key])">
                {{ row[column.key] }}
              </div>
              <div v-else-if="column.type === 'date'">
                {{ formatDate(row[column.key]) }}
              </div>
              <div v-else-if="column.type === 'currency'" class="font-semibold text-green-600">
                NT$ {{ Number(row[column.key]).toLocaleString() }}
              </div>
              <div v-else-if="column.key === 'actions'">
                <div class="flex justify-center space-x-2">
                  <button
                    v-for="action in row[column.key]"
                    :key="action.label"
                    @click="action.action()"
                    :class="action.class"
                    class="px-2 sm:px-3 py-1 rounded transition-colors text-xs sm:text-sm hover:underline"
                  >
                    {{ action.label }}
                  </button>
                </div>
              </div>
              <div v-else class="text-sm text-gray-900">
                {{ row[column.key] }}
              </div>
            </td>
            <td v-if="actions.length > 0" class="px-3 sm:px-6 py-3 sm:py-4 text-center text-sm font-medium">
              <div class="flex justify-center space-x-2">
                <button
                  v-for="action in actions"
                  :key="action.name"
                  @click="$emit(action.event, row)"
                  :disabled="isActionDisabled(action, row)"
                  :class="[
                    getActionClass(action.type, isActionDisabled(action, row)),
                    isActionDisabled(action, row) ? 'cursor-not-allowed opacity-50' : ''
                  ]"
                  class="px-2 sm:px-3 py-2 rounded transition-colors text-xs sm:text-sm"
                >
                  {{ action.label }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <Pagination
      v-if="showPagination && !loading"
      :current-page="internalCurrentPage"
      :total-pages="totalPages"
      :total-items="totalItems"
      @page-change="handlePageChange"
    />
  </div>
</template>

<script>
import Pagination from './Pagination.vue'

export default {
  name: 'DataTable',
  components: {
    Pagination
  },
  props: {
    title: {
      type: String,
      default: ''
    },
    columns: {
      type: Array,
      required: true
    },
    data: {
      type: Array,
      default: () => []
    },
    actions: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    searchable: {
      type: Boolean,
      default: true
    },
    showPagination: {
      type: Boolean,
      default: true
    },
    showAddButton: {
      type: Boolean,
      default: true
    },
    pageSize: {
      type: Number,
      default: 10
    },
    total: {
      type: Number,
      default: 0
    },
    currentPage: {
      type: Number,
      default: 1
    }
  },
  emits: ['edit', 'delete', 'view', 'add', 'search', 'page-change', 'sort'],
  data() {
    return {
      searchQuery: '',
      sortKey: '',
      sortOrder: 'asc',
      internalCurrentPage: this.currentPage
    }
  },
  watch: {
    currentPage(newVal) {
      this.internalCurrentPage = newVal
    }
  },
  computed: {
    filteredData() {
      // If total prop is provided, use server-side pagination
      if (this.total > 0) {
        return this.data
      }
      
      // Otherwise use client-side filtering
      if (!this.searchQuery) return this.data
      
      return this.data.filter(row => {
        return this.columns.some(column => {
          const value = row[column.key]
          return value && value.toString().toLowerCase().includes(this.searchQuery.toLowerCase())
        })
      })
    },
    sortedData() {
      // If total prop is provided, assume server handles sorting
      if (this.total > 0) {
        return this.filteredData
      }
      
      if (!this.sortKey) return this.filteredData
      
      const sorted = [...this.filteredData].sort((a, b) => {
        const aVal = a[this.sortKey]
        const bVal = b[this.sortKey]
        
        if (aVal === bVal) return 0
        if (aVal === null || aVal === undefined) return 1
        if (bVal === null || bVal === undefined) return -1
        
        if (typeof aVal === 'number') {
          return this.sortOrder === 'asc' ? aVal - bVal : bVal - aVal
        }
        
        return this.sortOrder === 'asc' 
          ? aVal.toString().localeCompare(bVal.toString())
          : bVal.toString().localeCompare(aVal.toString())
      })
      
      return sorted
    },
    paginatedData() {
      // If total prop is provided, return data as-is (server handles pagination)
      if (this.total > 0) {
        return this.sortedData
      }
      
      // Otherwise use client-side pagination
      if (!this.showPagination) return this.sortedData
      
      const start = (this.internalCurrentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.sortedData.slice(start, end)
    },
    totalPages() {
      if (this.total > 0) {
        return Math.ceil(this.total / this.pageSize)
      }
      return Math.ceil(this.filteredData.length / this.pageSize)
    },
    totalItems() {
      return this.total > 0 ? this.total : this.filteredData.length
    }
  },
  methods: {
    handleSearch() {
      this.internalCurrentPage = 1
      this.$emit('search', this.searchQuery)
    },
    handleSort(key) {
      if (this.sortKey === key) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortKey = key
        this.sortOrder = 'asc'
      }
      
      // Emit sort event to parent component
      this.$emit('sort', {
        sortBy: this.sortKey,
        sortOrder: this.sortOrder
      })
    },
    handlePageChange(page) {
      this.internalCurrentPage = page
      this.$emit('page-change', page)
    },
    getStatusClass(status) {
      const baseClass = 'inline-flex px-2 py-1 text-xs font-semibold rounded-full'
      switch (status) {
        // Order statuses
        case '已完成':
        case '已出貨':
        case 'delivered':
          return `${baseClass} bg-green-100 text-green-800`
        case '處理中':
        case '待出貨':
        case 'processing':
          return `${baseClass} bg-yellow-100 text-yellow-800`
        // Scrap management statuses
        case '已處理':
          return `${baseClass} bg-green-100 text-green-800`
        case '待處理':
          return `${baseClass} bg-yellow-100 text-yellow-800`
        case '已取消':
          return `${baseClass} bg-red-100 text-red-800`
        // General statuses
        case 'active':
        case '啟用':
          return `${baseClass} bg-green-100 text-green-800`
        case 'pending':
        case '待確認':
          return `${baseClass} bg-yellow-100 text-yellow-800`
        case 'cancelled':
        case 'inactive':
        case '停用':
          return `${baseClass} bg-red-100 text-red-800`
        default:
          return `${baseClass} bg-gray-100 text-gray-800`
      }
    },
    getQuantityClass(quantity) {
      if (quantity < 20) {
        return 'text-red-600 font-semibold'
      }
      return 'text-gray-900'
    },
    isActionDisabled(action, row) {
      // Check if edit/cancel actions should be disabled for shipped/delivered orders
      if ((action.name === 'edit' || action.name === 'cancel') && 
          (row.status === '已送達' || row.status === '已出貨')) {
        return true
      }
      return false
    },

    getActionClass(type, disabled = false) {
      const baseClass = disabled 
        ? 'bg-gray-300 text-gray-500' 
        : 'text-white shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-200'
      
      if (disabled) {
        return baseClass
      }
      
      switch (type) {
        case 'edit':
          return `bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 ${baseClass}`
        case 'delete':
          return `bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 ${baseClass}`
        case 'view':
          return `bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 ${baseClass}`
        default:
          return `bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 ${baseClass}`
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-TW')
    }
  }
}
</script> 