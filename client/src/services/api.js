import axios from 'axios'

class ApiClient {
  constructor() {
    this.apiClient = axios.create({
      baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/',
      withCredentials: true
    })
  }

  async get(url) {
    return await this.apiClient.get(url)
  }

  async post(url, data) {
    return await this.apiClient.post(url, data)
  }
}

export default new ApiClient()