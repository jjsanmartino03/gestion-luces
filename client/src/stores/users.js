import { defineStore } from 'pinia'
import api from '../services/api'

export const useUsersStore = defineStore('users', {
  state: () => ({
    users: [],
    loading: false
  }),
  actions: {
    async getUsers() {
      this.loading = true
      try {
        const response = await api.get('api/usuarios/')
        this.users = response.data
      } catch (e) {
        alert('Error al obtener los usuarios')
      } finally {
        this.loading = false
      }
    }
  }
})