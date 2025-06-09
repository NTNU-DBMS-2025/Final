<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">帳號管理</h1>
      <p class="mt-1 text-sm text-gray-500">
        管理所有使用者帳號。
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
        <h3 class="text-lg font-medium text-gray-900 mb-4">
          {{ isEditing ? '編輯帳號' : '新增帳號' }}
        </h3>
        
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">帳號名稱</label>
            <input
              v-model="form.account"
              type="text"
              required
              class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="請輸入帳號名稱"
            />
          </div>
          
          <div v-if="!isEditing">
            <label class="block text-sm font-medium text-gray-700">密碼</label>
            <input
              v-model="form.password"
              type="password"
              required
              class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="請輸入密碼 (至少6位)"
            />
          </div>
          
          <div v-if="isEditing">
            <div class="flex items-center justify-between">
              <label class="block text-sm font-medium text-gray-700">密碼</label>
              <button
                type="button"
                @click="showPasswordField = !showPasswordField"
                class="text-sm text-blue-600 hover:text-blue-800"
              >
                {{ showPasswordField ? '取消修改密碼' : '修改密碼' }}
              </button>
            </div>
            <input
              v-if="showPasswordField"
              v-model="form.password"
              type="password"
              class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="請輸入新密碼 (至少6位)"
            />
          </div>
          
                      <div>
              <label class="block text-sm font-medium text-gray-700">角色</label>
              <select
                v-model="form.role_id"
                required
                :disabled="isOwnerRoleUser"
                class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
              >
                <option value="">請選擇角色</option>
                <option v-for="role in filteredRoles" :key="role.role_id" :value="role.role_id">
                  {{ role.role_name }}
                </option>
              </select>
              <p v-if="isOwnerRoleUser" class="mt-1 text-xs text-gray-500">
                擁有者角色不能被修改
              </p>
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

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
          <h3 class="text-lg font-medium text-gray-900">確認刪除</h3>
          <div class="mt-2 px-7 py-3">
            <p class="text-sm text-gray-500">
              確定要刪除帳號「{{ deleteTarget?.account }}」嗎？此操作無法復原。
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
  deleteUser,
  fetchRoles
} from '../api/users'

