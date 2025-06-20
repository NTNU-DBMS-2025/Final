<template>
  <div :class="cardClasses">
    <div class="flex items-center justify-between mb-4" v-if="title || icon">
      <div class="flex items-center">
        <div v-if="icon" :class="iconClasses" class="mr-3">
          <span class="text-lg">{{ iconEmoji }}</span>
        </div>
        <h3 v-if="title" class="text-lg font-semibold text-gray-900">{{ title }}</h3>
      </div>
      <router-link 
        v-if="link && linkText" 
        :to="link" 
        class="text-sm text-blue-600 hover:text-blue-800 transition-colors"
      >
        {{ linkText }}
      </router-link>
    </div>
    
    <div class="mb-4">
      <slot></slot>
    </div>
    
    <div v-if="footerText" class="text-sm text-gray-500 border-t pt-3">
      {{ footerText }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    title: {
      type: String,
      default: ''
    },
    icon: {
      type: String,
      default: ''
    },
    color: {
      type: String,
      default: 'bg-white'
    },
    footerText: {
      type: String,
      default: ''
    },
    link: {
      type: [String, Object],
      default: ''
    },
    linkText: {
      type: String,
      default: '查看詳情'
    }
  },
  computed: {
    cardClasses() {
      return [
        'rounded-lg shadow-lg p-6 transition-shadow card-hover',
        this.color
      ]
    },
    iconClasses() {
      const baseClasses = 'w-12 h-12 rounded-full flex items-center justify-center'
      switch (this.icon) {
        case 'inventory':
          return [baseClasses, 'bg-green-100 text-green-600']
        case 'orders':
          return [baseClasses, 'bg-blue-100 text-blue-600']
        case 'shipments':
          return [baseClasses, 'bg-purple-100 text-purple-600']
        case 'products':
          return [baseClasses, 'bg-yellow-100 text-yellow-600']
        case 'customers':
          return [baseClasses, 'bg-pink-100 text-pink-600']
        case 'warning':
          return [baseClasses, 'bg-red-100 text-red-600']
        default:
          return [baseClasses, 'bg-gray-100 text-gray-600']
      }
    },
    iconEmoji() {
      const iconMap = {
        'inventory': '📦',
        'orders': '📋',
        'shipments': '🚚',
        'products': '🏷️',
        'customers': '👥',
        'warning': '⚠️',
        'scrap': '🗑️',
        'suppliers': '🏭',
        'reports': '📊'
      }
      return iconMap[this.icon] || '📄'
    }
  }
}
</script>

<style scoped>
/* Card hover effects - only on hover-capable devices */
.card-hover {
  cursor: default;
}

@media (hover: hover) and (pointer: fine) {
  .card-hover:hover {
    box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  }
}

/* Ensure links within cards have proper cursor */
a {
  cursor: pointer;
}

/* Reset any unwanted pointer behavior */
.card-hover * {
  pointer-events: auto;
}
</style>