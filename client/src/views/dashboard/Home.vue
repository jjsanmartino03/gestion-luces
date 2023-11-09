<script setup>
import CustomButton from '../../components/CustomButton.vue'
import Input from '../../components/CustomInput.vue'
import { onMounted, ref } from 'vue'
import { useHomeStore } from '../../stores/home'

const searchText = ref('')
const homeStore = useHomeStore()

onMounted(() => {
  homeStore.getAulas()
})

function turnOn(aulaId) {
  alert('Encender ' + aulaId)
}

function turnOff(aulaId) {
  alert('Apagar ' + aulaId)
}

</script>

<template>
  <div class='home-container'>
    <div class='search-container'>
      <Input placeholder='Buscar' input-id='search' v-model='searchText' />
    </div>

    <div v-if='homeStore.loading'>
      Cargando...
    </div>
    <table v-else class='aulas-table'>
      <tbody>
      <tr
        v-for='(aula, index) in homeStore.aulas.filter(aula => aula.nombre.toLowerCase().match(searchText.toLowerCase()))'
        :key='index'>
        <td>{{ aula.nombre }}</td>
        <td>{{ aula.from }}</td>
        <td>
          <custom-button @click='aula.estado === 0 ? turnOn(aula.nombre) : turnOff(aula.nombre)'
                         :theme='aula.estado === 0 ? "secondary" : "gray"'>
            {{ aula.estado === 0 ? 'Encender' : 'Apagar' }}
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

.aulas-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #ddd;
  font-size: 18px;
  text-align: center;
}

.aulas-table td {
  width: 33%;
  padding: .5rem 1rem;
  border-top: 2px solid #828589;
}

.aulas-table tr:last-child td {
  border-bottom: 2px solid #828589; /* Increase space for all rows except the last one */
}

.search-container {
  align-self: center;
  width: 75%;
}
</style>
