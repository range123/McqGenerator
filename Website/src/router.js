import {createRouter,createWebHistory} from "vue-router"
import Home from './pages/Home'
import About from './pages/About'
const routes = [
    { path : '/', component : Home},
    { path : '/about', component : About}
]
const router = createRouter({
    // history : createWebHashHistory(),
    history : createWebHistory(),
    routes,
})
export default router;