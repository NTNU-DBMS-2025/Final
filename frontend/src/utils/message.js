// Simple message utility for notifications
export const message = {
    success(text) {
        this.show(text, 'success')
    },

    error(text) {
        this.show(text, 'error')
    },

    info(text) {
        this.show(text, 'info')
    },

    warning(text) {
        this.show(text, 'warning')
    },

    show(text, type = 'info') {
        // Create notification element
        const notification = document.createElement('div')
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transform transition-all duration-300 ${this.getTypeStyles(type)}`
        notification.textContent = text

        // Add to DOM
        document.body.appendChild(notification)

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)'
            notification.style.opacity = '1'
        }, 10)

        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)'
            notification.style.opacity = '0'

            setTimeout(() => {
                if (notification.parentNode) {
                    document.body.removeChild(notification)
                }
            }, 300)
        }, 3000)

        // Click to dismiss
        notification.addEventListener('click', () => {
            notification.style.transform = 'translateX(100%)'
            notification.style.opacity = '0'

            setTimeout(() => {
                if (notification.parentNode) {
                    document.body.removeChild(notification)
                }
            }, 300)
        })
    },

    getTypeStyles(type) {
        const styles = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            warning: 'bg-yellow-500 text-white',
            info: 'bg-blue-500 text-white'
        }
        return styles[type] || styles.info
    }
}

// Vue plugin
export default {
    install(app) {
        app.config.globalProperties.$message = message
        app.provide('message', message)
    }
} 