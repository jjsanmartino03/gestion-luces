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
      default: 'primary' // possible values: 'primary', 'secondary', 'gray'
    },
    variant: {
      type: String,
      default: 'solid' // possible values: 'solid', 'link'
    },
    onclick: {
      type: Function,
      default: () => {
      }
    }
  },
  computed: {
    computedClass() {
      return [this.theme, this.variant, 'button', this.disabled ? 'disabled' : '',
        this.class]
    }
  },
  methods: {
    handleClick(e) {
      if (!this.disabled) {
        this.onclick(e)
      }
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

.button:disabled{
  cursor: not-allowed;
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

.secondary.solid {
  background-color: #c1ff72;
  color: var(--color-text);
}

.gray.solid {
  background-color: #828589;
  color: white;
}

.primary.link {
  background-color: transparent;
  color: #386aa4;
}

.primary.link:hover, .primary.link:active {
  text-decoration: underline;
  text-underline: #386aa4;
}
</style>
