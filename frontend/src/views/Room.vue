<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRoomStore } from '@/stores/room'
import { useToast } from '@/composables/useToast'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Badge from '@/components/ui/Badge.vue'
import Avatar from '@/components/ui/Avatar.vue'
import AvatarImage from '@/components/ui/AvatarImage.vue'
import AvatarFallback from '@/components/ui/AvatarFallback.vue'
import ScrollArea from '@/components/ui/ScrollArea.vue'
import { Crown, Send, LogOut, Users, Copy, Loader2, Home } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const roomStore = useRoomStore()
const { toast } = useToast()

const messageInput = ref('')
const messagesEndRef = ref(null)
const isInitialLoad = ref(true)

const scrollToBottom = () => {
  nextTick(() => {
    messagesEndRef.value?.scrollIntoView({ behavior: 'smooth' })
  })
}

watch(
  () => roomStore.messages,
  () => {
    scrollToBottom()
  },
  { deep: true }
)

onMounted(() => {
  isInitialLoad.value = false
})

// Redirect logic
watch(
  () => [roomStore.activeRoom, roomStore.isReconnecting],
  ([activeRoom, isReconnecting]) => {
    if (isInitialLoad.value) return
    if (isReconnecting) return

    const hasSavedRoom = localStorage.getItem('activeRoom')
    if (!activeRoom && !hasSavedRoom) {
      router.push('/dashboard')
    }
  }
)

const isLeader = () => {
  return roomStore.activeRoom?.leaderId === authStore.user?.id
}

const handleSendMessage = () => {
  if (!messageInput.value.trim()) return
  roomStore.sendMessage(messageInput.value)
  messageInput.value = ''
}

const handleEndSession = async () => {
  await roomStore.endSession()
  toast({
    title: 'Sesi selesai',
    description: 'Room telah ditutup oleh leader.'
  })
  router.push('/dashboard')
}

const handleLeaveRoom = async () => {
  await roomStore.leaveRoom()
  toast({
    title: 'Keluar dari room',
    description: 'Anda telah meninggalkan tim.'
  })
  router.push('/dashboard')
}

const handleBackToDashboard = () => {
  roomStore.clearAutoNavigate()
  toast({
    title: 'Kembali ke Dashboard',
    description: 'Anda tetap terhubung di room ini.'
  })
  router.push('/dashboard')
}

const handleCopyRoomId = () => {
  navigator.clipboard.writeText(roomStore.activeRoom?.id || '')
  toast({
    title: 'Disalin',
    description: 'ID Room disalin ke clipboard.'
  })
}
</script>

