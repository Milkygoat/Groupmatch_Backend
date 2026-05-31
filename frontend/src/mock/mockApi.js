/**
 * Mock API Service
 * Mensimulasikan response backend untuk preview UI tanpa backend
 */

// Simulated delay untuk mensimulasikan network latency
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

// Helper untuk persist mock user ke localStorage
const MOCK_USER_KEY = 'mockCurrentUser'
const MOCK_ROOM_KEY = 'mockRoom'
const MOCK_HISTORY_KEY = 'mockRoomHistory'
const MOCK_QUEUE_KEY = 'mockMatchmakingQueue'

const saveMockUser = (user) => {
  if (user) {
    localStorage.setItem(MOCK_USER_KEY, JSON.stringify(user))
  } else {
    localStorage.removeItem(MOCK_USER_KEY)
  }
}

const loadMockUser = () => {
  const saved = localStorage.getItem(MOCK_USER_KEY)
  return saved ? JSON.parse(saved) : null
}

const saveMockRoom = (room) => {
  if (room) {
    localStorage.setItem(MOCK_ROOM_KEY, JSON.stringify(room))
  } else {
    localStorage.removeItem(MOCK_ROOM_KEY)
  }
}

const loadMockRoom = () => {
  const saved = localStorage.getItem(MOCK_ROOM_KEY)
  return saved ? JSON.parse(saved) : null
}

const saveMockHistory = (history) => {
  localStorage.setItem(MOCK_HISTORY_KEY, JSON.stringify(history))
}

const loadMockHistory = () => {
  const saved = localStorage.getItem(MOCK_HISTORY_KEY)
  return saved ? JSON.parse(saved) : []
}

const saveMockQueue = (queue) => {
  localStorage.setItem(MOCK_QUEUE_KEY, JSON.stringify(queue))
}

const loadMockQueue = () => {
  const saved = localStorage.getItem(MOCK_QUEUE_KEY)
  return saved ? JSON.parse(saved) : []
}

const addToQueue = (user) => {
  const queue = loadMockQueue()
  const exists = queue.find(u => u.id === user.id)
  if (!exists) {
    queue.push({
      id: user.id,
      name: user.name,
      username: user.username,
      role: user.role,
      pict: user.pict,
      joinedAt: Date.now()
    })
    saveMockQueue(queue)
  }
  return queue
}

// Mock teammates untuk instant match di mock mode
const generateMockTeammates = () => {
  const mockNames = ['Alex Dev', 'Budi Coder', 'Cindy Tech', 'Deni Stack']
  const mockRoles = ['Backend Engineer', 'Frontend Engineer', 'UI/UX Designer', 'DevOps Engineer']
  
  return mockNames.slice(0, 2 + Math.floor(Math.random() * 2)).map((name, idx) => ({
    user_id: 'mock_user_' + Math.random().toString(36).substring(2, 8),
    name: name,
    username: name.toLowerCase().replace(' ', '_'),
    role: mockRoles[idx % mockRoles.length],
    pict: `https://api.dicebear.com/7.x/avataaars/svg?seed=${name.replace(' ', '')}`
  }))
}

const removeFromQueue = (userId) => {
  const queue = loadMockQueue()
  const filtered = queue.filter(u => u.id !== userId)
  saveMockQueue(filtered)
  return filtered
}

const addToHistory = (roomData) => {
  const history = loadMockHistory()
  const entry = {
    id: Date.now().toString(),
    room_id: roomData.id,
    action: `Room dengan ${roomData.members?.length || 0} anggota`,
    created_at: new Date().toISOString(),
    ...roomData
  }
  history.unshift(entry)
  const trimmed = history.slice(0, 10)
  saveMockHistory(trimmed)
}

// Mock state - load from localStorage if available
let mockCurrentUser = loadMockUser()
let mockToken = localStorage.getItem('token')
let mockRoom = loadMockRoom()
let mockMessages = []

// Generate mock token
const generateMockToken = () => {
  const token = 'mock_token_' + Math.random().toString(36).substring(2, 15)
  localStorage.setItem('token', token)
  return token
}

// Generate mock user ID
const generateUserId = () => {
  return 'user_' + Math.random().toString(36).substring(2, 10)
}

/**
 * Mock API handlers
 */
