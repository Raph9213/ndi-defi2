<template>
  <div class="p-10 flex flex-col items-center justify-center min-h-screen gap-4 bg-gray-50 "> <!--dark:bg-gray-900-->
    <h1 class="text-4xl font-bold text-primary-500">
      Nuxt UI + Tailwind CSS
    </h1>
    <p class="text-gray-600 dark:text-gray-300">
      Tailwind CSS est déjà inclus avec Nuxt UI !
    </p>
    
    <div class="flex gap-4">
      <button class="px-4 py-2 text-white bg-green-500 rounded-lg hover:bg-green-600 transition-colors flex items-center gap-2">
        <span class="i-heroicons-check w-5 h-5" />
        Bouton Standard
      </button>
      
      <button class="px-4 py-2 text-red-500 bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors">
        Bouton HTML + Tailwind
      </button>
    </div>
  </div>
</template>
