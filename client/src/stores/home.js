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
        const response = await api.get('api/interacciones/')
        this.aulas = response.data.map(a => {
          return {
            nombre: `Aula ${a.aula_numero}`,
            estado: a.estado,
            has_rele: a.has_rele,
            has_fotosensible: a.has_fotosensible,
            from: a.desde,
            id: a.aula_id
          }
        })
      } catch (e) {
        alert('Error al obtener las aulas')
      } finally {
        this.loading = false
      }
    },
    async toggleAula(id) {
      this.loading = true
      try {
        const response = await api.post(`api/interacciones/`, {
          id_aula: id
        })
        this.aulas = this.aulas.map(a => {
          if (a.id === id) {
            return {
              ...a,
              estado: !!response.data.estado
            }
          }
          return a
        })


      } catch (e) {
        alert("Error al cambiar el estado de un aula")
      } finally {
        this.loading = false
      }

    }
  }
})