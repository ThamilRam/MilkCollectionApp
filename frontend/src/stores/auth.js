import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('milk_token') || null,
    user: null
  }),
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('milk_token', token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    },
    clearAuth() {
      this.token = null
      this.user = null
      localStorage.removeItem('milk_token')
      delete axios.defaults.headers.common['Authorization']
    },
    async login(email, password) {
      const params = new URLSearchParams()
      params.append('username', email)
      params.append('password', password)
      const { data } = await axios.post(`${API_URL}/auth/login`, params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      this.setToken(data.access_token)
      await this.fetchMe()
    },
    async fetchMe() {
      const { data } = await axios.get(`${API_URL}/auth/me`)
      this.user = data
    },
    logout() {
      this.clearAuth()
    },
    init() {
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        this.fetchMe().catch(() => this.clearAuth())
      }
    }
  }
})