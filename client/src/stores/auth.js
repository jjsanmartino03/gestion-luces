import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user: null
  }),
  actions: {
    login: (username, password) => {
      const response = api.post('api-token-auth/', { username, password });

      console.dir(response);
    }
  }
})