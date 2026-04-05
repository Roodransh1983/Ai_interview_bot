import { create } from 'zustand'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const useAuthStore = create((set, get) => ({
  user: null,
  token: localStorage.getItem('token'),
  isLoading: false,
  error: null,

  setUser: (user) => set({ user }),
  setToken: (token) => {
    if (token) localStorage.setItem('token', token)
    else localStorage.removeItem('token')
    set({ token })
  },

  login: async (email, password) => {
    set({ isLoading: true, error: null })
    try {
      const res = await axios.post(`${API_URL}/auth/login`, { email, password })
      const { access_token, user } = res.data
      get().setToken(access_token)
      set({ user })
      return true
    } catch (err) {
      set({ error: err.response?.data?.detail || 'Login failed' })
      return false
    } finally {
      set({ isLoading: false })
    }
  },

  register: async (name, email, password) => {
    set({ isLoading: true, error: null })
    try {
      const res = await axios.post(`${API_URL}/auth/register`, { name, email, password })
      const { access_token, user } = res.data
      get().setToken(access_token)
      set({ user })
      return true
    } catch (err) {
      set({ error: err.response?.data?.detail || 'Registration failed' })
      return false
    } finally {
      set({ isLoading: false })
    }
  },

  fetchMe: async () => {
    const token = get().token
    if (!token) return
    try {
      const res = await axios.get(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      set({ user: res.data })
    } catch {
      get().logout()
    }
  },

  logout: () => {
    localStorage.removeItem('token')
    set({ user: null, token: null })
  },
}))
