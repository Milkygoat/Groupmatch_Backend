import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const loading = ref(true)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const isProfileComplete = computed(() => user.value?.profileComplete ?? false)

  // Actions
  const fetchUserProfile = async () => {
    const token = localStorage.getItem('token')
    console.log('[AUTH] fetchUserProfile called, token:', token ? 'exists' : 'missing')
    if (!token) return false

    try {
      console.log('[AUTH] Calling GET /profile/me...')
      const response = await api.get('/profile/me')
      const profileData = response.data
      console.log('[AUTH] Profile data received:', profileData)

      const formattedUser = {
        id: profileData.user_id,
        name: profileData.name,
        username: profileData.username,
        email: profileData.email,
        role: profileData.role,
        skills: profileData.skill ? profileData.skill.split(',') : [],
        avatar: profileData.pict,
        profileComplete: true
      }

      user.value = formattedUser
      localStorage.setItem('currentUser', JSON.stringify(formattedUser))
      console.log('[AUTH] User set successfully:', formattedUser.name)
      return true
    } catch (error) {
      console.log('[AUTH] fetchUserProfile error:', error.response?.status, error.response?.data)
      
      if (error.response && error.response.status === 404) {
        console.log("[AUTH] User login, but no profile yet.")
        user.value = { profileComplete: false }
        return true
      }

      if (error.response && error.response.status === 401) {
        console.log('[AUTH] Token invalid, removing...')
        localStorage.removeItem('token')
        user.value = null
      }
      return false
    }
  }

  const initAuth = async () => {
    console.log('[AUTH] initAuth() called')
    const token = localStorage.getItem('token')
    console.log('[AUTH] Token on init:', token ? 'exists' : 'missing')
    if (token) {
      await fetchUserProfile()
    }
    loading.value = false
    console.log('[AUTH] initAuth() completed, loading set to false')
  }

  const login = async (email, password) => {
    try {
      console.log('[AUTH] login() called with email:', email)
      const response = await api.post('/auth/login', { email, password })
      const { access_token } = response.data
      console.log('[AUTH] login response, token:', access_token ? 'received' : 'missing')

      localStorage.setItem('token', access_token)
      console.log('[AUTH] Token saved to localStorage')

      await fetchUserProfile()
      console.log('[AUTH] fetchUserProfile completed')

      return { success: true }
    } catch (error) {
      console.error("[AUTH] Login error:", error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Gagal login.'
      }
    }
  }

  const register = async (userData) => {
    try {
      await api.post('/auth/register', {
        email: userData.email,
        password: userData.password,
        confirm_password: userData.password
      })
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Gagal mendaftar.'
      }
    }
  }

  const loginWithGoogle = async () => {
    try {
      const response = await api.get('/auth/google/login')
      const { login_url } = response.data

      if (login_url) {
        window.location.href = login_url
      }
    } catch (error) {
      console.error("Gagal inisialisasi Google Login:", error)
    }
  }

  const uploadAvatar = async (imageFile) => {
    try {
      const formData = new FormData()
      formData.append('file', imageFile)

      const response = await api.post('/profile/upload-avatar', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      return response.data
    } catch (error) {
      console.error("Upload avatar error:", error)
      throw error
    }
  }

  const updateProfile = async (profileData) => {
    try {
      let skillString = ""
      if (Array.isArray(profileData.skills)) {
        skillString = profileData.skills.join(',')
      } else if (typeof profileData.skills === 'string') {
        skillString = profileData.skills
      }

      const payload = {
        username: profileData.username,
        name: profileData.name,
        birthdate: profileData.birthdate,
        role: profileData.role,
        skill: skillString,
        pict: profileData.avatarUrl || ""
      }

      console.log("Sending profile payload:", payload)

      if (user.value?.profileComplete) {
        await api.put('/profile/', payload)
      } else {
        await api.post('/profile/', payload)
        user.value = {
          ...user.value,
          profileComplete: true
        }
      }

      await fetchUserProfile()
      return { success: true }
    } catch (error) {
      console.error("Update profile error:", error)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('currentUser')
    user.value = null
  }

  return {
    // State
    user,
    loading,
    // Getters
    isAuthenticated,
    isProfileComplete,
    // Actions
    initAuth,
    fetchUserProfile,
    login,
    register,
    loginWithGoogle,
    uploadAvatar,
    updateProfile,
    logout
  }
})
