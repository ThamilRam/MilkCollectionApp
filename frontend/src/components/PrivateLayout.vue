<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />
    <PageLoader />
    <main class="w-full max-w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from './NavBar.vue'
import PageLoader from './PageLoader.vue'
</script>