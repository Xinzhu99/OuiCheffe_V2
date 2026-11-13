<script setup>
import { ref } from 'vue'
import { Check, Plus, UtensilsCrossed } from '@lucide/vue'

defineProps({
  recipe: { type: Object, required: true },
  index: { type: Number, required: true },
})

const selected = ref(false)



</script>

<template>
    <article class="border-b border-border py-3 first:pt-0 last:border-b-0">
        <div class="grid grid-cols-2 items-center gap-3">
            <div class="flex min-w-0 flex-col gap-1.5">
                <span class="font-display text-[34px] leading-none">
                    {{  String(index).padStart(2, '0') }}

                </span>
                <h3 class="font-display text-[20px] leading-snug line-clamp-2">
                    {{ recipe.name }}
                </h3>
                <p class="text-[12px] text-muted-foreground">
                    {{ recipe.prep_time }} min · {{  recipe.tags.map(t=>t.name).join(', ') }} 
                </p>

                <button 
                    type="button"
                    class="inline-flex h-10 w-fit items-center gap-1.5 rounded px-3.5 text-[14px] font-medium"

                    :class="selected
                        ? 'bg-success text-success-foreground border border-success-border'
                        : 'bg-primary text-primary-foreground'"
                    @click="selected = !selected">
                    
                    {{ selected ? 'Ajouté' : 'Ajouter' }}
                </button>
            </div>

            <div class="mr-1 flex aspect-[4/3] items-center justify-center overflow-hidden bg-muted text-muted-foreground">
                <img
                    v-if="recipe.image_url"
                    :src="recipe.image_url"
                    :alt="recipe.name"
                    class="h-full w-full object-cover"
                    loading="lazy"
                />
                <UtensilsCrossed v-else :size="28" :stroke-width="1.5" />
            </div>
        </div>

    </article>
</template>