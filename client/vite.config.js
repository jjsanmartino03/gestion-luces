import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  mode: 'development',
  base: '/',
  plugins: [
    vue(),
    vueJsx(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'Gestión de Luces - UTN San Francisco',
        short_name: 'Luces',
        theme_color: '#ffffff',
        icons: [
          {
            src: 'logo500x500.png',
            sizes: '500x500',
            type: 'image/png'
          }]

      }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