const mockHandlers = {
  'POST /auth/login': async (data) => {
    await delay(500)
    const { email, password } = data

    if (!email || !password) {
      throw { response: { status: 400, data: { detail: 'Email dan password harus diisi' } } }
    }

    mockToken = generateMockToken()
    mockCurrentUser = {
      id: generateUserId(),
      email: email,
      name: email.split('@')[0],
      username: email.split('@')[0],
      profileComplete: true,
      role: 'FE Engineer',
      skills: ['Vue', 'JavaScript'],
      pict: `https://api.dicebear.com/7.x/avataaars/svg?seed=${email}`
    }

    saveMockUser(mockCurrentUser)
    return { access_token: mockToken }
  },

  'POST /auth/register': async (data) => {
    await delay(500)
    const { email, name, username, password } = data

    if (!email || !password || !name) {
      throw { response: { status: 400, data: { detail: 'Semua field harus diisi' } } }
    }

    return { message: 'Registration successful' }
  },

  'GET /auth/google/login': async () => {
    await delay(300)
    mockToken = generateMockToken()
    mockCurrentUser = {
      id: generateUserId(),
      email: 'mock.google.user@gmail.com',
      name: 'Mock Google User',
      username: 'mockgoogleuser',
      profileComplete: false,
      role: null,
      skills: [],
      pict: 'https://api.dicebear.com/7.x/avataaars/svg?seed=GoogleUser'
    }

    saveMockUser(mockCurrentUser)
    return { login_url: `/auth/google/callback?token=${mockToken}` }
  },

  'GET /profile/me': async () => {
    await delay(300)

    if (!mockCurrentUser) {
      mockCurrentUser = loadMockUser()
    }

    if (!mockCurrentUser) {
      throw { response: { status: 401, data: { detail: 'Unauthorized' } } }
    }

    if (!mockCurrentUser.profileComplete) {
      throw { response: { status: 404, data: { detail: 'Profile not found' } } }
    }

    return {
      user_id: mockCurrentUser.id,
      name: mockCurrentUser.name,
      email: mockCurrentUser.email,
      role: mockCurrentUser.role,
      skill: mockCurrentUser.skills?.join(',') || '',
      pict: mockCurrentUser.pict
    }
  },

  'POST /profile/': async (data) => {
    await delay(400)

    if (!mockCurrentUser) {
      mockCurrentUser = loadMockUser()
    }

    if (!mockCurrentUser) {
      throw { response: { status: 401, data: { detail: 'Unauthorized' } } }
    }

    mockCurrentUser = {
      ...mockCurrentUser,
      name: data.name || mockCurrentUser.name,
      role: data.role || mockCurrentUser.role,
      skills: data.skill ? data.skill.split(',') : mockCurrentUser.skills,
      pict: data.pict || mockCurrentUser.pict,
      profileComplete: true
    }

    saveMockUser(mockCurrentUser)
    return { message: 'Profile created successfully' }
  },

  'PUT /profile/': async (data) => {
    await delay(400)

    if (!mockCurrentUser) {
      mockCurrentUser = loadMockUser()
    }

    if (!mockCurrentUser) {
      throw { response: { status: 401, data: { detail: 'Unauthorized' } } }
    }

    mockCurrentUser = {
      ...mockCurrentUser,
      name: data.name || mockCurrentUser.name,
      role: data.role || mockCurrentUser.role,
      skills: data.skill ? data.skill.split(',') : mockCurrentUser.skills,
      pict: data.pict || mockCurrentUser.pict
    }

    saveMockUser(mockCurrentUser)
    return { message: 'Profile updated successfully' }
  },

  'POST /profile/upload-avatar': async () => {
    await delay(800)
    const avatarUrl = `https://api.dicebear.com/7.x/avataaars/svg?seed=${Date.now()}`
    return { url: avatarUrl }
  },

  'POST /matchmaking/join': async () => {
    await delay(500)

    if (!mockCurrentUser) {
      mockCurrentUser = loadMockUser()
    }

    if (!mockCurrentUser) {
      throw { response: { status: 401, data: { detail: 'Unauthorized' } } }
    }

    // Di mock mode, langsung buat room dengan mock teammates (instant match)
    const mockTeammates = generateMockTeammates()
    const currentUserMember = {
      user_id: mockCurrentUser.id,
      name: mockCurrentUser.name,
      username: mockCurrentUser.username,
      role: mockCurrentUser.role,
      pict: mockCurrentUser.pict
    }

    mockRoom = {
      id: 'room_' + Math.random().toString(36).substring(2, 8),
      leader_id: mockCurrentUser.id, // User jadi leader
      members: [currentUserMember, ...mockTeammates],
      status: 'active'
    }

    mockMessages = []
    saveMockRoom(mockRoom)
    removeFromQueue(mockCurrentUser.id)

    return {
      room_id: mockRoom.id,
      id: mockRoom.id,
      leader_id: mockRoom.leader_id,
      members: mockRoom.members
    }
  },

  'GET /matchmaking/status': async () => {
    await delay(300)

    if (!mockCurrentUser) {
      mockCurrentUser = loadMockUser()
    }

    if (!mockRoom) {
      mockRoom = loadMockRoom()
    }

    if (mockRoom) {
      const isMember = mockRoom.members.some(m => m.user_id === mockCurrentUser?.id)
      if (isMember) {
        return {
          status: 'matched',
          room_id: mockRoom.id,
          id: mockRoom.id,
          leader_id: mockRoom.leader_id,
          members: mockRoom.members
        }
      }
    }

    const queue = loadMockQueue()
    const MIN_USERS_FOR_MATCH = 2

    if (queue.length >= MIN_USERS_FOR_MATCH) {
      const matchedUsers = queue.slice(0, Math.min(4, queue.length))

      mockRoom = {
        id: 'room_' + Math.random().toString(36).substring(2, 8),
        leader_id: matchedUsers[0].id,
        members: matchedUsers.map(u => ({
          user_id: u.id,
          name: u.name,
          username: u.username,
          role: u.role,
          pict: u.pict
        })),
        status: 'active'
      }

      saveMockRoom(mockRoom)
      matchedUsers.forEach(u => removeFromQueue(u.id))

      return {
        status: 'matched',
        room_id: mockRoom.id,
        id: mockRoom.id,
        leader_id: mockRoom.leader_id,
        members: mockRoom.members
      }
    }

    return {
      status: 'waiting',
      queue_size: queue.length
    }
  },

  'POST /matchmaking/leave': async () => {
    await delay(200)

    if (!mockCurrentUser) {
      mockCurrentUser = loadMockUser()
    }

    if (mockCurrentUser) {
      removeFromQueue(mockCurrentUser.id)
    }

    if (mockRoom) {
      addToHistory(mockRoom)
      mockRoom = null
      saveMockRoom(null)
    }

    return { message: 'Left queue' }
  },

  'POST /matchmaking/end-room': async () => {
    await delay(300)

    if (!mockCurrentUser) {
      mockCurrentUser = loadMockUser()
    }

    if (!mockCurrentUser) {
      throw { response: { status: 401, data: { detail: 'Unauthorized' } } }
    }

    if (!mockRoom) {
      throw { response: { status: 404, data: { detail: 'No active room' } } }
    }

    if (mockRoom.leader_id !== mockCurrentUser.id) {
      throw { response: { status: 403, data: { detail: 'Only room leader can end session' } } }
    }

    addToHistory(mockRoom)
    mockRoom = null
    mockMessages = []
    saveMockRoom(null)

    return { message: 'Room session ended successfully' }
  },

  'GET /rooms/': async () => {
    await delay(300)
    if (!mockRoom) {
      mockRoom = loadMockRoom()
    }
    return mockRoom ? [mockRoom] : []
  },

  'GET /rooms/my': async () => {
    await delay(300)

    if (!mockRoom) {
      mockRoom = loadMockRoom()
    }

    if (!mockRoom) {
      throw { response: { status: 404, data: { detail: 'No active room' } } }
    }

    return mockRoom
  },

  'GET /rooms/:id': async (data, params) => {
    await delay(300)

    if (!mockRoom) {
      mockRoom = loadMockRoom()
    }

    if (mockRoom && String(mockRoom.id) === String(params.id)) {
      return mockRoom
    }

    throw { response: { status: 404, data: { detail: 'Room not found' } } }
  },

  'POST /rooms/:id/leave': async () => {
    await delay(300)

    if (mockRoom) {
      addToHistory(mockRoom)
    }

    mockRoom = null
    mockMessages = []
    saveMockRoom(null)
    return { message: 'Left room' }
  },

  'DELETE /rooms/:id/members/me': async () => {
    await delay(300)

    if (mockRoom) {
      addToHistory(mockRoom)
    }

    mockRoom = null
    mockMessages = []
    saveMockRoom(null)
    return { message: 'Left room' }
  },

  'GET /rooms/history': async () => {
    await delay(300)

    if (!mockCurrentUser) {
      mockCurrentUser = loadMockUser()
    }

    if (!mockCurrentUser) {
      return []
    }

    return loadMockHistory()
  }
}

