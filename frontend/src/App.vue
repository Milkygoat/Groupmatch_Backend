<script setup>
import { onMounted, computed } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { MOCK_MODE } from '@/services/api'
import Toaster from '@/components/ui/Toaster.vue'
import { Loader2, Users } from 'lucide-vue-next'

const authStore = useAuthStore()

onMounted(() => {
  authStore.initAuth()
})

const isLoading = computed(() => authStore.loading)
</script>

<template>
  <!-- Loading Screen -->
  <div
    v-if="isLoading"
    class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-cyan-50 via-white to-teal-50"
  >
    <div class="w-16 h-16 bg-gradient-to-br from-cyan-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg mb-4 animate-pulse">
      <Users class="h-8 w-8 text-white" />
    </div>
    <h2 class="text-xl font-bold bg-gradient-to-r from-cyan-600 to-teal-500 bg-clip-text text-transparent">GroupMatch</h2>
    <p class="text-slate-400 text-sm mt-2">Memuat...</p>
  </div>

  <!-- Main App -->
  <template v-else>
    <RouterView />

    <!-- Mock Mode Banner -->
    <div
      v-if="MOCK_MODE"
      class="fixed bottom-4 left-4 z-50 bg-gradient-to-r from-amber-500 to-orange-500 text-white px-4 py-2.5 rounded-xl shadow-lg text-sm font-medium flex items-center gap-2 backdrop-blur-sm"
    >
      <div class="w-2 h-2 bg-white rounded-full animate-pulse"></div>
      <span>Mock Mode - UI Preview</span>
    </div>
  </template>

  <!-- Toast Notifications -->
  <Toaster />
</template>
