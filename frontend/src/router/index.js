import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import EmployeesView from '../views/EmployeesView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/employees',
    name: 'employees',
    component: EmployeesView,
    meta: { 
      requiresAuth: true,
      requiresRole: ['admin', 'manager']
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const isAuthenticated = store.getters['auth/isAuthenticated']
    
    if (!isAuthenticated) {
      next('/login')
      return
    }

    if (to.meta.requiresRole) {
      const userRole = store.getters['auth/userRole']
      if (!to.meta.requiresRole.includes(userRole)) {
        next('/dashboard')
        return
      }
    }
    
    next()
  } else {
    next()
  }
})

export default router