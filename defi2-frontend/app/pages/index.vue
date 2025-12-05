<template>
  <div class="min-h-screen flex flex-col">
    <!-- Hero Section -->
    <div class="relative bg-emerald-900 overflow-hidden">
      <div class="absolute inset-0">
        <img class="w-full h-full object-cover opacity-30" src="/forest-bg.webp" alt="Forest background" onerror="this.style.display='none'" />
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-900 to-emerald-800 mix-blend-multiply" />
      </div>
      <div class="relative max-w-7xl mx-auto py-24 px-4 sm:py-32 sm:px-6 lg:px-8">
        <h1 class="text-4xl font-extrabold tracking-tight text-white sm:text-5xl lg:text-6xl">
          Agissez pour la planète, <br class="hidden sm:block" />
          <span class="text-emerald-400">une mission à la fois.</span>
        </h1>
        <p class="mt-6 text-xl text-emerald-100 max-w-3xl">
          Rejoignez une communauté engagée, formez votre tribu et accomplissez des défis quotidiens pour réduire votre empreinte carbone. Chaque geste compte !
        </p>
        <div class="mt-10 max-w-sm sm:flex sm:max-w-none">
          <div class="space-y-4 sm:space-y-0 sm:mx-auto sm:inline-grid sm:grid-cols-2 sm:gap-5">
            <button @click="openPanel('register')" class="flex items-center justify-center px-4 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-emerald-900 bg-white hover:bg-emerald-50 sm:px-8">
              Rejoindre l'aventure
            </button>
            <button @click="openPanel('login')" class="flex items-center justify-center px-4 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-emerald-600 bg-opacity-60 hover:bg-opacity-70 sm:px-8">
              Déjà membre ?
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="py-16 bg-white overflow-hidden lg:py-24">
      <div class="relative max-w-xl mx-auto px-4 sm:px-6 lg:px-8 lg:max-w-7xl">
        <div class="relative">
          <h2 class="text-center text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Pourquoi participer ?
          </h2>
          <p class="mt-4 max-w-3xl mx-auto text-center text-xl text-gray-500">
            Le changement climatique est un défi collectif. Nous rendons l'action écologique ludique, sociale et gratifiante.
          </p>
        </div>

        <div class="relative mt-12 lg:mt-24 lg:grid lg:grid-cols-3 lg:gap-8">
          <div class="mt-10 lg:mt-0">
            <div class="flex items-center justify-center h-12 w-12 rounded-md bg-emerald-500 text-white mx-auto">
              <!-- Heroicon name: outline/globe-alt -->
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
              </svg>
            </div>
            <div class="mt-5">
              <h3 class="text-lg leading-6 font-medium text-gray-900 text-center">Impact Réel</h3>
              <p class="mt-2 text-base text-gray-500 text-center">
                Visualisez les kilos de CO2 économisés grâce à vos actions.
              </p>
            </div>
          </div>

          <div class="mt-10 lg:mt-0">
            <div class="flex items-center justify-center h-12 w-12 rounded-md bg-emerald-500 text-white mx-auto">
              <!-- Heroicon name: outline/users -->
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
            <div class="mt-5">
              <h3 class="text-lg leading-6 font-medium text-gray-900 text-center">Jeu en Équipe</h3>
              <p class="mt-2 text-base text-gray-500 text-center">
                Créez votre tribu, invitez vos amis et grimpez dans le classement.
              </p>
            </div>
          </div>

          <div class="mt-10 lg:mt-0">
            <div class="flex items-center justify-center h-12 w-12 rounded-md bg-emerald-500 text-white mx-auto">
              <!-- Heroicon name: outline/lightning-bolt -->
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div class="mt-5">
              <h3 class="text-lg leading-6 font-medium text-gray-900 text-center">Défis Variés</h3>
              <p class="mt-2 text-base text-gray-500 text-center">
                Des missions simples et amusantes pour adopter des habitudes durables.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { openPanel } = useAuthUI();
</script>
