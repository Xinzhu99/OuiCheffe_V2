const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function getRecipes() {
    const response = await fetch(`${API_URL}/`)
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
}

