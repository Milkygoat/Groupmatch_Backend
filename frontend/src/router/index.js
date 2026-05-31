import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Views
import LandingPage from '@/views/LandingPage.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import ProfileSetup from '@/views/ProfileSetup.vue'
import Dashboard from '@/views/Dashboard.vue'
import Room from '@/views/Room.vue'
import OAuthCallback from '@/views/OAuthCallback.vue'

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
    meta: { guest: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { guest: true }
  },
  {
    path: '/auth/callback',
    name: 'OAuthCallback',
    component: OAuthCallback
  },
  {
    path: '/auth/google/callback',
    name: 'OAuthCallbackGoogle',
    component: OAuthCallback
  },
  {
    path: '/oauth/callback',
    name: 'OAuthCallbackAlt',
    component: OAuthCallback
  },
  {
    path: '/profile-setup',
    name: 'ProfileSetup',
    component: ProfileSetup,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true, requiresProfile: true }
  },
  {
    path: '/room',
    name: 'Room',
    component: Room,
    meta: { requiresAuth: true, requiresProfile: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Wait for auth initialization
  if (authStore.loading) {
    await new Promise(resolve => {
      const unwatch = authStore.$subscribe(() => {
        if (!authStore.loading) {
          unwatch()
          resolve()
        }
      })
      // Fallback timeout
      setTimeout(() => {
        unwatch()
        resolve()
      }, 3000)
    })
  }

  const isAuthenticated = authStore.isAuthenticated
  const isProfileComplete = authStore.isProfileComplete

  // Guest routes (login, register)
  if (to.meta.guest) {
    if (isAuthenticated && isProfileComplete) {
      return next('/dashboard')
    }
    if (isAuthenticated && !isProfileComplete) {
      return next('/profile-setup')
    }
    return next()
  }

  // Protected routes
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      return next('/login')
    }

    if (to.meta.requiresProfile && !isProfileComplete) {
      return next('/profile-setup')
    }
  }

  next()
})

export default router
