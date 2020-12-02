import { createApp } from 'vue'
import App from './App.vue'
import './assets/style.css'
import router from './router'
import  VueHtmlToPaper from './VueHtmlToPaper'

const app = createApp(App)
app.use(router)
app.use(VueHtmlToPaper)
app.mount('#app')
