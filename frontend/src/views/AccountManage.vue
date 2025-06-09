<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">帳號管理</h1>
      <p class="mt-1 text-sm text-gray-500">
        管理所有帳號。
      </p>
    </div>
    
    <!-- Account Table -->
    <DataTable
      title="帳號列表"
      :columns="columns"
      :data="users"
      :actions="actions"
      :loading="loading"
      :total="total"
      :current-page="currentPage"
      :page-size="pageSize"
      @add="openAddModal"
      @edit="openEditModal"
      @delete="handleDelete"
      @search="handleSearch"
      @page-change="handlePageChange"
    />

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ isEditing ? '編輯帳號' : '新增帳號' }}
          </h3>
          
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">帳號名稱</label>
              <input
                v-model="form.name"
                type="text"
                required
                class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="請輸入帳號名稱"
              />
            </div>
            
            
             <div>
              <label class="block text-sm font-medium text-gray-700">帳號密碼</label>
              <input
                v-model.number="form.pwd_hash"
                type="password"
                required
                class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="0000"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">權限</label>
              <select
                v-model="form.category"
                required
                class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">請選擇權限</option>
                <option value="Admin">Admin</option>
                <option value="Sales">Sales</option>
                <option value="Warehouse">Warehouse</option>
              </select>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-400"
              >
                {{ submitting ? '處理中...' : (isEditing ? '更新' : '新增') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
          <h3 class="text-lg font-medium text-gray-900">確認刪除</h3>
          <div class="mt-2 px-7 py-3">
            <p class="text-sm text-gray-500">
              確定要刪除帳號「{{ deleteTarget?.name }}」嗎？此操作無法復原。
            </p>
          </div>
          <div class="items-center px-4 py-3 flex justify-center space-x-3">
            <button
              @click="showDeleteModal = false"
              class="px-4 py-2 bg-gray-300 text-gray-800 text-base font-medium rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300"
            >
              取消
            </button>
            <button
              @click="confirmDelete"
              :disabled="submitting"
              class="px-4 py-2 bg-red-600 text-white text-base font-medium rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-600 disabled:bg-red-400"
            >
              {{ submitting ? '刪除中...' : '確認刪除' }}
            </button>
          </div>
        </div>
      </div>
    </div>
   </div>
  
</template>

<script>
import DataTable from '../components/DataTable.vue'
import { mapActions } from 'vuex'
import {
  fetchUsers,
  createUser,
  updateUser,
  deleteUser
} from '../api/users'

export default {
  name: 'AccountManage',
  components: {
    DataTable
  },
  data() {
    return {
      accounts: [],
      loading: false,
      total: 0,
      currentPage: 1,
      pageSize: 10,
      searchQuery: '',
      showModal: false,
      showDeleteModal: false,
      isEditing: false,
      submitting: false,
      deleteTarget: null,
      form: {
        user_id: '',
        account: '',
        pwd_hash: '',
        role_id: ''
      },
      columns: [
        { key: 'user_id', label: '使用者id', sortable: true },
        { key: 'account', label: '帳號', sortable: true },
        { key: 'pwd_hash', label: '密碼', sortable: true },
        { key: 'role_id', label: '角色', sortable: true }
      ],
      actions: [
        { name: 'edit', label: '編輯', event: 'edit', type: 'edit' },
        { name: 'delete', label: '刪除', event: 'delete', type: 'delete' }
      ]
    }
  },
  async created() {
    await this.loadUsers()
  },
  methods: {
    // ...mapActions(['showNotification']),

    async loadUsers() {
      this.loading = true
      try {
        const params = {
          page: this.currentPage,
          per_page: this.pageSize,
          search: this.searchQuery
        }
        const response = await fetchUsers(params)
        this.accounts = response.data.data
        this.total = response.data.pagination?.total || response.data.data.length
      } catch (error) {
        console.error('Failed to load users:', error)
        this.showNotification({
          type: 'error',
          message: '載入使用者失敗'
        })
      } finally {
        this.loading = false
      }
    },

    openAddModal() {
      this.isEditing = false
      this.form = {
        user_id: '',
        account: '',
        pwd_hash: '',
        role_id: ''
      }
      this.showModal = true
    },

    openEditModal(user) {
      this.isEditing = true
      this.form = {
        user_id: user.user_id,
        account: user.account,
        pwd_hash: user.pwd_hash,
        role_id: user.role_id
      }
      this.showModal = true
    },

    closeModal() {
      this.showModal = false
      this.form = {
        user_id: '',
        account: '',
        pwd_hash: '',
        role_id: ''
      }
    },

    async handleSubmit() {
      this.submitting = true
      try {
        const payload = {
          account: this.form.account,
          role_id: this.form.role_id
        }

        if (this.isEditing) {
          await updateUser(this.form.id, payload)
          this.showNotification({
            type: 'success',
            message: '帳號更新成功'
          })
        } else {
          await createUser(payload)
          this.showNotification({
            type: 'success',
            message: '帳號新增成功'
          })
        }
        this.closeModal()
        await this.loadUsers()
      } catch (error) {
        console.error('Submit failed:', error)
        this.showNotification({
          type: 'error',
          message: this.isEditing ? '帳號更新失敗' : '帳號新增失敗'
        })
      } finally {
        this.submitting = false
      }
    },

    handleDelete(user) {
      this.deleteTarget = user
      this.showDeleteModal = true
    },

    async confirmDelete() {
      this.submitting = true
      try {
        await deleteUser(this.deleteTarget.user_id)
        this.showNotification({
          type: 'success',
          message: '帳號刪除成功'
        })
        this.showDeleteModal = false
        this.deleteTarget = null
        await this.loadUsers()
      } catch (error) {
        console.error('Delete failed:', error)
        this.showNotification({
          type: 'error',
          message: '帳號刪除失敗'
        })
      } finally {
        this.submitting = false
      }
    },

    async handleSearch(query) {
      this.searchQuery = query
      this.currentPage = 1
      await this.loadUsers()
    },

    async handlePageChange(page) {
      this.currentPage = page
      await this.loadUsers()
    }
  }
}
</script>