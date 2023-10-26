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
            <RouterLink to='/login'>Cerrar sesión</RouterLink>
          </li>
        </ul>
      </div>

    </transition>
  </div>

</template>

<script>
import  { RouterLink, RouterView, useRoute } from 'vue-router'
import CustomButton from '../components/CustomButton.vue'
import { computed } from 'vue'

export default {
  name: 'DashboardView',
  components: {
    CustomButton,
    RouterLink,
    RouterView
  },
  data() {
    return {
      showMenu: false,
      startY: 0,  // Initial touch Y coordinate
      currentY: 0 // Current touch Y coordinate
    }
  },
  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu
    },
    handleTouchStart(event) {
      this.startY = event.touches[0].clientY
    },
    handleTouchMove(event) {
      const touchY = event.touches[0].clientY
      const diffY = touchY - this.startY

      if (diffY > 0) { // Swipe Down
        this.$refs.menu.style.transform = `translateY(${diffY}px)`
      }
    },
    handleTouchEnd() {
      if (this.startY - this.currentY > 50) { // Adjust this value as needed
        this.showMenu = false
      } else {
        this.$refs.menu.style.transform = `translateY(0)`
      }
    }
  },
  setup() {
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

    return {
      title
    }
  }
}
</script>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100vh;
  width: 100%;
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
  margin-top: 2rem;
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


.menu li a{
  color: inherit;
}
</style>
