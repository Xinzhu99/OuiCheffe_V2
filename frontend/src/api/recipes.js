const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function getRecipes(tagId, search) {
    const params = new URLSearchParams()           

    if (tagId) {
        params.append('tag_id', tagId)             
    }
    if (search && search.trim()) {                 
        params.append('search', search.trim())     
    }

    const url = `${API_URL}/?${params.toString()}`

    const response = await fetch(url)
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
}