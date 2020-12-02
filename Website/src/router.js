import {createRouter,createWebHistory} from "vue-router"
import Home from './pages/Home'
const routes = [
    { path : '/', component : Home},
]
const router = createRouter({
    // history : createWebHashHistory(),
    history : createWebHistory(),
    routes,
})
export default router;