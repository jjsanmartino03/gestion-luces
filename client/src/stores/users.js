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
    },
    async toggleUser(id, newStatus) {
      this.loading = true
      try {
        const response = await api.patch(`api/usuarios/${id}/`, { is_active: newStatus })

        const index = this.users.findIndex(user => user.id === id)
        this.users[index] = response.data
      } catch (e) {
        alert('Error al actualizar el usuario')
      } finally {
        this.loading = false
      }
    },
    async createUser(userData) {
      this.loading = true
      try {
        const response = await api.post('api/usuarios/', userData)
        this.users.push(response.data)

        return true
      } catch (e) {
        alert('Error al crear el usuario')
        return false
      } finally {
        this.loading = false
      }
    },
    async editUser(id, userData) {
      this.loading = true
      try {
        const response = await api.put(`api/usuarios/${id}/`, userData)

        const index = this.users.findIndex(user => user.id === id)
        this.users[index] = response.data

        return true
      } catch (e) {
        alert('Error al actualizar el usuario')
        return false
      } finally {
        this.loading = false
      }
    },
    async getUser(id) {
      this.loading = true
      try {
        const response = await api.get(`api/usuarios/${id}/`)
        return response.data
      } catch (e) {
        alert('Error al obtener el usuario')
      } finally {
        this.loading = false
      }
    }
  }
})