import axios from 'axios'

class ApiClient {
  constructor() {
    this.apiClient = axios.create({
      baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/',
      withCredentials: true
    })
  }

  async get(url) {
    return await this.request('get', url)
  }

  async post(url, data) {
    return await this.request('post', url, data)
  }

  async put(url, data) {
    return await this.request('put', url, data)
  }

  async patch(url, data) {
    return await this.request('patch', url, data)
  }

  async request(method, url, data) {
    let headers = {}
    const token = localStorage.getItem('token')
    if (token) {
      headers.Authorization = `Token ${token}`
    }

    return await this.apiClient.request({
      method,
      url,
      data,
      headers
    })
  }
}

export default new ApiClient()