<template>
  <div class="bg-white rounded-3xl shadow-lg border border-gray-100 p-12 flex flex-col justify-center items-center text-center lg:col-span-2 relative overflow-hidden">
    <div class="absolute top-0 right-0 -mt-4 -mr-4 w-32 h-32 bg-green-50 rounded-full blur-2xl opacity-60"></div>
    <div class="absolute bottom-0 left-0 -mb-4 -ml-4 w-32 h-32 bg-indigo-50 rounded-full blur-2xl opacity-60"></div>
    
    <h2 class="text-3xl font-extrabold text-gray-900 mb-4">Vous n'avez pas encore de tribu 🥷 !</h2>
    <p class="text-lg text-gray-600 max-w-2xl">Rejoignez un village numérique résistant ! Ensemble, on va plus loin !</p>
    <p class="text-lg text-gray-600 mb-10 max-w-2xl">David contre Goliath, Astérix contre l'Empire Numérique</p>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-3xl">
      <!-- Create Option -->
      <div v-if="!isCreating" @click="isCreating = true" class="group bg-gray-50 hover:bg-green-50 border-2 border-dashed border-gray-300 hover:border-green-400 rounded-2xl p-8 transition-all cursor-pointer flex flex-col items-center">
        <div class="w-16 h-16 bg-white rounded-full shadow-sm flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
          <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">🏡 Créer une tribu</h3>
        <p class="text-gray-500 text-sm">Fondez votre village, invitez vos compagnons et partez l'assaut contre l'Empire Numérique</p>
      </div>

      <div v-else class="bg-green-50 border-2 border-green-400 rounded-2xl p-8 flex flex-col items-center transition-all">
        <div class="w-16 h-16 bg-white rounded-full shadow-sm flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-4">Nom de votre tribu</h3>
        <div class="w-full space-y-3">
          <input v-model="newTribeName" type="text" placeholder="Ex: Les Red Code Chili Peppers" class="w-full px-4 py-2 rounded-lg border-gray-300 focus:ring-green-500 focus:border-green-500 text-center" @keyup.enter="createTribe">
          <div class="flex gap-2">
            <button @click="isCreating = false" class="flex-1 bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors font-medium">Annuler</button>
            <button @click="createTribe" class="flex-1 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors font-medium">Confirmer</button>
          </div>
        </div>
      </div>

      <!-- Join Option -->
      <div class="bg-gray-50 border border-gray-200 rounded-2xl p-8 flex flex-col items-center">
        <div class="w-16 h-16 bg-white rounded-full shadow-sm flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-4">🏡 Rejoindre un village</h3>
        <div class="w-full space-y-3">
          <input v-model="joinCode" type="text" placeholder="Saisissez le sésame 🥷" class="w-full px-4 py-2 rounded-lg border-gray-300 focus:ring-indigo-500 focus:border-indigo-500 text-center" @keyup.enter="joinTribe">
          <button @click="joinTribe" class="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors font-medium">Rejoindre</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const isCreating = ref(false);
const newTribeName = ref('');
const joinCode = ref('');

const emit = defineEmits(['create', 'join']);

const createTribe = () => {
  if (newTribeName.value.trim()) {
    emit('create', newTribeName.value.trim());
  }
};

const joinTribe = () => {
  if (joinCode.value.trim()) {
    emit('join', joinCode.value.trim());
  }
};
</script>
