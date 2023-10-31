import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    isAuthenticated: localStorage.getItem('token') !== null
  }),

  actions: {
    async login(username, password) {

      try {
        const response = await api.post('api-token-auth/', { username, password })

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
    }
  }
})