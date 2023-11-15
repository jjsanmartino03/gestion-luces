<script setup>
import { useUsersStore } from '../../../stores/users'
import { useRouter } from 'vue-router'
import UsuarioForm from './UsuarioForm.vue'

const usersStore = useUsersStore()
const router = useRouter()

async function handleSubmit(data) {
  const result = await usersStore.createUser(data)

  if (result) router.push('/dashboard/usuarios')
}

</script>

<template>
  <div class='home-container'>
    <h2>Crear usuario</h2>

    <div v-if='usersStore.loading'>
      Cargando...
    </div>
    <usuario-form v-else :handle-submit='handleSubmit' />

  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding-top: 1rem;

  padding-left: .5rem;
  padding-right: .5rem;
}
</style>
