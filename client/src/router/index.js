import { createRouter, createWebHistory } from 'vue-router'

const options = {
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'welcome',
      component: () => import('../views/WelcomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      children: [
        {
          path: '', // Default child route.
          name: 'home',
          component: () => import('@/views/dashboard/Home.vue')
        },
        {
          path: '/stats', // Default child route.
          name: 'stats',
          component: () => import('@/views/dashboard/Stats.vue')
        },
        {
          path: '/aulas', // Default child route.
          name: 'aulas',
          component: () => import('@/views/dashboard/Aulas.vue')
        },
        {
          path: '/usuarios', // Default child route.
          name: 'usuarios',
          component: () => import('@/views/dashboard/Usuarios.vue')
        }
      ]

    }
  ]
}

const router = createRouter(options)

export default router
