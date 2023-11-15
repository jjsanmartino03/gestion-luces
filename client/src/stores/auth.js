import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    isAuthenticated: localStorage.getItem('token') !== null,
    user: null
  }),

  actions: {
    async login(username, password) {

      try {
        const response = await api.post('login/', { username, password })

        this.token = response.data.token
        localStorage.setItem('token', response.data.token)
        this.isAuthenticated = true
        return true
      } catch (e) {
        alert('Error al iniciar sesión, intente nuevamente')
        return false
      }
    },
    logout() {
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
    },
    async getCurrentUser() {
      try {
        const response = await api.get('api/user/')
        this.user = response.data
      } catch (e) {
        alert('Error al obtener el usuario')
        return false
      }
    }
  }
})