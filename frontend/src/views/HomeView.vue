<script setup>
import { getRecipes } from '../api/recipes.js'
import { ref, onMounted } from 'vue'
import RecipeCard from '../components/RecipeCard.vue' 
import SearchBar from '../components/SearchBar.vue'  
import TagsBar from '../components/TagsBar.vue'  

const recipes = ref([])
const loading = ref(true)
const error = ref(null)

// 📒 le carnet
const selectedTagId = ref(null)
const searchText = ref('')

// lit le carnet et appelle l'API
const loadRecipes = async () => {
  loading.value = true            // regroupé ici : plus besoin de le répéter ailleurs
  error.value = null
  try {
    recipes.value = await getRecipes(selectedTagId.value, searchText.value)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

// au chargement : carnet vide → toutes les recettes
onMounted(loadRecipes)            // on donne la recette à Vue, sans ()

const onTagSelected = (tagId) => {
  selectedTagId.value = tagId     // noter dans le carnet
  loadRecipes()                   // recharger
}

const onAddSearch = (search) => {
  searchText.value = search       // le trim est déjà fait dans api/recipes.js
  loadRecipes()
}
</script>

<template>
  <div class="px-4 py-6">
    <h1 class="font-display text-[34px] italic leading-[1.1]">Bonjour !</h1>
    <p class="mt-1 text-muted-foreground">De quoi vous avez envie ?</p>
    
    <SearchBar @search="onAddSearch"/>
    <TagsBar @selected_tag="onTagSelected"/>

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