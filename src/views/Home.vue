<template>
  <div class="container">
    <h1>{{ message }}</h1>
    <p>{{ backendMessage }}</p>
    
    <div class="auth-section">
      <h2>TikTok Authentication</h2>
      <button @click="loginWithTikTok" class="tiktok-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/>
        </svg>
        Login with TikTok
      </button>
      <p class="hint">Click to authenticate with your TikTok account</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const message = ref('Welcome to Cookr!')
const backendMessage = ref('Loading...')

const API_URL = import.meta.env.VITE_API_URL || 'https://api.cookr.dev'

onMounted(async () => {
  try {
    const response = await fetch(`${API_URL}/`)
    const data = await response.json()
    backendMessage.value = data.message
  } catch (error) {
    backendMessage.value = 'Backend not connected'
  }
})

const loginWithTikTok = () => {
  // Redirect to backend TikTok OAuth endpoint
  window.location.href = `${API_URL}/auth/tiktok`
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  font-family: Arial, sans-serif;
  gap: 2rem;
}

h1 {
  color: #42b983;
  font-size: 3rem;
  margin-bottom: 1rem;
}

p {
  color: #666;
  font-size: 1.5rem;
}

.auth-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding: 2rem;
  border-radius: 12px;
  background: #f7f7f7;
}

.auth-section h2 {
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.tiktok-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(45deg, #ff0050, #00f2ea);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tiktok-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 0, 80, 0.3);
}

.tiktok-btn:active {
  transform: translateY(0);
}

.hint {
  color: #999;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}
</style>

