import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// Layout
import AppLayout from '../components/AppLayout.vue'

// Views
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import EmployeesView from '../views/EmployeesView.vue'
import ActivityView from '../views/ActivityView.vue'
import ReportsView from '../views/ReportsView.vue'

// Components (для вложенного отображения в dashboard)
import WorkTimer from '@/components/WorkTimer.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'Начальная' }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { title: 'Авторизация' }
  },
  {
    path: '/',
    component: AppLayout, // обёртка с боковой панелью
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        component: DashboardView,
        meta: { title: 'Главная' },
        children: [
          {
            path: '',
            name: 'dashboard-home',
            component: WorkTimer
          }
        ]
      },
      {
        path: 'activity',
        name: 'activity',
        component: ActivityView,
        meta: { 
          title: 'Активность'
        }
      },
      {
        path: 'reports',
        name: 'reports',
        component: ReportsView,
        meta: { 
          title: 'Отчеты'
        }
      },
      {
        path: 'employees',
        name: 'employees',
        component: EmployeesView,
        meta: { 
          title: 'Сотрудники',
          requiresRole: ['admin', 'manager']
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Глобальный охранник маршрутов
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresRole = to.meta?.requiresRole

  const isAuthenticated = store.getters['auth/isAuthenticated']
  const userRole = store.getters['auth/userRole']

  if (requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }

  if (requiresRole && !requiresRole.includes(userRole)) {
    next('/dashboard')
    return
  }

  // Обновляем title страницы
  document.title = to.meta?.title 
    ? `${to.meta.title} | TimeTracker Pro` 
    : 'TimeTracker Pro'

  next()
})

export default router