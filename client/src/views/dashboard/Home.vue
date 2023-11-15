<script setup>
import CustomButton from '../../components/CustomButton.vue'
import { onMounted, onUnmounted, ref } from 'vue'
import { useHomeStore } from '../../stores/home'
import CustomInput from '../../components/CustomInput.vue'

const searchText = ref('')
const homeStore = useHomeStore()

let interval

onMounted(() => {
  homeStore.getAulas()
  interval = setInterval(() => {
    homeStore.getAulas()
  }, 10000)
})

onUnmounted(() => {
  clearInterval(interval)
})

const getDateDiff = (date) => {
  const minutes = ((new Date() - new Date(date)) / 1000 / 60) % 60
  const hours = ((new Date() - new Date(date)) / 1000 / 60 / 60) % 24

  const formattedMinutes = minutes < 10 ? `0${Math.floor(minutes)}` : Math.floor(minutes)
  const formattedHours = hours < 10 ? `0${Math.floor(hours)}` : Math.floor(hours)

  return `Hace ${formattedHours}:${formattedMinutes} hs`
}
</script>

<template>
  <div class='home-container'>
    <div class='search-container'>
      <custom-input placeholder='Buscar' input-id='search' v-model='searchText' />
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
        <td v-if='aula.has_fotosensible'>{{ aula.estado ? getDateDiff(aula.from) : '' }}</td>
        <td v-if='aula.has_fotosensible && aula.has_rele'>
          <custom-button :onclick='() => homeStore.toggleAula(aula.id)'
                         :theme='aula.estado ? "secondary" : "primary"'>
            {{ aula.estado ? 'Apagar' : 'Encender' }}
          </custom-button>
        </td>
        <td v-else-if='aula.has_fotosensible'> Falta relé</td>

        <td colspan='2' v-if='!aula.has_fotosensible'>Falta relé y sensor</td>
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
  width: auto;
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
