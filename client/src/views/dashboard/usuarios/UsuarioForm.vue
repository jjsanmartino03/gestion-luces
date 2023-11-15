<script setup>
import CustomButton from '../../../components/CustomButton.vue'
import CustomInput from '../../../components/CustomInput.vue'
import { ref } from 'vue'

const props = defineProps({
  user: {
    type: Object,
    required: false
  },
  handleSubmit: {
    type: Function,
    required: true
  }
})

console.log(props.user)


const inputs = ref(props.user || {
  username: '',
  password: '',
  first_name: '',
  last_name: '',
  email: '',
  is_staff: false
})


async function handleSubmit(e) {
  e.preventDefault()

  props.handleSubmit(inputs.value)
}

</script>

<template>
  <form :onsubmit='handleSubmit'>
    <custom-input input-id='username' v-model='inputs.username' placeholder='Nombre de usuario' required />
    <custom-input input-id='password' v-model='inputs.password' placeholder='Contraseña' required type='password' />
    <custom-input input-id='first_name' v-model='inputs.first_name' placeholder='Nombre' required />
    <custom-input input-id='last_name' v-model='inputs.last_name' placeholder='Apellido' required />
    <custom-input input-id='email' v-model='inputs.email' placeholder='Email' type='email' required />
    <div class='checkbox-container'>
      <p class='radio-title'>Administrador</p>
      <label class='yes-label'>
        <input type='radio' v-model='inputs.is_staff' id='is_staff' name='is_staff' :value='true' /> Si
      </label>
      <label>
        <input type='radio' id='is_staff' name='is_staff' v-model='inputs.is_staff' :value='false' /> No
      </label>
    </div>
    <CustomButton theme='primary' type='submit' variant='solid'>
      Guardar
    </CustomButton>
  </form>
</template>

<style scoped>
form {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: .5rem
}

.checkbox-container {
  display: flex;
  flex-direction: column;
  gap: .3rem;
  margin-top: .5rem;
  padding: .5rem;
  border: solid 2px #676767;
  border-radius: 1rem;

  position: static;
  color: #676767;

}

.yes-label {
  margin-top: -1.5rem;
}

.radio-title {
  position: relative;
  top: -20px;
  align-self: center;
  background-color: #eaeaea;
  width: 150px;
  text-align: center;
}
</style>
