<script setup>
import CustomInput from '../../components/CustomInput.vue'
import CustomButton from '../../components/CustomButton.vue'
import { useAulasStore } from '../../stores/aulas'
import { onMounted, onRenderTracked, ref } from 'vue'
import { useRouter } from 'vue-router'

const aulasStore = useAulasStore()

const router = useRouter()
const aulaData = ref(null)

const createInformation = ref({
  numero: 0,
  ip: ''
})

onMounted(() => {
  aulasStore.getAulas()
})

async function handleSubmit(e) {
  e.preventDefault()
  const result = await aulasStore.createAula(createInformation.value)

  if(result){
    await router.push('/dashboard/')
  }
}

const aulaId = ref(null)

function handleSelectAula(id) {
  aulaId.value = parseInt(id)

  const aulaInformation = aulasStore.aulas.find(aula => aula.id === aulaId.value)
  aulaData.value = {
    numero: aulaInformation.numero,
    ip: aulaInformation.ip
  }
}

async function handleEditSubmit() {
  const success = await aulasStore.editAula(aulaId.value, aulaData.value)

  if (success) {
    aulaId.value = null
    aulaData.value = null
  }
}

async function handleDeleteAula(e){
  e.stopPropagation()

  const success = await aulasStore.deleteAula(aulaId.value)

  if (success) {
    aulaId.value = null
    aulaData.value = null
  }
}


onRenderTracked(() => {
  console.log(aulaId.value)
  console.log(aulaData.value)
  console.log(aulasStore.aulas)
})
</script>

<template>
  <div class='aulas-container'>
    <div v-if='!aulasStore.loading' class='create-aula-card'>
      <h2>Crear aula</h2>
      <form :onsubmit='handleSubmit ' class='create-form'>
        <custom-input input-id='numero' v-model.number='createInformation.numero' label='Número del aula' type='number'
                      required />
        <custom-input input-id='ip' v-model='createInformation.ip' label='IP del Arduino asignado' required />
        <custom-button>Agregar</custom-button>
      </form>
    </div>
    <div v-if='!aulasStore.loading' class='edit-aula-card'>
      <h2>Editar o eliminar aula</h2>
      <form :onsubmit='() => handleEditSubmit()' class='edit-form'>
        <label class='select-label'>
          Seleccione el aula
          <select name='id' :value='aulaId' :onchange='(e) => handleSelectAula(e.target.value)'>
            <option disabled selected>
            </option>
            <option v-for='aula in aulasStore.aulas' :value='aula.id'>Aula {{ aula.numero }}</option>
          </select>
        </label>
        <div v-if='aulaId && aulaData'>

          <custom-input :disabled='!aulaId' input-id='numero' v-model.number='aulaData.numero' label='Nuevo número'
                        type='number'
                        required />
          <custom-input :disabled='!aulaId' input-id='ip' v-model='aulaData.ip' label='Nuevo IP Arduino'
                        required />
          <ul>
            <li>
              Sólo completar los campos “Nuevo número” y “Nuevo IP Arduino” en caso de edición. Si quiere eliminar, sólo
              seleccione el aula.
            </li>
          </ul>
          <div class='button-container'>
            <custom-button type='submit'>Editar</custom-button>
            <custom-button theme='gray' :onclick='handleDeleteAula'>Eliminar</custom-button>
          </div>
        </div>
      </form>
    </div>
    <div v-if='aulasStore.loading'>Cargando...</div>
  </div>
</template>

<style scoped>
.aulas-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
}

.create-aula-card, .edit-aula-card {
  display: flex;
  flex-direction: column;
  width: 100%;
  background-color: #f1faf6;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  padding: 1rem;
}

.create-form, .edit-form, .edit-form > div {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
  justify-content: center;
  gap: .5rem;
}

.select-label {
  display: flex;
  flex-direction: column;
}

.button-container {
  display: flex;
  flex-direction: row;
  width: 234px;
  justify-content: space-between;
}

.edit-form ul {
  width: 300px;
}

</style>
