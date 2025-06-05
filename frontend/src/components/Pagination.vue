<template>
  <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
    <div class="flex-1 flex justify-between sm:hidden">
      <!-- Mobile pagination -->
      <button
        @click="previousPage"
        :disabled="currentPage === 1"
        class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:bg-gray-100 disabled:text-gray-400"
      >
        上一頁
      </button>
      <button
        @click="nextPage"
        :disabled="currentPage === totalPages"
        class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:bg-gray-100 disabled:text-gray-400"
      >
        下一頁
      </button>
    </div>
    
    <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-gray-700">
          顯示
          <span class="font-medium">{{ startItem }}</span>
          到
          <span class="font-medium">{{ endItem }}</span>
          共
          <span class="font-medium">{{ totalItems }}</span>
          筆資料
        </p>
      </div>
      
      <div>
        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
          <!-- Previous page button -->
          <button
            @click="previousPage"
            :disabled="currentPage === 1"
            class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:bg-gray-100 disabled:text-gray-400"
          >
            <span class="sr-only">上一頁</span>
            ←
          </button>
          
          <!-- Page numbers -->
          <template v-for="page in visiblePages" :key="page">
            <button
              v-if="page !== '...'"
              @click="goToPage(page)"
              :class="[
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                page === currentPage
                  ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                  : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
              ]"
            >
              {{ page }}
            </button>
            <span
              v-else
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
            >
              ...
            </span>
          </template>
          
          <!-- Next page button -->
          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:bg-gray-100 disabled:text-gray-400"
          >
            <span class="sr-only">下一頁</span>
            →
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Pagination',
  props: {
    currentPage: {
      type: Number,
      required: true
    },
    totalPages: {
      type: Number,
      required: true
    },
    totalItems: {
      type: Number,
      required: true
    },
    pageSize: {
      type: Number,
      default: 10
    }
  },
  emits: ['page-change'],
  computed: {
    startItem() {
      return (this.currentPage - 1) * this.pageSize + 1
    },
    endItem() {
      return Math.min(this.currentPage * this.pageSize, this.totalItems)
    },
    visiblePages() {
      const pages = []
      const maxVisible = 7 // Maximum number of page buttons to show
      
      if (this.totalPages <= maxVisible) {
        // Show all pages if total is small
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i)
        }
      } else {
        // Always show first page
        pages.push(1)
        
        if (this.currentPage > 4) {
          pages.push('...')
        }
        
        // Show pages around current page
        const start = Math.max(2, this.currentPage - 1)
        const end = Math.min(this.totalPages - 1, this.currentPage + 1)
        
        for (let i = start; i <= end; i++) {
          if (i !== 1 && i !== this.totalPages) {
            pages.push(i)
          }
        }
        
        if (this.currentPage < this.totalPages - 3) {
          pages.push('...')
        }
        
        // Always show last page
        if (this.totalPages > 1) {
          pages.push(this.totalPages)
        }
      }
      
      return pages
    }
  },
  methods: {
    previousPage() {
      if (this.currentPage > 1) {
        this.$emit('page-change', this.currentPage - 1)
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.$emit('page-change', this.currentPage + 1)
      }
    },
    goToPage(page) {
      if (page !== this.currentPage && page >= 1 && page <= this.totalPages) {
        this.$emit('page-change', page)
      }
    }
  }
}
</script> 