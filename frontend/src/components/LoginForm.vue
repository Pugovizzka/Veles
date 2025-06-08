<template>
  <div class="login-container">
    <div class="login-form">
      <h2>Вход в систему</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email:</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required 
            class="form-control"
          >
        </div>
        
        <div class="form-group">
          <label for="password">Пароль:</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            class="form-control"
          >
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const router = useRouter()
const store = useStore()

const handleLogin = async () => {
  try {
    loading.value = true
    error.value = ''
    
    await store.dispatch('auth/login', {
      email: email.value,
      password: password.value
    })
    
    router.push('/dashboard')
  } catch (err) {
    error.value = 'Неверный email или пароль'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gabarito:wght@400;500;600;700&display=swap');

.login-container {
  min-height: 100vh;
  background: rgba(58, 60, 65, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Gabarito', sans-serif;
}

.login-form {
  max-width: 400px;
  width: 100%;
  margin: 40px auto;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  background: rgba(19, 24, 27, 1);
  border: 1px solid rgba(243, 238, 232, 0.1);
}

.login-form h2 {
  color: rgba(243, 238, 232, 1);
  text-align: center;
  margin-bottom: 30px;
  font-weight: 600;
}

.form-group {
  margin-bottom: 20px;
}

.form-control {
  width: 100%;
  padding: 12px;
  border: 1px solid rgba(243, 238, 232, 0.3);
  border-radius: 6px;
  background: rgba(58, 60, 65, 1);
  color: rgba(243, 238, 232, 1);
  font-family: 'Gabarito', sans-serif;
  transition: all 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: rgba(131, 21, 21, 1);
  box-shadow: 0 0 0 2px rgba(131, 21, 21, 0.2);
}

label {
  display: block;
  margin-bottom: 8px;
  color: rgba(243, 238, 232, 1);
  font-weight: 500;
}

button {
  width: 100%;
  padding: 12px;
  background-color: rgba(131, 21, 21, 1);
  color: rgba(243, 238, 232, 1);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-family: 'Gabarito', sans-serif;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
}

button:hover:not(:disabled) {
  background-color: rgba(151, 31, 31, 1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(131, 21, 21, 0.4);
}

button:disabled {
  background-color: rgba(131, 21, 21, 0.5);
  cursor: not-allowed;
  transform: none;
}

.error-message {
  color: #ff6b6b;
  margin-bottom: 15px;
  text-align: center;
  font-weight: 500;
}
</style>