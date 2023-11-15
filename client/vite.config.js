import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: '0.0.0.0'
  },
  mode: 'development', base: '/', plugins: [vue(), vueJsx(), VitePWA({
    registerType: 'autoUpdate', devOptions: {
      enabled: true
    }, manifest: {
      start_url: '/',
      name: 'Gestión de Luces - UTN San Francisco',
      description: 'Aplicación para la gestión de luces de UTN',
      short_name: 'Luces',
      theme_color: '#ffffff',
      icons: [{
        src: 'logo512x512.png', sizes: '512x512', type: 'image/png'
      }, {
        src: 'logo192x5192.png', sizes: '192x192', type: 'image/png'
      }, {
        src: 'maskable_icon.png',
        sizes: '512x512',
        type: 'image/png',
        purpose: 'any maskable'
      },
        {
          src: 'maskable_icon.png',
          sizes: '144x144',
          type: 'image/png',
          purpose: 'any maskable'
        }]
    }
  })], resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
