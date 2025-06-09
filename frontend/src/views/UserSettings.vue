<template>
  <div class="max-w-2xl mx-auto space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">用戶設定</h1>
      <p class="mt-1 text-sm text-gray-500">
        管理您的個人資訊和帳號設定。
      </p>
    </div>

    <!-- User Info Card -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">用戶資訊</h3>
        
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label class="block text-sm font-medium text-gray-700">帳號名稱</label>
            <div class="mt-1 p-3 bg-gray-50 border border-gray-300 rounded-md">
              {{ user?.account || '未設定' }}
            </div>
            <p class="mt-1 text-xs text-gray-500">帳號名稱無法修改</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">用戶角色</label>
            <div class="mt-1 p-3 bg-gray-50 border border-gray-300 rounded-md">
              {{ user?.role_name || '未知' }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Password Change Card -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">更改密碼</h3>
        
        <form @submit.prevent="handlePasswordChange" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">目前密碼</label>
            <input
              v-model="passwordForm.currentPassword"
              type="password"
              required
              class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="請輸入目前密碼"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">新密碼</label>
            <input
              v-model="passwordForm.newPassword"
              type="password"
              required
              class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="請輸入新密碼 (至少6位)"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">確認新密碼</label>
            <input
              v-model="passwordForm.confirmPassword"
              type="password"
              required
              class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="請再次輸入新密碼"
            />
          </div>
          
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="resetPasswordForm"
              class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              取消
            </button>
            <button
              type="submit"
              :disabled="submitting || !isPasswordFormValid"
              class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-400"
            >
              {{ submitting ? '更新中...' : '更新密碼' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { changePassword } from '../api/users'

export default {
  name: 'UserSettings',
  data() {
    return {
      submitting: false,
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    }
  },
  computed: {
    ...mapState(['user']),
    
    isPasswordFormValid() {
      return (
        this.passwordForm.currentPassword &&
        this.passwordForm.newPassword &&
        this.passwordForm.confirmPassword &&
        this.passwordForm.newPassword === this.passwordForm.confirmPassword &&
        this.passwordForm.newPassword.length >= 6
      )
    }
  },
  methods: {
    ...mapActions(['showNotification']),
    
    async handlePasswordChange() {
      if (!this.isPasswordFormValid) {
        this.showNotification({
          type: 'error',
          message: '請檢查密碼輸入是否正確'
        })
        return
      }

      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        this.showNotification({
          type: 'error',
          message: '新密碼與確認密碼不一致'
        })
        return
      }

      if (this.passwordForm.newPassword.length < 6) {
        this.showNotification({
          type: 'error',
          message: '新密碼長度至少需要6位'
        })
        return
      }

      this.submitting = true
      try {
        const passwordData = {
          current_password: this.passwordForm.currentPassword,
          new_password: this.passwordForm.newPassword
        }

        await changePassword(this.user.user_id, passwordData)
        
        this.showNotification({
          type: 'success',
          message: '密碼更新成功'
        })
        
        this.resetPasswordForm()
      } catch (error) {
        console.error('Password change failed:', error)
        const errorMessage = error.response?.data?.error || error.message || '密碼更新失敗'
        this.showNotification({
          type: 'error',
          message: errorMessage
        })
      } finally {
        this.submitting = false
      }
    },
    
    resetPasswordForm() {
      this.passwordForm = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    }
  }
}
</script> 