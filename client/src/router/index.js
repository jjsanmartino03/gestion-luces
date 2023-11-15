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
          path: '/dashboard/stats', // Default child route.
          name: 'stats',
          component: () => import('@/views/dashboard/Stats.vue')
        },
        {
          path: '/dashboard/aulas', // Default child route.
          name: 'aulas',
          component: () => import('@/views/dashboard/Aulas.vue')
        },
        {
          path: '/dashboard/usuarios', // Default child route.
          name: 'usuarios',
          component: () => import('@/views/dashboard/usuarios/Usuarios.vue')
        },
        {
          path: '/dashboard/usuarios/crear', // Default child route.
          name: 'nuevo-usuario',
          component: () => import('@/views/dashboard/usuarios/NuevoUsuario.vue')
        },
        {
          path: '/dashboard/usuarios/:id', // Default child route.
          name: 'editar-usuario',
          component: () => import('@/views/dashboard/usuarios/EditarUsuario.vue')
        }
      ]

    }
  ]
}

const router = createRouter(options)

export default router
