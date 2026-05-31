# GroupMatch - Vue.js Version

Aplikasi matchmaking tim berbasis skill menggunakan Vue.js 3 dan Pinia.

## Fitur

- 🔐 Autentikasi (Login, Register, OAuth Google)
- 👤 Manajemen Profil
- 🔍 Smart Matchmaking
- 💬 Real-time Chat dengan WebSocket
- 📜 Riwayat Tim

## Teknologi

- **Frontend**: Vue.js 3 (Composition API)
- **State Management**: Pinia
- **Routing**: Vue Router 4
- **Styling**: Tailwind CSS
- **Icons**: Lucide Vue Next
- **Build Tool**: Vite

## Instalasi

```bash
# Masuk ke folder project
cd FE-Groupmatch-Vue

# Install dependencies
npm install

# Jalankan dengan mock mode (tanpa backend)
npm run dev:mock
```

## Struktur Folder

```
src/
├── assets/          # CSS dan asset statis
├── components/      # Komponen Vue
│   └── ui/          # Komponen UI reusable
├── composables/     # Vue composables (hooks)
├── lib/             # Utility functions
├── mock/            # Mock API dan data
├── router/          # Konfigurasi Vue Router
├── services/        # API services
├── stores/          # Pinia stores
│   ├── auth.js      # Store untuk autentikasi
│   └── room.js      # Store untuk room & matchmaking
└── views/           # Halaman/views
    ├── Dashboard.vue
    ├── LandingPage.vue
    ├── Login.vue
    ├── OAuthCallback.vue
    ├── ProfileSetup.vue
    ├── Register.vue
    └── Room.vue
```

## Environment Variables

Buat file `.env` di root folder:

```env
VITE_MOCK_MODE=true
```

## Scripts

- `npm run dev:mock` - Development dengan mock mode
- `npm run build` - Build production
- `npm run preview` - Preview production build

### Catatan
Untuk frontendnya sebelumnya menggunakan backend asli yang sudah di deploy tetapi karena trialnya sudah habis 
jadi pada codingan kami menggunakan Mockup saja, tidak menggunakan backend. 