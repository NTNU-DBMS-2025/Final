<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          倉儲管理系統
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          請登入您的帳號
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="account" class="sr-only">帳號</label>
            <input
              id="account"
              v-model="form.account"
              name="account"
              type="text"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="帳號"
            />
          </div>
          <div>
            <label for="password" class="sr-only">密碼</label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="密碼"
            />
          </div>
        </div>

        <div v-if="error" class="bg-red-50 border border-red-300 rounded-md p-3">
          <p class="text-sm text-red-700 text-center">{{ error }}</p>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-400 disabled:cursor-not-allowed transition-colors"
          >
            <span v-if="loading">登入中...</span>
            <span v-else>登入</span>
          </button>
        </div>

        <!-- Demo accounts info -->
        <div class="mt-6 bg-blue-50 border border-blue-200 rounded-md p-4">
          <h3 class="text-sm font-medium text-blue-900 mb-2">測試帳號</h3>
          <div class="text-xs text-blue-800 space-y-1">
            <p><strong>管理者:</strong> 帳號/密碼: admin</p>
            <p><strong>銷售員:</strong> 帳號/密碼: sales</p>
            <p><strong>倉庫員:</strong> 帳號/密碼: warehouse</p>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        account: '',
        password: ''
      },
      loading: false,
      error: ''
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  created() {
    // Redirect if already logged in
    if (this.isAuthenticated) {
      this.redirectToDashboard()
    }
  },
  methods: {
    ...mapActions(['login', 'showNotification']),
    async handleSubmit() {
      this.loading = true
      this.error = ''

      try {
        const response = await this.login(this.form)
        
        this.showNotification({
          type: 'success',
          message: '登入成功'
        })

        // Redirect based on user role
        this.redirectToDashboard()
      } catch (error) {
        this.error = error.message || '登入失敗，請檢查您的帳號密碼'
      } finally {
        this.loading = false
      }
    },
    redirectToDashboard() {
      const roles = this.$store.state.roles
      
      if (roles.includes('Admin')) {
        this.$router.push('/admin')
      } else if (roles.includes('Sales')) {
        this.$router.push('/sales')
      } else if (roles.includes('Warehouse')) {
        this.$router.push('/warehouse')
      } else {
        this.$router.push('/admin') // Default fallback
      }
    }
  }
}
</script> 