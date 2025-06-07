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
            class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm w-full sm:w-auto min-w-0"
          />
          <button 
            v-if="showAddButton"
            @click="$emit('add')"
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
                column.sortable ? 'cursor-pointer hover:bg-gray-100' : ''
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
          <tr v-else v-for="(row, index) in paginatedData" :key="index" class="hover:bg-gray-50">
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
              <div v-else-if="column.type === 'currency'">
                NT$ {{ Number(row[column.key]).toLocaleString() }}
              </div>
              <div v-else-if="column.key === 'actions'">
                <div class="flex justify-end space-x-2">
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
              <div class="flex justify-end space-x-2">
                <button
                  v-for="action in actions"
                  :key="action.name"
                  @click="$emit(action.event, row)"
                  :class="getActionClass(action.type)"
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
      :current-page="currentPage"
      :total-pages="totalPages"
      :total-items="filteredData.length"
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
    }
  },
  emits: ['edit', 'delete', 'view', 'add', 'search', 'page-change'],
  data() {
    return {
      searchQuery: '',
      sortKey: '',
      sortOrder: 'asc',
      currentPage: 1
    }
  },
  computed: {
    filteredData() {
      if (!this.searchQuery) return this.data
      
      return this.data.filter(row => {
        return this.columns.some(column => {
          const value = row[column.key]
          return value && value.toString().toLowerCase().includes(this.searchQuery.toLowerCase())
        })
      })
    },
    sortedData() {
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
      if (!this.showPagination) return this.sortedData
      
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.sortedData.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.filteredData.length / this.pageSize)
    }
  },
  methods: {
    handleSearch() {
      this.currentPage = 1
      this.$emit('search', this.searchQuery)
    },
    handleSort(key) {
      if (this.sortKey === key) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortKey = key
        this.sortOrder = 'asc'
      }
    },
    handlePageChange(page) {
      this.currentPage = page
      this.$emit('page-change', page)
    },
    getStatusClass(status) {
      const baseClass = 'inline-flex px-2 py-1 text-xs font-semibold rounded-full'
      switch (status) {
        case '已完成':
        case '已出貨':
          return `${baseClass} bg-green-100 text-green-800`
        case '處理中':
        case '待出貨':
          return `${baseClass} bg-yellow-100 text-yellow-800`
        case '已取消':
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
    getActionClass(type) {
      switch (type) {
        case 'edit':
          return 'bg-blue-500 hover:bg-blue-600 text-white'
        case 'delete':
          return 'bg-red-500 hover:bg-red-600 text-white'
        case 'view':
          return 'bg-gray-500 hover:bg-gray-600 text-white'
        default:
          return 'bg-gray-500 hover:bg-gray-600 text-white'
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