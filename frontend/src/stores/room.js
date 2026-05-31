import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import api, { SOCKET_URL, getRoomHistory, MockWebSocket, MOCK_MODE } from '@/services/api'
import { useAuthStore } from './auth'
import { useToast } from '@/composables/useToast'

export const useRoomStore = defineStore('room', () => {
  const authStore = useAuthStore()
  const { toast } = useToast()

  // State
  const activeRoom = ref(null)
  const matchmakingStatus = ref('idle')
  const messages = ref([])
  const roomHistory = ref([])
  const isReconnecting = ref(false)
  const isNewMatch = ref(false)

  // Refs (tidak reaktif)
  let socket = null
  let pollingInterval = null
  let hasLeftRoom = false

  // Watch activeRoom untuk sync ke localStorage
  watch(activeRoom, (newRoom) => {
    if (newRoom) {
      localStorage.setItem('activeRoom', JSON.stringify(newRoom))
    } else {
      localStorage.removeItem('activeRoom')
    }
  }, { deep: true })

  // Actions
  const restoreRoom = async () => {
    if (!authStore.user || hasLeftRoom) return

    const saved = localStorage.getItem('activeRoom')
    if (!saved) return

    try {
      isReconnecting.value = true
      isNewMatch.value = false
      const parsed = JSON.parse(saved)

      const res = await api.get(`/rooms/${parsed.id}`)
      if (res.data) {
        if (res.data.status !== 'active') {
          throw new Error('Room sudah ditutup')
        }
        handleMatchFound(parsed.id, res.data, true)
        toast({
          title: 'Terhubung kembali',
          description: 'Kembali ke room sebelumnya',
        })
      }
    } catch {
      localStorage.removeItem('activeRoom')
    } finally {
      isReconnecting.value = false
    }
  }

  const fetchRoomHistory = async () => {
    if (!authStore.user) return
    try {
      const data = await getRoomHistory()
      roomHistory.value = data
    } catch (err) {
      console.error('Fetch room history failed', err)
      roomHistory.value = []
    }
  }

  const initRoom = async () => {
    if (!authStore.user) return
    await restoreRoom()
    await fetchRoomHistory()
  }

  const startMatchmaking = async () => {
    matchmakingStatus.value = 'searching'
    messages.value = []

    try {
      const res = await api.post('/matchmaking/join')

      if (res.data?.room_id) {
        handleMatchFound(res.data.room_id, res.data)
      } else if (res.data?.status === 'waiting') {
        startPolling()
        toast({
          title: 'Menunggu user lain',
          description: res.data.message || 'Menunggu user lain bergabung ke antrian...',
        })
      } else {
        startPolling()
        toast({
          title: 'Mencari tim',
          description: 'Sedang mencarikan tim...',
        })
      }
    } catch (err) {
      matchmakingStatus.value = 'idle'
      toast({
        title: 'Gagal',
        description: err.response?.data?.detail || 'Matchmaking gagal',
        variant: 'destructive',
      })
    }
  }

  const startPolling = () => {
    if (pollingInterval) clearInterval(pollingInterval)

    pollingInterval = setInterval(async () => {
      try {
        const res = await api.get('/matchmaking/status')
        if (res.data?.status === 'matched' && res.data?.room_id) {
          clearInterval(pollingInterval)
          handleMatchFound(res.data.room_id, res.data)
        }
      } catch {}
    }, 2000)
  }

  const handleMatchFound = async (roomId, roomData, isReconnect = false) => {
    console.log('[RoomStore] handleMatchFound called with:', { roomId, roomData, isReconnect })

    matchmakingStatus.value = 'matched'
    isReconnecting.value = false
    isNewMatch.value = !isReconnect

    let detail = roomData
    if (!roomData.members) {
      console.log('[RoomStore] No members in roomData, fetching from API...')
      const res = await api.get(`/rooms/${roomId}`)
      detail = res.data
      console.log('[RoomStore] Fetched room detail:', detail)
    }

    const activeRoomData = {
      id: detail.id || roomId,
      leaderId: detail.leader_id,
      status: detail.status,
      members: (detail.members || []).map((m) => ({
        id: m.user_id || m.id,
        name: m.name || m.username || m.user_name,
        username: m.username || m.user_name || m.name,
        role: m.role,
        avatar:
          m.pict || m.avatar || m.picture ||
          `https://api.dicebear.com/7.x/avataaars/svg?seed=${m.username || m.user_id || m.id}`,
      })),
    }

    console.log('[RoomStore] Setting activeRoom:', activeRoomData)
    activeRoom.value = activeRoomData

    connectWebSocket(roomId || detail.id, isReconnect)
  }

  const connectWebSocket = (roomId, isReconnect) => {
    const token = localStorage.getItem('token')
    if (!token) return

    // TUTUP SOCKET LAMA JIKA ADA agar tidak ada duplikasi pesan
    if (socket) {
      console.log('[RoomStore] Closing existing socket before opening a new one.')
      socket.close()
    }

    const wsUrl = `${SOCKET_URL}/ws/rooms/${roomId}?token=${token}`
    const ws = MOCK_MODE ? new MockWebSocket(wsUrl) : new WebSocket(wsUrl)

    ws.onopen = () => {
      console.log('[RoomStore] WebSocket connected, readyState:', ws.readyState)
      if (!isReconnect) {
        toast({
          title: 'Tim terbentuk',
          description: 'Anda masuk ke workspace',
        })
      }
    }

    ws.onmessage = (e) => {
      console.log('[RoomStore] WebSocket message received:', e.data)
      const payload = JSON.parse(e.data)

      if (payload.type === 'chat') {
        console.log('[RoomStore] Adding chat message:', payload.data)

        const chatUserId = payload.data.user_id
        const chatUsername = payload.data.username
        if (chatUserId && chatUsername && activeRoom.value) {
          activeRoom.value.members = activeRoom.value.members.map((m) => {
            if (String(m.id) === String(chatUserId) && (!m.username || m.username.startsWith('User '))) {
              return { ...m, username: chatUsername, name: chatUsername }
            }
            return m
          })
        }

        messages.value.push({
          id: Date.now(),
          userId: payload.data.user_id,
          username: payload.data.username,
          text: payload.data.text,
        })
      } else if (payload.type === 'users_list' && payload.data && activeRoom.value) {
        activeRoom.value.members = activeRoom.value.members.map((m) => {
          const wsUser = payload.data.find((u) => String(u.user_id) === String(m.id))
          if (wsUser) {
            return {
              ...m,
              username: wsUser.username || m.username,
              name: wsUser.name || wsUser.username || m.name,
              role: wsUser.role || m.role,
              avatar: wsUser.pict || m.avatar,
            }
          }
          return m
        })
      } else if (payload.type === 'room_ended') {
        toast({
          title: 'Sesi Berakhir',
          description: 'Leader telah mengakhiri sesi room ini.',
        })
        socket?.close()
        activeRoom.value = null
        messages.value = []
        matchmakingStatus.value = 'idle'
        isNewMatch.value = false
        localStorage.removeItem('activeRoom')
      }
    }

    ws.onclose = async () => {
      console.log('[RoomStore] WebSocket closed')
      if (!hasLeftRoom && activeRoom.value) {
        // Jika putus bukan karena leave, cek status room
        try {
          const res = await api.get(`/rooms/${activeRoom.value.id}`)
          if (res.data?.status !== 'active') {
            toast({
              title: 'Sesi Berakhir',
              description: 'Room telah ditutup atau koneksi terputus.',
            })
            activeRoom.value = null
            messages.value = []
            matchmakingStatus.value = 'idle'
            isNewMatch.value = false
            localStorage.removeItem('activeRoom')
          }
        } catch {
          // Abaikan error
        }
      }
    }
    socket = ws
  }

  const sendMessage = (text) => {
    console.log('[RoomStore] sendMessage called with:', text)
    console.log('[RoomStore] socket:', socket)
    console.log('[RoomStore] readyState:', socket?.readyState)

    if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === 1)) {
      console.log('[RoomStore] Sending message...')
      socket.send(JSON.stringify({ type: 'chat', text }))
    } else {
      console.log('[RoomStore] WebSocket not ready, cannot send')
    }
  }

  const leaveRoom = async () => {
    hasLeftRoom = true

    try {
      await api.post('/matchmaking/leave')
      fetchRoomHistory()
    } catch {}

    socket?.close()
    activeRoom.value = null
    messages.value = []
    matchmakingStatus.value = 'idle'
    isNewMatch.value = false
    localStorage.removeItem('activeRoom')

    setTimeout(() => (hasLeftRoom = false), 500)
  }

  const endSession = async () => {
    hasLeftRoom = true

    try {
      await api.post('/matchmaking/end-room')
      fetchRoomHistory()
    } catch (err) {
      toast({
        title: 'Gagal',
        description: 'Tidak bisa mengakhiri sesi',
        variant: 'destructive',
      })
    }

    socket?.close()
    activeRoom.value = null
    messages.value = []
    matchmakingStatus.value = 'idle'
    isNewMatch.value = false
    localStorage.removeItem('activeRoom')

    setTimeout(() => (hasLeftRoom = false), 500)
  }

  const clearAutoNavigate = () => {
    isNewMatch.value = false
  }

  return {
    // State
    activeRoom,
    matchmakingStatus,
    messages,
    roomHistory,
    isReconnecting,
    isNewMatch,
    // Actions
    initRoom,
    startMatchmaking,
    sendMessage,
    leaveRoom,
    endSession,
    fetchRoomHistory,
    clearAutoNavigate,
  }
})
