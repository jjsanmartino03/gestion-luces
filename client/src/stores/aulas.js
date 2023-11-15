import { defineStore } from 'pinia'
import api from '../services/api'

export const useAulasStore = defineStore('aulas', {
  state: () => ({
    aulas: [],
    loading: false
  }),
  actions: {
    async getAulas() {
      this.loading = true
      try {
        const response = await api.get('api/aulas/')
        this.aulas = response.data
      } catch (e) {
        alert('Error al obtener las aulas')
      } finally {
        this.loading = false
      }
    },
    async createAula(aulaData) {
      this.loading = true
      try {
        const response = await api.post('api/aulas/', aulaData)
        this.aulas.push(response.data)

        return true
      } catch (e) {
        alert('Error al crear el aula')
        return false
      } finally {
        this.loading = false
      }
    },
    async editAula(id, aulaData) {
      this.loading = true
      try {
        const response = await api.put(`api/aulas/${id}/`, aulaData)

        const index = this.aulas.findIndex(user => user.id === id)
        this.aulas[index] = response.data

        return true
      } catch (e) {
        alert('Error al actualizar el aula')
        return false
      } finally {
        this.loading = false
      }
    },
    async getAula(id) {
      this.loading = true
      try {
        const response = await api.get(`api/aulas/${id}/`)
        return response.data
      } catch (e) {
        alert('Error al obtener el aula')
      } finally {
        this.loading = false
      }
    },
    async deleteAula(id) {
      this.loading = true
      try {
        const response = await api.delete(`api/aulas/${id}/`)
        this.aulas = this.aulas.filter(aula => aula.id !== id)

        return true;
      } catch (e) {
        alert('Error al eliminar el aula')
      } finally {
        this.loading = false
      }
    }
  }
})