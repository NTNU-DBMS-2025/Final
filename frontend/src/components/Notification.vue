<template>
  <div class="fixed top-4 inset-x-0 flex justify-center z-50">
    <div
      v-for="notification in notifications"
      :key="notification.id"
      :class="[
        'mb-4 max-w-sm w-full rounded-lg shadow-lg pointer-events-auto transition-all duration-500 transform',
        getNotificationClass(notification.type)
      ]"
    >
      <div class="p-4">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <div :class="getIconClass(notification.type)">
              {{ getIcon(notification.type) }}
            </div>
          </div>
          <div class="ml-3 w-0 flex-1 pt-0.5">
            <p :class="getTextClass(notification.type)" class="text-sm font-medium">
              {{ notification.message }}
            </p>
          </div>
          <div class="ml-4 flex-shrink-0 flex">
            <button
              @click="removeNotification(notification.id)"
              :class="getButtonClass(notification.type)"
              class="rounded-md inline-flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2"
            >
              <span class="sr-only">關閉</span>
              ×
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

export default {
  name: 'Notification',
  computed: {
    ...mapState(['notifications'])
  },
  methods: {
    ...mapMutations(['removeNotification']),
    getNotificationClass(type) {
      switch (type) {
        case 'success':
          return 'bg-green-50 border border-green-200'
        case 'error':
          return 'bg-red-50 border border-red-200'
        case 'warning':
          return 'bg-yellow-50 border border-yellow-200'
        case 'info':
        default:
          return 'bg-blue-50 border border-blue-200'
      }
    },
    getIconClass(type) {
      const baseClass = 'flex items-center justify-center w-6 h-6 rounded-full text-sm font-bold'
      switch (type) {
        case 'success':
          return `${baseClass} bg-green-100 text-green-600`
        case 'error':
          return `${baseClass} bg-red-100 text-red-600`
        case 'warning':
          return `${baseClass} bg-yellow-100 text-yellow-600`
        case 'info':
        default:
          return `${baseClass} bg-blue-100 text-blue-600`
      }
    },
    getTextClass(type) {
      switch (type) {
        case 'success':
          return 'text-green-900'
        case 'error':
          return 'text-red-900'
        case 'warning':
          return 'text-yellow-900'
        case 'info':
        default:
          return 'text-blue-900'
      }
    },
    getButtonClass(type) {
      switch (type) {
        case 'success':
          return 'text-green-400 hover:text-green-600 focus:ring-green-500'
        case 'error':
          return 'text-red-400 hover:text-red-600 focus:ring-red-500'
        case 'warning':
          return 'text-yellow-400 hover:text-yellow-600 focus:ring-yellow-500'
        case 'info':
        default:
          return 'text-blue-400 hover:text-blue-600 focus:ring-blue-500'
      }
    },
    getIcon(type) {
      switch (type) {
        case 'success':
          return '✓'
        case 'error':
          return '✕'
        case 'warning':
          return '!'
        case 'info':
        default:
          return 'i'
      }
    }
  }
}
</script> 