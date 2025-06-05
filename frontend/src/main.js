import './assets/main.css'
import './assets/tailwind.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Global responsive utilities
const globalStyles = `
/* Full width layout fixes */
html, body, #app {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  box-sizing: border-box !important;
}

* {
  box-sizing: border-box;
}
/* Responsive container utilities */
.responsive-container {
  width: 100%;
  max-width: none;
  padding: 0;
}

.responsive-grid-1-2-3-4 {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1rem;
}

@media (min-width: 640px) {
  .responsive-grid-1-2-3-4 {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .responsive-grid-1-2-3-4 {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1280px) {
  .responsive-grid-1-2-3-4 {
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
  }
}

.responsive-grid-1-2 {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1rem;
}

@media (min-width: 1024px) {
  .responsive-grid-1-2 {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
}

/* Better form layouts */
.responsive-form-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1rem;
}

@media (min-width: 768px) {
  .responsive-form-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Table responsive wrapper */
.table-responsive {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.table-responsive::-webkit-scrollbar {
  height: 4px;
}

.table-responsive::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.table-responsive::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

/* Modal responsive improvements */
.responsive-modal {
  width: 95vw;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

@media (min-width: 640px) {
  .responsive-modal {
    width: 90vw;
  }
}

@media (min-width: 768px) {
  .responsive-modal {
    width: 600px;
  }
}

/* Responsive text scaling */
.responsive-title {
  font-size: 1.25rem;
  font-weight: 700;
}

@media (min-width: 640px) {
  .responsive-title {
    font-size: 1.5rem;
  }
}

/* Navigation responsive improvements */
.nav-item-responsive {
  font-size: 0.75rem;
  padding: 0.5rem;
}

@media (min-width: 1280px) {
  .nav-item-responsive {
    font-size: 0.875rem;
    padding: 0.5rem 0.75rem;
  }
}
`

// Add global styles to head
const style = document.createElement('style')
style.textContent = globalStyles
document.head.appendChild(style)

const app = createApp(App)

app.use(store)
app.use(router)

app.mount('#app')
