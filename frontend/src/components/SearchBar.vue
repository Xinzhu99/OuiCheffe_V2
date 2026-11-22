<script setup>
import { Search } from '@lucide/vue'   // l'icône 🔍 (majuscule)
import { ref } from 'vue'

const emit = defineEmits(['search'])   // la sonnette, même nom que @search dans HomeView

const search = ref('')                 // le texte tapé (minuscule)

// appelée au clic sur le bouton OU à l'appui sur Entrée
const onSubmit = () => {
  emit('search', search.value)         // dans le script → .value
}
</script>

<template>
  <!-- @submit.prevent : 
       - @submit  = se déclenche au clic sur le bouton ET à la touche Entrée
       - .prevent = empêche le navigateur de recharger la page (comportement par défaut d'un form) -->
  <form @submit.prevent="onSubmit" class="mt-4 flex items-center gap-2">
    <input
      v-model="search"                 
      type="search"
      placeholder="Rechercher une recette..."
      class="h-10 flex-1 rounded border px-3 text-[14px]"
    />
    <!-- type="submit" : ce bouton déclenche le @submit du form -->
    <button
      type="submit"
      aria-label="Rechercher"
      class="inline-flex h-10 w-10 items-center justify-center rounded bg-primary text-primary-foreground"
    >
      <Search class="h-5 w-5" />       <!-- l'icône dans le bouton -->
    </button>
  </form>
</template>