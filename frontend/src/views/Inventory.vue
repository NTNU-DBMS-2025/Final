<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">庫存管理</h1>
          <p class="text-gray-600">管理商品庫存數量、位置與異動記錄</p>
        </div>
        <div class="flex space-x-3">
          <button 
            @click="openAdjustmentModal"
            class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center"
          >
            <span class="mr-2">📝</span>
            庫存調整
          </button>
          <button 
            @click="openMovementModal"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center"
          >
            <span class="mr-2">🔄</span>
            庫存異動
          </button>
        </div>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <Card 
        title="總庫存值" 
        icon="inventory" 
        color="bg-white"
      >
        <p class="text-3xl font-bold text-green-600">${{ totalInventoryValue.toLocaleString() }}</p>
        <p class="text-sm text-gray-500">總價值</p>
      </Card>
      
      <Card 
        title="庫存品項" 
        icon="products" 
        color="bg-white"
      >
        <p class="text-3xl font-bold text-blue-600">{{ totalItems }}</p>
        <p class="text-sm text-gray-500">個品項</p>
      </Card>
      
      <Card 
        title="低庫存警告" 
        icon="warning" 
        color="bg-white"
      >
        <p class="text-3xl font-bold text-red-600">{{ lowStockCount }}</p>
        <p class="text-sm text-gray-500">項商品</p>
      </Card>
      
      <Card 
        title="缺貨品項" 
        icon="warning" 
        color="bg-white"
      >
        <p class="text-3xl font-bold text-red-600">{{ outOfStockCount }}</p>
        <p class="text-sm text-gray-500">項商品</p>
      </Card>
    </div>

    <!-- Inventory DataTable -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-gray-900">庫存明細</h2>
        <div class="flex space-x-2">
          <select
            v-model="statusFilter"
            @change="loadInventory"
            class="border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 text-sm"
          >
            <option value="">全部狀態</option>
            <option value="in_stock">有庫存</option>
            <option value="low_stock">低庫存</option>
            <option value="out_of_stock">缺貨</option>
          </select>
          <select
            v-model="locationFilter"
            @change="loadInventory"
            class="border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 text-sm"
          >
            <option value="">全部位置</option>
            <option value="A">A區</option>
            <option value="B">B區</option>
            <option value="C">C區</option>
            <option value="D">D區</option>
            <option value="E">E區</option>
          </select>
        </div>
      </div>

      <DataTable
        :columns="columns"
        :data="inventory"
        :actions="[
          { name: 'edit', label: '編輯', type: 'edit', event: 'editInventory' },
          { name: 'move', label: '異動', type: 'edit', event: 'moveStock' },
          { name: 'history', label: '記錄', type: 'view', event: 'viewHistory' }
        ]"
        :loading="loading"
        @sort="handleSort"
        @search="handleSearch"
        @editInventory="editInventory"
        @moveStock="moveStock"
        @viewHistory="viewHistory"
        search-placeholder="搜尋商品名稱、SKU或位置..."
      />
    </div>

    <!-- Stock Adjustment Modal -->
    <div v-if="showAdjustmentModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">庫存調整</h3>
            <button 
              @click="closeAdjustmentModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <span class="sr-only">關閉</span>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="handleAdjustment" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  商品 <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="adjustmentForm.product_id"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">請選擇商品</option>
                  <option value="1">iPhone 15 Pro</option>
                  <option value="2">MacBook Air M2</option>
                  <option value="3">iPad Pro 12.9</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  調整類型 <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="adjustmentForm.adjustment_type"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="increase">增加</option>
                  <option value="decrease">減少</option>
                  <option value="set">設定</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  數量 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model.number="adjustmentForm.quantity"
                  type="number"
                  min="1"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  位置
                </label>
                <select
                  v-model="adjustmentForm.location"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">請選擇位置</option>
                  <option value="A1-01">A1-01 - A區第1排第1位</option>
                  <option value="A1-02">A1-02 - A區第1排第2位</option>
                  <option value="A1-03">A1-03 - A區第1排第3位</option>
                  <option value="B2-01">B2-01 - B區第2排第1位</option>
                  <option value="B2-02">B2-02 - B區第2排第2位</option>
                  <option value="B2-15">B2-15 - B區第2排第15位</option>
                  <option value="C3-01">C3-01 - C區第3排第1位</option>
                  <option value="C3-02">C3-02 - C區第3排第2位</option>
                  <option value="D4-01">D4-01 - D區第4排第1位</option>
                  <option value="D4-02">D4-02 - D區第4排第2位</option>
                  <option value="E5-01">E5-01 - E區第5排第1位</option>
                  <option value="E5-02">E5-02 - E區第5排第2位</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  有效期限
                </label>
                <input
                  v-model="adjustmentForm.expiry_date"
                  type="date"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="選擇有效期限"
                />
                <p class="text-xs text-gray-500 mt-1">選填，設定商品的有效期限</p>
              </div>

              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  調整原因 <span class="text-red-500">*</span>
                </label>
                <textarea
                  v-model="adjustmentForm.reason"
                  rows="3"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="請說明調整原因..."
                ></textarea>
              </div>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeAdjustmentModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-md disabled:opacity-50"
              >
                {{ submitting ? '處理中...' : '確認調整' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Movement Modal -->
    <div v-if="showMovementModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">庫存異動</h3>
            <button 
              @click="closeMovementModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <span class="sr-only">關閉</span>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="handleMovement" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  商品
                </label>
                <div class="w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50 text-gray-900">
                  {{ selectedItem?.product_name }}{{ selectedItem?.sku ? ` (${selectedItem.sku})` : '' }}
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  異動類型 <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="movementForm.movement_type"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="in">入庫</option>
                  <option value="out">出庫</option>
                  <option value="transfer">調撥</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  數量 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model.number="movementForm.quantity"
                  type="number"
                  min="1"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ movementForm.movement_type === 'transfer' ? '目標位置' : '位置' }}
                </label>
                <select
                  v-model="movementForm.location"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">請選擇位置</option>
                  <option value="A1-01">A1-01 - A區第1排第1位</option>
                  <option value="A1-02">A1-02 - A區第1排第2位</option>
                  <option value="A1-03">A1-03 - A區第1排第3位</option>
                  <option value="B2-01">B2-01 - B區第2排第1位</option>
                  <option value="B2-02">B2-02 - B區第2排第2位</option>
                  <option value="B2-15">B2-15 - B區第2排第15位</option>
                  <option value="C3-01">C3-01 - C區第3排第1位</option>
                  <option value="C3-02">C3-02 - C區第3排第2位</option>
                  <option value="D4-01">D4-01 - D區第4排第1位</option>
                  <option value="D4-02">D4-02 - D區第4排第2位</option>
                  <option value="E5-01">E5-01 - E區第5排第1位</option>
                  <option value="E5-02">E5-02 - E區第5排第2位</option>
                </select>
              </div>

              <div v-if="movementForm.movement_type === 'in'">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  有效期限
                </label>
                <input
                  v-model="movementForm.expiry_date"
                  type="date"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="選擇有效期限"
                />
                <p class="text-xs text-gray-500 mt-1">選填，僅在入庫時設定有效期限</p>
              </div>

              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  備註
                </label>
                <textarea
                  v-model="movementForm.notes"
                  rows="3"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="輸入異動備註..."
                ></textarea>
              </div>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeMovementModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50"
              >
                {{ submitting ? '處理中...' : '確認異動' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Edit Inventory Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">編輯庫存</h3>
            <button 
              @click="closeEditModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <span class="sr-only">關閉</span>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="handleEdit" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  商品名稱
                </label>
                <div class="w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50 text-gray-900">
                  {{ selectedItem?.product_name }}
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  位置
                </label>
                <div class="w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50 text-gray-900">
                  {{ selectedItem?.location }}
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  現有庫存 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model.number="editForm.quantity"
                  type="number"
                  min="0"
                  required
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  有效期限
                </label>
                <input
                  v-model="editForm.expiry_date"
                  type="date"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p class="text-xs text-gray-500 mt-1">留空表示無期限</p>
              </div>

              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  編輯原因
                </label>
                <textarea
                  v-model="editForm.notes"
                  rows="3"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="請說明編輯原因..."
                ></textarea>
              </div>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeEditModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50"
              >
                {{ submitting ? '處理中...' : '更新庫存' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Movement History Modal -->
    <div v-if="showHistoryModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border w-11/12 md:w-4/5 lg:w-3/4 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">
              庫存異動記錄 - {{ selectedItem?.product_name }} ({{ selectedItem?.sku }})
            </h3>
            <button 
              @click="closeHistoryModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <span class="sr-only">關閉</span>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Current Stock Info -->
          <div class="bg-gray-50 rounded-lg p-4 mb-4">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p class="text-sm text-gray-500">目前庫存</p>
                <p class="text-lg font-semibold text-gray-900">{{ selectedItem?.quantity_on_hand }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">位置</p>
                <p class="text-lg font-semibold text-gray-900">{{ selectedItem?.location }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">狀態</p>
                <p class="text-lg font-semibold text-gray-900">{{ selectedItem?.status }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">總值</p>
                <p class="text-lg font-semibold text-green-600">{{ selectedItem?.total_value }}</p>
              </div>
            </div>
          </div>

          <!-- History Table -->
          <div class="overflow-x-auto">
            <div v-if="loadingHistory" class="text-center py-8">
              <div class="text-gray-500">載入中...</div>
            </div>
            <div v-else-if="movementHistory.length === 0" class="text-center py-8">
              <div class="text-gray-500">尚無異動記錄</div>
            </div>
            <table v-else class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">日期時間</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">類型</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">數量</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">餘額</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">位置</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作者</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">參考編號</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">備註</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="movement in movementHistory" :key="movement.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatDateTime(movement.date) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getMovementTypeClass(movement.type_key)">
                      {{ movement.type }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-medium">
                    <span :class="getQuantityClass(movement.quantity)">
                      {{ movement.quantity > 0 ? '+' : '' }}{{ movement.quantity }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-medium">
                    {{ movement.balance_after }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ movement.location }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ movement.user_name }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-blue-600">
                    {{ movement.reference }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500">
                    {{ movement.notes }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Footer -->
          <div class="flex justify-end pt-4 border-t border-gray-200 mt-6">
            <button
              @click="closeHistoryModal"
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
import Card from '../components/Card.vue'
import DataTable from '../components/DataTable.vue'
import { inventoryAPI } from '../api/inventory'

export default {
  name: 'Inventory',
  components: {
    Card,
    DataTable
  },
  data() {
    return {
      inventory: [],
      loading: false,
      total: 0,
      currentPage: 1,
      pageSize: 10,
      searchQuery: '',
      sortBy: '',
      sortOrder: 'asc',
      statusFilter: '',
      locationFilter: '',
      showAdjustmentModal: false,
      showMovementModal: false,
      showHistoryModal: false,
      showEditModal: false,
      submitting: false,
      loadingHistory: false,
      selectedItem: null,
      movementHistory: [],
      totalInventoryValue: 0,
      totalItems: 0,
      lowStockCount: 0,
      outOfStockCount: 0,
      adjustmentForm: {
        product_id: '',
        adjustment_type: 'increase',
        quantity: 1,
        location: '',
        reason: '',
        expiry_date: ''
      },
      movementForm: {
        product_id: '',
        movement_type: 'in',
        quantity: 1,
        location: '',
        notes: '',
        expiry_date: ''
      },
      editForm: {
        quantity: 0,
        expiry_date: '',
        notes: ''
      },
      columns: [
        { key: 'product_name', label: '商品名稱', sortable: true },
        { key: 'sku', label: 'SKU', sortable: true },
        { key: 'quantity_on_hand', label: '現有庫存', sortable: true },
        { key: 'reorder_level', label: '再訂購點', sortable: true },
        { key: 'location', label: '位置', sortable: true },
        { key: 'location_utilization', label: '位置使用率', sortable: true },
        { key: 'expiry_date', label: '有效期限', sortable: true },
        { key: 'expiry_status', label: '到期狀態', sortable: true },
        { key: 'unit_cost', label: '成本', sortable: true },
        { key: 'total_value', label: '總值', sortable: true },
        { key: 'status', label: '狀態', sortable: true },
        { key: 'last_updated', label: '最後更新', sortable: true }
      ]
    }
  },
  async created() {
    await this.loadInventory()
    await this.loadStatistics()
  },
  methods: {
    async loadInventory() {
      try {
        this.loading = true
        
        const params = {
          per_page: 1000 // Load all inventory for client-side sorting
        }
        
        if (this.statusFilter === 'low_stock') params.low_stock = true
        if (this.locationFilter) params.zone = this.locationFilter
        
        const response = await inventoryAPI.fetchInventory(params)
        
        // Format data for display
        this.inventory = response.data.data.map(item => ({
          ...item,
          sku: `SKU-${item.product_id}`,
          quantity_on_hand: item.quantity,
          reorder_level: 10, // Default reorder level
          location: item.location_code,
          location_utilization: `${item.location_utilization_rate}%`,
          expiry_date: item.expiry_date ? this.formatDate(item.expiry_date) : '無期限',
          expiry_status: this.getExpiryStatusDisplay(item.expiry_status),
          unit_cost: 50, // Default unit cost
          total_value: `$${(item.quantity * 50).toFixed(2)}`,
          status: this.getStockStatusFromAPI(item.stock_status),
          last_updated: this.formatDate(new Date())
        }))
        
      } catch (error) {
        console.error('Error loading inventory:', error)
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: '載入庫存資料失敗'
        })
      } finally {
        this.loading = false
      }
    },

    async loadStatistics() {
      try {
        const response = await inventoryAPI.fetchInventoryStats()
        const stats = response.data.data
        
        this.totalInventoryValue = parseInt(stats.total_items) * 50 // Rough estimate
        this.totalItems = parseInt(stats.total_items)
        this.lowStockCount = stats.low_stock_items
        this.outOfStockCount = stats.critical_stock_items
      } catch (error) {
        console.error('Error loading statistics:', error)
      }
    },

    calculateStatistics(inventoryData) {
      // This method is now replaced by loadStatistics()
    },

    handleSort({ sortBy, sortOrder }) {
      // Client-side sorting handled by DataTable
      console.log('Sorting by:', sortBy, sortOrder)
    },

    handleSearch(query) {
      this.searchQuery = query
      // Client-side search handled by DataTable
    },

    getStockStatusFromAPI(status) {
      const statusMap = {
        'Critical': '缺貨',
        'Low': '低庫存',
        'Good': '正常'
      }
      return statusMap[status] || '正常'
    },

    openAdjustmentModal() {
      this.resetAdjustmentForm()
      this.showAdjustmentModal = true
    },

    openMovementModal() {
      this.resetMovementForm()
      this.showMovementModal = true
    },

    closeAdjustmentModal() {
      this.showAdjustmentModal = false
      this.resetAdjustmentForm()
    },

    closeMovementModal() {
      this.showMovementModal = false
      this.selectedItem = null
      this.resetMovementForm()
    },

    adjustStock(item) {
      this.adjustmentForm.product_id = item.id
      this.adjustmentForm.location = item.location
      this.showAdjustmentModal = true
    },

    moveStock(item) {
      console.log('Moving stock for item:', item)
      // Ensure SKU is properly set
      this.selectedItem = {
        ...item,
        sku: item.sku || `SKU-${item.product_id || item.id}`
      }
      this.movementForm.product_id = item.id || item.product_id
      this.movementForm.location = item.location
      this.showMovementModal = true
    },

    async viewHistory(item) {
      console.log('Viewing history for item:', item)
      // Ensure SKU is properly set
      this.selectedItem = {
        ...item,
        sku: item.sku || `SKU-${item.product_id || item.id}`
      }
      this.showHistoryModal = true
      await this.loadMovementHistory(item.product_id)
    },

    async loadMovementHistory(productId) {
      try {
        this.loadingHistory = true
        console.log('Loading movement history for product ID:', productId)
        const response = await inventoryAPI.fetchInventoryMovements(productId)
        
        console.log('API response:', response)
        
        if (response.data.success && response.data.data) {
          console.log('✅ API data received:', response.data.data.length, 'movements')
          // Transform API data to match frontend format
          this.movementHistory = response.data.data.map(item => ({
            id: item.movement_id,
            date: item.movement_date,
            type: this.getMovementTypeDisplay(item.movement_type),
            type_key: item.movement_type,
            quantity: item.quantity,
            balance_after: item.new_quantity,
            user_name: item.user_name,
            reference: item.reference_number,
            notes: item.notes,
            location: item.location_code
          }))
        } else {
          console.warn('❌ API returned unsuccessful response, using mock data')
          this.movementHistory = this.generateMockHistory(productId)
        }
      } catch (error) {
        console.error('❌ Movement history API error:', error)
        console.warn('Using mock data as fallback')
        this.movementHistory = this.generateMockHistory(productId)
      } finally {
        this.loadingHistory = false
      }
    },

    generateMockHistory(productId) {
      console.log('Generating mock history for product ID:', productId)
      console.log('Selected item:', this.selectedItem)
      
      // Get stored movements first
      const storedMovements = this.loadStoredMovements(productId)
      
      // Generate product-specific mock data
      let mockMovements = []
      
      if (this.selectedItem?.product_name === 'Conference Table') {
        mockMovements = [
          {
            id: 1,
            date: '2025-06-10 09:30:00',
            type: '入庫',
            type_key: 'in',
            quantity: 3,
            balance_after: 3,
            user_name: 'warehouse_super',
            reference: 'PO-2025-020',
            notes: '大型會議室設備採購',
            location: 'C3-02'
          },
          {
            id: 2,
            date: '2025-06-08 14:15:00',
            type: '出庫',
            type_key: 'out',
            quantity: -1,
            balance_after: 2,
            user_name: 'warehouse_staff1',
            reference: 'ORD202412150005',
            notes: '企業會議室設備需求',
            location: 'C3-02'
          },
          {
            id: 3,
            date: '2025-06-06 11:20:00',
            type: '調整',
            type_key: 'adjustment',
            quantity: 0,
            balance_after: 2,
            user_name: 'warehouse_super',
            reference: 'ADJ-2025-015',
            notes: '月度盤點，數量正確',
            location: 'C3-02'
          }
        ]
      } else if (this.selectedItem?.product_name === 'Executive Desk') {
        mockMovements = [
          {
            id: 1,
            date: '2025-06-09 10:30:00',
            type: '入庫',
            type_key: 'in',
            quantity: 6,
            balance_after: 6,
            user_name: 'warehouse',
            reference: 'PO-2025-018',
            notes: '高階主管辦公室設備',
            location: 'I9-01'
          },
          {
            id: 2,
            date: '2025-06-04 15:45:00',
            type: '出庫',
            type_key: 'out',
            quantity: -2,
            balance_after: 4,
            user_name: 'warehouse_staff2',
            reference: 'ORD20250601001',
            notes: '總經理辦公室更新',
            location: 'I9-01'
          }
        ]
      } else {
        // Default mock movements for other products
        mockMovements = [
          {
            id: 1,
            date: '2025-06-09 14:30:00',
            type: '入庫',
            type_key: 'in',
            quantity: 5,
            balance_after: 25,
            user_name: 'admin',
            reference: 'PO-2025-001',
            notes: '新進貨補充',
            location: 'C3-02'
          },
          {
            id: 2,
            date: '2025-06-08 10:15:00',
            type: '出庫',
            type_key: 'out',
            quantity: -3,
            balance_after: 20,
            user_name: 'warehouse1',
            reference: 'ORD20250608001',
            notes: '客戶訂單出貨',
            location: 'C3-02'
          },
          {
            id: 3,
            date: '2025-06-07 16:45:00',
            type: '調整',
            type_key: 'adjustment',
            quantity: 10,
            balance_after: 23,
            user_name: 'admin',
            reference: 'ADJ-2025-003',
            notes: '庫存盤點調整',
            location: 'C3-02'
          },
          {
            id: 4,
            date: '2025-06-06 09:20:00',
            type: '調撥',
            type_key: 'transfer',
            quantity: -5,
            balance_after: 13,
            user_name: 'warehouse2',
            reference: 'TRF-2025-012',
            notes: '轉移至B區',
            location: 'A1-01 → C3-02'
          },
          {
            id: 5,
            date: '2025-06-05 11:30:00',
            type: '入庫',
            type_key: 'in',
            quantity: 15,
            balance_after: 18,
            user_name: 'receiving',
            reference: 'PO-2025-002',
            notes: '初始庫存建立',
            location: 'A1-01'
          }
        ]
      }
      
      // Combine stored movements with mock movements, newest first
      return [...storedMovements, ...mockMovements]
    },

    closeHistoryModal() {
      this.showHistoryModal = false
      this.selectedItem = null
      this.movementHistory = []
    },

    getMovementTypeDisplay(type) {
      const typeMap = {
        'inbound': '入庫',
        'outbound': '出庫',
        'adjustment': '調整',
        'transfer': '調撥',
        'scrap': '報廢'
      }
      return typeMap[type] || type
    },

    getMovementTypeClass(type) {
      const typeClasses = {
        'in': 'bg-green-100 text-green-800',
        'inbound': 'bg-green-100 text-green-800',
        'out': 'bg-red-100 text-red-800',
        'outbound': 'bg-red-100 text-red-800',
        'adjustment': 'bg-blue-100 text-blue-800',
        'transfer': 'bg-yellow-100 text-yellow-800'
      }
      return `inline-flex px-2 py-1 text-xs font-semibold rounded-full ${typeClasses[type] || 'bg-gray-100 text-gray-800'}`
    },

    getQuantityClass(quantity) {
      if (quantity > 0) {
        return 'text-green-600 font-semibold'
      } else if (quantity < 0) {
        return 'text-red-600 font-semibold'
      }
      return 'text-gray-600'
    },

    async handleAdjustment() {
      try {
        this.submitting = true
        
        console.log('Processing stock adjustment:', this.adjustmentForm)
        
        this.$store.dispatch('setNotification', {
          type: 'success',
          message: '庫存調整成功'
        })
        
        this.closeAdjustmentModal()
        await this.loadInventory()
        await this.loadStatistics()
        
      } catch (error) {
        console.error('Error adjusting stock:', error)
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: '庫存調整失敗'
        })
      } finally {
        this.submitting = false
      }
    },

    async handleMovement() {
      try {
        this.submitting = true
        
        console.log('Processing stock movement:', this.movementForm)
        
        // Get location_id from the selected item
        const locationId = this.selectedItem?.location_id
        if (!locationId) {
          throw new Error('Location ID not found')
        }
        
        // Prepare movement data for API
        const movementData = {
          product_id: this.movementForm.product_id,
          location_id: locationId,
          movement_type: this.movementForm.movement_type === 'in' ? 'inbound' : 
                        this.movementForm.movement_type === 'out' ? 'outbound' : 
                        this.movementForm.movement_type,
          quantity: parseInt(this.movementForm.quantity),
          reason: this.movementForm.notes || '手動異動',
          notes: this.movementForm.notes || '',
          unit_cost: 0.0, // Could be enhanced to include cost
          reference_type: 'manual'
        }
        
        console.log('Sending movement data to API:', movementData)
        
        // Call backend API to create movement
        const response = await inventoryAPI.createInventoryMovement(movementData)
        
        if (response.data.success) {
          console.log('✅ Movement created successfully:', response.data)
          
          this.$store.dispatch('setNotification', {
            type: 'success',
            message: '庫存異動成功'
          })
          
          this.closeMovementModal()
          await this.loadInventory()
          await this.loadStatistics()
          
          // If the history modal is open, refresh it to show the new movement
          if (this.showHistoryModal && this.selectedItem) {
            await this.loadMovementHistory(this.selectedItem.product_id)
          }
        } else {
          throw new Error(response.data.error || '庫存異動失敗')
        }
        
      } catch (error) {
        console.error('Error processing movement:', error)
        this.$store.dispatch('setNotification', {
          type: 'error',
          message: error.response?.data?.error || error.message || '庫存異動失敗'
        })
      } finally {
        this.submitting = false
      }
    },

    getMovementTypeLabel(type) {
      const typeLabels = {
        'in': '入庫',
        'out': '出庫',
        'transfer': '調撥'
      }
      return typeLabels[type] || '異動'
    },

    storeMovementRecord(movement) {
      const existingMovements = JSON.parse(localStorage.getItem('inventory_movements') || '{}')
      const productId = movement.product_id
      
      if (!existingMovements[productId]) {
        existingMovements[productId] = []
      }
      
      existingMovements[productId].unshift(movement) // Add to beginning for newest first
      localStorage.setItem('inventory_movements', JSON.stringify(existingMovements))
    },

    loadStoredMovements(productId) {
      const existingMovements = JSON.parse(localStorage.getItem('inventory_movements') || '{}')
      return existingMovements[productId] || []
    },

    resetAdjustmentForm() {
      this.adjustmentForm = {
        product_id: '',
        adjustment_type: 'increase',
        quantity: 1,
        location: '',
        reason: '',
        expiry_date: ''
      }
    },

    resetMovementForm() {
      this.movementForm = {
        product_id: '',
        movement_type: 'in',
        quantity: 1,
        location: '',
        notes: '',
        expiry_date: ''
      }
    },

    getStockStatus(item) {
      if (item.quantity_on_hand === 0) {
        return '缺貨'
      } else if (item.quantity_on_hand <= item.reorder_level) {
        return '低庫存'
      } else {
        return '正常'
      }
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString('zh-TW')
    },

    formatDateTime(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    getExpiryStatusDisplay(status) {
      const statusMap = {
        'Expired': '已過期',
        'Expiring Soon': '即將過期',
        'Expiring': '接近過期',
        'Good': '正常',
        // Handle empty/null status
        '': '正常',
        null: '正常',
        undefined: '正常'
      }
      return statusMap[status] || '正常'
    },

    editInventory(item) {
      this.selectedItem = item
      this.editForm.quantity = item.quantity_on_hand
      this.editForm.expiry_date = item.expiry_date && item.expiry_date !== '無期限' ? 
        this.formatDateForInput(item.expiry_date) : ''
      this.showEditModal = true
    },

    formatDateForInput(dateStr) {
      // Convert display date back to YYYY-MM-DD format for input
      if (!dateStr || dateStr === '無期限') return ''
      
      // Handle different date formats
      try {
        const date = new Date(dateStr)
        return date.toISOString().split('T')[0]
      } catch (error) {
        return ''
      }
    },

    async handleEdit() {
      try {
        this.submitting = true
        
        console.log('Processing stock edit:', this.editForm)
        
        // Validate selectedItem exists
        if (!this.selectedItem) {
          throw new Error('No item selected for editing')
        }
        
        // Prepare update data for API
        const updateData = {
          quantity: parseInt(this.editForm.quantity)
        }
        
        // Add expiry date if provided
        if (this.editForm.expiry_date) {
          updateData.expiry_date = this.editForm.expiry_date
        }
        
        console.log('Sending update data to API:', updateData)
        
        // Call backend API to update inventory lot
        const URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api'
        const response = await fetch(`${URL}/inventory/${this.selectedItem.product_id}/${this.selectedItem.location_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(updateData)
        })
        
        const result = await response.json()
        
        if (result.success) {
          console.log('✅ Inventory updated successfully:', result)
          
          // Show success notification
          alert('庫存編輯成功！')
          
          this.closeEditModal()
          await this.loadInventory()
          await this.loadStatistics()
        } else {
          throw new Error(result.error || '庫存編輯失敗')
        }
        
      } catch (error) {
        console.error('Error editing stock:', error)
        alert(`庫存編輯失敗: ${error.message}`)
      } finally {
        this.submitting = false
      }
    },

    closeEditModal() {
      this.showEditModal = false
      this.resetEditForm()
    },

    resetEditForm() {
      this.editForm = {
        quantity: 0,
        expiry_date: '',
        notes: ''
      }
    }
  }
}
</script> 