import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue') },
  {
    path: '/',
    component: () => import('../components/PrivateLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Dashboard', component: () => import('../views/DashboardView.vue') },
      { path: 'reports', name: 'Reports', component: () => import('../views/ReportsView.vue') },
      { path: 'daily-entry', name: 'DailyEntry', component: () => import('../views/DailyEntryView.vue') },
      { path: 'bulk-entry', name: 'BulkEntry', component: () => import('../views/BulkEntryView.vue') },
      { path: 'customers', name: 'Customers', component: () => import('../views/CustomersView.vue') },
      { path: 'portal/:id?', name: 'CustomerPortal', component: () => import('../views/CustomerPortalView.vue') },
      { path: 'payments', name: 'Payments', component: () => import('../views/PaymentsView.vue') }
    ]
  }
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.token) {
    next('/login')
  } else {
    next()
  }
})

export default router