/**
 * Parse route pattern dan match dengan URL
 */
const matchRoute = (method, url) => {
  const fullKey = `${method} ${url}`

  if (mockHandlers[fullKey]) {
    return { handler: mockHandlers[fullKey], params: {} }
  }

  for (const key of Object.keys(mockHandlers)) {
    const [handlerMethod, handlerPath] = key.split(' ')
    if (handlerMethod !== method) continue

    const pathParts = handlerPath.split('/')
    const urlParts = url.split('?')[0].split('/')

    if (pathParts.length !== urlParts.length) continue

    const params = {}
    let isMatch = true

    for (let i = 0; i < pathParts.length; i++) {
      if (pathParts[i].startsWith(':')) {
        params[pathParts[i].substring(1)] = urlParts[i]
      } else if (pathParts[i] !== urlParts[i]) {
        isMatch = false
        break
      }
    }

    if (isMatch) {
      return { handler: mockHandlers[key], params }
    }
  }

  return null
}

/**
 * Mock API instance yang meniru axios
 */
export const createMockApi = () => {
  const mockRequest = async (method, url, data = null) => {
    console.log(`[MOCK API] ${method} ${url}`, data)

    const match = matchRoute(method, url)

    if (!match) {
      console.warn(`[MOCK API] No handler for ${method} ${url}`)
      throw { response: { status: 404, data: { detail: 'Endpoint not found' } } }
    }

    try {
      const result = await match.handler(data, match.params)
      console.log(`[MOCK API] Response:`, result)
      return { data: result }
    } catch (error) {
      console.error(`[MOCK API] Error:`, error)
      throw error
    }
  }

  return {
    get: (url, config) => mockRequest('GET', url),
    post: (url, data, config) => mockRequest('POST', url, data),
    put: (url, data, config) => mockRequest('PUT', url, data),
    delete: (url, config) => mockRequest('DELETE', url),

    interceptors: {
      request: { use: () => {} },
      response: { use: () => {} }
    }
  }
}

