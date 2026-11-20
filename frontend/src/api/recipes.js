const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function getRecipes(tagId) {
    let url = API_URL + "/"

    if (tagId) {
        url += `?tag_id=${tagId}`
    }
    const response = await fetch(`${url}`)
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
    }
   


