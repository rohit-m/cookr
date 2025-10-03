<template>
  <div class="search-container">
    <!-- Header with user info -->
    <header class="header">
      <div class="logo">
        <h1>🍳 Cookr</h1>
      </div>
      <div v-if="user" class="user-info">
        <img v-if="user.avatar_url" :src="user.avatar_url" :alt="user.display_name" class="avatar" />
        <span class="username">{{ user.display_name }}</span>
      </div>
    </header>

    <!-- Auth Status -->
    <div v-if="loading" class="status-message loading">
      <div class="spinner"></div>
      <p>Authenticating with TikTok...</p>
    </div>

    <div v-else-if="error" class="status-message error">
      <p>❌ {{ error }}</p>
      <button @click="goHome" class="btn-secondary">Go Back</button>
    </div>

    <!-- Main Search Section -->
    <div v-else class="main-content">
      <div class="search-section">
        <h2>Search TikTok Videos</h2>
        <div class="search-bar">
          <input 
            v-model="searchQuery" 
            @keyup.enter="searchVideos"
            type="text" 
            placeholder="Search for recipes, cooking tips, ingredients..."
            class="search-input"
          />
          <button @click="searchVideos" class="search-button" :disabled="!searchQuery.trim()">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
            Search
          </button>
        </div>
        <p class="hint">Press Enter or click Search to find TikTok videos</p>
      </div>

      <!-- Search Results -->
      <div v-if="searching" class="results-loading">
        <div class="spinner"></div>
        <p>Searching TikTok...</p>
      </div>

      <div v-else-if="searchResults.length > 0" class="results-section">
        <h3>Search Results</h3>
        <div class="results-grid">
          <div v-for="video in searchResults" :key="video.id" class="video-card">
            <div class="video-thumbnail">
              <img :src="video.cover_image_url" :alt="video.title" />
            </div>
            <div class="video-info">
              <h4>{{ video.title }}</h4>
              <p class="video-stats">
                👁️ {{ formatNumber(video.view_count) }} views · 
                ❤️ {{ formatNumber(video.like_count) }} likes
              </p>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="hasSearched" class="no-results">
        <p>No results found. Try a different search term.</p>
      </div>

      <!-- API Info Panel (for development) -->
      <div class="api-info">
        <details>
          <summary>🔧 API Info (Development)</summary>
          <div class="api-details">
            <p><strong>Access Token:</strong> {{ accessToken ? '✓ Available' : '❌ Not available' }}</p>
            <p><strong>Token (first 20 chars):</strong> {{ accessToken ? accessToken.substring(0, 20) + '...' : 'N/A' }}</p>
            <p><strong>User ID:</strong> {{ user?.open_id || 'N/A' }}</p>
            <p><strong>Ready to call TikTok API:</strong> {{ accessToken ? '✅ Yes' : '❌ No' }}</p>
          </div>
        </details>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const API_URL = import.meta.env.VITE_API_URL || 'https://api.cookr.dev'

const loading = ref(true)
const error = ref(null)
const user = ref(null)
const accessToken = ref(null)
const searchQuery = ref('')
const searching = ref(false)
const searchResults = ref([])
const hasSearched = ref(false)

onMounted(async () => {
  await handleTikTokCallback()
})

async function handleTikTokCallback() {
  try {
    // Check if we have the access token and user data in the URL query params
    const urlParams = new URLSearchParams(window.location.search)
    const token = urlParams.get('access_token')
    const userData = urlParams.get('user')
    
    if (token) {
      accessToken.value = token
      
      // Parse user data if present
      if (userData) {
        try {
          user.value = JSON.parse(decodeURIComponent(userData))
        } catch (e) {
          console.error('Error parsing user data:', e)
        }
      }
      
      // Clean up URL (remove query params)
      window.history.replaceState({}, document.title, window.location.pathname)
      
      loading.value = false
    } else {
      // No token in URL - check if we're coming from OAuth or already authenticated
      error.value = 'No access token found. Please authenticate with TikTok first.'
      loading.value = false
    }
  } catch (err) {
    console.error('Error handling TikTok callback:', err)
    error.value = err.message || 'Failed to authenticate with TikTok'
    loading.value = false
  }
}

async function searchVideos() {
  if (!searchQuery.value.trim() || !accessToken.value) {
    return
  }

  searching.value = true
  hasSearched.value = true
  searchResults.value = []

  try {
    // Example: Call TikTok Video List API
    // Note: You'll need to implement this endpoint in your backend
    const response = await fetch(`${API_URL}/tiktok/search?query=${encodeURIComponent(searchQuery.value)}`, {
      headers: {
        'Authorization': `Bearer ${accessToken.value}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('Search failed')
    }

    const data = await response.json()
    searchResults.value = data.videos || []
  } catch (err) {
    console.error('Search error:', err)
    error.value = 'Failed to search videos. The API endpoint may not be implemented yet.'
  } finally {
    searching.value = false
  }
}

function formatNumber(num) {
  if (!num) return '0'
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

function goHome() {
  router.push('/')
}
</script>

<style scoped>
.search-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logo h1 {
  font-size: 1.8rem;
  margin: 0;
  color: #333;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #ff0050;
}

.username {
  font-weight: 600;
  color: #333;
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

/* Search Section */
.search-section {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.search-section h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 1.5rem;
  text-align: center;
}

.search-bar {
  display: flex;
  gap: 1rem;
  max-width: 700px;
  margin: 0 auto;
}

.search-input {
  flex: 1;
  padding: 1rem 1.5rem;
  font-size: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  outline: none;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #ff0050;
  box-shadow: 0 0 0 3px rgba(255, 0, 80, 0.1);
}

.search-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(45deg, #ff0050, #00f2ea);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(255, 0, 80, 0.3);
}

.search-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.hint {
  text-align: center;
  color: #999;
  font-size: 0.9rem;
  margin-top: 1rem;
}

/* Status Messages */
.status-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 1rem;
}

.status-message.loading {
  color: #666;
}

.status-message.error {
  color: #d32f2f;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #ff0050;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Results */
.results-loading {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.results-section h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.video-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
}

.video-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.video-thumbnail {
  width: 100%;
  height: 180px;
  overflow: hidden;
  background: #f0f0f0;
}

.video-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-info {
  padding: 1rem;
}

.video-info h4 {
  font-size: 1rem;
  color: #333;
  margin: 0 0 0.5rem 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.video-stats {
  font-size: 0.85rem;
  color: #666;
  margin: 0;
}

.no-results {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.1rem;
}

/* API Info Panel */
.api-info {
  margin-top: 3rem;
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.api-info summary {
  cursor: pointer;
  font-weight: 600;
  color: #666;
  padding: 0.5rem;
  user-select: none;
}

.api-info summary:hover {
  color: #333;
}

.api-details {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  margin-top: 0.5rem;
}

.api-details p {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  color: #555;
  font-family: 'Courier New', monospace;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  color: #666;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  border-color: #ff0050;
  color: #ff0050;
}
</style>

