<template>
  <div class='wrapper'>
    <header>
      <h1>{{ title }}</h1>
    </header>
    <main>
      <RouterView />
    </main>
    <nav>
      <RouterLink to='/stats' class='nav-link'>
        <img class='nav-logo' alt='Logo de un foco' src='/graphic_icon.png' />
      </RouterLink>
      <RouterLink to='/dashboard' class='nav-link'>
        <img class='nav-logo' alt='Logo de un foco' src='/lightbulb_icon.png' />
      </RouterLink>
      <button class='nav-link' @click='toggleMenu'>
        <img class='nav-logo' alt='Logo de un foco' src='/menu_icon.png' />
      </button>

    </nav>
    <div class='menu-overlay' @click='toggleMenu' v-if='showMenu'>
    </div>
    <transition name='slide-in'>
      <div v-if='showMenu' class='menu' ref='menu' @touchstart='handleTouchStart' @touchmove='handleTouchMove'
           @touchend='handleTouchEnd'>
        <hr />
        <ul>
          <li>
            <RouterLink to='/usuarios'>Usuarios</RouterLink>
          </li>
          <li>
            <RouterLink to='/aulas'>Crear aula</RouterLink>
          </li>
          <li>
            <CustomButton class='logout-button' variant='link' @click='logout'>Cerrar sesión</CustomButton>
          </li>
        </ul>
      </div>

    </transition>
  </div>

</template>

<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import CustomButton from '../components/CustomButton.vue'
import { computed, reactive, ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const router = useRouter()

if (!authStore.isAuthenticated) {
  router.push('/login')

}
const showMenu = ref(false)
const startY = ref(0)
const currentY = ref(0)

const menu = ref(null)

function toggleMenu() {
  showMenu.value = !showMenu.value
}

function handleTouchStart(event) {
  startY.value = event.touches[0].clientY
}

function handleTouchMove(event) {
  const touchY = event.touches[0].clientY
  const diffY = touchY - startY.value
  if (diffY > 0) { // Swipe Down
    if (menu.value) {
      menu.value.style.transform = `translateY(${diffY}px)`
      console.log(diffY)
    }
    console.log(diffY)
  }
}

function handleTouchEnd() {
  if (startY.value - currentY.value > 50) { // Adjust this value as needed
    showMenu.value = false
  } else {
    if (menu.value) menu.value.style.transform = `translateY(0)`
  }
}

function logout() {
  authStore.logout()
  router.push('/login')
}

const route = useRoute()

const title = computed(() => {
  switch (route.name) {
    case 'stats':
      return 'Estadísticas'
    case 'home':
      return 'Gestión de Luces'
    case 'usuarios':
      return 'Usuarios'
    case 'aulas':
      return 'Aulas'
    default:
      return 'Gestión de Luces'
  }
})

</script>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100vh;
  width: 100%;
}

main{
  height: 100%;
  background-color: #eaeaea;
}

header {
  display: flex;
  width: 100%;
  justify-content: center;
  color: white;
  padding: .5rem;
  background-color: #193250;
}

nav {
  font-size: 12px;
  background-color: #386aa4;
  padding: .5rem 1rem;
  display: flex;
  justify-content: space-between;
  width: 100%;
}

nav .nav-logo {
  width: 50px;
  height: 50px;
}

nav button {
  background-color: transparent;
  border: none;
  cursor: pointer;
}

.slide-in-enter-active, .slide-in-leave-active {
  transition: transform 0.5s;
}

.slide-in-enter-from, .slide-in-leave-to {
  transform: translateY(100%);
}

.slide-in-enter-to, .slide-in-leave-from {
  transform: translateY(0);
}

.menu-overlay {
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.66);
  height: 100vh;
  position: fixed;

  bottom: 0;
  width: 100%;
  max-width: 768px;
}

.menu {
  z-index: 2;
  bottom: 0;
  width: 100%;
  max-width: 768px;
  position: fixed;
  background-color: #fff;
  padding: 1rem 2rem 4rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: transform 0.3s;
  gap: 1rem;
}

.menu hr {
  width: 6rem;
  border: 3px solid #b8bdbb;
  border-radius: 99999px;
  align-self: center;
}

.menu ul {
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: .5rem;
}

.menu li {
  font-size: 1.5rem;
  list-style-type: none;
  margin: 0;

}


.menu li a {
  color: inherit;
}

.logout-button{
  font-size: 1.5rem;
}
</style>
