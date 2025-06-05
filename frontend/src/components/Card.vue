<template>
  <div :class="cardClasses">
    <div class="flex items-center justify-between mb-4" v-if="title || icon">
      <div class="flex items-center">
        <div v-if="icon" :class="iconClasses" class="mr-3">
          <component :is="iconComponent" class="w-6 h-6" />
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
      type: String,
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
        'rounded-lg shadow-lg p-6 transition-shadow hover:shadow-xl',
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
    iconComponent() {
      // For now, using simple div. In production, you might use an icon library
      return 'div'
    }
  }
}
</script> 