<template>
  <button :disabled='disabled' :class='computedClass' @click='handleClick'>
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'CustomButton',
  props: {
    class: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    theme: {
      type: String,
      default: 'primary' // possible values: 'primary', 'secondary'
    },
    variant: {
      type: String,
      default: 'solid' // possible values: 'solid', 'link'
    }
  },
  computed: {
    computedClass() {
      return [this.theme, this.variant, 'button', this.disabled ? 'disabled' : '',
        this.class]
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
.button {
  cursor: pointer;
  outline: none;
  border: none;
  font-size: 1rem;
  padding: 0;
}

.solid {
  border-radius: .5rem;
  padding: .5rem 1rem;
}

.solid:hover, .solid:active {
  opacity: 0.7;
}

.primary.solid {
  background-color: #386aa4;
  color: white;
}

.primary.link {
  background-color: transparent;
  color: #386aa4;
}

.primary.link:hover,.primary.link:active{
  text-decoration: underline;
  text-underline: #386aa4;
}
</style>
