<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-900">報表管理</h1>
          <button
            @click="generateCustomReport"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            <i class="fas fa-file-alt mr-2"></i>
            生成自訂報表
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Quick Report Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div 
          @click="generateReport('inventory')"
          class="bg-white rounded-lg shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow"
        >
          <div class="flex items-center">
            <div class="p-3 bg-blue-100 rounded-lg">
              <i class="fas fa-boxes text-blue-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">庫存報表</h3>
              <p class="text-sm text-gray-600">目前庫存狀況</p>
            </div>
          </div>
        </div>

        <div 
          @click="generateReport('sales')"
          class="bg-white rounded-lg shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow"
        >
          <div class="flex items-center">
            <div class="p-3 bg-green-100 rounded-lg">
              <i class="fas fa-chart-line text-green-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">銷售報表</h3>
              <p class="text-sm text-gray-600">銷售績效分析</p>
            </div>
          </div>
        </div>

        <div 
          @click="generateReport('orders')"
          class="bg-white rounded-lg shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow"
        >
          <div class="flex items-center">
            <div class="p-3 bg-yellow-100 rounded-lg">
              <i class="fas fa-shopping-cart text-yellow-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">訂單報表</h3>
              <p class="text-sm text-gray-600">訂單處理狀況</p>
            </div>
          </div>
        </div>

        <div 
          @click="generateReport('financial')"
          class="bg-white rounded-lg shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow"
        >
          <div class="flex items-center">
            <div class="p-3 bg-purple-100 rounded-lg">
              <i class="fas fa-dollar-sign text-purple-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">財務報表</h3>
              <p class="text-sm text-gray-600">收入支出分析</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Report Filters -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">報表篩選</h2>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">報表類型</label>
            <select
              v-model="selectedReportType"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">選擇報表類型</option>
              <option value="inventory">庫存報表</option>
              <option value="sales">銷售報表</option>
              <option value="orders">訂單報表</option>
              <option value="financial">財務報表</option>
              <option value="movement">貨物異動報表</option>
              <option value="scrap">報廢報表</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">開始日期</label>
            <input
              v-model="startDate"
              type="date"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">結束日期</label>
            <input
              v-model="endDate"
              type="date"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">格式</label>
            <select
              v-model="selectedFormat"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="pdf">PDF</option>
              <option value="excel">Excel</option>
              <option value="csv">CSV</option>
            </select>
          </div>
        </div>
        <div class="mt-4 flex justify-end">
          <button
            @click="generateFilteredReport"
            :disabled="!selectedReportType"
            class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg transition-colors"
          >
            <i class="fas fa-download mr-2"></i>
            生成報表
          </button>
        </div>
      </div>

      <!-- Recent Reports -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">最近報表</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  報表名稱
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  類型
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  日期範圍
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  格式
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  生成時間
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  生成人
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  操作
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="report in recentReports" :key="report.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ report.name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ report.type }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ report.date_range }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ report.format }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ report.generated_at }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ report.generated_by }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex space-x-2">
                    <button
                      @click="downloadReport(report)"
                      class="text-blue-600 hover:text-blue-800"
                    >
                      下載
                    </button>
                    <button
                      @click="viewReport(report)"
                      class="text-green-600 hover:text-green-800"
                    >
                      預覽
                    </button>
                    <button
                      @click="deleteReport(report)"
                      class="text-red-600 hover:text-red-800"
                    >
                      刪除
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Loading Modal -->
    <div
      v-if="isGenerating"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    >
      <div class="relative top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100">
            <i class="fas fa-spinner fa-spin text-blue-600 text-xl"></i>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mt-4">正在生成報表</h3>
          <p class="text-sm text-gray-500 mt-2">請稍等，報表正在生成中...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Reports',
  data() {
    return {
      isGenerating: false,
      selectedReportType: '',
      startDate: '',
      endDate: '',
      selectedFormat: 'pdf',
      recentReports: [
        {
          id: 1,
          name: '2024年1月庫存報表',
          type: '庫存報表',
          date_range: '2024-01-01 ~ 2024-01-31',
          format: 'PDF',
          generated_at: '2024-02-01 09:30:00',
          generated_by: '系統管理員',
          file_url: '/reports/inventory_2024_01.pdf'
        },
        {
          id: 2,
          name: '銷售週報',
          type: '銷售報表',
          date_range: '2024-01-22 ~ 2024-01-28',
          format: 'Excel',
          generated_at: '2024-01-29 14:15:00',
          generated_by: '業務經理',
          file_url: '/reports/sales_weekly_2024_01_w4.xlsx'
        },
        {
          id: 3,
          name: '訂單處理報表',
          type: '訂單報表',
          date_range: '2024-01-15 ~ 2024-01-21',
          format: 'CSV',
          generated_at: '2024-01-22 11:45:00',
          generated_by: '倉庫主管',
          file_url: '/reports/orders_2024_01_w3.csv'
        }
      ]
    }
  },
  methods: {
    generateReport(type) {
      this.selectedReportType = type
      this.generateFilteredReport()
    },
    generateFilteredReport() {
      if (!this.selectedReportType) return
      
      this.isGenerating = true
      
      // Simulate report generation
      setTimeout(() => {
        this.isGenerating = false
        
        // Add new report to recent reports
        const newReport = {
          id: this.recentReports.length + 1,
          name: `${this.getReportTypeName(this.selectedReportType)}報表`,
          type: this.getReportTypeName(this.selectedReportType),
          date_range: this.startDate && this.endDate ? `${this.startDate} ~ ${this.endDate}` : '全部資料',
          format: this.selectedFormat.toUpperCase(),
          generated_at: new Date().toLocaleString('zh-TW'),
          generated_by: '當前用戶',
          file_url: `/reports/${this.selectedReportType}_${Date.now()}.${this.selectedFormat}`
        }
        
        this.recentReports.unshift(newReport)
        
        // Show success message
        alert(`${this.getReportTypeName(this.selectedReportType)}報表生成成功！`)
      }, 2000)
    },
    generateCustomReport() {
      // Open custom report configuration modal
      alert('自訂報表功能開發中...')
    },
    getReportTypeName(type) {
      const typeNames = {
        inventory: '庫存',
        sales: '銷售',
        orders: '訂單',
        financial: '財務',
        movement: '貨物異動',
        scrap: '報廢'
      }
      return typeNames[type] || type
    },
    downloadReport(report) {
      // Simulate file download
      alert(`正在下載 ${report.name}...`)
      
      // Create a temporary download link
      const link = document.createElement('a')
      link.href = report.file_url
      link.download = report.name
      link.click()
    },
    viewReport(report) {
      // Open report preview
      alert(`正在預覽 ${report.name}...`)
    },
    deleteReport(report) {
      if (confirm(`確定要刪除 ${report.name} 嗎？`)) {
        const index = this.recentReports.findIndex(r => r.id === report.id)
        if (index !== -1) {
          this.recentReports.splice(index, 1)
          alert('報表已刪除')
        }
      }
    }
  },
  mounted() {
    // Set default dates (last 30 days)
    const today = new Date()
    const thirtyDaysAgo = new Date(today.getTime() - (30 * 24 * 60 * 60 * 1000))
    
    this.endDate = today.toISOString().split('T')[0]
    this.startDate = thirtyDaysAgo.toISOString().split('T')[0]
  }
}
</script> 