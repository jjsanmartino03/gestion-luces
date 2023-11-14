<script setup>
import CustomButton from '../../components/CustomButton.vue'
import Input from '../../components/CustomInput.vue'
import { onMounted, onUnmounted, ref } from 'vue'
import { useUsersStore } from '../../stores/users'

const searchText = ref('')
const usersStore = useUsersStore()

onMounted(() => {
  usersStore.getUsers()
})

console.log(usersStore.users)
const filteredUsers = usersStore.users.filter(user => (user.first_name + ' ' + user.last_name)
  .toLowerCase().match(searchText.toLowerCase()))
</script>

<template>
  <div class='home-container'>
    <div class='search-container'>
      <Input placeholder='Buscar' input-id='search' v-model='searchText' />
    </div>

    <div v-if='usersStore.loading'>
      Cargando...
    </div>
    <table v-else class='users-table'>
      <tbody>
      <tr
        v-for='(user, index) in usersStore.users'
        :key='index'>
        <td>{{ user.first_name + ' ' + user.last_name }}</td>
        <td>
          <custom-button disabled='disabled'
            :theme='user.is_active ? "secondary" : "primary"'>
            {{ user.is_active ? 'Activo' : 'Inactivo' }}
          </custom-button>
        </td>
      </tr>
      </tbody>
    </table>
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

.users-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #ddd;
  font-size: 18px;
  text-align: center;
}

.users-table td {
  width: 33%;
  padding: .5rem 1rem;
  border-top: 2px solid #828589;
}

.users-table tr:last-child td {
  border-bottom: 2px solid #828589; /* Increase space for all rows except the last one */
}

.search-container {
  align-self: center;
  width: 75%;
}
</style>
