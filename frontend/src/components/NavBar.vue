<template>
  <nav class="bg-indigo-900 text-white">
    <div class="w-full max-w-full mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center gap-3">
          <span class="text-2xl">🥛</span>
          <span class="font-bold text-xl tracking-tight">Milk Collection</span>
        </div>
        <div class="flex items-center gap-3">
          <button
            @click="toggleMobileMenu"
            class="inline-flex items-center justify-center rounded-md p-2 text-indigo-100 hover:bg-indigo-800 md:hidden"
            type="button"
            aria-label="Open mobile menu"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <div class="hidden md:flex items-center gap-1">
            <router-link
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              :class="[
                'px-3 py-2 rounded-md text-sm font-medium transition-colors',
                $route.path === item.path ? 'bg-indigo-800 text-white' : 'text-indigo-100 hover:bg-indigo-800 hover:text-white'
              ]"
            >
              {{ item.name }}
            </router-link>
            <div class="ml-4 flex items-center gap-3">
              <div v-if="auth.isAuthenticated" class="relative" ref="userMenuWrapper">
                <button
                  @click="toggleUserMenu"
                  class="flex items-center justify-center w-10 h-10 rounded-full bg-indigo-800 text-indigo-100 hover:bg-indigo-700 transition"
                  type="button"
                  aria-label="User menu"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 2a4 4 0 100 8 4 4 0 000-8zM2 18a8 8 0 0116 0H2z" clip-rule="evenodd" />
                  </svg>
                </button>
                <div
                  v-show="showUserMenu"
                  class="transition duration-150 ease-out absolute right-0 mt-2 w-56 rounded-xl bg-white text-left shadow-lg border border-gray-200 z-50"
                >
                  <div class="px-4 py-3 border-b border-gray-100">
                    <p class="text-sm font-semibold text-gray-900">Logged in as</p>
                    <p class="truncate text-sm text-gray-600">{{ auth.user?.full_name || 'User' }}</p>
                  </div>
                  <button
                    @click="logout"
                    class="w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-gray-50"
                  >
                    Logout
                  </button>
                </div>
              </div>
              <router-link
                v-else
                to="/login"
                class="px-3 py-2 rounded-md text-sm font-medium text-indigo-100 hover:bg-indigo-800 hover:text-white"
              >
                Login
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <div v-show="mobileMenuOpen" class="md:hidden border-t border-indigo-800 bg-indigo-900/95">
        <div class="space-y-1 px-4 py-3">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            @click="mobileMenuOpen = false"
            :class="[
              'block rounded-md px-3 py-2 text-base font-medium transition-colors',
              $route.path === item.path ? 'bg-indigo-800 text-white' : 'text-indigo-100 hover:bg-indigo-800 hover:text-white'
            ]"
          >
            {{ item.name }}
          </router-link>
          <div v-if="auth.isAuthenticated" class="pt-2 border-t border-indigo-800">
            <button
              @click="logout"
              class="w-full text-left rounded-md px-3 py-2 text-base font-medium text-indigo-100 hover:bg-indigo-800 hover:text-white"
            >
              Logout
            </button>
          </div>
          <router-link
            v-else
            to="/login"
            class="block rounded-md px-3 py-2 text-base font-medium text-indigo-100 hover:bg-indigo-800 hover:text-white"
            @click="mobileMenuOpen = false"
          >
            Login
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const showUserMenu = ref(false)
const mobileMenuOpen = ref(false)
const userMenuWrapper = ref(null)

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeUserMenu = (event) => {
  if (!userMenuWrapper.value) return
  if (userMenuWrapper.value.contains(event.target)) return
  showUserMenu.value = false
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

onMounted(() => {
  document.addEventListener('click', closeUserMenu)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', closeUserMenu)
})

const navItems = [
  { name: 'Dashboard', path: '/' },
  { name: 'Reports', path: '/reports' },
  { name: 'Daily Entry', path: '/daily-entry' },
  { name: 'Bulk Entry', path: '/bulk-entry' },
  { name: 'Customers', path: '/customers' },
  { name: 'Products', path: '/products' },
  { name: 'Purchase Products', path: '/purchase-products' },
  { name: 'Portal', path: '/portal' },
  { name: 'Payments', path: '/payments' }
]

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>