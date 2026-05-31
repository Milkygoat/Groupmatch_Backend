<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardFooter from '@/components/ui/CardFooter.vue'
import { Loader2, LogIn, Users } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const { toast } = useToast()

const formData = ref({
  email: '',
  password: ''
})
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true

  const result = await authStore.login(formData.value.email, formData.value.password)

  if (result.success) {
    console.log('[LOGIN] Login successful, navigating to dashboard...')
    toast({
      title: 'Login Berhasil',
      description: 'Selamat datang kembali!',
    })
    setTimeout(() => {
      router.push('/dashboard')
    }, 100)
  } else {
    console.log('[LOGIN] Login failed:', result.error)
    toast({
      title: 'Login Gagal',
      description: result.error || 'Email atau password salah.',
      variant: 'destructive'
    })
    loading.value = false
  }
}

const handleGoogleLogin = async () => {
  try {
    await authStore.loginWithGoogle()
  } catch (error) {
    console.error('Google login error:', error)
    toast({
      title: 'Error',
      description: 'Gagal memuat login Google.',
      variant: 'destructive'
    })
  }
}

const navigateTo = (path) => {
  router.push(path)
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-cyan-50 via-white to-teal-50 px-4">
    <!-- Background decoration -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-cyan-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-teal-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
    </div>

    <Card class="w-full max-w-md shadow-xl border-0 bg-white/80 backdrop-blur-sm relative z-10">
      <CardHeader class="space-y-1 text-center pb-2">
        <!-- Logo -->
        <div class="mx-auto mb-4">
          <div class="w-16 h-16 bg-gradient-to-br from-cyan-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg">
            <Users class="h-8 w-8 text-white" />
          </div>
        </div>
        <h1 class="text-2xl font-bold bg-gradient-to-r from-cyan-600 to-teal-500 bg-clip-text text-transparent">
          GroupMatch
        </h1>
        <CardTitle class="text-xl font-semibold text-slate-800 pt-2">Selamat Datang!</CardTitle>
        <CardDescription class="text-slate-500">
          Masuk untuk menemukan tim impianmu
        </CardDescription>
      </CardHeader>
      
      <CardContent class="space-y-4 pt-4">
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div class="space-y-2">
            <Label for="email" class="text-slate-700">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="nama@email.com"
              v-model="formData.email"
              required
              class="h-11 bg-slate-50 border-slate-200 focus:bg-white transition-colors"
            />
          </div>
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <Label for="password" class="text-slate-700">Password</Label>
              <a href="#" class="text-xs text-cyan-600 hover:text-cyan-700 hover:underline">
                Lupa password?
              </a>
            </div>
            <Input
              id="password"
              type="password"
              v-model="formData.password"
              required
              class="h-11 bg-slate-50 border-slate-200 focus:bg-white transition-colors"
            />
          </div>
          <Button
            type="submit"
            class="w-full h-11 bg-gradient-to-r from-cyan-600 to-teal-500 hover:from-cyan-700 hover:to-teal-600 shadow-md"
            :disabled="loading"
          >
            <template v-if="loading">
              <Loader2 class="mr-2 h-4 w-4 animate-spin" />
              Memproses...
            </template>
            <template v-else>
              <LogIn class="mr-2 h-4 w-4" /> Masuk
            </template>
          </Button>
        </form>

        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <span class="w-full border-t border-slate-200" />
          </div>
          <div class="relative flex justify-center text-xs uppercase">
            <span class="bg-white px-3 text-slate-400">atau</span>
          </div>
        </div>

        <Button
          variant="outline"
          type="button"
          class="w-full h-11 border-slate-200 hover:bg-slate-50"
          @click="handleGoogleLogin"
        >
          <svg class="mr-2 h-4 w-4" viewBox="0 0 488 512">
            <path fill="currentColor" d="M488 261.8C488 403.3 391.1 504 248 504 110.8 504 0 393.2 0 256S110.8 8 248 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9C258.5 52.6 94.3 116.6 94.3 256c0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9H248v-85.3h236.1c2.3 12.7 3.9 24.9 3.9 41.4z"/>
          </svg>
          Masuk dengan Google
        </Button>
      </CardContent>

      <CardFooter class="flex flex-col space-y-4 pt-2">
        <div class="text-center text-sm text-slate-500">
          Belum punya akun?
          <a
            href="#"
            @click.prevent="navigateTo('/register')"
            class="font-medium text-cyan-600 hover:text-cyan-700 hover:underline"
          >
            Daftar sekarang
          </a>
        </div>
      </CardFooter>
    </Card>
  </div>
</template>
