<script setup>
import { getRecipes } from '../api/recipes.js'
import { ref, onMounted } from 'vue'
import RecipeCard from '../components/RecipeCard.vue' 

const recipes = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    recipes.value = await getRecipes()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="px-4 py-6">
    <h1 class="font-display text-[34px] italic leading-[1.1]">Bonjour !</h1>
    <p class="mt-1 text-muted-foreground">De quoi vous avez envie ?</p>

    <section class="mt-4">
        <p v-if="loading">Chargement...</p>
        <p v-else-if="error" class="py-10 text-center text-[#A6472A]">Erreur : {{ error }}</p>
        <p v-else-if="recipes.length === 0" class="py-10 text-center text-muted-foreground">
            Aucune recette disponible
        </p>

        <RecipeCard
            v-for="(recipe, i) in recipes"
            :key="recipe.id"
            :recipe="recipe"
            :index="i + 1"
        />
    </section>
  </div>
</template>