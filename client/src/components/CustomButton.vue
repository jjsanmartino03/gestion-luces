<template>
  <button :class='computedClass' @click='handleClick'>
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'CustomButton',
  props: {
    theme: {
      type: String,
      default: 'light' // possible values: 'light', 'dark'
    },
    variant: {
      type: String,
      default: 'primary' // possible values: 'primary', 'secondary'
    }
  },
  computed: {
    computedClass() {
      return [this.theme, this.variant]
    }
  },
  methods: {
    handleClick() {
      this.$emit('click')
    }
  }
}
</script>

<style scoped>
/* Light theme */
button {
  cursor: pointer;
}

.light.primary {
  background-color: #007BFF;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.light.secondary {
  background-color: #6C757D;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

/* Dark theme */
.dark.primary {
  background-color: #001F3F;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.dark.secondary {
  background-color: #343A40;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}
</style>
