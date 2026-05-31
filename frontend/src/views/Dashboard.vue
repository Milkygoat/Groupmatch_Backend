<script setup>
import { watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRoomStore } from '@/stores/room'
import { useToast } from '@/composables/useToast'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Badge from '@/components/ui/Badge.vue'
import Avatar from '@/components/ui/Avatar.vue'
import AvatarImage from '@/components/ui/AvatarImage.vue'
import AvatarFallback from '@/components/ui/AvatarFallback.vue'
import DropdownMenu from '@/components/ui/DropdownMenu.vue'
import DropdownMenuContent from '@/components/ui/DropdownMenuContent.vue'
import DropdownMenuItem from '@/components/ui/DropdownMenuItem.vue'
import DropdownMenuLabel from '@/components/ui/DropdownMenuLabel.vue'
import DropdownMenuSeparator from '@/components/ui/DropdownMenuSeparator.vue'
import {
  Tag,
  Users,
  LogOut,
  Loader2,
  Zap,
  Settings,
  UserCircle,
  ArrowRight,
  CheckCircle,
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const roomStore = useRoomStore()
const { toast } = useToast()

onMounted(() => {
  roomStore.initRoom()
})

// Auto navigate ke room
watch(
  () => [roomStore.activeRoom, roomStore.matchmakingStatus, roomStore.isNewMatch],
  ([activeRoom, matchmakingStatus, isNewMatch]) => {
    if (activeRoom && matchmakingStatus === 'matched' && isNewMatch) {
      setTimeout(() => router.push('/room'), 1200)
    }
  }
)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const navigateTo = (path) => {
  router.push(path)
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-cyan-50">
    <!-- HEADER -->
    <div class="bg-white/80 backdrop-blur-md border-b border-slate-100 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <router-link to="/dashboard" class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-cyan-500 to-teal-500 rounded-xl flex items-center justify-center shadow-md">
            <Users class="h-5 w-5 text-white" />
          </div>
          <h1 class="text-2xl font-bold bg-gradient-to-r from-cyan-600 to-teal-500 bg-clip-text text-transparent">GroupMatch</h1>
        </router-link>

        <DropdownMenu v-slot="{ isOpen, toggle, close }">
          <Button variant="ghost" class="flex gap-3 hover:bg-slate-100/80" @click="toggle">
            <Avatar class="ring-2 ring-cyan-100">
              <AvatarImage :src="authStore.user?.avatar" />
              <AvatarFallback class="bg-gradient-to-br from-cyan-500 to-teal-500 text-white">{{ authStore.user?.name?.[0] }}</AvatarFallback>
            </Avatar>
            <div class="hidden sm:block text-left">
              <p class="text-sm font-semibold text-slate-700">{{ authStore.user?.name }}</p>
              <p class="text-xs text-slate-500">@{{ authStore.user?.username }}</p>
            </div>
          </Button>

          <DropdownMenuContent v-if="isOpen" align="end" class="w-56">
            <DropdownMenuLabel class="font-normal">
              <div class="flex flex-col space-y-1">
                <p class="text-sm font-medium">{{ authStore.user?.name }}</p>
                <p class="text-xs text-slate-500">{{ authStore.user?.email }}</p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="navigateTo('/profile-setup'); close()" class="cursor-pointer">
              <UserCircle class="mr-2 h-4 w-4" /> Edit Profil
            </DropdownMenuItem>
            <DropdownMenuItem @click="toast({ title: 'Coming soon' }); close()" class="cursor-pointer">
              <Settings class="mr-2 h-4 w-4" /> Pengaturan
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="handleLogout(); close()" class="text-red-600 cursor-pointer focus:text-red-600">
              <LogOut class="mr-2 h-4 w-4" /> Keluar
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>

    <!-- CONTENT -->
    <div class="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- PROFILE -->
      <Card class="lg:sticky lg:top-24 border-0 shadow-lg bg-white/80 backdrop-blur-sm overflow-hidden">
        <div class="h-20 bg-gradient-to-r from-cyan-500 to-teal-500"></div>
        <CardContent class="pt-0 text-center relative">
          <Avatar class="mx-auto h-24 w-24 -mt-12 ring-4 ring-white shadow-lg">
            <AvatarImage :src="authStore.user?.avatar" />
            <AvatarFallback class="text-2xl bg-gradient-to-br from-cyan-500 to-teal-500 text-white">{{ authStore.user?.name?.[0] }}</AvatarFallback>
          </Avatar>
          <h3 class="text-xl font-bold mt-4 text-slate-800">{{ authStore.user?.name }}</h3>
          <p class="text-sm text-slate-500">@{{ authStore.user?.username }}</p>

          <Badge class="mt-3 bg-gradient-to-r from-cyan-500 to-teal-500 text-white border-0">
            {{ authStore.user?.role || 'Member' }}
          </Badge>

          <div class="mt-6 pt-6 border-t border-slate-100">
            <p class="text-xs uppercase text-slate-400 mb-3 flex items-center justify-center gap-1 font-medium">
              <Tag class="h-3 w-3" /> Skills
            </p>
            <div class="flex flex-wrap justify-center gap-2">
              <template v-if="authStore.user?.skills?.length">
                <Badge
                  v-for="(skill, index) in authStore.user.skills"
                  :key="index"
                  variant="outline"
                  class="bg-slate-50 border-slate-200"
                >
                  {{ skill }}
                </Badge>
              </template>
              <span v-else class="text-xs text-slate-400 italic">Belum ada skill ditambahkan</span>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- MATCHMAKING & HISTORY -->
      <div class="lg:col-span-2 space-y-6">
        <!-- MATCHMAKING CARD -->
        <Card class="border-0 shadow-lg bg-white/80 backdrop-blur-sm overflow-hidden relative">
          <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-cyan-500 to-teal-500"></div>
          <CardHeader class="text-center pb-4">
            <div class="mx-auto w-16 h-16 bg-gradient-to-br from-cyan-100 to-teal-100 rounded-2xl flex items-center justify-center mb-4">
              <Zap class="h-8 w-8 text-cyan-600" />
            </div>
            <CardTitle class="text-2xl text-slate-800">
              {{ roomStore.activeRoom ? '🎉 Tim Aktif!' : 'Siap Cari Tim?' }}
            </CardTitle>
            <CardDescription class="text-slate-500">
              {{ roomStore.activeRoom
                ? 'Kamu sudah punya tim aktif. Kembali ke room untuk melanjutkan.'
                : 'Temukan rekan tim terbaik dengan satu klik' }}
            </CardDescription>
          </CardHeader>
          <CardContent class="flex flex-col items-center pb-8">
            <template v-if="roomStore.activeRoom">
              <Button
                size="lg"
                @click="navigateTo('/room')"
                class="h-14 px-8 bg-gradient-to-r from-cyan-600 to-teal-500 hover:from-cyan-700 hover:to-teal-600 shadow-lg hover:shadow-xl transition-all"
              >
                Kembali ke Room <ArrowRight class="ml-2 h-5 w-5" />
              </Button>
            </template>
            <template v-else-if="roomStore.matchmakingStatus === 'searching'">
              <div class="text-center space-y-4">
                <div class="w-20 h-20 rounded-full border-4 border-cyan-100 flex items-center justify-center mx-auto">
                  <Loader2 class="h-10 w-10 animate-spin text-cyan-600" />
                </div>
                <p class="text-slate-600 font-medium">Mencari tim untukmu...</p>
                <Button variant="outline" @click="roomStore.leaveRoom" class="mt-2">
                  Batalkan Pencarian
                </Button>
              </div>
            </template>
            <template v-else-if="roomStore.matchmakingStatus === 'matched'">
              <div class="text-center space-y-4">
                <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center">
                  <CheckCircle class="h-10 w-10 text-green-600" />
                </div>
                <p class="text-green-600 font-medium">Tim ditemukan!</p>
              </div>
            </template>
            <template v-else>
              <Button
                size="lg"
                @click="roomStore.startMatchmaking"
                class="h-14 px-8 bg-gradient-to-r from-cyan-600 to-teal-500 hover:from-cyan-700 hover:to-teal-600 shadow-lg hover:shadow-xl transition-all"
              >
                <Zap class="mr-2 h-5 w-5" /> Cari Tim Sekarang
              </Button>
            </template>
          </CardContent>
        </Card>

        <!-- HISTORY -->
        <Card class="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
          <CardHeader class="pb-4">
            <CardTitle class="flex gap-2 items-center text-slate-800">
              <div class="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center">
                <Users class="h-4 w-4 text-slate-600" />
              </div>
              Riwayat Tim
            </CardTitle>
          </CardHeader>
          <CardContent>
            <template v-if="roomStore.roomHistory.length === 0">
              <div class="text-center py-8">
                <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users class="h-8 w-8 text-slate-300" />
                </div>
                <p class="text-sm text-slate-400">
                  Belum ada riwayat tim
                </p>
                <p class="text-xs text-slate-300 mt-1">
                  Riwayat akan muncul setelah kamu bergabung dengan tim
                </p>
              </div>
            </template>
            <template v-else>
              <div class="space-y-3">
                <div
                  v-for="(r, index) in roomStore.roomHistory"
                  :key="r.id"
                  class="p-4 bg-slate-50 hover:bg-slate-100 rounded-xl border border-slate-100 transition-colors"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 bg-gradient-to-br from-cyan-100 to-teal-100 rounded-lg flex items-center justify-center">
                        <Users class="h-5 w-5 text-cyan-600" />
                      </div>
                      <div>
                        <p class="font-medium text-slate-700">Room #{{ r.room_id ? String(r.room_id).slice(-6) : index + 1 }}</p>
                        <p class="text-xs text-slate-500">{{ r.action }}</p>
                      </div>
                    </div>
                    <Badge variant="outline" class="text-xs">Selesai</Badge>
                  </div>
                </div>
              </div>
            </template>
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>
