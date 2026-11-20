<script setup>
import { getTags} from '../api/tags.js'
import { ref, onMounted } from 'vue'

const tags = ref([])
const emit = defineEmits(['selected_tag'])
const error = ref(null)
const selected = ref(null)

onMounted(async () => {
    try {
        tags.value = await getTags()
    } catch(e) {
        error.value = e.message
    } 
})


</script>

<template>
    <div 
        v-for="tag in tags" :key="tag.id">
        <button 
                type="button"
                class="inline-flex h-10 w-fit items-center gap-1.5 rounded px-3.5 text-[14px] font-medium"
                :class="tag.id == selected
                    ? 'bg-success text-success-foreground border border-success-border'
                    : 'bg-primary text-primary-foreground'
                    "
                @click="emit('selected_tag',tag.id), selected = tag.id"
                >
                    
                    {{ tag.name}}
                </button>
    </div>

</template>