export default {
  name: 'AccountManage',
  components: {
    DataTable
  },
  data() {
    return {
      users: [],
      availableRoles: [],
      loading: false,
      total: 0,
      currentPage: 1,
      pageSize: 10,
      searchQuery: '',
      showModal: false,
      showDeleteModal: false,
      showPasswordField: false,
      isEditing: false,
      submitting: false,
      deleteTarget: null,
      form: {
        account: '',
        password: '',
        role_id: ''
      },
      columns: [
        { key: 'user_id', label: '使用者ID', sortable: true },
        { key: 'account', label: '帳號', sortable: true },
        { key: 'primary_role', label: '角色', sortable: true }
      ],
      actions: [
        { name: 'edit', label: '編輯', event: 'edit', type: 'edit' },
        { name: 'delete', label: '刪除', event: 'delete', type: 'delete' }
      ]
    }
  },
  computed: {
    // Check if current user is Owner
    isCurrentUserOwner() {
      return this.$store.getters.hasRole('Owner')
    },
    // Check if the user being edited has Owner role
    isOwnerRoleUser() {
      if (!this.isEditing) return false
      const ownerRole = this.availableRoles.find(role => role.role_name === 'Owner')
      return ownerRole && this.form.role_id === ownerRole.role_id
    },
    // Filter roles based on current user permissions
    filteredRoles() {
      if (this.isCurrentUserOwner) {
        // Owner can assign any role
        return this.availableRoles
      } else if (this.$store.getters.hasRole('Admin')) {
        // Admin cannot assign Owner or Admin roles
        return this.availableRoles.filter(role => role.role_name !== 'Owner' && role.role_name !== 'Admin')
      } else {
        // Other roles cannot assign Owner role
        return this.availableRoles.filter(role => role.role_name !== 'Owner')
      }
    }
  },
  async created() {
    await Promise.all([
      this.loadUsers(),
      this.loadRoles()
    ])
  },
  methods: {
    ...mapActions(['showNotification']),

    async loadUsers() {
      this.loading = true
      try {
        const params = {
          page: this.currentPage,
          per_page: this.pageSize,
          search: this.searchQuery
        }
        const response = await fetchUsers(params)
        this.users = response.data.data
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

    async loadRoles() {
      try {
        const response = await fetchRoles()
        this.availableRoles = response.data.data
      } catch (error) {
        console.error('Failed to load roles:', error)
        this.showNotification({
          type: 'error',
          message: '載入角色失敗'
        })
      }
    },

    openAddModal() {
      this.isEditing = false
      this.showPasswordField = false
      this.form = {
        account: '',
        password: '',
        role_id: ''
      }
      this.showModal = true
    },

    openEditModal(user) {
      // Check if trying to edit an Owner user without being an Owner
      if (user.primary_role === 'Owner' && !this.isCurrentUserOwner) {
        this.showNotification({
          type: 'error',
          message: '只有擁有者可以編輯擁有者帳號'
        })
        return
      }

      // Check if Admin trying to edit another Admin user
      if (user.primary_role === 'Admin' && this.$store.getters.hasRole('Admin') && !this.isCurrentUserOwner) {
        this.showNotification({
          type: 'error',
          message: '管理者無法編輯其他管理者帳號'
        })
        return
      }

      this.isEditing = true
      this.showPasswordField = false
      this.form = {
        user_id: user.user_id,
        account: user.account,
        password: '', // Don't show current password
        role_id: user.role_id
      }
      this.showModal = true
    },

    closeModal() {
      this.showModal = false
      this.showPasswordField = false
      this.form = {
        account: '',
        password: '',
        role_id: ''
      }
    },

    async handleSubmit() {
      this.submitting = true
      try {
        const payload = {
          account: this.form.account,
          role_id: parseInt(this.form.role_id)
        }

        if (this.isEditing) {
          // Prevent changing Owner role if user is Owner but current user is not Owner
          const originalUser = this.users.find(u => u.user_id === this.form.user_id)
          if (originalUser && originalUser.primary_role === 'Owner' && !this.isCurrentUserOwner) {
            this.showNotification({
              type: 'error',
              message: '只有擁有者可以修改擁有者帳號的角色'
            })
            return
          }

          // Prevent Admin from modifying other Admin accounts
          if (originalUser && originalUser.primary_role === 'Admin' && this.$store.getters.hasRole('Admin') && !this.isCurrentUserOwner) {
            this.showNotification({
              type: 'error',
              message: '管理者無法修改其他管理者帳號'
            })
            return
          }

          // Only add password if we're in edit mode and password field is shown and password is provided
          if (this.showPasswordField && this.form.password && this.form.password.trim()) {
            payload.password = this.form.password
          }
          await updateUser(this.form.user_id, payload)
          this.showNotification({
            type: 'success',
            message: '帳號更新成功'
          })
        } else {
          // For new users, password is required
          if (!this.form.password || !this.form.password.trim()) {
            this.showNotification({
              type: 'error',
              message: '新增帳號時必須提供密碼'
            })
            return
          }

          // Prevent Admin from creating Admin or Owner accounts
          const selectedRole = this.availableRoles.find(r => r.role_id == this.form.role_id)
          if (selectedRole && (selectedRole.role_name === 'Admin' || selectedRole.role_name === 'Owner') && this.$store.getters.hasRole('Admin') && !this.isCurrentUserOwner) {
            this.showNotification({
              type: 'error',
              message: '管理者無法創建管理者或擁有者帳號'
            })
            return
          }

          payload.password = this.form.password
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
        const errorMessage = error.response?.data?.error || error.message || '操作失敗'
        this.showNotification({
          type: 'error',
          message: this.isEditing ? `帳號更新失敗: ${errorMessage}` : `帳號新增失敗: ${errorMessage}`
        })
      } finally {
        this.submitting = false
      }
    },

    handleDelete(user) {
      // Check if trying to delete an Owner user without being an Owner
      if (user.primary_role === 'Owner' && !this.isCurrentUserOwner) {
        this.showNotification({
          type: 'error',
          message: '只有擁有者可以刪除擁有者帳號'
        })
        return
      }

      // Check if Admin trying to delete another Admin user
      if (user.primary_role === 'Admin' && this.$store.getters.hasRole('Admin') && !this.isCurrentUserOwner) {
        this.showNotification({
          type: 'error',
          message: '管理者無法刪除其他管理者帳號'
        })
        return
      }

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
        const errorMessage = error.response?.data?.error || error.message || '刪除失敗'
        this.showNotification({
          type: 'error',
          message: `帳號刪除失敗: ${errorMessage}`
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