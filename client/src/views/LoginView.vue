<script setup>
import Input from '../components/CustomInput.vue'
import CustomButton from '../components/CustomButton.vue'
import { useAuthStore } from '../stores/auth'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const router = useRouter()


if (authStore.isAuthenticated) {
  router.push('/dashboard')
}

async function login(e) {
  e.preventDefault()
  const result = await authStore.login(username.value, password.value)

  if (result) {
    router.push('/dashboard')
  }
}
</script>

<template>
  <main>
    <div class='login-card'>
      <form @submit='login'>
        <h1>Ingresar</h1>
        <div class='inputs-container'>
          <Input required input-id='username' label='Nombre de Usuario' v-model='username'
                 placeholder='Ingresa tu nombre de usuario' />
          <Input required placeholder='Ingresa tu contraseña' input-id='password' label='Contraseña' v-model='password'
                 type='password' />
        </div>
        <CustomButton type='submit' theme='primary' variant='solid'>
          Continuar</CustomButton>
      </form>
    </div>
  </main>
</template>

<style scoped>
main {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 1rem 1rem;
}

h1 {
  font-size: 3rem;
}

form {
  display: flex;
  flex-direction: column;


  height: 100%;
  gap: 3rem;
  align-items: center;
  justify-content: space-between;
}

form input {
  width: 100%;
}

label {
  text-align: center;
}

.login-card {
  display: flex;
  justify-content: center;
  flex-direction: column;
}

input {
  outline: none;
  border: none;
  border-bottom: 1px solid gray;
}

.inputs-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

form button {
  font-size: 1.5rem;
}
</style>