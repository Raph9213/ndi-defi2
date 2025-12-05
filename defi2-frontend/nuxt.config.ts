// https://nuxt.com/docs/api/configuration/nuxt-config
// Declare `process` for TypeScript in environments without @types/node
declare const process: any
export default defineNuxtConfig({
  future: {
    compatibilityVersion: 4
  },
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  // Vite dev server options — ensure custom hosts are allowed when Nuxt delegates to Vite
  vite: {
    server: {
      allowedHosts: ['ndi.raph9213.xyz', 'localhost']
    }
  },
  runtimeConfig: {
    public: {
      API_URL: process.env.API_URL || 'http://localhost:5000'
    }
  }
})