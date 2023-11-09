import { defineStore } from 'pinia'
import api from '../services/api'

export const useHomeStore = defineStore('home', {
  state: () => ({
    aulas: [],
    loading: false
  }),
  actions: {
    async getAulas() {
      this.loading = true
      try {
        const response = await api.get('api/aulas/')
        this.aulas = response.data.map(a => {
          return {
            nombre: `Aula ${a.numero}`,
            estado: a.id % 2 ? 0 : 1,
            from: `Hace ${a.numero % 5}:00 hs.`
          }
        })
      } catch (e) {
        alert('Error al obtener las aulas')
      } finally {
        this.loading = false
      }
    }
  }
})