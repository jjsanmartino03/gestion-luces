<script setup>
</script>

<template>
  <main>
    <h1>
      Gestor de luces UTN San Francisco
    </h1>
    <img alt='Gestión logo' class='logo' src='/logo-alt.png' />
    <p>Bienvenidos!</p>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 768px;
  width: 100%;
  background-color: #eaeaea;
  height: 100vh;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

h1 {
  text-align: center;
}

.logo {
  width: 100%;
  max-width: 200px;
  margin: 0 auto;
  display: block;
  border-radius: 2rem;
}

p {
  font-size: 1.3rem;
}
</style>

<script>
export default {
  name: 'WelcomeView',
  components: {},
  data() {
    return {}
  },
  methods: {},
  created() {
    setTimeout(() => {
      this.$router.push('/login')
    }, 3000)
  }
}
</script>
