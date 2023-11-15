<script setup>
import { useUsersStore } from '../../../stores/users'
import { useRoute, useRouter } from 'vue-router'
import UsuarioForm from './UsuarioForm.vue'
import { onMounted, ref } from 'vue'

const usersStore = useUsersStore()
const router = useRouter()

const route = useRoute()

const formData = ref(null)

onMounted(async () => {
  const userData = await usersStore.getUser(route.params.id)

  if (userData) formData.value = userData
})

async function handleSubmit(data) {
  const result = await usersStore.editUser(route.params.id, data)

  if (result) router.push('/dashboard/usuarios')
}

</script>

<template>
  <div class='home-container'>
    <h2>Crear usuario</h2>

    <div v-if='usersStore.loading || !formData'>
      Cargando...
    </div>
    <usuario-form v-else :user='formData' :handle-submit='handleSubmit' />

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
}
</style>
