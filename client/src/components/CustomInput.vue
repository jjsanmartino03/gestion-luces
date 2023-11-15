<template>
  <div class='input-container'>
    <label v-if='label' :for='inputId'>{{ label }}</label>
    <input
      :id='inputId'
      :type='type'
      :value='modelValue'
      :required='required'
      @input="$emit('update:modelValue', $event.target.value)"
      :placeholder='placeholder'
    />
  </div>
</template>

<script>
export default {
  name: 'CustomInput',
  props: {
    required: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: ''
    },
    modelValue: {
      type: String,
      default: ''
    },
    inputId: {
      type: String,
      required: true
    },
    placeholder: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'text'
    }
  },
  emits: ['update:modelValue']
}
</script>

<style scoped>
.input-container {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input {
  background-color: #b2b2b2;
  color: white;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: .5rem;
  font-size: 1rem;
}
</style>
