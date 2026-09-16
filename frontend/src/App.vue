<script setup>
import { ref, onMounted } from 'vue'

const backendStatus = ref('en attente...')

onMounted(async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/`)
    const data = await response.json()
    backendStatus.value = data.Hello
    console.log('Backend status:', data)
  } catch (error) {
    backendStatus.value = 'erreur: ' + error.message
  }
})
</script>

<template>
  <h1 class="text-blue-600">
    You did it!
  </h1>
  <p>Statut backend : {{ backendStatus }}</p>
</template>

<style scoped></style>