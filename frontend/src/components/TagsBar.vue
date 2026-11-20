<script setup>
import { getTags} from '../api/tags.js'
import { ref, onMounted } from 'vue'

const tags = ref([])

const error = ref(null)

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
        v-for="tag in tags">
        <button 
                type="button"
                class="inline-flex h-10 w-fit items-center gap-1.5 rounded px-3.5 text-[14px] font-medium"
                    >
                    
                    {{ tag.name}}
                </button>
    </div>

</template>