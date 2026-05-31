<script setup>
import { useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { Users, ArrowRight, Target, MessageSquare, Shield, Zap, CheckCircle, Star } from 'lucide-vue-next'

const router = useRouter()

const features = [
  {
    icon: Target,
    title: 'Smart Matching',
    description: 'Algoritma cerdas yang mencocokkan Anda dengan rekan tim berdasarkan skill dan preferensi.',
  },
  {
    icon: MessageSquare,
    title: 'Real-time Chat',
    description: 'Komunikasi langsung dengan anggota tim melalui fitur chat real-time yang responsif.',
  },
  {
    icon: Shield,
    title: 'Aman & Terpercaya',
    description: 'Keamanan data terjamin dengan sistem autentikasi dan enkripsi modern.',
  },
]

const benefits = [
  'Temukan rekan tim dengan skill yang saling melengkapi',
  'Proses matchmaking otomatis dan cepat',
  'Chat real-time untuk koordinasi tim',
  'Riwayat tim tersimpan dengan rapi',
]

const navigateTo = (path) => {
  router.push(path)
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-cyan-50">
    <!-- Decorative Elements -->
    <div class="fixed top-20 left-10 text-cyan-200 opacity-50">
      <Users class="h-20 w-20" />
    </div>
    <div class="fixed top-32 right-10 text-teal-200 opacity-50">
      <Zap class="h-16 w-16" />
    </div>

    <!-- Header/Navbar -->
    <header class="bg-white/80 backdrop-blur-md border-b border-slate-100 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-cyan-500 to-teal-500 rounded-xl flex items-center justify-center shadow-md">
            <Users class="h-5 w-5 text-white" />
          </div>
          <h1 class="text-2xl font-bold bg-gradient-to-r from-cyan-600 to-teal-500 bg-clip-text text-transparent">
            GroupMatch
          </h1>
        </div>

        <div class="flex items-center gap-3">
          <Button
            variant="ghost"
            @click="navigateTo('/login')"
            class="text-slate-600 hover:text-slate-800"
          >
            Masuk
          </Button>
          <Button
            @click="navigateTo('/register')"
            class="bg-gradient-to-r from-cyan-600 to-teal-500 hover:from-cyan-700 hover:to-teal-600 text-white shadow-md"
          >
            Daftar Gratis
          </Button>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="max-w-7xl mx-auto px-6 py-20 text-center relative">
      <div class="inline-flex items-center gap-2 bg-gradient-to-r from-cyan-100 to-teal-100 text-cyan-700 px-4 py-2 rounded-full text-sm font-medium mb-6">
        <Zap class="h-4 w-4" />
        Smart Team Matching
      </div>

      <h2 class="text-5xl md:text-6xl font-bold text-slate-800 mb-4">
        Temukan Tim
      </h2>
      <h2 class="text-5xl md:text-6xl font-bold bg-gradient-to-r from-cyan-600 to-teal-500 bg-clip-text text-transparent mb-6">
        Impian Anda
      </h2>

      <p class="text-lg text-slate-600 max-w-2xl mx-auto mb-10">
        Platform matchmaking tim berbasis skill yang membantu Anda menemukan rekan kerja yang sempurna untuk proyek Anda.
      </p>

      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <Button
          size="lg"
          @click="navigateTo('/register')"
          class="h-14 px-8 bg-gradient-to-r from-cyan-600 to-teal-500 hover:from-cyan-700 hover:to-teal-600 shadow-lg hover:shadow-xl transition-all text-lg"
        >
          Mulai Sekarang
        </Button>
        <Button
          size="lg"
          variant="outline"
          @click="navigateTo('/login')"
          class="h-14 px-8 border-2 text-lg"
        >
          Sudah Punya Akun
        </Button>
      </div>
    </section>

    <!-- Features Section -->
    <section class="max-w-7xl mx-auto px-6 py-16">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card
          v-for="(feature, index) in features"
          :key="index"
          class="border border-slate-100 shadow-lg bg-white/80 backdrop-blur-sm hover:shadow-xl transition-shadow"
        >
          <CardContent class="p-6">
            <div class="w-12 h-12 bg-gradient-to-br from-cyan-100 to-teal-100 rounded-xl flex items-center justify-center mb-4">
              <component :is="feature.icon" class="h-6 w-6 text-cyan-600" />
            </div>
            <h3 class="text-xl font-bold text-slate-800 mb-2">{{ feature.title }}</h3>
            <p class="text-slate-600">{{ feature.description }}</p>
          </CardContent>
        </Card>
      </div>
    </section>

    <!-- Benefits Section -->
    <section class="max-w-7xl mx-auto px-6 py-16">
      <div class="rounded-3xl p-8 md:p-12 text-white shadow-xl" style="background: linear-gradient(120deg, rgba(15, 23, 42, 88%) 16%, rgba(19, 184, 167, 100%) 100%);">
        <div class="grid md:grid-cols-2 gap-8 items-center">
          <div>
            <h3 class="text-3xl md:text-4xl font-bold mb-4" style="color: #CEFBF8;">
              Mengapa Memilih GroupMatch?
            </h3>
            <p class="text-cyan-100 mb-6" style="color: #CEFBF8;">
              GroupMatch memudahkan Anda menemukan rekan tim yang tepat dengan teknologi matchmaking berbasis skill.
            </p>
            <ul class="space-y-3" style="color: #CEFBF8;">
              <li v-for="(benefit, index) in benefits" :key="index" class="flex items-center gap-3">
                <CheckCircle class="h-5 w-5 text-cyan-200" />
                <span>{{ benefit }}</span>
              </li>
            </ul>
          </div>
          <div class="flex justify-center">
            <div class="w-48 h-48 rounded-3xl flex items-center justify-center" style="background: linear-gradient(-40deg, rgba(15, 23, 42, 70%) 18%, rgba(19, 184, 167, 80%) 100%);">
              <Star class="h-24 w-24 text-white/80" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-slate-900 text-white py-12">
      <div class="max-w-7xl mx-auto px-6 text-center">
        <div class="flex items-center justify-center gap-3 mb-4">
          <div class="w-10 h-10 bg-gradient-to-br from-cyan-500 to-teal-500 rounded-xl flex items-center justify-center">
            <Users class="h-5 w-5 text-white" />
          </div>
          <span class="text-xl font-bold">GroupMatch</span>
        </div>
        <p class="text-slate-400 text-sm">
          © 2025 GroupMatch. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>