<template>
  <!-- Loading: Reconnecting -->
  <div v-if="roomStore.isReconnecting" class="h-screen flex flex-col items-center justify-center bg-gradient-to-br from-cyan-50 via-white to-teal-50">
    <div class="w-20 h-20 bg-gradient-to-br from-cyan-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg mb-6">
      <Loader2 class="h-10 w-10 text-white animate-spin" />
    </div>
    <h2 class="text-xl font-bold bg-gradient-to-r from-cyan-600 to-teal-500 bg-clip-text text-transparent mb-2">
      Menghubungkan...
    </h2>
    <p class="text-slate-400 text-sm">
      Menghubungkan kembali ke room
    </p>
  </div>

  <!-- Loading: Has saved room but not loaded yet -->
  <div v-else-if="!roomStore.activeRoom && localStorage.getItem('activeRoom')" class="h-screen flex flex-col items-center justify-center bg-gradient-to-br from-cyan-50 via-white to-teal-50">
    <div class="w-20 h-20 bg-gradient-to-br from-cyan-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg mb-6">
      <Loader2 class="h-10 w-10 text-white animate-spin" />
    </div>
    <h2 class="text-xl font-bold bg-gradient-to-r from-cyan-600 to-teal-500 bg-clip-text text-transparent mb-2">
      Memuat Room
    </h2>
    <p class="text-slate-400 text-sm">Mohon tunggu sebentar...</p>
  </div>

  <!-- No active room -->
  <div v-else-if="!roomStore.activeRoom"></div>

  <!-- Room Content -->
  <div v-else class="h-screen flex flex-col bg-gradient-to-br from-slate-50 via-white to-cyan-50">
    <!-- Header -->
    <div class="bg-white/80 backdrop-blur-md border-b border-slate-100 px-4 py-3">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 bg-gradient-to-br from-cyan-500 to-teal-500 rounded-lg flex items-center justify-center">
              <Users class="h-4 w-4 text-white" />
            </div>
            <span class="font-bold bg-gradient-to-r from-cyan-600 to-teal-500 bg-clip-text text-transparent hidden sm:inline">GroupMatch</span>
          </div>
          <div class="h-6 w-px bg-slate-200 hidden sm:block"></div>
          <div class="flex items-center gap-2 bg-slate-100 px-3 py-1.5 rounded-lg">
            <span class="text-xs text-slate-500">Room:</span>
            <code class="text-sm font-mono font-medium text-slate-700">
              {{ roomStore.activeRoom?.id ? String(roomStore.activeRoom.id).slice(-8) : '...' }}
            </code>
            <Button size="icon" variant="ghost" class="h-6 w-6" @click="handleCopyRoomId">
              <Copy class="h-3 w-3" />
            </Button>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <Badge class="bg-gradient-to-r from-cyan-500 to-teal-500 text-white border-0 shadow-sm">
            <Users class="h-3 w-3 mr-1" />
            {{ roomStore.activeRoom?.members?.length || 0 }} Anggota
          </Badge>
        </div>
      </div>
    </div>

    <!-- Navbar -->
    <div class="bg-white border-b border-slate-100 px-4 py-3">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <h1 class="text-lg font-bold text-slate-800 flex items-center gap-2">
          <Crown class="h-5 w-5 text-amber-500" />
          Team Workspace
        </h1>
        <div class="flex gap-2">
          <Button variant="ghost" size="sm" @click="handleBackToDashboard" class="text-slate-600 hover:text-slate-800">
            <Home class="mr-2 h-4 w-4" /> Dashboard
          </Button>
          <Button v-if="isLeader()" variant="destructive" size="sm" @click="handleEndSession" class="shadow-sm">
            <Crown class="mr-2 h-4 w-4" /> End Session
          </Button>
          <Button variant="outline" size="sm" @click="handleLeaveRoom" class="border-slate-200">
            <LogOut class="mr-2 h-4 w-4" /> Keluar
          </Button>
        </div>
      </div>
    </div>

    <div class="flex-1 flex max-w-7xl mx-auto w-full p-4 gap-4 overflow-hidden">
      <!-- Sidebar - Members -->
      <div class="w-72 hidden md:flex bg-white/80 backdrop-blur-sm rounded-2xl border border-slate-100 shadow-lg flex-col overflow-hidden">
        <div class="p-4 border-b border-slate-100 bg-gradient-to-r from-cyan-50 to-teal-50">
          <h3 class="font-semibold text-slate-700 flex items-center gap-2">
            <Users class="h-4 w-4 text-cyan-600" /> Anggota Tim ({{ roomStore.activeRoom?.members?.length || 0 }})
          </h3>
        </div>
        <div class="flex-1 p-3 space-y-2 overflow-y-auto">
          <div v-if="!roomStore.activeRoom?.members || roomStore.activeRoom.members.length === 0" class="text-center py-4">
            <p class="text-sm text-slate-400">Memuat anggota...</p>
          </div>
          <div
            v-for="m in roomStore.activeRoom?.members || []"
            :key="m.id"
            :class="[
              'flex gap-3 p-3 rounded-xl transition-all',
              m.id === authStore.user?.id
                ? 'bg-gradient-to-r from-cyan-50 to-teal-50 border border-cyan-100'
                : 'hover:bg-slate-50'
            ]"
          >
            <Avatar class="h-10 w-10 ring-2 ring-white shadow-sm">
              <AvatarImage :src="m.avatar || ''" />
              <AvatarFallback class="bg-gradient-to-br from-cyan-500 to-teal-500 text-white text-sm">
                {{ m.name?.[0] || 'U' }}
              </AvatarFallback>
            </Avatar>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-slate-700 truncate flex items-center gap-1">
                <template v-if="m.id === authStore.user?.id">
                  <span class="text-cyan-600">(Kamu)</span>
                </template>
                <template v-else>
                  {{ m.name || m.username || `User ${String(m.id).slice(-4)}` }}
                </template>
                <Crown v-if="m.id === roomStore.activeRoom?.leaderId" class="h-3.5 w-3.5 text-amber-500" />
              </p>
              <p class="text-xs text-slate-500 truncate">
                {{ m.role || 'Member' }}<template v-if="m.username"> • @{{ m.username }}</template>
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Chat Area -->
      <div class="flex-1 bg-white/80 backdrop-blur-sm rounded-2xl border border-slate-100 shadow-lg flex flex-col overflow-hidden">
        <div class="p-4 border-b border-slate-100 bg-gradient-to-r from-slate-50 to-white">
          <h3 class="font-semibold text-slate-700 flex items-center gap-2">
            <Send class="h-4 w-4 text-cyan-600" /> Chat Room
          </h3>
        </div>

        <ScrollArea class="flex-1 p-4">
          <div class="space-y-4">
            <div v-if="roomStore.messages.length === 0" class="text-center py-12">
              <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Send class="h-8 w-8 text-slate-300" />
              </div>
              <p class="text-slate-400 text-sm">Belum ada pesan</p>
              <p class="text-slate-300 text-xs mt-1">Mulai percakapan dengan timmu!</p>
            </div>
            <div
              v-for="msg in roomStore.messages"
              :key="msg.id"
              :class="['flex gap-3', msg.userId === authStore.user?.id ? 'flex-row-reverse' : '']"
            >
              <Avatar class="h-8 w-8 ring-2 ring-white shadow-sm flex-shrink-0">
                <AvatarFallback :class="[
                  'text-xs',
                  msg.userId === authStore.user?.id
                    ? 'bg-gradient-to-br from-cyan-500 to-teal-500 text-white'
                    : 'bg-slate-200'
                ]">
                  {{ msg.username?.[0] || 'U' }}
                </AvatarFallback>
              </Avatar>
              <div :class="['max-w-[70%]', msg.userId === authStore.user?.id ? 'text-right' : '']">
                <p class="text-xs text-slate-400 mb-1 px-1">
                  {{ msg.userId === authStore.user?.id ? 'Kamu' : msg.username }}
                </p>
                <div :class="[
                  'px-4 py-2.5 rounded-2xl text-sm shadow-sm',
                  msg.userId === authStore.user?.id
                    ? 'bg-gradient-to-r from-cyan-500 to-teal-500 text-white rounded-br-md'
                    : 'bg-slate-100 text-slate-700 rounded-bl-md'
                ]">
                  {{ msg.text }}
                </div>
              </div>
            </div>
            <div ref="messagesEndRef" />
          </div>
        </ScrollArea>

        <form @submit.prevent="handleSendMessage" class="p-4 border-t border-slate-100 bg-slate-50/80 flex gap-3">
          <Input
            v-model="messageInput"
            placeholder="Ketik pesan..."
            class="flex-1 h-11 bg-white border-slate-200 focus:border-cyan-300 rounded-xl"
          />
          <Button
            type="submit"
            :disabled="!messageInput.trim()"
            class="h-11 px-5 bg-gradient-to-r from-cyan-600 to-teal-500 hover:from-cyan-700 hover:to-teal-600 rounded-xl shadow-md"
          >
            <Send class="h-4 w-4" />
          </Button>
        </form>
      </div>
    </div>
  </div>
</template>
