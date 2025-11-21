import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('user_token') || '')
  // Ensure user object has fields expected by App.vue (likedArticles, keywords)
  const user = ref({ id: null, username: '', keywords: '', likedArticles: [] })

  const isAuthenticated = () => !!token.value

  function setToken(t) {
    token.value = t
    if (t) localStorage.setItem('user_token', t)
    else localStorage.removeItem('user_token')
  }

  function loginSimulate(username = 'UserA') {
    // Development-only simulated login
    const demoToken = 'demo-token'
    setToken(demoToken)
    user.value = { id: 1, username, keywords: 'IT/테크, 경제/금융' }
  }

  function logout() {
    setToken('')
    user.value = { id: null, username: '', keywords: '' }
  }

  function registerSimulate(username, topics = []) {
    // simulator: register then auto-login
    user.value = { id: Math.floor(Math.random() * 1000) + 2, username, keywords: topics.join(', ') }
    const demoToken = 'demo-token'
    setToken(demoToken)
  }

  return { token, user, isAuthenticated, setToken, loginSimulate, logout, registerSimulate }
})
