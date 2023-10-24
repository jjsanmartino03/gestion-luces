<script setup>
import Input from '../components/CustomInput.vue'
import CustomButton from '../components/CustomButton.vue'
</script>

<template>
  <main>
    <div class='login-card'>
      <form>
        <h1>Ingresar</h1>
        <Input input-id='username' label='Nombre de Usuario' v-model='username'
               placeholder='Ingresa tu nombre de usuario' />
        <Input placeholder='Ingresa tu contraseña' input-id='password' label='Contraseña' v-model='password'
               type='password' />
        <CustomButton theme='light' variant='primary' @click='login'>Iniciar sesión</CustomButton>
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

form {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 500px;
  height: 100%;
  gap: 2rem;
  align-items: center;
  justify-content: space-between;
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

</style>

<script>
import Input from '../components/CustomInput.vue'

export default {
  name: 'LoginView',
  components: {
    Input
  },
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login() {
      alert('Hello!')
    }
  }
}
</script>