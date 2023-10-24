<script setup>
import {RouterLink, RouterView} from 'vue-router'
</script>

<template>
  <!--  <header>
      <img alt="Gestión logo" class="logo" src="/logo500x500.png" width="40" height="40"/>

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
      </nav>
    </header>-->

  <RouterView/>
</template>

<style scoped>
header {
  display: flex;
  width: 100%;
  justify-content: space-between;
  line-height: 1.5;
  max-height: 100vh;
  border-bottom: black 1px solid;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
  }

  .logo {
    margin: 0 2rem 0 0;
    border-radius: 9999px;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
