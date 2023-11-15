<script setup>
import CustomButton from '../../../components/CustomButton.vue'
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useUsersStore } from '../../../stores/users'
import { useRouter } from 'vue-router'
import CustomInput from '../../../components/CustomInput.vue'

const searchText = ref('')
const router = useRouter()
const usersStore = useUsersStore()

onMounted(() => {
  usersStore.getUsers()
})

const filteredUsers = computed(() => usersStore.users.filter(user => (user.first_name + ' ' + user.last_name)
  .toLowerCase().match(searchText.value.toLowerCase())))

const createUser = () => router.push('/dashboard/usuarios/crear')

const editUser = (id) => router.push('/dashboard/usuarios/' + id)

const handleToggleClick = (e,id,status) => {
  e.stopPropagation()
  usersStore.toggleUser(id,status)
}

</script>

<template>
  <div class='home-container'>
    <custom-button :onclick='createUser' variant='link' class='add-user-container'>
      <p>Agregar nuevo usuario</p>
      <img src='/add-circle.svg' width='40' height='40' />
    </custom-button>

    <div class='search-container'>
      <custom-input placeholder='Buscar' input-id='search' v-model='searchText' />
    </div>

    <div v-if='usersStore.loading'>
      Cargando...
    </div>
    <table v-else class='users-table'>
      <tbody>
      <tr @click='() => editUser(user.id)'
        v-for='(user, index) in filteredUsers'
        :key='index'>
        <td>{{ user.first_name + ' ' + user.last_name }}</td>
        <td>
          <custom-button :onclick='(e) => handleToggleClick(e,user.id,!user.is_active)'
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
  overflow-y: scroll;
}

.users-table tr{
  cursor: pointer;
}

.users-table td {
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

.add-user-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  width: 100%;
  color: inherit !important;

  font-size: 1.3rem;
}
</style>