/**
 * Mock WebSocket untuk simulasi real-time chat
 */
export class MockWebSocket {
  static CONNECTING = 0
  static OPEN = 1
  static CLOSING = 2
  static CLOSED = 3

  constructor(url) {
    this.url = url
    this.readyState = 0 // CONNECTING
    this.onopen = null
    this.onmessage = null
    this.onclose = null
    this.onerror = null

    const savedRoom = loadMockRoom()
    if (savedRoom) {
      mockRoom = savedRoom
    }

    setTimeout(() => {
      this.readyState = 1 // OPEN
      if (this.onopen) this.onopen({ type: 'open' })

      if (mockRoom) {
        setTimeout(() => {
          this.simulateMessage({
            type: 'users_list',
            data: mockRoom.members.map(m => ({
              user_id: m.user_id,
              username: m.username,
              name: m.name,
              role: m.role,
              pict: m.pict
            }))
          })
        }, 500)
      }
    }, 300)
  }

  simulateMessage(payload) {
    console.log('[MOCK WS] simulateMessage called with:', payload)
    if (this.onmessage) {
      console.log('[MOCK WS] Calling onmessage handler')
      this.onmessage({ data: JSON.stringify(payload) })
    } else {
      console.log('[MOCK WS] No onmessage handler set')
    }
  }

  send(data) {
    if (this.readyState !== 1) {
      console.log('[MOCK WS] Cannot send, not connected. readyState:', this.readyState)
      return
    }

    const parsed = JSON.parse(data)
    console.log('[MOCK WS] Sent:', parsed)

    const currentUser = loadMockUser()
    console.log('[MOCK WS] Current user from localStorage:', currentUser)

    if (parsed.type === 'chat' && currentUser) {
      const self = this
      setTimeout(() => {
        console.log('[MOCK WS] Echoing back message')
        self.simulateMessage({
          type: 'chat',
          data: {
            user_id: currentUser.id,
            username: currentUser.username,
            name: currentUser.name,
            text: parsed.text
          }
        })
      }, 100)
    } else if (parsed.type === 'chat' && !currentUser) {
      console.log('[MOCK WS] No user found in localStorage')
    }
  }

  close() {
    this.readyState = 3 // CLOSED
    if (this.onclose) this.onclose({ type: 'close' })
  }
}

// Reset mock state
export const resetMockState = () => {
  mockCurrentUser = null
  mockToken = null
  mockRoom = null
  mockMessages = []
  saveMockQueue([])
}

// Set mock user langsung
export const setMockUser = (user) => {
  mockCurrentUser = user
  mockToken = generateMockToken()
}

// Get current mock user
export const getMockUser = () => mockCurrentUser

// Check if mock mode is enabled
export const isMockMode = () => {
  return import.meta.env.VITE_MOCK_MODE === 'true'
}
