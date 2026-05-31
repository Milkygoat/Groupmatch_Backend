<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Loader2 } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const processed = ref(false)

onMounted(async () => {
  await handleCallback()
})

const handleCallback = async () => {
  if (processed.value) return

  // Coba ambil token dari query params dengan berbagai kemungkinan nama
  let token = route.query.token || route.query.access_token || route.query.jwt

  // Juga cek dari hash fragment
  if (!token && window.location.hash) {
    const hashParams = new URLSearchParams(window.location.hash.substring(1))
    token = hashParams.get('token') || hashParams.get('access_token') || hashParams.get('jwt')
  }

  console.log('OAuth Callback - URL:', window.location.href)
  console.log('OAuth Callback - Token found:', token ? 'Yes' : 'No')

  if (token) {
    processed.value = true
    localStorage.setItem('token', token)
    console.log('Token saved to localStorage')

    // Panggil fetch untuk memastikan token valid & cek status profil
    const isAuthSuccess = await authStore.fetchUserProfile()
    console.log('Auth success:', isAuthSuccess)

    if (isAuthSuccess) {
      setTimeout(() => {
        const savedUser = localStorage.getItem('currentUser')
        console.log('Saved user:', savedUser)

        if (savedUser) {
          const userData = JSON.parse(savedUser)
          if (userData.profileComplete) {
            console.log('Redirecting to dashboard')
            router.replace('/dashboard')
          } else {
            console.log('Redirecting to profile-setup')
            router.replace('/profile-setup')
          }
        } else {
          console.log('No saved user, redirecting to profile-setup')
          router.replace('/profile-setup')
        }
      }, 200)
    } else {
      console.log('Auth failed, redirecting to login')
      localStorage.removeItem('token')
      router.replace('/login')
    }
  } else {
    console.log('No token found in URL, redirecting to login')
    if (!processed.value) {
      processed.value = true
      router.replace('/login')
    }
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center">
    <Loader2 class="h-8 w-8 animate-spin text-cyan-600" />
    <p class="ml-2 text-slate-600">Sinkronisasi data akun...</p>
  </div>
</template>
